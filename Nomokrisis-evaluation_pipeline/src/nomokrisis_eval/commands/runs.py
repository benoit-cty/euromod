"""Evaluation-run commands: run, resume, benchmark, rescore, list and report."""

from __future__ import annotations

import time
from collections import Counter
from datetime import date

import typer
from nomoscope_workflow.tracing import set_progress

from .. import benchmark
from .. import db as evaldb
from .. import golden_store
from ..config import EvalConfig, load_eval_config
from ..runner import (
    execute_run,
    golden_set_drift,
    latest_incomplete_run,
    list_runs,
    rescore_run,
    resume_run,
    start_run,
    store_rescored,
)
from ..schema import CaseResult, GoldenCase, RunManifest
from ..summary import summarize
from .common import app, concurrency_option, emit_progress, emit_result, parse_date, verbose_option


@app.command()
def run(
    as_of: str = typer.Option(
        ..., "--as-of",
        help="The run's reference date, YYYY-MM-DD (recorded on the run; each case runs on its own as_of)",
    ),
    model: str = typer.Option(..., "--model", help="Provider-prefixed model, e.g. anthropic/claude-sonnet-5 or mock/extractor"),
    country: list[str] = typer.Option(None, "--country", help="Restrict to country code(s)"),
    language: list[str] = typer.Option(None, "--language", help="Restrict to language(s)"),
    verified_only: bool = typer.Option(True, "--verified-only/--include-drafts", help="Evaluate only human-verified cases"),
    notes: str = typer.Option(None, "--notes"),
    verbose: bool = verbose_option(),
    concurrency: int = concurrency_option(),
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
        manifest = start_run(conn, cfg, cases, parse_date(as_of), model, notes=notes)
        typer.echo(
            f"run {manifest.run_id}  model={manifest.model}  as_of={manifest.as_of}"
            f"  dataset={manifest.dataset_version}  cases={len(cases)}"
        )
        _execute_and_report(conn, cfg, manifest, cases, [], verbose=verbose, concurrency=concurrency)


@app.command("run-benchmark")
def run_benchmark(
    country: str = typer.Argument(..., help="ISO country code, e.g. FR"),
    year: int = typer.Option(..., "--year", help="System year to find, starting blind from the year before"),
    model: str = typer.Option(..., "--model", help="Provider-prefixed model, e.g. azure_openai/gpt-5.6-luna or mock/extractor"),
    sample: int = typer.Option(None, "--sample", help="Run N parameters drawn at random"),
    seed: int = typer.Option(None, "--seed", help="Seed for --sample (reproducible draw)"),
    exclude_policy: list[str] = typer.Option(None, "--exclude-policy", help="Skip a whole policy, e.g. tco_fr"),
    target: list[str] = typer.Option(None, "--target", help="Only these refs (model_target or group:<id>)"),
    notes: str = typer.Option(None, "--notes"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build and list the cases, run nothing"),
    verbose: bool = verbose_option(),
    concurrency: int = concurrency_option(),
) -> None:
    """Every parameter of a country, updated blind from EUROMOD Y-1 and scored
    against EUROMOD Y and OpenFisca Y (see `benchmark`).

    A normal evaluation run with `blind_before` = 1 January of Y: resumable
    with `nomokrisis-eval resume`, summarised with `benchmark-report`. Ends
    with `@result {"run_id": …}`.
    """
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        build = benchmark.build_cases(
            conn, country, year, sample=sample, seed=seed,
            exclude_policies=exclude_policy or None, targets=target or None,
        )
        routings = Counter(c.expected.routing.value for c in build.cases)
        typer.echo(
            f"{country.upper()} {year - 1} -> {year}: {len(build.cases)} case(s) "
            f"({', '.join(f'{k} {v}' for k, v in sorted(routings.items()))}); "
            f"{len(build.skipped)} skipped"
        )
        for reason, count in Counter(build.skipped.values()).most_common(8):
            typer.echo(f"  skipped {count:>4}  {reason}")
        if dry_run:
            for case in build.cases:
                exp = case.expected
                typer.echo(
                    f"  {case.parameter_target:<60} {exp.routing.value:<21} {exp.value!r}"
                    + (f"  accept={exp.accept!r}" if exp.accept else "")
                    + (f"  openfisca={exp.openfisca['value']!r}" if exp.openfisca else "")
                )
            return
        if not build.cases:
            raise typer.Exit(1)
        manifest = start_run(
            conn, cfg, build.cases, benchmark.anchor_date(year), model,
            notes=notes or f"benchmark {country.upper()} {year - 1}->{year}",
            blind_before=date(year, 1, 1),
        )
        typer.echo(
            f"run {manifest.run_id}  model={manifest.model}  blind_before={manifest.blind_before}"
            f"  cases={len(build.cases)}"
        )
        _execute_and_report(conn, cfg, manifest, build.cases, [], verbose=verbose, concurrency=concurrency)
        _echo_benchmark(evaldb.load_results(conn, evaldb.load_run(conn, manifest.run_id)[0]))


def _echo_benchmark(results: list[CaseResult]) -> None:
    summary = benchmark.summarize_benchmark(results)
    typer.echo("\nbenchmark")
    for key, value in summary["headline"].items():
        typer.echo(f"  {key:<38} {value}")
    width = max(len(o) for o in benchmark.OUTCOMES)
    typer.echo("\n  EUROMOD \\ workflow " + " ".join(f"{o:>{width}}" for o in benchmark.OUTCOMES))
    for side, counts in summary["matrix"].items():
        typer.echo(f"  {side:<18} " + " ".join(f"{counts.get(o, 0):>{width}}" for o in benchmark.OUTCOMES))
    if summary["not_legislative"]:
        typer.echo(f"  national team / derived: {summary['not_legislative']}")
    if summary["arbitration"]:
        typer.echo("\n  disagreements")
        for who, count in sorted(summary["arbitration"].items(), key=lambda kv: -kv[1]):
            typer.echo(f"    {count:>4}  {who}")
    typer.echo("\n  per policy")
    for policy, counts in summary["by_policy"].items():
        typer.echo(
            f"    {policy:<14} " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: kv[0] != 'cases'))
        )


