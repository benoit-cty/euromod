"""Irish adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

from datetime import date

from nomotheca_ingest.countries.ie.fetcher import SOURCE_CODE_EISB, fetch_ie
from nomotheca_ingest.countries.ie.parser import act_index_child_metadata, parse_ie
from nomotheca_ingest.countries.ie.resolver import IeResolver, canary_facts
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
from nomotheca_ingest.core.snapshots import SnapshotClient


class IeAdapter:
    """Ireland implementation of the country adapter protocol."""

    jurisdiction = "IE"
    default_source_code = SOURCE_CODE_EISB

    def __init__(self, resolver: IeResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or IeResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve an Irish citation to exact act or act-index references."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch an act from eISB or an act index from the Oireachtas API."""
        return fetch_ie(ref, http)

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Parse archived eISB XML or Oireachtas JSON into country-neutral IR."""
        return parse_ie(snapshot_bytes, ref, snapshot)

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        """Return follow-up work discovered from the parsed document.

        An act index yields one work item per fiscal act of that year. The
        children cross hosts, so each carries its own source_code rather than
        inheriting the index's.
        """
        work: list[WorkItem] = []
        for child in doc.metadata.get("child_refs", []):
            work.append(
                WorkItem(
                    ref=SourceRef(
                        jurisdiction=doc.ref.jurisdiction,
                        source_code=child.get("source_code") or doc.ref.source_code,
                        source_id=child["source_id"],
                        source_type=child["source_type"],
                        metadata=act_index_child_metadata(child),
                    ),
                    reason=f"{doc.ref.source_id} lists {child.get('title') or child['source_id']}",
                )
            )
        return work

    def canary_facts(self) -> list[CanaryFact]:
        """Return Irish freshness canaries for supported fiscal years."""
        return canary_facts()
