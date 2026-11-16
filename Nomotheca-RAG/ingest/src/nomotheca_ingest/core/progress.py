"""Progress reporting shared by the batch builds (embeddings, translations).

A batch build walks a backlog and calls ``progress(event)`` as it goes; the
event always has the same shape (:class:`BatchStats` plus a phase, the size
of the batch in flight and a detail), whichever build emits it. Two renderers
consume those events: :func:`json_progress` prints ``@progress {json}`` lines
for a wrapping UI or the worker, :func:`rich_progress` draws a terminal bar.
A build names itself to both through a :class:`BatchTask`.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field, replace

# Sentinel prefix for machine-readable progress lines (--progress-json). A
# wrapping UI (the Tauri Ingest tab) or the worker matches this prefix on
# stdout and renders a real progress bar instead of scrolling log text.
PROGRESS_PREFIX = "@progress "

ProgressEvent = dict[str, int | str]
ProgressCallback = Callable[[ProgressEvent], None]


@dataclass(frozen=True, slots=True)
class BatchStats:
    """Counts of one batch build: candidates scanned, items done (embedded or
    translated — or, in a dry run, that would be), skipped and failed."""

    scanned: int = 0
    done: int = 0
    skipped: int = 0
    failed: int = 0

    def plus(self, *, scanned: int = 0, done: int = 0, skipped: int = 0, failed: int = 0) -> BatchStats:
        return replace(
            self,
            scanned=self.scanned + scanned,
            done=self.done + done,
            skipped=self.skipped + skipped,
            failed=self.failed + failed,
        )


def emit(
    progress: ProgressCallback | None,
    phase: str,
    stats: BatchStats,
    *,
    batch_size: int = 0,
    detail: str = "",
) -> None:
    """Send one progress event, if a callback is registered."""
    if progress is None:
        return
    progress(
        {
            "phase": phase,
            "scanned": stats.scanned,
            "done": stats.done,
            "skipped": stats.skipped,
            "failed": stats.failed,
            "batch_size": batch_size,
            "detail": detail,
        }
    )


@dataclass(frozen=True, slots=True)
class BatchTask:
    """How a batch build names itself in progress output."""

    #: ``task`` field of the JSON lines ("embeddings", "translate").
    task: str
    #: What a done item is called, past tense ("embedded"); also the JSON key.
    action: str
    #: The same in a dry run ("would embed").
    dry_action: str
    #: Label of the terminal bar ("embedding chunks").
    description: str
    #: Phases too frequent for a JSON line each (per-candidate events).
    quiet_phases: frozenset[str] = field(default_factory=frozenset)


EMBEDDINGS = BatchTask(
    task="embeddings",
    action="embedded",
    dry_action="would embed",
    description="embedding chunks",
    quiet_phases=frozenset({"candidate"}),
)
TRANSLATIONS = BatchTask(
    task="translate",
    action="translated",
    dry_action="would translate",
    description="translating texts",
)


def emit_json(payload: dict[str, object]) -> None:
    """Print one '@progress {json}' line, flushed so lines stream live."""
    print(PROGRESS_PREFIX + json.dumps(payload, ensure_ascii=False), flush=True)


def report_failure(event: ProgressEvent) -> None:
    """Say on stderr which item failed (stdout carries the JSON protocol)."""
    if event["phase"] == "failed":
        print(f"failed {event['detail']}", file=sys.stderr, flush=True)


def json_progress(spec: BatchTask, total: int) -> ProgressCallback:
    """Callback printing one '@progress' line per event (quiet phases skipped)."""

    def update(event: ProgressEvent) -> None:
        phase = str(event["phase"])
        report_failure(event)
        if phase in spec.quiet_phases:
            return
        emit_json(
            {
                "task": spec.task,
                "phase": phase,
                "done": int(event["scanned"]),
                "total": total,
                spec.action: int(event["done"]),
                "failed": int(event["failed"]),
                "detail": str(event["detail"]),
            }
        )

    return update


def status_line(spec: BatchTask, event: ProgressEvent, *, dry_run: bool) -> str:
    """Compact status text for the terminal bar."""
    action = spec.dry_action if dry_run else spec.action
    phase = str(event["phase"])
    batch = int(event["batch_size"])
    counts = f"found={event['scanned']} {action}={event['done']}"
    if int(event["failed"]):
        counts += f" failed={event['failed']}"
    detail = str(event["detail"])
    if phase == "done":
        return f"done {counts}"
    if phase == "candidate":
        return f"{counts} queued={batch}"
    if phase == "encoding":
        return f"encoding batch={batch} {counts}"
    if phase == "embedded":
        return f"{counts} last_batch={batch}"
    return f"{counts} [{detail}]" if detail else counts


@contextmanager
def rich_progress(spec: BatchTask, *, limit: int | None, dry_run: bool) -> Iterator[ProgressCallback]:
    """A live Rich bar for the duration of the build; yields its callback."""
    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.fields[status]}"),
        TimeElapsedColumn(),
    ) as bar:
        task_id = bar.add_task(spec.description, total=limit, status="starting")

        def update(event: ProgressEvent) -> None:
            phase = str(event["phase"])
            scanned = int(event["scanned"])
            if phase == "failed":
                bar.console.print(f"[red]failed[/red] {event['detail']}")
            total = scanned if phase == "done" and limit is None else limit
            bar.update(task_id, completed=scanned, total=total, status=status_line(spec, event, dry_run=dry_run))

        yield update


@contextmanager
def batch_progress(
    spec: BatchTask,
    *,
    json_total: Callable[[], int] | None,
    show: bool,
    limit: int | None,
    dry_run: bool,
) -> Iterator[ProgressCallback]:
    """The progress callback a batch command asked for.

    ``json_total`` set: '@progress' lines against that total (counted
    before the scan starts). Else a Rich bar when ``show``, else only
    failures, on stderr.
    """
    if json_total is not None:
        yield json_progress(spec, json_total())
    elif show:
        with rich_progress(spec, limit=limit, dry_run=dry_run) as update:
            yield update
    else:
        yield report_failure
