"""Country benchmark: every parameter of a country, updated blind from the year before.

The golden set measures the model on ~50 hand-picked cases. The benchmark asks
the question a EUROMOD country team asks each year: starting from system year
Y-1, does the workflow find what the law changed for Y? One case per parameter
(and per bracket schedule), drafted mechanically from the params DB:

  expected.value    EUROMOD's own value for system year Y
  expected.routing  changed / unchanged / new against EUROMOD Y-1 — mirroring
                    the pipeline's own short-circuits (national_team_source,
                    derived) so a correct run scores a correct routing
  expected.accept   for a mid-year change EUROMOD stores the weighted average
                    "(59.87*9+60.59*3)/12#m"; the law states the point value, so
                    the one in force on the reference date is accepted too
  expected.openfisca  the linked OpenFisca value for the same date, a second
                    ground truth reported beside EUROMOD, never instead of it

A benchmark run is a normal evaluation run (eval.runs / run_cases / results,
resumable, impact attached) with `blind_before` set to 1 January of Y: the
workflow never sees the Y row it is scored against (`paramdb.blind_record`).
Cases are not stored in eval.golden_cases — they are regenerated from the
params DB and frozen into eval.run_cases by the run that uses them.
"""

from __future__ import annotations

import random
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date

import psycopg

from nomoscope_workflow import paramdb, retrieval
from nomoscope_workflow.pipeline import _current_value, _derived_refs
from nomoscope_workflow.schema import (
    Bracket,
    ParameterRecord,
    ParameterValue,
    Routing,
    SourceType,
    TemporalBasis,
    income_year_for,
)

from .openfisca_golden import db_constants, external_parameter, schedule_at, value_at
from .runner import GROUP_PREFIX, load_case_record
from .schema import CaseResult, Expected, GoldenCase
from .scoring import normalise_value, values_equal

#: Same anchor as `nomoscope-workflow --year`: the reference date of a system year.
ANCHOR_MONTH_DAY = (7, 1)

CASE_PREFIX = "bench"

#: "(a*n1+b*n2+…)/12" with an optional period suffix: EUROMOD's full-year
#: average of in-year values, each held for n months, in calendar order.
_WEIGHTED = re.compile(r"^\(\s*(?P<terms>[^()]+)\)\s*/\s*12\s*(?:#\s*(?P<period>[a-z]))?$")
_TERM = re.compile(r"^\s*(?P<a>\d+(?:\.\d+)?)\s*\*\s*(?P<b>\d+(?:\.\d+)?)\s*$")


@dataclass
class BenchmarkBuild:
    cases: list[GoldenCase] = field(default_factory=list)
    skipped: dict[str, str] = field(default_factory=dict)


def anchor_date(year: int) -> date:
    return date(year, *ANCHOR_MONTH_DAY)


def case_id(country: str, year: int, target: str) -> str:
    return f"{CASE_PREFIX}:{country.upper()}:{year}:{target}"


def comparable(value: ParameterValue | None):
    """The value as scoring compares it: the scalar/schedule, else the raw
    EUROMOD string (formula and weighted-average rows materialise as null)."""
    if value is None:
        return None
    if value.value is not None:
        return value.value
    return value.lineage.model_answer if value.lineage is not None else None


def is_missing(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip().casefold() in ("n/a", "na", ""))


def mid_year_component(raw, on: date) -> str | float | None:
    """The point value a weighted average holds on `on`, or None.

    "(59.87*9+60.59*3)/12#m" on 1 July -> "59.87#m": the first term covers
    January-September. Terms are read as value*months (or months*value when the
    first factor is the one that fits a month count and the second does not).
    Anything that does not add up to twelve months is not a weighted average.
    """
    if not isinstance(raw, str):
        return None
    match = _WEIGHTED.match(raw.strip())
    if not match:
        return None
    terms: list[tuple[float, int]] = []
    for term in match.group("terms").split("+"):
        parsed = _TERM.match(term)
        if not parsed:
            return None
        a, b = float(parsed.group("a")), float(parsed.group("b"))
        if b.is_integer() and 1 <= b <= 12:
            terms.append((a, int(b)))
        elif a.is_integer() and 1 <= a <= 12:
            terms.append((b, int(a)))
        else:
            return None
    if sum(months for _, months in terms) != 12 or len(terms) < 2:
        return None
    elapsed = 0
    for value, months in terms:
        elapsed += months
        if on.month <= elapsed:
            period = match.group("period")
            return f"{value!r}#{period}" if period else value
    return None


