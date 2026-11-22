"""Protocol shared by all country-specific legislation adapters."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from typing import Protocol

from nomotheca_ingest.core.ir import (
    CanaryFact,
    CitationRef,
    ContributedKinds,
    ParsedDoc,
    Snapshot,
    SourceRef,
    WorkItem,
)
from nomotheca_ingest.core.snapshots import SnapshotClient


class ResolvedId(Protocol):
    """A national id recovered from a URL, and which tier recovered it."""

    national_id: str
    tier: str


@dataclass(frozen=True, slots=True)
class UrlSource:
    """How one country's official portal shows up in a URL a reviewer pastes.

    Declared by the adapter, because which domains a country publishes on,
    what its ids look like and which URLs are not one document are adapter
    facts. `core/routing.py` reads these and knows no country: adding a sixth
    member state stays an adapter, not an edit to the router.

    The Nomoscope gap-fill scout (`nomoscope_workflow.scout.COUNTRY_SOURCES`)
    keeps its own copy of `domains` and `id_pattern` — it cannot import them,
    since that package must not depend on this one — so changing either here
    means changing it there. `tests/test_routing.py` fails when they diverge.
    """

    #: What to call the source when telling the reviewer we recognised it.
    name: str
    #: Domains served by this portal; subdomains match too.
    domains: tuple[str, ...]
    #: The national id, as it appears in the portal's own URLs.
    id_pattern: re.Pattern[str]
    #: (pattern, hint) pairs for URLs that are recognisably this portal's but
    #: must not be ingested — a whole code is two thousand articles, not one
    #: document. Checked before `id_pattern`.
    refusals: tuple[tuple[re.Pattern[str], str], ...] = ()
    #: What to tell the reviewer when the URL is this portal's but carries no
    #: ingestible id and nothing resolved it.
    no_id_hint: str | None = None
    #: Last resort for a URL with no id in it: (url, database_url) -> id.
    #: None for a portal that always puts its id in the path.
    resolve: Callable[[str, str | None], ResolvedId | None] | None = field(default=None)


class CountryAdapter(Protocol):
    """Country boundary for citation resolution, fetching, parsing, and expansion.

    Everything core reads from an adapter is declared here — core calls these
    directly, never through `getattr`. `BaseAdapter` supplies the defaults.
    """

    jurisdiction: str
    #: The sources.code an adapter fetches from when none is given.
    default_source_code: str
    #: How the country's official portal shows up in a pasted URL; None = never.
    url_source: UrlSource | None
    #: The kinds a reviewer may state for a contributed document, in the
    #: country's own words; () = the default table.
    contributed_kinds: ContributedKinds

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Return exact fetchable source ids for a citation at a point in time."""

    def fetch(self, ref: SourceRef, http: SnapshotClient) -> Snapshot:
        """Fetch and archive raw source bytes before parsing."""

    def parse(self, snapshot_bytes: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
        """Convert archived bytes to country-neutral IR without network or DB access."""

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        """Return structural or amendment-linked follow-up work."""

    def source_code_for(self, national_id: str) -> str:
        """The sources.code a national id is fetched from (FR: KALI ids are FR-KALI)."""

    def source_ref_from_url(self, url: str, source_code: str) -> SourceRef | None:
        """Rebuild a snapshot's SourceRef from its URL, for snapshots archived
        before the ref itself was stored with them (FR only)."""

    def canary_facts(self) -> list[CanaryFact]:
        """Known-truth assertions used to gate resolver freshness."""


class BaseAdapter:
    """Defaults every country adapter shares; an adapter overrides what differs.

    `expand` follows the parser's `child_refs`, one work item per child, each
    fetched from the child's own `source_code` when it names one (IE's act
    index crosses hosts) and otherwise from the parent's. Until 16 Nov 2026
    FR, LT and NL each carried a byte-identical copy of it.
    """

    jurisdiction: str = ""
    url_source: UrlSource | None = None
    contributed_kinds: ContributedKinds = ()

    @property
    def default_source_code(self) -> str:
        return f"{self.jurisdiction.upper()}-LEGI"

    def source_code_for(self, national_id: str) -> str:
        return self.default_source_code

    def expand(self, doc: ParsedDoc) -> list[WorkItem]:
        work: list[WorkItem] = []
        for child in doc.metadata.get("child_refs", []):
            source_id = child["source_id"]
            work.append(
                WorkItem(
                    ref=SourceRef(
                        jurisdiction=doc.ref.jurisdiction,
                        source_code=child.get("source_code") or doc.ref.source_code,
                        source_id=source_id,
                        source_type=child["source_type"],
                        metadata=self.child_metadata(child),
                    ),
                    reason=self.child_reason(doc, child),
                )
            )
        return work

    def child_metadata(self, child: dict) -> dict:
        """What a child's SourceRef carries besides its id (IE: the act's year)."""
        return {}

    def child_reason(self, doc: ParsedDoc, child: dict) -> str:
        return f"{doc.ref.source_id} contains {child['source_type']} {child.get('title') or child['source_id']}"

    def source_ref_from_url(self, url: str, source_code: str) -> SourceRef | None:
        return None

    def canary_facts(self) -> list[CanaryFact]:
        return []
