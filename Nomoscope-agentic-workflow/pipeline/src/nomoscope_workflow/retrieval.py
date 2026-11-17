"""Retrieval against the legislation DB (Nomotheca-RAG/db/schema.sql).

Two paths, per Nomotheca-RAG/11_database-model.md §5:
  1. citation fast path — pg_trgm match on legal_units.citation / national_id,
     filtered to the version in force at as_of (the majority case: updates
     start from last year's citation);
  2. hybrid — candidates pre-filtered by as_of/jurisdiction/lang, then
     FTS top-50 || vector top-50 merged by Reciprocal Rank Fusion (k=60),
     the SQL pattern from Nomotheca-RAG/db/demo_queries.sql (f).

The vector leg encodes the query with the real BGE-M3 encoder (model_id 1,
via query_encoder — the ingest package's subprocess, or the worker's encode
job when WORKFLOW_ENCODER=db) and falls back to FTS-only when the encoder is unavailable. The demo placeholder embedder
(model_id 99) keeps its embed-in-SQL path via placeholder_embedding().
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date

import psycopg
from psycopg.rows import dict_row

from . import query_encoder
from .quotes import closest_passage, quote_span, verify_extract  # noqa: F401  (re-exported)
from .config import PLACEHOLDER_MODEL_ID, WorkflowConfig
from .schema import ParameterRecord, RetrievalHit
from .corpus import (  # noqa: F401  (re-exported: retrieval is the facade)
    CHUNK_JOINS,
    HIT_COLUMNS,
    LANG_BY_COUNTRY,
    Scope,
    _LIVE_VERSION_CTE,
    _fts_query,
    connect,
    jurisdiction_scope,
    law_language,
    record_scope,
    scope_codes,
    unit_chunks,
    validity_end,
    validity_start,
    version_provenance,
)
from .country_report import (  # noqa: F401
    _CR_SEARCH_SQL,
    country_report_search,
    cr_enrichment_terms,
    euromod_ident_tokens,
)
from .crossrefs import (  # noqa: F401
    CROSS_REF_MAX,
    IMPLEMENTING_MAX,
    _code_refs,
    _same_act_citing,
    _same_act_refs,
    cross_referenced_articles,
    implementing_acts,
    same_act_articles,
)
from .locate import (  # noqa: F401
    _article_tokens,
    _citation_pattern,
    _entered_since,
    act_numbers,
    gap_articles,
    instruments_of_chunks,
    locate_named_units,
)

_CITATION_SQL = f"""
WITH {_LIVE_VERSION_CTE}
SELECT {HIT_COLUMNS},
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

# Hybrid search is the database's search_chunks() (Nomotheca-RAG/db/schema.sql):
# one implementation for the workflow, the eval, the review UI and the MCP
# server — live version, trust class, OR-of-terms FTS, RRF + vector top-3 slot.
_HYBRID_SQL = f"""
SELECT {HIT_COLUMNS},
       s.score
FROM search_chunks(%(q)s, {{qvec}}, %(model_id)s, %(jurisdictions)s::text[],
                   ARRAY[%(lang)s]::text[], %(as_of)s::date, %(k)s, %(use_fts)s) s
JOIN chunks ch             ON ch.id = s.chunk_id
{CHUNK_JOINS}
ORDER BY s.score DESC, s.chunk_id
"""


def citation_fast_path(
    conn: psycopg.Connection, country: Scope, lang: str, as_of: date, citations: list[str], k: int
) -> list[RetrievalHit]:
    """Look up chunks by known citation strings / national ids, as-of filtered."""
    hits: dict[str, RetrievalHit] = {}
    jurisdictions = scope_codes(country)
    for cit in citations:
        with conn.cursor(row_factory=dict_row) as cur:
            rows = cur.execute(
                _CITATION_SQL,
                {"jurisdictions": jurisdictions, "lang": lang, "as_of": as_of, "cit": cit, "k": k},
            ).fetchall()
        for row in rows:
            hits.setdefault(row["chunk_id"], RetrievalHit(method="citation", **row))
    return list(hits.values())


