"""Fetch utilities for the Dutch Basiswettenbestand (BWB).

wetten.overheid.nl is the human-facing portal and rate-limits plain HTTP
clients (the Triangulator needed browser impersonation to scrape it). The same
consolidations are published by KOOP as static, keyless XML from the
repository host, which is what this adapter fetches. See
``Nomotheca-RAG/Netherlands_sources_analysis.md``.

Source ids used by this adapter:

- ``BWBR0011353``                 -> the act's version index (``manifest.xml``)
- ``BWBR0011353/2025-01-01_0``    -> one dated consolidation (a ``toestand``)

The label after the slash is BWB's own ``{inwerkingtreding}_{zicht generation}``
expression label, not a version number -- see ``parser.select_toestanden``.
"""

from __future__ import annotations

import time
import urllib.parse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomotheca_ingest.core.ir import Snapshot, SourceRef
    from nomotheca_ingest.core.snapshots import SnapshotClient


REPOSITORY_BASE = "https://repository.officiele-overheidspublicaties.nl/bwb"
SRU_ENDPOINT = "https://zoekservice.overheid.nl/sru/Search"

# The SRU service answers 406 without it, while still returning a valid body;
# the repository ignores it. Sent on every request so neither has a special case.
XML_HEADERS = {"Accept": "application/xml"}


def manifest_url(bwb_id: str) -> str:
    """Return the URL of an act's version index, listing every toestand."""
    return f"{REPOSITORY_BASE}/{bwb_id}/manifest.xml"


def toestand_url(bwb_id: str, label: str) -> str:
    """Return the URL of one dated consolidation of an act."""
    return f"{REPOSITORY_BASE}/{bwb_id}/{label}/xml/{bwb_id}_{label}.xml"


def sru_search_url(query: str, max_records: int = 50) -> str:
    """Return an SRU 2.0 query URL against the BWB collection.

    Discovery only: this adapter fetches legal text from the repository, and
    uses SRU to map an unknown act name onto a BWB id when extending
    ``parser.KNOWN_ACTS``. Prefer ``overheidbwb.afkorting`` or an exact match on
    the returned ``dcterms:title`` -- ``overheidbwb.titel`` is a substring
    search that ranks amending acts ("Wijzigingswet ...") above the base act.
    """
    params = urllib.parse.urlencode(
        {
            "version": "2.0",
            "operation": "searchRetrieve",
            "x-connection": "BWB",
            "query": query,
            "maximumRecords": str(max_records),
        }
    )
    return f"{SRU_ENDPOINT}?{params}"


def url_for_ref(ref: SourceRef) -> str:
    """Map an NL source reference onto the URL that serves it."""
    source_id = ref.source_id
    if "/" in source_id:
        bwb_id, label = source_id.split("/", 1)
        return toestand_url(bwb_id, label)
    return manifest_url(source_id)


_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 5


def fetch_bwb(ref: SourceRef, http: SnapshotClient) -> Snapshot:
    """Fetch and archive a BWB payload, retrying transient upstream errors."""
    url = url_for_ref(ref)
    snapshot = http.get(ref, url, headers=XML_HEADERS)
    for attempt in range(1, _MAX_ATTEMPTS):
        if snapshot.http_status not in _RETRY_STATUSES:
            break
        time.sleep(2**attempt)
        snapshot = http.get(ref, url, headers=XML_HEADERS)
    if snapshot.http_status != 200:
        # Failing here keeps an error page's HTML from reaching the XML parser
        # as an opaque ParseError.
        msg = f"BWB fetch failed with HTTP {snapshot.http_status} after retries: {url}"
        raise RuntimeError(msg)
    return snapshot
