"""``nomergon``: serve the worker, or submit and follow jobs from a shell."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any

import typer

from . import client, db, jobs
from .config import WorkerConfig, load_config

app = typer.Typer(help="Nomergon worker: the process that owns every model call (ADR 0004).", no_args_is_help=True)


def _cfg() -> WorkerConfig:
    return load_config()


def _connect(cfg: WorkerConfig):
    try:
        return db.connect(cfg.database_url)
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"cannot connect to {_redact_url(cfg.database_url)}: {exc}", err=True)
        raise typer.Exit(2) from None


def _redact_url(url: str) -> str:
    if "://" in url and "@" in url:
        scheme, rest = url.split("://", 1)
        credentials, host = rest.rsplit("@", 1)
        return f"{scheme}://{credentials.split(':', 1)[0]}:***@{host}"
    return url


@app.command("init-db")
def init_db() -> None:
    """Create the ops schema (idempotent)."""
    cfg = _cfg()
    with _connect(cfg) as conn:
        db.apply_schema(conn)
    typer.echo(f"ops schema applied to {_redact_url(cfg.database_url)}")


@app.command()
def serve(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Debug logging"),
) -> None:
    """Run the worker: claim jobs, run them, keep BGE-M3 warm for encode jobs."""
    from .worker import configure_logging, serve as _serve

    configure_logging(logging.DEBUG if verbose else logging.INFO)
    _serve(_cfg())


def parse_key_values(job_type: str, pairs: list[str]) -> dict[str, Any]:
    """``key=value`` pairs → a payload dict: JSON values where they parse, comma lists for list fields."""
    model = jobs.PAYLOAD_MODELS.get(job_type)
    payload: dict[str, Any] = {}
    for pair in pairs:
        if "=" not in pair:
            msg = f"expected key=value, got {pair!r}"
            raise typer.BadParameter(msg)
        key, raw = pair.split("=", 1)
        key = key.strip().replace("-", "_")
        value: Any
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = raw
        if model is not None and isinstance(value, str):
            field = model.model_fields.get(key)
            annotation = str(field.annotation) if field is not None else ""
            if annotation.startswith("list["):
                value = [part.strip() for part in value.split(",") if part.strip()]
        payload[key] = value
    return payload


@app.command()
def submit(
    job_type: str = typer.Argument(..., help="One of: " + ", ".join(jobs.JOB_TYPES)),
    fields: list[str] = typer.Argument(None, help="key=value pairs (JSON values; comma lists for list fields)"),
    payload: str = typer.Option(None, "--payload", help="The whole payload as JSON (instead of key=value pairs)"),
    priority: int = typer.Option(None, "--priority", help="Higher runs first (encode defaults to 100)"),
    wait: bool = typer.Option(False, "--wait", help="Follow the job's events and exit with its status"),
) -> None:
    """Queue one job; the worker validates the payload and runs it."""
    if job_type not in jobs.JOB_TYPES:
        raise typer.BadParameter(f"unknown job type {job_type!r}; one of {', '.join(jobs.JOB_TYPES)}")
    if payload and fields:
        raise typer.BadParameter("give either --payload or key=value pairs, not both")
    data = json.loads(payload) if payload else parse_key_values(job_type, fields or [])
    try:
        jobs.parse_payload(job_type, data)  # fail here, not on the worker
    except ValueError as exc:
        typer.echo(f"invalid payload: {exc}", err=True)
        raise typer.Exit(2) from None
    if priority is None:
        priority = jobs.ENCODE_PRIORITY if job_type == "encode" else 0

    cfg = _cfg()
    with _connect(cfg) as conn:
        job_id = client.submit(conn, job_type, data, priority)
        typer.echo(f"job {job_id} queued ({job_type})")
        if wait:
            row = client.wait(conn, job_id, on_event=_print_event)
            _print_final(row)
            raise typer.Exit(0 if row["status"] == "succeeded" else 1)


def _print_event(event: dict[str, Any]) -> None:
    stream = event["stream"]
    if stream == "progress":
        typer.echo(f"[progress] {db.dumps(event['data'])}")
    elif stream == "system":
        typer.echo(f"[worker] {event['line']}")
    else:
        typer.echo(event["line"], err=stream == "stderr")


def _print_final(row: dict[str, Any]) -> None:
    typer.echo(f"job {row['id']} {row['status']}")
    if row.get("result") is not None:
        typer.echo("@result " + db.dumps(row["result"]))
    if row.get("error"):
        typer.echo(row["error"], err=True)


def _summarise_progress(progress: Any) -> str:
    if not isinstance(progress, dict):
        return ""
    parts = []
    for key in ("phase", "status", "done", "completed", "scanned", "embedded", "total", "message"):
        if key in progress:
            parts.append(f"{key}={progress[key]}")
    return " ".join(parts) or db.dumps(progress)[:60]


def _fmt_time(value: datetime | None) -> str:
    """Local wall-clock time (the rows are timestamptz)."""
    return value.astimezone().strftime("%Y-%m-%d %H:%M:%S") if value else ""


def _table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        widths = [max(w, len(cell)) for w, cell in zip(widths, row, strict=True)]
    typer.echo("  ".join(h.ljust(w) for h, w in zip(headers, widths, strict=True)))
    for row in rows:
        typer.echo("  ".join(cell.ljust(w) for cell, w in zip(row, widths, strict=True)))


@app.command("jobs")
def jobs_cmd(limit: int = typer.Option(20, "--limit", help="Newest jobs to show")) -> None:
    """List jobs, newest first."""
    cfg = _cfg()
    with _connect(cfg) as conn:
        rows = db.list_jobs(conn, limit)
    _table(
        ["id", "type", "status", "submitted_by", "submitted_at", "progress"],
        [
            [
                str(row["id"]),
                row["job_type"],
                row["status"],
                row["submitted_by"],
                _fmt_time(row["submitted_at"]),
                _summarise_progress(row["progress"]),
            ]
            for row in rows
        ],
    )


@app.command()
def events(
    job_id: int = typer.Argument(..., help="Job id"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Keep printing until the job is final"),
) -> None:
    """Print a job's log lines (and, with --follow, stream them until it finishes)."""
    cfg = _cfg()
    with _connect(cfg) as conn:
        row = db.get_job(conn, job_id)
        if row is None:
            typer.echo(f"no job {job_id}", err=True)
            raise typer.Exit(2)
        if follow:
            row = client.wait(conn, job_id, on_event=_print_event)
        else:
            for event in db.events_after(conn, job_id, 0, limit=100_000):
                _print_event(event)
        _print_final(row)


