"""Read-only hybrid retrieval over the EUROMOD legislation database."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from typing import Literal

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
    source_trust_class: str
    context_header: str
    content: str
    score: float
    full_text_rank: int | None
    full_text_score: float | None
    full_text_contribution: float
    vector_rank: int | None
    vector_distance: float | None
    vector_contribution: float


DEFAULT_MODEL_SQL = "SELECT id FROM embedding_models WHERE is_default ORDER BY id LIMIT 1"

# The database's search_chunks() (Nomotheca-RAG/db/schema.sql) — the one
# hybrid search the workflow, the eval and the review UI use too: live version
# on as_of, Country Reports (trust class 'context') excluded, OR-of-terms FTS,
# RRF plus the vector top-3 slot, vector leg ranked over the filtered set.
_SEARCH_SQL = """
SELECT ch.id::text AS chunk_id, t.version_id::text AS version_id, ch.seq AS sequence,
       j.code AS country, u.citation, i.title, t.lang AS language,
       t.authenticity, v.validity::text, v.version_status, i.source_trust_class,
       ch.context_header, ch.content,
       s.score,
       s.fts_rank AS full_text_rank,
       s.fts_score AS full_text_score,
       coalesce(1.0 / (60 + s.fts_rank), 0)::float8 AS full_text_contribution,
       s.vec_rank AS vector_rank,
       s.vec_distance AS vector_distance,
       coalesce(1.0 / (60 + s.vec_rank), 0)::float8 AS vector_contribution
FROM search_chunks(
        %(query)s, %(query_vector)s::halfvec(1024), %(model_id)s,
        CASE WHEN %(country)s::text IS NULL THEN NULL ELSE jurisdiction_tree(%(country)s) END,
        %(languages)s::text[], %(as_of)s::date, %(candidates)s, %(use_fts)s) s
JOIN chunks ch             ON ch.id = s.chunk_id
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
ORDER BY s.score DESC, s.chunk_id
"""


def default_model_id(conn: Connection) -> int:
    """The embedding model the corpus is searched with (embedding_models.is_default)."""
    row = conn.execute(DEFAULT_MODEL_SQL).fetchone()
    if row is None:
        raise ValueError("no default embedding model in embedding_models")
    return int(row[0])


def search(
    conn: Connection,
    *,
    query: str,
    mode: SearchMode,
    query_vector: str | None,
    model_id: int,
    country: str | None = None,
    as_of: date | None = None,
    languages: Sequence[str] | None = None,
    limit: int = 8,
) -> list[SearchHit]:
    """Search citable legislation and return the component ranks of each result.

    ``model_id`` must be the model that encoded ``query_vector``.
    """
    if not query.strip():
        raise ValueError("query must not be empty")
    if mode not in {"hybrid", "full_text", "vector"}:
        raise ValueError(f"Unsupported search mode: {mode}")
    if mode in {"hybrid", "vector"} and query_vector is None:
        raise ValueError(f"{mode} search requires a query vector")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")

    params = {
        "query": query,
        "query_vector": query_vector if mode != "full_text" else None,
        "model_id": model_id,
        "country": country,
        "as_of": as_of,
        "languages": list(languages) if languages else None,
        # Room for the per-(version, seq) de-duplication below.
        "candidates": min(50, limit * 4),
        "use_fts": mode != "vector",
    }
    with conn.cursor(row_factory=dict_row) as cursor:
        cursor.execute(_SEARCH_SQL, params)
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
               v.version_status, i.source_trust_class, c.context_header, c.content,
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
