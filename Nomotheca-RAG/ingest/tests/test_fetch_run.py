"""A failed ingest still leaves its fetch run and snapshots (needs the stack up).

Before 16 Nov 2026 the `failed` status was written inside the transaction the
re-raised exception rolled back: the dev database held thousands of
`succeeded` runs and not one `failed`.
"""

from __future__ import annotations

import os

import psycopg
import pytest

from nomotheca_ingest.core.db import fetch_run
from nomotheca_ingest.core.ir import SourceRef, Trigger

DB_URL = os.environ.get("EUROMOD_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


@pytest.fixture
def db_available():
    try:
        psycopg.connect(DB_URL, connect_timeout=2).close()
    except psycopg.OperationalError:
        pytest.skip("database not reachable")


def test_a_failed_run_keeps_its_row_and_snapshot(db_available):
    ref = SourceRef(jurisdiction="FR", source_code="FR-LEGI", source_id="TEST", source_type="instrument")
    run_id = None
    with pytest.raises(RuntimeError, match="parser broke"):
        with fetch_run(DB_URL, "FR-LEGI", "test-0", Trigger.MANUAL) as run:
            run_id = run.id
            run.store.write_snapshot(ref, "https://test.invalid/fetch-run", 200, "text/plain", "0" * 64, b"x")
            with psycopg.connect(DB_URL) as conn:
                conn.execute("SELECT 1")
                raise RuntimeError("parser broke")
    try:
        with psycopg.connect(DB_URL) as conn:
            status, stats = conn.execute(
                "SELECT status, stats FROM fetch_runs WHERE id = %s", (run_id,)
            ).fetchone()
            snapshots = conn.execute(
                "SELECT count(*) FROM fetch_snapshots WHERE run_id = %s", (run_id,)
            ).fetchone()[0]
        assert status == "failed"
        assert stats["error"] == "parser broke"
        assert snapshots == 1
    finally:
        with psycopg.connect(DB_URL) as conn:
            conn.execute("DELETE FROM fetch_snapshots WHERE run_id = %s", (run_id,))
            conn.execute("DELETE FROM fetch_runs WHERE id = %s", (run_id,))
