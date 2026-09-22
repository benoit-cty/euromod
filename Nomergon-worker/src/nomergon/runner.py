"""Run one subprocess job and stream its output into ``ops.job_events``.

The child is one of the three CLIs, started from the worker's own interpreter
(``sys.executable -m …``) in its package directory. Its stdout and stderr are
read concurrently; every line becomes an event, ``@progress {json}`` lines
also update ``ops.jobs.progress`` and ``@result {json}`` is captured as the
job's result. ``cancel_requested`` is polled once a second.
"""

from __future__ import annotations

import json
import logging
import os
import queue
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

import psycopg

from . import db, jobs
from .config import WorkerConfig

log = logging.getLogger("nomergon.runner")

PROGRESS_PREFIX = "@progress "
RESULT_PREFIX = "@result "
STDERR_TAIL_LINES = 20
CANCEL_POLL_SECONDS = 1.0
TERM_GRACE_SECONDS = 10.0
_EOF = object()


@dataclass(frozen=True, slots=True)
class ParsedLine:
    """One line of child output, classified.

    ``kind`` is ``log`` (a plain line on ``stream``), ``progress`` (``data``
    holds the parsed JSON) or ``result`` (``data`` is the job's result). A
    sentinel line whose JSON does not parse stays a plain log line, so a
    broken emitter is visible in the log rather than swallowed.
    """

    stream: str
    line: str
    kind: str = "log"
    data: dict[str, Any] | None = None


def parse_line(stream: str, line: str) -> ParsedLine:
    """Classify one output line (pure; the protocol lives here)."""
    if stream == "stdout":
        for prefix, kind in ((PROGRESS_PREFIX, "progress"), (RESULT_PREFIX, "result")):
            if line.startswith(prefix):
                try:
                    data = json.loads(line[len(prefix) :])
                except json.JSONDecodeError:
                    break
                if isinstance(data, dict):
                    return ParsedLine(stream, line, kind, data)
                break
    return ParsedLine(stream, line)


@dataclass(slots=True)
class JobOutcome:
    status: str
    result: Any = None
    error: str | None = None


def _write(what: str, fn: Any, *args: Any) -> bool:
    """Run one bookkeeping write; a failing database (disk full, dropped
    connection) is logged and skipped, never fatal. The job's stdout/stderr is
    still consumed and its exit code still decides its outcome; only the log
    rows for the moment of the outage are lost. The connection is autocommit,
    so a failed statement leaves nothing to roll back."""
    try:
        fn(*args)
        return True
    except Exception as exc:  # noqa: BLE001
        log.warning("%s not recorded: %s", what, str(exc).splitlines()[0] if str(exc) else type(exc).__name__)
        return False


def _note(conn: psycopg.Connection[Any], job_id: int, line: str) -> None:
    _write(f"job {job_id} note", db.append_event, conn, job_id, "system", line)


def job_environment(cfg: WorkerConfig, job_id: int) -> dict[str, str]:
    """The child's environment: the worker's, plus the switches the packages honour."""
    env = dict(os.environ)
    env.update(
        {
            "PYTHONUNBUFFERED": "1",
            "NOMOS_PYTHON": sys.executable,
            "WORKFLOW_ENCODER": "db",
            "WORKFLOW_DATABASE_URL": cfg.database_url,
            "EUROMOD_DATABASE_URL": cfg.database_url,
            "EVAL_DATABASE_URL": cfg.database_url,
            "WORKER_JOB_ID": str(job_id),
        }
    )
    if cfg.default_model:
        # The worker's default LLM: what a job with no model runs on, and the
        # critique model of every workflow run. It overrides a WORKFLOW_MODEL
        # inherited from a .env — the published list is the authority on what
        # runs here (free-text model strings hid the Azure mix-up for a month).
        # An explicit WORKFLOW_CRITIQUE_MODEL is left to the operator.
        env["WORKFLOW_MODEL"] = cfg.default_model
    env.pop("VIRTUAL_ENV", None)
    return env


def _pump(stream: IO[str], name: str, sink: queue.Queue[Any]) -> None:
    try:
        for raw in stream:
            sink.put((name, raw.rstrip("\r\n")))
    finally:
        sink.put((name, _EOF))


