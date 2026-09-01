"""Command-line entry points for the ingestion package."""

from __future__ import annotations

import json
from datetime import date
from typing import Annotated

import psycopg
import typer
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from nomotheca_ingest.core.embeddings import (
    EMBEDDING_BACKENDS,
    BGE_M3_MODEL,
    SentenceTransformerBackend,
    build_embeddings,
    count_chunks_needing_embeddings,
)
from nomotheca_ingest.core.pipeline import PipelineResult, run_database_ingest
from nomotheca_ingest.core.translate import (
    DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS,
    DEFAULT_TARGET_LANG,
    LLMTranslationBackend,
    build_translations,
    count_texts_needing_translation,
)
from nomotheca_ingest.tui import PipelineTui

# Sentinel prefix for machine-readable progress lines (--progress-json). A
# wrapping UI (the Tauri Ingest tab) matches this prefix on stdout and renders
# a real progress bar instead of scrolling log text.
PROGRESS_PREFIX = "@progress "


app = typer.Typer(help="Archive-first legislation ingestion commands.")
embeddings_app = typer.Typer(help="Build derived chunk embeddings.")
app.add_typer(embeddings_app, name="embeddings")
translate_app = typer.Typer(help="Machine-translate unit texts with an LLM.")
app.add_typer(translate_app, name="translate")


@app.command()
def instrument(
    jurisdiction: str,
    national_id: str,
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    source_code: Annotated[str | None, typer.Option("--source-code", "-s")] = None,
    max_items: Annotated[int, typer.Option("--max-items", min=1)] = 500,
) -> None:
    """Ingest a known national instrument id."""
    result = run_database_ingest(
        jurisdiction=jurisdiction,
        identifier=national_id,
        database_url=database_url,
        source_code=source_code,
        mode="instrument",
        max_items=max_items,
    )
    _print_result(result)


@app.command()
def citation(
    jurisdiction: str,
    citation_text: str,
    as_of: str,
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    source_code: Annotated[str | None, typer.Option("--source-code", "-s")] = None,
    max_items: Annotated[int, typer.Option("--max-items", min=1)] = 500,
) -> None:
    """Resolve and ingest a citation at a point in time."""
    result = run_database_ingest(
        jurisdiction=jurisdiction,
        identifier=citation_text,
        database_url=database_url,
        source_code=source_code,
        mode="citation",
        as_of=date.fromisoformat(as_of),
        max_items=max_items,
    )
    _print_result(result)


@app.command("country-report")
def country_report(
    jurisdiction: str,
    file: str,
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    vintage: Annotated[str, typer.Option("--vintage", help="CR vintage label, e.g. Y16.")] = "Y16",
    valid_from: Annotated[
        str, typer.Option("--valid-from", help="Start of the policy-year span the CR covers.")
    ] = "2022-01-01",
) -> None:
    """Ingest a EUROMOD Country Report Markdown file as a non-legislative corpus.

    Loaded instruments are tagged instrument_type='country_report' so the
    agentic workflow can exclude them from citable evidence retrieval.
    """
    from nomotheca_ingest.core.country_reports import ingest_country_report

    stats = ingest_country_report(
        file,
        jurisdiction,
        database_url,
        vintage=vintage,
        valid_from=date.fromisoformat(valid_from),
    )
    typer.echo(
        json.dumps(
            {
                "instruments": stats.instruments,
                "units": stats.units,
                "versions": stats.versions,
                "texts": stats.texts,
                "chunks": stats.chunks,
            },
            indent=2,
        )
    )


@app.command()
def tui() -> None:
    """Launch the interactive terminal UI for staged ingestion runs."""
    PipelineTui().run()


