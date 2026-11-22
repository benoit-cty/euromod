"""Corpus readiness for a system year: are the finance-act vintages in place?

Verifying system year Y needs, per parameter family:
  - in_force parameters: the act FOR Y (voted late Y-1 / early Y), which
    governs them during Y;
  - temporal_basis=income_year parameters (FR income-tax family): the act
    carrying the barème the law labels "income income_year_for(Y)", i.e. the
    act FOR income_year_for(Y) + 1. With INCOME_YEAR_OFFSET = -1 that is the
    act for Y too (LF 2025 for system year 2025), so one vintage serves both.
    Before 16 Nov 2026 this module still used the pre-offset model and probed
    the act for Y+1, announcing false "provisional" parameters (code audit D3).

This module answers, per vintage: is the act ingested, and are its chunks
embedded (chunks without vectors are invisible to the vector leg of
retrieval)? The result feeds the CLI banner printed before a run, so "N
parameters will be provisional" is said once, up front, instead of N times in
critique failures.

Probes are per-country; countries without one simply report nothing.
"""

from __future__ import annotations

from dataclasses import dataclass

import psycopg
from psycopg.rows import dict_row

from .schema import income_year_for

# How to recognise the annual budget act of vintage V in instrument titles.
# The pattern receives the vintage year via format(); matched against
# instruments.title_search (all language variants concatenated).
_BUDGET_ACT_TITLE = {
    "FR": r"finances pour {year}(\D|$)",
}

_STATUS_SQL = """
SELECT i.national_id AS national_id, i.title_search AS title,
       count(c.id)          AS chunks,
       count(e.chunk_id)    AS embedded
FROM instruments i
JOIN jurisdictions j ON j.id = i.jurisdiction_id
LEFT JOIN legal_units lu ON lu.instrument_id = i.id
LEFT JOIN legal_unit_versions v ON v.legal_unit_id = lu.id
LEFT JOIN unit_texts ut ON ut.version_id = v.id
LEFT JOIN chunks c ON c.unit_text_id = ut.id
LEFT JOIN embeddings e ON e.chunk_id = c.id
WHERE j.code = %(country)s AND i.title_search ~* %(pattern)s
GROUP BY i.id, i.national_id, i.title_search
ORDER BY count(c.id) DESC
"""


@dataclass
class ActStatus:
    """One finance-act vintage as seen by the corpus."""

    vintage: int  # the year the act is FOR (LF pour <vintage>)
    roles: tuple[str, ...]  # 'in_force' and/or 'income_year' — which parameters need it
    national_id: str | None = None
    title: str | None = None
    chunks: int = 0
    embedded: int = 0

    @property
    def present(self) -> bool:
        return self.national_id is not None

    @property
    def backlog(self) -> int:
        """Chunks not yet embedded — invisible to vector retrieval."""
        return self.chunks - self.embedded


def finance_act_readiness(conn: psycopg.Connection, country: str, year: int) -> list[ActStatus]:
    """Corpus status of the finance-act vintages system year `year` needs.

    Empty list when no probe is configured for the country.
    """
    pattern = _BUDGET_ACT_TITLE.get(country)
    if pattern is None:
        return []
    return [_status(conn, country, pattern, vintage, roles) for vintage, roles in vintages_for(year)]


def vintages_for(year: int) -> list[tuple[int, tuple[str, ...]]]:
    """The finance-act vintages system year `year` needs, with who needs each."""
    needs: dict[int, list[str]] = {}
    needs.setdefault(year, []).append("in_force")
    needs.setdefault(income_year_for(year) + 1, []).append("income_year")
    return [(vintage, tuple(roles)) for vintage, roles in sorted(needs.items())]


def _status(conn: psycopg.Connection, country: str, pattern: str, vintage: int, roles: tuple[str, ...]) -> ActStatus:
    status = ActStatus(vintage=vintage, roles=roles)
    with conn.cursor(row_factory=dict_row) as cur:
        row = cur.execute(_STATUS_SQL, {"country": country, "pattern": pattern.format(year=vintage)}).fetchone()
    if row is not None:
        status.national_id = row["national_id"]
        status.title = row["title"]
        status.chunks = row["chunks"]
        status.embedded = row["embedded"]
    return status


def describe(status: ActStatus, income_year_params: int = 0) -> str:
    """One human-readable banner line for the CLI."""
    need = " and ".join("in-force params" if role == "in_force" else "income-year params" for role in status.roles)
    head = f"  finance act for {status.vintage} ({need}): "
    if not status.present:
        line = head + "✗ not in corpus"
        if "income_year" in status.roles and income_year_params:
            line += f" → {income_year_params} income-year parameter(s) will be provisional"
        return line
    line = head + f"✓ {status.title} ({status.national_id}) — {status.embedded}/{status.chunks} chunks embedded"
    if status.backlog:
        line += f" ⚠ {status.backlog} not embedded: run `nomergon submit embed --wait`"
    return line