def expected_routing(
    record: ParameterRecord,
    blind: ParameterRecord,
    as_of: date,
    constants: Mapping[str, object],
) -> Routing:
    """What a correct run on the blind record routes: the pipeline's own
    pre-retrieval short-circuits first, then the value against Y-1."""
    baseline = _current_value(blind, as_of)
    if baseline is not None and baseline.source_type == SourceType.NATIONAL_TEAM:
        return Routing.NATIONAL_TEAM_SOURCE
    if _derived_refs(blind, baseline):
        return Routing.DERIVED
    if baseline is None:
        return Routing.NEW
    before, now = comparable(baseline), comparable(_current_value(record, as_of))
    if not is_missing(before) and values_equal(before, now, constants):
        return Routing.UNCHANGED
    return Routing.CHANGED


def openfisca_reference(
    conn: psycopg.Connection, record: ParameterRecord, as_of: date
) -> dict | None:
    """The linked OpenFisca value on the date the case is about.

    One link per parameter: a human-validated one first, then the best score.
    The date follows the parameter's temporal_basis exactly as golden cases do
    (`income_year` -> 1 January of the income year), never the link's
    year_offset.
    """
    info = record.information
    row = conn.execute(
        """
        SELECT ep.path, pl.component, pl.factor, pl.validated_by IS NOT NULL, pl.match_method
        FROM params.parameter_links pl
        JOIN params.parameters p ON p.id = pl.parameter_id
        JOIN params.external_parameters ep ON ep.id = pl.external_parameter_id
        WHERE p.model_target = %s
        ORDER BY pl.validated_by IS NULL, pl.score DESC NULLS LAST, pl.id
        LIMIT 1
        """,
        (info.model_target,),
    ).fetchone()
    if row is None:
        return None
    path, component, factor, validated, method = row
    external = external_parameter(conn, info.country, path)
    if external is None:
        return None
    on = (
        date(income_year_for(as_of.year), 1, 1)
        if info.temporal_basis == TemporalBasis.INCOME_YEAR
        else as_of
    )
    if component == "brackets":
        schedule, source_date = schedule_at(conn, external["id"], on)
        value = [b.model_dump(exclude_none=True) for b in schedule] if schedule else None
    else:
        point, source_date = value_at(conn, external["id"], component, on)
        value = None if point is None else point * float(factor or 1)
    return {
        "path": path,
        "component": component,
        "factor": factor,
        "validated": validated,
        "match_method": method,
        "on": on.isoformat(),
        "source_date": source_date.isoformat() if source_date else None,
        "value": value,
    }


def build_case(
    conn: psycopg.Connection,
    ref: str,
    year: int,
    constants: Mapping[str, object],
) -> GoldenCase:
    """One benchmark case, or ValueError with the reason it cannot be one."""
    record = load_case_record(conn, ref)
    info = record.information
    as_of = anchor_date(year)
    blind = paramdb.blind_record(record, date(year, 1, 1))
    target = comparable(_current_value(record, as_of))
    if is_missing(target):
        raise ValueError(f"no EUROMOD value in force on {as_of}")

    routing = expected_routing(record, blind, as_of, constants)
    # A national-team or formula parameter has no legislated value to find:
    # the pipeline routes it before retrieval and proposes nothing, so only
    # the routing is scored.
    scored = routing not in (Routing.NATIONAL_TEAM_SOURCE, Routing.DERIVED)
    component = mid_year_component(target, as_of)
    hazards = []
    if info.temporal_basis == TemporalBasis.INCOME_YEAR:
        hazards.append("income_year")
    if component is not None:
        hazards.append("mid_year_change")

    expected = Expected(
        routing=routing,
        value=target if scored else None,
        accept=[component] if scored and component is not None else None,
        openfisca=openfisca_reference(conn, record, as_of) if scored else None,
    )
    if isinstance(target, list) and target and not isinstance(target[0], Bracket):
        raise ValueError("unreadable bracket schedule")
    if scored and isinstance(target, str) and normalise_value(target, constants) is None:
        raise ValueError(f"EUROMOD value cannot be normalised ({target!r})")
    return GoldenCase(
        id=case_id(info.country, year, ref),
        country=info.country,
        language=retrieval.LANG_BY_COUNTRY.get(info.country, "en"),
        parameter_target=ref,
        as_of=as_of,
        hazards=hazards,
        expected=expected,
        drafted_by="euromod",
        notes=f"benchmark: EUROMOD {year - 1} -> {year}",
    )


