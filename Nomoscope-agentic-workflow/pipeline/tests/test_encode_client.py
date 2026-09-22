"""encode_client against a real ops.jobs table (no worker: the job never runs).

Skipped when the dev Postgres or the ops schema is not there. The success
path needs a live worker and is covered by Nomergon's own tests; here we pin
the submit shape, the terminal-failure path and the timeout path, plus the
query_encoder fallback that keeps retrieval FTS-only when the worker is gone.
"""

from __future__ import annotations

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
    job = conn.execute(
        "SELECT priority, payload FROM ops.jobs WHERE payload ->> 'query' = %s", (marker,)
    ).fetchone()
    assert job == (encode_client.ENCODE_PRIORITY, {"query": marker})


def test_score_via_jobs_sends_the_sentences(conn, marker):
    worker = threading.Thread(target=_settle, args=(conn, marker, "succeeded", {"similarities": [0.9, 0.1]}))
    worker.start()
    try:
        scores = encode_client.score_via_jobs(DATABASE_URL, marker, ["a", "b"], timeout=5, poll=0.02)
    finally:
        worker.join()
    assert scores == [0.9, 0.1]
    assert conn.execute(
        "SELECT payload -> 'sentences' FROM ops.jobs WHERE payload ->> 'query' = %s", (marker,)
    ).fetchone()[0] == ["a", "b"]


def test_a_failed_job_raises_its_error(conn, marker):
    worker = threading.Thread(target=_settle, args=(conn, marker, "failed", None, "CUDA out of memory"))
    worker.start()
    try:
        with pytest.raises(RuntimeError, match="CUDA out of memory"):
            encode_client.encode_via_jobs(DATABASE_URL, marker, timeout=5, poll=0.02)
    finally:
        worker.join()


def test_no_worker_is_a_timeout(conn, marker):
    with pytest.raises(TimeoutError, match="no worker"):
        encode_client.encode_via_jobs(DATABASE_URL, marker, timeout=0.2, poll=0.02)


def test_query_encoder_db_mode_degrades_to_fts_only(conn, marker, monkeypatch, capsys):
    """WORKFLOW_ENCODER=db with no worker: vector leg disabled for the process, one note."""
    monkeypatch.setenv("WORKFLOW_ENCODER", "db")
    monkeypatch.setattr(query_encoder, "_disabled", False)
    monkeypatch.setattr(encode_client, "encode_via_jobs", lambda url, q, timeout=60.0, poll=0.1: (_ for _ in ()).throw(TimeoutError("no worker alive")))

    assert query_encoder.encode(marker, DATABASE_URL) is None
    assert query_encoder._disabled is True
    assert query_encoder.encode(marker, DATABASE_URL) is None  # latched, no second attempt
    out = capsys.readouterr().out
    assert out.count("vector leg disabled") == 1 and "encoder=db" in out
