"""Round trip against a live Postgres: skipped when none answers.

Uses WORKER_DATABASE_URL / WORKFLOW_DATABASE_URL or the dev stack's default.
Applies the ops schema (idempotent) and deletes the jobs it creates.
"""

from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

import psycopg
import pytest

from nomergon import client, db, jobs, runner
from nomergon.config import DEFAULT_DATABASE_URL, WorkerConfig

DATABASE_URL = os.environ.get("WORKER_DATABASE_URL") or os.environ.get("WORKFLOW_DATABASE_URL") or DEFAULT_DATABASE_URL


def _reachable() -> bool:
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=2):
            return True
    except Exception:  # noqa: BLE001
        return False


pytestmark = pytest.mark.skipif(not _reachable(), reason=f"no Postgres at {DATABASE_URL}")


@pytest.fixture
def conn():
    connection = db.connect(DATABASE_URL)
    db.apply_schema(connection)
    created: list[int] = []
    original = db.submit_job

    def tracking_submit(c, job_type, payload, priority=0):
        job_id = original(c, job_type, payload, priority)
        created.append(job_id)
        return job_id

    db.submit_job = tracking_submit
    try:
        yield connection
    finally:
        db.submit_job = original
        if created:
            connection.execute("DELETE FROM ops.jobs WHERE id = ANY(%s)", (created,))
        connection.close()


@pytest.fixture
def cfg(tmp_path: Path) -> WorkerConfig:
    return WorkerConfig(repo_root=tmp_path, database_url=DATABASE_URL, worker_id="pytest-worker")


def test_submit_claim_event_finish_list(conn) -> None:
    job_id = client.submit(conn, "impact", {"zone": "EEE"}, priority=0)
    low = client.submit(conn, "impact", {}, priority=-1)
    encode = client.submit(conn, "encode", {"query": "q"}, priority=100)

    claimed = db.claim_job(conn, "pytest-worker")
    assert claimed is not None and claimed["id"] == job_id  # encode excluded, priority 0 before -1
    assert claimed["status"] == "running" and claimed["worker_id"] == "pytest-worker"

    event_id = db.append_event(conn, job_id, "stdout", "hello")
    db.append_events(conn, job_id, [("progress", '@progress {"phase":"x"}', {"phase": "x"})])
    db.set_progress(conn, job_id, {"phase": "x"})
    events = db.events_after(conn, job_id, 0)
    assert [e["stream"] for e in events] == ["stdout", "progress"]
    assert events[0]["id"] == event_id and events[1]["data"] == {"phase": "x"}

    db.finish_job(conn, job_id, "succeeded", result={"ok": True})
    row = db.get_job(conn, job_id)
    assert row["status"] == "succeeded" and row["result"] == {"ok": True} and row["progress"] == {"phase": "x"}
    assert row["finished_at"] is not None

    encode_claim = db.claim_encode_job(conn, "pytest-worker")
    assert encode_claim is not None and encode_claim["id"] == encode
    db.finish_job(conn, encode, "failed", error="no model in tests")

    assert db.claim_job(conn, "pytest-worker")["id"] == low
    db.finish_job(conn, low, "cancelled")

    listed = [r["id"] for r in db.list_jobs(conn, 10)]
    assert listed[:3] == [encode, low, job_id]

    waited = client.wait(conn, job_id, timeout=1)
    assert waited["status"] == "succeeded"


def test_cancel_of_a_queued_job_is_immediate(conn) -> None:
    job_id = client.submit(conn, "impact", {})
    assert client.cancel(conn, job_id)
    assert db.get_job(conn, job_id)["status"] == "cancelled"
    assert not client.cancel(conn, job_id)


