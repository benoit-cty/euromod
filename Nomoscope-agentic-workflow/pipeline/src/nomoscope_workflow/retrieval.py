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

_VALIDITY_START = re.compile(r"[\[\(](\d{4}-\d{2}-\d{2})")


def validity_start(validity: str | None) -> date | None:
    """Lower bound of a Postgres daterange rendered as text ('[2025-02-15,)')."""
    match = _VALIDITY_START.match(validity or "")
    return date.fromisoformat(match.group(1)) if match else None

# One version per article, not per (legal_unit, version) row. `validity @> as_of`
# alone stops discriminating whenever the same article exists twice: Legifrance
# mints a new consolidated text per amendment, and an article fetched standalone
# nests under a different path than the same article fetched with its code, so
# ingest can leave two open-ended `in_force` versions side by side (CGI art. 197:
# the seeded 2025 barème at 11 497 next to the ingested 2026 one at 11 600).
# Both then compete in the ranking and the superseded text can win. Keep the one
# with the latest start — the article as consolidated on the reference date.
_LIVE_VERSION_CTE = """
live_version AS (
  SELECT DISTINCT ON (i.id, coalesce(u.citation, u.id::text)) v.id AS version_id
  FROM legal_unit_versions v
  JOIN legal_units u         ON u.id = v.legal_unit_id
  JOIN instruments i         ON i.id = u.instrument_id
  JOIN jurisdictions j       ON j.id = i.jurisdiction_id
  WHERE v.validity @> %(as_of)s::date AND j.code = %(country)s
    -- Class rule, not a type string (ADR 0001): a 'context' corpus describes
    -- the model rather than the law and is never citable evidence. Country
    -- Reports are the only one today; a future one is excluded by the same
    -- predicate without touching this SQL.
    AND i.source_trust_class <> 'context'
  ORDER BY i.id, coalesce(u.citation, u.id::text), lower(v.validity) DESC
)"""

_CITATION_SQL = f"""
WITH {_LIVE_VERSION_CTE}
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class,
       similarity(u.citation, %(cit)s)::float8 AS score
FROM legal_units u
JOIN instruments i         ON i.id = u.instrument_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
JOIN live_version lv       ON lv.version_id = v.id
JOIN unit_texts t          ON t.version_id = v.id
JOIN chunks ch             ON ch.unit_text_id = t.id
WHERE t.lang = %(lang)s
  AND (similarity(u.citation, %(cit)s) > 0.55 OR u.national_id = %(cit)s)
ORDER BY score DESC, ch.seq
LIMIT %(k)s
"""

_HYBRID_SQL_TEMPLATE = f"""
WITH {_LIVE_VERSION_CTE},
candidate AS (
  SELECT c.id AS chunk_id, c.tsv, c.search_config
  FROM chunks c
  JOIN unit_texts t    ON t.id = c.unit_text_id
  JOIN live_version lv ON lv.version_id = t.version_id
  WHERE t.lang = %(lang)s
),
fts AS (
  SELECT chunk_id,
         row_number() OVER (
           -- 1|32: log-length normalisation, then rank/(rank+1). Without the
           -- length term, long amending acts that repeat common fiscal words
           -- outrank the short implementing act that actually sets the value.
           ORDER BY ts_rank_cd(tsv, websearch_to_tsquery(search_config, %(fts_q)s), 1|32) DESC
         ) AS r
  FROM candidate
  WHERE tsv @@ websearch_to_tsquery(search_config, %(fts_q)s)
  LIMIT 50
){{vec_cte}}
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class,
       {{score_expr}} AS score
FROM {{joined}}
JOIN chunks ch             ON ch.id = chunk_id
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
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


_CR_SEARCH_SQL = """
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class,
       ts_rank_cd(ch.tsv, websearch_to_tsquery(ch.search_config, %(fts_q)s), 1|32)::float8 AS score
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
WHERE i.source_trust_class = 'context'
  AND j.code = %(country)s
  AND v.validity @> %(as_of)s::date
  AND ch.tsv @@ websearch_to_tsquery(ch.search_config, %(fts_q)s)
