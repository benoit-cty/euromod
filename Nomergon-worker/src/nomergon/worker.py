"""The serve loop: one worker, one job at a time, plus the encode lane."""

from __future__ import annotations

import logging
import signal
import socket
import sys
import threading
import time
from typing import Any

import psycopg

from . import __version__, db, runner
from .config import EMBEDDING_MODEL_NAME, WorkerConfig
from .encoder import EncodeLane, describe_device

log = logging.getLogger("nomergon.worker")

PRUNE_INTERVAL_SECONDS = 24 * 3600.0


class Heartbeat(threading.Thread):
    """Touches ``ops.workers.heartbeat_at`` on its own connection."""

    def __init__(self, cfg: WorkerConfig, stop: threading.Event) -> None:
        super().__init__(name="nomergon-heartbeat", daemon=True)
        self.cfg = cfg
        self.stop_event = stop
        self.current_job_id: int | None = None

    def run(self) -> None:
        conn: psycopg.Connection[Any] | None = None
        try:
            while not self.stop_event.wait(self.cfg.heartbeat_seconds):
                try:
                    if conn is None or conn.closed:
                        conn = db.connect(self.cfg.database_url)
                    db.heartbeat(conn, self.cfg.worker_id, self.current_job_id)
                except Exception as exc:  # noqa: BLE001 - a missed beat is not fatal
                    log.warning("heartbeat failed: %s", str(exc).splitlines()[0] if str(exc) else type(exc).__name__)
                    if conn is not None:
                        try:
                            conn.close()
                        except Exception:  # noqa: BLE001
                            pass
                        conn = None  # reconnect on the next beat
        finally:
            if conn is not None:
                conn.close()


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    # The hub client logs every HEAD it makes while resolving BGE-M3.
    for noisy in ("httpx", "httpcore", "urllib3"):
        logging.getLogger(noisy).setLevel(max(level, logging.WARNING))


FINISH_RETRY_SECONDS = 5.0
FINISH_RETRY_ATTEMPTS = 60  # five minutes of outage before giving up on the row


def _finish_with_retry(
    conn: psycopg.Connection[Any],
    cfg: WorkerConfig,
    job_id: int,
    outcome: runner.JobOutcome,
    stop: threading.Event,
) -> psycopg.Connection[Any]:
    """Write the job's final status, reconnecting as needed; returns the
    connection to keep using (a new one if the old broke)."""
    for attempt in range(1, FINISH_RETRY_ATTEMPTS + 1):
        try:
            if conn.closed:
                conn = db.connect(cfg.database_url)
            db.finish_job(conn, job_id, outcome.status, outcome.result, outcome.error)
            return conn
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "job %s: could not record final status %s (attempt %d/%d): %s",
                job_id, outcome.status, attempt, FINISH_RETRY_ATTEMPTS, str(exc).splitlines()[0],
            )
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                pass
            try:
                conn = db.connect(cfg.database_url)
            except Exception:  # noqa: BLE001
                pass
            if stop.wait(FINISH_RETRY_SECONDS):
                break
    log.error("job %s: final status %s never recorded; the stale-heartbeat rule will mark it failed", job_id, outcome.status)
    return conn


def serve(cfg: WorkerConfig) -> None:
    """Register, publish, then claim and run jobs until SIGTERM/SIGINT."""
    stop = threading.Event()

    def _request_stop(signum: int, _frame: Any) -> None:
        log.info("received %s, stopping after the current job", signal.Signals(signum).name)
        stop.set()

    signal.signal(signal.SIGTERM, _request_stop)
    signal.signal(signal.SIGINT, _request_stop)

    conn = db.connect(cfg.database_url)
    device = describe_device()
    log.info("worker %s starting (device=%s, models=%s)", cfg.worker_id, device, cfg.models or "none")

    db.apply_schema(conn)
    db.prune_dead_workers(conn, cfg.stale_seconds)
    db.register_worker(conn, cfg.worker_id, socket.gethostname(), device, __version__)
    failed = db.fail_stale_running_jobs(conn, cfg.stale_seconds)
    if failed:
        log.warning("marked %d orphaned running job(s) failed: %s", len(failed), failed)
    db.publish_models(conn, cfg.worker_id, cfg.models, [EMBEDDING_MODEL_NAME])

    heartbeat = Heartbeat(cfg, stop)
    heartbeat.start()
    encoder = EncodeLane(cfg, stop)
    encoder.start()

    next_prune = time.monotonic()
    try:
        while not stop.is_set():
            if time.monotonic() >= next_prune:
                next_prune = time.monotonic() + PRUNE_INTERVAL_SECONDS
                try:
                    pruned = db.prune_events(conn, cfg.event_retention_days)
                    if pruned:
                        log.info("pruned %d job event(s) older than %d days", pruned, cfg.event_retention_days)
                except Exception:  # noqa: BLE001
                    log.exception("event pruning failed")

            try:
                job = db.claim_job(conn, cfg.worker_id)
            except Exception:  # noqa: BLE001 - keep polling through a DB hiccup
                log.exception("claim failed; retrying")
                stop.wait(cfg.poll_seconds)
                continue
            if job is None:
                stop.wait(cfg.poll_seconds)
                continue

            job_id = int(job["id"])
            heartbeat.current_job_id = job_id
            log.info("job %s (%s) started", job_id, job["job_type"])
            outcome = runner.run_job(conn, cfg, job, stop=stop)
            # The final status is the one write that must land: retry it on a
            # fresh connection through a database outage (disk full, restart)
            # rather than leave the job "running" with a live heartbeat.
            conn = _finish_with_retry(conn, cfg, job_id, outcome, stop)
            heartbeat.current_job_id = None
            log.info("job %s %s%s", job_id, outcome.status, f": {outcome.error.splitlines()[-1]}" if outcome.error else "")
    finally:
        stop.set()
        heartbeat.join(timeout=2.0)
        encoder.join(timeout=2.0)
        try:
            db.unregister_worker(conn, cfg.worker_id)
        finally:
            conn.close()
        log.info("worker %s stopped", cfg.worker_id)
