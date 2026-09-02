"""Draft golden cases from a hand-curated selection file — countries with no external corpus.

The sibling drafter (`openfisca_golden`) reads ground truth out of the ingested
OpenFisca corpus. Ireland and Lithuania have no OpenFisca package, so their
ground truth is hand-curated from the acts themselves and written down in
`golden_sources/<cc>.json` (`"corpus": "curated"`): each entry names the
parameter, the value the LAW states, and the routing a correct pipeline owes.

What this module adds over hand-writing the case files is everything that must
NOT be typed by hand:

- the parameter under test is loaded from the params DB and materialized under
  `data/parameters/eval/` (`openfisca_golden._load_record`), so no case points
  at a hand-authored parameter file;
- the value EUROMOD holds at `as_of` is read back into the case notes, which is
  what a reviewer needs in front of them at the verification gate;
- the selection's explicit `routing:` is cross-checked against the deterministic
  routing (`route_against_current`), and a disagreement SKIPS the entry rather
  than writing ground truth the drafter believes is wrong.

The routing a selection file must state is the pipeline's question — "does the
proposal differ from the value EUROMOD currently holds?" — not "did the law
change this year?". EUROMOD's system-year N database already encodes the law of
year N, so a parameter the legislature changed for N and that the export already
carries is `unchanged`: the pipeline's job there is to re-confirm it with a
citation. Use `changed` only where EUROMOD is genuinely stale relative to the
law. The `changed`/`unchanged` distinction stays exercised either way — through
parameters the export has not caught up with, not by mislabelling ones it has.

Ground truth is never invented here: a case with no `expected_value` in the
selection leaves the value leg unscored rather than freezing EUROMOD's own value
into the golden set. Every case is written `verified: false`; the human gate is
the UI's Golden set tab (or `nomokrisis-eval verify`).
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import date
from pathlib import Path

import psycopg

from nomoscope_workflow.queue_store import slugify
from nomoscope_workflow.schema import Bracket, Routing, SourceType, TemporalBasis

from .build_dataset import _current_value
from .config import REPO_ROOT
from .dataset import save_drafted_case
from .openfisca_golden import (
    DraftOutcome,
    _case_slug,
    _load_record,
    _retire_skipped,
    db_constants,
    load_selection,
    route_against_current,
)
from .schema import Expected, GoldenCase
from .scoring import PERIOD_TO_MONTHLY, normalise_value

# The value the store holds at as_of, in the form the scorer compares: the
# scalar when there is one, else the raw EUROMOD string ('140#m*$sw_weeks',
# '4.1%'), which formula rows keep in their lineage.
def _comparable(current) -> object | None:
    if current is None:
        return None
    if current.value is not None:
        return current.value
    return current.lineage.model_answer if current.lineage is not None else None


def _expected_value(entry: dict) -> object | None:
    """The selection's curated value, with a bracket schedule promoted to Brackets."""
    value = entry.get("expected_value")
    if isinstance(value, list):
        return [Bracket.model_validate(bracket) for bracket in value]
    return value


def _period_ambiguous(current_value, expected_value, constants: Mapping[str, object] | None) -> bool:
    """True when the two values differ by nothing but a period basis.

    EUROMOD's stored scalar is a bare magnitude — the '#y' of '8964#y' lives in
    the parameter's unit, not in the value row — while a curated expectation
    states its own basis ('747#m'). `values_equal` deliberately refuses to guess
    a conversion for a bare number, so 8964 against 747#m reads as a difference
    that is in fact only the yearly/monthly basis. True only when reading the
    curated value on SOME period reproduces the stored magnitude exactly: a real
    difference (IE's 27 383 against the law's 27 382) stays a real difference.
    """
    normalised = [normalise_value(current_value, constants), normalise_value(expected_value, constants)]
    if any(value is None for value in normalised):
        return False
    with_period = [value for value in normalised if value.period is not None]
    without = [value for value in normalised if value.period is None]
    if len(with_period) != 1 or len(without) != 1:
        return False
    monthly = with_period[0].monthly()
    return any(
        math.isclose(monthly / factor, without[0].magnitude, rel_tol=1e-6)
        for factor in PERIOD_TO_MONTHLY.values()
    )