ORDER BY score DESC
LIMIT %(k)s
"""


def country_report_search(
    conn: psycopg.Connection, country: str, as_of: date, query: str, k: int
) -> list[RetrievalHit]:
    """FTS over the Country Report corpus (instrument_type='country_report').

    Context-only companion to retrieve(): CR sections translate EUROMOD
    parameter acronyms into semantic, native-language descriptions and so
    improve query framing — but they describe the model, not the law, and
    must never be offered to propose/critique as citable evidence. CRs are
    English, so no per-country lang mapping applies.
    """
    rows = conn.execute(
        _CR_SEARCH_SQL,
        {"country": country, "as_of": as_of, "fts_q": _fts_query(query), "k": k},
    ).fetchall()
    return [RetrievalHit(method="country_report", **row) for row in rows]


# Path segments / tokens of a model_target that carry no searchable meaning.
_IDENT_NOISE = {"euromod", "def", "const", "s"}


def euromod_ident_tokens(model_target: str) -> list[str]:
    """Searchable tokens of a parameter's EUROMOD identity.

    'euromod://FR/tin_fr/def_const/$tinrt_cdhr' -> ['tin', 'tinrt', 'cdhr']:
    the policy stem and constant-name parts. These are the tokens CR section
    headings carry ('... — tinto01_s ("Contribution différentielle ...", CDHR)'),
    so they anchor CR matches far better than generic label words.
    """
    # [a-z0-9]+ (not \w+): underscores must split, 'tinrt_cdhr' -> tinrt, cdhr
    raw = re.findall(r"[a-z0-9]+", model_target.lower())
    country = raw[1] if len(raw) > 1 and len(raw[1]) == 2 else None
    tokens = dict.fromkeys(
        t for t in raw if len(t) >= 3 and not t.isdigit() and t not in _IDENT_NOISE and t != country
    )
    return list(tokens)


def cr_enrichment_terms(
    hits: list[RetrievalHit], ident_tokens: list[str], base_query: str, cap: int = 12
) -> list[str]:
    """Harvest query-enrichment words from Country Report section headings.

    Precision gate: only the FIRST hit whose heading shares a token with the
    parameter's EUROMOD identity contributes — FTS rank alone lets long
    generic sections ('Income test', CSG) outrank the right one, and later
    ident-matching headings are cross-references that add mostly junk
    ('Carry-over from 2.7.6 ... end of section'). Harvest is heading-only
    (native names live there: '(Allocation Familiale, AF)'); chunk bodies
    are ~6k chars and would dilute the query into noise.
    """
    ident = set(ident_tokens)
    have = {w.lower() for w in re.findall(r"\w+", base_query)}
    terms: list[str] = []
    for hit in hits:
        heading = hit.citation or ""
        if not ident & set(re.findall(r"[a-z0-9]+", heading.lower())):
            continue
        text = heading.split("§", 1)[-1]
        text = re.sub(r"\[.*?\]", "", text)          # page refs: [pp. 110-111]
        text = re.sub(r"^[\d.\s]+", "", text)         # leading section numbering
        for word in re.findall(r"\w+", text):
            lower = word.lower()
            if len(word) < 3 or any(c.isdigit() for c in word) or "_" in word:
                continue
            if lower in have:
                continue
            have.add(lower)
            terms.append(word)
            if len(terms) >= cap:
                break
        break
    return terms


def unit_chunks(conn: psycopg.Connection, chunk_id: str) -> list[RetrievalHit]:
    """ALL chunks of the unit text a chunk belongs to, in document order.

    Long articles are split into several chunks and retrieval may surface only
    one of them; income-year date checks (and the proposal retry) need the
    whole article — e.g. LF 2025 art. 10 states the CDHR mechanism in chunk 1
    and its "revenus de l'année 2025" applicability clause in chunk 2.
    """
    rows = conn.execute(
        """
        SELECT c2.id::text AS chunk_id, u.citation, c2.context_header, c2.content,
               t.lang, v.validity::text AS validity, v.version_status,
               i.source_trust_class
        FROM chunks c1
        JOIN unit_texts t ON t.id = c1.unit_text_id
        JOIN legal_unit_versions v ON v.id = t.version_id
        JOIN legal_units u ON u.id = v.legal_unit_id
        JOIN instruments i ON i.id = u.instrument_id
        JOIN chunks c2 ON c2.unit_text_id = t.id
        WHERE c1.id = %(chunk_id)s::uuid
        ORDER BY c2.seq
        """,
        {"chunk_id": chunk_id},
    ).fetchall()
    return [RetrievalHit(method="sibling", **row) for row in rows]


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
