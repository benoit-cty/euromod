"""PostgreSQL helpers for fetch run lifecycle and snapshot persistence."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from uuid import UUID

import psycopg
from psycopg import Connection
from psycopg.types.json import Jsonb

from nomotheca_ingest.core.ir import SourceRef, Trigger


@dataclass(slots=True)
class PostgresSnapshotStore:
    """Snapshot store implementation backed by the legislation PostgreSQL schema."""

    conn: Connection
    run_id: UUID

    def write_snapshot(
        self,
        ref: SourceRef,
        url: str,
        status_code: int,
        content_type: str | None,
        content_hash: str,
        content: bytes,
    ) -> UUID:
        """Insert raw response bytes into fetch_snapshots and return its id."""
        source_id = self._source_id(ref.source_code)
        with self.conn.cursor() as cur:
            # The SourceRef goes with the bytes: `reparse` replays any country's
            # archive from it, with no per-country URL reverse-engineering.
            cur.execute(
                """
                INSERT INTO fetch_snapshots
                  (run_id, source_id, url, http_status, content_type, content_hash, raw_content, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    self.run_id, source_id, url, status_code, content_type, content_hash, content,
                    Jsonb({"source_ref": ref.model_dump(mode="json")}),
                ),
            )
            return cur.fetchone()[0]

    def _source_id(self, source_code: str) -> int:
        """Resolve a source code to its database identity."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM sources WHERE code = %s", (source_code,))
            row = cur.fetchone()
        if row is None:
            msg = f"Unknown source code: {source_code}"
            raise ValueError(msg)
        return row[0]


def ensure_source(
    conn: Connection,
    jurisdiction: str,
    source_code: str,
    *,
    name: str,
    id_system: str,
    fetch_skill: str,
    note: str,
) -> None:
    """Idempotently register a source row for a corpus fed from a local file.

    Country adapters fetch from sources the seed already declares; the two
    file-fed corpora (Country Reports, contributed documents) mint theirs on
    first use, so no seed change is needed before a reviewer's first upload.
    """
    row = conn.execute(
        "SELECT id FROM jurisdictions WHERE code = %s", (jurisdiction.upper(),)
    ).fetchone()
    if row is None:
        msg = f"Unknown jurisdiction: {jurisdiction} (seed it before ingesting for it)"
        raise ValueError(msg)
    conn.execute(
        """
        INSERT INTO sources (jurisdiction_id, code, name, id_system, fetch_skill, terms)
        VALUES (%s, %s, %s, %s, %s, jsonb_build_object('note', %s::text))
        ON CONFLICT (code) DO NOTHING
        """,
        (row[0], source_code, name, id_system, fetch_skill, note),
    )


def create_fetch_run(
    conn: Connection,
    source_code: str,
    skill_version: str,
    trigger: Trigger = Trigger.CACHE_MISS,
    frozen_label: str | None = None,
) -> UUID:
    """Create a fetch_runs row and return its generated id."""
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE code = %s", (source_code,))
        row = cur.fetchone()
        if row is None:
            msg = f"Unknown source code: {source_code}"
            raise ValueError(msg)
        source_id = row[0]
        cur.execute(
            """
            INSERT INTO fetch_runs (source_id, skill_version, trigger, frozen_label)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            (source_id, skill_version, trigger.value, frozen_label),
        )
        return cur.fetchone()[0]


def finish_fetch_run(conn: Connection, run_id: UUID, status: str, stats: dict | None = None) -> None:
    """Mark a fetch run as finished with a terminal status and optional stats."""
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE fetch_runs
            SET finished_at = now(), status = %s, stats = COALESCE(%s::jsonb, stats)
            WHERE id = %s
            """,
            (status, Jsonb(stats) if stats is not None else None, run_id),
        )


@dataclass(slots=True)
class FetchRun:
    """An open fetch run: its id, the archive connection and the stats to record.

    `archive` is an autocommit connection: the run row and every snapshot
    written through `store` are committed as they are written, so a failed
    load (rolled back on the caller's own connection) still leaves the run,
    marked `failed`, and the bytes it fetched. Archive-first holds on failure.
    """

    id: UUID
    archive: Connection
    trigger: Trigger
    stats: dict = field(default_factory=dict)

    @property
    def store(self) -> PostgresSnapshotStore:
        return PostgresSnapshotStore(self.archive, self.id)


@contextmanager
def fetch_run(
    database_url: str,
    source_code: str,
    skill_version: str,
    trigger: Trigger = Trigger.CACHE_MISS,
    frozen_label: str | None = None,
    *,
    setup: Callable[[Connection], None] | None = None,
) -> Iterator[FetchRun]:
    """Open a fetch run whose outcome is recorded whatever happens.

    The body loads on its own connection (one transaction, rolled back on
    error); the run row and snapshots live on the autocommit archive
    connection. On exit the run is marked `succeeded` with `run.stats`, or
    `failed` with the error, and the exception propagates. `setup` runs on
    the archive connection before the run row is created (`ensure_source`).
    """
    with psycopg.connect(database_url, autocommit=True) as archive:
        if setup is not None:
            setup(archive)
        run = FetchRun(
            id=create_fetch_run(archive, source_code, skill_version, trigger, frozen_label),
            archive=archive,
            trigger=trigger,
        )
        try:
            yield run
        except BaseException as exc:
            finish_fetch_run(
                archive, run.id, "failed", {"trigger": trigger.value, "error": str(exc) or type(exc).__name__}
            )
            raise
        finish_fetch_run(archive, run.id, "succeeded", {"trigger": trigger.value, **run.stats})
