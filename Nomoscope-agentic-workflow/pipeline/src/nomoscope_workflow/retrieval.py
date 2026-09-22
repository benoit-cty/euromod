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

import re
from collections.abc import Sequence
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
) -> list[RetrievalHit]:
    """Citation fast path first, then hybrid; dedup by chunk_id, fast-path wins.

    ``country`` is a jurisdiction scope (see ``jurisdiction_scope``); the
    law language is the country's, i.e. the scope's first code.
    """
    lang = LANG_BY_COUNTRY.get(scope_codes(country)[0], "en")
    merged: dict[str, RetrievalHit] = {}
    for hit in citation_fast_path(conn, country, lang, as_of, citations, cfg.retrieval_k):
        merged[hit.chunk_id] = hit
    query_vector = (
        query_encoder.encode(query, cfg.database_url) if cfg.embedding_model_id != 99 else None
    )
    for hit in hybrid_search(
        conn, country, lang, as_of, query, cfg.embedding_model_id, cfg.retrieval_k, query_vector
    ):
        merged.setdefault(hit.chunk_id, hit)
    return list(merged.values())[: cfg.retrieval_k]


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
    if not hits and act_ids:
        for act in acts:
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
    return list(hits.values())[:k]


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
