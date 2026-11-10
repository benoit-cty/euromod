"""A batch run skips parameters EUROMOD holds as n/a in the system year."""

from datetime import date

from nomoscope_workflow.paramdb import dormant_in_year
from nomoscope_workflow.schema import Lineage, ParameterInformation, ParameterRecord, ParameterValue


def _value(value, start, end, answer=None):
    return ParameterValue(
        value=value,
        valid_from=date.fromisoformat(start),
        valid_to=date.fromisoformat(end) if end else None,
        lineage=Lineage(model_answer=answer) if answer else None,
    )


def _record(*values):
    info = ParameterInformation(
        country="ES", model_target="euromod://ES/tscse_es/def_const/$x", value_type="scalar", unit="currency"
    )
    return ParameterRecord(information=info, values=list(values))


# ES $tscse_agebs2018_minamt1: n/a, valued in 2018 only, n/a from 2019 on.
AGEBS2018 = _record(
    _value(None, "2005-01-01", "2017-12-31", "n/a"),
    _value(932.7, "2018-01-01", "2018-12-31", "932.7#m"),
    _value(None, "2019-01-01", None, "n/a"),
)


def test_na_in_the_year_is_dormant():
    assert dormant_in_year(AGEBS2018, 2025)
    assert dormant_in_year(AGEBS2018, 2017)
    assert not dormant_in_year(AGEBS2018, 2018)


def test_history_ended_before_the_year_is_dormant():
    assert dormant_in_year(_record(_value(10.0, "2010-01-01", "2018-12-31")), 2025)


def test_revived_in_the_year_is_not_dormant():
    # n/a in Y-1, valued in Y (37 ES parameters in 2025): the run's year decides.
    rec = _record(_value(None, "2019-01-01", "2024-12-31", "n/a"), _value(0.05, "2025-01-01", None))
    assert not dormant_in_year(rec, 2025)


def test_expression_and_legacy_string_na():
    assert not dormant_in_year(_record(_value(None, "2020-01-01", None, "$PSS * 4")), 2025)
    assert dormant_in_year(_record(_value("n/a", "2020-01-01", None)), 2025)
