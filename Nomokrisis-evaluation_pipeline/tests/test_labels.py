"""Difficulty ladder, hazard flags, and the readiness split that gates them."""

from __future__ import annotations

from datetime import date

import pytest

from nomoscope_workflow.schema import Routing, TemporalBasis

from nomokrisis_eval.labels import draft_labels, instrument_of, is_formula
from nomokrisis_eval.runner import summarize
from nomokrisis_eval.schema import CaseResult, Expected, GoldenCase


def make_case(**kwargs) -> GoldenCase:
    expected = kwargs.pop("expected", None) or Expected(routing=Routing.UNCHANGED, value=1.0)
    return GoldenCase(
        id=kwargs.pop("id", "fr_case"),
        country="FR",
        language="fr",
        parameter_target="euromod://FR/x_fr/def_const/$x",
        as_of=date(2025, 6, 1),
        expected=expected,
        **kwargs,
    )


# --------------------------------------------------------------------------- #
# The ladder
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "value, citations, rung",
    [
        (4.1, ["CGI, art. 197"], "verbatim"),
        ("4.1%", ["CGI, art. 197"], "verbatim"),
        # A period suffix is a unit, not arithmetic: '#w' must not read as a
        # formula and promote a plain weekly rate to `derive`.
        ("109.50#w", ["SWCA 2005, Sch. 4"], "verbatim"),
        ("$PSS * 4", ["CSS, art. L241-3"], "derive"),
        (0.041, ["CGI, art. 197", "LOI 2025-127, art. 3"], "combine"),
        ([{"lower": 0, "rate": 0.11}], ["CGI, art. 197"], "table"),
    ],
)
def test_rungs(value, citations, rung):
    assert draft_labels(value=value, citations=citations).difficulty == rung


def test_two_pinpoints_into_one_instrument_is_not_combine():
    """`combine` means two documents to read, not two article numbers: two
    pinpoints into the same code is still one text in front of you."""
    drafted = draft_labels(value=1.0, citations=["CGI, art. 197", "CGI, art. 196 B"])
    assert drafted.difficulty == "verbatim"
    assert "cross_instrument" not in drafted.hazards


def test_table_outranks_a_formula_valued_bracket():
    """The rungs are ordered by work, and the highest applicable one wins."""
    drafted = draft_labels(value=1.0, citations=[], is_bracket_table=True)
    assert drafted.difficulty == "table"


def test_labels_never_read_a_run():
    """draft_labels takes ground truth only. A signature that could accept an
    outcome is how a difficulty ladder quietly becomes unfalsifiable."""
    import inspect

    assert set(inspect.signature(draft_labels).parameters) == {
        "value", "citations", "temporal_basis", "is_bracket_table",
    }


# --------------------------------------------------------------------------- #
# Hazards
# --------------------------------------------------------------------------- #


def test_income_year_hazard_is_orthogonal_to_the_rung():
    drafted = draft_labels(
        value=1.0, citations=["CGI, art. 197"], temporal_basis=TemporalBasis.INCOME_YEAR
    )
    assert drafted.difficulty == "verbatim"
    assert drafted.hazards == ["income_year"]


def test_dollar_reference_flags_cross_instrument():
    """`$PSS * 4` defers to a parameter another act fixes — the pointer-following
    failure the gap-fill scout exists for."""
    assert "cross_instrument" in draft_labels(value="$PSS * 4", citations=[]).hazards


def test_instrument_of_strips_the_pinpoint():
    assert instrument_of("CGI, art. 197") == instrument_of("CGI, Article 197 bis") == "cgi"
    assert instrument_of("WKB, artikel 2") == instrument_of("WKB, artikel 1") == "wkb"
    assert instrument_of("Ley IMV, Artículo 13") == "ley imv"


def test_is_formula_ignores_the_period_suffix():
    assert not is_formula("109.50#w")
    assert is_formula("$PSS * 4")


# --------------------------------------------------------------------------- #
# Readiness
# --------------------------------------------------------------------------- #


def test_readiness_states():
    ready = make_case(
        expected=Expected(routing=Routing.UNCHANGED, value=1.0, citations=["CGI, art. 197"]),
        corpus_available=True,
    )
    assert ready.readiness == "ready"

    undocumented = make_case(expected=Expected(routing=Routing.UNCHANGED, value=1.0))
    assert undocumented.readiness == "undocumented"

    # corpus-first: an uningested source is the stronger, positively established
    # fact, so it wins over "we never wrote down a citation".
    no_corpus = make_case(expected=Expected(routing=Routing.UNCHANGED, value=1.0),
                          corpus_available=False)
    assert no_corpus.readiness == "no_corpus"


def test_legacy_plain_label_still_loads():
    """Frozen cases.json files from earlier runs say `plain`; `rescore` has to
    keep reading them."""
    assert make_case(difficulty="plain").difficulty == "verbatim"


# --------------------------------------------------------------------------- #
# The report split
# --------------------------------------------------------------------------- #


def make_result(**kwargs) -> CaseResult:
    return CaseResult(
        case_id=kwargs.pop("case_id", "c"),
        country="FR",
        language="fr",
        routing_expected="unchanged",
        routing_actual="unchanged",
        **kwargs,
    )


def test_summarize_splits_ready_from_unready_and_breaks_down_only_the_ready():
    results = [
        make_result(case_id="a", readiness="ready", difficulty="verbatim",
                    routing_correct=True, hazards=["income_year"]),
        make_result(case_id="b", readiness="ready", difficulty="combine",
                    routing_correct=False),
        # Unready cases drag the headline down and must not land in any bucket:
        # they fail for a reason that has nothing to do with their rung.
        make_result(case_id="c", readiness="no_corpus", difficulty="verbatim",
                    routing_correct=False),
        make_result(case_id="d", readiness="undocumented", difficulty="verbatim",
                    routing_correct=False),
    ]
    table = summarize(results)

    assert table["fr"]["cases"] == "4"
    assert table["fr"]["routing_correct"] == "25%"
    assert table["fr"]["no_corpus"] == "1"
    assert table["fr"]["undocumented"] == "1"
    assert table["fr (ready)"]["cases"] == "2"
    assert table["fr (ready)"]["routing_correct"] == "50%"

    assert table["difficulty: verbatim"]["cases"] == "1"  # only the ready one
    assert table["difficulty: verbatim"]["routing_correct"] == "100%"
    assert table["difficulty: combine"]["cases"] == "1"
    assert table["hazard: income_year"]["cases"] == "1"


def test_summarize_falls_back_for_results_written_before_readiness_existed():
    """Old rows know corpus_available and nothing finer, so they take the coarser
    split rather than silently claiming to be ready."""
    results = [
        make_result(case_id="a", corpus_available=False, routing_correct=False),
        make_result(case_id="b", corpus_available=True, routing_correct=True),
    ]
    table = summarize(results)
    assert table["fr"]["no_corpus"] == "1"
    assert table["fr (ready)"]["cases"] == "1"
    assert table["fr (ready)"]["routing_correct"] == "100%"


def test_summarize_hides_a_lone_difficulty_bucket():
    """One rung compares with nothing; printing it just adds a row."""
    results = [make_result(case_id="a", readiness="ready", difficulty="verbatim",
                           routing_correct=True)]
    assert not any(k.startswith("difficulty:") for k in summarize(results))
