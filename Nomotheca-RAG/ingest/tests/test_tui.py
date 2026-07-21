"""Smoke tests for the Textual ingestion TUI."""

from __future__ import annotations

import asyncio
from pathlib import Path

from textual.widgets import Button, Input, Select

from nomotheca_ingest.tui import DEFAULT_DATABASE_URL, PipelineTui, _format_fetch_progress


def test_pipeline_tui_mounts_run_button() -> None:
    """The TUI mounts and exposes the primary run button."""

    async def run_check() -> None:
        """Mount the app in Textual test mode and inspect its widgets."""
        app = PipelineTui()
        async with app.run_test():
            assert str(app.query_one("#run", Button).label) == "Run pipeline"

    asyncio.run(run_check())


def test_pipeline_tui_defaults_to_database_load() -> None:
    """The TUI starts with the local database URL filled in, not preview mode."""

    async def run_check() -> None:
        """Mount the app and inspect the database URL field."""
        app = PipelineTui()
        async with app.run_test():
            assert app.query_one("#database_url", Input).value == DEFAULT_DATABASE_URL

    asyncio.run(run_check())


def test_pipeline_tui_defaults_to_complete_fiscal_bill() -> None:
    """The TUI defaults to the LF2025 fiscal bill worklist mode."""

    async def run_check() -> None:
        """Mount the app and inspect fiscal bill defaults."""
        app = PipelineTui()
        async with app.run_test():
            assert app.query_one("#mode", Select).value == "bill"
            assert app.query_one("#identifier", Input).value == "JORFTEXT000051168007"
            assert app.query_one("#max_items", Input).value == "500"

    asyncio.run(run_check())


def test_pipeline_tui_creates_visible_log_file(tmp_path: Path, monkeypatch) -> None:
    """Starting a run log creates a file and exposes its path in the UI."""

    async def run_check() -> None:
        """Mount the app, start a log file, and verify panel/file output."""
        monkeypatch.chdir(tmp_path)
        app = PipelineTui()
        async with app.run_test():
            app._start_log_file()
            app._log("[green]stage:[/green] success detail")
            assert app._current_log_path is not None
            assert str(app._current_log_path).startswith("logs/ingest-tui-")
            assert "stage: success detail" in app._current_log_path.read_text(encoding="utf-8")

    asyncio.run(run_check())


def test_format_fetch_progress_includes_live_counts() -> None:
    """Fetch progress lines expose count and queue movement while a run is active."""
    line = _format_fetch_progress(
        source_id="JORFARTI000051168017",
        status_code=200,
        byte_count=2718,
        content_hash="dfcc05edb68a" + "0" * 52,
        snapshot_id="snapshot-id",
        fetched_count=9,
        queue_count=217,
        max_items=500,
        discovered_count=0,
    )

    assert "9/500 JORFARTI000051168017" in line
    assert "queue=217" in line
    assert "discovered=0" in line