def test_worker_registration_models_and_stale_jobs(conn) -> None:
    db.register_worker(conn, "pytest-worker", "host", "cpu", "0.0.0")
    db.publish_models(conn, "pytest-worker", ["mock/extractor", "mock/other"], ["bge-m3"])
    try:
        models = {m["model"]: m for m in db.list_models(conn) if m["published_by"] == "pytest-worker"}
        assert models["mock/extractor"]["is_default"] and not models["mock/other"]["is_default"]
        assert models["bge-m3"]["kind"] == "embedding"

        orphan = client.submit(conn, "impact", {})
        conn.execute("UPDATE ops.jobs SET status='running', worker_id='ghost-worker' WHERE id=%s", (orphan,))
        alive = client.submit(conn, "impact", {})
        conn.execute("UPDATE ops.jobs SET status='running', worker_id='pytest-worker' WHERE id=%s", (alive,))
        failed = db.fail_stale_running_jobs(conn, 60)
        assert orphan in failed and alive not in failed
        assert db.get_job(conn, orphan)["error"] == "worker died"

        conn.execute("UPDATE ops.workers SET heartbeat_at = now() - interval '1 hour' WHERE worker_id='pytest-worker'")
        assert db.fail_stale_running_jobs(conn, 60) == [alive]
        assert db.prune_dead_workers(conn, 60) >= 1
    finally:
        conn.execute("DELETE FROM ops.worker_models WHERE published_by = 'pytest-worker'")
        db.unregister_worker(conn, "pytest-worker")


def test_subprocess_output_streams_into_events(conn, cfg: WorkerConfig, tmp_path: Path) -> None:
    job_id = client.submit(conn, "workflow", {"targets": ["x"], "year": 2025})
    conn.execute("UPDATE ops.jobs SET status='running', worker_id=%s WHERE id=%s", (cfg.worker_id, job_id))
    script = (
        "import sys\n"
        "print('line one')\n"
        "print('@progress {\"phase\": \"half\", \"done\": 1}')\n"
        "print('oops', file=sys.stderr)\n"
        "print('@result {\"item_ids\": [\"FR_x_2025\"]}')\n"
    )
    payload = jobs.parse_payload("workflow", {"targets": ["x"], "year": 2025})
    outcome = runner._run_subprocess(conn, cfg, job_id, "workflow", payload, [sys.executable, "-c", script], tmp_path, None)
    assert outcome.status == "succeeded"
    assert outcome.result == {"item_ids": ["FR_x_2025"]}
    events = db.events_after(conn, job_id, 0)
    by_stream = {}
    for event in events:
        by_stream.setdefault(event["stream"], []).append(event["line"])
    assert "line one" in by_stream["stdout"]
    assert not any(line.startswith("@result") for line in by_stream["stdout"])
    assert by_stream["stderr"] == ["oops"]
    assert by_stream["progress"] == ['@progress {"phase": "half", "done": 1}']
    assert db.get_job(conn, job_id)["progress"] == {"phase": "half", "done": 1}
    assert any("exit code 0" in line for line in by_stream["system"])


def test_failed_subprocess_reports_the_stderr_tail(conn, cfg: WorkerConfig, tmp_path: Path) -> None:
    job_id = client.submit(conn, "impact", {})
    payload = jobs.parse_payload("impact", {})
    script = "import sys\nprint('boom', file=sys.stderr)\nsys.exit(3)\n"
    outcome = runner._run_subprocess(conn, cfg, job_id, "impact", payload, [sys.executable, "-c", script], tmp_path, None)
    assert outcome.status == "failed" and outcome.error == "boom"


def test_cancel_terminates_a_running_subprocess(conn, cfg: WorkerConfig, tmp_path: Path) -> None:
    job_id = client.submit(conn, "impact", {})
    conn.execute("UPDATE ops.jobs SET status='running', worker_id=%s WHERE id=%s", (cfg.worker_id, job_id))
    payload = jobs.parse_payload("impact", {})

    def request_cancel_soon() -> None:
        time.sleep(0.5)
        with db.connect(DATABASE_URL) as other:
            client.cancel(other, job_id)

    threading.Thread(target=request_cancel_soon, daemon=True).start()
    started = time.monotonic()
    outcome = runner._run_subprocess(
        conn, cfg, job_id, "impact", payload, [sys.executable, "-c", "import time; time.sleep(30)"], tmp_path, None
    )
    assert outcome.status == "cancelled"
    assert time.monotonic() - started < 15
