"""Following references: code cross-references (L. -> R./D.), articles of the
same act, implementing acts naming a retrieved article (split out of
retrieval.py, code audit 4)."""

from __future__ import annotations

import re
from datetime import date, timedelta

import psycopg
from psycopg.rows import dict_row

from .schema import RetrievalHit
from . import idiom
from .corpus import article_label, CHUNK_JOINS, HIT_COLUMNS, Scope, scope_codes
from .locate import _citation_pattern

_CODE_ARTICLE_REF = idiom.FR_CODE_ARTICLE_REF
#: Explicit references followed per article (regulatory R./D. ones first:
#: they carry the figures), and the most a call adds.
CROSS_REF_PER_ARTICLE = 4
CROSS_REF_MAX = 8

_REF_CHUNKS_SQL = f"""
SELECT ch.id::text AS chunk_id, ch.content, u.citation, i.id::text AS instrument_id,
       i.instrument_type = 'code' AS is_code
FROM chunks ch
{CHUNK_JOINS}
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
        if after is None and idiom.FR_SAME_CODE in tail:
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
            own = article_label(row["citation"]) if row["is_code"] else ""
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


_SAME_ACT_REF = idiom.FR_SAME_ACT_REF
_OTHER_ACT_AFTER = idiom.FR_OTHER_ACT_AFTER
SAME_ACT_PER_ARTICLE = 3
SAME_ACT_MAX = 6
#: Backwards: the retrieved articles whose citing articles are looked up
#: (best-ranked first), citing articles kept per article, and the most added.
SAME_ACT_CITED = 10
SAME_ACT_CITING_PER_ARTICLE = 2
SAME_ACT_CITING_MAX = 4

# Per (act, article) lookup: the act's other articles in force on the date the
# cited article's version starts whose text names it; which mentions are
# really to this act is decided in Python (_same_act_refs).
_SAME_ACT_CITING_SQL = """
WITH wanted AS (
  SELECT * FROM unnest(%(instrument_ids)s::uuid[], %(patterns)s::text[], %(dates)s::date[], %(owns)s::text[])
         WITH ORDINALITY AS w(instrument_id, pattern, at, own, ord)
)
SELECT DISTINCT ON (w.ord, ch.id) w.ord, ch.id::text AS chunk_id, u.citation, ch.context_header,
       ch.content, t.lang, v.validity::text AS validity, v.version_status, i.source_trust_class,
       0.0::float8 AS score
FROM wanted w
JOIN legal_units u         ON u.instrument_id = w.instrument_id AND u.citation <> w.own
JOIN instruments i         ON i.id = u.instrument_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id AND v.validity @> w.at
JOIN unit_texts t          ON t.version_id = v.id AND t.lang = %(lang)s
JOIN chunks ch             ON ch.unit_text_id = t.id
WHERE i.instrument_type <> 'code' AND i.source_trust_class <> 'context' AND ch.content ~* w.pattern
ORDER BY w.ord, ch.id
"""

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
        own = article_label(row["citation"])
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
    return found + _same_act_citing(conn, lang, rows, seen)


def _same_act_citing(conn: psycopg.Connection, lang: str, rows: list[dict], seen: set[str]) -> list[RetrievalHit]:
    """The articles of the same act that name a retrieved one: references followed backwards.

    The agreement states the rule where the article it modifies is not:
    «Un pourcentage d'appel, fixé à 127 %, est appliqué aux taux visés à
    l'article 35» (ANI AGIRC-ARRCO du 17 novembre 2017, art. 36). Art. 35 was
    retrieved, art. 36 was not, and the AGIRC-ARRCO schedules came back
    not_found for want of the call rate (7 Nov batch). Codes are left out:
    their articles are numbered L./R./D. and followed by
    ``cross_referenced_articles``.
    """
    lookups: list[tuple[str, str, date, str, str]] = []
    for row in rows[:SAME_ACT_CITED]:
        own = article_label(row["citation"])
        number = re.fullmatch(r"(\d+)(?:\s?er)?", own)
        if number is None:
            continue
        token = number.group(1)
        lookup = (row["instrument_id"], rf"\marticles?\s+{token}(\s?er)?\M", row["valid_from"], row["citation"], token)
        if lookup not in lookups:
            lookups.append(lookup)
    if not lookups:
        return []
    with conn.cursor(row_factory=dict_row) as cur:
        hits = cur.execute(
            _SAME_ACT_CITING_SQL,
            {
                "lang": lang,
                "instrument_ids": [l[0] for l in lookups],
                "patterns": [l[1] for l in lookups],
                "dates": [l[2] for l in lookups],
                "owns": [l[3] for l in lookups],
            },
        ).fetchall()
    def distance(hit: dict) -> tuple[int, int]:
        # Nearest article first: the rule for art. 35 sits in art. 36, not in
        # art. 13 or 49, which name it too.
        number = re.search(r"art\. (\d+)", hit["citation"] or "")
        cited = int(lookups[hit["ord"] - 1][4])
        return hit["ord"], abs(int(number.group(1)) - cited) if number else 10_000

    hits.sort(key=distance)
    found: list[RetrievalHit] = []
    kept: dict[int, int] = {}
    for hit in hits:
        ord_ = hit.pop("ord")
        token = lookups[ord_ - 1][4]
        if hit["chunk_id"] in seen or token not in _same_act_refs(hit["content"] or ""):
            continue
        if kept.get(ord_, 0) >= SAME_ACT_CITING_PER_ARTICLE:
            continue
        kept[ord_] = kept.get(ord_, 0) + 1
        seen.add(hit["chunk_id"])
        found.append(RetrievalHit(method="located", **hit))
        if len(found) >= SAME_ACT_CITING_MAX:
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
_ACT_NEAREST_SQL = f"""
SELECT {HIT_COLUMNS}, 0.0::float8 AS score
FROM legal_units u
JOIN instruments i         ON i.id = u.instrument_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
JOIN unit_texts t          ON t.version_id = v.id AND t.lang = %(lang)s
JOIN chunks ch             ON ch.unit_text_id = t.id
JOIN embeddings e          ON e.chunk_id = ch.id AND e.model_id = %(model_id)s
WHERE u.instrument_id = %(instrument_id)s::uuid AND v.validity @> %(as_of)s::date
-- `+ 0`: never the bare `embedding <=> q` the HNSW index could serve (it would
-- return the corpus's nearest and filter to this act afterwards).
ORDER BY (e.embedding <=> %(qvec)s::halfvec(1024)) + 0
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
        token = article_label(row["citation"])
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
