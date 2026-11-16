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
                "SELECT metadata FROM fetch_snapshots WHERE run_id = %s", (run_id,)
            ).fetchall()
        assert status == "failed"
        assert stats["error"] == "parser broke"
        assert len(snapshots) == 1
        # the SourceRef travels with the bytes, so `reparse` works for any country
        assert snapshots[0][0]["source_ref"]["source_id"] == "TEST"
    finally:
        with psycopg.connect(DB_URL) as conn:
            conn.execute("DELETE FROM fetch_snapshots WHERE run_id = %s", (run_id,))
            conn.execute("DELETE FROM fetch_runs WHERE id = %s", (run_id,))


def test_reparse_reads_the_stored_source_ref(monkeypatch):
    """No URL mapping needed: the ref stored with the snapshot is replayed."""
    from uuid import uuid4

    from nomotheca_ingest.core import pipeline
    from nomotheca_ingest.core.ir import ParsedDoc

    stored = {"jurisdiction": "NL", "source_code": "NL-BWB", "source_id": "BWBR0011353", "source_type": "instrument"}
    rows = [
        (uuid4(), "https://repository.officiele-overheidspublicaties.nl/x.xml", 200, "text/xml", "0" * 64, b"<x/>", "NL-BWB", stored),
        (uuid4(), "https://example.invalid/old", 200, "text/xml", "0" * 64, b"<x/>", "NL-BWB", None),
    ]

    class Conn:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def execute(self, *args):
            class R:
                def fetchall(self_inner):
                    return rows
            return R()

    parsed = []

    class Adapter:
        jurisdiction = "NL"

        def source_ref_from_url(self, url, source_code):
            return None

        def parse(self, raw, ref, snapshot):
            parsed.append(ref.source_id)
            return ParsedDoc(ref=ref, instruments=[])

    monkeypatch.setattr(pipeline.psycopg, "connect", lambda url: Conn())
    monkeypatch.setattr(pipeline, "get_adapter", lambda cc: Adapter())
    monkeypatch.setattr(pipeline, "LegislationLoader", lambda conn: None)
    stats = pipeline.reparse_snapshots("NL", "postgresql://unused")
    assert parsed == ["BWBR0011353"]
    assert (stats.snapshots, stats.parsed, stats.skipped) == (2, 1, 1)
