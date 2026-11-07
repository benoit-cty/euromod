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

import difflib
import re
from collections.abc import Sequence
from datetime import date, timedelta

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


_VALIDITY_END = re.compile(r",(\d{4}-\d{2}-\d{2})[\])]")


def validity_end(validity: str | None) -> date | None:
    """Exclusive upper bound of a rendered daterange; None when open-ended."""
    match = _VALIDITY_END.search(validity or "")
    return date.fromisoformat(match.group(1)) if match else None


def version_provenance(conn: psycopg.Connection, chunk_id: str) -> dict | None:
    """Where a chunk's text comes from: instrument type, version window, snapshot date.

    The income-year critique needs to know whether a cited text is a
    consolidated code article (Legifrance mints one version per amendment,
    so the version in force on the retrieval date IS the text applied to that
    assessment) and how fresh our copy is (an open-ended version only proves
    "not amended" up to the day it was fetched).
    """
    row = conn.execute(
        """
        SELECT i.instrument_type, v.validity::text AS validity,
               upper_inf(v.validity) AS open_ended, s.retrieved_at
        FROM chunks c
        JOIN unit_texts t          ON t.id = c.unit_text_id
        JOIN legal_unit_versions v ON v.id = t.version_id
        JOIN legal_units u         ON u.id = v.legal_unit_id
        JOIN instruments i         ON i.id = u.instrument_id
        JOIN fetch_snapshots s     ON s.id = v.fetch_snapshot_id
        WHERE c.id = %(chunk_id)s::uuid
        """,
        {"chunk_id": chunk_id},
    ).fetchone()
    return dict(row) if row else None

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
  -- Jurisdiction SCOPE, not country (ADR 0003): the country's own code plus,
  -- for a regional parameter, its region's child jurisdiction — see
  -- jurisdiction_scope(). A national run therefore never sees regional acts,
  -- and Aragón's run never sees Asturias's decree.
  WHERE v.validity @> %(as_of)s::date AND j.code = ANY(%(jurisdictions)s::text[])
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


Scope = str | Sequence[str]


def scope_codes(scope: Scope) -> list[str]:
    """Normalise a jurisdiction scope: a bare country code or a list of codes.

    The first code is the country; the rest are its child jurisdictions the run
    may also draw on. Every caller that used to pass ``country`` still can.
    """
    codes = [scope] if isinstance(scope, str) else list(scope)
    if not codes:
        msg = "empty jurisdiction scope"
        raise ValueError(msg)
    return codes


_SCOPE_SQL = """
SELECT j.code
FROM jurisdictions j
JOIN jurisdictions p ON p.id = j.parent_id
WHERE p.code = %(country)s AND j.metadata->>'nuts2' = %(region)s
"""


