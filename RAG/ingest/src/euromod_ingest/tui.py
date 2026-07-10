"""Textual terminal UI for running and inspecting ingestion pipeline stages."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
import os
from pathlib import Path
import re
from threading import Thread
from traceback import format_exc
from uuid import UUID, uuid4

import psycopg
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, RichLog, Select, Static

from euromod_ingest.countries.registry import get_adapter
from euromod_ingest.core.db import PostgresSnapshotStore, create_fetch_run, finish_fetch_run
from euromod_ingest.core.ir import CitationRef, SourceRef, Trigger
from euromod_ingest.core.loader import LegislationLoader
from euromod_ingest.core.snapshots import SnapshotClient


DEFAULT_DATABASE_URL = os.getenv("EUROMOD_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation")


def _format_fetch_progress(
    source_id: str,
    status_code: int | None,
    byte_count: int,
    content_hash: str,
    snapshot_id: object,
    fetched_count: int,
    queue_count: int,
    max_items: int,
    discovered_count: int,
) -> str:
    """Build one live progress line for a completed fetch."""
    return (
        f"[cyan]fetch:[/cyan] {fetched_count}/{max_items} {source_id} "
        f"status={status_code} bytes={byte_count} sha256={content_hash[:12]} "
        f"snapshot={snapshot_id} queue={queue_count} discovered={discovered_count}"
    )


@dataclass(frozen=True, slots=True)
class RunConfig:
    """User-selected settings for one TUI pipeline run."""

    jurisdiction: str
    mode: str
    identifier: str
    as_of: date | None
    source_code: str
    database_url: str | None
    max_items: int


@dataclass(slots=True)
class InMemorySnapshotStore:
    """Snapshot store used by preview runs that do not write to PostgreSQL."""

    snapshots: dict[UUID, bytes] = field(default_factory=dict)

    def write_snapshot(
        self,
        ref: SourceRef,
        url: str,
        status_code: int,
        content_type: str | None,
        content_hash: str,
        content: bytes,
    ) -> UUID:
        """Archive raw bytes in memory and return a generated snapshot id."""
        snapshot_id = uuid4()
        self.snapshots[snapshot_id] = content
        return snapshot_id


class PipelineTui(App):
    """Interactive UI that runs ingestion stages and shows status plus logs."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #form {
        border: solid $accent;
        padding: 1;
        height: 17;
    }

    .field {
        width: 1fr;
    }

    #steps {
        border: solid $primary;
        padding: 1;
        height: 10;
    }

    #log-header {
        height: 2;
        padding-left: 1;
        color: $text;
    }

    #log {
        border: solid $secondary;
        height: 1fr;
    }
    """

    STEP_IDS = ("adapter", "resolve", "fetch", "parse", "expand", "load")
    MARKUP_RE = re.compile(r"\[[^\]]+\]")

    def __init__(self) -> None:
        """Create the TUI and initialize per-run log file state."""
        super().__init__()
        self._current_log_path: Path | None = None

    def compose(self) -> ComposeResult:
        """Build the TUI layout with inputs, step indicators, and a log panel."""
        yield Header()
        with Vertical(id="form"):
            yield Label("Ingestion run")
            with Horizontal():
                yield Input(value="FR", placeholder="Jurisdiction", id="jurisdiction", classes="field")
                yield Select(
                    (("Complete fiscal bill", "bill"), ("Direct DILA id", "direct"), ("Citation", "citation")),
                    value="bill",
                    id="mode",
                    classes="field",
                )
            with Horizontal():
                yield Input(value="JORFTEXT000051168007", placeholder="DILA id or citation", id="identifier", classes="field")
                yield Input(value="2025-06-01", placeholder="As-of date", id="as_of", classes="field")
            with Horizontal():
                yield Input(value="FR-LEGI", placeholder="Source code", id="source_code", classes="field")
                yield Input(value="500", placeholder="Max source items", id="max_items", classes="field")
            with Horizontal():
                yield Input(
                    value=DEFAULT_DATABASE_URL,
                    placeholder="PostgreSQL URL; clear for preview only",
                    id="database_url",
                    password=True,
                    classes="field",
                )
            yield Button("Run pipeline", id="run", variant="primary")
        with Vertical(id="steps"):
            yield Label("Step status")
            for step_id in self.STEP_IDS:
                yield Static(self._format_step(step_id, "pending"), id=f"step-{step_id}")
        yield Static("Run log: not started", id="log-header")
        yield RichLog(id="log", markup=True, wrap=True, highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        """Write the initial guidance message once widgets are mounted."""
        self._log("Ready. Database load is enabled by default; clear the database URL for preview mode.")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Start an ingestion run when the user presses the run button."""
        if event.button.id != "run":
            return
        try:
            config = self._read_config()
        except ValueError as exc:
            self._log(f"[red]Configuration error:[/red] {exc}")
            return
        self.query_one("#run", Button).disabled = True
        for step_id in self.STEP_IDS:
            self._set_step(step_id, "pending")
        self.query_one("#log", RichLog).clear()
        self._start_log_file()
        Thread(target=self._run_pipeline, args=(config,), daemon=True).start()

    def _read_config(self) -> RunConfig:
        """Read and validate current input widgets into a run configuration."""
        jurisdiction = self.query_one("#jurisdiction", Input).value.strip().upper()
        mode = str(self.query_one("#mode", Select).value)
        identifier = self.query_one("#identifier", Input).value.strip()
        as_of_raw = self.query_one("#as_of", Input).value.strip()
        source_code = self.query_one("#source_code", Input).value.strip().upper()
        max_items_raw = self.query_one("#max_items", Input).value.strip()
        database_url = self.query_one("#database_url", Input).value.strip() or None
        if not jurisdiction:
            raise ValueError("jurisdiction is required")
        if not identifier:
            raise ValueError("identifier or citation is required")
        if not source_code:
            raise ValueError("source code is required")
        max_items = int(max_items_raw) if max_items_raw else 500
        if max_items < 1:
            raise ValueError("max source items must be at least 1")
        as_of = date.fromisoformat(as_of_raw) if as_of_raw else None
        if mode == "citation" and as_of is None:
            raise ValueError("citation mode requires an as-of date")
        return RunConfig(jurisdiction, mode, identifier, as_of, source_code, database_url, max_items)

    def _run_pipeline(self, config: RunConfig) -> None:
        """Run ingestion stages in a worker thread and report status to the UI."""
        conn = None
        run_id = None
        current_step = "adapter"
        try:
            self.call_from_thread(self._log_run_start, config)
            if config.database_url is not None:
                conn = psycopg.connect(config.database_url)
                run_id = create_fetch_run(conn, config.source_code, "tui-0.1", Trigger.MANUAL)
                conn.commit()
                store = PostgresSnapshotStore(conn, run_id)
                self.call_from_thread(self._log, f"[cyan]run:[/cyan] Created fetch run {run_id}")
            else:
                store = InMemorySnapshotStore()
                self.call_from_thread(self._log, "[cyan]run:[/cyan] Preview mode; snapshots stay in memory")

            self._mark_running("adapter")
            adapter = get_adapter(config.jurisdiction)
            self._mark_success("adapter", f"Using {adapter.__class__.__name__}")

            current_step = "resolve"
            self._mark_running("resolve")
            if config.mode == "citation":
                refs = adapter.resolve(
                    CitationRef(jurisdiction=config.jurisdiction, citation=config.identifier),
                    config.as_of or date.today(),
                )
                self._mark_success("resolve", f"Resolved {len(refs)} source reference(s)")
            else:
                refs = [
                    SourceRef(
                        jurisdiction=config.jurisdiction,
                        source_code=config.source_code,
                        source_id=config.identifier,
                        source_type="direct_id",
                    )
                ]
                self._mark_success("resolve", "Direct id supplied")
            self.call_from_thread(self._log_source_refs, refs)

            current_step = "fetch"
            self._mark_running("fetch")
            http = SnapshotClient(store)
            snapshots = []
            parsed_docs = []
            queued = []
            pending = list(refs)
            seen: set[tuple[str, str]] = set()
            while pending and len(seen) < config.max_items:
                ref = pending.pop(0)
                ref_key = (ref.source_code, ref.source_id)
                if ref_key in seen:
                    continue
                seen.add(ref_key)
                self.call_from_thread(
                    self._log,
                    f"[cyan]fetch:[/cyan] fetching {len(seen)}/{config.max_items} {ref.source_id} queue={len(pending)}",
                )
                snapshot = adapter.fetch(ref, http)
                snapshots.append((ref, snapshot))
                parsed = adapter.parse(snapshot.raw_content, ref, snapshot)
                parsed_docs.append(parsed)
                followups = adapter.expand(parsed)
                queued.extend(followups)
                pending.extend(item.ref for item in followups)
                self._set_step_threadsafe("fetch", "running", f"Fetched {len(snapshots)}; queue {len(pending)}")
                self.call_from_thread(
                    self._log,
                    _format_fetch_progress(
                        source_id=ref.source_id,
                        status_code=snapshot.http_status,
                        byte_count=len(snapshot.raw_content),
                        content_hash=snapshot.content_hash,
                        snapshot_id=snapshot.id,
                        fetched_count=len(snapshots),
                        queue_count=len(pending),
                        max_items=config.max_items,
                        discovered_count=len(followups),
                    ),
                )
            self._mark_success("fetch", f"Fetched {len(snapshots)} snapshot(s)")

            current_step = "parse"
            self._mark_running("parse")
            instruments = sum(len(doc.instruments) for doc in parsed_docs)
            self._mark_success("parse", f"Parsed {instruments} instrument(s)")
            self.call_from_thread(self._log_parsed_docs, parsed_docs)

            current_step = "expand"
            self._mark_running("expand")
            self._mark_success("expand", f"Queued {len(queued)} follow-up item(s)")
            self.call_from_thread(self._log_queued_work, queued)
            if pending:
                self.call_from_thread(
                    self._log,
                    f"[yellow]expand:[/yellow] Stopped at max source items={config.max_items}; {len(pending)} item(s) remain",
                )

            current_step = "load"
            self._mark_running("load")
            if config.database_url is None:
                self._set_step_threadsafe("load", "skipped", "Preview mode; no database URL")
                self.call_from_thread(self._log, "[yellow]load:[/yellow] Skipped database load in preview mode")
            else:
                loader = LegislationLoader(conn)
                totals = [loader.load(doc) for doc in parsed_docs]
                finish_fetch_run(conn, run_id, "succeeded", {"trigger": "tui", "parsed_docs": len(parsed_docs)})
                conn.commit()
                loaded_chunks = sum(item.chunks for item in totals)
                self._mark_success("load", f"Loaded {loaded_chunks} chunk(s)")
                self.call_from_thread(self._log_load_totals, totals)
            self.call_from_thread(self._log, "[bold green]run:[/bold green] Completed successfully")
        except Exception:
            error = format_exc()
            self._set_step_threadsafe(current_step, "failed", "See log")
            if conn is not None and run_id is not None:
                finish_fetch_run(conn, run_id, "failed", {"trigger": "tui", "error": error})
                conn.commit()
            self.call_from_thread(self._log, f"[red]{error}[/red]")
        finally:
            if conn is not None:
                conn.close()
            self.call_from_thread(self._enable_run_button)

    def _mark_running(self, step_id: str) -> None:
        """Set a step to running from the worker thread."""
        self._set_step_threadsafe(step_id, "running")
        self.call_from_thread(self._log, f"[blue]{step_id}:[/blue] Started")

    def _mark_success(self, step_id: str, message: str) -> None:
        """Set a step to success and append an informational log line."""
        self._set_step_threadsafe(step_id, "success", message)
        self.call_from_thread(self._log, f"[green]{step_id}:[/green] {message}")

    def _set_step_threadsafe(self, step_id: str, status: str, detail: str | None = None) -> None:
        """Schedule a step status update from any thread."""
        self.call_from_thread(self._set_step, step_id, status, detail)

    def _set_step(self, step_id: str, status: str, detail: str | None = None) -> None:
        """Update one step indicator widget."""
        self.query_one(f"#step-{step_id}", Static).update(self._format_step(step_id, status, detail))

    def _format_step(self, step_id: str, status: str, detail: str | None = None) -> str:
        """Format a status line for the step panel."""
        labels = {
            "pending": "PENDING",
            "running": "RUNNING",
            "success": "OK",
            "failed": "FAIL",
            "skipped": "SKIP",
        }
        text = f"[{labels[status]}] {step_id}"
        return f"{text} - {detail}" if detail else text

    def _log(self, message: str) -> None:
        """Append a message to the TUI log panel."""
        self.query_one("#log", RichLog).write(message)
        if self._current_log_path is not None:
            plain_message = self.MARKUP_RE.sub("", message)
            with self._current_log_path.open("a", encoding="utf-8") as log_file:
                log_file.write(f"{datetime.now().isoformat(timespec='seconds')} {plain_message}\n")

    def _start_log_file(self) -> None:
        """Create a fresh persisted log file for the next run."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        self._current_log_path = log_dir / f"ingest-tui-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        self.query_one("#log-header", Static).update(f"Run log: {self._current_log_path}")
        self._log("[bold]log:[/bold] Writing this run to the log panel and file")

    def _log_run_start(self, config: RunConfig) -> None:
        """Log sanitized run settings at the start of a pipeline run."""
        as_of = config.as_of.isoformat() if config.as_of else "not set"
        persistence = "database" if config.database_url else "preview"
        self._log("[bold]run:[/bold] Starting ingestion pipeline")
        self._log(
            f"[cyan]run:[/cyan] jurisdiction={config.jurisdiction} mode={config.mode} "
            f"source={config.source_code} as_of={as_of} persistence={persistence} max_items={config.max_items}"
        )
        self._log(f"[cyan]run:[/cyan] identifier={config.identifier}")

    def _log_source_refs(self, refs: list[SourceRef]) -> None:
        """Log source references selected for fetching."""
        for ref in refs:
            self._log(f"[cyan]resolve:[/cyan] {ref.source_code}:{ref.source_type}:{ref.source_id}")

    def _log_snapshots(self, snapshots: list[tuple[SourceRef, object]]) -> None:
        """Log archived snapshot details for successful fetches."""
        for ref, snapshot in snapshots:
            size = len(snapshot.raw_content)
            self._log(
                f"[cyan]fetch:[/cyan] {ref.source_id} status={snapshot.http_status} "
                f"bytes={size} sha256={snapshot.content_hash[:12]} snapshot={snapshot.id}"
            )

    def _log_parsed_docs(self, parsed_docs: list[object]) -> None:
        """Log parsed document and IR row counts after parsing."""
        for doc in parsed_docs:
            units = sum(len(instrument.units) for instrument in doc.instruments)
            versions = sum(len(unit.versions) for instrument in doc.instruments for unit in instrument.units)
            texts = sum(
                len(version.texts)
                for instrument in doc.instruments
                for unit in instrument.units
                for version in unit.versions
            )
            self._log(
                f"[cyan]parse:[/cyan] {doc.ref.source_id} instruments={len(doc.instruments)} "
                f"units={units} versions={versions} texts={texts}"
            )

    def _log_queued_work(self, queued: list[object]) -> None:
        """Log follow-up work discovered during expansion."""
        if not queued:
            self._log("[cyan]expand:[/cyan] No follow-up work discovered")
            return
        for item in queued:
            self._log(f"[cyan]expand:[/cyan] {item.reason}: {item.ref.source_id}")

    def _log_load_totals(self, totals: list[object]) -> None:
        """Log aggregate database load counts for successful database runs."""
        instruments = sum(item.instruments for item in totals)
        units = sum(item.units for item in totals)
        versions = sum(item.versions for item in totals)
        texts = sum(item.texts for item in totals)
        chunks = sum(item.chunks for item in totals)
        self._log(
            f"[cyan]load:[/cyan] instruments={instruments} units={units} "
            f"versions={versions} texts={texts} chunks={chunks}"
        )

    def _enable_run_button(self) -> None:
        """Re-enable the run button after a worker finishes."""
        self.query_one("#run", Button).disabled = False
