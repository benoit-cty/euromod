"""Library-first orchestration helpers for ingestion runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from euromod_ingest.countries.registry import get_adapter
from euromod_ingest.core.ir import CitationRef, ParsedDoc, SourceRef, WorkItem
from euromod_ingest.core.snapshots import SnapshotClient


@dataclass(slots=True)
class PipelineResult:
    """Parsed documents and queued follow-up work produced by a pipeline run."""

    parsed: list[ParsedDoc] = field(default_factory=list)
    queued: list[WorkItem] = field(default_factory=list)


def ingest_citation(jurisdiction: str, citation: str, as_of: date, http: SnapshotClient) -> PipelineResult:
    """Resolve a citation at a date, then fetch, parse, and expand its sources."""
    adapter = get_adapter(jurisdiction)
    refs = adapter.resolve(CitationRef(jurisdiction=jurisdiction.upper(), citation=citation), as_of)
    return _ingest_refs(adapter, refs, http)


def ingest_instrument(jurisdiction: str, national_id: str, http: SnapshotClient) -> PipelineResult:
    """Fetch, parse, and expand a known national instrument identifier."""
    adapter = get_adapter(jurisdiction)
    ref = SourceRef(
        jurisdiction=jurisdiction.upper(),
        source_code=f"{jurisdiction.upper()}-LEGI",
        source_id=national_id,
        source_type="instrument",
    )
    return _ingest_refs(adapter, [ref], http)


def _ingest_refs(adapter, refs: list[SourceRef], http: SnapshotClient) -> PipelineResult:
    """Run the common fetch-parse-expand loop for resolved source references."""
    result = PipelineResult()
    for ref in refs:
        snapshot = adapter.fetch(ref, http)
        parsed = adapter.parse(snapshot.raw_content, ref, snapshot)
        result.parsed.append(parsed)
        result.queued.extend(adapter.expand(parsed))
    return result
