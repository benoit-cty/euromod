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
- `income_year` (the FR income-tax family): system year Y holds the
  schedule of the finance act for Y, which EUROMOD applies to Y incomes and
  French law labels by the PREVIOUS year's income — system year 2025 holds the
  "income 2024" schedule ("impôt 2025 sur les revenus 2024").
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
from datetime import date

import psycopg
from nomoscope_workflow.schema import (
    Bracket,
    Routing,
    TemporalBasis,
    income_year_for,
    start_of_year_as_of,
)

from .golden_drafting import (
    DraftOutcome,
    golden_case,
    load_record,
    resolve_corpus_available,
    retire_skipped,
    save_outcome,
)
from .parameter_store import current_value, db_constants, route_against_current
from .schema import Expected

_BRACKET_COMPONENT = re.compile(r"^brackets\[(\d+)\]\.(\w+)$")


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
        "id": row[0],
        "value_kind": row[1],
        "unit": row[2],
        "short_label": row[3],
        "description": row[4],
        "commit": row[5],
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


def schedule_at(conn: psycopg.Connection, external_parameter_id: int, on: date) -> tuple[list[Bracket], date | None]:
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


def references_at(conn: psycopg.Connection, external_parameter_id: int, on: date) -> list[dict]:
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
    row = conn.execute("SELECT citation FROM legal_units WHERE national_id = %s LIMIT 1", (national_id,)).fetchone()
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
    row = conn.execute("SELECT national_id FROM instruments WHERE national_id = %s LIMIT 1", (national_id,)).fetchone()
    return row[0] if row else None


# ---------------------------------------------------------------------------
# Drafting one case
# ---------------------------------------------------------------------------


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
        record, parameter_target = load_record(conn, entry)
    except (KeyError, ValueError) as exc:
        outcome.skipped = f"parameter not available: {exc}"
        return outcome

    external = external_parameter(conn, country, entry["openfisca_path"], kind=kind)
    if external is None:
        outcome.skipped = f"no external parameter {entry['openfisca_path']}"
        return outcome

    income_year = record.information.temporal_basis == TemporalBasis.INCOME_YEAR
    target_date = date(income_year_for(as_of.year), 1, 1) if income_year else as_of
    if record.information.temporal_basis == TemporalBasis.START_OF_YEAR:
        target_date = start_of_year_as_of(as_of)
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
            outcome.skipped = f"no value in force at {target_date} for {entry['openfisca_path']}" + (
                f" :: {component}" if component != "value" else ""
            )
            return outcome
        expected_value = value * factor
        raw = value

    valid_from = date(income_year_for(as_of.year), 1, 1) if income_year else source_date

    # Routing is deterministic: the drafted value against the value EUROMOD
    # currently holds (an explicit `routing:` on the entry overrides).
    current = current_value(record, as_of)
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
        f"euromod value in force at {as_of}: " + (f"{current.value} from {current.valid_from}" if current else "none"),
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
    corpus_available = resolve_corpus_available(entry, in_corpus if references else None)
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

    outcome.case = golden_case(
        entry,
        record,
        parameter_target,
        as_of,
        country,
        language,
        Expected(routing=routing, value=expected_value, valid_from=valid_from, citations=citations),
        corpus_available=corpus_available,
        drafted_by=f"openfisca@{(external['commit'] or 'unknown')[:7]}",
        notes=note_parts,
        is_bracket_table=component == "brackets",
    )
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
    # `exclude: true` keeps a parameter out of the set, top-up included: its
    # OpenFisca series is stale (FR's RCI ceiling, abolished by the 2025
    # self-employed reform, is still `montant_du_plafond_rci`). A header with
    # `fill_from_links: false` is a selection that names every case itself.
    excluded = [e for e in entries if e.get("exclude")]
    entries = [e for e in entries if not e.get("exclude")]
    fill_from_links = fill_from_links and header.get("fill_from_links", True)
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
            if save_outcome(conn, outcome):
                written += 1

    drain(entries)
    if fill_from_links and written < limit:
        # Ask for more than the shortfall: entries drop out on formula values
        # and missing change points, and a short golden set is the failure mode
        # that matters here.
        exclude = {e["model_target"] for e in [*entries, *excluded] if e.get("model_target")}
        extra = entries_from_links(conn, country, as_of, (limit - written) * 3, exclude, kind=kind)
        drain(extra)
    retire_skipped(conn, outcomes, as_of, country)
    return outcomes
