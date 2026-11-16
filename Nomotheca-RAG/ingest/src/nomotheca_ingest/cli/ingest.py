"""Ingest commands: acts by id or citation, contributed documents, Country
Reports, routing, reparse/rechunk of what is stored, canaries, the TUI."""

from __future__ import annotations

import json
from datetime import date
from typing import Annotated

import psycopg
import typer

from nomotheca_ingest.cli._app import DatabaseUrl, app
from nomotheca_ingest.core.ir import Trigger
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats
from nomotheca_ingest.core.pipeline import PipelineResult, run_database_ingest
from nomotheca_ingest.core.progress import emit_json


@app.command()
def instrument(
    jurisdiction: str,
    national_id: str,
    database_url: DatabaseUrl,
    source_code: Annotated[str | None, typer.Option("--source-code", "-s")] = None,
    max_items: Annotated[int, typer.Option("--max-items", min=1)] = 500,
) -> None:
    """Ingest a known national instrument id."""
    result = run_database_ingest(
        jurisdiction=jurisdiction,
        identifier=national_id,
        database_url=database_url,
        source_code=source_code,
        mode="instrument",
        max_items=max_items,
    )
    _print_result(result)


@app.command()
def citation(
    jurisdiction: str,
    citation_text: str,
    as_of: str,
    database_url: DatabaseUrl,
    source_code: Annotated[str | None, typer.Option("--source-code", "-s")] = None,
    max_items: Annotated[int, typer.Option("--max-items", min=1)] = 500,
) -> None:
    """Resolve and ingest a citation at a point in time."""
    result = run_database_ingest(
        jurisdiction=jurisdiction,
        identifier=citation_text,
        database_url=database_url,
        source_code=source_code,
        mode="citation",
        as_of=date.fromisoformat(as_of),
        max_items=max_items,
    )
    _print_result(result)


@app.command("reparse-documents")
def reparse_documents_cmd(
    database_url: DatabaseUrl,
    jurisdiction: Annotated[str | None, typer.Option("--jurisdiction", "-j")] = None,
    title_like: Annotated[
        str | None, typer.Option("--title-like", help="SQL ILIKE filter on the title, e.g. %Cnav 2025%.")
    ] = None,
) -> None:
    """Re-parse contributed documents from their stored bytes — no fetch.

    The units are replaced, the instrument and the reviewer's declaration
    stay. Run `embeddings build` afterwards.
    """
    from nomotheca_ingest.core.contributed import reparse_documents

    done = reparse_documents(
        database_url,
        jurisdiction=jurisdiction.upper() if jurisdiction else None,
        title_like=title_like,
        progress=lambda event: typer.echo(f"{event['phase']}: {event['detail']}"),
    )
    typer.echo(json.dumps({"documents": len(done)}))


@app.command()
def reparse(
    jurisdiction: str,
    database_url: DatabaseUrl,
    url_like: Annotated[
        str, typer.Option("--url-like", help="SQL LIKE filter on the snapshot URL, e.g. %LEGI/ARTI%.")
    ] = "%",
    limit: Annotated[int | None, typer.Option("--limit", min=1)] = None,
) -> None:
    """Replay the parser and loader over archived snapshots — no fetch.

    Use after a parser change so the corpus reflects it everywhere: the
    stored bytes are parsed again and loaded with the usual idempotent
    upsert. Texts whose content changed get new chunks; run
    `embeddings build` afterwards to refresh their (now stale) vectors.
    """
    from nomotheca_ingest.core.pipeline import reparse_snapshots

    stats = reparse_snapshots(jurisdiction, database_url, url_like=url_like, limit=limit)
    typer.echo(json.dumps(stats.as_dict(), indent=2))


@app.command()
def rechunk(
    database_url: DatabaseUrl,
    jurisdiction: Annotated[
        str | None, typer.Argument(help="Country code (ES includes its regions); all when omitted.")
    ] = None,
) -> None:
    """Restore the chunks missing from the end of stored texts — no fetch, no parse.

    Until 3 Nov 2026 re-loading a text over 6 000 chars deleted its last
    chunk. This re-chunks every authentic text whose chunks stop short of its
    content; run `embeddings build` afterwards for the restored chunks.
    """
    with psycopg.connect(database_url) as conn:
        stats = LegislationLoader(conn).rechunk_truncated(jurisdiction.upper() if jurisdiction else None)
    typer.echo(json.dumps({"texts": stats.texts, "chunks": stats.chunks}, indent=2))


