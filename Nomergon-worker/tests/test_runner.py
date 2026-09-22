"""The `@progress` / `@result` line protocol and the child's environment (no DB)."""

from __future__ import annotations

import sys
from pathlib import Path

from nomergon import runner
from nomergon.config import WorkerConfig


def test_plain_lines_are_logs() -> None:
    parsed = runner.parse_line("stdout", "materialized parameters/db/x.json")
    assert (parsed.kind, parsed.stream, parsed.data) == ("log", "stdout", None)
    assert runner.parse_line("stderr", "warning: CUDA out of memory").kind == "log"


def test_progress_line_is_parsed() -> None:
    parsed = runner.parse_line("stdout", '@progress {"phase": "embedded", "scanned": 10, "embedded": 8}')
    assert parsed.kind == "progress"
    assert parsed.data == {"phase": "embedded", "scanned": 10, "embedded": 8}
    assert parsed.line.startswith("@progress ")


def test_result_line_is_parsed() -> None:
    parsed = runner.parse_line("stdout", '@result {"item_ids": ["FR_x_2025"]}')
    assert parsed.kind == "result"
    assert parsed.data == {"item_ids": ["FR_x_2025"]}


def test_malformed_sentinel_stays_a_log_line() -> None:
    assert runner.parse_line("stdout", "@progress not json").kind == "log"
    assert runner.parse_line("stdout", "@result [1, 2]").kind == "log"
    assert runner.parse_line("stdout", "@progress").kind == "log"


def test_sentinels_on_stderr_are_not_protocol() -> None:
    assert runner.parse_line("stderr", '@progress {"phase": "x"}').kind == "log"


def test_job_environment_sets_the_switches_the_packages_honour(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("VIRTUAL_ENV", "/somewhere/.venv")
    monkeypatch.delenv("WORKFLOW_MODEL", raising=False)
    cfg = WorkerConfig(repo_root=tmp_path, database_url="postgresql://w:x@db/legislation", models=["jrc/m"])
    env = runner.job_environment(cfg, 42)
    assert env["PYTHONUNBUFFERED"] == "1"
    assert env["NOMOS_PYTHON"] == sys.executable
    assert env["WORKFLOW_ENCODER"] == "db"
    assert env["WORKFLOW_DATABASE_URL"] == env["EUROMOD_DATABASE_URL"] == env["EVAL_DATABASE_URL"] == cfg.database_url
    assert env["WORKER_JOB_ID"] == "42"
    assert env["WORKFLOW_MODEL"] == "jrc/m"
    assert "VIRTUAL_ENV" not in env


def test_the_worker_default_overrides_an_inherited_workflow_model(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("WORKFLOW_MODEL", "azure_openai/gpt-5.6-luna")
    monkeypatch.setenv("WORKFLOW_CRITIQUE_MODEL", "mock/extractor")
    env = runner.job_environment(WorkerConfig(repo_root=tmp_path, models=["jrc/m"]), 1)
    assert env["WORKFLOW_MODEL"] == "jrc/m"
    assert env["WORKFLOW_CRITIQUE_MODEL"] == "mock/extractor"


def test_no_worker_models_leaves_the_inherited_workflow_model(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("WORKFLOW_MODEL", "mock/extractor")
    assert runner.job_environment(WorkerConfig(repo_root=tmp_path), 1)["WORKFLOW_MODEL"] == "mock/extractor"


def test_redact_hides_the_password() -> None:
    url = "postgresql://jrc:jrc@localhost:5434/legislation"
    assert runner._redact(["x", url], url) == ["x", "postgresql://jrc:***@localhost:5434/legislation"]


def test_a_failing_database_does_not_kill_the_job(tmp_path, monkeypatch):
    """Disk full mid-run (seen 2026-09-22): every bookkeeping write raises, the
    child still runs to completion and its exit code decides the outcome."""
    import sys

    from nomergon import runner
    from nomergon.config import WorkerConfig

    class BrokenConnection:
        closed = False

        def execute(self, *_args, **_kwargs):
            raise RuntimeError("DiskFull: could not extend file")

        def cursor(self):
            raise RuntimeError("DiskFull: could not extend file")

    cfg = WorkerConfig(repo_root=tmp_path, database_url="postgresql://x/y", worker_id="t", models=[])
    monkeypatch.setattr(runner.jobs, "package_dir", lambda *_a, **_k: tmp_path)
    monkeypatch.setattr(
        runner.jobs, "build_command",
        lambda *_a, **_k: [sys.executable, "-c", "print('@progress {\"done\": 1}'); print('@result {\"ok\": true}')"],
    )
    monkeypatch.setattr(runner.jobs, "parse_payload", lambda *_a, **_k: {})
    monkeypatch.setattr(runner.jobs, "extract_result", lambda *_a, **k: k["result_line"])

    outcome = runner.run_job(BrokenConnection(), cfg, {"id": 1, "job_type": "impact", "payload": {}})

    assert outcome.status == "succeeded"
    assert outcome.result == {"ok": True}
