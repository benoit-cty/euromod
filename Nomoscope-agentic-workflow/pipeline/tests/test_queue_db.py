"""The review queue as rows: write_item, decide_review_item, and a mock run that enqueues.

Needs the dev Postgres (docker compose up -d at the repo root, then
`nomoscope-workflow init-param-db`); skipped when it is not reachable.
Only mock/extractor is ever used here.
"""

from __future__ import annotations

import json
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
    SourceType,
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


def _item_with_history(target: str, status: ItemStatus, routing: Routing) -> ReviewItem:
    """An item whose record holds the received history plus the proposed value last."""
    item = _item(target, status)
    item.routing = routing
    item.proposed_record.values = [
        ParameterValue(value=0.40, valid_from=date(2023, 1, 1), valid_to=date(2024, 12, 31)),
        ParameterValue(value=0.45, valid_from=date(2025, 1, 1)),
    ]
    return item


def _change(conn, target: str) -> dict | None:
    return next(
        (c for c in queue_store.export_change_set(conn).get("FR", []) if c["model_target"] == target),
        None,
    )


def test_change_set_holds_only_the_accepted_new_value(conn, scratch_target):
    assert queue_store.write_item(conn, _item_with_history(scratch_target, ItemStatus.ACCEPTED, Routing.CHANGED))
    change = _change(conn, scratch_target)
    assert change["metadata"] == {}
    assert [v["value"]["value"] for v in change["values"]] == [0.45]  # no history
    assert change["values"][0]["system_year"] == 2025

    # an accepted `unchanged` confirms, it changes nothing
    assert queue_store.write_item(
        conn, _item_with_history(scratch_target, ItemStatus.ACCEPTED, Routing.UNCHANGED), force=True
    )
    assert _change(conn, scratch_target) is None
    # a rejected change never leaves
    assert queue_store.write_item(
        conn, _item_with_history(scratch_target, ItemStatus.REJECTED, Routing.CHANGED), force=True
    )
    assert _change(conn, scratch_target) is None


@pytest.fixture
def scratch_parameter(conn, scratch_target):
    """A throwaway params.parameters row (one value row), and its edits cleaned up."""
    parameter_id = conn.execute(
        "INSERT INTO params.parameters (country, model_target, parameter_key, value_type, unit, "
        "unit_structured, label, source_file) VALUES ('FR', %s, %s, 'scalar', 'currency', "
        "'{\"quantity\": \"money\", \"currency\": \"EUR\"}', '{\"en\": \"Old label\"}', 'test') RETURNING id",
        (scratch_target, scratch_target.removeprefix("euromod://").replace("/", ":")),
    ).fetchone()[0]
    conn.execute(
        "INSERT INTO params.model_values (parameter_id, seq, value_raw, value_kind, valid_from) "
        "VALUES (%s, 0, '0.2', 'numeric', '2024-01-01')",
        (parameter_id,),
    )
    conn.commit()
    yield scratch_target
    conn.rollback()
    conn.execute("DELETE FROM params.parameter_edits WHERE model_target = %s", (scratch_target,))
    conn.execute("DELETE FROM params.parameters WHERE model_target = %s", (scratch_target,))
    conn.commit()


def _edit(conn, target: str, field: str, value, note: str | None = None):
    return conn.execute(
        "SELECT params.edit_parameter(%s, %s, %s::jsonb, %s)", (target, field, json.dumps(value), note)
    ).fetchone()[0]


def test_edit_parameter_applies_audits_and_exports_the_net_change(conn, scratch_parameter):
    target = scratch_parameter
    assert _edit(conn, target, "unit", "/1", "a rate, not an amount") is not None
    assert _edit(conn, target, "unit", "/1") is None  # already the store's value: no row
    assert _edit(conn, target, "label", {"en": "New label"}) is not None
    assert _edit(conn, target, "source_type", "national_team") is not None
    unit, structured, label = conn.execute(
        "SELECT unit, unit_structured, label FROM params.parameters WHERE model_target = %s", (target,)
    ).fetchone()
    assert (unit, structured, label) == ("/1", {"quantity": "rate", "scale": "/1"}, {"en": "New label"})
    assert conn.execute(
        "SELECT source_type FROM params.model_values v JOIN params.parameters p ON p.id = v.parameter_id "
        "WHERE p.model_target = %s", (target,)
    ).fetchone()[0] == "national_team"
    reviewer = conn.execute("SELECT DISTINCT reviewer FROM params.parameter_edits WHERE model_target = %s",
                            (target,)).fetchall()
    assert reviewer == [(conn.info.user,)]  # the login, via session_user

    change = _change(conn, target)
    assert change["parameter_key"] == target.removeprefix("euromod://").replace("/", ":")
    assert change["values"] == []
    assert {k: (v["from"], v["to"]) for k, v in change["metadata"].items()} == {
        "unit": ("currency", "/1"),
        "label": ({"en": "Old label"}, {"en": "New label"}),
        "source_type": (None, "national_team"),
    }
    assert change["metadata"]["unit"]["note"] == "a rate, not an amount"

    # an edit reverted is no change: it leaves the change set
    _edit(conn, target, "label", {"en": "Old label"})
    assert set(_change(conn, target)["metadata"]) == {"unit", "source_type"}
    conn.commit()


def test_edits_survive_a_re_ingest(conn, scratch_parameter):
    target = scratch_parameter
    _edit(conn, target, "unit", "currency/month")
    # what ingest-params does to the row, then what it runs last
    conn.execute("UPDATE params.parameters SET unit = 'currency' WHERE model_target = %s", (target,))
    assert paramdb.reapply_parameter_edits(conn) >= 1
    unit, structured = conn.execute(
        "SELECT unit, unit_structured FROM params.parameters WHERE model_target = %s", (target,)
    ).fetchone()
    assert unit == "currency/month"
    assert structured == {"quantity": "money", "currency": "EUR", "period": "month"}  # currency kept
    conn.commit()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("unit", "EUR"),  # not in KNOWN_UNITS
        ("source_type", "hearsay"),
        ("label", {"en": 3}),
        ("label", "bare text"),
        ("model_target", "euromod://FR/x/y/$z"),  # identity is never editable
        ("parameter_key", "FR:x:y:$z"),
        ("value", 0.5),  # values change only through a review decision
    ],
)
def test_edit_parameter_refuses(conn, scratch_parameter, field, value):
    with pytest.raises(psycopg.errors.RaiseException):
        _edit(conn, scratch_parameter, field, value)
    conn.rollback()


def test_edit_parameter_refuses_an_unknown_parameter(conn):
    with pytest.raises(psycopg.errors.RaiseException, match="not in the parameter store"):
        _edit(conn, "euromod://FR/nope/def_const/$nope", "unit", "/1")
    conn.rollback()


def test_sql_unit_vocabulary_matches_known_units(conn):
    """edit_parameter hard-codes the vocabulary; it must not drift from KNOWN_UNITS."""
    source = conn.execute(
        "SELECT prosrc FROM pg_proc WHERE proname = 'edit_parameter'"
    ).fetchone()[0]
    for unit in paramdb.KNOWN_UNITS:
        assert f"'{unit}'" in source
    for source_type in SourceType:
        assert f"'{source_type.value}'" in source


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
