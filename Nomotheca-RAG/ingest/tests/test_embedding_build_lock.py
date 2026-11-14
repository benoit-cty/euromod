"""The embeddings-build lock says who it waits for (needs the stack up).

Uses its own advisory key, never the live build lock.
"""

from __future__ import annotations

import json
import os
import threading
import time

import psycopg
import pytest

from nomotheca_ingest import cli

DB_URL = os.environ.get("EUROMOD_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")
TEST_KEY = 0x74657374  # "test"


@pytest.fixture
def db_available():
    try:
        psycopg.connect(DB_URL, connect_timeout=2).close()
    except psycopg.OperationalError:
        pytest.skip("database not reachable")


def test_application_name_names_the_worker_job(monkeypatch):
    monkeypatch.setenv("WORKER_JOB_ID", "608")
    assert cli.embedding_lock_application_name() == "embeddings build (job #608)"
    monkeypatch.delenv("WORKER_JOB_ID")
    assert cli.embedding_lock_application_name().startswith(f"embeddings build (pid {os.getpid()} on ")


def test_waiting_build_reports_the_holder_then_acquires(db_available, monkeypatch, capsys):
    monkeypatch.setattr(cli, "EMBEDDING_BUILD_LOCK_KEY", TEST_KEY)
    monkeypatch.setattr(cli, "EMBEDDING_LOCK_POLL_SECONDS", 0.1)
    monkeypatch.setattr(cli, "_embedding_lock_conn", None)

    holder = psycopg.connect(DB_URL, autocommit=True, application_name="embeddings build (job #42)")
    assert holder.execute("SELECT pg_try_advisory_lock(%s)", (TEST_KEY,)).fetchone()[0]

    def release():
        time.sleep(0.5)
        holder.close()

    threading.Thread(target=release).start()
    try:
        cli._hold_embedding_build_lock(DB_URL, progress_json=True)
        out = capsys.readouterr().out
        progress = [json.loads(line[len("@progress ") :]) for line in out.splitlines() if line.startswith("@progress ")]
        assert progress[0]["phase"] == "waiting"
        assert "embeddings build (job #42)" in progress[0]["detail"]
        assert progress[-1]["phase"] == "starting"
    finally:
        if cli._embedding_lock_conn is not None:
            cli._embedding_lock_conn.close()
