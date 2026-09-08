"""Protocol shared by all country-specific legislation adapters."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Protocol

from nomotheca_ingest.core.ir import CanaryFact, CitationRef, ParsedDoc, Snapshot, SourceRef, WorkItem
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
