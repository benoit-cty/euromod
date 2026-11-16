"""The one Typer app every command module registers on, and what they share.

Commands a worker job wraps end with one `@result {json}` line on stdout
(`emit_result`); long ones print `@progress {json}` lines as they go.
"""

from __future__ import annotations

import json
from datetime import date

import typer

app = typer.Typer(no_args_is_help=True, add_completion=False)


def verbose_option():
    """`--verbose/--quiet`, shared by every command that runs cases."""
    return typer.Option(
        False, "--verbose/--quiet", "-v", help="Also mirror every workflow step of every case"
    )


def concurrency_option():
    """`-j`, shared by every command that runs cases."""
    return typer.Option(
        4, "--concurrency", "-j", min=1, envvar="EVAL_CONCURRENCY",
        help="Cases run at once (each case is mostly waiting on the LLM)",
    )


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def emit_result(payload: dict) -> None:
    """The one `@result` line a worker job parses (contracts.md)."""
    typer.echo("@result " + json.dumps(payload))


def emit_progress(payload: dict) -> None:
    typer.echo("@progress " + json.dumps(payload))
