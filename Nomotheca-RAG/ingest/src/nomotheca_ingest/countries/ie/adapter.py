"""Irish adapter wiring resolver, fetcher, parser, and expansion hooks."""

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
from nomotheca_ingest.countries.ie.fetcher import SOURCE_CODE_EISB, fetch_ie
from nomotheca_ingest.countries.ie.parser import act_index_child_metadata, parse_ie
from nomotheca_ingest.countries.ie.resolver import IeResolver, canary_facts
from nomotheca_ingest.countries.ie.revised import SOURCE_CODE_LRC, is_revised

IE_URL_SOURCE = UrlSource(
    name="electronic Irish Statute Book",
    domains=("irishstatutebook.ie",),
    # The eISB ELI id of an Act (<year>/act/<no>) or of a statutory
    # instrument as made (<year>/si/<no>, see si.py).
    id_pattern=re.compile(r"\b(?:19|20)\d{2}/(?:act/\d{1,3}|si/\d{1,4})\b"),
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

    def source_code_for(self, national_id: str) -> str:
        """A ``…/revised`` id is the Law Reform Commission's text, the rest eISB."""
        return SOURCE_CODE_LRC if is_revised(national_id) else self.default_source_code

    def __init__(self, resolver: IeResolver | None = None) -> None:
        """Create the adapter with an optional resolver implementation."""
        self._resolver = resolver or IeResolver()

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve an Irish citation to exact act or act-index references."""
        return self._resolver.resolve(ref, as_of)

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch an act from eISB, a Revised Act from the LRC, or an act index."""
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
