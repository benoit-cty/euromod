"""Irish adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

import re
from datetime import date

from nomotheca_ingest.countries.ie.fetcher import SOURCE_CODE_EISB, fetch_ie
from nomotheca_ingest.countries.ie.parser import act_index_child_metadata, parse_ie
from nomotheca_ingest.countries.ie.resolver import IeResolver, canary_facts
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


IE_URL_SOURCE = UrlSource(
    name="electronic Irish Statute Book",
    domains=("irishstatutebook.ie",),
    # The eISB ELI act id: Acts of the Oireachtas only. Statutory instruments
    # (/eli/<year>/si/<no>) are not ingestible yet.
    id_pattern=re.compile(r"\b(?:19|20)\d{2}/act/\d{1,3}\b"),
)


class IeAdapter(BaseAdapter):
    """Ireland implementation of the country adapter protocol."""

    #: The kinds a reviewer may state for a contributed document, in the
    #: country's own words, in hierarchy order (see core.contributed.kinds).
    contributed_kinds: ContributedKinds = (
        ("act", NormLevel.STATUTE),
        ("statutory_instrument", NormLevel.GOVERNMENT_REGULATION),
        ("regulation", NormLevel.MINISTERIAL_ORDER),
        ("employment_agreement", NormLevel.COLLECTIVE_AGREEMENT),
        ("tax_and_duty_manual", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("guidance", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    )

    jurisdiction = "IE"
    url_source = IE_URL_SOURCE
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

    # expand: BaseAdapter's. An act index yields one work item per fiscal act
    # of that year; the children cross hosts, so each names its own source_code.

    def child_metadata(self, child: dict) -> dict:
        return act_index_child_metadata(child)

    def child_reason(self, doc: ParsedDoc, child: dict) -> str:
        return f"{doc.ref.source_id} lists {child.get('title') or child['source_id']}"

    def canary_facts(self) -> list[CanaryFact]:
        """Return Irish freshness canaries for supported fiscal years."""
        return canary_facts()
