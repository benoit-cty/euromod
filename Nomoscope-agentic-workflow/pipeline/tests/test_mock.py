"""The mock extractor: key-less, deterministic proposals for tests and demos."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow import mock
from nomoscope_workflow.schema import Bracket

from workflow_fixtures import FR_TEXT, _hit, _record


def test_mock_extracts_brackets_with_leading_zero_band():
    record = _record("bracket_schedule", "/1", [Bracket(threshold=0, rate=0.0)])
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit()])
    assert draft.found
    assert [b.threshold for b in draft.value_brackets] == [0, 11497, 29315, 180294]
    assert draft.value_brackets[1].rate == 0.11
    assert draft.valid_from == date(2025, 1, 1)
    assert draft.supporting_extract in FR_TEXT  # verbatim contract


def test_mock_scalar_uses_band_rates_not_incidental_percentages():
    record = _record("scalar", "/1", 0.45)
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit()])
    assert draft.found
    assert draft.value_scalar == 0.45  # not the 45,25 % réduction clause


def test_mock_ignores_hybrid_only_hits():
    record = _record("scalar", "/1", 0.2)
    draft = mock.propose_with_mock(record, date(2025, 6, 1), [_hit(method="hybrid")])
    assert not draft.found
