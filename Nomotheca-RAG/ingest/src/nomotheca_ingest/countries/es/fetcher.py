"""Fetch utilities for Spanish legislation via the BOE open-data API.

Spain publishes its consolidated legislation ("legislación consolidada")
keyless and free at ``boe.es/datosabiertos``. See
``Nomotheca-RAG/Spain_sources_analysis.md``.

Unlike FR (Anubis) and LT (e-tar 403s), nothing here blocks plain HTTP
clients — but the API is **XML-only and picky about it**: without
``Accept: application/xml`` every request fails with HTTP 400
("No soportado ningún mime type de la cabecera Accept"). No header value
other than ``application/xml`` works, and there is no query-parameter
override (``?format=``/``?formato=``/``?output=``/``.xml`` were all
verified to fail), so the header is mandatory rather than cosmetic.

Source ids used by this adapter are plain BOE analytical identifiers:

- ``BOE-A-2006-20764``  -> the whole consolidated act (metadata + every
  block + every dated version of every block) in one response.

One GET is the entire act, so this adapter needs no expansion generation.

BOE consolidates only some acts. An annual order or resolution that is never
amended — the yearly cotización orders (Orden ESS/55/2018, Orden
TMS/1289/2018), where the contribution bases and ceilings live — has
``estado_consolidacion`` 0 and the consolidated API answers 404 for it. Those
are fetched from the daily-gazette XML (``/diario_boe/xml.php?id=``) instead:
the act as published, one text, which the parser reads as a single version.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomotheca_ingest.core.ir import Snapshot, SourceRef
    from nomotheca_ingest.core.snapshots import SnapshotClient


API_BASE = "https://www.boe.es/datosabiertos/api/legislacion-consolidada"

SOURCE_CODE = "ES-BOE"

# The one header the API insists on; see the module docstring.
XML_HEADERS = {"Accept": "application/xml"}


def instrument_url(boe_id: str) -> str:
    """Return the API URL serving one consolidated act in full."""
    return f"{API_BASE}/id/{boe_id}"


def diario_url(boe_id: str) -> str:
    """Return the daily-gazette XML of an act as published (never consolidated)."""
    return f"https://www.boe.es/diario_boe/xml.php?id={boe_id}"


def html_url(boe_id: str) -> str:
    """Return the human-facing consolidated view, recorded as provenance."""
    return f"https://www.boe.es/buscar/act.php?id={boe_id}"


def url_for_ref(ref: SourceRef) -> str:
    """Map an ES source reference onto the URL that serves it."""
    return instrument_url(ref.source_id)


_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
_MAX_ATTEMPTS = 4


def fetch_boe(ref: SourceRef, http: SnapshotClient) -> Snapshot:
    """Fetch and archive a BOE payload, retrying transient upstream errors.

    An act the consolidated API does not know (404) is fetched from the
    daily-gazette XML: an unconsolidated annual order is only there.
    """
    url = url_for_ref(ref)
    snapshot = _get_with_retries(ref, url, http)
    if snapshot.http_status == 404:
        url = diario_url(ref.source_id)
        snapshot = _get_with_retries(ref, url, http)
    if snapshot.http_status != 200:
        # The API answers unknown ids and bad Accept headers with a 400/404
        # XML error envelope; failing here keeps that from reaching the parser
        # as a confusing "no metadatos element" error.
        msg = f"BOE fetch failed with HTTP {snapshot.http_status} after retries: {url}"
        raise RuntimeError(msg)
    return snapshot


def _get_with_retries(ref: SourceRef, url: str, http: SnapshotClient) -> Snapshot:
    """GET one URL, retrying the statuses that mean "try again later"."""
    snapshot = http.get(ref, url, headers=XML_HEADERS)
    for attempt in range(1, _MAX_ATTEMPTS):
        if snapshot.http_status not in _RETRY_STATUSES:
            break
        time.sleep(2**attempt)
        snapshot = http.get(ref, url, headers=XML_HEADERS)
    return snapshot
