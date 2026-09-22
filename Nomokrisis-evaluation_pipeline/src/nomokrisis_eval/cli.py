"""CLI: build the golden dataset, run evaluations, report KPIs.

  uv run nomokrisis-eval init-db
  uv run nomokrisis-eval import-golden            # once: dataset/, dataset_embedding/, golden_sources/ -> eval.*
  uv run nomokrisis-eval build-openfisca-dataset --year 2025 --country FR
  uv run nomokrisis-eval build-curated-dataset --year 2025 --country IE
  uv run nomokrisis-eval build-dataset notes.md --country FR --as-of 2025-06-01 --target 'euromod://FR/…'
  uv run nomokrisis-eval list-cases
  uv run nomokrisis-eval selections                 # the selection rows (what golden_sources/ used to be)
  uv run nomokrisis-eval selection-export ES --out es.json   # edit the JSON, then:
  uv run nomokrisis-eval selection-import es.json            # ... and rebuild
  uv run nomokrisis-eval run --as-of 2025-06-01 --model anthropic/claude-sonnet-5
  uv run nomokrisis-eval resume            # continue the last interrupted run
  uv run nomokrisis-eval list-runs
  uv run nomokrisis-eval report

Everything lives in the eval schema of the shared Postgres (ADR 0004): there
is no dataset directory, no run directory and no `--no-db`. Commands a worker
job wraps end with one `@result {json}` line on stdout.
"""

from __future__ import annotations

import json
import time
from collections import Counter
from datetime import date
from pathlib import Path

import typer
from nomoscope_workflow import paramdb
from nomoscope_workflow.tracing import set_progress

from . import build_dataset as builder
from . import curated_golden
from . import db as evaldb
from . import golden_store
from . import openfisca_golden
from .config import EvalConfig, load_eval_config
from .import_golden import (
    DEFAULT_DATASET_DIR,
    DEFAULT_EMBEDDING_DATASET_DIR,
    DEFAULT_SOURCES_DIR,
    import_golden,
)
from .labels import DraftedLabels, draft_labels
from .runner import (
    execute_run,
    latest_incomplete_run,
    list_runs,
    load_case_record,
    rescore_run,
    resume_run,
    start_run,
    store_rescored,
    summarize,
)
from .schema import CaseResult, GoldenCase, RunManifest

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _result(payload: dict) -> None:
    """The one `@result` line a worker job parses (contracts.md)."""
    typer.echo("@result " + json.dumps(payload))


def _progress(payload: dict) -> None:
    typer.echo("@progress " + json.dumps(payload))


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
    _result(
        {
            "selections": report.selections,
            "cases": report.cases,
            "embedding_cases": report.embedding_cases,
            "unresolved": len(report.unresolved),
            "dry_run": dry_run,
        }
    )


# --------------------------------------------------------------------------- #
# Building the golden set
# --------------------------------------------------------------------------- #


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
    language: str = typer.Option(None, "--language", help="Source-legislation language (default: country code lowercased)"),
    target: list[str] = typer.Option(
        None, "--target",
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
        targets = list(target or [])
        if not targets:
            targets = [
                row[0] for row in conn.execute(
                    "SELECT model_target FROM params.parameters WHERE country = %s ORDER BY spine_order, model_target",
                    (country.upper(),),
                ).fetchall()
            ]
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
            drafting_model, source_text, records, _parse_date(as_of), (language or country).lower()
        )
        written = 0
        for case, message in results:
            typer.echo(message)
            if case is not None and case.country.upper() == country.upper():
                reset = golden_store.save_drafted_case(conn, case)
                typer.echo(f"  -> {case.id} ({'verdict reset — ' if reset else ''}review before freezing)")
                written += 1
    typer.echo(f"{written} draft case(s) written to eval.golden_cases. Review them in the UI's Golden set tab.")
    _result({"written": written})


