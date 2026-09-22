"""Query encoding through the worker's job table (`WORKFLOW_ENCODER=db`).

The pipeline never loads BGE-M3 itself when it runs inside the worker: it
submits an `encode` job to `ops.jobs` and polls for the result, which the
worker computes in-process with the model kept warm (a priority lane that
never waits behind a GPU batch). This is a deliberately tiny copy of
`nomergon.client.submit`/`wait` — the dependency direction is worker ->
packages, so the pipeline must not import nomergon.
"""

from __future__ import annotations

import json
import time

import psycopg

ENCODE_PRIORITY = 100


def _submit(database_url: str, payload: dict, timeout: float, poll: float) -> dict:
    """Insert one encode job, poll it to a terminal state, return its result."""
    with psycopg.connect(database_url, autocommit=True) as conn:
        job_id = conn.execute(
            "INSERT INTO ops.jobs (job_type, payload, priority) VALUES ('encode', %s, %s) RETURNING id",
            (json.dumps(payload, ensure_ascii=False), ENCODE_PRIORITY),
        ).fetchone()[0]
        deadline = time.monotonic() + timeout
        while True:
            status, result, error = conn.execute(
                "SELECT status, result, error FROM ops.jobs WHERE id = %s", (job_id,)
            ).fetchone()
            if status == "succeeded":
                return result or {}
            if status in ("failed", "cancelled"):
                raise RuntimeError(error or f"encode job {job_id} {status}")
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"encode job {job_id} still {status} after {timeout:.0f}s (no worker alive?)"
                )
            time.sleep(poll)


def encode_via_jobs(database_url: str, query: str, timeout: float = 60.0, poll: float = 0.1) -> str:
    """halfvec literal for `query`, computed by the worker.

    Raises RuntimeError when the job failed or was cancelled, TimeoutError
    when no worker picked it up in time.
    """
    return _submit(database_url, {"query": query}, timeout, poll)["halfvec"]


def score_via_jobs(
    database_url: str,
    query: str,
    sentences: list[str],
    timeout: float = 60.0,
    poll: float = 0.1,
) -> list[float]:
    """Cosine similarities of `query` against `sentences`, computed by the worker."""
    return list(
        _submit(database_url, {"query": query, "sentences": list(sentences)}, timeout, poll)[
            "similarities"
        ]
    )
