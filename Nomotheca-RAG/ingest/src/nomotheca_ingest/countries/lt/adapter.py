"""Lithuanian adapter wiring resolver, fetcher, parser, and expansion hooks."""

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
from nomotheca_ingest.countries.lt.fetcher import fetch_tar
from nomotheca_ingest.countries.lt.parser import parse_tar_json
from nomotheca_ingest.countries.lt.resolver import LtResolver, canary_facts

LT_URL_SOURCE = UrlSource(
    name="e-seimas / e-tar",
    domains=("e-seimas.lrs.lt", "e-tar.lt"),
    # Two id generations coexist in TAR: "TAR." + 12 uppercase hex for acts
    # migrated in 2014, and a 32-lowercase-hex registration id since.
    id_pattern=re.compile(r"\b(?:TAR\.[0-9A-F]{12}|[0-9a-f]{32})\b"),
)


class LtAdapter(BaseAdapter):
    """Lithuania implementation of the country adapter protocol."""

    #: The kinds a reviewer may state for a contributed document, in the
    #: country's own words, in hierarchy order (see core.contributed.kinds).
    contributed_kinds: ContributedKinds = (
        ("istatymas", NormLevel.STATUTE),
        ("nutarimas", NormLevel.GOVERNMENT_REGULATION),
        ("isakymas", NormLevel.MINISTERIAL_ORDER),
        ("kolektyvine_sutartis", NormLevel.COLLECTIVE_AGREEMENT),
        ("isaiskinimas", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("komentaras", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    )

    jurisdiction = "LT"
    url_source = LT_URL_SOURCE
    default_source_code = "LT-TAR"

    def __init__(self, resolver: LtResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or LtResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Lithuanian citation to exact TAR source identifiers."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch a TAR payload from the data.gov.lt Spinta API."""
        return fetch_tar(ref, http)

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Parse archived TAR JSON into country-neutral IR."""
        return parse_tar_json(snapshot_bytes, ref, snapshot)

    def canary_facts(self) -> list[CanaryFact]:
        """Return Lithuanian freshness canaries for supported fiscal years."""
        return canary_facts()
