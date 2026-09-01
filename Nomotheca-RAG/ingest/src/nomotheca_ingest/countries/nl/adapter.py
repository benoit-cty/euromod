"""Dutch adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

from datetime import date

from nomotheca_ingest.countries.nl.fetcher import fetch_bwb
from nomotheca_ingest.countries.nl.parser import parse_bwb_xml
from nomotheca_ingest.countries.nl.resolver import NlResolver, canary_facts
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
from nomotheca_ingest.core.snapshots import SnapshotClient


class NlAdapter:
    """Netherlands implementation of the country adapter protocol."""

    jurisdiction = "NL"
    default_source_code = "NL-BWB"

    def __init__(self, resolver: NlResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or NlResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Dutch citation to exact BWB source identifiers."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch a BWB payload from the official repository."""
        return fetch_bwb(ref, http)

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Parse archived BWB XML into country-neutral IR."""
        return parse_bwb_xml(snapshot_bytes, ref, snapshot)

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        """Return follow-up work discovered from the parsed document."""
        work: list[WorkItem] = []
        for child in doc.metadata.get("child_refs", []):
            source_id = child["source_id"]
            work.append(
                WorkItem(
                    ref=SourceRef(
                        jurisdiction=doc.ref.jurisdiction,
                        source_code=doc.ref.source_code,
                        source_id=source_id,
                        source_type=child["source_type"],
                    ),
                    reason=f"{doc.ref.source_id} contains {child['source_type']} {child.get('title') or source_id}",
                )
            )
        return work

    def canary_facts(self) -> list[CanaryFact]:
        """Return Dutch freshness canaries for supported fiscal years."""
        return canary_facts()
