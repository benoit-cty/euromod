"""Scoring unit tests: KPI semantics on synthetic ReviewItems."""

from __future__ import annotations

from datetime import date, datetime, timezone

from nomoscope_workflow.schema import (
    Bracket,
    CritiqueReport,
    ParameterValue,
    Reference,
    RetrievalHit,
    ReviewItem,
    Routing,
)

from nomokrisis_eval.schema import Expected, GoldenCase
from nomokrisis_eval.scoring import (
    citation_matches,
    normalise_value,
    score_item,
    values_equal,
)


def make_case(**expected_kwargs) -> GoldenCase:
    return GoldenCase(
        id="fr_test_case",
        country="FR",
        language="fr",
        parameter_file="Nomoscope-agentic-workflow/data/parameters/eval/euromod_fr_tinkt_fr_def_const_tin_rate6.json",
        as_of=date(2025, 6, 1),
        expected=Expected(**expected_kwargs),
        verified=True,
    )


def make_item(
    routing: Routing = Routing.UNCHANGED,
    value=0.45,
    valid_from: date = date(2025, 1, 1),
    citation: str | None = "CGI, art. 197",
    citation_verified: bool = True,
    with_proposal: bool = True,
    trace_citation: str | None = "CGI, art. 197",
) -> ReviewItem:
    proposed = None
    if with_proposal:
        proposed = ParameterValue(
            value=value,
            valid_from=valid_from,
            references=[Reference(title=citation)] if citation else [],
        )
    return ReviewItem(
        id="fr_item",
        run_id="run",
        created_at=datetime.now(timezone.utc),
        country="FR",
        model_target="euromod://FR/tin_fr/def_const/$tinrt_top",
        as_of=date(2025, 6, 1),
        value_type="scalar",
        unit="/1",
        routing=routing,
        proposed_value=proposed,
        critique=CritiqueReport(citation_verified=citation_verified),
        retrieval_trace=(
            [RetrievalHit(chunk_id="c1", citation=trace_citation)] if trace_citation else []
        ),
    )


def test_all_correct_scalar():
    case = make_case(routing=Routing.UNCHANGED, value=0.45, valid_from=date(2025, 1, 1),
                     citations=["CGI, art. 197"])
    r = score_item(case, make_item())
    assert r.routing_correct and r.value_correct and r.date_correct
    assert r.citation_correct and r.supportedness and r.retrieval_hit
    assert not r.hallucination


def test_wrong_value_and_routing():
    case = make_case(routing=Routing.CHANGED, value=0.46, citations=["CGI, art. 197"])
    r = score_item(case, make_item(routing=Routing.UNCHANGED, value=0.45))
    assert r.routing_correct is False
    assert r.value_correct is False


def test_bracket_comparison():
    expected = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    proposed = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    assert values_equal(proposed, expected)
    assert not values_equal([Bracket(threshold=0, rate=0.0)], expected)
    assert not values_equal(
        [Bracket(threshold=0, rate=0.0), Bracket(threshold=11294, rate=0.11)], expected
    )


def test_unscored_kpis_are_none():
    case = make_case(routing=Routing.NOT_FOUND)  # no expected value/date/citations
    r = score_item(case, make_item(routing=Routing.NOT_FOUND, with_proposal=False))
    assert r.routing_correct is True
    assert r.value_correct is None and r.date_correct is None
    assert r.citation_correct is None and r.retrieval_hit is None
    assert r.supportedness is None and r.hallucination is False


def test_hallucination_flag():
    case = make_case(routing=Routing.UNCHANGED, value=0.45)
    r = score_item(case, make_item(citation_verified=False))
    assert r.hallucination is True
    assert r.supportedness is False


def test_missed_proposal_scores_false():
    case = make_case(routing=Routing.UNCHANGED, value=0.45, citations=["CGI, art. 197"])
    r = score_item(case, make_item(routing=Routing.NOT_FOUND, with_proposal=False,
                                   trace_citation=None))
    assert r.value_correct is False
    assert r.citation_correct is False
    assert r.retrieval_hit is False


def test_citation_normalisation():
    assert citation_matches("CGI, art. 197", "cgi art 197")
    assert citation_matches("CGI, art. 197", "Code général des impôts > CGI, art. 197 (vig. 2025)")
    assert not citation_matches("CGI, art. 197", "CGI, art. 200")
    assert not citation_matches("CGI, art. 197", None)


# ---------------------------------------------------------------------------
# Raw EUROMOD value normalisation (FR_parameter_matching.md §1.1–1.2)
# ---------------------------------------------------------------------------


