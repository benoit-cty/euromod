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

from nomoscope_workflow.schema import Lineage, ParameterValue, Routing, income_year_for

from nomokrisis_eval.openfisca_golden import (
    _case_slug,
    route_against_current,
    schedule_at,
    value_at,
)


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


def test_system_year_maps_to_the_previous_income_year():
    """The knob every FR income-tax expectation turns on.

    France assesses in year Y the income of year Y-1, so a golden case anchored
    on EUROMOD system year 2025 must read OpenFisca's income-year-2024 entry
    (11 497), not the 2025 one (11 600) that LF 2026 introduced. Getting this
    backwards produces a case that looks right and scores every correct
    proposal as wrong.
    """
    assert income_year_for(2025) == 2024
    conn = FakeConn(BAREME)
    target = date(income_year_for(2025), 1, 1)
    assert value_at(conn, 1, "brackets[2].threshold", target) == (11497.0, date(2024, 1, 1))


def _current(value, model_answer=None):
    return ParameterValue(
        value=value,
        valid_from=date(2025, 1, 1),
        lineage=Lineage(model_answer=model_answer) if model_answer else None,
    )


def test_routing_normalises_formula_values():
    """The drafter no longer skips every formula parameter (§ 'Still open').

    A derived value like '$csg_red_thres = $PSS * 4' routes deterministically
    once the reference resolves; formula rows materialize with value null, so
    the raw string is read back from lineage.model_answer.
    """
    constants = {"pss": 47100.0}
    current = _current(None, model_answer="$PSS * 4")
    assert route_against_current(current, 188400.0, constants) == (Routing.UNCHANGED, None)
    assert route_against_current(None, 188400.0, constants) == (Routing.NEW, None)
    assert route_against_current(_current(11496.0), 11497.0) == (Routing.CHANGED, None)


def test_routing_refuses_to_guess_on_ambiguous_formulas():
    # unknown $-reference: normalisation cannot read it
    routing, reason = route_against_current(_current(None, model_answer="$Mystery * 2"), 5.0)
    assert routing is None and "cannot be normalised" in reason

    # FYA average differing from the point value: 'changed' would be fabricated
    fya = _current(None, model_answer="(1766.92*10+1801.80*2)/12#m")
    assert route_against_current(fya, (1766.92 * 10 + 1801.80 * 2) / 12) == (
        Routing.UNCHANGED,
        None,
    )
    routing, reason = route_against_current(fya, 1801.80)
    assert routing is None and "ambiguous by convention" in reason

    routing, reason = route_against_current(_current(None), 5.0)
    assert routing is None and "no scalar and no raw string" in reason
