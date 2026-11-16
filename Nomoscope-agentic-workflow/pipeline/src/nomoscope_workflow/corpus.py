"""The legislation corpus as retrieval reads it: scope, versions, provenance,
the hit columns and joins shared by every query (split out of retrieval.py,
code audit 4)."""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import date

import psycopg
from psycopg.rows import dict_row

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
#: The RetrievalHit columns every hit query selects (aliases: ch chunks,
#: t unit_texts, v legal_unit_versions, u legal_units, i instruments), and the
#: joins from a chunk up to its instrument. One place to add a hit field —
#: the column list used to be written out in every query (code audit 4).
HIT_COLUMNS = (
    "ch.id::text AS chunk_id, u.citation, ch.context_header, ch.content, t.lang,\n"
    "       v.validity::text AS validity, v.version_status, i.source_trust_class"
)
CHUNK_JOINS = """JOIN unit_texts t          ON t.id = ch.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u         ON u.id = v.legal_unit_id
JOIN instruments i         ON i.id = u.instrument_id"""

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


