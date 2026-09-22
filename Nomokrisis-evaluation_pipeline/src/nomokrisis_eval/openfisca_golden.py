"""Draft golden cases from the ingested OpenFisca corpus (params.external_*).

OpenFisca-France is a human-curated parameter database: per-date values with
per-date legal references (`LEGIARTI`/`JORFTEXT` hrefs). That is exactly the
`(value, effective date, reference)` triple a golden case needs, for thousands
of parameters, at a pinned git commit — §4.3 of
Param_Schema/openfisca_france_usage.md.

What this module does NOT do: decide anything. Every case it writes (a row in
eval.golden_cases) is `verified: false` and carries its own provenance in `notes` (OpenFisca path,
component, scale, the reference titles, whether the cited act is in the
legislation corpus). A human confirms each one in the validation UI's Golden
set tab before it counts as ground truth. OpenFisca is curated and occasionally
wrong or lagging, so an unreviewed case is a suggestion, not a fact.

Two dating conventions meet here, and the parameter's own `temporal_basis`
decides which applies:

- `in_force` (SMIC, PSS, benefit amounts): the expected value is the OpenFisca
  value in force at `as_of`, and the expected `valid_from` is the date that
  value took effect.
- `income_year` (the FR income-tax family): the system year is the year the tax
  is assessed, and French law assesses it on the PREVIOUS year's income —
  system year 2025 is income year 2024 ("impôt 2025 sur les revenus 2024").
  `schema.income_year_for` owns that mapping. OpenFisca keys these parameters
  by income year too, so the expected value is its entry at
  `income_year_for(system year)-01-01`, and the expected `valid_from` is that
  same date, whatever the enacting finance act's own publication date.

OpenFisca stores change points only, so "the value at date D" always means the
latest entry at or before D — never an entry keyed exactly D.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date

import psycopg

from nomoscope_workflow.queue_store import slugify
from nomoscope_workflow.schema import (
    Bracket,
    ParameterRecord,
    Routing,
    TemporalBasis,
    income_year_for,
)
from nomoscope_workflow import paramdb

from .build_dataset import _current_value, case_slug
from .golden_store import delete_case, load_case, save_drafted_case
from .labels import draft_labels
from .schema import Expected, GoldenCase
from .scoring import normalise_value, values_equal

GROUP_PREFIX = "group:"

_BRACKET_COMPONENT = re.compile(r"^brackets\[(\d+)\]\.(\w+)$")

#: Kept under its old name for the callers (and tests) that import it here.
_case_slug = case_slug


@dataclass
class DraftOutcome:
    """One entry's result: a case, or the reason it produced none."""

    entry: dict
    case: GoldenCase | None = None
    skipped: str | None = None
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Reading the external corpus
# ---------------------------------------------------------------------------


def external_parameter(conn: psycopg.Connection, country: str, path: str, kind: str = "openfisca") -> dict | None:
    row = conn.execute(
        """
        SELECT ep.id, ep.value_kind, ep.unit, ep.short_label, ep.description, ec.commit_sha
        FROM params.external_parameters ep
        JOIN params.external_corpora ec ON ec.id = ep.corpus_id
        WHERE ec.country = %s AND ec.kind = %s AND ep.path = %s
        """,
        (country, kind, path),
    ).fetchone()
    if row is None:
        return None
    return {
        "id": row[0], "value_kind": row[1], "unit": row[2],
        "short_label": row[3], "description": row[4], "commit": row[5],
    }


def value_at(
    conn: psycopg.Connection, external_parameter_id: int, component: str, on: date
) -> tuple[float | None, date | None]:
    """Latest change point at or before `on` for one component."""
    row = conn.execute(
        """
        SELECT value_numeric, valid_from FROM params.external_values
        WHERE external_parameter_id = %s AND component = %s AND valid_from <= %s
        ORDER BY valid_from DESC LIMIT 1
        """,
        (external_parameter_id, component, on),
    ).fetchone()
    return (None, None) if row is None else (row[0], row[1])


