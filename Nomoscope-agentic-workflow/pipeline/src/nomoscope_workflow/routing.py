"""Routing: what EUROMOD holds, value comparison, and the record after acceptance.

Pure functions of the parameter record (split out of pipeline.py, code audit
4): the value held on a date, the formula references of a derived parameter,
value equality (scalars and bracket schedules), the window an unchanged value
keeps, and the merged record an Accept would export.
"""

from __future__ import annotations

import math
import re
from datetime import date, timedelta

from .schema import Bracket, ParameterRecord, ParameterValue, ProposalDraft, Routing

def _values_equal(a, b) -> bool:
    """Compare parameter values (scalar/bool/str/brackets) with float tolerance."""
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return False
        return all(_values_equal_bracket(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b)) < 1e-9
    return a == b


def _values_equal_bracket(a: Bracket, b: Bracket) -> bool:
    def eq(x: float | None, y: float | None) -> bool:
        return (x is None) == (y is None) and (x is None or abs(x - y) < 1e-9)

    return eq(a.threshold, b.threshold) and eq(a.rate, b.rate) and eq(a.amount, b.amount)


_PARAM_REF = re.compile(r"\$[A-Za-z_]\w*")


def _derived_refs(record: ParameterRecord, current: ParameterValue | None) -> list[str]:
    """$references to other parameters in the current value / raw EUROMOD string.

    A value like `$PSS * 4` has no independent legislative existence: the
    anchor parameter is what legislation sets, so asking the corpus about the
    derived one is a guaranteed not_found.
    """
    if current is None:
        return []
    own = record.information.model_target.rsplit("/", 1)[-1]
    sources = [
        current.value if isinstance(current.value, str) else "",
        (current.lineage.model_answer or "") if current.lineage else "",
    ]
    refs = dict.fromkeys(m for s in sources for m in _PARAM_REF.findall(s))
    return [r for r in refs if r != own]


def _unchanged_window(proposed: ParameterValue, current: ParameterValue) -> ParameterValue:
    """The proposal rewritten to keep the validity window already in force.

    The value the law states is the one EUROMOD already holds, so the existing
    period simply continues: proposing a fresh valid_from (the model's date, or
    as_of) would read as a legislative change that did not happen. The citation
    re-confirms the value, it does not restart it — everything else about the
    proposal (evidence, legal_status, OJ date) is kept as proposed.
    """
    return proposed.model_copy(
        update={"valid_from": current.valid_from, "valid_to": current.valid_to}
    )


def _current_value(record: ParameterRecord, as_of: date) -> ParameterValue | None:
    """The value in force at as_of, if any."""
    for value in record.values:
        if value.valid_from <= as_of and (value.valid_to is None or value.valid_to >= as_of):
            return value
    return None


def _draft_value(draft: ProposalDraft):
    return draft.value_brackets if draft.value_brackets is not None else draft.value_scalar


def _confirms_held(draft: ProposalDraft, held: ParameterValue | None) -> bool:
    """Whether a scalar proposal is the value already held."""
    value = held.value if held is not None else None
    if draft.value_scalar is None or isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isclose(draft.value_scalar, float(value), rel_tol=1e-9, abs_tol=1e-12)


def _merge_record(
    record: ParameterRecord, proposed: ParameterValue, as_of: date, routing: Routing
) -> ParameterRecord:
    """The full record as it would look after acceptance (export-first write-back)."""
    merged = record.model_copy(deep=True)
    if routing == Routing.UNCHANGED:
        merged.information.last_confirmed_valid_on = as_of
        return merged
    for value in merged.values:
        if value.valid_to is None and value.valid_from < proposed.valid_from:
            value.valid_to = proposed.valid_from - timedelta(days=1)
    merged.values.append(proposed)
    merged.information.last_confirmed_valid_on = as_of
    return merged


# Public names for the other packages (the eval used the private ones).
current_value = _current_value
derived_refs = _derived_refs
values_equal = _values_equal
