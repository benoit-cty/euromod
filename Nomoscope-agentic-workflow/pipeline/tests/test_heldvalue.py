"""The held-figure patterns (no database): what a legal text may write for a number."""

import re
from datetime import date

from nomoscope_workflow.heldvalue import _figure_pattern, held_figures
from nomoscope_workflow.schema import Bracket, ParameterValue


def _states(number: float, text: str) -> bool:
    return re.search(_figure_pattern(number), text) is not None


def test_an_amount_is_found_however_it_is_grouped():
    for text in ("of “€44,000” for “€42,000”", "42 000 euros", "42.000 €", "42000", "€42,000.00"):
        assert _states(42000, text), text


def test_a_figure_is_never_part_of_a_longer_number():
    assert not _states(801.8, "1 801,80 €")
    assert not _states(42000, "142,000")
    assert not _states(42000, "42,000.50")
    assert not _states(181.7, "181.75")


def test_decimals_are_written_with_a_dot_or_a_comma():
    assert _states(181.7, "“€191.10” for “€181.70”")
    assert _states(181.7, "181,7 EUR")
    assert _states(646.52, "fixé à 646,52 euros.")


def test_a_short_figure_is_not_searched():
    assert _figure_pattern(20) is None and _figure_pattern(1.5) is None
    assert _figure_pattern(0) is None and _figure_pattern(225) is not None


def test_a_rate_is_searched_in_percent_and_a_schedule_by_each_figure():
    value = ParameterValue(value=0.1105, valid_from=date(2024, 1, 1))
    (pattern,) = held_figures(value, "/1")
    assert re.search(pattern, "11.05 per cent")
    schedule = ParameterValue(
        value=[Bracket(threshold=0, rate=0.088), Bracket(threshold=441, rate=0.1105)],
        valid_from=date(2024, 1, 1),
    )
    patterns = held_figures(schedule, "/1")
    assert len(patterns) == 2  # 441 and 11.05; 0 and 8.8 are too short
    assert held_figures(ParameterValue(value="$PSS*4", valid_from=date(2024, 1, 1)), "currency") == []
    assert len(held_figures(ParameterValue(value="8964#y", valid_from=date(2024, 1, 1)), "currency")) == 1
