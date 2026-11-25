"""Dated editions of one publication: a later edition closes the earlier one.

A contributed document is one instrument per URL, and a publisher that keeps
every edition of a page online gives each its own URL. BOFiP does:
``…/identifiant=BOI-RSA-BASE-30-30-20170724`` is the commentary as published
on 24 July 2017, and the 2012 and 2016 editions stay reachable beside it.
Loaded as three unrelated documents, all three were in force with no end
date: they took 8 of the 15 search results for the deductible share of the
CSG, and the 2017 edition's «5,1 points» was proposed for 2025 (the law has
said 6,8 since 2018; panel run 261, 24 Nov 2026).

Editions of one series are chained like the versions of one article
(`LegislationLoader._chain_versions`): each ends where the next one held
begins. The latest edition held stays open — whether it is the publisher's
current one is not something the store can know.
"""

from __future__ import annotations

import itertools
import re
from collections import defaultdict
from datetime import date

import psycopg

#: How a national id names its series and its edition date, per publisher.
SERIES_PATTERNS: tuple[re.Pattern[str], ...] = (
    # BOFiP: …/bofip/2491-PGP.html/identifiant=BOI-IR-LIQ-20-20-10-20250414
    re.compile(r"/identifiant=(?P<series>BOI-[A-Z0-9-]+?)-(?P<y>\d{4})(?P<m>\d{2})(?P<d>\d{2})$"),
)


def edition_of(national_id: str) -> tuple[str, date] | None:
    """(series, edition date) when the id names a dated edition, else None."""
    for pattern in SERIES_PATTERNS:
        match = pattern.search(national_id)
        if match:
            try:
                return match["series"], date(int(match["y"]), int(match["m"]), int(match["d"]))
            except ValueError:
                return None
    return None


def chain_editions(conn: psycopg.Connection) -> int:
    """End every edition held where the next edition of its series begins.

    Idempotent and cheap (one pass over the contributed instruments), so it
    runs after every contributed load and reparse. Returns the number of
    versions closed.
    """
    rows = conn.execute(
        "SELECT i.id, i.source_id, i.national_id FROM instruments i WHERE i.metadata ->> 'contributed' = 'true'"
    ).fetchall()
    series: dict[tuple[int, str], list[tuple[date, object]]] = defaultdict(list)
    for instrument_id, source_id, national_id in rows:
        edition = edition_of(national_id or "")
        if edition:
            series[(source_id, edition[0])].append((edition[1], instrument_id))
    closed = 0
    for editions in series.values():
        editions.sort(key=lambda e: e[0])
        for (_, older), (next_start, _) in itertools.pairwise(editions):
            cur = conn.execute(
                """
                UPDATE legal_unit_versions v
                SET validity = daterange(lower(v.validity), %(end)s, '[)'),
                    version_status = CASE WHEN v.version_status = 'in_force'
                                          THEN 'repealed' ELSE v.version_status END
                FROM legal_units u
                WHERE u.id = v.legal_unit_id AND u.instrument_id = %(instrument)s
                  AND lower(v.validity) < %(end)s
                  AND (upper_inf(v.validity) OR upper(v.validity) > %(end)s)
                """,
                {"instrument": older, "end": next_start},
            )
            closed += cur.rowcount
    return closed
