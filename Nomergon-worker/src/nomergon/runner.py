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
from dataclasses import dataclass, field
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
        # The worker's default LLM: what a job with no model runs on. It is
        # WORKFLOW_MODEL itself when that is set (published first); otherwise
        # the first of WORKER_MODELS, so a job never runs on a model the
        # pickers do not show (free-text model strings hid the Azure mix-up for
        # a month). WORKFLOW_CRITIQUE_MODEL is left to the operator.
        env["WORKFLOW_MODEL"] = cfg.default_model
    env.pop("VIRTUAL_ENV", None)
    return env


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
        return _run_subprocess(conn, cfg, job_id, job_type, argv, cwd, stop)
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
    argv: list[str],
    cwd: Path,
    stop: threading.Event | None,
) -> JobOutcome:
    """Start the child, stream its output until both pipes close, map the outcome."""
    _note(conn, job_id, "$ " + " ".join(_redact(argv, cfg.database_url)))
    _note(conn, job_id, f"cwd: {cwd}")
    try:
        child = _start_child(argv, cwd, job_environment(cfg, job_id))
    except OSError as exc:
        _note(conn, job_id, f"failed to start: {exc}")
        return JobOutcome("failed", error=f"failed to start: {exc}")

    output = _ChildOutput(child)
    capture = _Capture()
    interrupt = _Interrupt(conn, job_id, child, stop)
    while output.open:
        capture.record(conn, job_id, output.next_batch())
        interrupt.check()

    returncode = child.wait()
    _kill_group(child)  # nothing the job started outlives it
    output.join()
    return _outcome(conn, job_id, job_type, returncode, interrupt.reason, capture)


def _start_child(argv: list[str], cwd: Path, env: dict[str, str]) -> subprocess.Popen[str]:
    return subprocess.Popen(
        argv,
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        # Its own process group, so a cancel reaches what the job started
        # too: the scout runs an ingest and an embeddings build (GPU, the
        # advisory lock) as grandchildren (code audit D11).
        start_new_session=os.name == "posix",
    )


class _ChildOutput:
    """The child's stdout and stderr, read on two threads into one queue."""

    def __init__(self, child: subprocess.Popen[str]) -> None:
        assert child.stdout is not None and child.stderr is not None
        self._sink: queue.Queue[Any] = queue.Queue()
        self._open = 2
        self._readers = [
            threading.Thread(target=self._pump, args=(child.stdout, "stdout"), daemon=True),
            threading.Thread(target=self._pump, args=(child.stderr, "stderr"), daemon=True),
        ]
        for reader in self._readers:
            reader.start()

    def _pump(self, stream: IO[str], name: str) -> None:
        try:
            for raw in stream:
                self._sink.put((name, raw.rstrip("\r\n")))
        finally:
            self._sink.put((name, _EOF))

    @property
    def open(self) -> bool:
        """Until both pipes reached end of file."""
        return self._open > 0

    def next_batch(self, timeout: float = 0.2) -> list[ParsedLine]:
        """Every line available now, waiting up to ``timeout`` for the first."""
        lines: list[ParsedLine] = []
        try:
            item = self._sink.get(timeout=timeout)
        except queue.Empty:
            return lines
        while item is not None:
            name, value = item
            if value is _EOF:
                self._open -= 1
            else:
                lines.append(parse_line(name, value))
            try:
                item = self._sink.get_nowait()
            except queue.Empty:
                item = None
        return lines

    def join(self) -> None:
        for reader in self._readers:
            reader.join(timeout=1.0)


@dataclass(slots=True)
class _Capture:
    """What the job's output leaves behind: the protocol lines and the stderr tail."""

    stderr_tail: deque[str] = field(default_factory=lambda: deque(maxlen=STDERR_TAIL_LINES))
    last_progress: dict[str, Any] | None = None
    result_line: dict[str, Any] | None = None

    def record(self, conn: psycopg.Connection[Any], job_id: int, lines: list[ParsedLine]) -> None:
        """Keep the protocol lines; write the batch as events and the latest progress."""
        pending: list[tuple[str, str, dict[str, Any] | None]] = []
        for parsed in lines:
            if parsed.kind == "progress":
                self.last_progress = parsed.data
                pending.append(("progress", parsed.line, parsed.data))
            elif parsed.kind == "result":
                self.result_line = parsed.data
            else:
                pending.append((parsed.stream, parsed.line, None))
                if parsed.stream == "stderr":
                    self.stderr_tail.append(parsed.line)
        if not pending:
            return
        _write(f"job {job_id} log lines", db.append_events, conn, job_id, pending)
        if self.last_progress is not None and any(stream == "progress" for stream, _, _ in pending):
            _write(f"job {job_id} progress", db.set_progress, conn, job_id, self.last_progress)


