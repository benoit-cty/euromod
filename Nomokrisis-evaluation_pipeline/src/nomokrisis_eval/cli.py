"""CLI: build the golden dataset, run evaluations, report KPIs.

  uv run nomokrisis-eval init-db
  uv run nomokrisis-eval build-dataset docs/fr_country_report_excerpt.md --country FR --as-of 2025-06-01
  uv run nomokrisis-eval list-cases
  uv run nomokrisis-eval run --as-of 2025-06-01 --model anthropic/claude-sonnet-5
  uv run nomokrisis-eval resume            # continue the last interrupted run
  uv run nomokrisis-eval list-runs
  uv run nomokrisis-eval report
"""

from __future__ import annotations

import json
import time
from collections import Counter
from datetime import date
from pathlib import Path

import typer
from nomoscope_workflow.queue_store import load_record
from nomoscope_workflow.tracing import set_progress

from . import build_dataset as builder
from . import curated_golden
from . import db as evaldb
from . import openfisca_golden
from .config import REPO_ROOT, EvalConfig, load_eval_config
from .dataset import dataset_version, load_cases, load_embedding_cases, save_case
from .labels import DraftedLabels, draft_labels
from .runner import (
    RESULTS_FILENAME,
    execute_run,
    latest_incomplete_run,
    list_runs,
    load_partial_results,
    rescore_run,
    resume_run,
    run_directory,
    rewrite_partial,
    start_run,
    summarize,
)
from .schema import CaseResult, GoldenCase, RunManifest

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


