"""The review queue as rows: write_item, decide_review_item, and a mock run that enqueues.

Needs the dev Postgres (docker compose up -d at the repo root, then
`nomoscope-workflow init-param-db`); skipped when it is not reachable.
Only mock/extractor is ever used here.
"""

from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timezone

import psycopg
import pytest

from nomoscope_workflow import paramdb, queue_store
from nomoscope_workflow.config import WorkflowConfig, load_config
from nomoscope_workflow.schema import (
    Decision,
    ItemStatus,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    ReviewItem,
    Routing,
)

DATABASE_URL = os.environ.get("WORKFLOW_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


@pytest.fixture(scope="module")
def conn():
    try:
        connection = psycopg.connect(DATABASE_URL, connect_timeout=3)
        ok = connection.execute("SELECT to_regclass('params.review_queue')").fetchone()[0]
    except Exception as exc:  # pragma: no cover - environment-dependent
        pytest.skip(f"dev Postgres not reachable ({exc.__class__.__name__}: {exc})")
    if not ok:
        pytest.skip("params.review_queue missing — run `nomoscope-workflow init-param-db`")
    yield connection
    connection.close()


@pytest.fixture
def scratch_target(conn):
    """A unique model_target whose queue/audit rows are deleted afterwards."""
    target = f"euromod://FR/test_queue/def_const/$q_{uuid.uuid4().hex[:8]}"
    yield target
    conn.rollback()
    conn.execute("DELETE FROM params.review_decisions WHERE model_target = %s", (target,))
    conn.execute("DELETE FROM params.review_queue WHERE model_target = %s", (target,))
    conn.commit()


def _item(target: str, status: ItemStatus = ItemStatus.PENDING, run_id: str = "run-1") -> ReviewItem:
    record = ParameterRecord(
        information=ParameterInformation(country="FR", model_target=target, value_type="scalar", unit="/1"),
        values=[ParameterValue(value=0.45, valid_from=date(2024, 1, 1))],
    )
    return ReviewItem(
        id=queue_store.item_id("FR", target, 2025),
        run_id=run_id,
        created_at=datetime.now(timezone.utc),
        country="FR",
        model_target=target,
        as_of=date(2025, 7, 1),
        system_year=2025,
        value_type="scalar",
        unit="/1",
        routing=Routing.UNCHANGED,
        status=status,
        proposed_record=record,
        parameter_ref=target,
    )


def test_write_item_replaces_pending_and_keeps_decided_unless_forced(conn, scratch_target):
    item = _item(scratch_target)
    assert queue_store.write_item(conn, item)
    assert queue_store.load_item(conn, item.id).run_id == "run-1"

    # a re-run replaces a pending item
    assert queue_store.write_item(conn, _item(scratch_target, run_id="run-2"))
    assert queue_store.load_item(conn, item.id).run_id == "run-2"

    # a decided item is immutable to re-runs, unless forced
    assert queue_store.write_item(conn, _item(scratch_target, ItemStatus.ACCEPTED, run_id="run-3"), force=True)
    assert not queue_store.write_item(conn, _item(scratch_target, run_id="run-4"))
    kept = queue_store.load_item(conn, item.id)
    assert kept.run_id == "run-3" and kept.status == ItemStatus.ACCEPTED
    assert queue_store.write_item(conn, _item(scratch_target, run_id="run-5"), force=True)
    assert queue_store.load_item(conn, item.id).status == ItemStatus.PENDING

    listed = queue_store.load_items(conn, country="FR", status="pending")
    assert item.id in {i.id for i in listed}
    assert item.id not in {i.id for i in queue_store.load_items(conn, status="accepted")}


def test_export_accepted_groups_records_by_country(conn, scratch_target):
    assert queue_store.write_item(conn, _item(scratch_target, ItemStatus.ACCEPTED))
    exported = queue_store.export_accepted(conn)
    records = [r for r in exported.get("FR", []) if r["information"]["model_target"] == scratch_target]
    assert len(records) == 1
    assert records[0]["values"][0]["value"] == 0.45

    assert queue_store.write_item(conn, _item(scratch_target, ItemStatus.REJECTED), force=True)
    assert not [
        r for r in queue_store.export_accepted(conn).get("FR", [])
        if r["information"]["model_target"] == scratch_target
    ]


def test_decide_review_item_records_the_decision_and_updates_the_item(conn, scratch_target):
    """The UI's decide path: one SQL call, audit row + queue update, idempotent on decided_at."""
    item = _item(scratch_target)
    assert queue_store.write_item(conn, item)
    decided_at = datetime(2026, 9, 22, 10, 0, tzinfo=timezone.utc)
    decided = item.model_copy(
        update={"status": ItemStatus.ACCEPTED, "decision": Decision(action=ItemStatus.ACCEPTED, decided_at=decided_at)}
    )
    entry = {
        "action": "accepted",
        "reviewer": "ignored-by-the-function",
        "note": "looks right",
        "item_id": item.id,
        "run_id": item.run_id,
        "model_target": scratch_target,
        "as_of": "2025-07-01",
        "routing": "unchanged",
        "decided_at": decided_at.isoformat(),
        "logged_at": decided_at.isoformat(),
    }
    with conn.transaction():
        (audit_id,) = conn.execute(
            "SELECT params.decide_review_item(%s, %s::jsonb, %s::jsonb)",
            (item.id, psycopg.types.json.Jsonb(decided.model_dump(mode="json")), psycopg.types.json.Jsonb(entry)),
        ).fetchone()
    assert audit_id is not None

    row = conn.execute(
        "SELECT action, reviewer, note, model_target FROM params.review_decisions WHERE id = %s", (audit_id,)
    ).fetchone()
    assert row == ("accepted", conn.execute("SELECT current_user").fetchone()[0], "looks right", scratch_target)

    stored = queue_store.load_item(conn, item.id)
    assert stored.status == ItemStatus.ACCEPTED
    assert stored.decision is not None and stored.decision.action == ItemStatus.ACCEPTED
    assert conn.execute(
        "SELECT status FROM params.review_queue WHERE item_id = %s", (item.id,)
    ).fetchone()[0] == "accepted"

    # the same decision again (same decided_at) is a no-op on the audit table
    with conn.transaction():
        (again,) = conn.execute(
            "SELECT params.decide_review_item(%s, %s::jsonb, %s::jsonb)",
            (item.id, psycopg.types.json.Jsonb(decided.model_dump(mode="json")), psycopg.types.json.Jsonb(entry)),
        ).fetchone()
    assert again is None
    assert conn.execute(
        "SELECT count(*) FROM params.review_decisions WHERE item_id = %s", (item.id,)
    ).fetchone()[0] == 1

    # a decided item is now immutable to a re-run
    assert not queue_store.write_item(conn, _item(scratch_target, run_id="run-9"))

    # a decision on an item that is not in the queue fails outright
    with pytest.raises(psycopg.Error):
        with conn.transaction():
            conn.execute(
                "SELECT params.decide_review_item(%s, %s::jsonb, %s::jsonb)",
                ("no_such_item", psycopg.types.json.Jsonb({}), psycopg.types.json.Jsonb(entry)),
            )


def test_mock_run_from_the_params_db_lands_in_the_queue(conn):
    """run-targets' path: load a record from params.*, run the mock model, find the row."""
    from nomoscope_workflow.pipeline import run_parameter
    from nomoscope_workflow.tracing import setup_tracing

    target = "euromod://FR/tin_fr/def_const/$tinrt_cdhr"
    try:
        record = paramdb.load_record(conn, target)
    except KeyError:
        pytest.skip(f"{target} not ingested (ingest-params FR)")
    cfg: WorkflowConfig = load_config()
    cfg.database_url = DATABASE_URL
    cfg.model = cfg.critique_model = "mock/extractor"
    cfg.tracing_enabled = False
    cfg.scout = "off"
    cfg.embedding_model_id = 99  # placeholder embedder: no encoder subprocess, no worker

    item = run_parameter(cfg, setup_tracing(cfg), record, date(2025, 7, 1), force=True, parameter_ref=target)

    assert item.id == queue_store.item_id("FR", target, 2025)
    assert item.parameter_ref == target
    stored = queue_store.load_item(conn, item.id)
    assert stored is not None and stored.run_id == item.run_id
    assert stored.routing == item.routing
