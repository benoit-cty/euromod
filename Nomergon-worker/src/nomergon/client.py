"""Submit a job and wait for it: what a Python caller with a connection needs.

The pipeline must not import this (dependency direction is worker → packages);
it has its own copy in ``nomoscope_workflow/encode_client.py``.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

import psycopg

from . import db
from .db import FINAL_STATUSES

EventCallback = Callable[[dict[str, Any]], None]


class JobTimeout(TimeoutError):
    """The job did not reach a final status in time."""


def submit(conn: psycopg.Connection[Any], job_type: str, payload: dict[str, Any], priority: int = 0) -> int:
    """Insert one queued job and return its id (payload validated worker-side)."""
    job_id = db.submit_job(conn, job_type, payload, priority)
    if not conn.autocommit:
        conn.commit()
    return job_id


def wait(
    conn: psycopg.Connection[Any],
    job_id: int,
    timeout: float | None = None,
    poll: float = 0.5,
    on_event: EventCallback | None = None,
) -> dict[str, Any]:
    """Poll until the job is final; stream new events to ``on_event`` meanwhile."""
    deadline = None if timeout is None else time.monotonic() + timeout
    last_event = 0
    while True:
        if on_event is not None:
            for event in db.events_after(conn, job_id, last_event):
                last_event = int(event["id"])
                on_event(event)
        row = db.get_job(conn, job_id)
        if not conn.autocommit:
            conn.commit()  # release the snapshot so the next poll sees new rows
        if row is None:
            msg = f"job {job_id} does not exist"
            raise KeyError(msg)
        if row["status"] in FINAL_STATUSES:
            if on_event is not None:
                for event in db.events_after(conn, job_id, last_event):
                    last_event = int(event["id"])
                    on_event(event)
            return row
        if deadline is not None and time.monotonic() >= deadline:
            msg = f"job {job_id} still {row['status']} after {timeout}s"
            raise JobTimeout(msg)
        time.sleep(poll)


def cancel(conn: psycopg.Connection[Any], job_id: int) -> bool:
    """Ask the worker to stop the job (a queued job is cancelled at once)."""
    changed = db.request_cancel(conn, job_id)
    if not conn.autocommit:
        conn.commit()
    return changed