@embeddings_app.command("build")
def build_chunk_embeddings(
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    model_path: Annotated[str, typer.Option("--model-path", help="Local path or Hugging Face id for BGE-M3.")] = BGE_M3_MODEL,
    backend: Annotated[
        str,
        typer.Option("--backend", help="sentence-transformers backend: torch or openvino."),
    ] = "torch",
    model_id: Annotated[int, typer.Option("--model-id", min=1)] = 1,
    batch_size: Annotated[int, typer.Option("--batch-size", min=1)] = 16,
    limit: Annotated[int | None, typer.Option("--limit", min=1)] = None,
    device: Annotated[str | None, typer.Option("--device", help="Optional device, e.g. cpu, cuda, or CPU.")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Count stale chunks without writing embeddings.")] = False,
    show_progress: Annotated[bool, typer.Option("--progress/--no-progress", help="Show live embedding progress.")] = True,
    progress_json: Annotated[
        bool,
        typer.Option("--progress-json", help="Emit '@progress {json}' lines for wrapping UIs."),
    ] = False,
    fix_mistral_regex: Annotated[
        bool,
        typer.Option("--fix-mistral-regex", help="Forward fix_mistral_regex=True to the tokenizer."),
    ] = False,
    slow_tokenizer: Annotated[
        bool,
        typer.Option("--slow-tokenizer", help="Use the slow tokenizer; may require sentencepiece."),
    ] = False,
) -> None:
    """Build local BGE-M3 embeddings for chunks missing fresh vectors."""
    if backend not in EMBEDDING_BACKENDS:
        allowed = ", ".join(EMBEDDING_BACKENDS)
        raise typer.BadParameter(f"backend must be one of: {allowed}")
    embedding_backend = (
        _DryRunEmbeddingBackend()
        if dry_run
        else SentenceTransformerBackend(
            model_path=model_path,
            device=device,
            backend=backend,
            fix_mistral_regex=fix_mistral_regex,
            slow_tokenizer=slow_tokenizer,
        )
    )
    with psycopg.connect(database_url) as conn:
        if progress_json:
            total = count_chunks_needing_embeddings(conn, model_id=model_id, limit=limit)
            stats = build_embeddings(
                conn,
                embedding_backend,
                model_id=model_id,
                batch_size=batch_size,
                limit=limit,
                dry_run=dry_run,
                progress=_embedding_json_progress(total),
                commit_each_batch=True,
            )
        else:
            stats = _build_embeddings_with_optional_progress(
                conn=conn,
                embedding_backend=embedding_backend,
                model_id=model_id,
                batch_size=batch_size,
                limit=limit,
                dry_run=dry_run,
                show_progress=show_progress,
            )
        conn.commit()
    if dry_run:
        typer.echo(
            f"scanned={stats.scanned} would_embed={stats.embedded} "
            f"model_id={model_id} backend={backend} dry_run=True"
        )
    else:
        typer.echo(
            f"scanned={stats.scanned} embedded={stats.embedded} skipped={stats.skipped} "
            f"model_id={model_id} backend={backend} dry_run=False"
        )
        if stats.skipped:
            typer.echo(
                f"note: {stats.skipped} chunk(s) were re-chunked by a concurrent ingest "
                "during this run; re-run the build to embed the replacements."
            )


@translate_app.command("run")
def run_translations(
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    model: Annotated[
        str,
        typer.Option(
            "--model",
            "-m",
            envvar="EUROMOD_TRANSLATE_MODEL",
            help="Provider-prefixed model, e.g. anthropic/..., openai/..., openrouter/... (see nomoscope_workflow.llm).",
        ),
    ] = "openrouter/google/gemma-4-31b-it:free",
    target_lang: Annotated[str, typer.Option("--target-lang", help="Target language (must exist in lang_fts_config).")] = DEFAULT_TARGET_LANG,
    limit: Annotated[int | None, typer.Option("--limit", min=1)] = None,
    request_timeout: Annotated[
        float | None,
        typer.Option(
            "--request-timeout",
            min=1,
            help="Per-provider-request timeout in seconds. Use 0 to disable.",
        ),
    ] = DEFAULT_TRANSLATION_REQUEST_TIMEOUT_SECONDS,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Count untranslated texts without calling the LLM.")] = False,
    show_progress: Annotated[bool, typer.Option("--progress/--no-progress", help="Show live translation progress.")] = True,
    progress_json: Annotated[
        bool,
        typer.Option("--progress-json", help="Emit '@progress {json}' lines for wrapping UIs."),
    ] = False,
) -> None:
    """Translate every unit text version missing a target-language rendering."""
    timeout = None if request_timeout == 0 else request_timeout
    backend = None if dry_run else LLMTranslationBackend(model, request_timeout=timeout)
    with psycopg.connect(database_url) as conn:
        if progress_json:
            total = count_texts_needing_translation(conn, target_lang=target_lang, limit=limit)
            stats = build_translations(
                conn,
                backend,
                target_lang=target_lang,
                limit=limit,
                dry_run=dry_run,
                progress=_translation_json_progress(total),
            )
        else:
            stats = _build_translations_with_optional_progress(
                conn=conn,
                backend=backend,
                target_lang=target_lang,
                limit=limit,
                dry_run=dry_run,
                show_progress=show_progress,
            )
    action = "would_translate" if dry_run else "translated"
    typer.echo(
        f"scanned={stats.scanned} {action}={stats.scanned if dry_run else stats.translated} "
        f"failed={stats.failed} model={model} target_lang={target_lang} dry_run={dry_run}"
    )
    if stats.failed:
        raise typer.Exit(code=1)


def _emit_json_progress(payload: dict[str, object]) -> None:
    """Print one '@progress {json}' line; typer.echo flushes so lines stream live."""
    typer.echo(PROGRESS_PREFIX + json.dumps(payload, ensure_ascii=False))


def _translation_json_progress(total: int):
    """Progress callback emitting one JSON line per translation event."""

    def update(event: dict[str, int | str]) -> None:
        phase = str(event["phase"])
        if phase == "failed":
            typer.echo(f"failed {event['detail']}", err=True)
        _emit_json_progress(
            {
                "task": "translate",
                "phase": phase,
                "done": int(event["scanned"]),
                "total": total,
                "translated": int(event["translated"]),
                "failed": int(event["failed"]),
                "detail": str(event["detail"]),
            }
        )

    return update


def _embedding_json_progress(total: int):
    """Progress callback emitting JSON lines per embedding batch.

    Skips the per-chunk 'candidate' events — one line per encoded batch is
    plenty for a UI bar and keeps stdout small on large corpora.
    """

    def update(event: dict[str, int | str]) -> None:
        phase = str(event["phase"])
        if phase == "candidate":
            return
        _emit_json_progress(
            {
                "task": "embeddings",
                "phase": phase,
                "done": int(event["scanned"]),
                "total": total,
                "embedded": int(event["embedded"]),
                "detail": "",
            }
        )

    return update


def _build_translations_with_optional_progress(
    *,
    conn: psycopg.Connection,
    backend: LLMTranslationBackend | None,
    target_lang: str,
    limit: int | None,
    dry_run: bool,
    show_progress: bool,
):
    """Build translations with an optional Rich progress display."""
    if not show_progress:

        def report_failures(event: dict[str, int | str]) -> None:
            if event["phase"] == "failed":
                typer.echo(f"failed {event['detail']}", err=True)

        return build_translations(
            conn,
            backend,
            target_lang=target_lang,
            limit=limit,
            dry_run=dry_run,
            progress=report_failures,
        )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.fields[status]}"),
        TimeElapsedColumn(),
    ) as progress:
        task_id = progress.add_task("translating texts", total=limit, status="starting")

        def update(event: dict[str, int | str]) -> None:
            phase = str(event["phase"])
            scanned = int(event["scanned"])
            translated = int(event["translated"])
            failed = int(event["failed"])
            detail = str(event["detail"])
            action = "would translate" if dry_run else "translated"
            counts = f"found={scanned} {action}={scanned if dry_run else translated} failed={failed}"
            if phase == "failed":
                progress.console.print(f"[red]failed[/red] {detail}")
            status = counts if phase == "done" else f"{counts} [{detail}]"
            total = scanned if phase == "done" and limit is None else limit
            progress.update(task_id, completed=scanned, total=total, status=status)

        return build_translations(
            conn,
            backend,
            target_lang=target_lang,
            limit=limit,
            dry_run=dry_run,
            progress=update,
        )


