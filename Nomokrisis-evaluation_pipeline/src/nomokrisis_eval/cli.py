"""CLI: build the golden dataset, run evaluations, report KPIs.

  uv run nomokrisis-eval init-db
  uv run nomokrisis-eval build-dataset docs/fr_country_report_excerpt.md --country FR --as-of 2025-06-01
  uv run nomokrisis-eval list-cases
  uv run nomokrisis-eval run --as-of 2025-06-01 --model anthropic/claude-sonnet-5
  uv run nomokrisis-eval report
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import typer

from . import build_dataset as builder
from . import db as evaldb
from .config import load_eval_config
from .dataset import dataset_version, load_cases, load_embedding_cases, save_case
from .runner import run_evaluation, summarize

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
) -> None:
    """Run the agentic workflow over the golden set, score it, store the results."""
    cfg = load_eval_config()
    cases = load_cases(
        cfg.dataset_dir, countries=country or None, languages=language or None, verified_only=verified_only
    )
    if not cases:
        typer.echo("No matching golden cases (try --include-drafts).")
        raise typer.Exit(1)

    manifest, results = run_evaluation(cfg, cases, _parse_date(as_of), model, notes=notes)

    # Run manifest + full results on disk (reproducibility, per 04_activity4_validation.md)
    run_dir = cfg.runs_dir / manifest.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    (run_dir / "results.json").write_text(
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
def report(
    run_id: str = typer.Option(None, "--run-id", help="Restrict to one run"),
    limit: int = typer.Option(20, "--limit"),
) -> None:
    """KPI summary per (run, language) from Postgres (view eval.run_summary)."""
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        rows = evaldb.fetch_summary(conn, run_id=run_id, limit=limit)
    if not rows:
        typer.echo("No evaluation runs stored yet.")
        return
    def pct(value) -> str:
        return "-" if value is None else f"{value}%"

    def impact(row) -> str:
        if row.get("energy_kwh") is None:
            return ""
        return (
            f"  energy={row['energy_kwh'] * 1000:.1f}Wh"
            f"  co2={row['gwp_kgco2eq'] * 1000:.1f}g"
        )

    for row in rows:
        typer.echo(
            f"{row['created_at']:%Y-%m-%d %H:%M}  {row['model_provider']}/{row['model_name']}"
            f"  [{row['language']}/{row['country']}]  cases={row['cases']}"
            f"  routing={pct(row['routing_pct'])}  value={pct(row['value_pct'])}  date={pct(row['date_pct'])}"
            f"  citation={pct(row['citation_pct'])}  supported={pct(row['supportedness_pct'])}"
            f"  halluc={pct(row['hallucination_pct'])}  recall={pct(row['retrieval_recall_pct'])}"
            f"{impact(row)}"
            f"  {row['run_id']}"
        )


if __name__ == "__main__":
    app()
