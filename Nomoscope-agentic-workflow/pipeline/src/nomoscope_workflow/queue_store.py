"""The review queue, as rows in `params.review_queue` (ADR 0004).

One row per queue item, keyed `<country>_<target>_<system year>` (item_id),
holding the ReviewItem as JSON so the item schema can evolve pipeline-side
without a lockstep UI release. The pipeline writes items here (a re-run
replaces a pending item, never a decided one unless forced); the validation
UI reads them and records decisions through `params.decide_review_item()`,
which updates the item and appends to `params.review_decisions` in one
transaction. Nothing about the queue lives on disk.
"""

from __future__ import annotations

import json
import re

import psycopg

from .schema import ItemStatus, ReviewItem


def slugify(text: str) -> str:
    """Id-safe slug of a model_target path."""
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()


def item_id(country: str, model_target: str, system_year: int) -> str:
    """Stable id so re-runs of the same (parameter, system year) overwrite, not duplicate.

    Keyed on the system year, not the anchor date: one run verifies one EUROMOD
    system year, and re-running it on another day (or with a shifted anchor, as
    income_year parameters do) is the same review, not a second one.
    """
    return f"{country.lower()}_{slugify(model_target)}_{system_year}"


_COLUMNS = "item_id, country, model_target, system_year, routing, status, run_id, created_at, item"


def write_item(conn: psycopg.Connection, item: ReviewItem, force: bool = False) -> bool:
    """Upsert a queue item; never clobber an already-reviewed item unless forced.

    Returns whether the row was written. Commits: an item is the run's output
    and must survive whatever happens to the rest of the run.
    """
    row = conn.execute(
        f"""
        INSERT INTO params.review_queue ({_COLUMNS})
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (item_id) DO UPDATE SET
            country = EXCLUDED.country,
            model_target = EXCLUDED.model_target,
            system_year = EXCLUDED.system_year,
            routing = EXCLUDED.routing,
            status = EXCLUDED.status,
            run_id = EXCLUDED.run_id,
            created_at = EXCLUDED.created_at,
            item = EXCLUDED.item,
            updated_at = now()
        WHERE params.review_queue.status = 'pending' OR %s
        RETURNING item_id
        """,
        (
            item.id,
            item.country,
            item.model_target,
            item.system_year,
            item.routing.value,
            item.status.value,
            item.run_id,
            item.created_at,
            json.dumps(item.model_dump(mode="json"), ensure_ascii=False),
            force,
        ),
    ).fetchone()
    conn.commit()
    return row is not None


def _from_row(status: str, item: dict) -> ReviewItem:
    loaded = ReviewItem.model_validate(item)
    # The status column is what decide_review_item maintains; the JSON copy
    # normally agrees, but the column is authoritative.
    if loaded.status.value != status:
        loaded = loaded.model_copy(update={"status": ItemStatus(status)})
    return loaded


def load_items(
    conn: psycopg.Connection, country: str | None = None, status: str | None = None
) -> list[ReviewItem]:
    """Queue items, newest first, optionally filtered by country and/or status."""
    clauses, params = [], []
    if country:
        clauses.append("country = %s")
        params.append(country.upper())
    if status:
        clauses.append("status = %s")
        params.append(str(status))
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = conn.execute(
        f"SELECT status, item FROM params.review_queue {where} ORDER BY created_at DESC, item_id",
        params,
    ).fetchall()
    return [_from_row(status, item) for status, item in rows]


def load_item(conn: psycopg.Connection, item_id: str) -> ReviewItem | None:
    """One queue item by id, or None."""
    row = conn.execute(
        "SELECT status, item FROM params.review_queue WHERE item_id = %s", (item_id,)
    ).fetchone()
    return _from_row(*row) if row else None


def export_accepted(conn: psycopg.Connection) -> dict[str, list[dict]]:
    """Accepted/edited items' full records (Activity 1 format), grouped by country.

    Write-back is export-first: this is the only thing that leaves the DB, one
    file per country, and only after a human accepted the item in the UI.
    """
    exported: dict[str, list[dict]] = {}
    for item in load_items(conn):
        if item.status in (ItemStatus.ACCEPTED, ItemStatus.EDITED) and item.proposed_record:
            exported.setdefault(item.country, []).append(
                item.proposed_record.model_dump(mode="json")
            )
    return exported
