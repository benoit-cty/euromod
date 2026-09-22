"""The MCP server's query encoder is a client of ops.jobs, never a model."""

from __future__ import annotations

import os
import threading
import time
from contextlib import contextmanager
from typing import Any

import psycopg
import pytest

from nomotheca_mcp import encoder as encoder_module
from nomotheca_mcp.encoder import (
    ALIVE_WORKERS_SQL,
    CANCEL_SQL,
    POLL_SQL,
    SUBMIT_SQL,
    EncoderUnavailable,
    QueryEncoder,
)


class FakeCursor:
    def __init__(self, conn: "FakeConnection") -> None:
        self._conn = conn
        self._rows: list[tuple] = []

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def execute(self, sql: str, params: tuple = ()) -> None:
        self._conn.executed.append((sql, params))
        if sql == ALIVE_WORKERS_SQL:
            self._rows = [(w,) for w in self._conn.workers]
        elif sql == SUBMIT_SQL:
            self._rows = [(self._conn.job_id,)]
        elif sql == POLL_SQL:
            self._conn.polls += 1
            self._rows = [self._conn.poll_rows.pop(0)] if self._conn.poll_rows else []
        elif sql == CANCEL_SQL:
            self._conn.cancelled.append(params[0])
            self._rows = []
        else:  # pragma: no cover - a new statement must be scripted here
            raise AssertionError(f"unexpected SQL: {sql}")

    def fetchone(self) -> tuple | None:
        return self._rows[0] if self._rows else None

    def fetchall(self) -> list[tuple]:
        return list(self._rows)


class FakeConnection:
    """Scripted answers for the four statements the encoder may issue."""

    def __init__(self, *, workers: list[str], poll_rows: list[tuple], job_id: int = 42) -> None:
        self.workers = workers
        self.poll_rows = poll_rows
        self.job_id = job_id
        self.executed: list[tuple[str, tuple]] = []
        self.cancelled: list[int] = []
        self.polls = 0
        self.closed = False

    def cursor(self) -> FakeCursor:
        return FakeCursor(self)

    def close(self) -> None:
        self.closed = True


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0
        self.slept: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


def make_encoder(conn: FakeConnection, clock: FakeClock, timeout: float = 60.0) -> QueryEncoder:
    return QueryEncoder(
        "postgresql://unused",
        timeout=timeout,
        connect=lambda: conn,
        sleep=clock.sleep,
        clock=clock,
    )


def test_submits_encode_job_and_returns_halfvec_after_polling() -> None:
    conn = FakeConnection(
        workers=["worker-a"],
        poll_rows=[("queued", None, None), ("running", None, None), ("succeeded", {"halfvec": "[0.1,0.2]"}, None)],
    )
    clock = FakeClock()

    assert make_encoder(conn, clock).encode_literal("income tax") == "[0.1,0.2]"

    submit_sql, submit_params = conn.executed[1]
    assert submit_sql == SUBMIT_SQL
    assert submit_params[0].obj == {"query": "income tax"}
    assert submit_params[1] == 100
    assert conn.polls == 3
    assert clock.slept == [0.1, 0.1]
    assert conn.cancelled == []
    assert conn.closed


def test_refuses_when_no_worker_is_alive_without_submitting() -> None:
    conn = FakeConnection(workers=[], poll_rows=[])

    with pytest.raises(EncoderUnavailable, match="no Nomergon worker is alive"):
        make_encoder(conn, FakeClock()).encode_literal("income tax")

    assert [sql for sql, _ in conn.executed] == [ALIVE_WORKERS_SQL]
    assert conn.closed


def test_failed_job_raises_with_worker_error() -> None:
    conn = FakeConnection(workers=["worker-a"], poll_rows=[("failed", None, "CUDA out of memory")])

    with pytest.raises(EncoderUnavailable, match="Nomergon worker reported encode job 42 failed: CUDA out of memory"):
        make_encoder(conn, FakeClock()).encode_literal("income tax")


def test_timeout_requests_cancel_and_names_the_worker() -> None:
    conn = FakeConnection(workers=["worker-a"], poll_rows=[("queued", None, None)] * 10)
    clock = FakeClock()

    with pytest.raises(EncoderUnavailable, match=r"still queued after 0\.25 s \(worker\(s\) worker-a alive but busy\)"):
        make_encoder(conn, clock, timeout=0.25).encode_literal("income tax")

    assert conn.cancelled == [42]
    assert clock.now >= 0.25


