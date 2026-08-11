"""CLI: run the workflow, inspect the queue, export accepted records.

  uv run nomoscope-workflow run data/parameters/fr_tinsc_bareme.json --year 2025
  uv run nomoscope-workflow run-all --year 2025
  uv run nomoscope-workflow queue
  uv run nomoscope-workflow export
  uv run nomoscope-workflow migrate-queue-ids --apply
  uv run nomoscope-workflow init-param-db
  uv run nomoscope-workflow sync-decisions
  uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/FR.enriched.json
  uv run nomoscope-workflow curate-params curation/FR.curation.yaml
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

import typer

from . import (
    openfisca,
    openfisca_match,
    paramdb,
    pipeline,
    queue_store,
    readiness,
    retrieval,
    translate,
)
from .config import load_config
from .tracing import setup_tracing

app = typer.Typer(no_args_is_help=True, add_completion=False)

# One run verifies ONE EUROMOD system year — mirroring EUROMOD's
# one-software-version-per-year model. The mid-year anchor date only feeds
# "version in force at" selection for in_force parameters; income_year
# parameters shift it internally (see pipeline._retrieval_as_of).
_YEAR_ANCHOR_MONTH_DAY = (7, 1)

_YEAR_HELP = "EUROMOD system year to verify (e.g. 2025). One run = one system year."
_AS_OF_HELP = "Deprecated: reference date YYYY-MM-DD; use --year (only the year matters)."


def _anchor_date(year: int | None, as_of: str | None) -> date:
    """Resolve --year/--as-of into the run's anchor date (exactly one required)."""
    if (year is None) == (as_of is None):
        typer.echo("Pass exactly one of --year or --as-of (prefer --year).")
        raise typer.Exit(2)
    if year is not None:
        return date(year, *_YEAR_ANCHOR_MONTH_DAY)
    parsed = date.fromisoformat(as_of)
    typer.echo(
        f"note: --as-of is deprecated; this run verifies system year {parsed.year} "
        f"(same as --year {parsed.year})"
    )
    return parsed


def _countries_in(files: list[Path]) -> tuple[dict[str, int], dict[str, int]]:
    """Parameter counts per country, and how many of them are income-year."""
    totals: dict[str, int] = {}
    income_year: dict[str, int] = {}
    for path in files:
        try:
            info = json.loads(path.read_text(encoding="utf-8")).get("information", {})
        except (OSError, ValueError):
            continue  # jsonc / unreadable: the per-file run will report it
        country = info.get("country")
        if not country:
            continue
        totals[country] = totals.get(country, 0) + 1
        if info.get("temporal_basis") == "income_year":
            income_year[country] = income_year.get(country, 0) + 1
    return totals, income_year


def _assert_system_year(cfg, files: list[Path], anchor: date) -> None:
    """Refuse a system year EUROMOD does not define for the country.

    Anchoring on today's date is the easy mistake (the UI used to default to it)
    and it is not harmless: no system exists for the year, so the run compares
    the proposal against the newest value on file and routes every parameter
    `changed` — a confident-looking queue item for a system nobody can accept.
    """
    totals, _ = _countries_in(files)
    try:
        with paramdb.connect(cfg) as conn:
            bounds = {c: paramdb.system_year_bounds(conn, c) for c in sorted(totals)}
    except Exception:
        return  # DB unreachable: the run itself will fail with a clearer error
    for country, span in bounds.items():
        if span is None:
            continue
        first, last = span
        if not first <= anchor.year <= last:
            typer.echo(
                f"{country} has no EUROMOD system year {anchor.year} "
                f"(the export defines {first}-{last}); did you mean --year {last}?"
            )
            raise typer.Exit(2)


