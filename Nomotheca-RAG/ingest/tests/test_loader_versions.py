"""A re-fetch revises the version it already holds (needs the stack up; rolled back)."""

from __future__ import annotations

import os
from datetime import date
from uuid import uuid4

import psycopg
import pytest

from nomotheca_ingest.core.ir import (
    Authenticity,
    InstrumentIR,
    ParsedDoc,
    SourceRef,
    TextIR,
    UnitIR,
    VersionIR,
    VersionStatus,
)
from nomotheca_ingest.core.loader import LegislationLoader

DB_URL = os.environ.get("EUROMOD_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


@pytest.fixture
def conn():
    try:
        connection = psycopg.connect(DB_URL, connect_timeout=2)
    except psycopg.OperationalError:
        pytest.skip("database not reachable")
    yield connection
    connection.close()


def _doc(snapshot_id, valid_to=None, status=VersionStatus.IN_FORCE) -> ParsedDoc:
    ref = SourceRef(jurisdiction="FR", source_code="FR-LEGI", source_id="ZZTEST", source_type="instrument")
    version = VersionIR(
        valid_from=date(2020, 1, 1), valid_to=valid_to, status=status,
        source_version_id="ZZTEST-v1", fetch_snapshot_id=snapshot_id,
        texts=[TextIR(lang="fr", authenticity=Authenticity.AUTHENTIC, content="Texte.")],
    )
    unit = UnitIR(path="art_1", unit_type="article", citation="ZZTEST art. 1", versions=[version])
    instrument = InstrumentIR(
        jurisdiction="FR", source_code="FR-LEGI", instrument_type="loi", national_id="ZZTEST",
        title={"fr": "Loi de test"}, units=[unit],
    )
    return ParsedDoc(ref=ref, instruments=[instrument])


def test_a_later_learned_end_and_repeal_are_recorded(conn):
    with conn.transaction(force_rollback=True):
        run = conn.execute(
            "INSERT INTO fetch_runs (source_id, skill_version, trigger) "
            "VALUES ((SELECT id FROM sources WHERE code = 'FR-LEGI'), 'test', 'manual') RETURNING id"
        ).fetchone()[0]
        snaps = [
            conn.execute(
                "INSERT INTO fetch_snapshots (run_id, source_id, url, content_hash, raw_content) "
                "VALUES (%s, (SELECT id FROM sources WHERE code = 'FR-LEGI'), %s, 'x', 'x') RETURNING id",
                (run, f"https://test.invalid/{uuid4()}"),
            ).fetchone()[0]
            for _ in range(2)
        ]
        loader = LegislationLoader(conn)
        loader.load(_doc(snaps[0]))
        loader.load(_doc(snaps[1], valid_to=date(2024, 1, 1), status=VersionStatus.REPEALED))
        validity, status, snapshot = conn.execute(
            "SELECT v.validity::text, v.version_status, v.fetch_snapshot_id FROM legal_unit_versions v "
            "WHERE v.source_version_id = 'ZZTEST-v1'"
        ).fetchone()
        assert validity == "[2020-01-01,2024-01-01)"
        assert status == "repealed"
        assert snapshot == snaps[1]
