"""Fetch utilities for the Lithuanian TAR register via the data.gov.lt Spinta API.

The e-tar.lt portal 403s plain HTTP clients; the same register (acts, full texts,
and every dated consolidation) is served keyless as open data (CC BY 4.0) from
``get.data.gov.lt``. See ``Nomotheca-RAG/Lithuania_sources_analysis.md``.

Source ids used by this adapter (they double as e-tar URL path fragments):

- ``TAR.C677663D2202``                 -> the act itself (``Dokumentas`` row)
- ``TAR.C677663D2202/asr``             -> its consolidation index (``Suvestine`` rows, no text)
- ``TAR.C677663D2202/ExnKtBqZbP``      -> one dated consolidation (``Suvestine`` row with text)
"""

from __future__ import annotations

import time
import urllib.parse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomotheca_ingest.core.ir import Snapshot, SourceRef
    from nomotheca_ingest.core.snapshots import SnapshotClient


SPINTA_BASE = "https://get.data.gov.lt/datasets/gov/lrsk/teises_aktai"

# Keep Spinta structural characters intact; everything else (incl. '"') is percent-encoded.
_SAFE = "()=&.,!*"

CONSOLIDATION_INDEX_SUFFIX = "/asr"
#: ``<dokumento_id>/orig``: the act's own text (Dokumentas.tekstas_lt) as the
#: one dated version of an act that has no Suvestinė — TAR only consolidates
#: acts that were amended, so an annual law (the 2025 social-fund budget
#: indicators law, XV-46) has an empty consolidation index and its text lives
#: on the document row alone.
ORIGINAL_TEXT_SUFFIX = "/orig"


def _escape(value: str) -> str:
    """Escape a value for a Spinta string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def spinta_url(model: str, expression: str) -> str:
    """Return a Spinta query URL for a model and raw query expression."""
    return f"{SPINTA_BASE}/{model}?{urllib.parse.quote(expression, safe=_SAFE)}"


def document_url(dokumento_id: str) -> str:
    """Return the query URL for one registered act (metadata + as-published text)."""
    return spinta_url("Dokumentas", f'dokumento_id="{_escape(dokumento_id)}"')


def consolidation_index_url(dokumento_id: str) -> str:
    """Return the query URL listing an act's dated consolidations, without text."""
    expression = (
        f'dokumento_id="{_escape(dokumento_id)}"'
        "&select(dokumento_id,suvestines_id,galioja_nuo,galioja_iki,nuoroda)"
        "&sort(galioja_nuo)"
    )
    return spinta_url("Suvestine", expression)


def consolidation_url(dokumento_id: str, suvestines_id: str) -> str:
    """Return the query URL for one dated consolidation including its full text."""
    expression = f'dokumento_id="{_escape(dokumento_id)}"&suvestines_id="{_escape(suvestines_id)}"'
    return spinta_url("Suvestine", expression)


def url_for_ref(ref: SourceRef) -> str:
    """Map an LT source reference onto the Spinta query URL that serves it."""
    source_id = ref.source_id
    if source_id.endswith(CONSOLIDATION_INDEX_SUFFIX):
        return consolidation_index_url(source_id.removesuffix(CONSOLIDATION_INDEX_SUFFIX))
    if source_id.endswith(ORIGINAL_TEXT_SUFFIX):
        # An act TAR never consolidated (never amended) has its text only on
        # the Dokumentas row itself.
        return document_url(source_id.removesuffix(ORIGINAL_TEXT_SUFFIX))
    if "/" in source_id:
        dokumento_id, suvestines_id = source_id.split("/", 1)
        return consolidation_url(dokumento_id, suvestines_id)
    return document_url(source_id)


# The API intermittently 500s on its largest rows (observed on the GPMĮ's
# open-ended consolidation); a plain retry succeeds. Failed attempts still
# archive their snapshot, which is fine — snapshots are append-only provenance.
_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 5


def fetch_tar(ref: SourceRef, http: SnapshotClient) -> Snapshot:
    """Fetch and archive a TAR payload, retrying transient upstream errors."""
    url = url_for_ref(ref)
    snapshot = http.get(ref, url)
    for attempt in range(1, _MAX_ATTEMPTS):
        if snapshot.http_status not in _RETRY_STATUSES:
            break
        time.sleep(2**attempt)
        snapshot = http.get(ref, url)
    if snapshot.http_status != 200:
        # Nothing downstream checks the status; failing here keeps a 500's HTML
        # body from surfacing as an opaque JSONDecodeError in the parser.
        msg = f"TAR fetch failed with HTTP {snapshot.http_status} after retries: {url}"
        raise RuntimeError(msg)
    return snapshot
