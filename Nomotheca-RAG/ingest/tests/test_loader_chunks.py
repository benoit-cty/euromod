"""The loader's chunk upsert keeps every chunk of the text it just chunked."""

from __future__ import annotations

from types import SimpleNamespace

from nomotheca_ingest.core import loader as loader_mod
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats


class _ChunkTable:
    """In-memory `chunks` rows for one unit text, driven by the loader's SQL."""

    def __init__(self, seqs: list[int] | None = None) -> None:
        self.seqs: set[int] = set(seqs or [])
        self._last: tuple = (0,)

    def cursor(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def execute(self, sql: str, params: tuple) -> None:
        if sql.lstrip().startswith("INSERT INTO chunks"):
            self.seqs.add(params[1])
        elif "DELETE FROM chunks" in sql:
            keep = set(params[1])
            self.seqs = {s for s in self.seqs if s in keep}
        elif sql.startswith("SELECT count(*)"):
            keep = set(params[1])
            self._last = (sum(1 for s in self.seqs if s not in keep),)

    def fetchone(self):
        return self._last


def _replace(table: _ChunkTable, content: str, monkeypatch) -> None:
    monkeypatch.setattr(loader_mod, "_context_header", lambda *a: "Code > art. 1")
    LegislationLoader(table)._replace_chunks(
        "text-id", None, None, None, SimpleNamespace(content=content, lang="fr"), LoadStats()
    )


def test_split_text_keeps_its_last_chunk(monkeypatch):
    # CGI art. 83 (10 952 chars) kept only seq 1: its 3° — the 10 % — was gone.
    table = _ChunkTable()
    _replace(table, "a" * 6_000 + "\n" + "b" * 4_000, monkeypatch)
    assert table.seqs == {1, 2}


def test_text_grown_past_one_chunk_drops_the_lone_chunk(monkeypatch):
    table = _ChunkTable([0])
    _replace(table, "a" * 6_000 + "\n" + "b" * 4_000, monkeypatch)
    assert table.seqs == {1, 2}


def test_text_shrunk_to_one_chunk_drops_the_split_ones(monkeypatch):
    table = _ChunkTable([1, 2, 3])
    _replace(table, "short", monkeypatch)
    assert table.seqs == {0}


def test_an_empty_text_has_no_chunk():
    # A (0, 0) chunk breaks chunks_check and fails the whole act's load.
    from nomotheca_ingest.core.chunker import chunk_text

    assert chunk_text("", "header") == []