def test_period_suffix_is_parsed_not_string_matched():
    assert values_equal(11496.0, "11496#y")
    assert values_equal("0.45", 0.45)
    # the FR 2025 barème erratum (1 € below the law) must stay a difference
    assert not values_equal(11497.0, "11496#y")


def test_fya_weighted_average_evaluates():
    # SMIC 2024: raised in November, stored as a weighted average that appears
    # in no legal text (the flagship example from the FR deep-dive)
    assert values_equal("(1766.92*10+1801.80*2)/12#m", (1766.92 * 10 + 1801.80 * 2) / 12)
    # DB rows sometimes carry a space before the suffix
    assert values_equal("(11.65*10 + 11.88*2)/12 #m", (11.65 * 10 + 11.88 * 2) / 12)
    assert not values_equal("(1766.92*10+1801.80*2)/12#m", 1801.80)


def test_constant_references_resolve():
    constants = {"pss": 47100.0}
    assert values_equal("$PSS * 4", 188400.0, constants)  # case-insensitive
    assert not values_equal("$PSS * 4", 188401.0, constants)
    # unknown constant -> unparseable -> strict fallback, never a false match
    assert not values_equal("$PSS * 4", 188400.0)


def test_constant_references_resolve_recursively():
    constants = {"a": "$b * 2", "b": "10#y"}  # a ref's own suffix is dropped
    assert values_equal("$a", 20.0, constants)
    # a circular reference must not recurse forever, and must not match
    assert not values_equal("$loop", 5.0, {"loop": "$loop"})


def test_cross_period_comparison_converts_to_monthly():
    assert values_equal("1801.8#m", "21621.6#y")
    assert values_equal("10#d", "305#m")
    assert not values_equal("1801.8#m", "1801.8#y")
    # a bare number carries the parameter's own storage basis: no conversion
    assert values_equal(1801.8, "1801.8#m")
    assert not values_equal(1801.8, "21621.6#y")


def test_unreadable_values_fall_back_to_strict_equality():
    assert values_equal("n/a", "n/a")
    assert not values_equal("n/a", 5.0)
    assert not values_equal("import os", 5.0)
    assert values_equal(True, True)
    assert not values_equal(True, False)


def test_normalise_value_shapes():
    assert normalise_value("47100#y").magnitude == 47100.0
    assert normalise_value("47100#y").period == "y"
    assert normalise_value(0.45).period is None
    assert normalise_value("n/a") is None
    assert normalise_value(None) is None
    assert normalise_value(True) is None


def test_runner_builds_constants_from_parameter_files(tmp_path):
    import json

    from nomokrisis_eval.runner import _scoring_constants

    def write(name, model_target, values):
        (tmp_path / name).write_text(
            json.dumps(
                {
                    "information": {"country": "FR", "model_target": model_target},
                    "values": values,
                }
            )
        )

    write(
        "pss.json",
        "euromod://FR/ConstDef_fr/def_const/$PSS",
        [
            {"value": 46368.0, "valid_from": "2024-01-01", "valid_to": "2024-12-31"},
            {"value": 47100.0, "valid_from": "2025-01-01", "valid_to": None},
        ],
    )
    write(
        "minwage.json",
        "euromod://FR/SetDefault_fr/def_const/$MinWage",
        [
            {
                # formula rows materialize with no scalar; raw stays in lineage
                "value": None,
                "valid_from": "2024-01-01",
                "valid_to": "2024-12-31",
                "lineage": {"model_answer": "(1766.92*10+1801.80*2)/12#m"},
            }
        ],
    )

    case = make_case(routing=Routing.UNCHANGED, value=1.0)
    case = case.model_copy(update={"parameter_file": str(tmp_path / "pss.json")})

    by_country = _scoring_constants([case], date(2025, 6, 1))
    assert by_country["FR"]["pss"] == 47100.0
    assert "minwage" not in by_country["FR"]  # no 2025 row -> nothing in force

    by_country = _scoring_constants([case], date(2024, 6, 1))
    assert by_country["FR"]["pss"] == 46368.0
    assert values_equal("$MinWage", 1772.7333333333333, by_country["FR"])


def test_score_item_uses_constants():
    case = make_case(routing=Routing.UNCHANGED, value="$PSS * 4")
    r = score_item(case, make_item(value=188400.0), constants={"pss": "47100#y"})
    assert r.value_correct is True
    r = score_item(case, make_item(value=188400.0))
    assert r.value_correct is False  # no constants map -> no fabricated match