@app.command("build-openfisca-dataset")
def build_openfisca_dataset(
    year: int = typer.Option(..., "--year", help="EUROMOD system year to draft cases for, e.g. 2025"),
    country: str = typer.Option(..., "--country", help="ISO country code"),
    as_of: str = typer.Option(
        None, "--as-of", help="Anchor date inside the system year (default: <year>-06-01)"
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
    anchor = _parse_date(as_of) if as_of else date(year, 6, 1)
    with evaldb.connect(cfg.database_url) as conn:
        header, entries = _selection_or_exit(conn, country, "openfisca")
        outcomes = openfisca_golden.build_dataset(
            conn, header, entries, anchor,
            country=country.upper(), limit=limit, fill_from_links=fill,
        )
    written = _echo_outcomes(outcomes, 10)
    typer.echo(
        f"\n{written} draft case(s) in eval.golden_cases. "
        "Review them in the UI's Golden set tab (or `nomokrisis-eval verify <id>`) before running an evaluation."
    )
    _result({"written": written})


@app.command("build-curated-dataset")
def build_curated_dataset(
    year: int = typer.Option(..., "--year", help="EUROMOD system year to draft cases for, e.g. 2025"),
    country: str = typer.Option(..., "--country", help="ISO country code, e.g. IE"),
    as_of: str = typer.Option(
        None, "--as-of", help="Anchor date inside the system year (default: <year>-06-01)"
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
    anchor = _parse_date(as_of) if as_of else date(year, 6, 1)
    with evaldb.connect(cfg.database_url) as conn:
        header, entries = _selection_or_exit(conn, country, "curated")
        outcomes = curated_golden.build_dataset(
            conn, header, entries, anchor, country=country.upper(),
            selection_name=f"{country.lower()}.json",
        )
    written = _echo_outcomes(outcomes, 20)
    typer.echo(
        f"\n{written} draft case(s) in eval.golden_cases. "
        "Review them in the UI's Golden set tab (or `nomokrisis-eval verify <id>`) before running an evaluation."
    )
    _result({"written": written})


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
            typer.echo(
                f"  {'verified' if case.verified else 'unverified'} {case_id} by {case.reviewed_by}"
            )


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
            f"{flag:<8} {case.country} {case.language} as_of={case.as_of} "
            f"routing={case.expected.routing:<12} {case.id}"
        )
    typer.echo(f"{len(cases)} case(s), golden_set_hash={golden_store.golden_set_hash(cases)}")


# --------------------------------------------------------------------------- #
# Golden selections: the row is edited as a file, then written back
# --------------------------------------------------------------------------- #

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
        typer.echo(
            f"{country.upper()} has both a {' and a '.join(kinds)} selection — say which with --kind"
        )
    raise typer.Exit(1)


@app.command("selection-export")
def selection_export(
    country: str = typer.Argument(..., help="ISO country code, e.g. ES"),
    kind: str = typer.Option(
        None, "--kind", help="curated | openfisca (default: the one kind the country has)"
    ),
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
    file: Path = typer.Argument(..., help="A selection JSON file (header keys + \"entries\")"),
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
    _result({"country": country, "kind": kind, "entries": len(entries)})


# --------------------------------------------------------------------------- #
# Running
# --------------------------------------------------------------------------- #


@app.command()
def run(
    as_of: str = typer.Option(..., "--as-of", help="Reference date, YYYY-MM-DD"),
    model: str = typer.Option(..., "--model", help="Provider-prefixed model, e.g. anthropic/claude-sonnet-5 or mock/extractor"),
    country: list[str] = typer.Option(None, "--country", help="Restrict to country code(s)"),
    language: list[str] = typer.Option(None, "--language", help="Restrict to language(s)"),
    verified_only: bool = typer.Option(True, "--verified-only/--include-drafts", help="Evaluate only human-verified cases"),
    notes: str = typer.Option(None, "--notes"),
    verbose: bool = typer.Option(
        False, "--verbose/--quiet", "-v", help="Also mirror every workflow step of every case"
    ),
) -> None:
    """Run the agentic workflow over the golden set, score it, store the results.

    Progress is printed case by case, and every scored case is written to
    eval.results as it lands: a Ctrl-C (or a crash) is picked up again with
    `nomokrisis-eval resume`. Ends with `@result {"run_id": …}`.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        cases = golden_store.load_cases(
            conn, countries=country or None, languages=language or None, verified_only=verified_only
        )
        if not cases:
            typer.echo("No matching golden cases (try --include-drafts).")
            raise typer.Exit(1)
        manifest = start_run(conn, cfg, cases, _parse_date(as_of), model, notes=notes)
        typer.echo(
            f"run {manifest.run_id}  model={manifest.model}  as_of={manifest.as_of}"
            f"  dataset={manifest.dataset_version}  cases={len(cases)}"
        )
        _execute_and_report(conn, cfg, manifest, cases, [], verbose=verbose)


@app.command("list-runs")
def list_runs_cmd(
    limit: int = typer.Option(20, "--limit"),
    incomplete_only: bool = typer.Option(False, "--incomplete-only", help="Only runs left unfinished"),
) -> None:
    """Evaluation runs in eval.runs, newest first, with their progress."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        runs = [r for r in list_runs(conn) if not incomplete_only or not r["complete"]][:limit]
    if not runs:
        typer.echo("No evaluation runs yet.")
        return
    for entry in runs:
        manifest: RunManifest = entry["manifest"]
        total = entry["total"] or "?"
        typer.echo(
            f"{manifest.created_at:%Y-%m-%d %H:%M}  {manifest.model:<34}"
            f"  {entry['done']}/{total:<5} {entry['status']:<10} {manifest.run_id}"
        )


@app.command()
def resume(
    run_id: str = typer.Argument(None, help="Run id to continue (default: the most recent unfinished run)"),
    verbose: bool = typer.Option(
        False, "--verbose/--quiet", "-v", help="Also mirror every workflow step of every case"
    ),
) -> None:
    """Continue an interrupted evaluation run: same manifest, same case list,
    only the cases that have not been scored yet. Ends with `@result {"run_id": …}`."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        if run_id is None:
            candidate = latest_incomplete_run(conn)
            if candidate is None:
                typer.echo("No unfinished evaluation run in eval.runs.")
                raise typer.Exit(1)
            run_id = candidate["run_id"]
        try:
            manifest, cases, done = resume_run(conn, run_id)
        except (LookupError, ValueError) as exc:
            typer.echo(f"cannot resume: {exc}")
            raise typer.Exit(1) from exc

        current = golden_store.golden_set_hash(golden_store.load_cases(conn, verified_only=True))
        if current != manifest.dataset_version:
            typer.echo(
                f"! golden set is {current} today, this run froze {manifest.dataset_version}; "
                "replaying the run's frozen case list"
            )
        typer.echo(
            f"resuming {manifest.run_id}  model={manifest.model}  as_of={manifest.as_of}"
            f"  {len(done)}/{len(cases)} already scored"
        )
        _execute_and_report(conn, cfg, manifest, cases, done, verbose=verbose)


_MARK = {True: "\u2713", False: "\u2717", None: "\u00b7"}


def _fmt_duration(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h{minutes:02d}m" if hours else f"{minutes:d}m{secs:02d}s"


def _result_line(result: CaseResult) -> str:
    if result.error:
        return f"ERROR       {result.error[:90]}"
    marks = " ".join(
        f"{label}{_MARK[value]}"
        for label, value in (
            ("routing", result.routing_correct),
            ("value", result.value_correct),
            ("date", result.date_correct),
            ("cite", result.citation_correct),
        )
    )
    flag = "  HALLUCINATION" if result.hallucination else ""
    return f"{(result.routing_actual or '?'):<11} {marks}{flag}"


def _progress_callbacks(verbose: bool):
    """Print one line per case: `[ 7/42] <case id> routing... 4.1s eta 2m38s`.

    Quiet (the default) writes the prefix before the case runs — so a long LLM
    call shows what it is waiting on — and completes it in place once the case
    is scored. Verbose lets the workflow mirror its own steps in between, so the
    prefix and the outcome are printed as two separate lines.
    """
    state = {"start": time.perf_counter(), "completed": 0}

    def on_case_start(index: int, total: int, case: GoldenCase) -> None:
        typer.echo(f"[{index:>3}/{total}] {case.id:<46} ", nl=verbose)

    def on_case_done(index: int, total: int, case: GoldenCase, result: CaseResult) -> None:
        state["completed"] += 1
        elapsed = time.perf_counter() - state["start"]
        eta = elapsed / state["completed"] * (total - index)
        prefix = f"[{index:>3}/{total}] {case.id:<46} " if verbose else ""
        typer.echo(
            f"{prefix}{_result_line(result)}  {(result.latency_ms or 0) / 1000:5.1f}s"
            f"  eta {_fmt_duration(eta)}"
        )

    return on_case_start, on_case_done


def _execute_and_report(
    conn,
    cfg: EvalConfig,
    manifest: RunManifest,
    cases: list[GoldenCase],
    done: list[CaseResult],
    verbose: bool = False,
) -> None:
    """Score the pending cases with live progress, then summarize."""
    set_progress(verbose)  # per-step workflow chatter would drown the per-case lines
    on_case_start, on_case_done = _progress_callbacks(verbose)

    def on_done(index: int, total: int, case: GoldenCase, result: CaseResult) -> None:
        on_case_done(index, total, case, result)
        _progress({"done": index, "total": total, "case": case.id, "run_id": manifest.run_id})

    try:
        results = execute_run(
            conn, cfg, manifest, cases, done,
            on_case_start=on_case_start, on_case_done=on_done,
        )
    except KeyboardInterrupt:
        scored = len(evaldb.load_results(conn, evaldb.load_run(conn, manifest.run_id)[0]))
        typer.echo(
            f"\ninterrupted after {scored}/{len(cases)} case(s) — nothing lost.\n"
            f"  resume with: nomokrisis-eval resume {manifest.run_id}"
        )
        _result({"run_id": manifest.run_id, "status": "running"})
        raise typer.Exit(130) from None

    typer.echo(f"\nrun {manifest.run_id}  model={manifest.model}  dataset={manifest.dataset_version}")
    for lang, kpis in summarize(results).items():
        pretty = "  ".join(f"{k}={v}" for k, v in kpis.items())
        typer.echo(f"  [{lang}] {pretty}")
    typer.echo(f"stored in Postgres: run_id={manifest.run_id} (eval.runs / eval.results)")
    _result({"run_id": manifest.run_id})


@app.command("list-embedding-cases")
def list_embedding_cases(
    country: list[str] = typer.Option(None, "--country"),
    verified_only: bool = typer.Option(False, "--verified-only"),
) -> None:
    """List the embedding (retrieval) evaluation set (eval.embedding_cases)."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        cases = golden_store.load_embedding_cases(
            conn, countries=country or None, verified_only=verified_only
        )
    for case in cases:
        flag = "✓" if case.verified else "draft"
        corpus = case.corpus_lang or case.language
        xling = f"{case.language}→{corpus}" if corpus != case.language else case.language
        typer.echo(
            f"{flag:<6} {case.country} {xling:<6} as_of={case.as_of} "
            f"expects={'; '.join(case.expected_citations)}  {case.id}"
        )
    typer.echo(
        f"{len(cases)} case(s), dataset_version={golden_store.embedding_set_hash(cases)}"
    )


@app.command("run-embeddings")
def run_embeddings(
    country: list[str] = typer.Option(None, "--country", help="Restrict to country code(s)"),
    language: list[str] = typer.Option(None, "--language", help="Restrict to query language(s)"),
    k: int = typer.Option(10, "--k", help="Rank cutoff for hit@k / MRR"),
    embedding_model_id: int = typer.Option(
        1, "--embedding-model-id",
        help="embeddings.model_id to evaluate (1 = BGE-M3; 99 = in-SQL placeholder demo embedder, no encoder needed)",
    ),
    verified_only: bool = typer.Option(
        False, "--verified-only/--include-drafts",
        help="Restrict to human-verified cases (drafts included by default — this eval is diagnostic, not the contractual KPI freeze)",
    ),
    notes: str = typer.Option(None, "--notes"),
) -> None:
    """Rank each case's ground-truth chunks under fts / vector / hybrid search."""
    from .embedding_eval import run_embedding_eval, summarize_embedding

    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        cases = golden_store.load_embedding_cases(
            conn,
            countries=country or None,
            languages=language or None,
            verified_only=verified_only,
        )
    if not cases:
        typer.echo("No matching embedding cases.")
        raise typer.Exit(1)

    manifest, results = run_embedding_eval(
        cfg, cases, k=k, embedding_model_id=embedding_model_id, notes=notes
    )
    with evaldb.connect(cfg.database_url) as conn:
        evaldb.insert_embedding_run(conn, manifest, results)

    def fmt_rank(result, method) -> str:
        if method not in result.ranks:
            return "-"
        rank = result.ranks[method]
        return f"#{rank}" if rank is not None else "miss"

    typer.echo(f"run {manifest['run_id']}  model_id={embedding_model_id}  k={k}")
    for result in results:
        legs = "  ".join(f"{m}={fmt_rank(result, m):<5}" for m in ("fts", "vector", "hybrid"))
        pool = (
            f"({result.embedded_chunks}/{result.candidate_chunks} embedded)"
            if result.candidate_chunks is not None
            else ""
        )
        suffix = f"  ERROR {result.error}" if result.error else ""
        typer.echo(f"  {result.case_id:<32} {legs} {pool}{suffix}")

    for lang, methods in summarize_embedding(results).items():
        typer.echo(f"  [{lang}]")
        for method, metrics in methods.items():
            pretty = "  ".join(f"{k_}={v}" for k_, v in metrics.items()) or "not scored"
            typer.echo(f"    {method:<7} {pretty}")
    typer.echo(f"stored in Postgres: eval.embedding_runs run_id={manifest['run_id']}")
    _result({"run_id": manifest["run_id"]})


@app.command()
def rescore(
    run_id: str = typer.Argument(..., help="Run id to re-score under the current scoring rules"),
    write: bool = typer.Option(False, "--write", help="Persist the new scores into eval.results"),
) -> None:
    """Re-apply today's scoring to a finished run's stored ReviewItems.

    Costs nothing — no LLM calls, no retrieval — so a scoring fix can be checked
    against past runs. Expectations come from the run's frozen case list, so
    what you see is the effect of the SCORING change alone; to measure a
    golden-set change, start a new run. Dry-run by default.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        try:
            manifest, previous, results = rescore_run(conn, run_id)
        except LookupError as exc:
            typer.echo(str(exc))
            raise typer.Exit(1) from exc
        before = summarize(previous)
        after = summarize(results)

        typer.echo(f"run {manifest.run_id}  model={manifest.model}  cases={len(results)}")
        for key in sorted(set(before) | set(after)):
            old_kpis, new_kpis = before.get(key, {}), after.get(key, {})
            changes = [
                f"{k}: {old_kpis.get(k, '-')} -> {v}"
                for k, v in new_kpis.items()
                if old_kpis.get(k) != v
            ]
            typer.echo(f"  [{key}] " + ("  ".join(changes) if changes else "unchanged"))

        if not write:
            typer.echo("\ndry run — pass --write to persist")
            return
        store_rescored(conn, run_id, results)
    typer.echo(f"rescored results stored in Postgres: run_id={manifest.run_id}")


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
            typer.echo(
                f"{mark} {case.id:<52} {case.difficulty or '-':<9} -> {drafted.difficulty:<9}{flags}"
            )
            for reason in drafted.reasons:
                typer.echo(f"      · {reason}")
            if mark == "*":
                changed.append((case, drafted))
            elif mark == "=" and (case.difficulty, case.hazards) != (drafted.difficulty, drafted.hazards):
                locked.append(case)

        typer.echo(
            "\ndifficulty: " + "  ".join(f"{k}={v}" for k, v in sorted(buckets.items()))
            + "\nhazards:    " + ("  ".join(f"{k}={v}" for k, v in sorted(hazard_counts.items())) or "none")
        )
        # The drafter can see three hazards and is blind to three others; say so,
        # so a reviewer knows the flag list is a floor rather than a verdict.
        typer.echo(
            "not drafted (a human has to add these): mid_year_change, unit_conversion, "
            "budget_act_window"
        )

        if locked:
            typer.echo(
                f"\n{len(locked)} case(s) marked '=' keep a label set by hand in "
                "the selection and are left alone: "
                + ", ".join(c.id for c in locked)
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


@app.command()
def report(
    run_id: str = typer.Option(None, "--run-id", help="Restrict to one run"),
    limit: int = typer.Option(20, "--limit"),
) -> None:
    """KPI summary per (run, language) from Postgres (view eval.run_summary)."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        rows = evaldb.fetch_summary(conn, run_id=run_id, limit=limit)
        run_pks = sorted({r["run_pk"] for r in rows})
        by_difficulty = evaldb.fetch_difficulty(conn, run_pks)
        by_hazard = evaldb.fetch_hazards(conn, run_pks)
    if not rows:
        typer.echo("No evaluation runs stored yet.")
        return
    def pct(value) -> str:
        return "-" if value is None else f"{value}%"

    def impact(row) -> str:
        if row.get("energy_kwh") is None:
            return "  energy=n/a"  # model absent from the EcoLogits registry
        return (
            f"  energy={row['energy_kwh'] * 1000:.1f}Wh"
            f"  co2={row['gwp_kgco2eq'] * 1000:.1f}g"
        )

    def readiness(row) -> str:
        """The golden-set caveat, printed only when it applies: how many cases
        cannot measure a model at all, and what the KPIs look like without them.

        Two distinct gaps, because they take different work to close — ingest
        the act, versus record where the answer lives."""
        no_corpus = row.get("cases_no_corpus") or 0
        undocumented = row.get("cases_undocumented") or 0
        if not (no_corpus + undocumented):
            return ""
        reasons = []
        if no_corpus:
            reasons.append(f"{no_corpus} source not in corpus")
        if undocumented:
            reasons.append(f"{undocumented} no ground-truth citation")
        return (
            f"\n      not ready ({', '.join(reasons)}) — over the ready cases:"
            f"  routing={pct(row['routing_pct_ready'])}"
            f"  value={pct(row['value_pct_ready'])}"
            f"  citation={pct(row['citation_pct_ready'])}"
        )

    def guidance(row) -> str:
        """What share of this run's proposals rested on guidance alone.

        Printed only when it happened. Not a quality figure — it is the data
        the "guidance ranks equal to legislation" decision is to be revisited
        on (ADR 0001).
        """
        cases = row.get("guidance_only_cases") or 0
        if not cases:
            return ""
        return f"  guidance_only={cases} ({pct(row.get('guidance_only_pct'))})"

    def breakdown(row, label: str, source: list[dict], key: str) -> str:
        """One indented line per bucket, ready cases only. Silent when a single
        bucket holds everything — a lone rung compares with nothing."""
        buckets = [
            b for b in source
            if b["run_pk"] == row["run_pk"] and b["language"] == row["language"]
        ]
        if len(buckets) < 2 and label == "difficulty":
            return ""
        return "".join(
            f"\n      {label + ' ' + b[key]:<27} n={b['cases']:<3}"
            f"  routing={pct(b['routing_pct'])}  value={pct(b['value_pct'])}"
            f"  recall={pct(b['retrieval_recall_pct'])}"
            for b in buckets
        )

    for row in rows:
        abstentions = row.get("abstentions") or 0
        rejections = row.get("rejections") or 0
        typer.echo(
            f"{row['created_at']:%Y-%m-%d %H:%M}  {row['model_provider']}/{row['model_name']}"
            f"  [{row['language']}/{row['country']}]  cases={row['cases']}"
            f"  routing={pct(row['routing_pct'])}  value={pct(row['value_pct'])}  date={pct(row['date_pct'])}"
            f"  citation={pct(row['citation_pct'])}  verbatim={pct(row['extract_verbatim_pct'])}"
            f"  supported={pct(row['supportedness_pct'])}  critique={pct(row['critique_pass_pct'])}"
            f"  halluc={pct(row['hallucination_pct'])}  recall={pct(row['retrieval_recall_pct'])}"
            f"  abstained={abstentions}  rejected={rejections}"
            f"{guidance(row)}"
            f"{impact(row)}"
            f"  {row['run_id']}"
            f"{readiness(row)}"
            f"{breakdown(row, 'difficulty', by_difficulty, 'difficulty')}"
            f"{breakdown(row, 'hazard', by_hazard, 'hazard')}"
        )


if __name__ == "__main__":
    app()
