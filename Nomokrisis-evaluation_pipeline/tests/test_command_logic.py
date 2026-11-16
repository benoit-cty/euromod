"""Logic the CLI commands used to carry inline, now library functions."""

from __future__ import annotations

from datetime import date, datetime, timezone

from nomokrisis_eval import runner
from nomokrisis_eval.parameter_store import country_targets
from nomokrisis_eval.schema import RunManifest


class _Rows:
    def __init__(self, rows):
        self.rows = rows

    def fetchall(self):
        return self.rows


class _Conn:
    def __init__(self, rows):
        self.rows, self.params = rows, None

    def execute(self, sql, params=None):
        self.params = params
        return _Rows(self.rows)


def test_country_targets_reads_the_country_in_spine_order():
    conn = _Conn([("euromod://FR/a",), ("euromod://FR/b",)])
    assert country_targets(conn, "fr") == ["euromod://FR/a", "euromod://FR/b"]
    assert conn.params == ("FR",)


def _manifest(dataset_version: str, blind_before: date | None = None) -> RunManifest:
    return RunManifest(
        run_id="r", created_at=datetime.now(timezone.utc), as_of=date(2025, 7, 1),
        model="mock/extractor", model_provider="mock", model_name="extractor",
        prompt_version="p", agent_version="a", eval_version="e",
        dataset_version=dataset_version, blind_before=blind_before,
    )


def test_golden_set_drift(monkeypatch):
    monkeypatch.setattr(runner, "load_cases", lambda conn, verified_only: [])
    monkeypatch.setattr(runner, "golden_set_hash", lambda cases: "today")
    assert runner.golden_set_drift(None, _manifest("today")) is None
    assert runner.golden_set_drift(None, _manifest("frozen")) == "today"
    # A benchmark run's cases never came from the golden set.
    assert runner.golden_set_drift(None, _manifest("frozen", date(2025, 1, 1))) is None
