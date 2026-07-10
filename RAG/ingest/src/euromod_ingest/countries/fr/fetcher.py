"""Direct-id fetch utilities for French DILA JSON documents."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from euromod_ingest.core.ir import Snapshot, SourceRef
    from euromod_ingest.core.snapshots import SnapshotClient


TRICOTEUSES_JSON_BASE = "https://git.tricoteuses.fr/dila/donnees_juridiques/raw/branch/main"


def dila_json_path(source_id: str) -> str:
    """Return the Tricoteuses JSON repository path for a DILA identifier."""
    if len(source_id) < 18:
        msg = f"DILA id is too short: {source_id!r}"
        raise ValueError(msg)
    fond = source_id[:4]
    kind = source_id[4:8]
    digits = source_id[8:18]
    pairs = "/".join(digits[index : index + 2] for index in range(0, len(digits), 2))
    return f"{fond}/{kind}/{pairs}/{source_id}.json"


def dila_json_url(source_id: str) -> str:
    """Return the raw Tricoteuses JSON URL for a DILA identifier."""
    return f"{TRICOTEUSES_JSON_BASE}/{dila_json_path(source_id)}"


def fetch_direct_id(ref: SourceRef, http: SnapshotClient) -> Snapshot:
    """Fetch and archive a DILA JSON document by direct source id."""
    return http.get(ref, dila_json_url(ref.source_id))
