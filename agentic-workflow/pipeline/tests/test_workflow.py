"""DB-free unit tests: mock extraction, diff logic, queue round-trip."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from euromod_workflow import mock, queue_store
from euromod_workflow.pipeline import _current_value, _values_equal
from euromod_workflow.schema import (
    Bracket,
    ItemStatus,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    RetrievalHit,
    ReviewItem,
    Routing,
)

FR_TEXT = (
    "1. L'impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède "
    "11 497 € le taux de : 11 % pour la fraction supérieure à 11 497 € et inférieure ou égale à "
    "29 315 € ; 30 % pour la fraction supérieure à 29 315 € et inférieure ou égale à 83 823 € ; "
    "45 % pour la fraction supérieure à 180 294 €. 2. La réduction d'impôt est de 45,25 % de son montant."
)


def _hit(**kwargs) -> RetrievalHit:
    defaults = dict(
        chunk_id="c1",
        citation="CGI, art. 197",
        method="citation",
        score=1.0,
        validity="[2025-01-01,)",
        version_status="in_force",
        lang="fr",
        content=FR_TEXT,
    )
    return RetrievalHit(**{**defaults, **kwargs})


def _record(value_type: str, unit: str, value) -> ParameterRecord:
    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/test", value_type=value_type, unit=unit
        ),
        values=[ParameterValue(value=value, valid_from=date(2024, 1, 1))],
    )


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


def test_values_equal_and_current_value():
    a = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11294, rate=0.11)]
    b = [Bracket(threshold=0, rate=0.0), Bracket(threshold=11497, rate=0.11)]
    assert _values_equal(a, a.copy())
    assert not _values_equal(a, b)
    record = _record("scalar", "/1", 0.45)
    assert _current_value(record, date(2025, 6, 1)).value == 0.45
    assert _current_value(record, date(2023, 6, 1)) is None


def test_queue_roundtrip_preserves_reviewed_items(tmp_path: Path):
    record = _record("scalar", "/1", 0.45)
    item = ReviewItem(
        id="fr_test_2025-06-01",
        run_id="run-1",
        created_at="2026-07-09T00:00:00Z",
        country="FR",
        model_target="euromod://FR/test",
        as_of=date(2025, 6, 1),
        value_type="scalar",
        unit="/1",
        routing=Routing.UNCHANGED,
        proposed_record=record,
    )
    assert queue_store.write_item(item, tmp_path)
    loaded = queue_store.load_items(tmp_path)
    assert loaded[0].id == item.id

    # a decided item is not overwritten without force
    decided = item.model_copy(update={"status": ItemStatus.ACCEPTED})
    assert queue_store.write_item(decided, tmp_path, force=True)
    assert not queue_store.write_item(item, tmp_path)
    assert queue_store.write_item(item, tmp_path, force=True)