def build_cases(
    conn: psycopg.Connection,
    country: str,
    year: int,
    *,
    sample: int | None = None,
    seed: int | None = None,
    exclude_policies: list[str] | None = None,
    targets: list[str] | None = None,
) -> BenchmarkBuild:
    """Benchmark cases for a country and system year.

    `targets` restricts to explicit refs (model_targets or `group:<id>`);
    `exclude_policies` drops whole EUROMOD policies (`tco_fr`, VAT) — matched
    on the policy segment of the target; `sample` draws that many cases at
    random after skipping, reproducibly when `seed` is given.
    """
    country = country.upper()
    refs = targets or (
        paramdb.country_targets(conn, country)
        + [f"{GROUP_PREFIX}{g}" for g in paramdb.country_groups(conn, country)]
    )
    excluded = {p.casefold() for p in exclude_policies or []}
    constants = db_constants(conn, country, anchor_date(year))
    # A schedule is scored once, as its group: its member constants would
    # count every barème threshold twice.
    grouped = {} if targets else group_members(conn, country)
    build = BenchmarkBuild()
    for ref in refs:
        if excluded and _policy(ref) in excluded:
            continue
        if ref in grouped:
            build.skipped[ref] = "scored as part of its bracket schedule"
            continue
        try:
            build.cases.append(build_case(conn, ref, year, constants))
        except (KeyError, ValueError) as exc:
            conn.rollback()
            build.skipped[ref] = str(exc)
    if sample is not None and sample < len(build.cases):
        build.cases = sorted(random.Random(seed).sample(build.cases, sample), key=lambda c: c.id)
    return build


def group_members(conn: psycopg.Connection, country: str) -> dict[str, str]:
    """model_target -> `group:<id>` for every member of a bracket schedule."""
    rows = conn.execute(
        """
        SELECT p.model_target, g.group_id
        FROM params.parameter_groups g
        CROSS JOIN LATERAL jsonb_array_elements(g.components) c
        JOIN params.parameters p
          ON p.parameter_key = c ->> 'parameter_id' OR p.model_target = c ->> 'parameter_id'
        WHERE g.country = %s AND g.kind = 'bracket_schedule'
        """,
        (country.upper(),),
    ).fetchall()
    return {target: f"{GROUP_PREFIX}{group_id}" for target, group_id in rows}


def _policy(ref: str) -> str:
    """'euromod://FR/tco_fr/def_const/$x' -> 'tco_fr'; 'group:FR:tinkt_fr:…' -> 'tinkt_fr'."""
    if ref.startswith(GROUP_PREFIX):
        parts = ref[len(GROUP_PREFIX):].split(":")
        return parts[1].casefold() if len(parts) > 1 else ""
    parts = ref.split("/")
    return parts[3].casefold() if len(parts) > 3 else ""


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #

#: What EUROMOD did between Y-1 and Y (the rows of the matrix).
EUROMOD_CHANGED, EUROMOD_KEPT, NOT_LEGISLATIVE = "changed", "kept", "not_legislative"

