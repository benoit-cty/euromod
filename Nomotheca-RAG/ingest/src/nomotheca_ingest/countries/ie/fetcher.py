"""Fetch utilities for Irish legislation.

Ireland splits resolve and fetch across two hosts (see
``Nomotheca-RAG/Ireland_sources_analysis.md``):

- **eISB** (``irishstatutebook.ie``) serves the authentic *as-enacted* text at
  ELI-pattern URLs, whole-act XML in one request. It has no query API, so it
  cannot answer "which act number is the Finance Act of 2025?".
- The **Oireachtas Open Data API** answers exactly that, keyless, and hands back
  each act's ``statutebookURI`` — the eISB ELI the fetcher then uses.

Neither host blocks plain HTTP clients (unlike FR's Anubis or LT's e-tar), so no
browser impersonation is needed; a retry on transient upstream errors is enough.

Source ids used by this adapter:

- ``2024/act/43``  -> one act's as-enacted XML on eISB          (``IE-EISB``)
- ``index/2024``   -> the year's enacted acts on the API        (``IE-OIREACHTAS``)
- ``2005/act/26/revised`` -> the Law Reform Commission's consolidated text of
  one act, one HTML page (``IE-LRC``, see ``revised.py``)
- ``2007/si/142``  -> one statutory instrument as made, one HTML page on
  eISB (``IE-EISB``, see ``si.py``)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from nomotheca_ingest.core.snapshots import get_with_retries
from nomotheca_ingest.countries.ie.revised import is_revised, revised_url
from nomotheca_ingest.countries.ie.si import is_si, si_url

if TYPE_CHECKING:
    from nomotheca_ingest.core.ir import Snapshot, SourceRef
    from nomotheca_ingest.core.snapshots import SnapshotClient


EISB_BASE = "https://www.irishstatutebook.ie"
OIREACHTAS_BASE = "https://api.oireachtas.ie/v1"

SOURCE_CODE_EISB = "IE-EISB"
SOURCE_CODE_OIREACHTAS = "IE-OIREACHTAS"

ACT_INDEX_PREFIX = "index/"

# The API pages its results; a single act year has never exceeded ~70 enacted
# acts, so one request with a generous limit avoids paging entirely.
ACT_INDEX_LIMIT = 200


def act_url(act_id: str) -> str:
    """Return the eISB whole-act XML URL for an ``{year}/act/{no}`` id."""
    return f"{EISB_BASE}/eli/{act_id}/enacted/en/xml"


def act_eli(act_id: str) -> str:
    """Return the canonical eISB ELI recorded as the act's citation URL."""
    return f"{EISB_BASE}/eli/{act_id}"


def section_eli(act_id: str, number: str) -> str:
    """Return the eISB ELI of one section, the human-facing citation target."""
    return f"{EISB_BASE}/eli/{act_id}/section/{number}/enacted/en/html"


def act_index_url(year: int | str) -> str:
    """Return the Oireachtas query URL listing one year's enacted acts."""
    return f"{OIREACHTAS_BASE}/legislation?act_year={year}&bill_status=Enacted&limit={ACT_INDEX_LIMIT}"


def url_for_ref(ref: SourceRef) -> str:
    """Map an IE source reference onto the URL that serves it."""
    if ref.source_id.startswith(ACT_INDEX_PREFIX):
        return act_index_url(ref.source_id.removeprefix(ACT_INDEX_PREFIX))
    if is_revised(ref.source_id):
        return revised_url(ref.source_id)
    if is_si(ref.source_id):
        return si_url(ref.source_id)
    return act_url(ref.source_id)




def fetch_ie(ref: SourceRef, http: SnapshotClient) -> Snapshot:
    """Fetch and archive an Irish payload, retrying transient upstream errors."""
    url = url_for_ref(ref)
    snapshot = get_with_retries(http, ref, url, attempts=4)
    if snapshot.http_status != 200:
        # eISB answers unknown act numbers with a 404 HTML page; failing here
        # keeps that from reaching the parser as an opaque XML syntax error.
        msg = f"IE fetch failed with HTTP {snapshot.http_status} after retries: {url}"
        raise RuntimeError(msg)
    return snapshot
