"""French adapter wiring resolver, fetcher, parser, and expansion hooks."""

from __future__ import annotations

import re
from datetime import date

from nomotheca_ingest.countries.base import UrlSource
from nomotheca_ingest.countries.fr.fetcher import fetch_direct_id
from nomotheca_ingest.countries.fr.parser import parse_dila_json
from nomotheca_ingest.countries.fr.resolver import (
    FrResolver,
    canary_facts,
    resolve_legifrance_url,
)
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
from nomotheca_ingest.core.snapshots import SnapshotClient

DILA_ID = re.compile(r"\b(?:LEGI|JORF)(?:ARTI|TEXT|SCTA)\d{12}\b")

WHOLE_CODE_HINT = (
    "that is a whole Legifrance code (LEGITEXT), not one document — paste the "
    "article URL (LEGIARTI...) or the JORF text (JORFTEXT...) instead"
)

ELI_HINT = (
    "this Legifrance ELI URL carries a NOR, not a DILA id, and could not be "
    "resolved — paste the JORFTEXT id or upload the saved file"
)

FR_URL_SOURCE = UrlSource(
    name="Legifrance",
    domains=("legifrance.gouv.fr",),
    # JORF texts and single consolidated code articles (LEGIARTI — where most
    # rates live once codified).
    id_pattern=re.compile(r"\b(?:JORFTEXT|LEGIARTI)\d{12}\b"),
    # A whole code is two thousand articles, not a document. Same exclusion the
    # scout applies when harvesting ids.
    refusals=((re.compile(r"\bLEGITEXT\d{12}\b"), WHOLE_CODE_HINT),),
    no_id_hint=ELI_HINT,
    # ELI URLs carry a NOR, not a DILA id (ADR 0002).
    resolve=resolve_legifrance_url,
)


class FrAdapter:
    """France implementation of the country adapter protocol."""

    jurisdiction = "FR"
    url_source = FR_URL_SOURCE
    default_source_code = "FR-LEGI"

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

    def source_ref_from_url(self, url: str, source_code: str) -> SourceRef | None:
        """Rebuild the SourceRef an archived DILA snapshot was fetched for.

        Snapshots keep only the URL, and every DILA URL carries the id, so a
        re-parse never needs the network: `reparse` replays the parser over
        the archive after a parser change (the NOTA application notes, say).
        """
        match = DILA_ID.search(url)
        if not match:
            return None
        source_id = match.group(0)
        source_type = {"TEXT": "instrument", "SCTA": "section"}.get(source_id[4:8], "article")
        return SourceRef(
            jurisdiction=self.jurisdiction,
            source_code=source_code,
            source_id=source_id,
            source_type=source_type,
        )

    def canary_facts(self) -> list[CanaryFact]:
        """Return French freshness canaries for supported fiscal years."""
        return canary_facts()
