"""Corpus readiness for a system year: are the finance-act vintages in place?

Verifying system year Y needs two consecutive finance-act vintages:
  - the act FOR Y (voted late Y-1 / early Y) — governs in_force parameters
    during Y;
  - the act FOR Y+1 (voted late Y / early Y+1) — carries the income-Y values
    of temporal_basis=income_year parameters (FR income-tax family).

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

    vintage: int          # the year the act is FOR (LF pour <vintage>)
    role: str             # 'in_force' | 'income_year' — which parameters need it
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


def finance_act_readiness(
    conn: psycopg.Connection, country: str, year: int
) -> list[ActStatus]:
    """Corpus status of the two finance-act vintages system year `year` needs.

    Empty list when no probe is configured for the country.
    """
    pattern = _BUDGET_ACT_TITLE.get(country)
    if pattern is None:
        return []
    statuses = []
    for vintage, role in ((year, "in_force"), (year + 1, "income_year")):
        status = ActStatus(vintage=vintage, role=role)
        with conn.cursor(row_factory=dict_row) as cur:
            row = cur.execute(
                _STATUS_SQL, {"country": country, "pattern": pattern.format(year=vintage)}
            ).fetchone()
        if row is not None:
            status.national_id = row["national_id"]
            status.title = row["title"]
            status.chunks = row["chunks"]
            status.embedded = row["embedded"]
        statuses.append(status)
    return statuses


def describe(status: ActStatus, income_year_params: int = 0) -> str:
    """One human-readable banner line for the CLI."""
    need = "in-force params" if status.role == "in_force" else "income-year params"
    head = f"  finance act for {status.vintage} ({need}): "
    if not status.present:
        line = head + "✗ not in corpus"
        if status.role == "income_year" and income_year_params:
            line += f" → {income_year_params} income-year parameter(s) will be provisional"
        return line
    line = head + f"✓ {status.title} ({status.national_id}) — {status.embedded}/{status.chunks} chunks embedded"
    if status.backlog:
        line += f" ⚠ {status.backlog} not embedded: run `nomotheca_ingest.cli embeddings build`"
    return line