def _readiness_banner(cfg, files: list[Path], anchor: date) -> None:
    """Per-country corpus readiness for the system year, printed once, up front."""
    totals, income_year = _countries_in(files)
    for country in sorted(totals):
        try:
            with retrieval.connect(cfg) as conn:
                statuses = readiness.finance_act_readiness(conn, country, anchor.year)
        except Exception:
            return  # DB unreachable: the run itself will fail with a clearer error
        if not statuses:
            continue
        typer.echo(
            f"system year {anchor.year} — corpus readiness ({country}, "
            f"{totals[country]} parameter(s), {income_year.get(country, 0)} income-year):"
        )
        for status in statuses:
            typer.echo(readiness.describe(status, income_year.get(country, 0)))


@app.command()
def run(
    parameter_files: list[Path] = typer.Argument(..., help="Activity 1 parameter JSON file(s)"),
    year: int = typer.Option(None, "--year", help=_YEAR_HELP),
    as_of: str = typer.Option(None, "--as-of", help=_AS_OF_HELP),
    model: str = typer.Option(None, "--model", help="Override WORKFLOW_MODEL (e.g. anthropic/claude-sonnet-5)"),
    force: bool = typer.Option(False, "--force", help="Overwrite already-reviewed queue items"),
) -> None:
    """Run the workflow for the given parameter file(s) for ONE system year."""
    cfg = load_config()
    if model:
        cfg.model = model
        cfg.critique_model = model
    tracer = setup_tracing(cfg)
    reference_date = _anchor_date(year, as_of)
    _assert_system_year(cfg, parameter_files, reference_date)
    _readiness_banner(cfg, parameter_files, reference_date)
    for i, path in enumerate(parameter_files, 1):
        typer.echo(f"[{i}/{len(parameter_files)}] {path.name}")
        item = pipeline.run_parameter(cfg, tracer, path, reference_date, force=force)
        verdict = item.critique.verdict if item.critique else "-"
        typer.echo(f"{item.id}: routing={item.routing} critique={verdict} -> queue/{item.id}.json")


