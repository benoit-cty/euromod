"""URL-building and retry tests for the Dutch BWB fetcher."""

from uuid import uuid4

import pytest

from nomotheca_ingest.countries.nl.fetcher import (
    XML_HEADERS,
    fetch_bwb,
    manifest_url,
    sru_search_url,
    toestand_url,
    url_for_ref,
)
from nomotheca_ingest.core.ir import Snapshot, SourceRef


def _ref(source_id: str, source_type: str = "instrument") -> SourceRef:
    return SourceRef(jurisdiction="NL", source_code="NL-BWB", source_id=source_id, source_type=source_type)


def test_manifest_url_targets_the_repository_version_index():
    url = manifest_url("BWBR0011353")
    assert url == "https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0011353/manifest.xml"


def test_toestand_url_repeats_the_bwb_id_in_the_filename():
    url = toestand_url("BWBR0011353", "2025-01-01_0")
    assert url.endswith("/bwb/BWBR0011353/2025-01-01_0/xml/BWBR0011353_2025-01-01_0.xml")


def test_url_for_ref_dispatches_on_source_id_shape():
    assert url_for_ref(_ref("BWBR0011353")).endswith("/manifest.xml")
    toestand = url_for_ref(_ref("BWBR0011353/2025-01-01_0", "toestand"))
    assert toestand.endswith("/BWBR0011353_2025-01-01_0.xml")


def test_sru_search_url_targets_the_bwb_collection():
    url = sru_search_url('overheidbwb.afkorting="AWIR"', max_records=5)
    assert url.startswith("https://zoekservice.overheid.nl/sru/Search?")
    assert "x-connection=BWB" in url
    assert "operation=searchRetrieve" in url
    assert "maximumRecords=5" in url
    assert "overheidbwb.afkorting%3D%22AWIR%22" in url


class _RecordingClient:
    """SnapshotClient stand-in that 500s before succeeding."""

    def __init__(self, failures: int) -> None:
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
            raw_content=b"<work/>",
        )


def test_fetch_bwb_sends_the_xml_accept_header():
    # The SRU service answers 406 without it while still returning a valid body,
    # so a missing header fails silently rather than loudly.
    client = _RecordingClient(failures=0)
    fetch_bwb(_ref("BWBR0011353"), client)
    assert client.headers == [XML_HEADERS]


def test_fetch_bwb_retries_transient_upstream_errors(monkeypatch):
    monkeypatch.setattr("nomotheca_ingest.countries.nl.fetcher.time.sleep", lambda _s: None)
    client = _RecordingClient(failures=1)
    snapshot = fetch_bwb(_ref("BWBR0011353"), client)
    assert snapshot.http_status == 200
    assert client.calls == 2

    exhausted = _RecordingClient(failures=99)
    with pytest.raises(RuntimeError, match="HTTP 500 after retries"):
        fetch_bwb(_ref("BWBR0011353"), exhausted)
    assert exhausted.calls == 5
