"""Python and db/eval_schema.sql name the same columns (dev DB for the SQL side)."""

from __future__ import annotations

from nomokrisis_eval.db import RESULT_COLUMNS, SCHEMA_SQL
from nomokrisis_eval.schema import CaseResult


def _columns(db, table: str) -> set[str]:
    schema, name = table.split(".")
    return {
        row[0]
        for row in db.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema = %s AND table_name = %s",
            (schema, name),
        ).fetchall()
    }


def test_every_projected_result_column_is_a_case_result_field():
    assert set(RESULT_COLUMNS) <= set(CaseResult.model_fields)
    assert len(set(RESULT_COLUMNS)) == len(RESULT_COLUMNS)


def test_every_projected_result_column_exists_in_eval_results(db):
    assert set(RESULT_COLUMNS) | {"run_pk", "details", "review_item"} <= _columns(db, "eval.results")


def _applied_schema(db):
    """db/eval_schema.sql as it is in this checkout, applied inside the test's
    transaction (the fixture rolls it back): the views under test are the
    file's, not whatever the dev DB was last initialised with."""
    db.execute(SCHEMA_SQL.read_text(encoding="utf-8"))


def test_the_python_and_sql_kpi_summaries_name_the_same_kpis(db):
    from nomokrisis_eval.summary import COUNT_COLUMNS, KPIS, RATE_COLUMNS, SQL_ONLY_COLUMNS, summarize

    # Python side: every KPI and every count summarize() prints is mapped.
    assert list(RATE_COLUMNS) == KPIS
    row = summarize([CaseResult(case_id="c", country="FR", language="fr", routing_expected="unchanged")])["fr"]
    assert set(row) == set(KPIS) | set(COUNT_COLUMNS)

    # SQL side: run_summary has exactly the mapped columns plus its declared extras.
    _applied_schema(db)
    view = _columns(db, "eval.run_summary")
    mapped = set(RATE_COLUMNS.values()) | set(COUNT_COLUMNS.values())
    assert mapped <= view, f"missing from eval.run_summary: {sorted(mapped - view)}"
    assert view - mapped == SQL_ONLY_COLUMNS, (
        f"in the view only, undeclared: {sorted(view - mapped - SQL_ONLY_COLUMNS)}; "
        f"declared but gone: {sorted(SQL_ONLY_COLUMNS - (view - mapped))}"
    )


def test_findings_and_fts_only_cases_are_counted_by_both_summaries(db, monkeypatch):
    """euromod_discrepancy and vector_leg live only in `details`; the view reads them there."""
    from datetime import date, datetime, timezone

    from nomokrisis_eval import db as evaldb
    from nomokrisis_eval.schema import RunManifest
    from nomokrisis_eval.summary import summarize

    from conftest import TEST_PREFIX

    _applied_schema(db)
    manifest = RunManifest(
        run_id=TEST_PREFIX + "kpi_step", created_at=datetime.now(timezone.utc), as_of=date(2025, 7, 1),
        model="mock/extractor", model_provider="mock", model_name="extractor",
        prompt_version="p", agent_version="a", eval_version="e", dataset_version="d",
    )
    # insert_run/upsert_result commit; keep everything in the test transaction.
    monkeypatch.setattr(db, "commit", lambda: None)
    run_pk = evaldb.insert_run(db, manifest)
    results = [
        CaseResult(case_id="a", country="FR", language="fr", routing_expected="unchanged",
                   value_correct=False, euromod_discrepancy="stated", vector_leg=False),
        CaseResult(case_id="b", country="FR", language="fr", routing_expected="unchanged",
                   value_correct=True, vector_leg=True),
    ]
    for result in results:
        evaldb.upsert_result(db, run_pk, result)
    sql = db.execute(
        "SELECT euromod_discrepancies, fts_only_cases FROM eval.run_summary WHERE run_pk = %s", (run_pk,)
    ).fetchone()
    python = summarize(results)["fr"]
    assert sql == (1, 1)
    assert (python["euromod_off_law"], python["fts_only"]) == ("1", "1")
