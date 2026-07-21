"""Retrieval against the legislation DB (Nomotheca-RAG/db/schema.sql).

Two paths, per Nomotheca-RAG/11_database-model.md §5:
  1. citation fast path — pg_trgm match on legal_units.citation / national_id,
     filtered to the version in force at as_of (the majority case: updates
     start from last year's citation);
  2. hybrid — candidates pre-filtered by as_of/jurisdiction/lang, then
     FTS top-50 || vector top-50 merged by Reciprocal Rank Fusion (k=60),
     the SQL pattern from Nomotheca-RAG/db/demo_queries.sql (f).

The vector leg encodes the query with the real BGE-M3 encoder (model_id 1,
via query_encoder — the ingest package's OpenVINO subprocess) and falls back
to FTS-only when the encoder is unavailable. The demo placeholder embedder
(model_id 99) keeps its embed-in-SQL path via placeholder_embedding().
"""

from __future__ import annotations

import re
from datetime import date

import psycopg
from psycopg.rows import dict_row

from . import query_encoder
from .config import WorkflowConfig
from .schema import RetrievalHit

LANG_BY_COUNTRY = {"FR": "fr", "BE": "fr", "NL": "nl", "ES": "es", "IE": "en", "LT": "lt"}

_CITATION_SQL = """
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status,
       similarity(u.citation, %(cit)s)::float8 AS score
FROM legal_units u
JOIN instruments i        ON i.id = u.instrument_id
JOIN jurisdictions j      ON j.id = i.jurisdiction_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
JOIN unit_texts t         ON t.version_id = v.id
JOIN chunks ch            ON ch.unit_text_id = t.id
WHERE j.code = %(country)s AND t.lang = %(lang)s
  AND v.validity @> %(as_of)s::date
  AND (similarity(u.citation, %(cit)s) > 0.55 OR u.national_id = %(cit)s)
ORDER BY score DESC, ch.seq
LIMIT %(k)s
"""

_HYBRID_SQL_TEMPLATE = """
WITH candidate AS (
  SELECT c.id AS chunk_id, c.tsv, c.search_config
  FROM chunks c
  JOIN unit_texts t          ON t.id = c.unit_text_id
  JOIN legal_unit_versions v ON v.id = t.version_id
  JOIN legal_units u         ON u.id = v.legal_unit_id
  JOIN instruments i         ON i.id = u.instrument_id
  JOIN jurisdictions j       ON j.id = i.jurisdiction_id
  WHERE v.validity @> %(as_of)s::date AND j.code = %(country)s AND t.lang = %(lang)s
),
fts AS (
  SELECT chunk_id,
         row_number() OVER (
           ORDER BY ts_rank_cd(tsv, websearch_to_tsquery(search_config, %(fts_q)s), 32) DESC
         ) AS r
  FROM candidate
  WHERE tsv @@ websearch_to_tsquery(search_config, %(fts_q)s)
  LIMIT 50
){vec_cte}
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status,
       {score_expr} AS score
FROM {joined}
JOIN chunks ch             ON ch.id = chunk_id
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
ORDER BY score DESC
LIMIT %(k)s
"""

_VEC_CTE = """,
vec AS (
  SELECT e.chunk_id,
         row_number() OVER (ORDER BY e.embedding <=> placeholder_embedding(%(q)s)) AS r
  FROM embeddings e JOIN candidate USING (chunk_id)
  WHERE e.model_id = %(model_id)s
  LIMIT 50
)"""

_VEC_CTE_QVEC = """,
vec AS (
  SELECT e.chunk_id,
         row_number() OVER (ORDER BY e.embedding <=> %(qvec)s::halfvec(1024)) AS r
  FROM embeddings e JOIN candidate USING (chunk_id)
  WHERE e.model_id = %(model_id)s
  LIMIT 50
)"""


def _fts_query(query: str) -> str:
    """OR-of-terms websearch query.

    The framed query is long and often bilingual; websearch_to_tsquery ANDs
    every term, so no single chunk can satisfy it. OR the distinct terms
    instead and let ts_rank_cd surface the chunks matching most of them.
    """
    terms = dict.fromkeys(t for t in re.findall(r"\w{2,}", query.lower()) if t != "or")
    return " OR ".join(terms) or query


def connect(cfg: WorkflowConfig) -> psycopg.Connection:
    """Open a dict-row connection to the legislation DB."""
    return psycopg.connect(cfg.database_url, row_factory=dict_row)