def test_succeeded_without_halfvec_is_an_error() -> None:
    conn = FakeConnection(workers=["worker-a"], poll_rows=[("succeeded", {"similarities": [0.5]}, None)])

    with pytest.raises(EncoderUnavailable, match="without a halfvec"):
        make_encoder(conn, FakeClock()).encode_literal("income tax")


def test_empty_query_never_touches_the_database() -> None:
    conn = FakeConnection(workers=["worker-a"], poll_rows=[])

    with pytest.raises(ValueError, match="must not be empty"):
        make_encoder(conn, FakeClock()).encode_literal("   ")

    assert conn.executed == []


def test_timeout_env_var(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("EUROMOD_ENCODE_TIMEOUT", raising=False)
    assert QueryEncoder("postgresql://unused").timeout == 60.0
    monkeypatch.setenv("EUROMOD_ENCODE_TIMEOUT", "2.5")
    assert QueryEncoder("postgresql://unused").timeout == 2.5
    monkeypatch.setenv("EUROMOD_ENCODE_TIMEOUT", "-1")
    with pytest.raises(ValueError):
        _ = QueryEncoder("postgresql://unused").timeout


def test_module_does_not_import_a_model_library() -> None:
    import sys

    for name in ("torch", "sentence_transformers", "transformers", "openvino", "nomotheca_ingest"):
        assert name not in sys.modules, f"{name} was imported by the MCP encoder"
    assert not hasattr(encoder_module, "SentenceTransformerBackend")


# ------------------------------------------------------------------ smoke ----

DEV_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


def _dev_db_with_ops() -> bool:
    try:
        with psycopg.connect(DEV_DATABASE_URL, connect_timeout=2) as conn:
            return conn.execute("SELECT to_regclass('ops.jobs') IS NOT NULL").fetchone()[0]
    except Exception:
        return False


@contextmanager
def _fake_worker(conn: psycopg.Connection, worker_id: str) -> Any:
    conn.execute(
        "INSERT INTO ops.workers (worker_id, hostname) VALUES (%s, 'pytest') "
        "ON CONFLICT (worker_id) DO UPDATE SET heartbeat_at = now()",
        (worker_id,),
    )
    try:
        yield
    finally:
        conn.execute("DELETE FROM ops.workers WHERE worker_id = %s", (worker_id,))


@pytest.mark.skipif(not _dev_db_with_ops(), reason="dev Postgres at localhost:5434 with ops.jobs not reachable")
def test_smoke_round_trip_against_dev_postgres() -> None:
    """Insert a real encode job, complete it from a thread as the worker would, read it back."""
    worker_id = f"pytest-{os.getpid()}"
    query = f"pytest smoke {time.time()}"

    def complete_job() -> None:
        with psycopg.connect(DEV_DATABASE_URL, autocommit=True) as admin:
            for _ in range(100):
                row = admin.execute(
                    "SELECT id FROM ops.jobs WHERE job_type = 'encode' AND status = 'queued' "
                    "AND payload->>'query' = %s",
                    (query,),
                ).fetchone()
                if row:
                    admin.execute(
                        "UPDATE ops.jobs SET status = 'succeeded', result = '{\"halfvec\": \"[0.1]\"}', "
                        "started_at = now(), finished_at = now(), worker_id = %s WHERE id = %s",
                        (worker_id, row[0]),
                    )
                    return
                time.sleep(0.05)

    with psycopg.connect(DEV_DATABASE_URL, autocommit=True) as admin, _fake_worker(admin, worker_id):
        worker = threading.Thread(target=complete_job, daemon=True)
        worker.start()
        try:
            halfvec = QueryEncoder(DEV_DATABASE_URL, timeout=10).encode_literal(query)
        finally:
            worker.join(timeout=10)
        assert halfvec == "[0.1]"
        submitted_by, status = admin.execute(
            "SELECT submitted_by, status FROM ops.jobs WHERE job_type = 'encode' AND payload->>'query' = %s",
            (query,),
        ).fetchone()
        assert status == "succeeded"
        assert submitted_by  # current_user default, the analyst login
        admin.execute("DELETE FROM ops.jobs WHERE job_type = 'encode' AND payload->>'query' = %s", (query,))