@app.command("run-all")
def run_all(
    params_dir: Path = typer.Option(None, "--params-dir", help="Directory of parameter JSON files"),
    year: int = typer.Option(None, "--year", help=_YEAR_HELP),
    as_of: str = typer.Option(None, "--as-of", help=_AS_OF_HELP),
    model: str = typer.Option(None, "--model"),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """Run the workflow for every parameter file in a directory, for ONE system year."""
    cfg = load_config()
    folder = params_dir or cfg.data_dir / "parameters"
    files = sorted(p for p in folder.glob("*.json*") if p.suffix in (".json", ".jsonc"))
    if not files:
        typer.echo(f"No parameter files in {folder}")
        raise typer.Exit(1)
    run(parameter_files=files, year=year, as_of=as_of, model=model, force=force)


@app.command("run-targets")
def run_targets(
    targets: list[str] = typer.Argument(
        ..., help="model_target ids (euromod://…) or parameter_keys of parameters in the params DB"
    ),
    year: int = typer.Option(None, "--year", help=_YEAR_HELP),
    as_of: str = typer.Option(None, "--as-of", help=_AS_OF_HELP),
    model: str = typer.Option(None, "--model", help="Override WORKFLOW_MODEL"),
    force: bool = typer.Option(False, "--force", help="Overwrite already-reviewed queue items"),
) -> None:
    """Run the workflow for parameters stored in the params DB (see ingest-params).

    Each target is materialized as an Activity 1 JSON file under
    <data>/parameters/db/ (a subdirectory, so run-all's glob ignores it),
    then goes through the standard file-based workflow.
    """
    cfg = load_config()
    out_dir = cfg.data_dir / "parameters" / "db"
    out_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    with paramdb.connect(cfg) as conn:
        for target in targets:
            try:
                record = paramdb.load_record(conn, target)
            except KeyError as exc:
                typer.echo(str(exc))
                raise typer.Exit(1)
            path = out_dir / f"{queue_store.slugify(record.information.model_target)}.json"
            path.write_text(
                json.dumps(record.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            typer.echo(f"materialized {path.relative_to(cfg.data_dir)}")
            files.append(path)
    run(parameter_files=files, year=year, as_of=as_of, model=model, force=force)


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


@app.command("migrate-queue-ids")
def migrate_queue_ids(
    apply: bool = typer.Option(False, "--apply", help="Write the changes (default: dry run)"),
    db: bool = typer.Option(True, "--db/--no-db", help="Also re-point the params DB's item ids"),
) -> None:
    """Re-key queue files onto the system-year id and collapse the duplicates.

    Queue items used to be keyed by anchor date, so every re-run of the same
    parameter for the same system year left another near-identical review. This
    renames each file to `<country>_<target>_<year>.json` and moves the extra
    runs to `<data>/queue_superseded/` (kept, not deleted). Decided items win
    over pending ones; the newest wins among equals. Run it once per data dir.

    The params DB stores the same ids (extraction_runs.item_id is the Parameters
    tab's link into the queue), so they are rewritten too. data/decisions.jsonl
    is append-only and keeps the ids as they were logged.
    """
    cfg = load_config()
    plan = queue_store.migrate_item_ids(cfg.data_dir, apply=apply)
    counts: dict[str, int] = {}
    for entry in plan:
        counts[entry["action"]] = counts.get(entry["action"], 0) + 1
        if entry["action"] == "keep":
            continue
        detail = entry.get("reason") or f"-> {entry['new_id']} ({entry.get('status')})"
        typer.echo(f"{entry['action']:<10} {entry['path'].name} {detail}")
    summary = ", ".join(f"{n} {action}" for action, n in sorted(counts.items())) or "nothing to do"
    typer.echo(f"queue: {summary}{'' if apply else ' — dry run, pass --apply to write'}")
    if db:
        try:
            rows = paramdb.remap_item_ids(cfg, apply=apply)
        except Exception as exc:  # the file queue is the primary store
            typer.echo(f"params DB not migrated ({exc.__class__.__name__}: {exc})")
            return
        typer.echo("db: " + ", ".join(f"{n} {table}" for table, n in rows.items()))


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


@app.command("sync-decisions")
def sync_decisions(
    log: Path = typer.Option(None, "--log", help="Defaults to <data>/decisions.jsonl"),
) -> None:
    """Replay the local decision copy into params.review_decisions.

    A repair tool. The UI records decisions in the database directly and refuses
    the decision if it cannot, so the two only drift if a write succeeded in the
    DB but failed on disk, or the log is being restored from a backup.
    Idempotent: entries already recorded are skipped.
    """
    cfg = load_config()
    path = log or cfg.data_dir / "decisions.jsonl"
    if not path.exists():
        typer.echo(f"No decision log at {path} — nothing to sync.")
        return
    entries = [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    inserted, skipped = paramdb.sync_decisions(cfg, entries)
    typer.echo(f"{path}: {inserted} decision(s) recorded, {skipped} already present.")


@app.command("init-param-db")
def init_param_db() -> None:
    """Create/refresh the params schema in the legislation DB (idempotent)."""
    cfg = load_config()
    with paramdb.connect(cfg) as conn:
        paramdb.apply_schema(conn)
    typer.echo(f"params schema applied to {cfg.database_url}")


@app.command("ingest-params")
def ingest_params(
    files: list[Path] = typer.Argument(..., help="Enriched country export(s), e.g. FR.enriched.json"),
) -> None:
    """Ingest enriched parameter exports into params.parameters/model_values/parameter_usage."""
    cfg = load_config()
    with paramdb.connect(cfg) as conn:
        paramdb.apply_schema(conn)
        for path in files:
            stats = paramdb.ingest_file(conn, path)
            typer.echo(
                f"{path.name}: {stats['parameters']} parameters, "
                f"{stats['model_values']} model values, {stats['usage_edges']} usage edges"
            )


@app.command("curate-params")
def curate_params(
    files: list[Path] = typer.Argument(..., help="Curation overlay(s), e.g. curation/FR.curation.yaml"),
) -> None:
    """Apply curated fields (temporal_basis) the EUROMOD export does not carry.

    Run after ingest-params. Idempotent — re-run it whenever a new export lands.
    """
    cfg = load_config()
    exit_code = 0
    with paramdb.connect(cfg) as conn:
        paramdb.apply_schema(conn)
        for path in files:
            stats = paramdb.apply_curation(conn, path)
            typer.echo(f"{path.name}: {stats['updated']} updated, {stats['unchanged']} already set")
            for target in stats["missing"]:
                typer.echo(f"  ! not in params DB: {target}")
                exit_code = 1
    raise typer.Exit(exit_code)


@app.command("ingest-openfisca")
def ingest_openfisca(
    parameters_dir: Path = typer.Argument(..., help="parameters/ directory of an OpenFisca country package"),
    country: str = typer.Option(..., "--country", help="ISO country code of the package"),
    kind: str = typer.Option("openfisca", "--kind", help="Corpus kind"),
    license: str = typer.Option("AGPL-3.0", "--license", help="License of the corpus"),
) -> None:
    """Ingest an OpenFisca-format parameter corpus into params.external_* (no EUROMOD mapping)."""
    cfg = load_config()
    if not parameters_dir.is_dir():
        typer.echo(f"not a directory: {parameters_dir}")
        raise typer.Exit(1)
    with paramdb.connect(cfg) as conn:
        paramdb.apply_schema(conn)
        stats = openfisca.ingest_corpus(
            conn, parameters_dir, country.upper(), kind=kind, license=license, echo=typer.echo
        )
    typer.echo(
        f"{stats['parameters']} external parameters, {stats['values']} value points, "
        f"{stats['references']} references "
        f"({stats['skipped_files']} node files skipped, {stats['errors']} parse errors)"
    )


@app.command("match-openfisca")
def match_openfisca(
    country: str = typer.Option("FR", "--country", help="Country code to match"),
    kind: str = typer.Option("openfisca", "--kind", help="External corpus kind"),
    min_years: int = typer.Option(3, "--min-years", help="Years that must agree for a fingerprint"),
    factors: str = typer.Option(
        "1", "--factors", help="Comma-separated scales to try (euromod = factor * external), e.g. 1,3,4,8"
    ),
    seed: Path = typer.Option(
        None, "--seed", help="JSON file of curated pairs, stored as match_method='manual'"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print candidates without writing"),
    limit: int = typer.Option(30, "--limit", help="Candidates to print (0 = all)"),
) -> None:
    """Suggest params.parameter_links rows from value fingerprints (+ curated seeds).

    Suggestions only: a link counts as validated once a human sets
    `validated_by`, and rows already validated are never overwritten.
    """
    cfg = load_config()
    scales = tuple(float(f) for f in factors.split(",") if f.strip())
    with paramdb.connect(cfg) as conn:
        paramdb.apply_schema(conn)
        links = openfisca_match.fingerprint_candidates(
            conn, country.upper(), kind=kind, min_years=min_years, factors=scales
        )
        curated: list = []
        if seed is not None:
            curated, skipped = openfisca_match.seed_links(conn, seed, country.upper(), kind=kind)
            for message in skipped:
                typer.echo(f"  ~ skipped {message}")
        # Curated pairs win over a fingerprint for the same (parameter, component).
        curated_keys = {(l.parameter_id, l.external_parameter_id, l.component) for l in curated}
        links = curated + [
            l for l in links if (l.parameter_id, l.external_parameter_id, l.component) not in curated_keys
        ]
        for link in links[: limit or None]:
            typer.echo(
                f"{link.score:.2f} {link.match_method:<11} {link.model_target} -> {link.path}"
                + (f" :: {link.component}" if link.component != "value" else "")
                + (f"  ({link.note})" if link.note else "")
                + (f"  [{link.matched_years}/{link.euromod_years} yrs]" if link.euromod_years else "")
            )
        if dry_run:
            typer.echo(f"{len(links)} candidate link(s); nothing written (--dry-run).")
            return
        written = openfisca_match.store_links(conn, links)
    typer.echo(
        f"{len(links)} candidate link(s) ({len(curated)} curated), {written} row(s) written to "
        "params.parameter_links — unvalidated suggestions until a human sets validated_by."
    )


@app.command("translate-params")
def translate_params(
    country: str = typer.Option("FR", "--country", help="Country code whose parameters to translate"),
    lang: str = typer.Option(None, "--lang", help="Target language (default: the country's law language)"),
    model: str = typer.Option(None, "--model", help="Override WORKFLOW_MODEL"),
    batch_size: int = typer.Option(8, "--batch-size", help="Parameters per LLM call"),
    limit: int = typer.Option(0, "--limit", help="Translate at most N parameters (0 = all pending)"),
    force: bool = typer.Option(False, "--force", help="Re-translate parameters that already have MT rows"),
) -> None:
    """Machine-translate parameter labels/descriptions into the law language (params.parameter_texts)."""
    cfg = load_config()
    chosen = model or cfg.model
    if chosen.startswith("mock"):
        typer.echo("translate-params needs a real model — set WORKFLOW_MODEL or pass --model")
        raise typer.Exit(1)
    with paramdb.connect(cfg) as conn:
        paramdb.apply_schema(conn)
        stats = translate.translate_country(
            conn, chosen, country.upper(), lang,
            batch_size=batch_size, limit=limit, force=force, echo=typer.echo,
        )
    typer.echo(
        f"{stats['parameters']} parameter(s) translated, {stats['texts']} text rows written"
        + (f", {stats['mismatches']} mismatched model_targets skipped" if stats["mismatches"] else "")
    )


@app.command()
def impact(
    project: str = typer.Option(None, "--project", help="Restrict to one Phoenix project (default: all)"),
    since: str = typer.Option(None, "--since", help="Only spans on/after this ISO date/datetime"),
    until: str = typer.Option(None, "--until", help="Only spans before this ISO date/datetime"),
    zone: str = typer.Option(None, "--zone", help="EcoLogits electricity mix zone (default: config, EEE)"),
    json_output: bool = typer.Option(False, "--json", help="Machine-readable output (used by the UI)"),
) -> None:
    """Estimate the environmental impact of traced LLM calls (EcoLogits over Phoenix spans)."""
    from . import impact as impact_mod

    cfg = load_config()
    report = impact_mod.build_report(
        cfg.phoenix_database_url,
        project=project,
        since=datetime.fromisoformat(since) if since else None,
        until=datetime.fromisoformat(until) if until else None,
        electricity_mix_zone=zone or cfg.electricity_mix_zone,
    )
    if json_output:
        typer.echo(json.dumps(report.as_dict(), ensure_ascii=False))
        return
    if not report.models:
        typer.echo("No LLM spans with token counts found (mock runs carry none).")
        return
    typer.echo(
        f"{'model':<36} {'calls':>6} {'out tok':>9} {'energy (kWh)':>16} {'GWP (gCO2eq)':>16}"
    )
    for m in report.models:
        if m.estimated:
            energy = f"{m.energy_kwh_min:.4f}–{m.energy_kwh_max:.4f}"
            gwp = f"{m.gwp_kgco2eq_min * 1000:.2f}–{m.gwp_kgco2eq_max * 1000:.2f}"
        else:
            energy = gwp = "not in registry"
        typer.echo(f"{m.model:<36} {m.calls:>6} {m.output_tokens:>9} {energy:>16} {gwp:>16}")
    typer.echo(
        f"{'TOTAL (estimated)':<36} {report.total_calls:>6} {report.total_output_tokens:>9} "
        f"{report.energy_kwh_min:.4f}–{report.energy_kwh_max:.4f} "
        f"{report.gwp_kgco2eq_min * 1000:>8.2f}–{report.gwp_kgco2eq_max * 1000:.2f}"
    )
    typer.echo(f"electricity mix zone: {report.electricity_mix_zone}")
    if report.not_estimated:
        typer.echo(
            "not estimated (model missing from the EcoLogits registry): "
            + ", ".join(report.not_estimated)
        )


if __name__ == "__main__":
    app()
