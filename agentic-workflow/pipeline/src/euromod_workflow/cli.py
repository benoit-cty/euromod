"""CLI: run the workflow, inspect the queue, export accepted records.

  uv run euromod-workflow run data/parameters/fr_tinsc_bareme.json --as-of 2025-06-01
  uv run euromod-workflow run-all --as-of 2025-06-01
  uv run euromod-workflow queue
  uv run euromod-workflow export
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer

from . import pipeline, queue_store
from .config import load_config
from .tracing import setup_tracing

app = typer.Typer(no_args_is_help=True, add_completion=False)


def _parse_as_of(value: str) -> date:
    return date.fromisoformat(value)


@app.command()
def run(
    parameter_files: list[Path] = typer.Argument(..., help="Activity 1 parameter JSON file(s)"),
    as_of: str = typer.Option(..., "--as-of", help="Reference date, YYYY-MM-DD"),
    model: str = typer.Option(None, "--model", help="Override WORKFLOW_MODEL (e.g. anthropic/claude-sonnet-5)"),
    force: bool = typer.Option(False, "--force", help="Overwrite already-reviewed queue items"),
) -> None:
    """Run the workflow for the given parameter file(s)."""
    cfg = load_config()
    if model:
        cfg.model = model
        cfg.critique_model = model
    tracer = setup_tracing(cfg)
    reference_date = _parse_as_of(as_of)
    for path in parameter_files:
        item = pipeline.run_parameter(cfg, tracer, path, reference_date, force=force)
        verdict = item.critique.verdict if item.critique else "-"
        typer.echo(f"{item.id}: routing={item.routing} critique={verdict} -> queue/{item.id}.json")


@app.command("run-all")
def run_all(
    params_dir: Path = typer.Option(None, "--params-dir", help="Directory of parameter JSON files"),
    as_of: str = typer.Option(..., "--as-of"),
    model: str = typer.Option(None, "--model"),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """Run the workflow for every parameter file in a directory."""
    cfg = load_config()
    folder = params_dir or cfg.data_dir / "parameters"
    files = sorted(p for p in folder.glob("*.json*") if p.suffix in (".json", ".jsonc"))
    if not files:
        typer.echo(f"No parameter files in {folder}")
        raise typer.Exit(1)
    run(parameter_files=files, as_of=as_of, model=model, force=force)


@app.command()
def queue() -> None:
    """List the review queue."""
    cfg = load_config()
    items = queue_store.load_items(cfg.data_dir)
    if not items:
        typer.echo("Queue is empty.")
        return
    for item in items:
        verdict = item.critique.verdict if item.critique else "-"
        typer.echo(
            f"{item.status:<9} {item.routing:<21} critique={verdict:<4} "
            f"conf={item.proposed_value.lineage.confidence if item.proposed_value and item.proposed_value.lineage else '-'} "
            f"{item.id}"
        )


@app.command()
def export(
    out_dir: Path = typer.Option(None, "--out-dir", help="Defaults to <data>/export"),
) -> None:
    """Export accepted/edited records in the Activity 1 format."""
    cfg = load_config()
    written = queue_store.export_accepted(cfg.data_dir, out_dir)
    for path in written:
        typer.echo(f"exported {path}")
    typer.echo(f"{len(written)} record(s) exported.")


if __name__ == "__main__":
    app()