@app.command("benchmark-report")
def benchmark_report(
    run_id: str = typer.Argument(..., help="A run-benchmark run id"),
) -> None:
    """The change matrix, headline rates, OpenFisca arbitration and per-policy
    breakdown of a benchmark run, from its stored results (no LLM)."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        loaded = evaldb.load_run(conn, run_id)
        if loaded is None:
            typer.echo(f"no evaluation run {run_id} in eval.runs")
            raise typer.Exit(1)
        run_pk, manifest = loaded
        results = evaldb.load_results(conn, run_pk)
    typer.echo(
        f"run {manifest.run_id}  model={manifest.model}  blind_before={manifest.blind_before}"
        f"  {len(results)} result(s)"
    )
    _echo_benchmark(results)


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
    verbose: bool = verbose_option(),
    concurrency: int = concurrency_option(),
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

        current = golden_set_drift(conn, manifest)
        if current is not None:
            typer.echo(
                f"! golden set is {current} today, this run froze {manifest.dataset_version}; "
                "replaying the run's frozen case list"
            )
        typer.echo(
            f"resuming {manifest.run_id}  model={manifest.model}  as_of={manifest.as_of}"
            f"  {len(done)}/{len(cases)} already scored"
        )
        _execute_and_report(conn, cfg, manifest, cases, done, verbose=verbose, concurrency=concurrency)


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
    if result.euromod_discrepancy:
        flag += f"  EUROMOD-OFF-THE-LAW({result.euromod_discrepancy})"
    return f"{(result.routing_actual or '?'):<11} {marks}{flag}"


def _progress_callbacks(verbose: bool, concurrency: int = 1):
    """Print one line per case: `[ 7/42] <case id> routing... 4.1s eta 2m38s`.

    Quiet and sequential writes the prefix before the case runs — so a long LLM
    call shows what it is waiting on — and completes it in place once the case
    is scored. Verbose, or several cases in flight, prints the prefix and the
    outcome as two separate lines (the outcome line repeats the case id).
    """
    state = {"start": time.perf_counter(), "completed": 0}
    split = verbose or concurrency > 1

    def on_case_start(index: int, total: int, case: GoldenCase) -> None:
        typer.echo(f"[{index:>3}/{total}] {case.id:<46} " + ("started" if concurrency > 1 else ""), nl=split)

    def on_case_done(index: int, total: int, case: GoldenCase, result: CaseResult) -> None:
        state["completed"] += 1
        elapsed = time.perf_counter() - state["start"]
        eta = elapsed / state["completed"] * (total - index)
        prefix = f"[{index:>3}/{total}] {case.id:<46} " if split else ""
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
    concurrency: int = 1,
) -> None:
    """Score the pending cases with live progress, then summarize."""
    set_progress(verbose)  # per-step workflow chatter would drown the per-case lines
    on_case_start, on_case_done = _progress_callbacks(verbose, concurrency)

    def on_done(index: int, total: int, case: GoldenCase, result: CaseResult) -> None:
        on_case_done(index, total, case, result)
        emit_progress({"done": index, "total": total, "case": case.id, "run_id": manifest.run_id})

    try:
        results = execute_run(
            conn, cfg, manifest, cases, done,
            on_case_start=on_case_start, on_case_done=on_done, concurrency=concurrency,
        )
    except KeyboardInterrupt:
        scored = len(evaldb.load_results(conn, evaldb.load_run(conn, manifest.run_id)[0]))
        typer.echo(
            f"\ninterrupted after {scored}/{len(cases)} case(s) — nothing lost.\n"
            f"  resume with: nomokrisis-eval resume {manifest.run_id}"
        )
        emit_result({"run_id": manifest.run_id, "status": "running"})
        raise typer.Exit(130) from None

    typer.echo(f"\nrun {manifest.run_id}  model={manifest.model}  dataset={manifest.dataset_version}")
    for lang, kpis in summarize(results).items():
        pretty = "  ".join(f"{k}={v}" for k, v in kpis.items())
        typer.echo(f"  [{lang}] {pretty}")
    typer.echo(f"stored in Postgres: run_id={manifest.run_id} (eval.runs / eval.results)")
    emit_result({"run_id": manifest.run_id})


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
