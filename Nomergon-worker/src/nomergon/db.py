"""psycopg helpers over the ``ops`` schema (jobs, events, workers, models).

Every function takes an autocommit connection (see ``connect``): each call is
one statement, so a crash between two never leaves a half-written job.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

SCHEMA_SQL = Path(__file__).resolve().parents[2] / "db" / "ops_schema.sql"
FINAL_STATUSES = ("succeeded", "failed", "cancelled")


def connect(database_url: str) -> psycopg.Connection[dict[str, Any]]:
    """An autocommit, dict-row connection."""
    return psycopg.connect(database_url, autocommit=True, row_factory=dict_row)


def apply_schema(conn: psycopg.Connection[Any]) -> None:
    """Create the ``ops`` schema (idempotent; the same file the db container applies)."""
    conn.execute(SCHEMA_SQL.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ jobs ----


def submit_job(conn: psycopg.Connection[Any], job_type: str, payload: dict[str, Any], priority: int = 0) -> int:
    row = conn.execute(
        "INSERT INTO ops.jobs (job_type, payload, priority) VALUES (%s, %s, %s) RETURNING id",
        (job_type, Jsonb(payload), priority),
    ).fetchone()
    return int(row["id"])


def claim_job(
    conn: psycopg.Connection[Any],
    worker_id: str,
    exclude_types: Sequence[str] = ("encode",),
) -> dict[str, Any] | None:
    """Claim the highest-priority, oldest queued job not of an excluded type."""
    return conn.execute(
        """
        UPDATE ops.jobs SET status = 'running', started_at = now(), worker_id = %s
        WHERE id = (
            SELECT id FROM ops.jobs
            WHERE status = 'queued' AND job_type <> ALL(%s)
            ORDER BY priority DESC, id
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        RETURNING *
        """,
        (worker_id, list(exclude_types)),
    ).fetchone()


def claim_encode_job(conn: psycopg.Connection[Any], worker_id: str) -> dict[str, Any] | None:
    """The encode lane's claim: only ``encode`` jobs, oldest first."""
    return conn.execute(
        """
        UPDATE ops.jobs SET status = 'running', started_at = now(), worker_id = %s
        WHERE id = (
            SELECT id FROM ops.jobs
            WHERE status = 'queued' AND job_type = 'encode'
            ORDER BY priority DESC, id
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        RETURNING *
        """,
        (worker_id,),
    ).fetchone()


def get_job(conn: psycopg.Connection[Any], job_id: int) -> dict[str, Any] | None:
    return conn.execute("SELECT * FROM ops.jobs WHERE id = %s", (job_id,)).fetchone()


def list_jobs(conn: psycopg.Connection[Any], limit: int = 50) -> list[dict[str, Any]]:
    return conn.execute("SELECT * FROM ops.jobs ORDER BY id DESC LIMIT %s", (limit,)).fetchall()


def append_event(
    conn: psycopg.Connection[Any],
    job_id: int,
    stream: str,
    line: str,
    data: dict[str, Any] | None = None,
) -> int:
    row = conn.execute(
        "INSERT INTO ops.job_events (job_id, stream, line, data) VALUES (%s, %s, %s, %s) RETURNING id",
        (job_id, stream, line, Jsonb(data) if data is not None else None),
    ).fetchone()
    return int(row["id"])


def append_events(conn: psycopg.Connection[Any], job_id: int, events: Sequence[tuple[str, str, dict[str, Any] | None]]) -> None:
    """Insert several (stream, line, data) rows in one round trip."""
    if not events:
        return
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO ops.job_events (job_id, stream, line, data) VALUES (%s, %s, %s, %s)",
            [(job_id, stream, line, Jsonb(data) if data is not None else None) for stream, line, data in events],
        )


def events_after(conn: psycopg.Connection[Any], job_id: int, after: int = 0, limit: int = 1000) -> list[dict[str, Any]]:
    return conn.execute(
        "SELECT id, at, stream, line, data FROM ops.job_events WHERE job_id = %s AND id > %s ORDER BY id LIMIT %s",
        (job_id, after, limit),
    ).fetchall()


def set_progress(conn: psycopg.Connection[Any], job_id: int, data: dict[str, Any]) -> None:
    conn.execute("UPDATE ops.jobs SET progress = %s WHERE id = %s", (Jsonb(data), job_id))


def finish_job(
    conn: psycopg.Connection[Any],
    job_id: int,
    status: str,
    result: Any = None,
    error: str | None = None,
) -> None:
    if status not in FINAL_STATUSES:
        msg = f"not a final status: {status}"
        raise ValueError(msg)
    conn.execute(
        "UPDATE ops.jobs SET status = %s, finished_at = now(), result = %s, error = %s WHERE id = %s",
        (status, Jsonb(result) if result is not None else None, error, job_id),
    )


def cancel_requested(conn: psycopg.Connection[Any], job_id: int) -> bool:
    row = conn.execute("SELECT cancel_requested FROM ops.jobs WHERE id = %s", (job_id,)).fetchone()
    return bool(row and row["cancel_requested"])


