"""Read-only hybrid retrieval over the EUROMOD legislation database."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal, Sequence

from psycopg import Connection
from psycopg.rows import dict_row

SearchMode = Literal["hybrid", "full_text", "vector"]


@dataclass(frozen=True, slots=True)
class SearchHit:
    chunk_id: str
    version_id: str
    sequence: int
    country: str
    citation: str
    title: dict[str, str]
    language: str
    authenticity: str
    validity: str
    version_status: str
    context_header: str
    content: str
    score: float
    full_text_rank: int | None
    full_text_score: float | None
    full_text_contribution: float
    vector_rank: int | None
    vector_distance: float | None
    vector_contribution: float


_BASE_CANDIDATE = """
candidate AS MATERIALIZED (
    SELECT c.id AS chunk_id, c.tsv, c.search_config, c.unit_text_id, c.seq,
           t.version_id, t.lang, t.authenticity,
           v.validity, v.version_status,
           u.citation, i.title, j.code AS country
    FROM chunks c
    JOIN unit_texts t          ON t.id = c.unit_text_id
    JOIN legal_unit_versions v ON v.id = t.version_id
    JOIN legal_units u         ON u.id = v.legal_unit_id
    JOIN instruments i         ON i.id = u.instrument_id
    JOIN jurisdictions j       ON j.id = i.jurisdiction_id
    -- A country's scope includes its child jurisdictions (Spain's autonomous
    -- communities, ADR 0003); a child code narrows to that region alone.
    WHERE (%(country)s::text IS NULL OR j.code = upper(%(country)s)
           OR j.parent_id = (SELECT id FROM jurisdictions WHERE code = upper(%(country)s)))
      AND (%(as_of)s::date IS NULL OR v.validity @> %(as_of)s::date)
      AND (%(languages)s::text[] IS NULL OR t.lang = ANY(%(languages)s::text[]))
),
"""

_FTS_CTE = """
fts AS (
    SELECT chunk_id,
           row_number() OVER (ORDER BY rank_score DESC, chunk_id) AS rank,
           rank_score
    FROM (
        SELECT chunk_id,
               ts_rank_cd(tsv, websearch_to_tsquery(search_config, %(query)s), 32) AS rank_score
        FROM candidate
        WHERE tsv @@ websearch_to_tsquery(search_config, %(query)s)
    ) ranked_fts
    ORDER BY rank_score DESC
    LIMIT %(candidate_limit)s
)
"""

_VECTOR_CTE = """
vec AS (
    SELECT chunk_id,
           row_number() OVER (ORDER BY distance, chunk_id) AS rank,
           distance
    FROM (
        SELECT e.chunk_id, e.embedding <=> %(query_vector)s::halfvec AS distance
        FROM embeddings e
        JOIN candidate USING (chunk_id)
        WHERE e.model_id = %(model_id)s
        ORDER BY e.embedding <=> %(query_vector)s::halfvec
        LIMIT %(candidate_limit)s
    ) ranked_vec
)
"""

_RESULT_COLUMNS = """
SELECT c.chunk_id::text, c.version_id::text, c.seq AS sequence,
       c.country, c.citation, c.title, c.lang AS language,
       c.authenticity, c.validity::text, c.version_status,
       ch.context_header, ch.content,
       {score}::float8 AS score,
       {fts_rank} AS full_text_rank,
       {fts_score}::float8 AS full_text_score,
       {fts_contribution}::float8 AS full_text_contribution,
       {vec_rank} AS vector_rank,
       {vec_distance}::float8 AS vector_distance,
       {vec_contribution}::float8 AS vector_contribution
