"""Benchmark: blind baseline routing, mid-year alternatives, OpenFisca arbitration, matrix."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow import paramdb
from nomoscope_workflow.schema import (
    Lineage,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    Routing,
    SourceType,
)

from nomokrisis_eval import benchmark
from nomokrisis_eval.schema import CaseResult, Expected, GoldenCase
from nomokrisis_eval.scoring import score_item

from test_scoring import make_item

AS_OF = date(2025, 7, 1)


def record(*rows: tuple, source_type: SourceType | None = None) -> ParameterRecord:
    """rows: (valid_from, valid_to, value, raw)."""
    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/bhotn_fr/def_const/$x",
            value_type="scalar", unit="currency",
        ),
        values=[
            ParameterValue(
                value=value, valid_from=start, valid_to=end, source_type=source_type,
                lineage=Lineage(model_answer=raw) if raw else None,
            )
            for start, end, value, raw in rows
        ],
    )


def routing_of(rec: ParameterRecord) -> Routing:
    blind = paramdb.blind_record(rec, date(2025, 1, 1))
    return benchmark.expected_routing(rec, blind, AS_OF, {})


def test_routing_against_previous_year():
    changed = record(
        (date(2024, 1, 1), date(2024, 12, 31), 5186.0, "5186#y"),
        (date(2025, 1, 1), None, 5235.0, "5235#y"),
    )
    kept = record((date(2013, 1, 1), None, 0.1, None))
    new = record((date(2025, 1, 1), None, 30.0, None))
    assert routing_of(changed) == Routing.CHANGED
    assert routing_of(kept) == Routing.UNCHANGED
    assert routing_of(new) == Routing.NEW


def test_routing_mirrors_the_pipeline_short_circuits():
    team = record((date(2024, 1, 1), None, 3.0, None), source_type=SourceType.NATIONAL_TEAM)
    formula = record(
        (date(2024, 1, 1), date(2024, 12, 31), None, "$PSS * 4"),
        (date(2025, 1, 1), None, None, "$PSS * 4"),
    )
    assert routing_of(team) == Routing.NATIONAL_TEAM_SOURCE
    assert routing_of(formula) == Routing.DERIVED


def test_na_baseline_is_a_change_not_a_confirmation():
    rec = record(
        (date(2024, 1, 1), date(2024, 12, 31), None, "n/a"),
        (date(2025, 1, 1), None, 12.0, None),
    )
    assert routing_of(rec) == Routing.CHANGED


def test_mid_year_component_on_the_reference_date():
    raw = "(59.87*9+60.59*3)/12#m"
    assert benchmark.mid_year_component(raw, date(2025, 7, 1)) == "59.87#m"
    assert benchmark.mid_year_component(raw, date(2025, 11, 1)) == "60.59#m"
    assert benchmark.mid_year_component("(1766.92*10+1801.80*2)/12", date(2025, 7, 1)) == 1766.92
    # not a full-year average: refuse rather than guess a component
    assert benchmark.mid_year_component("(10*6+20*3)/12", date(2025, 7, 1)) is None
    assert benchmark.mid_year_component("$PSS * 4", date(2025, 7, 1)) is None


def bench_case(value, accept=None, openfisca=None, routing=Routing.CHANGED) -> GoldenCase:
    return GoldenCase(
        id="bench:FR:2025:x", country="FR", language="fr",
        parameter_target="euromod://FR/bhotn_fr/def_const/$x", as_of=AS_OF,
        expected=Expected(
            routing=routing, value=value, accept=accept,
            openfisca={"value": openfisca} if openfisca is not None else None,
        ),
    )


def test_mid_year_point_value_scores_as_an_alternative():
    case = bench_case("(59.87*9+60.59*3)/12#m", accept=["59.87#m"])
    result = score_item(case, make_item(routing=Routing.CHANGED, value=59.87))
    assert result.value_correct and result.value_alternative
    result = score_item(case, make_item(routing=Routing.CHANGED, value=60.0))
    assert not result.value_correct and not result.value_alternative


def test_openfisca_arbitrates_a_disagreement():
    # EUROMOD 59.87, the workflow and OpenFisca 59.97
    case = bench_case(59.87, openfisca=59.97)
    result = score_item(case, make_item(routing=Routing.CHANGED, value=59.97))
    assert not result.value_correct
    assert result.openfisca_agrees and result.euromod_openfisca_agree is False
    assert benchmark.arbitration(result) == "OpenFisca sides with the workflow"


def test_rejected_proposal_loses_the_alternative_too():
    case = bench_case("(59.87*9+60.59*3)/12#m", accept=["59.87#m"])
    result = score_item(case, make_item(routing=Routing.CHANGED, value=59.87, verdict="fail"))
    assert result.rejected and not result.value_correct and not result.value_alternative


def result(routing_expected: str, **kwargs) -> CaseResult:
    return CaseResult(
        case_id="c", country="FR", language="fr", routing_expected=routing_expected,
        model_target="euromod://FR/bhotn_fr/def_const/$x", **kwargs,
    )


def test_matrix_cells():
    rows = [
        result("changed", proposed_value=1.0, value_correct=True, routing_actual="changed"),
        result("changed", proposed_value=1.0, value_correct=False, routing_actual="unchanged"),
        result("changed", proposed_value=1.0, value_correct=False, routing_actual="changed"),
        result("changed", routing_actual="not_found"),
        result("unchanged", proposed_value=1.0, value_correct=True, routing_actual="unchanged"),
        result("national_team_source", routing_actual="national_team_source", routing_correct=True),
    ]
    summary = benchmark.summarize_benchmark(rows)
    assert summary["matrix"]["changed"] == {
        "same value": 1, "kept Y-1 value": 1, "different value": 1, "not found": 1,
    }
    assert summary["matrix"]["kept"] == {"same value": 1}
    assert summary["not_legislative"] == {"routed as expected": 1}
    assert summary["headline"]["change recall"] == "25.0% (1/4)"
    assert summary["headline"]["coverage"] == "80.0% (4/5)"
    assert summary["by_policy"]["bhotn_fr"]["cases"] == 6


def test_policy_of_a_ref():
    assert benchmark._policy("euromod://FR/tco_fr/def_const/$tco_a_01222") == "tco_fr"
    assert benchmark._policy("group:FR:tinkt_fr:tin_schedule") == "tinkt_fr"


def test_euromod_off_the_law_is_its_own_column_and_success():
    rows = [
        result("changed", proposed_value=1.0, value_correct=True, routing_actual="changed"),
        result("changed", proposed_value=151.80, value_correct=False, routing_actual="changed",
               euromod_discrepancy="stated"),
        result("changed", proposed_value=1.0, value_correct=False, routing_actual="changed"),
    ]
    summary = benchmark.summarize_benchmark(rows)
    assert summary["matrix"]["changed"] == {
        "same value": 1, "EUROMOD off the law": 1, "different value": 1,
    }
    headline = summary["headline"]
    assert headline["correct (same value, or routed around as expected)"] == "33.3% (1/3)"
    assert headline["EUROMOD off the law (findings)"] == "1 (1 stated, 0 derived)"
    assert headline["success (correct + findings)"] == "66.7% (2/3)"
