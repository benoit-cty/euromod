"""encode_client against a real ops.jobs table (no worker: the job never runs).

Skipped when the dev Postgres or the ops schema is not there. The success
path needs a live worker and is covered by Nomergon's own tests; here we pin
the submit shape, the terminal-failure path and the timeout path, plus the
query_encoder fallback that keeps retrieval FTS-only when the worker is gone.
"""

from __future__ import annotations

import json
import os
import threading
import time
import uuid

import psycopg
import pytest
from nomoscope_workflow import encode_client, query_encoder

DATABASE_URL = os.environ.get("WORKFLOW_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


@pytest.fixture(scope="module")
def conn():
    try:
        connection = psycopg.connect(DATABASE_URL, connect_timeout=3, autocommit=True)
        ok = connection.execute("SELECT to_regclass('ops.jobs')").fetchone()[0]
    except Exception as exc:  # pragma: no cover - environment-dependent
        pytest.skip(f"dev Postgres not reachable ({exc.__class__.__name__}: {exc})")
    if not ok:
        pytest.skip("ops.jobs missing — apply Nomergon-worker/db/ops_schema.sql")
    yield connection
    connection.close()


@pytest.fixture
def marker(conn):
    """A unique query text so the test can find (and delete) its own job rows."""
    text = f"encode-client-test {uuid.uuid4().hex}"
    yield text
    conn.execute("DELETE FROM ops.jobs WHERE job_type = 'encode' AND payload ->> 'query' = %s", (text,))


def _settle(conn, marker: str, status: str, result=None, error=None) -> None:
    """Play the worker: wait for the job row, then finish it."""
    for _ in range(100):
        row = conn.execute(
            "SELECT id FROM ops.jobs WHERE job_type = 'encode' AND payload ->> 'query' = %s", (marker,)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE ops.jobs SET status = %s, result = %s, error = %s, finished_at = now() WHERE id = %s",
                (status, psycopg.types.json.Jsonb(result) if result is not None else None, error, row[0]),
            )
            return
        time.sleep(0.02)


def test_encode_via_jobs_returns_the_halfvec_the_worker_wrote(conn, marker):
    worker = threading.Thread(target=_settle, args=(conn, marker, "succeeded", {"halfvec": "[0.1,0.2]"}))
    worker.start()
    try:
        assert encode_client.encode_via_jobs(DATABASE_URL, marker, timeout=5, poll=0.02) == "[0.1,0.2]"
    finally:
        worker.join()
    job = conn.execute("SELECT priority, payload FROM ops.jobs WHERE payload ->> 'query' = %s", (marker,)).fetchone()
    assert job == (encode_client.ENCODE_PRIORITY, {"query": marker})


def test_a_failed_job_raises_its_error(conn, marker):
    worker = threading.Thread(target=_settle, args=(conn, marker, "failed", None, "CUDA out of memory"))
    worker.start()
    try:
        with pytest.raises(RuntimeError, match="CUDA out of memory"):
            encode_client.encode_via_jobs(DATABASE_URL, marker, timeout=5, poll=0.02)
    finally:
        worker.join()


def test_no_worker_is_a_timeout(conn, marker):
    alive = conn.execute(
        "SELECT count(*) FROM ops.workers WHERE heartbeat_at > now() - interval '60 seconds'"
    ).fetchone()[0]
    if alive:
        pytest.skip("a worker is running: it would answer the job")
    with pytest.raises(TimeoutError, match="no worker"):
        encode_client.encode_via_jobs(DATABASE_URL, marker, timeout=0.2, poll=0.02)


def test_query_encoder_db_mode_degrades_to_fts_only(conn, marker, monkeypatch, capsys):
    """WORKFLOW_ENCODER=db and a timeout: this query FTS-only, the leg paused, then retried."""
    monkeypatch.setenv("WORKFLOW_ENCODER", "db")
    monkeypatch.setenv("WORKFLOW_ENCODER_COOLDOWN", "30")
    monkeypatch.setattr(query_encoder, "_disabled", False)
    monkeypatch.setattr(query_encoder, "_paused_until", 0.0)
    calls = []

    def fail_then_answer(url, q, timeout=60.0, poll=0.1, model_id=1):
        calls.append(q)
        if len(calls) == 1:
            raise TimeoutError("no worker alive")
        return "[0.5]"

    monkeypatch.setattr(encode_client, "encode_via_jobs", fail_then_answer)
    before = query_encoder.fts_only_queries

    assert query_encoder.encode(marker, DATABASE_URL) is None
    assert query_encoder._disabled is False  # a timeout is not a reason to give up for good
    assert query_encoder.encode(marker, DATABASE_URL) is None  # paused: no second attempt yet
    assert len(calls) == 1
    assert query_encoder.fts_only_queries == before + 2
    monkeypatch.setattr(query_encoder, "_paused_until", 0.0)  # the cooldown elapses
    assert query_encoder.encode(marker, DATABASE_URL) == "[0.5]"
    out = capsys.readouterr().out
    assert out.count("vector leg paused") == 1 and "encoder=db" in out


def test_an_encoder_that_cannot_start_disables_the_leg(monkeypatch, capsys):
    monkeypatch.setenv("WORKFLOW_ENCODER", "nonsense")
    monkeypatch.setattr(query_encoder, "_disabled", False)
    monkeypatch.setattr(query_encoder, "_paused_until", 0.0)
    assert query_encoder.encode("q") is None
    assert query_encoder._disabled is True
    assert "vector leg disabled" in capsys.readouterr().out


def test_threads_never_read_each_others_vector(monkeypatch):
    """One subprocess pipe shared by -j 4 eval threads: request/response is atomic (D4)."""

    class SlowEcho:
        """A fake encoder process: answers each request with its own query, slowly."""

        def __init__(self):
            self.pending = []
            self.stdin = self
            self.stdout = self

        def poll(self):
            return None

        def write(self, line):
            self.pending.append(json.loads(line)["query"])

        def flush(self):
            pass

        def readline(self):
            time.sleep(0.01)  # another thread would write here without the lock
            return json.dumps({"halfvec": self.pending.pop(0)}) + "\n"

    monkeypatch.setenv("WORKFLOW_ENCODER", "subprocess")
    monkeypatch.setattr(query_encoder, "_disabled", False)
    monkeypatch.setattr(query_encoder, "_paused_until", 0.0)
    monkeypatch.setattr(query_encoder, "_channels", {})
    monkeypatch.setattr(query_encoder, "_start", lambda model_id=1: SlowEcho())
    results = {}

    def run(i):
        results[i] = query_encoder.encode(f"q{i}")

    threads = [threading.Thread(target=run, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results == {i: f"q{i}" for i in range(8)}
