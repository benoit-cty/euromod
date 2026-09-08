"""Library-first orchestration helpers for ingestion runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

import psycopg

from nomotheca_ingest.countries.registry import get_adapter
from nomotheca_ingest.core.db import PostgresSnapshotStore, create_fetch_run, finish_fetch_run
from nomotheca_ingest.core.ir import CitationRef, ParsedDoc, Snapshot, SourceRef, Trigger, WorkItem
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats
from nomotheca_ingest.core.snapshots import SnapshotClient


@dataclass(slots=True)
class PipelineResult:
    """Parsed documents and queued follow-up work produced by a pipeline run."""

    parsed: list[ParsedDoc] = field(default_factory=list)
    queued: list[WorkItem] = field(default_factory=list)
    loaded: list[LoadStats] = field(default_factory=list)
    run_id: UUID | None = None


def ingest_citation(jurisdiction: str, citation: str, as_of: date, http: SnapshotClient) -> PipelineResult:
    """Resolve a citation at a date, then fetch, parse, and expand its sources."""
    adapter = get_adapter(jurisdiction)
    refs = adapter.resolve(CitationRef(jurisdiction=jurisdiction.upper(), citation=citation), as_of)
    return _ingest_refs(adapter, refs, http)


def default_source_code(jurisdiction: str) -> str:
    """Return the sources.code an adapter fetches from when none is given."""
    adapter = get_adapter(jurisdiction)
    return getattr(adapter, "default_source_code", f"{jurisdiction.upper()}-LEGI")


def ingest_instrument(
    jurisdiction: str,
    national_id: str,
    http: SnapshotClient,
    source_code: str | None = None,
    max_items: int = 500,
) -> PipelineResult:
    """Fetch, parse, and expand a known national instrument identifier."""
    jurisdiction_code = jurisdiction.upper()
    adapter = get_adapter(jurisdiction)
    ref = SourceRef(
        jurisdiction=jurisdiction_code,
        source_code=source_code or default_source_code(jurisdiction_code),
        source_id=national_id,
        source_type="instrument",
    )
    return _ingest_refs(adapter, [ref], http, max_items=max_items)


def run_database_ingest(
    jurisdiction: str,
    identifier: str,
    database_url: str,
    *,
    mode: str = "instrument",
    as_of: date | None = None,
    source_code: str | None = None,
    trigger: Trigger = Trigger.MANUAL,
    skill_version: str = "cli-0.1",
    frozen_label: str | None = None,
    max_items: int = 500,
) -> PipelineResult:
    """Fetch, parse, and load one instrument or citation into PostgreSQL."""
    jurisdiction_code = jurisdiction.upper()
    resolved_source_code = source_code or default_source_code(jurisdiction_code)
    with psycopg.connect(database_url) as conn:
        run_id = create_fetch_run(conn, resolved_source_code, skill_version, trigger, frozen_label)
        result = PipelineResult(run_id=run_id)
        try:
            http = SnapshotClient(PostgresSnapshotStore(conn, run_id))
            if mode == "citation":
                if as_of is None:
                    raise ValueError("citation ingestion requires as_of")
                result = ingest_citation(jurisdiction_code, identifier, as_of, http)
            elif mode == "instrument":
                result = ingest_instrument(jurisdiction_code, identifier, http, resolved_source_code, max_items=max_items)
            else:
                raise ValueError(f"Unsupported ingestion mode: {mode}")
            result.run_id = run_id
            loader = LegislationLoader(conn)
            result.loaded = [loader.load(doc) for doc in result.parsed]
            finish_fetch_run(conn, run_id, "succeeded", _result_stats(result, trigger))
        except Exception as exc:
            finish_fetch_run(conn, run_id, "failed", {"trigger": trigger.value, "error": str(exc)})
            raise
    return result


@dataclass(slots=True)
class ReparseStats:
    """What a `reparse` pass did: archive rows seen, parsed, loaded, skipped."""

    snapshots: int = 0
    parsed: int = 0
    loaded: int = 0
    skipped: int = 0
    texts_changed: int = 0


def reparse_snapshots(
    jurisdiction: str,
    database_url: str,
    *,
    url_like: str = "%",
    limit: int | None = None,
    on_progress=None,
) -> ReparseStats:
    """Re-run the parser and loader over archived snapshots — no fetch.

    Archive-first pays off here: a parser change (keeping Legifrance's NOTA,
    say) reaches every document already ingested by replaying the stored
    bytes, so the corpus never depends on the source still serving them. The
    adapter rebuilds the SourceRef from the snapshot URL; snapshots it cannot
    map are skipped and counted. Loading is the ordinary idempotent upsert:
    unchanged texts keep their hash, changed ones get new chunks, and their
    embeddings turn stale for `embeddings build` to refresh.
    """
    jurisdiction_code = jurisdiction.upper()
    adapter = get_adapter(jurisdiction_code)
    rebuild = getattr(adapter, "source_ref_from_url", None)
    if rebuild is None:
        raise ValueError(f"{jurisdiction_code} adapter cannot rebuild source refs from snapshot URLs")
    stats = ReparseStats()
    with psycopg.connect(database_url) as conn:
        rows = conn.execute(
            """
            SELECT fs.id, fs.url, fs.http_status, fs.content_type, fs.content_hash, fs.raw_content,
                   s.code AS source_code
            FROM fetch_snapshots fs
            JOIN sources s ON s.id = fs.source_id
            JOIN jurisdictions j ON j.id = s.jurisdiction_id
            WHERE j.code = %s AND fs.url LIKE %s AND fs.raw_content IS NOT NULL
            ORDER BY fs.retrieved_at
            """
            + (" LIMIT %s" if limit else ""),
            (jurisdiction_code, url_like, *([limit] if limit else [])),
        ).fetchall()
        loader = LegislationLoader(conn)
        for row in rows:
            snapshot_id, url, status, ctype, chash, raw, source_code = row
            stats.snapshots += 1
            ref = rebuild(url, source_code)
            if ref is None:
                stats.skipped += 1
                continue
            snapshot = Snapshot(
                id=snapshot_id,
                source_code=source_code,
                url=url,
                http_status=status,
                content_type=ctype,
                content_hash=chash,
                raw_content=bytes(raw),
            )
            doc = adapter.parse(snapshot.raw_content, ref, snapshot)
            stats.parsed += 1
            if doc.instruments:
                before = _text_hashes(conn, doc)
                loader.load(doc)
                stats.loaded += 1
                stats.texts_changed += sum(1 for h in _text_hashes(conn, doc) if h not in before)
            if on_progress is not None:
                on_progress(stats)
    return stats


def _text_hashes(conn, doc: ParsedDoc) -> set[str]:
    """Content hashes of the unit texts a parsed document maps to (change detection)."""
    hashes: set[str] = set()
    for instrument in doc.instruments:
        for unit in instrument.units:
            for version in unit.versions:
                for row in conn.execute(
                    """
                    SELECT t.content_hash
                    FROM unit_texts t
                    JOIN legal_unit_versions v ON v.id = t.version_id
                    WHERE v.source_version_id = %s AND v.fetch_snapshot_id = %s
                    """,
                    (version.source_version_id, version.fetch_snapshot_id),
                ).fetchall():
                    hashes.add(row[0])
    return hashes


def _ingest_refs(adapter, refs: list[SourceRef], http: SnapshotClient, max_items: int = 500) -> PipelineResult:
    """Run the common fetch-parse-expand loop for resolved source references."""
    result = PipelineResult()
    pending = list(refs)
    seen: set[tuple[str, str]] = set()
    while pending and len(seen) < max_items:
        ref = pending.pop(0)
        ref_key = (ref.source_code, ref.source_id)
        if ref_key in seen:
            continue
        seen.add(ref_key)
        snapshot = adapter.fetch(ref, http)
        parsed = adapter.parse(snapshot.raw_content, ref, snapshot)
        result.parsed.append(parsed)
        followups = adapter.expand(parsed)
        result.queued.extend(followups)
        pending.extend(item.ref for item in followups)
    return result


def _result_stats(result: PipelineResult, trigger: Trigger) -> dict[str, int | str]:
    """Summarize an ingest result for fetch_runs.stats."""
    return {
        "trigger": trigger.value,
        "parsed_docs": len(result.parsed),
        "queued": len(result.queued),
        "instruments": sum(item.instruments for item in result.loaded),
        "units": sum(item.units for item in result.loaded),
        "versions": sum(item.versions for item in result.loaded),
        "texts": sum(item.texts for item in result.loaded),
        "chunks": sum(item.chunks for item in result.loaded),
        "retained_chunks": sum(item.retained_chunks for item in result.loaded),
    }
