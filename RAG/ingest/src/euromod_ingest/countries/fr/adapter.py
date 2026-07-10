"""French adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

from datetime import date

from euromod_ingest.countries.fr.fetcher import fetch_direct_id
from euromod_ingest.countries.fr.parser import parse_dila_json
from euromod_ingest.countries.fr.resolver import FrResolver, canary_facts
from euromod_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
from euromod_ingest.core.snapshots import SnapshotClient


class FrAdapter:
    """France implementation of the country adapter protocol."""

    jurisdiction = "FR"

    def __init__(self, resolver: FrResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or FrResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a French citation to exact DILA source identifiers."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch a French DILA document by direct identifier."""
        return fetch_direct_id(ref, http)

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Parse archived DILA JSON into country-neutral IR."""
        return parse_dila_json(snapshot_bytes, ref, snapshot)

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
        """Return French freshness canaries for supported fiscal years."""
        return canary_facts()