def is_annually_indexed(
    conn: psycopg.Connection,
    external_parameter_id: int,
    component: str,
    before: date,
    years: int = 3,
    min_changes: int = 2,
) -> bool:
    """Does this series move nearly every year in the `years` before `before`?

    Tells "OpenFisca has no entry for this income year because the law did not
    change" (a tax rate, the CEHR thresholds — untouched since 2012) apart from
    "because the corpus has not caught up with the finance act" (any indexed
    amount). Only the second is a lag worth warning a reviewer about.
    """
    pattern = "brackets%" if component == "brackets" else component
    row = conn.execute(
        """
        SELECT count(DISTINCT valid_from) FROM params.external_values
        WHERE external_parameter_id = %s AND component LIKE %s
          AND valid_from >= %s AND valid_from < %s
        """,
        (external_parameter_id, pattern, date(before.year - years, before.month, before.day), before),
    ).fetchone()
    return bool(row and row[0] >= min_changes)


def schedule_at(
    conn: psycopg.Connection, external_parameter_id: int, on: date
) -> tuple[list[Bracket], date | None]:
    """The whole bracket schedule in force at `on`, band by band.

    Bands are reconstructed from the flattened `brackets[i].<field>` series,
    each field resolved independently (OpenFisca revalorises thresholds without
    restating rates). A band whose latest entry is null has been abolished —
    the 6th IR band was removed in 2014 — and is dropped.
    """
    rows = conn.execute(
        """
        SELECT DISTINCT component FROM params.external_values
        WHERE external_parameter_id = %s AND component LIKE 'brackets[%%'
        """,
        (external_parameter_id,),
    ).fetchall()
    bands: dict[int, dict[str, float | None]] = {}
    latest: date | None = None
    for (component,) in rows:
        match = _BRACKET_COMPONENT.match(component)
        if match is None:
            continue
        index, field_name = int(match.group(1)), match.group(2)
        if field_name not in ("threshold", "rate", "amount"):
            continue
        value, valid_from = value_at(conn, external_parameter_id, component, on)
        bands.setdefault(index, {})[field_name] = value
        if value is not None and valid_from is not None and (latest is None or valid_from > latest):
            latest = valid_from
    schedule: list[Bracket] = []
    for index in sorted(bands):
        fields = bands[index]
        if all(fields.get(name) is None for name in ("threshold", "rate", "amount")):
            continue
        schedule.append(
            Bracket(
                threshold=fields.get("threshold") or 0.0,
                rate=fields.get("rate"),
                amount=fields.get("amount"),
            )
        )
    return schedule, latest


def references_at(
    conn: psycopg.Connection, external_parameter_id: int, on: date
) -> list[dict]:
    """References attached to the value point in force at `on` (plus undated ones)."""
    rows = conn.execute(
        """
        SELECT title, href, national_id, valid_from FROM params.external_references
        WHERE external_parameter_id = %s
          AND (valid_from IS NULL OR valid_from = (
                SELECT max(valid_from) FROM params.external_references
                WHERE external_parameter_id = %s AND valid_from <= %s))
        ORDER BY valid_from NULLS LAST, id
        """,
        (external_parameter_id, external_parameter_id, on),
    ).fetchall()
    return [
        {"title": title, "href": href, "national_id": national_id, "valid_from": valid_from}
        for title, href, national_id, valid_from in rows
    ]


_PRE_INDEXATION = re.compile(r"avant\s+(?:revalorisation|indexation)", re.IGNORECASE)


def _is_pre_indexation_reference(reference: dict) -> bool:
    """Does OpenFisca label this reference as the text BEFORE annual indexation?"""
    return bool(_PRE_INDEXATION.search(reference.get("title") or ""))


def resolve_citation(conn: psycopg.Connection, national_id: str) -> str | None:
    """The legislation DB's own citation string for a national id, if ingested.

    Tried in order: the legal unit's id (`JORFARTI…`, `LEGIARTI…` for articles
    we hold), the id of one of its versions, then the instrument. An instrument
    id is a usable expected citation on its own: golden-set citations are
    matched by containment, so `JORFTEXT000053508155` matches the pinpoint
    `JORFTEXT000053508155, art. 4` the pipeline proposes.
    """
    row = conn.execute(
        "SELECT citation FROM legal_units WHERE national_id = %s LIMIT 1", (national_id,)
    ).fetchone()
    if row:
        return row[0]
    row = conn.execute(
        """
        SELECT lu.citation FROM legal_unit_versions lv
        JOIN legal_units lu ON lu.id = lv.legal_unit_id
        WHERE lv.source_version_id = %s LIMIT 1
        """,
        (national_id,),
    ).fetchone()
    if row:
        return row[0]
    row = conn.execute(
        "SELECT national_id FROM instruments WHERE national_id = %s LIMIT 1", (national_id,)
    ).fetchone()
    return row[0] if row else None


