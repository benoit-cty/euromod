"""paramdb.blind_record: the record an analyst updating from the previous year holds."""

from datetime import date

from nomoscope_workflow.paramdb import blind_record
from nomoscope_workflow.pipeline import _current_value
from nomoscope_workflow.schema import ParameterInformation, ParameterRecord, ParameterValue


def make_record() -> ParameterRecord:
    return ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/bhotn_fr/def_const/$bho_r0_amt1",
            value_type="scalar", unit="currency", last_confirmed_valid_on=date(2025, 9, 1),
        ),
        values=[
            ParameterValue(value=4949.0, valid_from=date(2023, 1, 1), valid_to=date(2023, 12, 31)),
            ParameterValue(value=5186.0, valid_from=date(2024, 1, 1), valid_to=date(2024, 12, 31)),
            ParameterValue(value=5235.0, valid_from=date(2025, 1, 1), valid_to=date(2025, 12, 31)),
            ParameterValue(value=5300.0, valid_from=date(2026, 1, 1)),
        ],
    )


def test_hides_the_year_under_test_and_later():
    blind = blind_record(make_record(), date(2025, 1, 1))
    assert [v.value for v in blind.values] == [4949.0, 5186.0]
    assert blind.information.last_confirmed_valid_on is None


def test_reopens_the_last_row_so_it_is_current_on_the_reference_date():
    blind = blind_record(make_record(), date(2025, 1, 1))
    assert _current_value(blind, date(2025, 7, 1)).value == 5186.0


def test_a_series_closed_long_before_stays_closed():
    record = make_record()
    record.values = record.values[:1]  # ends 2023-12-31
    blind = blind_record(record, date(2025, 1, 1))
    assert blind.values[0].valid_to == date(2023, 12, 31)
    assert _current_value(blind, date(2025, 7, 1)) is None


def test_leaves_the_original_untouched():
    record = make_record()
    blind_record(record, date(2025, 1, 1))
    assert len(record.values) == 4 and record.values[1].valid_to == date(2024, 12, 31)
