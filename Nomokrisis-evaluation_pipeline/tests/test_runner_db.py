"""A run lives in eval.runs / run_cases / results and resumes from them alone."""

from __future__ import annotations

from datetime import date, datetime, timezone

from nomoscope_workflow.schema import (
    Lineage,
    ParameterValue,
    ReviewItem,
    Routing,
)

from nomokrisis_eval import db as evaldb
from nomokrisis_eval import runner
from nomokrisis_eval.config import EvalConfig
from nomokrisis_eval.schema import CaseResult, Expected, GoldenCase

from conftest import TEST_PREFIX


def make_case(case_id: str, value: float = 47100.0) -> GoldenCase:
    return GoldenCase(
        id=case_id,
        country="FR",
        language="fr",
        parameter_target="euromod://FR/ConstDef_fr/def_const/$PSS",
        as_of=date(2025, 6, 1),
        expected=Expected(routing=Routing.UNCHANGED, value=value, citations=["JORFTEXT000050854392"]),
        verified=True,
    )


def fake_item(case: GoldenCase) -> ReviewItem:
    return ReviewItem(
        id=f"{TEST_PREFIX}item_{case.id}",
        run_id="fake",
        created_at=datetime.now(timezone.utc),
        country="FR",
        model_target=case.parameter_target,
        as_of=case.as_of,
        value_type="scalar",
        unit="currency",
        routing=Routing.UNCHANGED,
        proposed_value=ParameterValue(
            value=47100.0, valid_from=date(2025, 1, 1),
            lineage=Lineage(model_answer="47100", confidence=0.9),
        ),
    )


def _rename(manifest, db, new_id: str):
    """Give the run a zz_test_ id so conftest can sweep it."""
    db.execute("UPDATE eval.runs SET run_id = %s WHERE run_id = %s", (new_id, manifest.run_id))
    db.commit()
    manifest.run_id = new_id
    return manifest


def test_start_append_resume_from_the_tables(db, monkeypatch):
    cases = [make_case(TEST_PREFIX + "a"), make_case(TEST_PREFIX + "b")]
    cfg = EvalConfig(database_url="unused", phoenix_project="test")
    monkeypatch.setattr(runner, "_resolved_model_name", lambda model: None)

    manifest = runner.start_run(db, cfg, cases, date(2025, 6, 1), "mock/extractor", notes="t")
    manifest = _rename(manifest, db, TEST_PREFIX + manifest.run_id)
    assert manifest.status == "running"
    assert manifest.submitted_by == db.execute("SELECT current_user").fetchone()[0]
    assert manifest.dataset_version == runner.golden_set_hash(cases)

    run_pk, stored = evaldb.load_run(db, manifest.run_id)
    assert stored.model == "mock/extractor" and stored.status == "running"
    frozen = evaldb.load_run_cases(db, run_pk)
    assert [c.id for c in frozen] == [c.id for c in cases]

    # One case scored "by hand" (as execute_run does) — the run is now resumable.
    first = CaseResult(
        case_id=cases[0].id, country="FR", language="fr",
        routing_expected="unchanged", routing_actual="unchanged", routing_correct=True,
        value_correct=True, latency_ms=12,
    )
    evaldb.upsert_result(db, run_pk, first, fake_item(cases[0]).model_dump(mode="json"))
    evaldb.upsert_result(db, run_pk, first.model_copy(update={"latency_ms": 13}))  # idempotent
    resumed_manifest, resumed_cases, done = runner.resume_run(db, manifest.run_id)
    assert resumed_manifest.run_id == manifest.run_id
    assert [c.id for c in resumed_cases] == [c.id for c in cases]
    assert [r.case_id for r in done] == [cases[0].id] and done[0].latency_ms == 13
    assert set(evaldb.load_review_items(db, run_pk)) == {cases[0].id}  # kept through the second upsert

    listed = {r["run_id"]: r for r in runner.list_runs(db)}
    assert listed[manifest.run_id]["done"] == 1 and listed[manifest.run_id]["total"] == 2
    assert not listed[manifest.run_id]["complete"]
    assert runner.latest_incomplete_run(db)["run_id"] == manifest.run_id

    # Finish it through execute_run with a fake workflow: only the pending case runs.
    ran: list[str] = []

    def run_case(wf_cfg, tracer, record, case, as_of):
        ran.append(case.id)
        assert record.information.model_target == case.parameter_target
        return fake_item(case)

    monkeypatch.setattr(runner, "load_case_record", lambda conn, target: _fake_record(target))
    monkeypatch.setattr(runner, "_scoring_constants", lambda conn, cases, as_of: {})
    monkeypatch.setattr(runner, "setup_tracing", lambda wf_cfg: None)
    results = runner.execute_run(db, cfg, resumed_manifest, resumed_cases, done, run_case=run_case)
    assert ran == [cases[1].id]
    assert [r.case_id for r in results] == [c.id for c in cases]
    assert results[1].routing_correct and results[1].value_correct
    _, finished = evaldb.load_run(db, manifest.run_id)
    assert finished.status == "complete" and finished.finished_at is not None
    assert len(evaldb.load_results(db, run_pk)) == 2
    assert runner.latest_incomplete_run(db) is None or runner.latest_incomplete_run(db)["run_id"] != manifest.run_id

    # rescore reads the stored ReviewItems back, with measurements carried over.
    rescored_manifest, previous, rescored = runner.rescore_run(db, manifest.run_id)
    assert len(previous) == 2 and len(rescored) == 2
    assert rescored[0].latency_ms == 13 and rescored[1].value_correct


def _fake_record(target: str):
    from nomoscope_workflow.schema import ParameterInformation, ParameterRecord

    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target=target, value_type="scalar", unit="currency"
        ),
        values=[ParameterValue(value=47100.0, valid_from=date(2025, 1, 1))],
    )
