"""Locating a source the analyst named: act by number or title, article by
number, words inside the named act, recent texts, the article between two held
ones (split out of retrieval.py, code audit 4)."""

from __future__ import annotations

import re
from datetime import date, timedelta

import psycopg

from .corpus import _LIVE_VERSION_CTE, HIT_COLUMNS, Scope, _fts_query, fetch_dicts, scope_codes
from .schema import RetrievalHit

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

#: An act number the need spells out: «Ley 35/2006», «Real Decreto 439/2007»,
#: «loi n° 2025-127». When an act in scope carries it, that act IS the one
#: named: Ley 18/1991 «del Impuesto sobre la Renta de las Personas Físicas»
#: scores 0.72 on title words against a need naming Ley 35/2006 (0.47).
_ACT_NUMBER = re.compile(r"\b(\d{1,5}/\d{4})\b|\bn[°ºo]\s*(\d{4}-\d{1,5})\b", re.IGNORECASE)


def act_numbers(need: str) -> list[str]:
    """The act numbers a need names («35/2006», «2025-127»), in order."""
    return list(dict.fromkeys(a or b for a, b in _ACT_NUMBER.findall(need)))


_NAMED_INSTRUMENTS_SQL = """
SELECT i.id::text AS instrument_id, i.national_id, i.title_search,
       word_similarity(i.title_search, %(need)s)::float8 AS score,
       EXISTS (SELECT 1 FROM unnest(%(numbers)s::text[]) n
               WHERE i.title_search ~ ('(^|[^0-9])' || n || '([^0-9]|$)')) AS by_number
FROM instruments i
JOIN jurisdictions j ON j.id = i.jurisdiction_id
WHERE j.code = ANY(%(jurisdictions)s::text[])
  AND i.source_trust_class <> 'context'
  AND (word_similarity(i.title_search, %(need)s) >= %(min_score)s
       OR EXISTS (SELECT 1 FROM unnest(%(numbers)s::text[]) n
                  WHERE i.title_search ~ ('(^|[^0-9])' || n || '([^0-9]|$)')))
ORDER BY by_number DESC, score DESC
LIMIT %(limit)s
"""

#: Acts kept as "the act the need names".
NAMED_ACT_LIMIT = 3
#: Title candidates read before the header fragments among them are dropped.
_NAMED_ACT_CANDIDATES = 15


def named_acts(candidates: list[dict], limit: int = NAMED_ACT_LIMIT) -> list[dict]:
    """The acts a need names, without the titles that are no name at all.

    `word_similarity(title, need)` asks how much of the TITLE the need contains,
    so a title that is only the head of a real one scores 1.0 against every
    need: three Lithuanian acts stored as «LIETUVOS RESPUBLIKOS» (the parser
    kept the header's first line) outranked «LIETUVOS RESPUBLIKOS IŠMOKŲ
    VAIKAMS ĮSTATYMAS» (0.93) for «… išmokų vaikams įstatymo 6 straipsnis», the
    lookup returned art. 6 of the Social Services Act, and ten Lithuanian
    parameters proposed on 14 Nov 2026 were not_found on the 17 Nov panel.
    A candidate is dropped when its title is the leading words of another
    candidate's longer title, or when several candidates share it — a title
    two acts carry names neither. An act named by number is never dropped.
    """
    words = [tuple((c.get("title_search") or "").lower().split()) for c in candidates]
    kept = []
    for candidate, title in zip(candidates, words):
        fragment = any(len(other) > len(title) and other[: len(title)] == title for other in words)
        if candidate.get("by_number") or (title and not fragment and words.count(title) == 1):
            kept.append(candidate)
    return kept[:limit]


_NAMED_UNIT_SQL = f"""
WITH {_LIVE_VERSION_CTE}
SELECT {HIT_COLUMNS},
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
_RECENT_FTS_SQL = f"""
WITH q AS (
  SELECT to_tsquery(c.config, string_agg(quote_literal(l.lexeme), ' | ')) AS tq
  FROM lang_fts_config c, unnest(to_tsvector(c.config, %(need)s)) AS l
  WHERE c.lang = %(lang)s
  GROUP BY c.config
)
SELECT {HIT_COLUMNS},
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
SELECT {HIT_COLUMNS},
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


#: Chunks of other acts kept for naming the article a need names (step 2b).
DELEGATED_MAX = 3

# Step 2b: the texts of OTHER acts, in force on as_of, that name this article
# of this act in one clause — «artikel 11, derde lid, van de Wet financiering
# sociale verzekeringen», «section 461 of the Taxes Consolidation Act 1997».
# Ranked on the need's words, then newest first.
_DELEGATED_SQL = f"""
WITH {_LIVE_VERSION_CTE}
SELECT {HIT_COLUMNS},
       ts_rank_cd(ch.tsv, websearch_to_tsquery(ch.search_config, %(fts_q)s), 1|32)::float8 AS score
FROM chunks ch
JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN live_version lv       ON lv.version_id = v.id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id
WHERE t.lang = %(lang)s
  AND i.id <> %(instrument_id)s::uuid
  AND ch.content ~* %(pattern)s
ORDER BY score DESC, lower(v.validity) DESC
LIMIT %(k)s
"""