def run_job(
    conn: psycopg.Connection[Any],
    cfg: WorkerConfig,
    job: dict[str, Any],
    *,
    stop: threading.Event | None = None,
) -> JobOutcome:
    """Run one claimed job to completion and return its final status."""
    job_id = int(job["id"])
    job_type = str(job["job_type"])
    try:
        payload = jobs.parse_payload(job_type, job["payload"])
    except ValueError as exc:
        _note(conn, job_id, f"invalid payload: {exc}")
        return JobOutcome("failed", error=f"invalid payload: {exc}")

    scratch = Path(tempfile.mkdtemp(prefix=f"nomergon-job-{job_id}-"))
    try:
        cwd = jobs.package_dir(job_type, cfg)
        argv = jobs.build_command(job_type, payload, cfg, scratch_dir=scratch)
        return _run_subprocess(conn, cfg, job_id, job_type, payload, argv, cwd, stop)
    except Exception as exc:  # noqa: BLE001 - the job must end in a final state
        log.exception("job %s crashed the runner", job_id)
        _note(conn, job_id, f"runner error: {exc}")
        return JobOutcome("failed", error=f"runner error: {exc}")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def _run_subprocess(
    conn: psycopg.Connection[Any],
    cfg: WorkerConfig,
    job_id: int,
    job_type: str,
    payload: Any,
    argv: list[str],
    cwd: Path,
    stop: threading.Event | None,
) -> JobOutcome:
    _note(conn, job_id, "$ " + " ".join(_redact(argv, cfg.database_url)))
    _note(conn, job_id, f"cwd: {cwd}")

    try:
        child = subprocess.Popen(
            argv,
            cwd=cwd,
            env=job_environment(cfg, job_id),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
    except OSError as exc:
        _note(conn, job_id, f"failed to start: {exc}")
        return JobOutcome("failed", error=f"failed to start: {exc}")

    sink: queue.Queue[Any] = queue.Queue()
    assert child.stdout is not None and child.stderr is not None
    readers = [
        threading.Thread(target=_pump, args=(child.stdout, "stdout", sink), daemon=True),
        threading.Thread(target=_pump, args=(child.stderr, "stderr", sink), daemon=True),
    ]
    for reader in readers:
        reader.start()

    stderr_tail: deque[str] = deque(maxlen=STDERR_TAIL_LINES)
    stdout_tail: deque[str] = deque(maxlen=STDERR_TAIL_LINES)
    last_progress: dict[str, Any] | None = None
    result_line: dict[str, Any] | None = None
    open_streams = 2
    cancelled = False
    stopped = False
    next_cancel_check = time.monotonic()

    while open_streams > 0:
        pending: list[tuple[str, str, dict[str, Any] | None]] = []
        try:
            item = sink.get(timeout=0.2)
        except queue.Empty:
            item = None
        while item is not None:
            name, value = item
            if value is _EOF:
                open_streams -= 1
            else:
                parsed = parse_line(name, value)
                if parsed.kind == "progress":
                    last_progress = parsed.data
                    pending.append(("progress", parsed.line, parsed.data))
                elif parsed.kind == "result":
                    result_line = parsed.data
                else:
                    pending.append((parsed.stream, parsed.line, None))
                    (stderr_tail if name == "stderr" else stdout_tail).append(parsed.line)
            try:
                item = sink.get_nowait()
            except queue.Empty:
                item = None
        if pending:
            _write(f"job {job_id} log lines", db.append_events, conn, job_id, pending)
            if last_progress is not None and any(stream == "progress" for stream, _, _ in pending):
                _write(f"job {job_id} progress", db.set_progress, conn, job_id, last_progress)

        now = time.monotonic()
        if not (cancelled or stopped) and child.poll() is None and now >= next_cancel_check:
            next_cancel_check = now + CANCEL_POLL_SECONDS
            if stop is not None and stop.is_set():
                stopped = True
                _note(conn, job_id, "worker stopping: terminating the job")
                _terminate(child)
            elif _cancel_requested(conn, job_id):
                cancelled = True
                _note(conn, job_id, "cancel requested: terminating the job")
                _terminate(child)

    returncode = child.wait()
    for reader in readers:
        reader.join(timeout=1.0)

    if stopped:
        _note(conn, job_id, "worker stopped")
        return JobOutcome("failed", error="worker stopped")
    if cancelled:
        _note(conn, job_id, "cancelled")
        return JobOutcome("cancelled")
    _note(conn, job_id, f"exit code {returncode}")
    if returncode != 0:
        error = "\n".join(stderr_tail) or f"exit code {returncode}"
        return JobOutcome("failed", error=error)
    try:
        result = jobs.extract_result(
            job_type,
            payload,
            result_line=result_line,
            last_progress=last_progress,
            stdout_tail=list(stdout_tail),
        )
    except Exception as exc:  # noqa: BLE001
        return JobOutcome("failed", error=f"could not read the job's result: {exc}")
    return JobOutcome("succeeded", result=result)


def _cancel_requested(conn: psycopg.Connection[Any], job_id: int) -> bool:
    try:
        return db.cancel_requested(conn, job_id)
    except Exception as exc:  # noqa: BLE001 - an unreadable flag is "not cancelled"
        log.warning("job %s cancel flag unreadable: %s", job_id, str(exc).splitlines()[0])
        return False


def _terminate(child: subprocess.Popen[str]) -> None:
    """SIGTERM, wait the grace period, then SIGKILL."""
    if child.poll() is not None:
        return
    try:
        child.send_signal(signal.SIGTERM)
        child.wait(timeout=TERM_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait()
    except ProcessLookupError:
        pass


def _redact(argv: list[str], database_url: str) -> list[str]:
    """Hide the database password in the logged command line."""
    if "@" not in database_url or "://" not in database_url:
        return argv
    scheme, rest = database_url.split("://", 1)
    credentials, host = rest.rsplit("@", 1)
    user = credentials.split(":", 1)[0]
    redacted = f"{scheme}://{user}:***@{host}"
    return [redacted if arg == database_url else arg for arg in argv]