def hybrid_search(
    conn: psycopg.Connection,
    country: Scope,
    lang: str,
    as_of: date,
    query: str,
    model_id: int,
    k: int,
    query_vector: str | None = None,
    *,
    use_fts: bool = True,
) -> list[RetrievalHit]:
    """RRF-merged FTS + vector search over as-of/jurisdiction/lang candidates.

    ``use_fts=False`` is the vector leg alone (the embedding comparison's
    "vector" method), ranked by the same function.
    """
    # The demo placeholder embedder (99) lives in SQL; see the module docstring.
    if model_id == PLACEHOLDER_MODEL_ID:
        qvec = "placeholder_embedding(%(q)s)"
    elif query_vector is not None:
        qvec = "%(qvec)s::halfvec(1024)"
    else:
        qvec = "NULL"
    sql = _HYBRID_SQL.format(qvec=qvec)
    params = {
        "jurisdictions": scope_codes(country),
        "lang": lang,
        "as_of": as_of,
        "q": query,
        "qvec": query_vector,
        "k": k,
        "model_id": model_id,
        "use_fts": use_fts,
    }
    # Rows are unpacked by name: bind the row factory here rather than relying on
    # the caller's connection (a plain `psycopg.connect` yields tuples).
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(sql, params).fetchall()
    # "fts": the vector leg was unavailable (encoder down or paused) — the
    # review item's retrieval trace, and the eval, record the degradation.
    if not use_fts:
        method = "vector"
    elif model_id == PLACEHOLDER_MODEL_ID or query_vector is not None:
        method = "hybrid"
    else:
        method = "fts"
    return [RetrievalHit(method=method, **row) for row in rows]


def retrieve(
    conn: psycopg.Connection,
    cfg: WorkflowConfig,
    country: Scope,
    as_of: date,
    query: str,
    citations: list[str],
    later_until: date | None = None,
) -> list[RetrievalHit]:
    """Citation fast path first, then hybrid; dedup by chunk_id, fast-path wins.

    The articles the k hits send the reader to follow them (up to
    CROSS_REF_MAX, see ``cross_referenced_articles``), and so do the articles
    of the same act they name (``same_act_articles``). With ``later_until``,
    up to LATER_MAX_HITS versions that enter into force
    after ``as_of`` and by that date follow the k hits (see ``later_in_year``).

    ``country`` is a jurisdiction scope (see ``jurisdiction_scope``); the
    law language is the country's, i.e. the scope's first code.
    """
    lang = law_language(country)
    merged: dict[str, RetrievalHit] = {}
    for hit in citation_fast_path(conn, country, lang, as_of, citations, cfg.retrieval_k):
        merged[hit.chunk_id] = hit
    query_vector = (
        query_encoder.encode(query, cfg.database_url, cfg.embedding_model_id)
        if cfg.embedding_model_id != PLACEHOLDER_MODEL_ID
        else None
    )
    for hit in hybrid_search(
        conn, country, lang, as_of, query, cfg.embedding_model_id, cfg.retrieval_k, query_vector
    ):
        merged.setdefault(hit.chunk_id, hit)
    hits = list(merged.values())[: cfg.retrieval_k]
    hits += cross_referenced_articles(conn, country, lang, as_of, [h.chunk_id for h in hits])
    hits += implementing_acts(
        conn, country, lang, as_of, [h.chunk_id for h in hits], query_vector, cfg.embedding_model_id
    )
    if later_until is not None and later_until > as_of:
        hits += later_in_year(
            conn, country, lang, as_of, later_until, query, cfg.embedding_model_id,
            cfg.retrieval_k, query_vector, known={h.chunk_id for h in hits},
        )
    hits += same_act_articles(conn, lang, [h.chunk_id for h in hits])
    return hits


#: How many later-in-the-year versions join the hits: enough for an order's
#: amount article and its threshold article, few enough not to drown the
#: versions in force on the reference date.
LATER_MAX_HITS = 8
LATER_DEPTH = 4


