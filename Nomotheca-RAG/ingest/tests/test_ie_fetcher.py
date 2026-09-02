"""URL-building and retry tests for the Irish eISB / Oireachtas fetcher."""

from uuid import uuid4

import pytest

from nomotheca_ingest.countries.ie.adapter import IeAdapter
from nomotheca_ingest.countries.ie.fetcher import (
    act_eli,
    act_index_url,
    act_url,
    fetch_ie,
    section_eli,
    url_for_ref,
)
from nomotheca_ingest.core.ir import Snapshot, SourceRef


def _ref(source_id: str, source_type: str = "act", source_code: str = "IE-EISB") -> SourceRef:
    return SourceRef(
        jurisdiction="IE", source_code=source_code, source_id=source_id, source_type=source_type
    )


def test_act_url_follows_the_eli_pattern_for_whole_act_xml():
    # Section-level XML does not exist on eISB (404); the whole act is one GET.
    assert act_url("2024/act/43") == "https://www.irishstatutebook.ie/eli/2024/act/43/enacted/en/xml"
    assert act_eli("2024/act/43") == "https://www.irishstatutebook.ie/eli/2024/act/43"
    assert (
        section_eli("1997/act/39", "531AN")
        == "https://www.irishstatutebook.ie/eli/1997/act/39/section/531AN/enacted/en/html"
    )


def test_act_index_url_queries_enacted_acts_for_one_year():
    url = act_index_url(2024)
    assert url.startswith("https://api.oireachtas.ie/v1/legislation?")
    assert "act_year=2024" in url
    assert "bill_status=Enacted" in url
    assert "limit=200" in url


def test_url_for_ref_dispatches_across_the_two_hosts():
    assert url_for_ref(_ref("2024/act/43")).startswith("https://www.irishstatutebook.ie/eli/")
    index_url = url_for_ref(_ref("index/2024", "act_index", "IE-OIREACHTAS"))
    assert index_url.startswith("https://api.oireachtas.ie/")


def test_adapter_defaults_to_the_eisb_source_code():
    # The Nomoscope scout invokes the CLI without --source-code; a wrong default
    # fails the run with "Unknown source code".
    adapter = IeAdapter()
    assert adapter.jurisdiction == "IE"
    assert adapter.default_source_code == "IE-EISB"


class _FlakyClient:
    """SnapshotClient stand-in that fails before succeeding."""

    def __init__(self, failures: int, status: int = 503) -> None:
        self.failures = failures
        self.status = status
        self.calls = 0

    def get(self, ref: SourceRef, url: str) -> Snapshot:
        self.calls += 1
        status = self.status if self.calls <= self.failures else 200
        return Snapshot(
            id=uuid4(),
            source_code=ref.source_code,
            url=url,
            http_status=status,
            content_type="application/xml",
            content_hash="0" * 64,
            raw_content=b"<act/>",
        )


def test_fetch_ie_retries_transient_upstream_errors(monkeypatch):
    monkeypatch.setattr("nomotheca_ingest.countries.ie.fetcher.time.sleep", lambda _s: None)
    client = _FlakyClient(failures=1)
    assert fetch_ie(_ref("2024/act/43"), client).http_status == 200
    assert client.calls == 2

    exhausted = _FlakyClient(failures=99)
    with pytest.raises(RuntimeError, match="HTTP 503 after retries"):
        fetch_ie(_ref("2024/act/43"), exhausted)
    assert exhausted.calls == 4


def test_fetch_ie_fails_fast_on_an_unknown_act_number(monkeypatch):
    # eISB answers an unknown act with a 404 HTML page; raising here keeps that
    # from reaching the parser as an opaque XML syntax error.
    monkeypatch.setattr("nomotheca_ingest.countries.ie.fetcher.time.sleep", lambda _s: None)
    client = _FlakyClient(failures=99, status=404)
    with pytest.raises(RuntimeError, match="HTTP 404"):
        fetch_ie(_ref("2024/act/999"), client)
    assert client.calls == 1