#: What the workflow answered (the columns).
OUTCOMES = ("same value", "different value", "kept Y-1 value", "not found", "rejected", "error")


def euromod_side(result: CaseResult) -> str:
    if result.routing_expected in (Routing.CHANGED, Routing.NEW):
        return EUROMOD_CHANGED
    if result.routing_expected == Routing.UNCHANGED:
        return EUROMOD_KEPT
    return NOT_LEGISLATIVE


def outcome(result: CaseResult) -> str:
    """The workflow's answer, in the matrix's terms.

    `kept Y-1 value` is a routing of unchanged whose value is not EUROMOD's Y
    value: on a parameter EUROMOD changed, the missed change.
    """
    if result.error:
        return "error"
    if result.rejected:
        return "rejected"
    if result.proposed_value is None:
        return "not found"
    if result.value_correct:
        return "same value"
    if result.routing_actual == Routing.UNCHANGED:
        return "kept Y-1 value"
    return "different value"


def arbitration(result: CaseResult) -> str | None:
    """Who OpenFisca sides with when the workflow and EUROMOD disagree."""
    if outcome(result) not in ("different value", "kept Y-1 value"):
        return None
    if result.openfisca_value is None:
        return "no OpenFisca value"
    if result.openfisca_agrees and not result.euromod_openfisca_agree:
        return "OpenFisca sides with the workflow"
    if result.euromod_openfisca_agree and not result.openfisca_agrees:
        return "OpenFisca sides with EUROMOD"
    return "OpenFisca agrees with neither"


def _pct(numerator: int, denominator: int) -> str:
    return f"{100 * numerator / denominator:.1f}% ({numerator}/{denominator})" if denominator else "-"


def summarize_benchmark(results: list[CaseResult]) -> dict:
    """The matrix, the headline rates and the per-policy breakdown of a run."""
    matrix: dict[str, Counter] = {side: Counter() for side in (EUROMOD_CHANGED, EUROMOD_KEPT)}
    not_legislative = Counter()
    arbitrations = Counter()
    by_policy: dict[str, Counter] = {}
    for result in results:
        side = euromod_side(result)
        # An error result has no model_target; the case id ends with the ref.
        policy = _policy(result.model_target or result.case_id.split(":", 3)[-1]) or "?"
        counts = by_policy.setdefault(policy, Counter())
        counts["cases"] += 1
        if side == NOT_LEGISLATIVE:
            not_legislative[
                "routed as expected" if result.routing_correct else f"routed {result.routing_actual}"
            ] += 1
            counts["not legislative"] += 1
            continue
        answer = outcome(result)
        matrix[side][answer] += 1
        counts[answer] += 1
        if (who := arbitration(result)) is not None:
            arbitrations[who] += 1

    changed, kept = matrix[EUROMOD_CHANGED], matrix[EUROMOD_KEPT]
    scored = [r for r in results if euromod_side(r) != NOT_LEGISLATIVE]
    answered = [r for r in scored if outcome(r) in ("same value", "different value", "kept Y-1 value")]
    mid_year = [r for r in scored if "mid_year_change" in r.hazards]
    with_openfisca = [r for r in scored if r.openfisca_value is not None]
    headline = {
        "parameters": len(results),
        "legislative": len(scored),
        "coverage": _pct(len(answered), len(scored)),
        "change recall": _pct(changed["same value"], sum(changed.values())),
        "precision": _pct(sum(1 for r in answered if r.value_correct), len(answered)),
        "unchanged confirmed": _pct(kept["same value"], sum(kept.values())),
        "mid-year accepted on the point value": sum(1 for r in mid_year if r.value_alternative),
        "EUROMOD = OpenFisca": _pct(
            sum(1 for r in with_openfisca if r.euromod_openfisca_agree), len(with_openfisca)
        ),
    }
    return {
        "headline": headline,
        "matrix": {side: dict(counts) for side, counts in matrix.items()},
        "not_legislative": dict(not_legislative),
        "arbitration": dict(arbitrations),
        "by_policy": {policy: dict(counts) for policy, counts in sorted(by_policy.items())},
    }