@app.command("init-db")
def init_db() -> None:
    """Create the eval schema (tables + summary view) in the legislation DB."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        evaldb.apply_schema(conn)
    typer.echo(f"eval schema applied to {cfg.database_url}")


@app.command("build-dataset")
def build_dataset_cmd(
    source_file: Path = typer.Argument(..., help="Trusted source document (country report excerpt, notes)"),
    country: str = typer.Option(..., "--country", help="ISO country code, e.g. FR"),
    as_of: str = typer.Option(..., "--as-of", help="Reference date, YYYY-MM-DD"),
    language: str = typer.Option(None, "--language", help="Source-legislation language (default: country code lowercased)"),
    params_dir: Path = typer.Option(
        None, "--params-dir", help="Directory of Activity 1 parameter JSON files (default: Nomoscope-agentic-workflow/data/parameters)"
    ),
    model: str = typer.Option(None, "--model", help="Drafting model (default: EVAL_BUILDER_MODEL, claude-fable-5)"),
) -> None:
    """Draft golden cases with Claude (verified=false until a human confirms them)."""
    cfg = load_eval_config()
    from .config import REPO_ROOT

    folder = params_dir or REPO_ROOT / "Nomoscope-agentic-workflow" / "data" / "parameters"
    files = sorted(p for p in folder.glob("*.json*") if p.suffix in (".json", ".jsonc"))
    if not files:
        typer.echo(f"No parameter files in {folder}")
        raise typer.Exit(1)

    results = builder.build_cases(
        model or cfg.builder_model,
        source_file,
        files,
        _parse_date(as_of),
        (language or country).lower(),
    )
    written = 0
    for case, message in results:
        typer.echo(message)
        if case is not None and case.country.upper() == country.upper():
            path = save_case(cfg.dataset_dir, case)
            typer.echo(f"  -> {path} (verified=false — review before freezing)")
            written += 1
    typer.echo(f"{written} draft case(s) written. Review them, set verified=true, commit to git.")


@app.command("build-openfisca-dataset")
def build_openfisca_dataset(
    year: int = typer.Option(..., "--year", help="EUROMOD system year to draft cases for, e.g. 2025"),
    country: str = typer.Option("FR", "--country", help="ISO country code"),
    source: Path = typer.Option(
        None, "--source", help="Curated selection file (default: golden_sources/openfisca_<cc>.json)"
    ),
    limit: int = typer.Option(50, "--limit", help="Maximum number of cases to write"),
    fill: bool = typer.Option(
        True, "--fill/--curated-only", help="Top the set up from params.parameter_links suggestions"
    ),
    as_of: str = typer.Option(
        None, "--as-of", help="Anchor date inside the system year (default: <year>-06-01)"
    ),
) -> None:
    """Draft golden cases from the ingested OpenFisca corpus (verified=false).

    Ground truth comes from OpenFisca's curated per-date values and legal
    references; routing is computed deterministically against what EUROMOD
    holds. Review each case in the UI's Golden set tab before it counts.
    """
    cfg = load_eval_config()
    from .config import EVAL_ROOT

    selection = source or EVAL_ROOT / "golden_sources" / f"openfisca_{country.lower()}.json"
    if not selection.exists():
        typer.echo(f"no selection file at {selection} — pass --source or use --curated-only")
        selection = None
    anchor = _parse_date(as_of) if as_of else date(year, 6, 1)
    with evaldb.connect(cfg.database_url) as conn:
        outcomes = openfisca_golden.build_dataset(
            conn, cfg.dataset_dir, selection, anchor,
            country=country.upper(), limit=limit, fill_from_links=fill,
        )
    written = 0
    for outcome in outcomes:
        label = outcome.entry.get("model_target") or outcome.entry.get("parameter_file", "?")
        if outcome.case is None:
            typer.echo(f"  ~ skipped {label}: {outcome.skipped}")
            # A skip can retire a case the previous run wrote; never silently.
            for warning in outcome.warnings:
                typer.echo(f"    ! {warning}")
            continue
        written += 1
        expected = outcome.case.expected
        typer.echo(
            f"  {expected.routing:<10} {outcome.case.id}"
            f"  value={expected.value}  valid_from={expected.valid_from}"
            f"  citations={expected.citations or '[]'}"
        )
    typer.echo(
        f"\n{written} draft case(s) in {cfg.dataset_dir} (verified=false). "
        "Review them in the UI's Golden set tab (or `nomokrisis-eval verify <id>`) before running an evaluation."
    )


@app.command("build-curated-dataset")
def build_curated_dataset(
    year: int = typer.Option(..., "--year", help="EUROMOD system year to draft cases for, e.g. 2025"),
    country: str = typer.Option(..., "--country", help="ISO country code, e.g. IE"),
    source: Path = typer.Option(
        None, "--source", help="Curated selection file (default: golden_sources/<cc>.json)"
    ),
    as_of: str = typer.Option(
        None, "--as-of", help="Anchor date inside the system year (default: <year>-06-01)"
    ),
) -> None:
    """Draft golden cases from a hand-curated selection file (verified=false).

    For countries with no external corpus to read ground truth from (IE, LT):
    the expected values are curated in golden_sources/<cc>.json from the acts
    themselves. The parameter under test still comes from the params DB, and
    the selection's routing is cross-checked against what EUROMOD holds.
    """
    cfg = load_eval_config()

    selection = source or curated_golden.selection_path(country)
    if not selection.exists():
        typer.echo(f"no selection file at {selection}")
        raise typer.Exit(1)
    anchor = _parse_date(as_of) if as_of else date(year, 6, 1)
    with evaldb.connect(cfg.database_url) as conn:
        outcomes = curated_golden.build_dataset(
            conn, cfg.dataset_dir, selection, anchor, country=country.upper()
        )
    written = 0
    for outcome in outcomes:
        label = outcome.entry.get("model_target") or outcome.entry.get("group_id", "?")
        if outcome.case is None:
            typer.echo(f"  ~ skipped {label}: {outcome.skipped}")
            for warning in outcome.warnings:
                typer.echo(f"    ! {warning}")
            continue
        written += 1
        expected = outcome.case.expected
        typer.echo(
            f"  {expected.routing:<20} {outcome.case.id}"
            f"  value={expected.value}  valid_from={expected.valid_from}"
            f"  citations={expected.citations or '[]'}"
        )
        for warning in outcome.warnings:
            typer.echo(f"    ! {warning}")
    typer.echo(
        f"\n{written} draft case(s) in {cfg.dataset_dir} (verified=false). "
        "Review them in the UI's Golden set tab (or `nomokrisis-eval verify <id>`) before running an evaluation."
    )


@app.command()
def verify(
    case_ids: list[str] = typer.Argument(..., help="Golden case ids to mark as human-verified"),
    unverify: bool = typer.Option(False, "--unverify", help="Clear the flag instead of setting it"),
    reviewer: str = typer.Option(None, "--reviewer", help="Recorded in the case's notes"),
) -> None:
    """Flip `verified` on golden cases — the human gate before the set counts as ground truth."""
    cfg = load_eval_config()
    cases = {case.id: case for case in load_cases(cfg.dataset_dir)}
    for case_id in case_ids:
        case = cases.get(case_id)
        if case is None:
            typer.echo(f"  ! unknown case {case_id}")
            continue
        case.verified = not unverify
        if reviewer and not unverify:
            case.notes = " | ".join(filter(None, [case.notes, f"verified by {reviewer}"]))
        save_case(cfg.dataset_dir, case)
        typer.echo(f"  {'verified' if case.verified else 'unverified'} {case_id}")


@app.command("list-cases")
def list_cases(
    country: list[str] = typer.Option(None, "--country"),
    verified_only: bool = typer.Option(False, "--verified-only"),
) -> None:
    """List the golden set."""
    cfg = load_eval_config()
    cases = load_cases(cfg.dataset_dir, countries=country or None, verified_only=verified_only)
    for case in cases:
        flag = "✓" if case.verified else "draft"
        typer.echo(
            f"{flag:<6} {case.country} {case.language} as_of={case.as_of} "
            f"routing={case.expected.routing:<12} {case.id}"
        )
    typer.echo(f"{len(cases)} case(s), dataset_version={dataset_version(cfg.dataset_dir)}")


@app.command()
def run(
    as_of: str = typer.Option(..., "--as-of", help="Reference date, YYYY-MM-DD"),
    model: str = typer.Option(..., "--model", help="Provider-prefixed model, e.g. anthropic/claude-sonnet-5 or mock/extractor"),
    country: list[str] = typer.Option(None, "--country", help="Restrict to country code(s)"),
    language: list[str] = typer.Option(None, "--language", help="Restrict to language(s)"),
    verified_only: bool = typer.Option(True, "--verified-only/--include-drafts", help="Evaluate only human-verified cases"),
    no_db: bool = typer.Option(False, "--no-db", help="Skip writing results to Postgres"),
    notes: str = typer.Option(None, "--notes"),
    verbose: bool = typer.Option(
        False, "--verbose/--quiet", "-v", help="Also mirror every workflow step of every case"
    ),
) -> None:
    """Run the agentic workflow over the golden set, score it, store the results.

    Progress is printed case by case, and every scored case is written to the
    run directory as it lands: a Ctrl-C (or a crash) is picked up again with
    `nomokrisis-eval resume`.
    """
    cfg = load_eval_config()
    cases = load_cases(
        cfg.dataset_dir, countries=country or None, languages=language or None, verified_only=verified_only
    )
    if not cases:
        typer.echo("No matching golden cases (try --include-drafts).")
        raise typer.Exit(1)

    manifest = start_run(cfg, cases, _parse_date(as_of), model, notes=notes)
    typer.echo(
        f"run {manifest.run_id}  model={manifest.model}  as_of={manifest.as_of}"
        f"  dataset={manifest.dataset_version}  cases={len(cases)}"
    )
    _execute_and_report(cfg, manifest, cases, [], no_db=no_db, verbose=verbose)


@app.command("list-runs")
def list_runs_cmd(
    limit: int = typer.Option(20, "--limit"),
    incomplete_only: bool = typer.Option(False, "--incomplete-only", help="Only runs left unfinished"),
) -> None:
    """Evaluation runs on disk, newest first, with their progress."""
    cfg = load_eval_config()
    runs = [r for r in list_runs(cfg) if not incomplete_only or not r["complete"]][:limit]
    if not runs:
        typer.echo("No evaluation runs on disk yet.")
        return
    for entry in runs:
        manifest: RunManifest = entry["manifest"]
        state = "complete" if entry["complete"] else "incomplete"
        total = entry["total"] or "?"
        typer.echo(
            f"{manifest.created_at:%Y-%m-%d %H:%M}  {manifest.model:<34}"
            f"  {entry['done']}/{total:<5} {state:<10} {manifest.run_id}"
        )


@app.command()
def resume(
    run_id: str = typer.Argument(None, help="Run id to continue (default: the most recent unfinished run)"),
    no_db: bool = typer.Option(False, "--no-db", help="Skip writing results to Postgres"),
    verbose: bool = typer.Option(
        False, "--verbose/--quiet", "-v", help="Also mirror every workflow step of every case"
    ),
) -> None:
    """Continue an interrupted evaluation run: same manifest, same case list,
    only the cases that have not been scored yet."""
    cfg = load_eval_config()
    if run_id is None:
        candidate = latest_incomplete_run(cfg)
        if candidate is None:
            typer.echo("No unfinished evaluation run in the runs directory.")
            raise typer.Exit(1)
        run_id = candidate["run_id"]
    try:
        manifest, cases, done = resume_run(cfg, run_id)
    except (FileNotFoundError, ValueError) as exc:
        typer.echo(f"cannot resume: {exc}")
        raise typer.Exit(1) from exc

    current = dataset_version(cfg.dataset_dir)
    if current != manifest.dataset_version:
        typer.echo(
            f"! golden set changed since this run started "
            f"({manifest.dataset_version} -> {current}); replaying the run's frozen case list"
        )
    typer.echo(
        f"resuming {manifest.run_id}  model={manifest.model}  as_of={manifest.as_of}"
        f"  {len(done)}/{len(cases)} already scored"
    )
    _execute_and_report(cfg, manifest, cases, done, no_db=no_db, verbose=verbose)


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
    cfg: EvalConfig,
    manifest: RunManifest,
    cases: list[GoldenCase],
    done: list[CaseResult],
    no_db: bool,
    verbose: bool = False,
) -> None:
    """Score the pending cases with live progress, then persist and summarize."""
    set_progress(verbose)  # per-step workflow chatter would drown the per-case lines
    run_dir = run_directory(cfg, manifest.run_id)
    on_case_start, on_case_done = _progress_callbacks(verbose)
    try:
        results = execute_run(
            cfg, manifest, cases, done,
            on_case_start=on_case_start, on_case_done=on_case_done,
        )
    except KeyboardInterrupt:
        scored = len(load_partial_results(run_dir))
        typer.echo(
            f"\ninterrupted after {scored}/{len(cases)} case(s) — nothing lost.\n"
            f"  resume with: nomokrisis-eval resume {manifest.run_id}"
        )
        raise typer.Exit(130) from None

    # Run manifest + full results on disk (reproducibility, per 04_activity4_validation.md)
    (run_dir / RESULTS_FILENAME).write_text(
        json.dumps([r.model_dump(mode="json") for r in results], indent=2), encoding="utf-8"
    )

    if not no_db:
        with evaldb.connect(cfg.database_url) as conn:
            evaldb.apply_schema(conn)
            evaldb.insert_run(conn, manifest, results)
        typer.echo(f"stored in Postgres: run_id={manifest.run_id}")

    typer.echo(f"\nrun {manifest.run_id}  model={manifest.model}  dataset={manifest.dataset_version}")
    for lang, kpis in summarize(results).items():
        pretty = "  ".join(f"{k}={v}" for k, v in kpis.items())
        typer.echo(f"  [{lang}] {pretty}")
    typer.echo(f"\nmanifest + per-case results: {run_dir}")


@app.command("list-embedding-cases")
def list_embedding_cases(
    country: list[str] = typer.Option(None, "--country"),
    verified_only: bool = typer.Option(False, "--verified-only"),
) -> None:
    """List the embedding (retrieval) evaluation set."""
    cfg = load_eval_config()
    cases = load_embedding_cases(
        cfg.embedding_dataset_dir, countries=country or None, verified_only=verified_only
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
        f"{len(cases)} case(s), dataset_version={dataset_version(cfg.embedding_dataset_dir)}"
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
    cases = load_embedding_cases(
        cfg.embedding_dataset_dir,
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

    run_dir = cfg.runs_dir / manifest["run_id"]
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (run_dir / "results.json").write_text(
        json.dumps([r.model_dump(mode="json") for r in results], indent=2), encoding="utf-8"
    )

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
    typer.echo(f"\nmanifest + per-case results: {run_dir}")


@app.command()
def rescore(
    run_id: str = typer.Argument(..., help="Run id to re-score under the current scoring rules"),
    write: bool = typer.Option(
        False, "--write", help="Persist the new scores (results.json/.jsonl, and Postgres)"
    ),
    no_db: bool = typer.Option(False, "--no-db", help="With --write, skip Postgres"),
) -> None:
    """Re-apply today's scoring to a finished run's stored ReviewItems.

    Costs nothing — no LLM calls, no retrieval — so a scoring fix can be checked
    against past runs. Expectations come from the run's frozen case list, so
    what you see is the effect of the SCORING change alone; to measure a
    golden-set change, start a new run. Dry-run by default.
    """
    cfg = load_eval_config()
    manifest, results = rescore_run(cfg, run_id)
    run_dir = run_directory(cfg, run_id)
    before = summarize(load_partial_results(run_dir))
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
    (run_dir / RESULTS_FILENAME).write_text(
        json.dumps([r.model_dump(mode="json") for r in results], indent=2), encoding="utf-8"
    )
    rewrite_partial(run_dir, results)
    if not no_db:
        with evaldb.connect(cfg.database_url) as conn:
            evaldb.apply_schema(conn)
            evaldb.insert_run(conn, manifest, results)
        typer.echo(f"stored in Postgres: run_id={manifest.run_id}")
    typer.echo(f"rescored results written to {run_dir}")


@app.command("label-cases")
def label_cases(
    country: list[str] = typer.Option(None, "--country"),
    apply: bool = typer.Option(False, "--apply", help="Write the proposals into the case files"),
) -> None:
    """Draft a difficulty rung + hazard flags for each golden case, for review.

    Prints one line per case with the proposal and the reason for it, then a
    per-bucket count. Nothing is written without --apply, and even then only
    `difficulty`/`hazards` change: labels are metadata about a case, not ground
    truth about its value, so a human `verified` flag survives untouched.

    A label you disagree with belongs in the selection file
    (golden_sources/<cc>.json), as `difficulty` / `hazards` on the entry — the
    builders prefer an explicit entry value over anything drafted here, so a
    rebuild will not undo your correction.
    """
    cfg = load_eval_config()
    cases = load_cases(cfg.dataset_dir, countries=country or None)
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
            record = load_record(REPO_ROOT / case.parameter_file)
            basis = record.information.temporal_basis
        except (OSError, ValueError):
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
            mark = "="  # a human set this in the selection file; the draft is FYI only
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
            "golden_sources/ and are left alone: "
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
        save_case(cfg.dataset_dir, case)
    typer.echo(f"\nwrote {len(changed)} case file(s); `verified` untouched.")


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
        typer.echo(
            f"{row['created_at']:%Y-%m-%d %H:%M}  {row['model_provider']}/{row['model_name']}"
            f"  [{row['language']}/{row['country']}]  cases={row['cases']}"
            f"  routing={pct(row['routing_pct'])}  value={pct(row['value_pct'])}  date={pct(row['date_pct'])}"
            f"  citation={pct(row['citation_pct'])}  verbatim={pct(row['extract_verbatim_pct'])}"
            f"  supported={pct(row['supportedness_pct'])}  critique={pct(row['critique_pass_pct'])}"
            f"  halluc={pct(row['hallucination_pct'])}  recall={pct(row['retrieval_recall_pct'])}"
            f"  abstained={abstentions}"
            f"{impact(row)}"
            f"  {row['run_id']}"
            f"{readiness(row)}"
            f"{breakdown(row, 'difficulty', by_difficulty, 'difficulty')}"
            f"{breakdown(row, 'hazard', by_hazard, 'hazard')}"
        )


if __name__ == "__main__":
    app()