def _delegation_patterns(token: str, title: str, need: str) -> list[str]:
    """POSIX regexes for «<article> … of <act>» in one clause, the tightest first.

    When the need itself spells the clause («artikel 11, derde lid, van de Wet
    financiering sociale verzekeringen») that exact wording is tried before the
    loose form: art. 11 has three paragraphs, each with its own regulation,
    and the loose form returned the AOW and Anw premium articles (first and
    second paragraph) for a need about the third.
    """
    words = r"\s+".join(re.escape(word) for word in title.split())
    head = r"\m" + re.escape(token) + r"($|[^0-9A-Za-z.\-])"
    patterns = []
    clause = re.search(re.escape(token) + r"(?![0-9A-Za-z.\-])([^.;]{0,80}?)" + re.escape(title), need, re.IGNORECASE)
    if clause and clause.group(1).strip(" ,"):
        between = r"\s+".join(re.escape(word) for word in clause.group(1).split())
        patterns.append(r"\m" + re.escape(token) + r"\s*" + between + r"\s*" + words)
    # The paragraph named right after the number, wherever the title stands
    # in the need: «Wet financiering sociale verzekeringen, artikel 11, derde lid, …».
    after = re.search(re.escape(token) + r"(?![0-9A-Za-z.\-])[\s,]*(\w+\s+\w+)", need, re.IGNORECASE)
    if after:
        qualifier = r"\s+".join(re.escape(word) for word in after.group(1).split())
        patterns.append(r"\m" + re.escape(token) + r"[\s,]*" + qualifier + r"\M[^.;]{0,80}" + words)
    patterns.append(head + r"[^.;]{0,80}" + words)
    return list(dict.fromkeys(patterns))


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
    rows = fetch_dicts(conn, _GAP_ARTICLES_SQL, params)
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
    rows = fetch_dicts(
        conn,
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
    )
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
       (pg_trgm `word_similarity`, NAMED_ACT_MIN_SCORE), up to three; an act
       whose number the need spells out («Ley 35/2006») wins outright;
    2. the article — every legal unit whose citation carries an article number
       the need spells out, scoped to those acts when any matched (fallback for
       the ES paragraph idiom: «66.2» is article 66);
    2b. the acts made under that article — up to DELEGATED_MAX chunks of other
       acts whose text names the article of the named act («Het
       premiepercentage, bedoeld in artikel 11, derde lid, van de Wet
       financiering sociale verzekeringen, wordt … vastgesteld op 9,65%»).
       The need said «de ministeriële regeling tot vaststelling van het
       premiepercentage … op grond van artikel 11, derde lid, van de Wet
       financiering sociale verzekeringen»: the lookup returned art. 11
       itself, already retrieved, and the Regeling vaststelling
       premiepercentage Wlz (0.72 on its title, behind three statutes the
       need mentions) was never read (24 Nov 2026, NL Wlz rate not_found);
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
    acts = named_acts(
        fetch_dicts(
            conn,
            _NAMED_INSTRUMENTS_SQL,
            {
                **base,
                "min_score": NAMED_ACT_MIN_SCORE,
                "numbers": act_numbers(need),
                "limit": _NAMED_ACT_CANDIDATES,
            },
        )
    )
    # An act the need names by number is the act: drop title look-alikes.
    if any(act["by_number"] for act in acts):
        acts = [act for act in acts if act["by_number"]]
    act_ids = [act["instrument_id"] for act in acts] or None
    search_acts = acts
    if not acts and held_instrument_ids:
        search_acts = fetch_dicts(
            conn,
            "SELECT id::text AS instrument_id, title_search FROM instruments "
            "WHERE id = ANY(%(ids)s::uuid[]) AND source_trust_class <> 'context'",
            {"ids": held_instrument_ids},
        )
    hits: dict[str, RetrievalHit] = {}

    def lookup(token: str, scoped: bool) -> None:
        params = {
            **base,
            "pattern": _citation_pattern(token),
            "instrument_ids": act_ids if scoped else None,
            "k": k,
        }
        rows = fetch_dicts(conn, _NAMED_UNIT_SQL, params)
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
    delegated: dict[str, RetrievalHit] = {}
    if hits:
        for act in acts:
            title = (act.get("title_search") or "").strip()
            if len(title.split()) < 2:
                continue  # a one-word title would match half the corpus
            for token in tokens:
                for pattern in _delegation_patterns(token, title, need):
                    params = {
                        **base,
                        "instrument_id": act["instrument_id"],
                        "pattern": pattern,
                        "fts_q": _fts_query(need),
                        "k": DELEGATED_MAX,
                    }
                    rows = [r for r in fetch_dicts(conn, _DELEGATED_SQL, params) if r["chunk_id"] not in hits]
                    for row in rows:
                        delegated.setdefault(row["chunk_id"], RetrievalHit(method="located", **row))
                    if rows:
                        break
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
                rows = fetch_dicts(conn, _NAMED_INSTRUMENT_FTS_SQL, params)
                if rows:
                    for row in rows:
                        hits.setdefault(row["chunk_id"], RetrievalHit(method="located", **row))
                    break
    since = as_of - RECENT_LOOKBACK
    recent_found = any(_entered_since(h.validity, since) for h in hits.values())
    found = list(hits.values())[:k]
    # Slots of their own: the named article fills k by itself when several
    # acts carry that number.
    ranked = sorted(delegated.values(), key=lambda h: h.score or 0.0, reverse=True)
    found += ranked[:DELEGATED_MAX]
    hits.update(delegated)
    params = {**base, "since": since, "k": k}
    recent = [r for r in fetch_dicts(conn, _RECENT_FTS_SQL, params) if r["chunk_id"] not in hits]
    # Nothing recent found: this year's texts fill the slots. Something
    # recent found: they still get RECENT_EXTRA slots of their own — the
    # PAJE arrêté of December 2024 is recent, and the ceiling table of
    # instruction DSS/2B/2024/181 the need asked for never came back.
    room = k if not recent_found else RECENT_EXTRA
    found += [
        RetrievalHit(method="located", **row) for row in recent[: max(0, min(room, k + RECENT_EXTRA - len(found)))]
    ]
    return found
