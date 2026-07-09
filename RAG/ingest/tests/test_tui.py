"""Smoke tests for the Textual ingestion TUI."""

from __future__ import annotations

import asyncio
from pathlib import Path

from textual.widgets import Button

from euromod_ingest.tui import PipelineTui


def test_pipeline_tui_mounts_run_button() -> None:
    """The TUI mounts and exposes the primary run button."""

    async def run_check() -> None:
        """Mount the app in Textual test mode and inspect its widgets."""
        app = PipelineTui()
        async with app.run_test():
            assert str(app.query_one("#run", Button).label) == "Run pipeline"

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
