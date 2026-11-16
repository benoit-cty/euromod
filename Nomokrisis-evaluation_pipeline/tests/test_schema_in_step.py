"""Python and db/eval_schema.sql name the same columns (dev DB for the SQL side)."""

from __future__ import annotations

from nomokrisis_eval.db import RESULT_COLUMNS
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
