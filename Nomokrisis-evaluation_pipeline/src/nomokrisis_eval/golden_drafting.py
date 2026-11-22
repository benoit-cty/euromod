"""What every golden-case drafter shares, whatever its source of ground truth.

Three drafters write rows into eval.golden_cases — `openfisca_golden` (ground
truth read from the OpenFisca corpus), `curated_golden` (ground truth written
by hand into a `curated` selection) and `build_dataset` (an LLM reading a
trusted document). They differ in where the expected value comes from; the
rest is here, once:

- the case id, which a rebuild must reproduce exactly — a drifted id leaves the
  previous draft behind as a stale row (`golden_case_id`, `entry_case_id`);
- the parameter under test, always from the params DB (`load_record`);
- the selection entry's own word on `corpus_available`, labels and source
  class, and the GoldenCase built from them (`resolve_corpus_available`,
  `golden_case`);
- writing the draft and saying when its ground truth moved under a verdict
  (`save_outcome`), and retiring the draft of an entry that stopped drafting
  (`retire_skipped`).

The two selection-driven drafters (`openfisca_golden`, `curated_golden`) use
all of it; the LLM drafter only the id rule.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import psycopg
from nomoscope_workflow import paramdb
from nomoscope_workflow.queue_store import slugify
from nomoscope_workflow.schema import ParameterRecord

from .golden_store import delete_case, load_case, save_drafted_case
from .labels import draft_labels
from .parameter_store import GROUP_PREFIX
from .schema import Expected, GoldenCase


@dataclass
class DraftOutcome:
    """One selection entry's result: a case, or the reason it produced none."""

    entry: dict
    case: GoldenCase | None = None
    skipped: str | None = None
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Case ids
# ---------------------------------------------------------------------------


def case_slug(model_target: str, country: str) -> str:
    """euromod://FR/tinkt_fr/def_const/$tin_upthres1 -> 'tinkt_tin_upthres1'.

    The country prefixes the case id already and `def_const` is the only
    function in the export, so both are noise in a case id.
    """
    parts = paramdb.parse_model_target(model_target)
    policy = (parts["policy"] or "").removesuffix(f"_{country.lower()}")
    name = (parts["name"] or model_target).lstrip("$")
    return slugify(f"{policy}_{name}") if policy else slugify(name)


def golden_case_id(country: str, as_of: date, target: str, slug: str | None = None) -> str:
    """The id of the golden case for one parameter on one date — the one rule.

    `target` is what the case tests: a `euromod://…` model target, or a bracket
    schedule's group id (bare or as `group:<group_id>`). `slug`, when the
    selection entry states one (`id`), wins. A group is slugged from its group
    id, never from the `euromod://<cc>/<policy>/group/<name>` target its
    assembled record carries: the id must be computable from the selection
    entry alone, before (or without) loading the record, or a draft that stops
    building could never be found again to be retired.
    """
    if not slug:
        bare = target.removeprefix(GROUP_PREFIX)
        slug = case_slug(bare, country) if bare.startswith("euromod://") else slugify(bare)
    return f"{country.lower()}_{slug}_{as_of.isoformat()}"


def entry_case_id(entry: dict, as_of: date, country: str) -> str | None:
    """The id a selection entry's case carries (or would carry), from the entry alone.

    None for an entry that names no parameter at all.
    """
    target = entry.get("group_id") or entry.get("model_target")
    if not target:
        return None
    if entry.get("group_id"):
        target = f"{GROUP_PREFIX}{target}"
    return golden_case_id(country, as_of, target, entry.get("id"))


# ---------------------------------------------------------------------------
# Drafting one case
# ---------------------------------------------------------------------------


