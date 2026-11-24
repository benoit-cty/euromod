"""Dutch adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

import re
from datetime import date

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
from nomotheca_ingest.countries.base import BaseAdapter, UrlSource
from nomotheca_ingest.countries.nl.fetcher import fetch_bwb
from nomotheca_ingest.countries.nl.parser import parse_bwb_xml
from nomotheca_ingest.countries.nl.resolver import NlResolver, canary_facts
from nomotheca_ingest.countries.nl.staatscourant import SOURCE_CODE_STCRT, is_stcrt, parse_stcrt

NL_URL_SOURCE = UrlSource(
    name="wetten.overheid.nl / Staatscourant",
    domains=("wetten.overheid.nl", "officielebekendmakingen.nl"),
    # The BWB regulation id, in the plain path (/BWBR0011353/2025-01-01) and in
    # the Juriconnect form (/jci1.3:c:BWBR0011353&artikel=2.10). BWBV... ids are
    # treaties, deliberately excluded. Or a Staatscourant publication
    # (zoek.officielebekendmakingen.nl/stcrt-2024-39288.html, see
    # staatscourant.py); the other series printed there (kst-, stb-, trb-) are
    # not read.
    id_pattern=re.compile(r"\b(?:BWBR\d{7}|stcrt-\d{4}-\d+(?:-n\d+)?)\b"),
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

    def source_code_for(self, national_id: str) -> str:
        """A ``stcrt-…`` id is a Staatscourant publication, the rest BWB."""
        return SOURCE_CODE_STCRT if is_stcrt(national_id) else self.default_source_code

    def __init__(self, resolver: NlResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or NlResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Dutch citation to exact BWB source identifiers."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch a BWB payload or a Staatscourant publication from the official repository."""
        return fetch_bwb(ref, http)

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Parse archived BWB or Staatscourant XML into country-neutral IR."""
        if is_stcrt(ref.source_id):
            return parse_stcrt(snapshot_bytes, ref, snapshot)
        return parse_bwb_xml(snapshot_bytes, ref, snapshot)

    def canary_facts(self) -> list[CanaryFact]:
        """Return Dutch freshness canaries for supported fiscal years."""
        return canary_facts()
