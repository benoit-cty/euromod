"""HTTP snapshot capture for archive-first ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol
from uuid import UUID

import httpx

from nomotheca_ingest.core.ir import Snapshot, SourceRef


#: Default User-Agent for every archive-first fetch, wherever it starts.
USER_AGENT = "nomotheca-legislation-ingest/0.1"


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
    user_agent: str = USER_AGENT
    timeout_seconds: float = 30.0

    def get(self, ref: SourceRef, url: str, headers: dict[str, str] | None = None) -> Snapshot:
        """Fetch a URL, persist the raw response, and return snapshot metadata.

        ``headers`` lets an adapter add request headers its source requires —
        content negotiation is a per-source HTTP concern, not a parser one (the
        BOE API 400s unless ``Accept: application/xml`` is sent). They are
        merged over the default User-Agent, which callers may also override.
        """
        headers = {"User-Agent": self.user_agent, **(headers or {})}
        with httpx.Client(timeout=self.timeout_seconds, headers=headers, follow_redirects=True) as client:
            response = client.get(url)
        return self._persist(
            ref, str(response.url), response.status_code, response.headers.get("content-type"), response.content
        )

    def archive(self, ref: SourceRef, url: str, content: bytes, content_type: str) -> Snapshot:
        """Persist bytes a source serves only in bulk, as a 200 snapshot at ``url``.

        For sources with no per-document endpoint (KALI is published as dumps
        only): the adapter reads the document out of its local copy and the
        archive still holds exactly what the parser saw.
        """
        return self._persist(ref, url, 200, content_type, content)

    def _persist(
        self, ref: SourceRef, url: str, status_code: int, content_type: str | None, content: bytes
    ) -> Snapshot:
        content_hash = sha256(content).hexdigest()
        snapshot_id = self.store.write_snapshot(
            ref=ref,
            url=url,
            status_code=status_code,
            content_type=content_type,
            content_hash=content_hash,
            content=content,
        )
        return Snapshot(
            id=snapshot_id,
            source_code=ref.source_code,
            url=url,
            http_status=status_code,
            content_type=content_type,
            content_hash=content_hash,
            raw_content=content,
        )