def citation_fast_path(
    conn: psycopg.Connection, country: str, lang: str, as_of: date, citations: list[str], k: int
) -> list[RetrievalHit]:
    """Look up chunks by known citation strings / national ids, as-of filtered."""
    hits: dict[str, RetrievalHit] = {}
    for cit in citations:
        rows = conn.execute(
            _CITATION_SQL, {"country": country, "lang": lang, "as_of": as_of, "cit": cit, "k": k}
        ).fetchall()
        for row in rows:
            hits.setdefault(row["chunk_id"], RetrievalHit(method="citation", **row))
    return list(hits.values())


def hybrid_search(
    conn: psycopg.Connection,
    country: str,
    lang: str,
    as_of: date,
    query: str,
    model_id: int,
    k: int,
    query_vector: str | None = None,
) -> list[RetrievalHit]:
    """RRF-merged FTS + vector search over as-of/jurisdiction/lang candidates."""
    use_placeholder = model_id == 99  # demo embedder lives in SQL; see module docstring
    use_vector = use_placeholder or query_vector is not None
    sql = _HYBRID_SQL_TEMPLATE.format(
        vec_cte=(_VEC_CTE if use_placeholder else _VEC_CTE_QVEC) if use_vector else "",
        # RRF, plus guaranteed slots for the vector top-3: ts_rank_cd has no
        # IDF, so common fiscal terms let long amending acts crowd the FTS
        # leg, and a chunk ranked #1 by the (semantically reliable) vector
        # leg alone would lose the fusion to chunks present in both legs.
        score_expr=(
            "(coalesce(1.0/(60+fts.r),0) + coalesce(1.0/(60+vec.r),0)"
            " + CASE WHEN vec.r <= 3 THEN 1.0 ELSE 0 END)::float8"
            if use_vector
            else "(1.0/(60+fts.r))::float8"
        ),
        joined="fts FULL OUTER JOIN vec USING (chunk_id)" if use_vector else "fts",
    )
    params = {
        "country": country,
        "lang": lang,
        "as_of": as_of,
        "q": query,
        "fts_q": _fts_query(query),
        "qvec": query_vector,
        "k": k,
        "model_id": model_id,
    }
    rows = conn.execute(sql, params).fetchall()
    return [RetrievalHit(method="hybrid", **row) for row in rows]


def retrieve(
    conn: psycopg.Connection,
    cfg: WorkflowConfig,
    country: str,
    as_of: date,
    query: str,
    citations: list[str],
) -> list[RetrievalHit]:
    """Citation fast path first, then hybrid; dedup by chunk_id, fast-path wins."""
    lang = LANG_BY_COUNTRY.get(country, "en")
    merged: dict[str, RetrievalHit] = {}
    for hit in citation_fast_path(conn, country, lang, as_of, citations, cfg.retrieval_k):
        merged[hit.chunk_id] = hit
    query_vector = query_encoder.encode(query) if cfg.embedding_model_id != 99 else None
    for hit in hybrid_search(
        conn, country, lang, as_of, query, cfg.embedding_model_id, cfg.retrieval_k, query_vector
    ):
        merged.setdefault(hit.chunk_id, hit)
    return list(merged.values())[: cfg.retrieval_k]


def sibling_text(conn: psycopg.Connection, chunk_id: str, lang: str) -> str | None:
    """Content of the same version's chunk (same seq) in another language, if ingested."""
    row = conn.execute(
        """
        SELECT c2.content
        FROM chunks c1
        JOIN unit_texts t1 ON t1.id = c1.unit_text_id
        JOIN unit_texts t2 ON t2.version_id = t1.version_id AND t2.lang = %(lang)s
        JOIN chunks c2     ON c2.unit_text_id = t2.id AND c2.seq = c1.seq
        WHERE c1.id = %(chunk_id)s::uuid
        LIMIT 1
        """,
        {"chunk_id": chunk_id, "lang": lang},
    ).fetchone()
    return row["content"] if row else None


def verify_extract(
    conn: psycopg.Connection, chunk_id: str, extract: str
) -> tuple[int, int] | None:
    """Locate a supposedly-verbatim extract inside the cited chunk.

    Returns (char_start, char_end) offsets into unit_texts.content — the
    anti-hallucination check: no offsets, no verified citation. Whitespace
    runs are treated as equivalent so line-wrapping differences don't fail
    an otherwise verbatim quote.
    """
    row = conn.execute(
        "SELECT content, char_start FROM chunks WHERE id = %s::uuid", (chunk_id,)
    ).fetchone()
    if row is None or not extract:
        return None
    content, base = row["content"], row["char_start"] or 0
    idx = content.find(extract)
    if idx >= 0:
        return (base + idx, base + idx + len(extract))
    pattern = re.compile(r"\s+".join(re.escape(part) for part in extract.split()))
    match = pattern.search(content)
    if match:
        return (base + match.start(), base + match.end())
    return None
