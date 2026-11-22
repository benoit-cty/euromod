"""Golden-set commands: the schema, the selections, drafting and verifying cases."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import typer
from nomoscope_workflow.schema import system_year_anchor

from .. import build_dataset as builder
from .. import curated_golden, golden_store, openfisca_golden
from .. import db as evaldb
from ..config import load_eval_config
from ..import_golden import (
    DEFAULT_DATASET_DIR,
    DEFAULT_EMBEDDING_DATASET_DIR,
    DEFAULT_SOURCES_DIR,
    import_golden,
)
from ..labels import DraftedLabels, draft_labels
from ..parameter_store import country_targets, load_case_record
from ..schema import GoldenCase
from .common import app, emit_result, parse_date


@app.command("init-db")
def init_db() -> None:
    """Create the eval schema (tables + summary view) in the legislation DB."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        evaldb.apply_schema(conn)
    typer.echo(f"eval schema applied to {cfg.database_url}")


@app.command("import-golden")
def import_golden_cmd(
    dataset_dir: Path = typer.Option(DEFAULT_DATASET_DIR, "--dataset-dir", help="dataset/<cc>/*.json"),
    embedding_dataset_dir: Path = typer.Option(
        DEFAULT_EMBEDDING_DATASET_DIR, "--embedding-dataset-dir", help="dataset_embedding/<cc>/*.json"
    ),
    sources_dir: Path = typer.Option(DEFAULT_SOURCES_DIR, "--sources-dir", help="golden_sources/*.json"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Resolve and count, write nothing"),
) -> None:
    """Import the on-disk golden set (cases, retrieval cases, selections) into eval.*, once.

    Idempotent: every row is upserted. Cases keep the verdict recorded in their
    file. A case whose `parameter_file` cannot be mapped to a parameter in the
    params DB is reported and skipped.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        report = import_golden(
            conn,
            dataset_dir=dataset_dir,
            embedding_dataset_dir=embedding_dataset_dir,
            sources_dir=sources_dir,
            dry_run=dry_run,
        )
    verb = "would import" if dry_run else "imported"
    typer.echo(
        f"{verb}: {report.selections} selection(s), {report.cases} golden case(s) "
        f"({report.cases_verified} verified), {report.embedding_cases} embedding case(s)"
    )
    if report.resolved_by:
        typer.echo("  targets resolved via " + ", ".join(f"{k}={v}" for k, v in sorted(report.resolved_by.items())))
    for warning in report.warnings:
        typer.echo(f"  ! {warning}")
    for unresolved in report.unresolved:
        typer.echo(f"  x skipped {unresolved}")
    emit_result(
        {
            "selections": report.selections,
            "cases": report.cases,
            "embedding_cases": report.embedding_cases,
            "unresolved": len(report.unresolved),
            "dry_run": dry_run,
        }
    )


def _selection_or_exit(conn, country: str, kind: str) -> tuple[dict, list[dict]]:
    try:
        return golden_store.load_selection(conn, country, kind)
    except KeyError as exc:
        typer.echo(
            f"{exc.args[0]} — write one with `nomokrisis-eval selection-import <file>` "
            "(or `import-golden` for the pre-ADR-0004 golden_sources/ files)"
        )
        raise typer.Exit(1) from exc


def _echo_outcomes(outcomes, width: int) -> int:
    written = 0
    for outcome in outcomes:
        label = outcome.entry.get("model_target") or outcome.entry.get("group_id", "?")
        if outcome.case is None:
            typer.echo(f"  ~ skipped {label}: {outcome.skipped}")
            # A skip can retire a case the previous run wrote; never silently.
            for warning in outcome.warnings:
                typer.echo(f"    ! {warning}")
            continue
        written += 1
        expected = outcome.case.expected
        verdict = "verified" if outcome.case.verified else "draft"
        typer.echo(
            f"  {expected.routing:<{width}} {outcome.case.id}"
            f"  value={expected.value}  valid_from={expected.valid_from}"
            f"  citations={expected.citations or '[]'}  [{verdict}]"
        )
        for warning in outcome.warnings:
            typer.echo(f"    ! {warning}")
    return written


@app.command("build-dataset")
def build_dataset_cmd(
    source_file: Path = typer.Argument(..., help="Trusted source document (country report excerpt, notes)"),
    country: str = typer.Option(..., "--country", help="ISO country code, e.g. FR"),
    as_of: str = typer.Option(..., "--as-of", help="Reference date, YYYY-MM-DD"),
    language: str = typer.Option(
        None, "--language", help="Source-legislation language (default: country code lowercased)"
    ),
    target: list[str] = typer.Option(
        None,
        "--target",
        help="Parameter(s) to draft: euromod://… or group:<group_id> in the params DB "
        "(default: every parameter of the country)",
    ),
    model: str = typer.Option(None, "--model", help="Provider-prefixed drafting model (default: EVAL_BUILDER_MODEL)"),
) -> None:
    """Draft golden cases with an LLM from a trusted document (verified=false until a human confirms them)."""
    cfg = load_eval_config()
    try:
        drafting_model = builder.check_builder_model(model or cfg.builder_model)
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(1) from exc
    if not source_file.exists():
        typer.echo(f"no source document at {source_file}")
        raise typer.Exit(1)
    source_text = source_file.read_text(encoding="utf-8")

    with evaldb.connect(cfg.database_url) as conn:
        targets = list(target or []) or country_targets(conn, country)
        if not targets:
            typer.echo(f"no parameters for {country.upper()} in the params DB (ingest-params first)")
            raise typer.Exit(1)
        records = []
        for parameter_target in targets:
            try:
                records.append((load_case_record(conn, parameter_target), parameter_target))
            except (KeyError, ValueError) as exc:
                typer.echo(f"  ~ skipped {parameter_target}: {exc}")

        results = builder.build_cases(
            drafting_model, source_text, records, parse_date(as_of), (language or country).lower()
        )
        written = 0
        for case, message in results:
            typer.echo(message)
            if case is not None and case.country.upper() == country.upper():
                reset = golden_store.save_drafted_case(conn, case)
                typer.echo(f"  -> {case.id} ({'verdict reset — ' if reset else ''}review before freezing)")
                written += 1
    typer.echo(f"{written} draft case(s) written to eval.golden_cases. Review them in the UI's Golden set tab.")
    emit_result({"written": written})


@app.command("build-openfisca-dataset")
def build_openfisca_dataset(
    year: int = typer.Option(..., "--year", help="EUROMOD system year to draft cases for, e.g. 2025"),
    country: str = typer.Option(..., "--country", help="ISO country code"),
    as_of: str = typer.Option(
        None, "--as-of", help="Anchor date inside the system year (default: <year>-07-01, as --year runs)"
    ),
    limit: int = typer.Option(50, "--limit", help="Maximum number of cases to write"),
    fill: bool = typer.Option(
        True, "--fill/--curated-only", help="Top the set up from params.parameter_links suggestions"
    ),
) -> None:
    """Draft golden cases from the ingested OpenFisca corpus (verified=false).

    The selection comes from eval.golden_selections (kind `openfisca`). Ground
    truth comes from OpenFisca's curated per-date values and legal references;
    routing is computed deterministically against what EUROMOD holds. Review
    each case in the UI's Golden set tab before it counts.
    """
    cfg = load_eval_config()
    anchor = parse_date(as_of) if as_of else system_year_anchor(year)
    with evaldb.connect(cfg.database_url) as conn:
        header, entries = _selection_or_exit(conn, country, "openfisca")
        outcomes = openfisca_golden.build_dataset(
            conn,
            header,
            entries,
            anchor,
            country=country.upper(),
            limit=limit,
            fill_from_links=fill,
        )
    written = _echo_outcomes(outcomes, 10)
    typer.echo(
        f"\n{written} draft case(s) in eval.golden_cases. "
        "Review them in the UI's Golden set tab (or `nomokrisis-eval verify <id>`) before running an evaluation."
    )
    emit_result({"written": written})


@app.command("build-curated-dataset")
def build_curated_dataset(
    year: int = typer.Option(..., "--year", help="EUROMOD system year to draft cases for, e.g. 2025"),
    country: str = typer.Option(..., "--country", help="ISO country code, e.g. IE"),
    as_of: str = typer.Option(
        None, "--as-of", help="Anchor date inside the system year (default: <year>-07-01, as --year runs)"
    ),
) -> None:
    """Draft golden cases from the hand-curated selection (verified=false).

    For countries with no external corpus to read ground truth from (IE, LT,
    ES, NL): the expected values are curated from the acts themselves in the
    `curated` selection of eval.golden_selections. The parameter under test
    still comes from the params DB, and the selection's routing is
    cross-checked against what EUROMOD holds.
    """
    cfg = load_eval_config()
    anchor = parse_date(as_of) if as_of else system_year_anchor(year)
    with evaldb.connect(cfg.database_url) as conn:
        header, entries = _selection_or_exit(conn, country, "curated")
        outcomes = curated_golden.build_dataset(
            conn,
            header,
            entries,
            anchor,
            country=country.upper(),
            selection_name=f"{country.lower()}.json",
        )
    written = _echo_outcomes(outcomes, 20)
    typer.echo(
        f"\n{written} draft case(s) in eval.golden_cases. "
        "Review them in the UI's Golden set tab (or `nomokrisis-eval verify <id>`) before running an evaluation."
    )
    emit_result({"written": written})


@app.command()
def verify(
    case_ids: list[str] = typer.Argument(..., help="Golden case ids to mark as human-verified"),
    unverify: bool = typer.Option(False, "--unverify", help="Clear the flag instead of setting it"),
    note: str = typer.Option(None, "--note", help="Review note stored with the verdict"),
) -> None:
    """Flip `verified` on golden cases — the human gate before the set counts as ground truth.

    The reviewer is the database login (`current_user`), never a flag.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        for case_id in case_ids:
            case = golden_store.set_verified(conn, case_id, not unverify, note)
            if case is None:
                typer.echo(f"  ! unknown case {case_id}")
                continue
            typer.echo(f"  {'verified' if case.verified else 'unverified'} {case_id} by {case.reviewed_by}")


@app.command("list-cases")
def list_cases(
    country: list[str] = typer.Option(None, "--country"),
    verified_only: bool = typer.Option(False, "--verified-only"),
) -> None:
    """List the golden set (eval.golden_cases)."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        cases = golden_store.load_cases(conn, countries=country or None, verified_only=verified_only)
    for case in cases:
        flag = "✓" if case.verified else ("rejected" if case.reviewed_by else "draft")
        typer.echo(
            f"{flag:<8} {case.country} {case.language} as_of={case.as_of} routing={case.expected.routing:<12} {case.id}"
        )
    typer.echo(f"{len(cases)} case(s), golden_set_hash={golden_store.golden_set_hash(cases)}")


_REBUILD_FOR_KIND = {
    "curated": "build-curated-dataset",
    "openfisca": "build-openfisca-dataset",
}


@app.command("selections")
def selections_cmd() -> None:
    """List the golden selections (eval.golden_selections): country, kind, entries, last update."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        rows = golden_store.list_selections(conn)
    if not rows:
        typer.echo("No golden selections yet (selection-import <file>, or import-golden for the old files).")
        return
    for row in rows:
        typer.echo(
            f"{row['country']}  {row['kind']:<9} entries={row['entries']:<4}"
            f" updated={row['updated_at']:%Y-%m-%d %H:%M} by {row['updated_by']}"
        )


def _selection_kind_or_exit(conn, country: str, kind: str | None) -> str:
    """The kind to act on: the one given, else the single kind the country
    has; two kinds and none given is an error, not a guess."""
    if kind is not None:
        if kind not in golden_store.SELECTION_KINDS:
            typer.echo(f"--kind must be one of {', '.join(golden_store.SELECTION_KINDS)}, not {kind!r}")
            raise typer.Exit(2)
        return kind
    kinds = golden_store.selection_kinds(conn, country)
    if len(kinds) == 1:
        return kinds[0]
    if not kinds:
        typer.echo(f"no golden selection for {country.upper()} in eval.golden_selections")
    else:
        typer.echo(f"{country.upper()} has both a {' and a '.join(kinds)} selection — say which with --kind")
    raise typer.Exit(1)


@app.command("selection-export")
def selection_export(
    country: str = typer.Argument(..., help="ISO country code, e.g. ES"),
    kind: str = typer.Option(None, "--kind", help="curated | openfisca (default: the one kind the country has)"),
    out: Path = typer.Option(None, "--out", help="Write to this file instead of stdout"),
) -> None:
    """Write a golden selection row as the JSON file it used to be (golden_sources/<cc>.json).

    The header keys come first, `"entries"` last — edit the file, then
    `selection-import` it and rebuild the country's cases.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        resolved = _selection_kind_or_exit(conn, country, kind)
        header, entries = _selection_or_exit(conn, country, resolved)
    text = json.dumps(golden_store.selection_document(header, entries), indent=2, ensure_ascii=False) + "\n"
    if out is None:
        typer.echo(text, nl=False)
        return
    out.write_text(text, encoding="utf-8")
    typer.echo(f"{country.upper()} {resolved} selection ({len(entries)} entries) -> {out}")


@app.command("selection-import")
def selection_import(
    file: Path = typer.Argument(..., help='A selection JSON file (header keys + "entries")'),
    country: str = typer.Option(None, "--country", help="Override the country the file states"),
    kind: str = typer.Option(None, "--kind", help="curated | openfisca (default: the file's `corpus`, else its name)"),
) -> None:
    """Upsert a selection file into eval.golden_selections, then rebuild.

    Country and kind are read from the header (`country`, `corpus`) the way
    `import-golden` read golden_sources/ files, with the filename as fallback
    (`openfisca_fr.json` -> FR, openfisca). The cases are NOT rebuilt here:
    run the builder the reminder names, and read every skip it prints.
    """
    if not file.exists():
        typer.echo(f"no selection file at {file}")
        raise typer.Exit(1)
    try:
        doc = json.loads(file.read_text(encoding="utf-8"))
    except ValueError as exc:
        typer.echo(f"{file} is not valid JSON: {exc}")
        raise typer.Exit(1) from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("entries", []), list):
        typer.echo(f"{file} must be a JSON object with an `entries` list")
        raise typer.Exit(1)
    try:
        inferred_country, inferred_kind = golden_store.selection_identity(doc, str(file))
    except ValueError as exc:
        typer.echo(f"{exc} — pass --country")
        raise typer.Exit(1) from exc
    country = (country or inferred_country).upper()
    kind = kind or inferred_kind
    if kind not in golden_store.SELECTION_KINDS:
        typer.echo(f"--kind must be one of {', '.join(golden_store.SELECTION_KINDS)}, not {kind!r}")
        raise typer.Exit(2)
    header = {k: v for k, v in doc.items() if k != "entries"}
    entries = list(doc.get("entries", []))

    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        golden_store.save_selection(conn, country, kind, header, entries)
    typer.echo(
        f"{country} {kind} selection: {len(entries)} entries -> eval.golden_selections.\n"
        f"  the cases are not rebuilt yet — run:\n"
        f"  nomokrisis-eval {_REBUILD_FOR_KIND[kind]} --country {country} --year <YYYY>"
    )
    emit_result({"country": country, "kind": kind, "entries": len(entries)})


@app.command("label-cases")
def label_cases(
    country: list[str] = typer.Option(None, "--country"),
    apply: bool = typer.Option(False, "--apply", help="Write the proposals into the cases"),
) -> None:
    """Draft a difficulty rung + hazard flags for each golden case, for review.

    Prints one line per case with the proposal and the reason for it, then a
    per-bucket count. Nothing is written without --apply, and even then only
    `difficulty`/`hazards` change: labels are metadata about a case, not ground
    truth about its value, so a human `verified` flag survives untouched
    (golden_store.save_case never writes the verdict columns).

    A label you disagree with belongs in the selection (eval.golden_selections,
    as `difficulty` / `hazards` on the entry) — the builders prefer an explicit
    entry value over anything drafted here, so a rebuild will not undo your
    correction.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        cases = golden_store.load_cases(conn, countries=country or None)
        if not cases:
            typer.echo("No golden cases found.")
            return

        changed: list[tuple[GoldenCase, DraftedLabels]] = []
        locked: list[GoldenCase] = []
        buckets: Counter[str] = Counter()
        hazard_counts: Counter[str] = Counter()
        for case in sorted(cases, key=lambda c: c.id):
            # temporal_basis lives on the parameter record, not on the case.
            try:
                basis = load_case_record(conn, case.parameter_target).information.temporal_basis
            except (KeyError, ValueError):
                conn.rollback()
                basis = None
            drafted = draft_labels(
                value=case.expected.value,
                citations=case.expected.citations,
                temporal_basis=basis,
                is_bracket_table=isinstance(case.expected.value, list),
            )
            buckets[drafted.difficulty] += 1
            for hazard in drafted.hazards:
                hazard_counts[hazard] += 1
            if not case.labels_drafted:
                mark = "="  # a human set this in the selection; the draft is FYI only
            elif (case.difficulty, case.hazards) == (drafted.difficulty, drafted.hazards):
                mark = " "
            else:
                mark = "*"
            flags = f" +{','.join(drafted.hazards)}" if drafted.hazards else ""
            typer.echo(f"{mark} {case.id:<52} {case.difficulty or '-':<9} -> {drafted.difficulty:<9}{flags}")
            for reason in drafted.reasons:
                typer.echo(f"      · {reason}")
            if mark == "*":
                changed.append((case, drafted))
            elif mark == "=" and (case.difficulty, case.hazards) != (drafted.difficulty, drafted.hazards):
                locked.append(case)

        typer.echo(
            "\ndifficulty: "
            + "  ".join(f"{k}={v}" for k, v in sorted(buckets.items()))
            + "\nhazards:    "
            + ("  ".join(f"{k}={v}" for k, v in sorted(hazard_counts.items())) or "none")
        )
        # The drafter can see three hazards and is blind to three others; say so,
        # so a reviewer knows the flag list is a floor rather than a verdict.
        typer.echo("not drafted (a human has to add these): mid_year_change, unit_conversion, budget_act_window")

        if locked:
            typer.echo(
                f"\n{len(locked)} case(s) marked '=' keep a label set by hand in "
                "the selection and are left alone: " + ", ".join(c.id for c in locked)
            )
        if not changed:
            typer.echo("\nevery case already carries its drafted label.")
            return
        if not apply:
            typer.echo(f"\n{len(changed)} case(s) would change (*). Re-run with --apply to write them.")
            return
        for case, drafted in changed:
            case.difficulty = drafted.difficulty
            case.hazards = list(drafted.hazards)
            golden_store.save_case(conn, case)
        typer.echo(f"\nwrote {len(changed)} case(s); `verified` untouched.")