FROM {ranking}
JOIN candidate c USING (chunk_id)
JOIN chunks ch ON ch.id = c.chunk_id
ORDER BY score DESC, c.chunk_id
LIMIT %(limit)s
"""


def _search_sql(mode: SearchMode) -> str:
    if mode == "hybrid":
        score = "coalesce(1.0 / (%(rrf_k)s + f.rank), 0) + coalesce(1.0 / (%(rrf_k)s + v.rank), 0)"
        result = _RESULT_COLUMNS.format(
            score=score,
            fts_rank="f.rank",
            fts_score="f.rank_score",
            fts_contribution="coalesce(1.0 / (%(rrf_k)s + f.rank), 0)",
            vec_rank="v.rank",
            vec_distance="v.distance",
            vec_contribution="coalesce(1.0 / (%(rrf_k)s + v.rank), 0)",
            ranking="fts f FULL OUTER JOIN vec v USING (chunk_id)",
        )
        return "WITH " + _BASE_CANDIDATE + _FTS_CTE + ",\n" + _VECTOR_CTE + result
    if mode == "full_text":
        result = _RESULT_COLUMNS.format(
            score="1.0 / (%(rrf_k)s + f.rank)",
            fts_rank="f.rank",
            fts_score="f.rank_score",
            fts_contribution="1.0 / (%(rrf_k)s + f.rank)",
            vec_rank="NULL::bigint",
            vec_distance="NULL::double precision",
            vec_contribution="0.0",
            ranking="fts f",
        )
        return "WITH " + _BASE_CANDIDATE + _FTS_CTE + result
    if mode == "vector":
        result = _RESULT_COLUMNS.format(
            score="1.0 / (%(rrf_k)s + v.rank)",
            fts_rank="NULL::bigint",
            fts_score="NULL::real",
            fts_contribution="0.0",
            vec_rank="v.rank",
            vec_distance="v.distance",
            vec_contribution="1.0 / (%(rrf_k)s + v.rank)",
            ranking="vec v",
        )
        return "WITH " + _BASE_CANDIDATE + _VECTOR_CTE + result
    raise ValueError(f"Unsupported search mode: {mode}")


def search(
    conn: Connection,
    *,
    query: str,
    mode: SearchMode,
    query_vector: str | None,
    country: str | None = None,
    as_of: date | None = None,
    languages: Sequence[str] | None = None,
    model_id: int = 1,
    limit: int = 8,
    candidate_limit: int = 50,
    rrf_k: int = 60,
) -> list[SearchHit]:
    """Search legislation and return the component ranks used for each result."""
    if not query.strip():
        raise ValueError("query must not be empty")
    if mode in {"hybrid", "vector"} and query_vector is None:
        raise ValueError(f"{mode} search requires a query vector")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")

    params = {
        "query": query,
        "query_vector": query_vector,
        "country": country,
        "as_of": as_of,
        "languages": list(languages) if languages else None,
        "model_id": model_id,
        "limit": min(50, limit * 4),
        "candidate_limit": max(candidate_limit, limit),
        "rrf_k": rrf_k,
    }
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(_search_sql(mode), params)
        hits = [SearchHit(**row) for row in cursor.fetchall()]

    deduplicated: list[SearchHit] = []
    seen_versions: set[tuple[str, int]] = set()
    for hit in hits:
        identity = (hit.version_id, hit.sequence)
        if identity in seen_versions:
            continue
        seen_versions.add(identity)
        deduplicated.append(hit)
        if len(deduplicated) == limit:
            break
    return deduplicated


def get_chunk(conn: Connection, chunk_id: str) -> SearchHit | None:
    """Fetch one citable chunk and its provenance without running a search."""
    query = """
        SELECT c.id::text AS chunk_id, t.version_id::text AS version_id,
               c.seq AS sequence, j.code AS country, u.citation, i.title,
               t.lang AS language, t.authenticity, v.validity::text,
               v.version_status, c.context_header, c.content,
               0.0::float8 AS score, NULL::bigint AS full_text_rank,
               NULL::float8 AS full_text_score, 0.0::float8 AS full_text_contribution,
               NULL::bigint AS vector_rank, NULL::float8 AS vector_distance,
               0.0::float8 AS vector_contribution
        FROM chunks c
        JOIN unit_texts t          ON t.id = c.unit_text_id
        JOIN legal_unit_versions v ON v.id = t.version_id
        JOIN legal_units u         ON u.id = v.legal_unit_id
        JOIN instruments i         ON i.id = u.instrument_id
        JOIN jurisdictions j       ON j.id = i.jurisdiction_id
        WHERE c.id = %(chunk_id)s::uuid
    """
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(query, {"chunk_id": chunk_id})
        row = cursor.fetchone()
        return SearchHit(**row) if row else None