def draft_case(
    conn: psycopg.Connection,
    entry: dict,
    as_of: date,
    country: str,
    language: str,
    selection_name: str = "curated",
    constants: Mapping[str, object] | None = None,
) -> DraftOutcome:
    outcome = DraftOutcome(entry=entry)
    try:
        record, param_path = _load_record(conn, entry)
    except (KeyError, FileNotFoundError) as exc:
        outcome.skipped = f"parameter not available: {exc}"
        return outcome

    current = _current_value(record, as_of)
    comparable = _comparable(current)
    expected_value = _expected_value(entry)
    scored = "expected_value" in entry and expected_value is not None

    # Routing: the selection states it (these sets exist to pin routing traps
    # the deterministic drafter refuses to guess at); computed only as a
    # fallback, and always as a cross-check.
    computed, refusal = (None, "no expected value to route against")
    if scored:
        computed, refusal = route_against_current(current, expected_value, constants)
    # Only a `changed` verdict can be an artefact of the missing basis: equal
    # magnitudes stay equal whichever period they are read on.
    ambiguous = computed == Routing.CHANGED and _period_ambiguous(comparable, expected_value, constants)
    if ambiguous:
        outcome.warnings.append(
            f"routing not cross-checked: EUROMOD holds {comparable!r} with no period basis "
            f"while the expected value states one ({expected_value!r}) — the difference may be "
            "the y/m basis alone. Confirm against the parameter's unit when verifying"
        )
        computed = None
    explicit = entry.get("routing")
    if explicit:
        routing = Routing(explicit)
        if computed is not None and computed != routing:
            # Refuse, do not warn. A warning is only as good as the reviewer who
            # reads it: nine contested entries were verified straight through
            # because "the law changed for 2025" (what the selection meant) and
            # "differs from the value EUROMOD holds" (what the pipeline routes)
            # are different questions, and EUROMOD's 2025 database already
            # carries the 2025 law. Ground truth the drafter believes is wrong
            # must never reach a run.
            outcome.skipped = (
                f"contested routing: the selection says '{routing.value}' but the store "
                f"routes '{computed.value}' (EUROMOD holds {comparable!r} at {as_of}). "
                f"Pipeline routing compares the proposal against the value EUROMOD "
                f"currently holds — not against last year's law — so a value the export "
                f"already carries is 'unchanged' however recently the legislature changed "
                f"it. Fix `routing:` in the selection, or drop it and let "
                f"route_against_current decide"
            )
            return outcome
    elif computed is not None:
        routing = computed
    else:
        outcome.skipped = f"no `routing:` in the selection and the value {refusal}"
        return outcome

    valid_from = entry.get("expected_valid_from")
    valid_from = date.fromisoformat(valid_from) if valid_from else None
    if record.information.temporal_basis == TemporalBasis.INCOME_YEAR and valid_from is None:
        outcome.warnings.append(
            "income_year parameter with no `expected_valid_from`: the date leg is unscored, "
            "and the income-year start is not derivable from the selection"
        )

    if routing == Routing.NATIONAL_TEAM_SOURCE and (
        current is None or current.source_type != SourceType.NATIONAL_TEAM
    ):
        outcome.warnings.append(
            "expects national_team_source but the store does not flag the parameter "
            f"(source_type={getattr(current, 'source_type', None)}) — add it to "
            f"curation/{country.upper()}.curation.yaml and re-run curate-params, or the "
            "pipeline cannot route it"
        )

    note_parts = [
        f"curated: {selection_name}#{entry.get('id') or entry.get('model_target') or entry.get('group_id')}",
        f"euromod value in force at {as_of}: "
        + (f"{comparable!r} from {current.valid_from}" if current is not None else "none"),
    ]
    if not scored:
        note_parts.append(
            "value leg not scored: the selection states no expected_value "
            "(the law's value is not established for this case yet)"
        )
        outcome.warnings.append("value leg not scored (no expected_value in the selection)")
    if not entry.get("citations"):
        outcome.warnings.append(
            "no citations: the citation leg is unscored until the source act is ingested"
        )
    if entry.get("note"):
        note_parts.append(entry["note"])
    note_parts.extend(f"drafting warning: {warning}" for warning in outcome.warnings)

    target = entry.get("model_target") or entry.get("group_id") or ""
    slug = entry.get("id") or (
        _case_slug(record.information.model_target, country)
        if target.startswith("euromod://")
        else slugify(target)
    )
    corpus_available = entry.get("corpus_available")
    if corpus_available is False:
        note_parts.append(
            "corpus_available: false — the act stating this value is not ingested yet, so "
            "no retrieval can reach it. The case measures ingest coverage and is excluded "
            "from the 'source in corpus' KPI slice"
        )
    outcome.case = GoldenCase(
        id=f"{country.lower()}_{slug}_{as_of.isoformat()}",
        country=country.upper(),
        language=language,
        parameter_file=param_path.relative_to(REPO_ROOT).as_posix(),
        as_of=as_of,
        difficulty=entry.get("difficulty") or ("table" if entry.get("group_id") else "plain"),
        source_class=entry.get("source_class", "codified_law"),
        expected=Expected(
            routing=routing,
            value=expected_value if scored else None,
            valid_from=valid_from,
            citations=list(entry.get("citations", [])),
        ),
        corpus_available=corpus_available,
        verified=False,
        drafted_by="human",
        notes=" | ".join(note_parts),
    )
    outcome.path = param_path
    return outcome


def build_dataset(
    conn: psycopg.Connection,
    dataset_dir: Path,
    selection: Path,
    as_of: date,
    country: str | None = None,
    language: str | None = None,
) -> list[DraftOutcome]:
    doc, entries = load_selection(selection)
    country = (country or doc.get("country") or "").upper()
    language = (language or doc.get("language") or country).lower()
    if not country:
        raise ValueError(f"{selection}: no country in the selection file and none given")
    constants = db_constants(conn, country, as_of)
    outcomes: list[DraftOutcome] = []
    for entry in entries:
        outcome = draft_case(
            conn, entry, as_of, country, language,
            selection_name=selection.name, constants=constants,
        )
        outcomes.append(outcome)
        if outcome.case is not None:
            _, reset = save_drafted_case(dataset_dir, outcome.case)
            if reset:
                outcome.warnings.append(
                    "ground truth changed since it was reviewed — the case is back to "
                    "verified:false and must be re-verified before it counts"
                )
    _retire_skipped(dataset_dir, outcomes, as_of, country)
    return outcomes


def selection_path(country: str) -> Path:
    from .config import EVAL_ROOT

    return EVAL_ROOT / "golden_sources" / f"{country.lower()}.json"