class _DryRunEmbeddingBackend:
    """Backend placeholder used when no vectors will be written."""

    def encode(self, inputs: list[str]) -> list[list[float]]:
        return []


def _build_embeddings_with_optional_progress(
    *,
    conn: psycopg.Connection,
    embedding_backend: object,
    model_id: int,
    batch_size: int,
    limit: int | None,
    dry_run: bool,
    show_progress: bool,
):
    """Build embeddings with an optional Rich progress display."""
    if not show_progress:
        return build_embeddings(
            conn,
            embedding_backend,
            model_id=model_id,
            batch_size=batch_size,
            limit=limit,
            dry_run=dry_run,
            commit_each_batch=True,
        )

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.fields[status]}"),
        TimeElapsedColumn(),
    ) as progress:
        task_id = progress.add_task("embedding chunks", total=limit, status="starting")

        def update(event: dict[str, int | str]) -> None:
            status = _embedding_progress_status(event, dry_run=dry_run)
            scanned = int(event["scanned"])
            embedded = int(event["embedded"])
            phase = str(event["phase"])
            completed = scanned if phase != "done" else embedded
            total = scanned if phase == "done" and limit is None else limit
            progress.update(task_id, completed=completed, total=total, status=status)

        return build_embeddings(
            conn,
            embedding_backend,
            model_id=model_id,
            batch_size=batch_size,
            limit=limit,
            dry_run=dry_run,
            progress=update,
            commit_each_batch=True,
        )


def _embedding_progress_status(event: dict[str, int | str], *, dry_run: bool) -> str:
    """Return compact status text for the embedding progress bar."""
    action = "would embed" if dry_run else "embedded"
    phase = str(event["phase"])
    scanned = int(event["scanned"])
    embedded = int(event["embedded"])
    batch_size = int(event["batch_size"])
    if phase == "candidate":
        return f"found={scanned} {action}={embedded} queued={batch_size}"
    if phase == "encoding":
        return f"encoding batch={batch_size} found={scanned} {action}={embedded}"
    if phase == "embedded":
        return f"found={scanned} {action}={embedded} last_batch={batch_size}"
    return f"done found={scanned} {action}={embedded}"


def _print_result(result: PipelineResult) -> None:
    """Print a compact ingest summary for scripts and operators."""
    totals = {
        "instruments": sum(item.instruments for item in result.loaded),
        "units": sum(item.units for item in result.loaded),
        "versions": sum(item.versions for item in result.loaded),
        "texts": sum(item.texts for item in result.loaded),
        "chunks": sum(item.chunks for item in result.loaded),
    }
    retained = sum(item.retained_chunks for item in result.loaded)
    typer.echo(f"fetch_run={result.run_id}")
    typer.echo(
        "loaded "
        f"instruments={totals['instruments']} units={totals['units']} "
        f"versions={totals['versions']} texts={totals['texts']} chunks={totals['chunks']}"
    )
    if retained:
        # Cited chunks past the end of a shrunken text: kept, so the citation
        # still resolves, but no longer part of the current version's text.
        typer.echo(f"retained cited chunks={retained}")
    typer.echo(f"queued={len(result.queued)}")


if __name__ == "__main__":
    app()