@app.command()
def canary(
    database_url: DatabaseUrl,
    jurisdiction: Annotated[
        list[str] | None, typer.Argument(help="Country codes; every registered adapter when omitted.")
    ] = None,
) -> None:
    """Check each adapter's freshness canaries against the corpus.

    A canary is a known fact («CGI art. 197 was rewritten from 16 Feb 2025»):
    its newest version in the corpus must start on or after that date. Exit
    code 1 when one is stale or missing.
    """
    from nomotheca_ingest.core.canary import check_canaries
    from nomotheca_ingest.countries.registry import jurisdictions

    codes = [c.upper() for c in jurisdiction] if jurisdiction else jurisdictions()
    with psycopg.connect(database_url) as conn:
        results = check_canaries(conn, codes)
    for r in results:
        latest = r.latest_start.isoformat() if r.latest_start else "-"
        typer.echo(
            f"{r.status:<7} {r.jurisdiction} {r.fact.citation:<34} latest {latest} "
            f"(needs >= {r.fact.assert_latest_start_gte}) — {r.fact.reason}"
        )
    bad = [r for r in results if r.status != "ok"]
    typer.echo(f"@result {json.dumps({'checked': len(results), 'not_ok': len(bad)})}")
    if bad:
        raise typer.Exit(1)


@app.command("kali-sync")
def kali_sync() -> None:
    """Bring the local copy of the DILA KALI dumps (collective agreements) up to date.

    The first run downloads the global dump (~175 MB, ~1.8 GB extracted under
    NOMOTHECA_KALI_DIR); later runs apply the daily increments. `instrument fr
    KALITEXT…` syncs on its own when the copy is older than 12 h.
    """
    from nomotheca_ingest.countries.fr.kali import KaliStore

    store = KaliStore()
    report = store.sync()
    typer.echo(json.dumps({"root": str(store.root), **report, "applied": store.state().get("applied")}))
    typer.echo("@result " + json.dumps({"applied": store.state().get("applied")}))


@app.command("country-report")
def country_report(
    jurisdiction: str,
    file: str,
    database_url: DatabaseUrl,
    vintage: Annotated[str, typer.Option("--vintage", help="CR vintage label, e.g. Y16.")] = "Y16",
    valid_from: Annotated[
        str, typer.Option("--valid-from", help="Start of the policy-year span the CR covers.")
    ] = "2022-01-01",
) -> None:
    """Ingest a EUROMOD Country Report Markdown file as a non-legislative corpus.

    Loaded instruments are tagged instrument_type='country_report' so the
    agentic workflow can exclude them from citable evidence retrieval.
    """
    from nomotheca_ingest.core.country_reports import ingest_country_report

    stats = ingest_country_report(
        file,
        jurisdiction,
        database_url,
        vintage=vintage,
        valid_from=date.fromisoformat(valid_from),
    )
    typer.echo(
        json.dumps(
            {
                "instruments": stats.instruments,
                "units": stats.units,
                "versions": stats.versions,
                "texts": stats.texts,
                "chunks": stats.chunks,
            },
            indent=2,
        )
    )


#: Ordered phases of a `document` run, for the UI's progress bar.
DOCUMENT_PHASES = ("route", "fetch", "archive", "parse", "load", "done")


def _document_source(source: str) -> tuple[str | None, str | None]:
    """Split one positional into (url, file path) — whichever it is."""
    return (source, None) if source.startswith(("http://", "https://")) else (None, source)


