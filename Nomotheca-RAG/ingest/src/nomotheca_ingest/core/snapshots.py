"""HTTP snapshot capture for archive-first ingestion."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID

import httpx

from nomotheca_ingest.core.ir import Snapshot, SourceRef
from nomotheca_ingest.core.text import sha256_hex


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
    #: One HTTP client for every request of a run (connection reuse), opened
    #: on the first request and closed by `close` / the ``with`` block.
    _client: httpx.Client | None = field(default=None, init=False, repr=False)

    def __enter__(self) -> SnapshotClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def _http(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                timeout=self.timeout_seconds, headers={"User-Agent": self.user_agent}, follow_redirects=True
            )
        return self._client

    def get(self, ref: SourceRef, url: str, headers: dict[str, str] | None = None) -> Snapshot:
        """Fetch a URL, persist the raw response, and return snapshot metadata.

        ``headers`` lets an adapter add request headers its source requires —
        content negotiation is a per-source HTTP concern, not a parser one (the
        BOE API 400s unless ``Accept: application/xml`` is sent). They are
        merged over the default User-Agent, which callers may also override.
        """
        response = self._http().get(url, headers=headers)
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
        content_hash = sha256_hex(content)
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


#: Statuses that mean "try again later" on every portal we fetch from.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


def get_with_retries(
    http: SnapshotClient,
    ref: SourceRef,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    attempts: int = 4,
) -> Snapshot:
    """GET one URL, retrying the transient statuses with exponential back-off.

    Every attempt is archived (archive-first: a 503 page is what the portal
    said). Returns the last snapshot whatever its status; the adapter decides
    what a final non-200 means. The one retry loop of every fetcher — until
    16 Nov 2026 ES, IE, LT and NL each carried a copy and FR had none.
    """
    snapshot = http.get(ref, url, headers=headers) if headers else http.get(ref, url)
    for attempt in range(1, attempts):
        if snapshot.http_status not in RETRY_STATUSES:
            break
        time.sleep(2**attempt)
        snapshot = http.get(ref, url, headers=headers) if headers else http.get(ref, url)
    return snapshot
