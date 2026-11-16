"""Dutch adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

import re
from datetime import date

from nomotheca_ingest.countries.nl.fetcher import fetch_bwb
from nomotheca_ingest.countries.nl.parser import parse_bwb_xml
from nomotheca_ingest.countries.nl.resolver import NlResolver, canary_facts
from nomotheca_ingest.countries.base import BaseAdapter, UrlSource
from nomotheca_ingest.core.ir import (
    CanaryFact,
    CitationRef,
    ContributedKinds,
    NormLevel,
    ParsedDoc,
    Snapshot,
    SourceRef,
)
from nomotheca_ingest.core.snapshots import SnapshotClient


NL_URL_SOURCE = UrlSource(
    name="wetten.overheid.nl",
    domains=("wetten.overheid.nl",),
    # The BWB regulation id, in the plain path (/BWBR0011353/2025-01-01) and in
    # the Juriconnect form (/jci1.3:c:BWBR0011353&artikel=2.10). BWBV... ids are
    # treaties, deliberately excluded.
    id_pattern=re.compile(r"\bBWBR\d{7}\b"),
)


class NlAdapter(BaseAdapter):
    """Netherlands implementation of the country adapter protocol."""

    #: The kinds a reviewer may state for a contributed document, in the
    #: country's own words, in hierarchy order (see core.contributed.kinds).
    contributed_kinds: ContributedKinds = (
        ("wet", NormLevel.STATUTE),
        ("algemene_maatregel_van_bestuur", NormLevel.GOVERNMENT_REGULATION),
        ("ministeriele_regeling", NormLevel.MINISTERIAL_ORDER),
        ("cao", NormLevel.COLLECTIVE_AGREEMENT),
        ("beleidsregel", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("besluit", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    )

    jurisdiction = "NL"
    url_source = NL_URL_SOURCE
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

    def canary_facts(self) -> list[CanaryFact]:
        """Return Dutch freshness canaries for supported fiscal years."""
        return canary_facts()
