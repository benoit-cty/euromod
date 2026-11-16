"""Freshness canaries: known legal facts that tell a stale corpus from a current one.

Each adapter states, as `CanaryFact`s, citations whose latest version must
start on or after a known date (CGI art. 197 rewritten by LF 2025 from
16 February 2025). `check_canaries` looks each one up in the legislation DB:
an article whose newest version starts earlier means the corpus (or the
resolver that filled it) is stale for that year — the FR staleness trap the
facts were written for. Until 16 Nov 2026 no runner read them (code audit,
dead code); `cli canary` does now.

Matching is on the citation with case, punctuation and spacing folded
(«CGI art. 197» = «CGI, art. 197»), never on trigram similarity, which
equates «artikel 2.10» and «artikel 10.2». A fact naming a whole act («AOW»)
matches every unit whose citation starts with it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from psycopg import Connection

from nomotheca_ingest.core.ir import CanaryFact

_NORM = "btrim(regexp_replace(lower({x}), '[^[:alnum:]]+', ' ', 'g'))"

_LATEST_SQL = f"""
SELECT u.citation, max(lower(v.validity)) AS latest,
       {_NORM.format(x="u.citation")} = {_NORM.format(x="%(citation)s")} AS exact
FROM legal_units u
JOIN instruments i         ON i.id = u.instrument_id
JOIN jurisdictions j       ON j.id = i.jurisdiction_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id
WHERE (j.code = %(cc)s OR j.parent_id = (SELECT id FROM jurisdictions WHERE code = %(cc)s))
  AND i.source_trust_class <> 'context'
  AND u.citation IS NOT NULL
  AND ({_NORM.format(x="u.citation")} = {_NORM.format(x="%(citation)s")}
       OR {_NORM.format(x="u.citation")} LIKE {_NORM.format(x="%(citation)s")} || ' %%')
GROUP BY u.citation
"""


@dataclass(frozen=True, slots=True)
class CanaryResult:
    jurisdiction: str
    fact: CanaryFact
    matched: str | None       # the citation found (or the act's first unit)
    latest_start: date | None

    @property
    def status(self) -> str:
        """`ok`, `stale` (found, too old) or `missing` (not in the corpus)."""
        if self.latest_start is None:
            return "missing"
        return "ok" if self.latest_start >= self.fact.assert_latest_start_gte else "stale"


def check_fact(conn: Connection, jurisdiction: str, fact: CanaryFact) -> CanaryResult:
    rows = conn.execute(_LATEST_SQL, {"cc": jurisdiction.upper(), "citation": fact.citation}).fetchall()
    exact = [r for r in rows if r[2]]
    chosen = exact or rows
    if not chosen:
        return CanaryResult(jurisdiction.upper(), fact, None, None)
    latest = max(r[1] for r in chosen)
    matched = exact[0][0] if exact else f"{fact.citation} ({len(rows)} units)"
    return CanaryResult(jurisdiction.upper(), fact, matched, latest)


def check_canaries(conn: Connection, jurisdictions: list[str]) -> list[CanaryResult]:
    from nomotheca_ingest.countries.registry import get_adapter

    results = []
    for code in jurisdictions:
        for fact in get_adapter(code).canary_facts():
            results.append(check_fact(conn, code, fact))
    return results
