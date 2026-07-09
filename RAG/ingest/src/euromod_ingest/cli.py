"""Command-line entry points for the ingestion package."""

from __future__ import annotations

from datetime import date
from typing import Annotated

import typer

from euromod_ingest.core.pipeline import PipelineResult, run_database_ingest
from euromod_ingest.tui import PipelineTui


app = typer.Typer(help="Archive-first legislation ingestion commands.")


@app.command()
def instrument(
    jurisdiction: str,
    national_id: str,
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    source_code: Annotated[str | None, typer.Option("--source-code", "-s")] = None,
) -> None:
    """Ingest a known national instrument id."""
    result = run_database_ingest(
        jurisdiction=jurisdiction,
        identifier=national_id,
        database_url=database_url,
        source_code=source_code,
        mode="instrument",
    )
    _print_result(result)


@app.command()
def citation(
    jurisdiction: str,
    citation_text: str,
    as_of: str,
    database_url: Annotated[str, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")],
    source_code: Annotated[str | None, typer.Option("--source-code", "-s")] = None,
) -> None:
    """Resolve and ingest a citation at a point in time."""
    result = run_database_ingest(
        jurisdiction=jurisdiction,
        identifier=citation_text,
        database_url=database_url,
        source_code=source_code,
        mode="citation",
        as_of=date.fromisoformat(as_of),
    )
    _print_result(result)


@app.command()
def tui() -> None:
    """Launch the interactive terminal UI for staged ingestion runs."""
    PipelineTui().run()


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