def jurisdiction_scope(conn: psycopg.Connection, country: str, region: str | None) -> list[str]:
    """Codes a run may retrieve from: the country, plus its region's child jurisdiction.

    ``region`` is the parameter's NUTS-2 key (``regions.region_key``). A
    national parameter scopes to ``[country]`` alone — regional acts are filed
    under children and stay out of national runs. A regional parameter adds
    the one child whose seeded ``nuts2`` matches; a region the database does
    not know falls back to the country alone, which is the safe side (it can
    only produce not_found, never a sibling region's value).
    """
    scope = [country]
    if region:
        row = conn.execute(_SCOPE_SQL, {"country": country, "region": region}).fetchone()
        if row:
            scope.append(row["code"])
    return scope


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
        "jurisdictions": scope_codes(country),
        "lang": lang,
        "as_of": as_of,
        "q": query,
        "fts_q": _fts_query(query),
        "qvec": query_vector,
        "k": k,
        "model_id": model_id,
    }
    # Rows are unpacked by name: bind the row factory here rather than relying on
    # the caller's connection (a plain `psycopg.connect` yields tuples).
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(sql, params).fetchall()
    return [RetrievalHit(method="hybrid", **row) for row in rows]


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
    lang = LANG_BY_COUNTRY.get(scope_codes(country)[0], "en")
    merged: dict[str, RetrievalHit] = {}
    for hit in citation_fast_path(conn, country, lang, as_of, citations, cfg.retrieval_k):
        merged[hit.chunk_id] = hit
    query_vector = (
        query_encoder.encode(query, cfg.database_url, cfg.embedding_model_id)
        if cfg.embedding_model_id != 99
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


# ---------------------------------------------------------------------------
# Locating a source the analyst named
# ---------------------------------------------------------------------------

#: An article designator as the analyst writes it in a "missing source": the
#: country's word for article/section then the number — «article D. 633-3»,
#: «artículo 66.2», «artikel 2.10», «section 461», «s. 531AN» — or, in
#: Lithuanian, the number then «straipsnis».
_ARTICLE_REF = re.compile(
    r"(?:\b(?:art(?:[ií]culo|ikel|icle)?s?\.?|sections?|s\.|§)\s*(?:n[°º]\s*)?"
    r"([A-Z]?\.?\s?\d+(?:[.\-]\d+)*[A-Za-z]{0,2}(?:\s(?:bis|ter|quater|quinquies|sexies))?))"
    r"|(?:\b(\d+(?:[.\-]\d+)*)\s+straipsn)",
    re.IGNORECASE,
)

#: How much of an act's title must appear in the need for the act to count as
#: named: Ley 35/2006's full title scores 0.47 against «artículo 66.2 de la Ley
#: 35/2006, del Impuesto sobre la Renta de las Personas Físicas …» and the next
#: act 0.35; a code named in full scores 0.85–1.0.
NAMED_ACT_MIN_SCORE = 0.4

_NAMED_INSTRUMENTS_SQL = """
SELECT i.id::text AS instrument_id, i.national_id, i.title_search,
       word_similarity(i.title_search, %(need)s)::float8 AS score
FROM instruments i
JOIN jurisdictions j ON j.id = i.jurisdiction_id
WHERE j.code = ANY(%(jurisdictions)s::text[])
  AND i.source_trust_class <> 'context'
  AND word_similarity(i.title_search, %(need)s) >= %(min_score)s
ORDER BY score DESC
LIMIT 3
"""

_NAMED_UNIT_SQL = f"""
WITH {_LIVE_VERSION_CTE}
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class,
       word_similarity(i.title_search, %(need)s)::float8 AS score
FROM legal_units u
JOIN instruments i         ON i.id = u.instrument_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
JOIN live_version lv       ON lv.version_id = v.id
JOIN unit_texts t          ON t.version_id = v.id
JOIN chunks ch             ON ch.unit_text_id = t.id
WHERE t.lang = %(lang)s
  AND u.citation ~* %(pattern)s
  AND (%(instrument_ids)s::uuid[] IS NULL OR i.id = ANY(%(instrument_ids)s::uuid[]))
ORDER BY score DESC, u.citation, ch.seq
LIMIT %(k)s
"""

#: How far back step 4 of locate_named_units looks for a recently enacted text.
RECENT_LOOKBACK = timedelta(days=365)
#: Step-4 chunks added even when the named act was found and is recent.
RECENT_EXTRA = 3

# Step 4: the need's words, any of them, ranked over the chunks of versions in
# force on as_of that entered into force within RECENT_LOOKBACK of it.
_RECENT_FTS_SQL = """
WITH q AS (
  SELECT to_tsquery(c.config, string_agg(quote_literal(l.lexeme), ' | ')) AS tq
  FROM lang_fts_config c, unnest(to_tsvector(c.config, %(need)s)) AS l
  WHERE c.lang = %(lang)s
  GROUP BY c.config
)
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class,
       ts_rank_cd(ch.tsv, q.tq, 1|32)::float8 AS score
FROM q, chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id AND t.lang = %(lang)s
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
WHERE j.code = ANY(%(jurisdictions)s::text[]) AND i.source_trust_class <> 'context'
  AND v.validity @> %(as_of)s::date AND lower(v.validity) >= %(since)s::date
  AND ch.tsv @@ q.tq
ORDER BY score DESC
LIMIT %(k)s
"""

def _entered_since(validity: str | None, since: date) -> bool:
    """Whether a '[2025-04-01,)' daterange starts on or after `since`."""
    start = re.match(r"[\[(](\d{4}-\d{2}-\d{2})", validity or "")
    return start is not None and date.fromisoformat(start.group(1)) >= since


_NAMED_INSTRUMENT_FTS_SQL = f"""
WITH {_LIVE_VERSION_CTE}
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class,
       -- Content only: chunks.tsv carries the context header at weight A, and
       -- the header repeats the act's title in every chunk of the act.
       ts_rank_cd(to_tsvector(ch.search_config, ch.content),
                  websearch_to_tsquery(ch.search_config, %(fts_q)s), 1|32)::float8 AS score
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN live_version lv       ON lv.version_id = v.id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
WHERE t.lang = %(lang)s
  AND i.id = %(instrument_id)s::uuid
  AND to_tsvector(ch.search_config, ch.content) @@ websearch_to_tsquery(ch.search_config, %(fts_q)s)
ORDER BY score DESC
LIMIT %(k)s
"""


#: Most articles a gap may hold for `gap_articles` to fill it.
GAP_MAX_ARTICLES = 3

# An article's "series" is its path minus the article label — '' for the main
# text, 'annexe_a_' for an annex — so an annex's art. 1er never fills a gap
# between the agreement's own articles.
_GAP_ARTICLES_SQL = f"""
WITH {_LIVE_VERSION_CTE},
held AS (
  SELECT DISTINCT u.instrument_id, u.ordinal,
         regexp_replace(u.path::text, 'art_[^.]*$', '') AS series
  FROM chunks ch
  JOIN unit_texts t          ON t.id = ch.unit_text_id
  JOIN legal_unit_versions v ON v.id = t.version_id
  JOIN legal_units u         ON u.id = v.legal_unit_id
  WHERE ch.id = ANY(%(chunk_ids)s::uuid[]) AND u.path::text ~ '(^|[._])art_[^.]*$'
),
gaps AS (
  SELECT instrument_id, series, ordinal AS lo,
         lead(ordinal) OVER (PARTITION BY instrument_id, series ORDER BY ordinal) AS hi
  FROM held
)
SELECT g.lo, u.id::text AS unit_id, ch.id::text AS chunk_id, u.citation, ch.context_header,
       ch.content, t.lang, v.validity::text AS validity, v.version_status, i.source_trust_class,
       NULL::float8 AS score
FROM gaps g
JOIN legal_units u         ON u.instrument_id = g.instrument_id
                          AND regexp_replace(u.path::text, 'art_[^.]*$', '') = g.series
                          AND u.path::text ~ '(^|[._])art_[^.]*$'
                          AND u.ordinal > g.lo AND u.ordinal < g.hi
JOIN instruments i         ON i.id = u.instrument_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
JOIN live_version lv       ON lv.version_id = v.id
JOIN unit_texts t          ON t.version_id = v.id
JOIN chunks ch             ON ch.unit_text_id = t.id
WHERE g.hi IS NOT NULL AND g.hi - g.lo <= %(max_gap)s + 1 AND t.lang = %(lang)s
ORDER BY g.instrument_id, u.ordinal, ch.seq
"""


def gap_articles(
    conn: psycopg.Connection,
    scope: Scope,
    lang: str,
    as_of: date,
    chunk_ids: list[str],
    max_gap: int = GAP_MAX_ARTICLES,
) -> list[RetrievalHit]:
    """The articles missing between two retrieved articles of the same act.

    Consecutive articles state one scheme together, and retrieval ranks them
    one by one: on the 3 Nov benchmark the AGIRC-ARRCO rates were proposed with
    arts. 34 (rate = point rate × call percentage), 35 (6,20 % / 17 %) and 38
    (60 % employer) in hand — and not art. 36, the one line «Un pourcentage
    d'appel, fixé à 127 %». Four rates came back not_found, each asking for that
    percentage. A gap of at most `max_gap` articles between two held ones is
    filled; a wider one is a different part of the act. Hits are "located":
    looked up, not ranked.
    """
    if not chunk_ids:
        return []
    params = {
        "jurisdictions": scope_codes(scope),
        "as_of": as_of,
        "chunk_ids": chunk_ids,
        "lang": lang,
        "max_gap": max_gap,
    }
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(_GAP_ARTICLES_SQL, params).fetchall()
    # The ordinal is coarse for code articles (D621-1 … D621-9 are all 621), so
    # cap the gap by how many units it actually holds.
    units_per_gap: dict[tuple, set[str]] = {}
    for row in rows:
        units_per_gap.setdefault((row["lo"], row["citation"].rsplit(",", 1)[0]), set()).add(row["unit_id"])
    held = set(chunk_ids)
    hits = []
    for row in rows:
        key = (row["lo"], row["citation"].rsplit(",", 1)[0])
        if len(units_per_gap[key]) > max_gap or row["chunk_id"] in held:
            continue
        fields = {k: v for k, v in row.items() if k not in ("lo", "unit_id")}
        hits.append(RetrievalHit(method="located", **fields))
    return hits


def instruments_of_chunks(conn: psycopg.Connection, chunk_ids: list[str], limit: int = 3) -> list[str]:
    """The acts a set of retrieved chunks mostly comes from, most chunks first."""
    if not chunk_ids:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(
            """
            SELECT u.instrument_id::text AS instrument_id
            FROM chunks ch
            JOIN unit_texts t          ON t.id = ch.unit_text_id
            JOIN legal_unit_versions v ON v.id = t.version_id
            JOIN legal_units u         ON u.id = v.legal_unit_id
            WHERE ch.id = ANY(%(ids)s::uuid[])
            GROUP BY u.instrument_id
            ORDER BY count(*) DESC
            LIMIT %(limit)s
            """,
            {"ids": chunk_ids, "limit": limit},
        ).fetchall()
    return [row["instrument_id"] for row in rows]


def _article_tokens(need: str) -> list[str]:
    """Article numbers named in a need, spelled the way `legal_units.citation`
    spells them: «D. 633-3» -> «D633-3», «66.2» stays (the ES paragraph idiom is
    handled by the caller), «4 bis» keeps its suffix."""
    tokens: list[str] = []
    for match in _ARTICLE_REF.finditer(need):
        raw = (match.group(1) or match.group(2) or "").strip()
        token = re.sub(r"^([A-Za-z])\.?\s*", r"\1", raw)
        token = re.sub(r"\s+(bis|ter|quater|quinquies|sexies)$", r" \1", token, flags=re.IGNORECASE)
        if token and token not in tokens:
            tokens.append(token)
    return tokens


#: «article R. 522-2», «articles L. 531-2 et L. 531-3», «art. D. 633-3»: a
#: code article number as the text of a French code writes it.
_CODE_ARTICLE_REF = re.compile(r"\b([LRD])\.?\s?(\d+(?:-\d+)+)\b")
#: Explicit references followed per article (regulatory R./D. ones first:
#: they carry the figures), and the most a call adds.
CROSS_REF_PER_ARTICLE = 4
CROSS_REF_MAX = 8

_REF_CHUNKS_SQL = """
SELECT ch.id::text AS chunk_id, ch.content, u.citation, i.id::text AS instrument_id,
       i.instrument_type = 'code' AS is_code
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
WHERE ch.id = ANY(%(ids)s::uuid[])
"""

_SCOPE_CODES_SQL = """
SELECT i.id::text AS instrument_id, lower(i.title->>%(lang)s) AS title
FROM instruments i
JOIN jurisdictions j ON j.id = i.jurisdiction_id
WHERE i.instrument_type = 'code' AND j.code = ANY(%(jurisdictions)s::text[])
  AND i.title ? %(lang)s
"""

# One query per hop for every (instrument, citation pattern) a hop looks up:
# each pattern's first article version in force and its first chunk. Per
# lookup, _NAMED_UNIT_SQL's corpus-wide live_version CTE cost 4–13 s a retrieve.
_REFERENCED_UNITS_SQL = """
WITH wanted AS (
  SELECT * FROM unnest(%(instrument_ids)s::uuid[], %(patterns)s::text[]) WITH ORDINALITY AS w(instrument_id, pattern, ord)
),
unit AS (
  SELECT DISTINCT ON (w.ord) w.ord, v.id AS version_id, u.citation, v.validity, v.version_status,
         i.source_trust_class
  FROM wanted w
  JOIN legal_units u         ON u.instrument_id = w.instrument_id AND u.citation ~* w.pattern
  JOIN instruments i         ON i.id = u.instrument_id
  JOIN legal_unit_versions v ON v.legal_unit_id = u.id
  WHERE v.validity @> %(as_of)s::date AND i.source_trust_class <> 'context'
  ORDER BY w.ord, u.citation, lower(v.validity) DESC
)
SELECT DISTINCT ON (unit.ord) ch.id::text AS chunk_id, unit.citation, ch.context_header, ch.content,
       t.lang, unit.validity::text AS validity, unit.version_status, unit.source_trust_class,
       0.0::float8 AS score
FROM unit
JOIN unit_texts t ON t.version_id = unit.version_id AND t.lang = %(lang)s
JOIN chunks ch    ON ch.unit_text_id = t.id
ORDER BY unit.ord, ch.seq
"""

#: How far after an article number its code may be named: «l'article L. 531-3
#: du code de la sécurité sociale», «des articles L. 531-2 et L. 531-3 du même code».
_CODE_NAME_WINDOW = 80
#: How far a list of article numbers may run before the code that closes it.
_CODE_LIST_WINDOW = 600
_ARTICLE_LIST_GAP = re.compile(r"(?:[\s,;.\-–]|et|[lrd]\.?\s?\d+(?:\s?-\s?\d+)*)*\s(?:du|de la)\s+")


def _code_refs(content: str, own: str | None, codes: dict[str, str]) -> list[tuple[str, str]]:
    """(code instrument id, article token) for each code article `content` names.

    The code is the one named right after the number, in the same sentence
    («… du code de la sécurité sociale»), the one named last for «du même code», else the
    chunk's own code — an arrêté's bare article number has no code and is
    skipped. At one position the longest title wins, so «code général des
    impôts, annexe III» is not read as the CGI itself.
    """
    lowered = content.lower()
    mentions = sorted(
        ((m.start(), m.end(), iid) for iid, title in codes.items() for m in re.finditer(re.escape(title), lowered)),
        key=lambda m: (m[0], m[0] - m[1]),  # at one position, the longest title first
    )
    refs: list[tuple[str, str]] = []
    for match in _CODE_ARTICLE_REF.finditer(content):
        tail = lowered[match.end() : match.end() + _CODE_NAME_WINDOW]
        after = next(
            (
                iid
                for start, _, iid in mentions
                if match.end() <= start <= match.end() + _CODE_NAME_WINDOW
                and lowered.endswith("du ", 0, start)
                and ". " not in lowered[match.end() : start]
            ),
            None,
        )
        if after is None:
            # «Articles L. 381-1, L. 545-1, R. 522-2, … D. 521-1 du code de la
            # sécurité sociale» (instruction DSS/2B/2024/181): the code closes
            # the list, past the window — nothing but article numbers between.
            after = next(
                (
                    iid
                    for start, _, iid in mentions
                    if match.end() <= start <= match.end() + _CODE_LIST_WINDOW
                    and _ARTICLE_LIST_GAP.fullmatch(lowered[match.end() : start])
                ),
                None,
            )
        if after is None and "même code" in tail:
            after = next((iid for start, end, iid in reversed(mentions) if end <= match.start()), None)
        instrument = after or own
        if instrument is not None:
            ref = (instrument, f"{match.group(1)}{match.group(2)}")
            if ref not in refs:
                refs.append(ref)
    return refs


def cross_referenced_articles(
    conn: psycopg.Connection,
    country: Scope,
    lang: str,
    as_of: date,
    chunk_ids: list[str],
) -> list[RetrievalHit]:
    """The code articles a retrieved article sends the reader to.

    A French code states a rule in its statutory part and its figures in the
    regulatory part, chained by reference: the PAJE ceilings of the 2025
    arrêté are increased per child «dans les conditions définies aux deuxième
    et troisième alinéas de l'article R. 522-2» (R. 531-1), and L. 531-3,
    which retrieval did rank, names neither — its implementing articles share
    its chapter number (R. 531-*, D. 531-*). On the 3 Nov benchmark 11 bchyc
    ceilings came back not_found holding the arrêté and L. 531-3 but not the
    25 % / 30 % rule. Two hops, inside the same code: an L. article's first
    same-chapter R. and D. articles plus the articles each retrieved article
    names, then the articles those name. A non-code act's references count
    when it names the code («l'article L. 531-3 du code de la sécurité
    sociale» in the arrêté fixing the 2025 ceilings): on the 4 Nov run the
    critique rejected four PAJE ceilings as using «the complément familial's
    R. 522-2» because R. 531-1, the bridge, was never retrieved. Hits are
    "located".
    """
    base = {"jurisdictions": scope_codes(country), "lang": lang, "as_of": as_of, "need": ""}
    with conn.cursor(row_factory=dict_row) as cur:
        codes = {r["instrument_id"]: r["title"] for r in cur.execute(_SCOPE_CODES_SQL, base).fetchall()}
    found: dict[str, RetrievalHit] = {}
    seen = set(chunk_ids)
    frontier = list(chunk_ids)
    for hop in range(2):
        with conn.cursor(row_factory=dict_row) as cur:
            rows = cur.execute(_REF_CHUNKS_SQL, {"ids": frontier}).fetchall()
        rank = {chunk_id: i for i, chunk_id in enumerate(frontier)}
        rows.sort(key=lambda r: rank[r["chunk_id"]])  # the best-ranked hit's references first
        lookups: list[tuple[str, str]] = []
        for row in rows:
            own = (row["citation"] or "").rsplit("art. ", 1)[-1] if row["is_code"] else ""
            refs = [
                (iid, token)
                for iid, token in _code_refs(row["content"] or "", row["instrument_id"] if row["is_code"] else None, codes)
                if not (iid == row["instrument_id"] and token == own)
            ]
            refs.sort(key=lambda r: r[1][0] == "L")  # stable: R./D. first, text order kept
            for iid, token in refs[:CROSS_REF_PER_ARTICLE]:
                lookups.append((iid, _citation_pattern(token)))
                # An L. article's implementing R./D. articles share its chapter
                # number: L. 531-3 → R. 531-1, D. 531-1.
                chapter = re.fullmatch(r"L(\d+)-\d+", token)
                if hop == 0 and chapter and not row["is_code"]:
                    lookups += [(iid, rf"art\. {kind}{chapter.group(1)}-1($|[^0-9])") for kind in ("R", "D")]
            chapter = re.fullmatch(r"L(\d+)-\d+", own)
            if hop == 0 and chapter:
                lookups += [
                    (row["instrument_id"], rf"art\. {kind}{chapter.group(1)}-1($|[^0-9])")
                    for kind in ("R", "D")
                ]
        frontier = []
        if lookups:
            with conn.cursor(row_factory=dict_row) as cur:
                hits = cur.execute(
                    _REFERENCED_UNITS_SQL,
                    {
                        **base,
                        "instrument_ids": [iid for iid, _ in lookups],
                        "patterns": [pattern for _, pattern in lookups],
                    },
                ).fetchall()
        else:
            hits = []
        for hit in hits:
            if hit["chunk_id"] in seen:
                continue
            seen.add(hit["chunk_id"])
            frontier.append(hit["chunk_id"])
            found[hit["chunk_id"]] = RetrievalHit(method="located", **hit)
            if len(found) >= CROSS_REF_MAX:
                return list(found.values())
        if not frontier:
            break
    return list(found.values())


#: «l'article 1er», «aux articles 3 et 4», «à l'article 2 du présent décret»:
#: an article of the act itself. A number followed by another act («de la loi
#: du …», «du code …») is that act's, and skipped.
_SAME_ACT_REF = re.compile(r"\barticles?\s+(\d+)(?:\s?er)?\b(?!\s*[-.]\d)", re.IGNORECASE)
_OTHER_ACT_AFTER = re.compile(
    r"^\s*(?:,\s*)?(?:du|de la|de l'|de l’|des)\s+(?!présente?\b|même décret|même arrêté)",
    re.IGNORECASE,
)
SAME_ACT_PER_ARTICLE = 3
SAME_ACT_MAX = 6

# Per (act, article) lookup: its version in force on the date the citing
# article's version starts, and that version's first chunk.
_SAME_ACT_UNITS_SQL = """
WITH wanted AS (
  SELECT * FROM unnest(%(instrument_ids)s::uuid[], %(patterns)s::text[], %(dates)s::date[])
         WITH ORDINALITY AS w(instrument_id, pattern, at, ord)
),
unit AS (
  SELECT DISTINCT ON (w.ord) w.ord, v.id AS version_id, u.citation, v.validity, v.version_status,
         i.source_trust_class
  FROM wanted w
  JOIN legal_units u         ON u.instrument_id = w.instrument_id AND u.citation ~ w.pattern
  JOIN instruments i         ON i.id = u.instrument_id
  JOIN legal_unit_versions v ON v.legal_unit_id = u.id
  WHERE v.validity @> w.at AND i.source_trust_class <> 'context'
  ORDER BY w.ord, lower(v.validity) DESC
)
SELECT DISTINCT ON (unit.ord) ch.id::text AS chunk_id, unit.citation, ch.context_header, ch.content,
       t.lang, unit.validity::text AS validity, unit.version_status, unit.source_trust_class,
       0.0::float8 AS score
FROM unit
JOIN unit_texts t ON t.version_id = unit.version_id AND t.lang = %(lang)s
JOIN chunks ch    ON ch.unit_text_id = t.id
ORDER BY unit.ord, ch.seq
"""

_CITING_CHUNKS_SQL = """
SELECT ch.id::text AS chunk_id, ch.content, u.citation, u.instrument_id::text AS instrument_id,
       lower(v.validity) AS valid_from
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
WHERE ch.id = ANY(%(ids)s::uuid[])
"""


def _same_act_refs(content: str) -> list[str]:
    """Article numbers `content` names in its own act, in text order."""
    refs: list[str] = []
    for match in _SAME_ACT_REF.finditer(content):
        if _OTHER_ACT_AFTER.match(content[match.end() : match.end() + 40]):
            continue
        if match.group(1) not in refs:
            refs.append(match.group(1))
    return refs


def same_act_articles(conn: psycopg.Connection, lang: str, chunk_ids: list[str]) -> list[RetrievalHit]:
    """The articles of the same act a retrieved article refers to.

    A décret states the amount in one article and whom it is for in another:
    «Le montant de l'aide mentionnée à l'article 1er est égal à 152,45 euros»
    (décret n° 2025-1212, art. 2) — art. 1 lists the ASS among the
    allocations. On the 6 Nov batch art. 2 was retrieved and art. 1 was not,
    and all four prime-de-Noël amounts came back not_found, the model unable
    to tie 152,45 € to the ASS. The referenced article is read in its version
    in force when the citing one starts: art. 1 enters into force with art. 2,
    in December, after the reference date. Hits are "located".
    """
    if not chunk_ids:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(_CITING_CHUNKS_SQL, {"ids": chunk_ids}).fetchall()
    rank = {chunk_id: i for i, chunk_id in enumerate(chunk_ids)}
    rows.sort(key=lambda r: rank[r["chunk_id"]])
    lookups: list[tuple[str, str, date]] = []
    for row in rows:
        own = (row["citation"] or "").rsplit("art. ", 1)[-1]
        for token in [t for t in _same_act_refs(row["content"] or "") if t != own][:SAME_ACT_PER_ARTICLE]:
            lookup = (row["instrument_id"], rf"art\. {token}($|[^0-9A-Za-z])", row["valid_from"])
            if lookup not in lookups:
                lookups.append(lookup)
    if not lookups:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        hits = cur.execute(
            _SAME_ACT_UNITS_SQL,
            {
                "lang": lang,
                "instrument_ids": [l[0] for l in lookups],
                "patterns": [l[1] for l in lookups],
                "dates": [l[2] for l in lookups],
            },
        ).fetchall()
    seen = set(chunk_ids)
    found: list[RetrievalHit] = []
    for hit in hits:
        if hit["chunk_id"] in seen:
            continue
        seen.add(hit["chunk_id"])
        found.append(RetrievalHit(method="located", **hit))
        if len(found) >= SAME_ACT_MAX:
            break
    return found


#: Code articles whose implementing acts are looked up (best-ranked first),
#: acts kept per article, and the most a call adds; how far back an act's
#: version may have entered into force. Twenty, not six: ranked on «RSA,
#: increment per additional child», six family-benefit articles came first
#: and CASF L. 262-2 — whose 2025 decree states 646,52 € — was the 16th
#: ($bsa00_amt4 not_found, 5 Nov batch); the found chunks stay capped and
#: in article order, and only the first IMPLEMENTING_NEAREST_ACTS acts bring
#: their nearest chunks.
IMPLEMENTING_ARTICLES = 20
IMPLEMENTING_NEAREST_ACTS = 6
IMPLEMENTING_PER_ARTICLE = 3  # the 2025 RSA decree and its Mayotte twin share a date
IMPLEMENTING_MAX = 6
IMPLEMENTING_LOOKBACK = timedelta(days=365)

# Recent non-code act versions in scope with a chunk naming one of the article
# numbers; which code each mention names is decided in Python (_code_refs).
_IMPLEMENTING_SQL = """
SELECT DISTINCT ON (ch.id) ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content,
       t.lang, v.validity::text AS validity, v.version_status, i.source_trust_class,
       0.0::float8 AS score, i.id::text AS instrument_id
FROM legal_unit_versions v
JOIN legal_units u   ON u.id = v.legal_unit_id
JOIN instruments i   ON i.id = u.instrument_id
JOIN jurisdictions j ON j.id = i.jurisdiction_id
JOIN unit_texts t    ON t.version_id = v.id AND t.lang = %(lang)s
JOIN chunks ch       ON ch.unit_text_id = t.id
WHERE v.validity @> %(as_of)s::date AND lower(v.validity) >= %(since)s::date
  AND i.instrument_type <> 'code' AND i.source_trust_class <> 'context'
  AND j.code = ANY(%(jurisdictions)s::text[])
  AND ch.content ~ ANY(%(patterns)s::text[])
ORDER BY ch.id
"""


# The chunks of one act in force on as_of, nearest to the query vector first.
_ACT_NEAREST_SQL = """
SELECT ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,
       v.validity::text AS validity, v.version_status, i.source_trust_class, 0.0::float8 AS score
FROM legal_units u
JOIN instruments i         ON i.id = u.instrument_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
JOIN unit_texts t          ON t.version_id = v.id AND t.lang = %(lang)s
JOIN chunks ch             ON ch.unit_text_id = t.id
JOIN embeddings e          ON e.chunk_id = ch.id AND e.model_id = %(model_id)s
WHERE u.instrument_id = %(instrument_id)s::uuid AND v.validity @> %(as_of)s::date
ORDER BY e.embedding <=> %(qvec)s::halfvec(1024)
LIMIT %(k)s
"""
# Cosine distance of given chunks to the query vector.
_CHUNK_DISTANCE_SQL = """
SELECT e.chunk_id::text AS chunk_id, (e.embedding <=> %(qvec)s::halfvec(1024))::float8 AS d
FROM embeddings e
WHERE e.chunk_id = ANY(%(ids)s::uuid[]) AND e.model_id = %(model_id)s
"""
#: Further chunks of each implementing act, nearest to the query.
IMPLEMENTING_NEAREST = 2


def implementing_acts(
    conn: psycopg.Connection,
    country: Scope,
    lang: str,
    as_of: date,
    chunk_ids: list[str],
    query_vector: str | None = None,
    model_id: int = 1,
) -> list[RetrievalHit]:
    """The recent acts that apply a retrieved code article: references followed backwards.

    A code article says its figure is «fixé par décret» and the decree that
    fixes this year's figure names the article: «Le montant forfaitaire …
    mentionné à l'article L. 262-2 du code de l'action sociale et des
    familles … est porté à 646,52 euros» (décret du 28 mars 2025). Ranked on
    the RSA parameter's description, L. 262-2 came back and the decree did
    not (4 Nov run, $bsa00_amt3 not_found). For the best-ranked code articles,
    the non-code act versions in force on ``as_of``, entered into force in
    the year before it, whose text names that article of that code; most
    recent first, the best-ranked article's first, "located". With a query
    vector, each act found also brings its IMPLEMENTING_NEAREST chunks
    nearest to the query: an instruction names R. 522-2 in its «Textes de
    référence» and states the complément familial ceilings three sections
    on (DSS/2B/2024/181). Not later in the year: the arrêté of 26 December
    2025 fixing the 2026 PAJE ceilings names L. 531-2 too.
    """
    base = {"jurisdictions": scope_codes(country), "lang": lang, "as_of": as_of}
    with conn.cursor(row_factory=dict_row) as cur:
        rows = cur.execute(_REF_CHUNKS_SQL, {"ids": chunk_ids}).fetchall()
        codes = {r["instrument_id"]: r["title"] for r in cur.execute(_SCOPE_CODES_SQL, base).fetchall()}
    rank = {chunk_id: i for i, chunk_id in enumerate(chunk_ids)}
    articles: list[tuple[str, str]] = []
    for row in sorted(rows, key=lambda r: rank[r["chunk_id"]]):
        token = (row["citation"] or "").rsplit("art. ", 1)[-1]
        article = (row["instrument_id"], token)
        if row["is_code"] and re.fullmatch(r"[LRD]\d+(?:-\d+)+", token) and article not in articles:
            articles.append(article)
    articles = articles[:IMPLEMENTING_ARTICLES]
    if not articles or not codes:
        return []
    patterns = sorted({rf"\m{t[0]}\.? ?{re.escape(t[1:])}($|[^0-9-])" for _, t in articles})
    with conn.cursor(row_factory=dict_row) as cur:
        candidates = cur.execute(
            _IMPLEMENTING_SQL,
            {**base, "since": as_of - IMPLEMENTING_LOOKBACK, "patterns": patterns},
        ).fetchall()
    candidates.sort(key=lambda r: r["validity"], reverse=True)  # '[2025-03-30,)' sorts by its start
    named = [(row, set(_code_refs(row["content"] or "", None, codes))) for row in candidates]
    matched: list[dict] = []
    for article in articles:  # the best-ranked article's acts first
        acts = [row for row, refs in named if article in refs]
        matched += [row for row in acts[:IMPLEMENTING_PER_ARTICLE] if row not in matched]
    if query_vector is not None and matched:
        # Twenty articles name more acts than the caps keep: the nearest to
        # the query win — the prime d'activité decree (L. 842-3, 19th
        # article) over the family-benefit arrêtés of the first six.
        with conn.cursor(row_factory=dict_row) as cur:
            distance = {
                r["chunk_id"]: r["d"]
                for r in cur.execute(
                    _CHUNK_DISTANCE_SQL,
                    {"ids": [r["chunk_id"] for r in matched], "qvec": query_vector, "model_id": model_id},
                ).fetchall()
            }
        matched.sort(key=lambda r: distance.get(r["chunk_id"], 2.0))
    known = set(chunk_ids)
    found: list[RetrievalHit] = []
    instruments: list[str] = []
    for row in matched:
        # An act already retrieved still brings its nearest chunks: the
        # instruction's «Textes de référence» chunk ranked, its ceilings did not.
        if row["instrument_id"] not in instruments:
            instruments.append(row["instrument_id"])
        if row["chunk_id"] in known:
            continue
        known.add(row["chunk_id"])
        found.append(RetrievalHit(method="located", **{c: v for c, v in row.items() if c != "instrument_id"}))
    found = found[:IMPLEMENTING_MAX]
    if query_vector is not None:
        for instrument in instruments[:IMPLEMENTING_NEAREST_ACTS]:
            params = {**base, "instrument_id": instrument, "qvec": query_vector, "model_id": model_id,
                      "k": IMPLEMENTING_NEAREST + 1}
            with conn.cursor(row_factory=dict_row) as cur:
                near = [r for r in cur.execute(_ACT_NEAREST_SQL, params).fetchall() if r["chunk_id"] not in known]
            for row in near[:IMPLEMENTING_NEAREST]:
                known.add(row["chunk_id"])
                found.append(RetrievalHit(method="located", **row))
    return found


def _citation_pattern(token: str) -> str:
    """POSIX regex matching `token` as a whole article number inside a citation."""
    return r"(^|[^0-9A-Za-z.])" + re.escape(token) + r"($|[^0-9A-Za-z.\-])"


def locate_named_units(
    conn: psycopg.Connection,
    country: Scope,
    lang: str,
    as_of: date,
    need: str,
    k: int = 6,
    held_instrument_ids: list[str] | None = None,
) -> list[RetrievalHit]:
    """Chunks of the source an analyst NAMED, looked up rather than ranked.

    A proposal that answers found=false names what it lacks («artículo 66 de la
    Ley 35/2006», «article D. 633-3 du code de la sécurité sociale», «Finance
    Act 2024 … amending section 461»). The gap-fill scout treats that as a
    corpus gap, but on the 2026-09-09 eval six of nine such misses were acts
    already held — the framed query, written from the parameter's EUROMOD
    description, simply ranked the article below k (LIRPF art. 66 not in the
    top 60; CGI-style code articles at rank 17–31). Web search and ingest can
    do nothing for those; a direct lookup can, and it needs no ranking:

    1. the act — every instrument in scope whose title the need contains
       (pg_trgm `word_similarity`, NAMED_ACT_MIN_SCORE), up to three;
    2. the article — every legal unit whose citation carries an article number
       the need spells out, scoped to those acts when any matched (fallback for
       the ES paragraph idiom: «66.2» is article 66);
    3. failing an article, the analyst's own words searched inside each named
       act alone (FTS), two chunks per act — «Finance Act 2024 … personal tax
       credit» finds s. 3 without knowing its number.

    When the need names no act by title, step 3 searches inside the acts the
    retrieved chunks already come from (``held_instrument_ids``): the analyst
    who writes «l'article 34 dit que le taux résulte d'un pourcentage d'appel,
    mais les extraits ne donnent pas ce pourcentage» is describing a gap INSIDE
    the act it is reading — the AGIRC-ARRCO ANI, whose art. 36 («Un pourcentage
    d'appel, fixé à 127 %») retrieval never ranked in (3 Nov benchmark, four
    tscerpi rates not_found with arts. 34, 35 and 38 in hand).

    4. nothing found that entered into force in the year before ``as_of``:
       the need's words, any of them, ranked over the texts in force on
       ``as_of`` that did. «l'arrêté portant revalorisation, au 1er
       avril 2025, de la BMAF» names no title we hold — the amount is in an
       instruction «relative à la revalorisation au 1er avril 2025 des
       prestations familiales» (5 Nov re-run, every BMAF-based amount
       not_found with the instruction in the corpus); this year's figure is
       in this year's text.

    As-of and jurisdiction scoping are the retrieval CTE's; hits come back
    with method="located" so the trace shows they were not ranked in.
    """
    jurisdictions = scope_codes(country)
    base = {"jurisdictions": jurisdictions, "lang": lang, "as_of": as_of, "need": need}
    with conn.cursor(row_factory=dict_row) as cur:
        acts = cur.execute(
            _NAMED_INSTRUMENTS_SQL, {**base, "min_score": NAMED_ACT_MIN_SCORE}
        ).fetchall()
    act_ids = [act["instrument_id"] for act in acts] or None
    search_acts = acts
    if not acts and held_instrument_ids:
        with conn.cursor(row_factory=dict_row) as cur:
            search_acts = cur.execute(
                "SELECT id::text AS instrument_id, title_search FROM instruments "
                "WHERE id = ANY(%(ids)s::uuid[]) AND source_trust_class <> 'context'",
                {"ids": held_instrument_ids},
            ).fetchall()
    hits: dict[str, RetrievalHit] = {}

    def lookup(token: str, scoped: bool) -> None:
        params = {
            **base,
            "pattern": _citation_pattern(token),
            "instrument_ids": act_ids if scoped else None,
            "k": k,
        }
        with conn.cursor(row_factory=dict_row) as cur:
            rows = cur.execute(_NAMED_UNIT_SQL, params).fetchall()
        for row in rows:
            hits.setdefault(row["chunk_id"], RetrievalHit(method="located", **row))

    tokens = _article_tokens(need)
    for token in tokens:
        lookup(token, scoped=act_ids is not None)
    if not hits and act_ids:
        for token in tokens:
            head = re.match(r"[A-Za-z]?\d+", token)
            if head and head.group(0) != token:
                lookup(head.group(0), scoped=True)
    if not hits and search_acts:
        for act in search_acts:
            # The act's own title words match all of its chunks: search the
            # rest of the need — the article number, the concept, the year.
            # (A need that IS the title — «l'arrêté fixant le plafond de la
            # sécurité sociale pour 2025» — keeps nothing; then the whole need.)
            title_words = set(re.findall(r"\w{2,}", (act["title_search"] or "").lower()))
            terms = [t for t in re.findall(r"\w{2,}", need.lower()) if t not in title_words]
            queries = [" OR ".join(dict.fromkeys(terms))] if terms else []
            queries.append(_fts_query(need))
            for fts_q in queries:
                params = {**base, "instrument_id": act["instrument_id"], "fts_q": fts_q, "k": 3}
                with conn.cursor(row_factory=dict_row) as cur:
                    rows = cur.execute(_NAMED_INSTRUMENT_FTS_SQL, params).fetchall()
                if rows:
                    for row in rows:
                        hits.setdefault(row["chunk_id"], RetrievalHit(method="located", **row))
                    break
    since = as_of - RECENT_LOOKBACK
    recent_found = any(_entered_since(h.validity, since) for h in hits.values())
    found = list(hits.values())[:k]
    params = {**base, "since": since, "k": k}
    with conn.cursor(row_factory=dict_row) as cur:
        recent = [r for r in cur.execute(_RECENT_FTS_SQL, params).fetchall() if r["chunk_id"] not in hits]
    # Nothing recent found: this year's texts fill the slots. Something
    # recent found: they still get RECENT_EXTRA slots of their own — the
    # PAJE arrêté of December 2024 is recent, and the ceiling table of
    # instruction DSS/2B/2024/181 the need asked for never came back.
    room = k if not recent_found else RECENT_EXTRA
    found += [RetrievalHit(method="located", **row) for row in recent[: max(0, min(room, k + RECENT_EXTRA - len(found)))]]
    return found


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
    an otherwise verbatim quote, and so is whitespace a PDF extraction put
    between two letters of one word: DSS/2B/2025/38 reads «prestati ons»
    (a split "ti" ligature), and every quote of its BMAF sentence failed on
    the 5 Nov re-run with the right amount proposed. Between digits it is
    never ignored: «25 %» must not match two table cells «2» and «5».
    Punctuation at the quote's two ends is not part of the check either.
    """
    row = conn.execute(
        "SELECT content, char_start FROM chunks WHERE id = %s::uuid", (chunk_id,)
    ).fetchone()
    if row is None or not extract:
        return None
    span = quote_span(row["content"], extract)
    base = row["char_start"] or 0
    return (base + span[0], base + span[1]) if span is not None else None


def quote_span(content: str, extract: str) -> tuple[int, int] | None:
    """Where `extract` sits in `content` under verify_extract's rules, else None."""
    if not extract:
        return None
    idx = content.find(extract)
    if idx >= 0:
        return (idx, idx + len(extract))
    for quote in dict.fromkeys((extract, extract.strip(_QUOTE_EDGE_PUNCTUATION))):
        if not quote.strip():
            continue
        pattern = re.compile(r"\s+".join(re.escape(part) for part in quote.split()))
        match = pattern.search(content) or re.search(_split_word_pattern(quote), content)
        if match:
            return (match.start(), match.end())
    return None


#: Punctuation a quote may end (or start) on that the text does not: the model
#: closes «… deux personnes ; 3° A 16,5 %» on a full stop, or wraps it in «».
#: Stripped from the ends only — every word in between must still match.
_QUOTE_EDGE_PUNCTUATION = " \t\n.;:,«»\"“”'’"


def _split_word_pattern(extract: str) -> str:
    """`extract` as a regex in which whitespace may also fall between two letters."""
    parts: list[str] = []
    for word in extract.split():
        letters = [re.escape(c) + (r"\s*" if c.isalpha() and n.isalpha() else "") for c, n in zip(word, word[1:])]
        parts.append("".join(letters) + re.escape(word[-1]))
    return r"\s+".join(parts)


def closest_passage(content: str, extract: str) -> str | None:
    """The passage of a chunk that a non-verbatim extract was trying to quote.

    Feedback for the retry, never a substitute for the check: models "tidy"
    legal French (la contribution → la contribution sociale, a dropped «à
    charge», an added closing »), and told only "not verbatim" they repeat the
    same quote. The span runs from the first to the last stretch of 6+
    characters the extract shares with the chunk, widened to whole words;
    None when under half the extract matches or the matches are scattered.
    """
    if not extract.strip():
        return None
    matcher = difflib.SequenceMatcher(None, content, extract, autojunk=False)
    blocks = [b for b in matcher.get_matching_blocks() if b.size >= 6]
    if sum(b.size for b in blocks) < len(extract) / 2:
        return None
    start, end = blocks[0].a, blocks[-1].a + blocks[-1].size
    if end - start > 2 * len(extract) + 100:
        return None
    while start > 0 and not content[start - 1].isspace():
        start -= 1
    while end < len(content) and not content[end].isspace():
        end += 1
    return content[start:end]
