"""URL-building, header, and retry tests for the Spanish BOE fetcher."""

from uuid import uuid4

import pytest

from nomotheca_ingest.countries.es.fetcher import (
    XML_HEADERS,
    fetch_boe,
    html_url,
    instrument_url,
    url_for_ref,
)
from nomotheca_ingest.core.ir import Snapshot, SourceRef


def _ref(source_id: str = "BOE-A-2006-20764") -> SourceRef:
    return SourceRef(jurisdiction="ES", source_code="ES-BOE", source_id=source_id, source_type="instrument")


def test_instrument_url_targets_the_consolidated_api():
    url = instrument_url("BOE-A-2006-20764")
    assert url == (
        "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2006-20764"
    )


def test_url_for_ref_uses_the_bare_boe_id():
    assert url_for_ref(_ref()).endswith("/id/BOE-A-2006-20764")


def test_html_url_is_the_human_facing_citation_target():
    assert html_url("BOE-A-2006-20764") == "https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764"


class _RecordingClient:
    """SnapshotClient stand-in recording headers, failing a few times first."""

    def __init__(self, failures: int = 0) -> None:
        self.failures = failures
        self.calls = 0
        self.headers: list[dict[str, str] | None] = []

    def get(self, ref: SourceRef, url: str, headers: dict[str, str] | None = None) -> Snapshot:
        self.calls += 1
        self.headers.append(headers)
        status = 500 if self.calls <= self.failures else 200
        return Snapshot(
            id=uuid4(),
            source_code=ref.source_code,
            url=url,
            http_status=status,
            content_type="application/xml",
            content_hash="0" * 64,
            raw_content=b"<response/>",
        )


def test_fetch_sends_the_accept_header_the_api_demands():
    # Without this header every BOE request fails with HTTP 400; there is no
    # query-parameter override, so it is load-bearing rather than cosmetic.
    client = _RecordingClient()
    fetch_boe(_ref(), client)
    assert client.headers == [{"Accept": "application/xml"}]
    assert XML_HEADERS["Accept"] == "application/xml"


def test_fetch_boe_retries_transient_upstream_errors(monkeypatch):
    monkeypatch.setattr("nomotheca_ingest.countries.es.fetcher.time.sleep", lambda _s: None)
    client = _RecordingClient(failures=1)
    snapshot = fetch_boe(_ref(), client)
    assert snapshot.http_status == 200
    assert client.calls == 2
    assert all(header == {"Accept": "application/xml"} for header in client.headers)

    exhausted = _RecordingClient(failures=99)
    with pytest.raises(RuntimeError, match="HTTP 500 after retries"):
        fetch_boe(_ref(), exhausted)
    assert exhausted.calls == 4


def test_snapshot_client_merges_adapter_headers_over_the_user_agent():
    from nomotheca_ingest.core.snapshots import SnapshotClient

    captured: dict[str, object] = {}

    class _Response:
        status_code = 200
        content = b"<response/>"
        headers = {"content-type": "application/xml"}
        url = "https://example.test"

    class _HttpxClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def get(self, url):
            return _Response()

    class _Store:
        def write_snapshot(self, **kwargs):
            return uuid4()

    import nomotheca_ingest.core.snapshots as snapshots_module

    original = snapshots_module.httpx.Client
    snapshots_module.httpx.Client = _HttpxClient
    try:
        SnapshotClient(_Store()).get(_ref(), "https://example.test", headers=XML_HEADERS)
    finally:
        snapshots_module.httpx.Client = original

    assert captured["headers"]["Accept"] == "application/xml"
    assert "User-Agent" in captured["headers"]
