"""Command-line entry points for the ingestion package."""

from __future__ import annotations

from datetime import date
from typing import Annotated

import psycopg
import typer

from euromod_ingest.core.embeddings import EMBEDDING_BACKENDS, BGE_M3_MODEL, SentenceTransformerBackend, build_embeddings
from euromod_ingest.core.pipeline import PipelineResult, run_database_ingest
from euromod_ingest.tui import PipelineTui


app = typer.Typer(help="Archive-first legislation ingestion commands.")
embeddings_app = typer.Typer(help="Build derived chunk embeddings.")
app.add_typer(embeddings_app, name="embeddings")


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
) -> None:
    """Build local BGE-M3 embeddings for chunks missing fresh vectors."""
    if backend not in EMBEDDING_BACKENDS:
        allowed = ", ".join(EMBEDDING_BACKENDS)
        raise typer.BadParameter(f"backend must be one of: {allowed}")
    embedding_backend = (
        _DryRunEmbeddingBackend()
        if dry_run
        else SentenceTransformerBackend(model_path=model_path, device=device, backend=backend)
    )
    with psycopg.connect(database_url) as conn:
        stats = build_embeddings(
            conn,
            embedding_backend,
            model_id=model_id,
            batch_size=batch_size,
            limit=limit,
            dry_run=dry_run,
        )
        conn.commit()
    if dry_run:
        typer.echo(
            f"scanned={stats.scanned} would_embed={stats.embedded} "
            f"model_id={model_id} backend={backend} dry_run=True"
        )
    else:
        typer.echo(
            f"scanned={stats.scanned} embedded={stats.embedded} "
            f"model_id={model_id} backend={backend} dry_run=False"
        )


class _DryRunEmbeddingBackend:
    """Backend placeholder used when no vectors will be written."""

    def encode(self, inputs: list[str]) -> list[list[float]]:
        return []


def _print_result(result: PipelineResult) -> None:
    """Print a compact ingest summary for scripts and operators."""
    totals = {
        "instruments": sum(item.instruments for item in result.loaded),
        "units": sum(item.units for item in result.loaded),
        "versions": sum(item.versions for item in result.loaded),
        "texts": sum(item.texts for item in result.loaded),
        "chunks": sum(item.chunks for item in result.loaded),
    }
    typer.echo(f"fetch_run={result.run_id}")
    typer.echo(
        "loaded "
        f"instruments={totals['instruments']} units={totals['units']} "
        f"versions={totals['versions']} texts={totals['texts']} chunks={totals['chunks']}"
    )
    typer.echo(f"queued={len(result.queued)}")


if __name__ == "__main__":
    app()
