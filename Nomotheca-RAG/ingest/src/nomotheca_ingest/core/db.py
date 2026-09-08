"""PostgreSQL helpers for fetch run lifecycle and snapshot persistence."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

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
            cur.execute(
                """
                INSERT INTO fetch_snapshots
                  (run_id, source_id, url, http_status, content_type, content_hash, raw_content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (self.run_id, source_id, url, status_code, content_type, content_hash, content),
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
