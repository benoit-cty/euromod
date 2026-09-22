"""Query encoding through the Nomergon worker (ADR 0004).

The MCP server never loads a model. A query vector is obtained by inserting an
``encode`` job into ``ops.jobs`` and polling the row until the worker, which
keeps BGE-M3 warm in its priority lane, writes ``result = {"halfvec": "[...]"}``.
The login the server runs under is an analyst role (``IN ROLE nomos_reviewer``):
it may SELECT ``ops.jobs`` / ``ops.workers``, INSERT ``ops.jobs`` and set
``cancel_requested`` on its own rows, nothing more.
"""

from __future__ import annotations

import os
import time
from typing import Any, Callable

import psycopg
from psycopg.types.json import Jsonb

ENCODE_JOB_PRIORITY = 100
DEFAULT_TIMEOUT_SECONDS = 60.0
POLL_INTERVAL_SECONDS = 0.1
WORKER_HEARTBEAT_MAX_AGE_SECONDS = 60
TERMINAL_STATUSES = frozenset({"succeeded", "failed", "cancelled"})

SUBMIT_SQL = "INSERT INTO ops.jobs (job_type, payload, priority) VALUES ('encode', %s, %s) RETURNING id"
POLL_SQL = "SELECT status, result, error FROM ops.jobs WHERE id = %s"
ALIVE_WORKERS_SQL = (
    "SELECT worker_id FROM ops.workers WHERE heartbeat_at >= now() - make_interval(secs => %s) "
    "ORDER BY heartbeat_at DESC"
)
CANCEL_SQL = "UPDATE ops.jobs SET cancel_requested = true WHERE id = %s AND status = 'queued'"


class EncoderUnavailable(RuntimeError):
    """The Nomergon worker did not produce a query vector."""


def encode_timeout_from_env() -> float:
    raw = os.getenv("EUROMOD_ENCODE_TIMEOUT")
    if raw is None or not raw.strip():
        return DEFAULT_TIMEOUT_SECONDS
    try:
        timeout = float(raw)
    except ValueError as exc:
        raise ValueError(f"EUROMOD_ENCODE_TIMEOUT must be a number of seconds, got {raw!r}") from exc
    if timeout <= 0:
        raise ValueError("EUROMOD_ENCODE_TIMEOUT must be positive")
    return timeout


class QueryEncoder:
    """Submit ``encode`` jobs to ``ops.jobs`` and wait for the worker's vector.

    ``connect`` returns an *autocommit* connection with INSERT on ``ops.jobs``;
    it must not carry ``default_transaction_read_only=on``. The search side
    keeps its own read-only connection. ``sleep`` and ``clock`` exist so the
    polling loop can be tested without a database or real time.
    """

    def __init__(
        self,
        database_url: str | None = None,
        *,
        timeout: float | None = None,
        poll_interval: float = POLL_INTERVAL_SECONDS,
        connect: Callable[[], Any] | None = None,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._database_url = database_url or os.getenv(
            "DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation"
        )
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._connect = connect or self._default_connect
        self._sleep = sleep
        self._clock = clock

    @property
    def timeout(self) -> float:
        return self._timeout if self._timeout is not None else encode_timeout_from_env()

    def _default_connect(self) -> psycopg.Connection:
        return psycopg.connect(
            self._database_url,
            autocommit=True,
            options="-c statement_timeout=30000",
        )

    @staticmethod
    def alive_workers(conn: Any) -> list[str]:
        with conn.cursor() as cur:
            cur.execute(ALIVE_WORKERS_SQL, (WORKER_HEARTBEAT_MAX_AGE_SECONDS,))
            return [row[0] for row in cur.fetchall()]

    def encode_literal(self, query: str) -> str:
        """Return a PostgreSQL halfvec literal for one normalized query vector."""
        if not query.strip():
            raise ValueError("query must not be empty")
        conn = self._connect()
        try:
            if not self.alive_workers(conn):
                raise EncoderUnavailable(
                    "no Nomergon worker is alive (no ops.workers.heartbeat_at within "
                    f"{WORKER_HEARTBEAT_MAX_AGE_SECONDS} s): start the worker "
                    "(Nomergon-worker) or use mode='full_text'"
                )
            job_id = self._submit(conn, query)
            return self._wait(conn, job_id)
        finally:
            conn.close()

    def _submit(self, conn: Any, query: str) -> int:
        with conn.cursor() as cur:
            cur.execute(SUBMIT_SQL, (Jsonb({"query": query}), ENCODE_JOB_PRIORITY))
            row = cur.fetchone()
        if row is None:
            raise EncoderUnavailable("INSERT INTO ops.jobs returned no id")
        return int(row[0])

    def _wait(self, conn: Any, job_id: int) -> str:
        timeout = self.timeout
        deadline = self._clock() + timeout
        while True:
            with conn.cursor() as cur:
                cur.execute(POLL_SQL, (job_id,))
                row = cur.fetchone()
            if row is None:
                raise EncoderUnavailable(f"encode job {job_id} vanished from ops.jobs")
            status, result, error = row
            if status == "succeeded":
                return self._halfvec(job_id, result)
            if status in TERMINAL_STATUSES:
                detail = f": {error}" if error else ""
                raise EncoderUnavailable(f"Nomergon worker reported encode job {job_id} {status}{detail}")
            if self._clock() >= deadline:
                self._cancel(conn, job_id)
                alive = self.alive_workers(conn)
                why = (
                    f"worker(s) {', '.join(alive)} alive but busy"
                    if alive
                    else "no Nomergon worker is alive any more"
                )
                raise EncoderUnavailable(
                    f"encode job {job_id} still {status} after {timeout:g} s ({why}); "
                    "raise EUROMOD_ENCODE_TIMEOUT or wait for the worker's queue to drain"
                )
            self._sleep(self._poll_interval)

    @staticmethod
    def _halfvec(job_id: int, result: Any) -> str:
        halfvec = result.get("halfvec") if isinstance(result, dict) else None
        if not isinstance(halfvec, str) or not halfvec:
            raise EncoderUnavailable(
                f"encode job {job_id} succeeded without a halfvec in its result: {result!r}"
            )
        return halfvec

    @staticmethod
    def _cancel(conn: Any, job_id: int) -> None:
        try:
            with conn.cursor() as cur:
                cur.execute(CANCEL_SQL, (job_id,))
        except Exception:  # best effort: the job is stale either way
            pass