def later_in_year(
    conn: psycopg.Connection,
    country: Scope,
    lang: str,
    as_of: date,
    until: date,
    query: str,
    model_id: int,
    k: int,
    query_vector: str | None = None,
    known: set[str] | frozenset[str] = frozenset(),
) -> list[RetrievalHit]:
    """Versions entering into force after `as_of` and on or before `until`.

    A EUROMOD system year describes the whole year, and some of its values
    are only published after the 1 July reference date: the 2025 chèque
    énergie barème is the arrêté du 31 juillet 2025, in force from 2 August
    yet applying «à compter du 1er janvier 2025». Filtered on 1 July, all
    17 bhoey_fr parameters came back not_found with the arrêté in the corpus.
    The same hybrid search runs at `until`, LATER_DEPTH times deeper; only
    versions starting after `as_of` are kept, so nothing in force on the
    reference date is displaced. Deeper, because a December act competes
    with every text in force: at k the 2025 prime-de-Noël décret (in force
    14 December) was never among the hits, the RSA decrees always were.
    """
    hits = hybrid_search(conn, country, lang, until, query, model_id, k * LATER_DEPTH, query_vector)
    later = [
        hit.model_copy(update={"method": "later_in_year"})
        for hit in hits
        if hit.chunk_id not in known and (validity_start(hit.validity) or date.min) > as_of
    ]
    return later[:LATER_MAX_HITS]


def locate_sources(
    cfg: WorkflowConfig,
    record: ParameterRecord,
    as_of: date,
    needs: list[str],
    known_chunk_ids: Iterable[str],
    later_until: date | None = None,
) -> tuple[list[RetrievalHit], list[str]]:
    """Look the analyst's named sources up in the corpus we already hold.

    The complement of the scout's `run`: that one fetches what is missing, this one finds
    what is present but was ranked out. Nothing here weakens the contract —
    the chunks come from the database like any retrieved chunk and the
    verbatim-quote check still applies to whatever gets cited from them.
    Returns the new chunks (not already among `known_chunk_ids`) and the
    citations they belong to, for the ScoutResult and the reviewer. With
    `later_until`, a named source whose version starts after `as_of` and by
    that date is found too, as a "later_in_year" hit (`later_in_year`).
    """
    info = record.information
    seen = set(known_chunk_ids)
    hits: list[RetrievalHit] = []
    citations: list[str] = []
    with connect(cfg) as conn:
        scope = record_scope(conn, info)
        lang = law_language(scope)
        held = instruments_of_chunks(conn, list(seen))
        # Articles missing between two retrieved ones (AGIRC-ARRCO art. 36
        # between 35 and 38), then the code articles the retrieved ones send
        # the reader to (R. 531-1 → R. 522-2), come first: they need no named
        # source at all.
        for hit in [
            *gap_articles(conn, scope, lang, as_of, list(seen)),
            *cross_referenced_articles(conn, scope, lang, as_of, list(seen)),
            *same_act_articles(conn, lang, list(seen)),
        ]:
            if hit.chunk_id in seen:
                continue
            seen.add(hit.chunk_id)
            hits.append(hit)
            if hit.citation and hit.citation not in citations:
                citations.append(hit.citation)
        for need in needs[:5]:
            found = locate_named_units(
                conn, scope, lang, as_of, need, held_instrument_ids=held
            )
            if later_until is not None and later_until > as_of:
                found += [
                    hit.model_copy(update={"method": "later_in_year"})
                    for hit in locate_named_units(
                        conn, scope, lang, later_until, need, held_instrument_ids=held
                    )
                    if (validity_start(hit.validity) or date.min) > as_of
                ]
            for hit in found:
                if hit.chunk_id in seen:
                    continue
                seen.add(hit.chunk_id)
                hits.append(hit)
                if hit.citation and hit.citation not in citations:
                    citations.append(hit.citation)
    return hits, citations