@app.command()
def cancel(job_id: int = typer.Argument(..., help="Job id")) -> None:
    """Ask the worker to stop a job (a queued one is cancelled at once)."""
    cfg = _cfg()
    with _connect(cfg) as conn:
        if client.cancel(conn, job_id):
            typer.echo(f"job {job_id}: cancel requested")
        else:
            typer.echo(f"job {job_id}: nothing to cancel (unknown or already finished)", err=True)
            raise typer.Exit(1)


@app.command()
def status() -> None:
    """Workers (with heartbeat age) and the models they publish."""
    cfg = _cfg()
    with _connect(cfg) as conn:
        workers = db.list_workers(conn)
        models = db.list_models(conn)
    if not workers:
        typer.echo("no worker registered")
    else:
        _table(
            ["worker", "host", "device", "version", "heartbeat", "job"],
            [
                [
                    w["worker_id"],
                    w["hostname"],
                    w["device"] or "",
                    w["version"] or "",
                    _age(w["heartbeat_age"], cfg.stale_seconds),
                    str(w["current_job_id"] or ""),
                ]
                for w in workers
            ],
        )
    typer.echo("")
    if not models:
        typer.echo("no models published")
    else:
        _table(
            ["model", "kind", "default", "published_by"],
            [[m["model"], m["kind"], "yes" if m["is_default"] else "", m["published_by"]] for m in models],
        )


def _age(delta: timedelta, stale_seconds: float) -> str:
    seconds = delta.total_seconds()
    flag = " (stale)" if seconds > stale_seconds else ""
    return f"{seconds:.0f}s ago{flag}"


@app.command("prune-events")
def prune_events(
    days: int = typer.Option(None, "--days", help="Retention window (default: WORKER_EVENT_RETENTION_DAYS)"),
) -> None:
    """Delete job events older than the retention window."""
    cfg = _cfg()
    window = days if days is not None else cfg.event_retention_days
    with _connect(cfg) as conn:
        pruned = db.prune_events(conn, window)
    typer.echo(f"pruned {pruned} event(s) older than {window} days")


if __name__ == "__main__":  # pragma: no cover
    app()