def request_cancel(conn: psycopg.Connection[Any], job_id: int) -> bool:
    """Flag a job for cancellation; a queued job is cancelled outright."""
    row = conn.execute(
        """
        UPDATE ops.jobs
        SET cancel_requested = true,
            status = CASE WHEN status = 'queued' THEN 'cancelled' ELSE status END,
            finished_at = CASE WHEN status = 'queued' THEN now() ELSE finished_at END
        WHERE id = %s AND status IN ('queued', 'running')
        RETURNING id
        """,
        (job_id,),
    ).fetchone()
    return row is not None


# --------------------------------------------------------------- workers ----


def register_worker(
    conn: psycopg.Connection[Any],
    worker_id: str,
    hostname: str,
    device: str | None,
    version: str | None,
) -> None:
    conn.execute(
        """
        INSERT INTO ops.workers (worker_id, hostname, device, version)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (worker_id) DO UPDATE
        SET hostname = EXCLUDED.hostname, device = EXCLUDED.device, version = EXCLUDED.version,
            started_at = now(), heartbeat_at = now(), current_job_id = NULL
        """,
        (worker_id, hostname, device, version),
    )


def heartbeat(conn: psycopg.Connection[Any], worker_id: str, current_job_id: int | None = None) -> None:
    conn.execute(
        "UPDATE ops.workers SET heartbeat_at = now(), current_job_id = %s WHERE worker_id = %s",
        (current_job_id, worker_id),
    )


def set_worker_device(conn: psycopg.Connection[Any], worker_id: str, device: str) -> None:
    conn.execute("UPDATE ops.workers SET device = %s WHERE worker_id = %s", (device, worker_id))


def unregister_worker(conn: psycopg.Connection[Any], worker_id: str) -> None:
    conn.execute("DELETE FROM ops.workers WHERE worker_id = %s", (worker_id,))


def prune_dead_workers(conn: psycopg.Connection[Any], stale_seconds: float) -> int:
    """Drop worker rows whose heartbeat is older than the stale window."""
    return conn.execute(
        "DELETE FROM ops.workers WHERE heartbeat_at < now() - make_interval(secs => %s)",
        (stale_seconds,),
    ).rowcount


def list_workers(conn: psycopg.Connection[Any]) -> list[dict[str, Any]]:
    return conn.execute(
        """
        SELECT worker_id, hostname, device, version, started_at, heartbeat_at, current_job_id,
               now() - heartbeat_at AS heartbeat_age
        FROM ops.workers ORDER BY heartbeat_at DESC
        """
    ).fetchall()


def fail_stale_running_jobs(conn: psycopg.Connection[Any], stale_seconds: float) -> list[int]:
    """Mark ``running`` jobs whose worker is gone (row missing or heartbeat stale) as failed.

    No requeue (ADR 0004): a human resubmits; embedding and translation resume
    by construction.
    """
    rows = conn.execute(
        """
        UPDATE ops.jobs j
        SET status = 'failed', finished_at = now(), error = 'worker died'
        WHERE j.status = 'running'
          AND NOT EXISTS (
              SELECT 1 FROM ops.workers w
              WHERE w.worker_id = j.worker_id
                AND w.heartbeat_at >= now() - make_interval(secs => %s)
          )
        RETURNING j.id
        """,
        (stale_seconds,),
    ).fetchall()
    return [int(row["id"]) for row in rows]


# ---------------------------------------------------------------- models ----


def publish_models(
    conn: psycopg.Connection[Any],
    worker_id: str,
    llm_models: Sequence[str],
    embedding_models: Sequence[str],
) -> None:
    """Replace what this worker published: LLMs (first is default) plus embedding models."""
    with conn.transaction():
        conn.execute("DELETE FROM ops.worker_models WHERE published_by = %s", (worker_id,))
        rows = [(name, "llm", index == 0, worker_id) for index, name in enumerate(llm_models)]
        rows += [(name, "embedding", index == 0, worker_id) for index, name in enumerate(embedding_models)]
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO ops.worker_models (model, kind, is_default, published_by)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (model) DO UPDATE
                SET kind = EXCLUDED.kind, is_default = EXCLUDED.is_default,
                    published_by = EXCLUDED.published_by, published_at = now()
                """,
                rows,
            )


def list_models(conn: psycopg.Connection[Any]) -> list[dict[str, Any]]:
    return conn.execute(
        "SELECT model, kind, is_default, published_by, published_at FROM ops.worker_models ORDER BY kind, is_default DESC, model"
    ).fetchall()


# ---------------------------------------------------------------- events ----


def prune_events(conn: psycopg.Connection[Any], days: int) -> int:
    """Delete events older than ``days``; returns how many went."""
    return conn.execute(
        "DELETE FROM ops.job_events WHERE at < now() - make_interval(days => %s)",
        (days,),
    ).rowcount


def dumps(value: Any) -> str:
    """Compact JSON for log lines."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
