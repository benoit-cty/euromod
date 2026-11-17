"""Value comparison, routing against the value held, and value parsing."""

from __future__ import annotations

from datetime import date

import pytest

from nomoscope_workflow import paramdb, values
from nomoscope_workflow.paramdb import record_value
from nomoscope_workflow.routing import (
    _confirms_held,
    _current_value,
    _derived_refs,
    _unchanged_window,
    _values_equal,
)
from nomoscope_workflow.schema import (
    Bracket,
    Lineage,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    ProposalDraft,
)

from workflow_fixtures import _record


def test_values_equal_and_current_value():
    a = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11294, rate=0.11)]
    b = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    assert _values_equal(a, a.copy())
    assert not _values_equal(a, b)
    record = _record("scalar", "/1", 0.45)
    assert _current_value(record, date(2025, 6, 1)).value == 0.45
    assert _current_value(record, date(2023, 6, 1)) is None


def test_unchanged_routing_keeps_the_current_validity_window():
    # same value as the one in force -> no new period starts, whatever date the
    # model read off the (re-confirming) legal text
    current = ParameterValue(value=0.45, valid_from=date(2024, 1, 1))
    proposed = ParameterValue(
        value=0.45, valid_from=date(2025, 1, 1), valid_to=date(2025, 12, 31)
    )
    kept = _unchanged_window(proposed, current)
    assert kept.valid_from == date(2024, 1, 1)
    assert kept.valid_to is None
    assert kept.value == 0.45


def test_derived_refs_detects_formula_parameters():
    record = ParameterRecord(
        information=ParameterInformation(
            country="FR",
            model_target="euromod://FR/tinty_fr/def_const/$csg_red_thres",
            value_type="scalar",
            unit="currency",
        ),
        values=[
            ParameterValue(
                value=185568.0,
                valid_from=date(2024, 1, 1),
                lineage=Lineage(model_answer="$PSS * 4"),
            )
        ],
    )
    current = _current_value(record, date(2025, 6, 1))
    assert _derived_refs(record, current) == ["$PSS"]

    # a plain numeric answer is not derived, and a self-reference does not count
    plain = record.model_copy(deep=True)
    plain.values[0].lineage.model_answer = "11496#y"
    assert _derived_refs(plain, _current_value(plain, date(2025, 6, 1))) == []
    self_ref = record.model_copy(deep=True)
    self_ref.values[0].lineage.model_answer = "$csg_red_thres"
    assert _derived_refs(self_ref, _current_value(self_ref, date(2025, 6, 1))) == []
    assert _derived_refs(record, None) == []


def test_record_value_prefers_the_ingested_scalar_for_percent_literals():
    """`8.17%` is null in the export's normalized value; the ingester read it."""
    assert record_value(None, 0.0817, "numeric") == 0.0817
    assert record_value(0.2, 0.2, "numeric") == 0.2
    assert record_value("$PSS * 4", None, "expression") == "$PSS * 4"
    assert record_value(None, None, "n_a") is None


def test_a_proposal_confirming_the_held_value_is_recognised():
    held = ParameterValue(value=0.07, valid_from=date(2024, 1, 1))
    assert _confirms_held(ProposalDraft(found=True, value_scalar=0.07), held)
    assert not _confirms_held(ProposalDraft(found=True, value_scalar=0.06), held)
    assert not _confirms_held(ProposalDraft(found=True, value_scalar=0.07), None)


def test_one_value_parser_reads_every_spelling():
    """paramdb, scoring and the derivation check share values.py (code audit 2.1)."""
    assert values.percent_literal("8,17%") == paramdb.percent_literal("8.17%") == 0.0817
    assert values.normalise_value("4,1%").magnitude == pytest.approx(0.041)
    assert values.normalise_value("100%*$MMS", {"mms": 1038}).magnitude == 1038
    assert values.normalise_value("$PSS * 4#y", {"pss": 47100}).period == "y"
