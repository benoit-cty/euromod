"""Spanish adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

import re
from datetime import date

from nomotheca_ingest.countries.es.fetcher import SOURCE_CODE, fetch_boe
from nomotheca_ingest.countries.es.parser import parse_boe_xml
from nomotheca_ingest.countries.es.resolver import EsResolver, canary_facts
from nomotheca_ingest.countries.base import UrlSource
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
from nomotheca_ingest.core.snapshots import SnapshotClient


ES_URL_SOURCE = UrlSource(
    name="BOE",
    # boe.es serves both the human view (/buscar/act.php?id=) and the
    # open-data API this adapter fetches, so one domain covers both.
    domains=("boe.es",),
    # The analytical id, -A- series only: "disposiciones generales", the only
    # series the legislacion-consolidada API serves.
    id_pattern=re.compile(r"\bBOE-A-\d{4}-\d+\b"),
)


class EsAdapter:
    """Spain implementation of the country adapter protocol."""

    jurisdiction = "ES"
    url_source = ES_URL_SOURCE
    default_source_code = SOURCE_CODE

    def __init__(self, resolver: EsResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or EsResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Spanish citation to an exact BOE identifier."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch a consolidated act from the BOE open-data API."""
        return fetch_boe(ref, http)

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Parse archived BOE XML into country-neutral IR."""
        return parse_boe_xml(snapshot_bytes, ref, snapshot)

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        """Return follow-up work — always none for Spain.

        One BOE response is the whole act: metadata, every block, and every
        dated version of every block. There is nothing left to fetch, so the
        adapter deliberately has no expansion generation (contrast LT, whose
        consolidation index must be walked).
        """
        return []

    def canary_facts(self) -> list[CanaryFact]:
        """Return Spanish freshness canaries for supported fiscal years."""
        return canary_facts()
