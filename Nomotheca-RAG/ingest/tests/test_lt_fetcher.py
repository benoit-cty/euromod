"""URL-building and retry tests for the Lithuanian TAR fetcher."""

from uuid import uuid4

from nomotheca_ingest.countries.lt.fetcher import (
    consolidation_index_url,
    consolidation_url,
    document_url,
    fetch_tar,
    url_for_ref,
)
from nomotheca_ingest.core.ir import Snapshot, SourceRef


def _ref(source_id: str, source_type: str = "instrument") -> SourceRef:
    return SourceRef(jurisdiction="LT", source_code="LT-TAR", source_id=source_id, source_type=source_type)


def test_document_url_targets_dokumentas_with_quoted_id():
    url = document_url("TAR.C677663D2202")
    assert url.startswith("https://get.data.gov.lt/datasets/gov/lrsk/teises_aktai/Dokumentas?")
    assert 'dokumento_id=%22TAR.C677663D2202%22' in url


def test_consolidation_index_url_selects_light_fields_sorted():
    url = consolidation_index_url("TAR.C677663D2202")
    assert "/Suvestine?" in url
    assert "select(dokumento_id,suvestines_id,galioja_nuo,galioja_iki,nuoroda)" in url
    assert "sort(galioja_nuo)" in url
    assert "tekstas_lt" not in url


def test_consolidation_url_filters_both_ids():
    url = consolidation_url("TAR.C677663D2202", "ExnKtBqZbP")
    assert 'dokumento_id=%22TAR.C677663D2202%22' in url
    assert 'suvestines_id=%22ExnKtBqZbP%22' in url


def test_url_for_ref_dispatches_on_source_id_shape():
    assert "/Dokumentas?" in url_for_ref(_ref("TAR.C677663D2202"))
    index_url = url_for_ref(_ref("TAR.C677663D2202/asr", "consolidation_index"))
    assert "sort(galioja_nuo)" in index_url
    consolidation = url_for_ref(_ref("TAR.C677663D2202/ExnKtBqZbP", "consolidation"))
    assert 'suvestines_id=%22ExnKtBqZbP%22' in consolidation


class _FlakyClient:
    """SnapshotClient stand-in that 500s before succeeding."""

    def __init__(self, failures: int) -> None:
        self.failures = failures
        self.calls = 0

    def get(self, ref: SourceRef, url: str) -> Snapshot:
        self.calls += 1
        status = 500 if self.calls <= self.failures else 200
        return Snapshot(
            id=uuid4(),
            source_code=ref.source_code,
            url=url,
            http_status=status,
            content_type="application/json",
            content_hash="0" * 64,
            raw_content=b'{"_data": []}',
        )


def test_fetch_tar_retries_transient_upstream_errors(monkeypatch):
    monkeypatch.setattr("nomotheca_ingest.countries.lt.fetcher.time.sleep", lambda _s: None)
    client = _FlakyClient(failures=1)
    snapshot = fetch_tar(_ref("TAR.C677663D2202"), client)
    assert snapshot.http_status == 200
    assert client.calls == 2

    exhausted = _FlakyClient(failures=5)
    snapshot = fetch_tar(_ref("TAR.C677663D2202"), exhausted)
    assert snapshot.http_status == 500
    assert exhausted.calls == 3