def load_record(conn: psycopg.Connection, entry: dict) -> tuple[ParameterRecord, str]:
    """The parameter a selection entry names, plus the `parameter_target` the
    runner hands to the workflow.

    **Everything comes from the parameter store**, so a golden case never
    depends on a loose file whose provenance nobody can trace:

    - `group_id` — a bracket schedule assembled from `params.parameter_groups`
      (the FR barème is 4 thresholds + 5 rates; the export's groups block is the
      only place it exists as an object) → target `group:<group_id>`.
    - `model_target` — a single parameter from `params.parameters`. Parameters
      EUROMOD defines inside functions rather than as named constants (CDHR)
      reach the store through `extracted_parameters/curated/<CC>.in_function.json`
      like any other ingest, not through a file read at run time.
    """
    if entry.get("group_id"):
        record = paramdb.load_group_record(conn, entry["group_id"])
        return record, f"{GROUP_PREFIX}{entry['group_id']}"
    record = paramdb.load_record(conn, entry["model_target"])
    return record, record.information.model_target


def resolve_corpus_available(entry: dict, derived: bool | None = None) -> bool | None:
    """`corpus_available` for an entry's case: the selection's explicit value
    when it states one (it knows more than any reference list), else what the
    drafter derived (None = never established)."""
    return entry.get("corpus_available", derived)


def golden_case(
    entry: dict,
    record: ParameterRecord,
    parameter_target: str,
    as_of: date,
    country: str,
    language: str,
    expected: Expected,
    *,
    corpus_available: bool | None,
    drafted_by: str,
    notes: list[str],
    is_bracket_table: bool,
) -> GoldenCase:
    """The unverified GoldenCase for one selection entry.

    Labels are drafted from the ground truth and overridable per entry: a
    reviewer who disagrees writes `difficulty`/`hazards` into the selection,
    and the draft never overwrites it.
    """
    drafted = draft_labels(
        value=expected.value,
        citations=list(expected.citations),
        temporal_basis=record.information.temporal_basis,
        is_bracket_table=is_bracket_table,
    )
    return GoldenCase(
        id=golden_case_id(country, as_of, parameter_target, entry.get("id")),
        country=country.upper(),
        language=language,
        parameter_target=parameter_target,
        as_of=as_of,
        difficulty=entry.get("difficulty") or drafted.difficulty,
        hazards=entry.get("hazards", drafted.hazards),
        labels_drafted="difficulty" not in entry and "hazards" not in entry,
        source_class=entry.get("source_class", "codified_law"),
        expected=expected,
        corpus_available=corpus_available,
        verified=False,
        drafted_by=drafted_by,
        notes=" | ".join(notes),
    )


# ---------------------------------------------------------------------------
# Writing the drafts
# ---------------------------------------------------------------------------


def save_outcome(conn: psycopg.Connection, outcome: DraftOutcome) -> bool:
    """Upsert the outcome's case into eval.golden_cases; False when it has none.

    A rebuild whose ground truth differs from the reviewed one resets the
    verdict (golden_store.save_drafted_case); the outcome says so.
    """
    if outcome.case is None:
        return False
    if save_drafted_case(conn, outcome.case):
        outcome.warnings.append(
            "ground truth changed since it was reviewed — the case is back to "
            "verified:false and must be re-verified before it counts"
        )
    return True


def retire_skipped(conn: psycopg.Connection, outcomes: list[DraftOutcome], as_of: date, country: str) -> None:
    """Delete the case row of an entry that stopped drafting this run.

    An entry can stop producing a case because the world changed under it — the
    CDHR has no value in the income year the system year now maps to. Leaving
    the previous run's row in place would keep a case in the golden set that
    the current rules no longer generate, and the count would still read 50.
    A reviewed case is never removed: a human verdict outranks a rebuild, and
    the mismatch is worth seeing rather than silently erasing.
    """
    for outcome in outcomes:
        if outcome.case is not None or not outcome.skipped:
            continue
        case_id = entry_case_id(outcome.entry, as_of, country)
        if case_id is None:
            continue
        existing = load_case(conn, case_id)
        if existing is None:
            continue
        if existing.reviewed_by:
            outcome.warnings.append(
                f"reviewed case {case_id} kept although the entry no longer drafts "
                f"({outcome.skipped}) — re-verify or delete it by hand"
            )
            continue
        delete_case(conn, case_id)
        outcome.warnings.append(f"removed stale draft {case_id} ({outcome.skipped})")