@app.command()
def document(
    source: Annotated[str, typer.Argument(help="URL, or path to a PDF/HTML/Markdown/text file.")],
    database_url: DatabaseUrl,
    jurisdiction: Annotated[
        str | None, typer.Option("--jurisdiction", "-j", help="Country the document belongs to.")
    ] = None,
    lang: Annotated[str, typer.Option("--lang", help="Language of the document, as declared.")] = "fr",
    title: Annotated[str | None, typer.Option("--title", help="Document title.")] = None,
    kind: Annotated[
        str | None,
        typer.Option("--kind", help="Kind in the country's own words: loi, decret, arrete, circulaire, doctrine, other."),
    ] = None,
    valid_from: Annotated[
        str | None, typer.Option("--valid-from", help="Date the document is in force from (required).")
    ] = None,
    implements: Annotated[
        str | None,
        typer.Option("--implements", help="national_id of the ingested instrument this document implements."),
    ] = None,
    progress_json: Annotated[
        bool, typer.Option("--progress-json", help="Emit '@progress {json}' lines for wrapping UIs.")
    ] = False,
    trigger: Annotated[
        Trigger,
        typer.Option("--trigger", help="Why the run started: manual (a reviewer) or cache_miss (the scout)."),
    ] = Trigger.MANUAL,
) -> None:
    """Ingest a document a reviewer found: a URL, a PDF, an HTML page, Markdown or text.

    A URL on a known official portal is routed to that country's adapter
    instead, so official acts are ingested cleanly by national id; the
    contributed fields are then unused.
    """
    from nomotheca_ingest.core.contributed import ingest_document

    url, file_path = _document_source(source)
    try:
        result = ingest_document(
            database_url=database_url,
            jurisdiction=jurisdiction,
            lang=lang,
            title=title,
            kind=kind,
            valid_from=date.fromisoformat(valid_from) if valid_from else None,
            url=url,
            file_path=file_path,
            implements=implements,
            progress=_document_progress(progress_json),
            trigger=trigger,
        )
    except ValueError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=2) from exc

    typer.echo(
        json.dumps(
            {
                "routed_to": result.routed_to,
                "already_present": result.already_present,
                "jurisdiction": result.jurisdiction,
                "source_code": result.source_code,
                "national_id": result.national_id,
                "kind": result.kind,
                "source_trust_class": (
                    result.source_trust_class.value if result.source_trust_class else None
                ),
                "implements": result.implements,
                "units": result.units,
                "versions": result.versions,
                "texts": result.texts,
                "chunks": result.chunks,
                # Provenance: the run and the archived bytes this came from.
                "fetch_run_id": str(result.fetch_run_id) if result.fetch_run_id else None,
                "snapshot_id": str(result.snapshot_id) if result.snapshot_id else None,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


@app.command()
def route(
    source: Annotated[
        str, typer.Argument(help="URL, or path to a file, to classify. Omit for the kinds table only.")
    ] = "",
    database_url: Annotated[
        str | None, typer.Option("--database-url", "-d", envvar="EUROMOD_DATABASE_URL")
    ] = None,
) -> None:
    """Print, as one `@result {json}` line, whether a URL is a contributed document or an official act.

    The validation UI calls this before starting a run, so it can announce a
    switch to the legislation ingester, prefill the title and validity date,
    or show a refusal hint. With no source it answers with the kinds table
    alone — what the contributed-document form needs to render itself.
    """
    from nomotheca_ingest.core.contributed import KINDS_BY_JURISDICTION, TRUST_CLASS_BY_LEVEL
    from nomotheca_ingest.core.contributed import route as route_source
    from nomotheca_ingest.core.contributed import suggest
    from nomotheca_ingest.core.routing import RouteOutcome

    url, file_path = _document_source(source)
    outcome = RouteOutcome(kind="contributed", url=source)
    if source:
        if url:
            outcome = route_source(url, database_url)
        if outcome.kind == "contributed":
            try:
                outcome.suggestions = suggest(url=url, file_path=file_path)
            except Exception as exc:
                # A prefill is a convenience: an unreachable page must not stop
                # the reviewer from filling the fields themselves.
                outcome.suggestions = {"error": str(exc)}
    payload = outcome.as_json()
    if not source:
        payload["outcome"] = None
    # Everything the contributed-document form needs to render, from the one
    # call it already makes: the kinds a reviewer may state, in each
    # jurisdiction's own words, so the UI never keeps its own copy of the table.
    # Each kind carries its level AND the class derived from it, so the UI can
    # show what a kind means without re-implementing the mapping.
    payload["kinds"] = {
        jurisdiction: {
            label: {
                "norm_level": level.value,
                "source_trust_class": TRUST_CLASS_BY_LEVEL[level].value,
            }
            for label, level in table
        }
        for jurisdiction, table in KINDS_BY_JURISDICTION.items()
    }
    # The worker's job result (the UI's pre-check reads ops.jobs.result).
    typer.echo("@result " + json.dumps(payload, ensure_ascii=False))


@app.command()
def tui() -> None:
    """Launch the interactive terminal UI for staged ingestion runs (needs the `tui` extra)."""
    try:
        from nomotheca_ingest.tui import PipelineTui
    except ModuleNotFoundError as exc:
        raise typer.BadParameter("the TUI needs the tui extra: uv sync --extra tui") from exc
    PipelineTui().run()


def _document_progress(progress_json: bool):
    """Progress callback for a contributed-document run.

    Phases are a fixed, short list, so a wrapping UI gets a real bar out of a
    run whose total work is not countable in advance.
    """

    def update(event: dict) -> None:
        phase = str(event["phase"])
        detail = str(event.get("detail", ""))
        typer.echo(f"{phase}: {detail}" if detail else phase, err=True)
        if progress_json:
            done = DOCUMENT_PHASES.index(phase) + 1 if phase in DOCUMENT_PHASES else 0
            emit_json(
                {
                    "task": "document",
                    "phase": phase,
                    "done": done,
                    "total": len(DOCUMENT_PHASES),
                    "detail": detail,
                }
            )

    return update


def _print_result(result: PipelineResult) -> None:
    """Print a compact ingest summary for scripts and operators."""
    totals = LoadStats.total(result.loaded).as_dict()
    retained = totals["retained_chunks"]
    typer.echo(f"fetch_run={result.run_id}")
    typer.echo(
        "loaded "
        f"instruments={totals['instruments']} units={totals['units']} "
        f"versions={totals['versions']} texts={totals['texts']} chunks={totals['chunks']}"
    )
    if retained:
        # Cited chunks past the end of a shrunken text: kept, so the citation
        # still resolves, but no longer part of the current version's text.
        typer.echo(f"retained cited chunks={retained}")
    typer.echo(f"queued={len(result.queued)}")
