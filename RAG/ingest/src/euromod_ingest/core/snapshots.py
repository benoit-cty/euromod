"""HTTP snapshot capture for archive-first ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol
from uuid import UUID

import httpx

from euromod_ingest.core.ir import Snapshot, SourceRef


class SnapshotStore(Protocol):
    """Persistence boundary for archived source responses."""

    def write_snapshot(
        self,
        ref: SourceRef,
        url: str,
        status_code: int,
        content_type: str | None,
        content_hash: str,
        content: bytes,
    ) -> UUID:
        """Persist archived response bytes and return fetch_snapshots.id."""


@dataclass(slots=True)
class SnapshotClient:
    """Small HTTP client that archives bytes before returning them to parsers."""

    store: SnapshotStore
    user_agent: str = "euromod-legislation-ingest/0.1"
    timeout_seconds: float = 30.0

    def get(self, ref: SourceRef, url: str) -> Snapshot:
        """Fetch a URL, persist the raw response, and return snapshot metadata."""
        headers = {"User-Agent": self.user_agent}
        with httpx.Client(timeout=self.timeout_seconds, headers=headers, follow_redirects=True) as client:
            response = client.get(url)
        content_hash = sha256(response.content).hexdigest()
        snapshot_id = self.store.write_snapshot(
            ref=ref,
            url=str(response.url),
            status_code=response.status_code,
            content_type=response.headers.get("content-type"),
            content_hash=content_hash,
            content=response.content,
        )
        return Snapshot(
            id=snapshot_id,
            source_code=ref.source_code,
            url=str(response.url),
            http_status=response.status_code,
            content_type=response.headers.get("content-type"),
            content_hash=content_hash,
            raw_content=response.content,
        )
