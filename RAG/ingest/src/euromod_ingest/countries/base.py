"""Protocol shared by all country-specific legislation adapters."""

from __future__ import annotations

from datetime import date
from typing import Protocol

from euromod_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
from euromod_ingest.core.snapshots import SnapshotClient


class CountryAdapter(Protocol):
    """Country boundary for citation resolution, fetching, parsing, and expansion."""

    jurisdiction: str

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Return exact fetchable source ids for a citation at a point in time."""

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch and archive raw source bytes before parsing."""

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Convert archived bytes to country-neutral IR without network or DB access."""

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        """Return structural or amendment-linked follow-up work."""

    def canary_facts(self) -> list[CanaryFact]:
        """Known-truth assertions used to gate resolver freshness."""
