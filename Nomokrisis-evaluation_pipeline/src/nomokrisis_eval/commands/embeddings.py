"""Retrieval-eval commands: the embedding cases, their runs and the model comparison."""

from __future__ import annotations

import psycopg
import typer
from psycopg.rows import dict_row

from .. import db as evaldb
from .. import golden_store
from ..config import load_eval_config
from .common import app, emit_result


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


@app.command("build-embedding-cases")
def build_embedding_cases(
    country: list[str] = typer.Option(None, "--country", help="Restrict to country code(s)"),
    include_drafts: bool = typer.Option(
        False, "--include-drafts", help="Also derive from golden cases no human has verified yet"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print the cases, write nothing"),
) -> None:
    """Derive retrieval cases from the golden set, with the workflow's own query.

    One `golden:<case id>` row in eval.embedding_cases per golden case that
    expects a citation: the query the `frame` step builds for its parameter,
    the date and jurisdiction scope a run searches, and the golden citations
    resolved to the exact article citations in that corpus. Idempotent — a
    re-run after a golden or corpus change rewrites the rows.
    """
    from nomoscope_workflow.config import load_config as load_workflow_config

    from .embedding_eval import cases_from_golden

    cfg = load_eval_config()
    wf_cfg = load_workflow_config()
    with evaldb.connect(cfg.database_url) as conn:
        golden = golden_store.load_cases(
            conn, countries=country or None, verified_only=not include_drafts
        )
        # The retrieval helpers read rows by column name.
        with psycopg.connect(cfg.database_url, row_factory=dict_row) as corpus:
            derived = cases_from_golden(conn, corpus, wf_cfg, golden)
        if not dry_run:
            for case in derived.cases:
                golden_store.save_embedding_case(conn, case)
    for case in derived.cases:
        typer.echo(f"  {case.id:<48} expects={'; '.join(case.expected_citations)}")
        typer.echo(f"      query: {case.query[:160]}")
    for case_id, reason in derived.skipped.items():
        typer.echo(f"  skip {case_id}: {reason}")
    verb = "would write" if dry_run else "wrote"
    typer.echo(
        f"{verb} {len(derived.cases)} case(s) from {len(golden)} golden case(s); "
        f"{len(derived.skipped)} skipped"
    )
    emit_result({"cases": len(derived.cases), "skipped": len(derived.skipped)})


@app.command("compare-embeddings")
def compare_embeddings(
    method: str = typer.Option("vector", "--method", help="fts | vector | hybrid"),
    dataset_version: str = typer.Option(
        None, "--dataset-version", help="Only runs on this case set (default: each model's latest run)"
    ),
) -> None:
    """The latest `run-embeddings` of every model, side by side, per language.

    Only the cases every compared run scored are counted.
    """
    from .embedding_eval import METHODS, compare_runs, latest_runs

    if method not in METHODS:
        raise typer.BadParameter(f"method must be one of: {', '.join(METHODS)}")
    cfg = load_eval_config()
    with evaldb.connect(cfg.database_url) as conn:
        runs = latest_runs(conn, dataset_version)
    if not runs:
        typer.echo("No embedding runs yet: `nomokrisis-eval run-embeddings --embedding-model-id N`.")
        raise typer.Exit(1)
    for run in runs:
        manifest = run["manifest"]
        latency = manifest.get("query_encode_ms_median")
        typer.echo(
            f"  {run['run_id']}  model={manifest.get('embedding_model')}  "
            f"cases={manifest['cases']}  set={manifest['dataset_version']}"
            + (f"  query≈{latency} ms" if latency is not None else "")
            + (
                f"  reranker={manifest['reranker']} pool={manifest['rerank_pool']}"
                f" ≈{manifest.get('rerank_ms_median')} ms"
                if manifest.get("reranker")
                else ""
            )
        )
    rows = compare_runs(runs, method)
    if not rows:
        typer.echo(f"No {method} scores in these runs.")
        raise typer.Exit(1)
    columns = list(rows[0])
    widths = {c: max(len(c), *(len(r.get(c, "")) for r in rows)) for c in columns}
    typer.echo(f"\n{method} leg")
    typer.echo("  ".join(c.ljust(widths[c]) for c in columns))
    for row in rows:
        typer.echo("  ".join(row.get(c, "").ljust(widths[c]) for c in columns))


@app.command("run-embeddings")
def run_embeddings(
    country: list[str] = typer.Option(None, "--country", help="Restrict to country code(s)"),
    language: list[str] = typer.Option(None, "--language", help="Restrict to query language(s)"),
    k: int = typer.Option(10, "--k", help="Rank cutoff for hit@k / MRR"),
    embedding_model_id: int = typer.Option(
        1, "--embedding-model-id",
        help="embeddings.model_id to evaluate: an ingest registry id (`nomotheca-ingest embeddings models`; "
        "1 = BGE-M3), whose chunk vectors must be built; 99 = in-SQL placeholder demo embedder",
    ),
    verified_only: bool = typer.Option(
        False, "--verified-only/--include-drafts",
        help="Restrict to human-verified cases (drafts included by default — this eval is diagnostic, not the contractual KPI freeze)",
    ),
    notes: str = typer.Option(None, "--notes"),
    reranker: str = typer.Option(
        None, "--reranker",
        help="Also score a cross-encoder over the hybrid candidates (bge-reranker-v2-m3 | qwen3-reranker-0.6b)",
    ),
    rerank_pool: int = typer.Option(50, "--rerank-pool", help="Hybrid candidates handed to the reranker"),
) -> None:
    """Rank each case's ground-truth chunks under fts / vector / hybrid search (+ rerank)."""
    from .embedding_eval import METHODS, run_embedding_eval, summarize_embedding

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
        cfg, cases, k=k, embedding_model_id=embedding_model_id, notes=notes,
        reranker=reranker, rerank_pool=rerank_pool,
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
        legs = "  ".join(f"{m}={fmt_rank(result, m):<5}" for m in METHODS if m in result.ranks)
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
            if not metrics:
                continue
            pretty = "  ".join(f"{k_}={v}" for k_, v in metrics.items()) or "not scored"
            typer.echo(f"    {method:<7} {pretty}")
    typer.echo(f"stored in Postgres: eval.embedding_runs run_id={manifest['run_id']}")
    emit_result({"run_id": manifest["run_id"]})
