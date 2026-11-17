"""Country Reports: context, never evidence — the only sanctioned reader
(`country_report_search`) and the query enrichment drawn from them (split out
of retrieval.py, code audit 4)."""

from __future__ import annotations

import re
from datetime import date

import psycopg

from .schema import RetrievalHit
from .corpus import CHUNK_JOINS, HIT_COLUMNS, _fts_query, fetch_dicts

_CR_SEARCH_SQL = f"""
SELECT {HIT_COLUMNS},
       ts_rank_cd(ch.tsv, websearch_to_tsquery(ch.search_config, %(fts_q)s), 1|32)::float8 AS score
FROM chunks ch
{CHUNK_JOINS}
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
    rows = fetch_dicts(
        conn,
        _CR_SEARCH_SQL,
        {"country": country, "as_of": as_of, "fts_q": _fts_query(query), "k": k},
    )
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
