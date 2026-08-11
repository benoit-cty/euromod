"""OpenFisca-drafted golden cases: the corpus-reading semantics that decide a case.

The DB round trip is covered by running the CLI; what is worth pinning here is
the reading convention, because getting it wrong produces a plausible-looking
case with the wrong year's value:

- OpenFisca stores change points, so "the value at D" is the latest entry at or
  before D — never an entry keyed exactly D;
- a band whose latest entry is null was abolished and must leave the schedule.
"""

from __future__ import annotations

from datetime import date

from nomokrisis_eval.openfisca_golden import _case_slug, schedule_at, value_at


class _Cursor:
    def __init__(self, rows):
        self._rows = rows

    def fetchone(self):
        return self._rows[0] if self._rows else None

    def fetchall(self):
        return self._rows


class FakeConn:
    """Just enough of psycopg to answer the two external_values queries."""

    def __init__(self, series: dict[str, list[tuple[date, float | None]]]):
        self.series = series

    def execute(self, sql, params=None):
        if "SELECT DISTINCT component" in sql:
            return _Cursor([(component,) for component in self.series])
        _, component, on = params
        points = [(v, f) for f, v in sorted(self.series[component]) if f <= on]
        return _Cursor([(points[-1][0], points[-1][1])] if points else [])


# The FR income-tax schedule as OpenFisca holds it: thresholds revalorised every
# year, rates restated only when they change, band 6 abolished in 2014.
BAREME = {
    "brackets[1].threshold": [(date(2014, 1, 1), 0.0)],
    "brackets[1].rate": [(date(2014, 1, 1), 0.0)],
    "brackets[2].threshold": [(date(2024, 1, 1), 11497.0), (date(2025, 1, 1), 11600.0)],
    "brackets[2].rate": [(date(2014, 1, 1), 0.14), (date(2020, 1, 1), 0.11)],
    "brackets[6].rate": [(date(2012, 1, 1), 0.45), (date(2014, 1, 1), None)],
    "brackets[6].threshold": [(date(2012, 1, 1), 500000.0), (date(2014, 1, 1), None)],
}


def test_value_at_takes_the_latest_change_point():
    conn = FakeConn(BAREME)
    # The rate was last restated in 2020 and still applies in 2025.
    assert value_at(conn, 1, "brackets[2].rate", date(2025, 1, 1)) == (0.11, date(2020, 1, 1))
    # Income year 2024 must not pick up the following finance act's threshold.
    assert value_at(conn, 1, "brackets[2].threshold", date(2024, 6, 30)) == (
        11497.0,
        date(2024, 1, 1),
    )
    assert value_at(conn, 1, "brackets[2].threshold", date(2025, 1, 1)) == (
        11600.0,
        date(2025, 1, 1),
    )


def test_value_at_before_the_first_change_point_is_undetermined():
    assert value_at(FakeConn(BAREME), 1, "brackets[2].threshold", date(2020, 1, 1)) == (None, None)


def test_schedule_at_drops_abolished_bands_and_dates_from_the_newest_component():
    schedule, source_date = schedule_at(FakeConn(BAREME), 1, date(2025, 1, 1))
    assert [(b.threshold, b.rate) for b in schedule] == [(0.0, 0.0), (11600.0, 0.11)]
    # The band abolished in 2014 is gone, not carried as a null-rate band.
    assert len(schedule) == 2
    # The schedule's effective date is the most recent component change.
    assert source_date == date(2025, 1, 1)


def test_case_slug_drops_the_country_and_function_noise():
    assert (
        _case_slug("euromod://FR/tinkt_fr/def_const/$tin_upthres1", "FR") == "tinkt_tin_upthres1"
    )
    assert _case_slug("euromod://FR/SetDefault_fr/def_const/$MinWage", "FR") == "setdefault_minwage"
