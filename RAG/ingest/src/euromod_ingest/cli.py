"""Command-line entry points for the ingestion package."""

from __future__ import annotations

from datetime import date

import typer

from euromod_ingest.tui import PipelineTui


app = typer.Typer(help="Archive-first legislation ingestion commands.")


@app.command()
def instrument(jurisdiction: str, national_id: str) -> None:
    """Ingest a known national instrument id."""
    raise typer.BadParameter("Database-backed SnapshotClient wiring is not implemented yet.")


@app.command()
def citation(jurisdiction: str, citation_text: str, as_of: str) -> None:
    """Resolve and ingest a citation at a point in time."""
    date.fromisoformat(as_of)
    raise typer.BadParameter("Resolver and database wiring are not implemented yet.")


@app.command()
def tui() -> None:
    """Launch the interactive terminal UI for staged ingestion runs."""
    PipelineTui().run()


if __name__ == "__main__":
    app()