# ---------------------------------------------------------------------------
# Drafting one case
# ---------------------------------------------------------------------------


def _load_record(conn: psycopg.Connection, entry: dict) -> tuple[ParameterRecord, str]:
    """The parameter under test, plus the `parameter_target` the runner hands
    to the workflow.

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
    current,
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
    comparable = current.value
    if comparable is None and current.lineage is not None:
        comparable = current.lineage.model_answer
    if comparable is None:
        return None, "has no scalar and no raw string"
    if isinstance(comparable, str) and normalise_value(comparable, constants) is None:
        return None, (
            f"cannot be normalised ({comparable!r}) "
            "— set an explicit `routing:` in the selection file to include it"
        )
    if values_equal(comparable, expected_value, constants):
        return Routing.UNCHANGED, None
    if isinstance(comparable, str):
        return None, (
            f"is a formula/weighted average ({comparable!r}) that differs from the "
            f"drafted point value ({expected_value!r}) — ambiguous by convention "
            "(FYA); set an explicit `routing:` in the selection file"
        )
    return Routing.CHANGED, None


def draft_case(
    conn: psycopg.Connection,
    entry: dict,
    as_of: date,
    country: str,
    language: str,
    kind: str = "openfisca",
    constants: Mapping[str, object] | None = None,
) -> DraftOutcome:
    outcome = DraftOutcome(entry=entry)
    try:
        record, parameter_target = _load_record(conn, entry)
    except (KeyError, ValueError) as exc:
        outcome.skipped = f"parameter not available: {exc}"
        return outcome

    external = external_parameter(conn, country, entry["openfisca_path"], kind=kind)
    if external is None:
        outcome.skipped = f"no external parameter {entry['openfisca_path']}"
        return outcome

    income_year = record.information.temporal_basis == TemporalBasis.INCOME_YEAR
    target_date = date(income_year_for(as_of.year), 1, 1) if income_year else as_of
    factor = float(entry.get("factor", 1))
    component = entry.get("component", "value")

    if component == "brackets":
        schedule, source_date = schedule_at(conn, external["id"], target_date)
        if not schedule:
            outcome.skipped = f"no schedule in force at {target_date} in {entry['openfisca_path']}"
            return outcome
        if factor != 1:
            outcome.warnings.append("factor ignored for bracket schedules")
        expected_value: list[Bracket] | float = schedule
        raw = [b.model_dump(exclude_none=True) for b in schedule]
    else:
        value, source_date = value_at(conn, external["id"], component, target_date)
        if value is None:
            outcome.skipped = (
                f"no value in force at {target_date} for {entry['openfisca_path']}"
                + (f" :: {component}" if component != "value" else "")
            )
            return outcome
        expected_value = value * factor
        raw = value

    valid_from = date(income_year_for(as_of.year), 1, 1) if income_year else source_date

    # Routing is deterministic: the drafted value against the value EUROMOD
    # currently holds (an explicit `routing:` on the entry overrides).
    current = _current_value(record, as_of)
    explicit = entry.get("routing")
    if explicit:
        routing = Routing(explicit)
    else:
        routing, skip_reason = route_against_current(current, expected_value, constants)
        if routing is None:
            outcome.skipped = f"EUROMOD value in force at {as_of}: {skip_reason}"
            return outcome

    references = references_at(conn, external["id"], target_date)
    citations: list[str] = []
    unresolved: list[str] = []
    # True once a reference resolves to a legal unit the corpus actually holds.
    # A case where none does is unanswerable by any model — the text stating the
    # value has not been ingested — so it must be scored as corpus coverage, not
    # as model quality (`GoldenCase.corpus_available`).
    in_corpus = False
    for reference in references:
        national_id = reference.get("national_id")
        resolved = resolve_citation(conn, national_id) if national_id else None
        if resolved:
            # A reference OpenFisca itself marks as the pre-indexation text
            # ("Article L136-8 … (seuils avant revalorisation)") is the base
            # article, not the text stating this year's amount: that lives in
            # the companion reference (a ministerial letter with no id). It is
            # still a citation a correct pipeline produces, but it cannot make
            # the case answerable.
            if not _is_pre_indexation_reference(reference):
                in_corpus = True
            if resolved not in citations:
                citations.append(resolved)
        elif national_id and national_id.startswith(("JORFTEXT", "LEGITEXT")):
            # Instrument-level id: a correct pipeline citation contains it
            # ("JORFTEXT…, art. 4"), so it stays an expected citation and the
            # case scores an honest miss until the act is ingested.
            if national_id not in citations:
                citations.append(national_id)
            unresolved.append(f"{reference['title']} [{national_id}] not in the corpus yet")
        elif national_id:
            # Article-level id of an act we do not hold: no string the pipeline
            # could produce would match it, so it is provenance, not ground truth.
            unresolved.append(f"{reference['title']} [{national_id}] not in the corpus (not scorable)")
        else:
            unresolved.append(f"{reference['title']} (no Legifrance id)")
    for extra in entry.get("citations", []):
        if extra not in citations:
            citations.append(extra)

    note_parts = [
        f"openfisca: {entry['openfisca_path']}"
        + (f" :: {component}" if component != "value" else "")
        + (f" x{factor:g}" if factor != 1 else ""),
        f"openfisca value at {target_date}: {raw} (change point {source_date})",
        f"euromod value in force at {as_of}: "
        + (f"{current.value} from {current.valid_from}" if current else "none"),
        f"link: {entry.get('match_method', 'manual')}"
        + (f" score {entry['score']:.2f}" if entry.get("score") is not None else ""),
    ]
    # An annually indexed income-year parameter whose backing change point
    # predates the income year is the update lag itself, not a confirmed "no
    # change": the finance act setting that year's value has not reached the
    # OpenFisca corpus, so the expectation just repeats the previous year.
    # EUROMOD is a year behind for the same reason, so both sides agree and the
    # case reads `unchanged` — which would freeze the lag into the golden set if
    # a reviewer accepts it. A rate or ceiling the law simply has not touched
    # (the 45 % band, the CEHR thresholds) is excluded: there, no change point
    # in the income year is the correct answer, not a gap.
    if (
        income_year
        and source_date
        and source_date < target_date
        and is_annually_indexed(conn, external["id"], component, target_date)
    ):
        lag = (
            f"lag warning: OpenFisca has no change point in income year {target_date.year}; "
            f"the expected value is the {source_date.year} one carried forward. Do not accept "
            f"an `unchanged` verdict on this basis — re-draft once the finance act for income "
            f"year {target_date.year} is in the OpenFisca corpus."
        )
        note_parts.append(lag)
        outcome.warnings.append(lag)
    corpus_available = in_corpus if references else None
    if "corpus_available" in entry:
        # The selection file knows more than the reference list: an explicit
        # value on the entry wins (the curated builder has always allowed it).
        corpus_available = entry["corpus_available"]
    if corpus_available is False:
        note_parts.append(
            "corpus_available: false — not one of this parameter's OpenFisca references "
            "resolves in the legislation corpus, so no retrieval can reach the text stating "
            "the value. The case measures ingest coverage; it is excluded from the "
            "'source in corpus' KPI slice until the act is ingested"
        )
    if unresolved:
        note_parts.append("references not resolved in the legislation corpus: " + "; ".join(unresolved))
    if entry.get("note"):
        note_parts.append(entry["note"])
    outcome.warnings.extend(unresolved)

    drafted = draft_labels(
        value=expected_value,
        citations=citations,
        temporal_basis=record.information.temporal_basis,
        is_bracket_table=component == "brackets",
    )
    slug = entry.get("id") or _case_slug(record.information.model_target, country)
    case = GoldenCase(
        id=f"{country.lower()}_{slug}_{as_of.isoformat()}",
        country=country.upper(),
        language=language,
        parameter_target=parameter_target,
        as_of=as_of,
        difficulty=entry.get("difficulty") or drafted.difficulty,
        hazards=entry.get("hazards", drafted.hazards),
        labels_drafted="difficulty" not in entry and "hazards" not in entry,
        source_class=entry.get("source_class", "codified_law"),
        expected=Expected(
            routing=routing,
            value=expected_value,
            valid_from=valid_from,
            citations=citations,
        ),
        corpus_available=corpus_available,
        verified=False,
        drafted_by=f"openfisca@{(external['commit'] or 'unknown')[:7]}",
        notes=" | ".join(note_parts),
    )
    outcome.case = case
    return outcome


# ---------------------------------------------------------------------------
# Selecting what to draft
# ---------------------------------------------------------------------------


def entries_from_links(
    conn: psycopg.Connection,
    country: str,
    as_of: date,
    limit: int,
    exclude_targets: set[str],
    kind: str = "openfisca",
) -> list[dict]:
    """Top-scoring params.parameter_links rows as draft entries.

    Fills the golden set out beyond the hand-curated core. Ordered by score,
    and restricted to parameters EUROMOD still holds a numeric value for at
    `as_of` — 231 of the 702 FR series are closed (abolished instruments,
    hard-dated excises), and a dormant series makes a case about nothing.
    """
    rows = conn.execute(
        """
        SELECT p.model_target, ep.path, pl.component, pl.factor, pl.match_method, pl.score
        FROM params.parameter_links pl
        JOIN params.parameters p ON p.id = pl.parameter_id
        JOIN params.external_parameters ep ON ep.id = pl.external_parameter_id
        JOIN params.external_corpora ec ON ec.id = ep.corpus_id
        WHERE p.country = %s AND ec.country = %s AND ec.kind = %s
          AND EXISTS (
              SELECT 1 FROM params.model_values mv
              WHERE mv.parameter_id = p.id AND mv.value_numeric IS NOT NULL
                AND mv.valid_from <= %s AND (mv.valid_to IS NULL OR mv.valid_to >= %s)
          )
        ORDER BY pl.score DESC NULLS LAST, pl.id
        """,
        (country.upper(), country.upper(), kind, as_of, as_of),
    ).fetchall()
    entries: list[dict] = []
    seen: set[str] = set(exclude_targets)
    for model_target, path, component, factor, match_method, score in rows:
        if model_target in seen or len(entries) >= limit:
            continue
        seen.add(model_target)
        entries.append(
            {
                "model_target": model_target,
                "openfisca_path": path,
                "component": component,
                "factor": factor,
                "match_method": match_method,
                "score": score,
            }
        )
    return entries


def build_dataset(
    conn: psycopg.Connection,
    header: dict,
    entries: list[dict],
    as_of: date,
    country: str = "FR",
    language: str = "fr",
    limit: int = 50,
    fill_from_links: bool = True,
    kind: str = "openfisca",
) -> list[DraftOutcome]:
    """Draft (and upsert into eval.golden_cases) one case per selection entry,
    topped up from params.parameter_links when `fill_from_links`.

    `header`/`entries` are the selection row (`golden_store.load_selection`).
    """
    country = (header.get("country") or country).upper()
    language = (header.get("language") or language).lower()
    entries = list(entries)
    outcomes: list[DraftOutcome] = []
    written = 0
    constants = db_constants(conn, country, as_of)

    def drain(pool: list[dict]) -> None:
        nonlocal written
        for entry in pool:
            if written >= limit:
                return
            outcome = draft_case(conn, entry, as_of, country, language, kind=kind, constants=constants)
            outcomes.append(outcome)
            if outcome.case is not None:
                if save_drafted_case(conn, outcome.case):
                    outcome.warnings.append(
                        "ground truth changed since it was reviewed — the case is back to "
                        "verified:false and must be re-verified before it counts"
                    )
                written += 1

    drain(entries)
    if fill_from_links and written < limit:
        # Ask for more than the shortfall: entries drop out on formula values
        # and missing change points, and a short golden set is the failure mode
        # that matters here.
        exclude = {e["model_target"] for e in entries if e.get("model_target")}
        extra = entries_from_links(conn, country, as_of, (limit - written) * 3, exclude, kind=kind)
        drain(extra)
    _retire_skipped(conn, outcomes, as_of, country)
    return outcomes


def stale_case_id(entry: dict, as_of: date, country: str) -> str | None:
    """The id the entry's case carries (or would carry), from the entry alone."""
    target = entry.get("model_target") or entry.get("group_id")
    if not target:
        return None
    slug = entry.get("id") or (
        _case_slug(target, country) if target.startswith("euromod://") else slugify(target)
    )
    return f"{country.lower()}_{slug}_{as_of.isoformat()}"


def _retire_skipped(
    conn: psycopg.Connection, outcomes: list[DraftOutcome], as_of: date, country: str
) -> None:
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
        case_id = stale_case_id(outcome.entry, as_of, country)
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