class _Interrupt:
    """Polls, at most once a second, for a worker stop or a cancel request,
    and terminates the job's process group on the first one seen."""

    def __init__(
        self,
        conn: psycopg.Connection[Any],
        job_id: int,
        child: subprocess.Popen[str],
        stop: threading.Event | None,
    ) -> None:
        self.conn, self.job_id, self.child, self.stop = conn, job_id, child, stop
        #: None while the job runs undisturbed, else "stopped" or "cancelled".
        self.reason: str | None = None
        self._next_check = time.monotonic()

    def check(self) -> None:
        now = time.monotonic()
        if self.reason is not None or self.child.poll() is not None or now < self._next_check:
            return
        self._next_check = now + CANCEL_POLL_SECONDS
        if self.stop is not None and self.stop.is_set():
            self.reason = "stopped"
            _note(self.conn, self.job_id, "worker stopping: terminating the job")
        elif _cancel_requested(self.conn, self.job_id):
            self.reason = "cancelled"
            _note(self.conn, self.job_id, "cancel requested: terminating the job")
        else:
            return
        _terminate(self.child)


def _outcome(
    conn: psycopg.Connection[Any],
    job_id: int,
    job_type: str,
    returncode: int,
    interrupted: str | None,
    capture: _Capture,
) -> JobOutcome:
    """The job's final status, from how it ended."""
    if interrupted == "stopped":
        _note(conn, job_id, "worker stopped")
        return JobOutcome("failed", error="worker stopped")
    if interrupted == "cancelled":
        _note(conn, job_id, "cancelled")
        return JobOutcome("cancelled")
    _note(conn, job_id, f"exit code {returncode}")
    if returncode != 0:
        error = "\n".join(capture.stderr_tail) or f"exit code {returncode}"
        return JobOutcome("failed", error=error)
    try:
        result = jobs.extract_result(job_type, result_line=capture.result_line, last_progress=capture.last_progress)
    except Exception as exc:  # noqa: BLE001
        return JobOutcome("failed", error=f"could not read the job's result: {exc}")
    return JobOutcome("succeeded", result=result)


def _cancel_requested(conn: psycopg.Connection[Any], job_id: int) -> bool:
    try:
        return db.cancel_requested(conn, job_id)
    except Exception as exc:  # noqa: BLE001 - an unreadable flag is "not cancelled"
        log.warning("job %s cancel flag unreadable: %s", job_id, str(exc).splitlines()[0])
        return False


def _signal_group(child: subprocess.Popen[str], sig: int) -> None:
    """Signal the job's whole process group (POSIX), else the child alone."""
    try:
        if os.name == "posix":
            os.killpg(child.pid, sig)
        else:
            child.send_signal(sig)
    except (ProcessLookupError, PermissionError):
        pass


def _terminate(child: subprocess.Popen[str]) -> None:
    """SIGTERM the job's process group, wait the grace period, then SIGKILL it."""
    if child.poll() is not None:
        _kill_group(child)
        return
    _signal_group(child, signal.SIGTERM)
    try:
        child.wait(timeout=TERM_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        _signal_group(child, signal.SIGKILL)
        child.wait()
    _kill_group(child)


def _kill_group(child: subprocess.Popen[str]) -> None:
    """SIGKILL whatever is left in the job's process group (POSIX only)."""
    if os.name == "posix":
        _signal_group(child, signal.SIGKILL)


def _redact(argv: list[str], database_url: str) -> list[str]:
    """Hide the database password in the logged command line."""
    if "@" not in database_url or "://" not in database_url:
        return argv
    scheme, rest = database_url.split("://", 1)
    credentials, host = rest.rsplit("@", 1)
    user = credentials.split(":", 1)[0]
    redacted = f"{scheme}://{user}:***@{host}"
    return [redacted if arg == database_url else arg for arg in argv]
