"""What EUROMOD holds, read from the params DB, in the form the eval compares.

Every part of the eval that sets an expectation against EUROMOD — the golden
drafters, the benchmark, the runner's scoring constants — needs the same four
things: the parameter under test (`load_case_record`), the value it holds on a
date (`current_value`, `comparable`), the `$`-constants a formula value refers
to (`db_constants`) and the deterministic routing of an expected value against
the held one (`route_against_current`). They live here, once.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date

import psycopg

from nomoscope_workflow import routing
from nomoscope_workflow import paramdb
from nomoscope_workflow.schema import ParameterRecord, ParameterValue, Routing

from .scoring import normalise_value, values_equal

#: `parameter_target` prefix of a bracket schedule assembled from
#: params.parameter_groups (`group:<group_id>`).
GROUP_PREFIX = "group:"


def load_case_record(conn: psycopg.Connection, parameter_target: str) -> ParameterRecord:
    """The parameter under test, from the params DB: `group:<group_id>` is a
    bracket schedule assembled from params.parameter_groups, anything else a
    model_target (or parameter_key) in params.parameters."""
    if parameter_target.startswith(GROUP_PREFIX):
        return paramdb.load_group_record(conn, parameter_target[len(GROUP_PREFIX):])
    return paramdb.load_record(conn, parameter_target)


def country_targets(conn: psycopg.Connection, country: str) -> list[str]:
    """Every parameter of a country in the params DB, in EUROMOD's spine order."""
    rows = conn.execute(
        "SELECT model_target FROM params.parameters WHERE country = %s ORDER BY spine_order, model_target",
        (country.upper(),),
    ).fetchall()
    return [row[0] for row in rows]


def current_value(record: ParameterRecord, as_of: date) -> ParameterValue | None:
    """The value row in force at `as_of`, if any — the workflow's own rule
    (routing.current_value), so the eval scores against what `diff` routed on."""
    return routing.current_value(record, as_of)


def comparable(value: ParameterValue | None):
    """The value as scoring compares it: the scalar/schedule, else the raw
    EUROMOD string ('140#m*$sw_weeks', '4.1%'), which formula and
    weighted-average rows keep in their lineage (they materialise as null)."""
    if value is None:
        return None
    if value.value is not None:
        return value.value
    return value.lineage.model_answer if value.lineage is not None else None


def db_constants(conn: psycopg.Connection, country: str, as_of: date) -> dict[str, object]:
    """$-constant resolution map for value normalisation, from the params DB.

    Every parameter of the country, keyed by casefolded constant name, valued
    by its value in force at as_of — the numeric scalar when the store has one,
    else the raw EUROMOD string (scoring.normalise_value evaluates those
    recursively, so '$csg_red_thres = $PSS * 4' resolves through '$PSS')."""
    rows = conn.execute(
        """
        SELECT p.model_target, v.value_numeric, v.raw_euromod_value
        FROM params.parameters p
        JOIN LATERAL (
            SELECT mv.value_numeric, mv.raw_euromod_value
            FROM params.model_values mv
            WHERE mv.parameter_id = p.id
              AND mv.valid_from <= %s
              AND (mv.valid_to IS NULL OR mv.valid_to >= %s)
            ORDER BY mv.valid_from DESC
            LIMIT 1
        ) v ON true
        WHERE p.country = %s
        """,
        (as_of, as_of, country),
    ).fetchall()
    constants: dict[str, object] = {}
    for model_target, numeric, raw in rows:
        name = model_target.rsplit("/", 1)[-1].lstrip("$").casefold()
        value = numeric if numeric is not None else raw
        if value is not None:
            constants[name] = value
    return constants


def route_against_current(
    current: ParameterValue | None,
    expected_value,
    constants: Mapping[str, object] | None = None,
) -> tuple[Routing, None] | tuple[None, str]:
    """Deterministic routing of a drafted value against the recorded one.

    Returns (routing, None), or (None, skip reason) when refusing to guess.
    Formula and weighted-average ("FYA") values are normalised first
    (scoring.normalise_value: arithmetic, $-references via `constants`, period
    suffixes); formula rows materialize with value null, so the raw string is
    read back from lineage.model_answer. Two situations still refuse to guess:
    a raw string normalisation cannot read, and a formula value that normalises
    but DIFFERS from the drafted point value — an FYA average never equals a
    point value even when EUROMOD is right by convention, so 'changed' would be
    a fabricated ground truth. Both route to the curation file, where an
    explicit `routing:` on the entry overrides."""
    if current is None:
        return Routing.NEW, None
    held = comparable(current)
    if held is None:
        return None, "has no scalar and no raw string"
    if isinstance(held, str) and normalise_value(held, constants) is None:
        return None, (
            f"cannot be normalised ({held!r}) "
            "— set an explicit `routing:` in the selection file to include it"
        )
    if values_equal(held, expected_value, constants):
        return Routing.UNCHANGED, None
    if isinstance(held, str):
        return None, (
            f"is a formula/weighted average ({held!r}) that differs from the "
            f"drafted point value ({expected_value!r}) — ambiguous by convention "
            "(FYA); set an explicit `routing:` in the selection file"
        )
    return Routing.CHANGED, None
