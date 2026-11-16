"""The shared parser helpers in core/text.py."""

from __future__ import annotations

from nomotheca_ingest.core.text import (
    UniqueCitations,
    fold_accents,
    month_alternation,
    month_names,
    path_token,
    pipe_rows,
    sha256_hex,
)


def test_path_token_keeps_or_folds_accents():
    assert path_token("L. 262-2") == "l_262_2"
    assert path_token("Disposición adicional") == "disposici_n_adicional"
    assert path_token("Disposición adicional", fold=True) == "disposicion_adicional"
    assert path_token("—") == "unknown"


def test_fold_accents_keeps_case():
    assert fold_accents("Aragón") == "Aragon"


def test_sha256_hex_hashes_text_as_utf8():
    assert sha256_hex("é") == sha256_hex("é".encode())


def test_pipe_rows_drops_empty_rows():
    assert pipe_rows([["a", "1"], ["", ""], ["b", "2"]]) == ["a | 1", "b | 2"]
    assert pipe_rows([["a", "1"]], edges=True) == ["| a | 1 |"]


def test_month_names_are_keyed_by_language():
    assert month_names(["fr"])["août"] == 8
    assert "january" not in month_names(["fr"])
    assert month_names()["january"] == 1
    assert "décembre" in month_alternation(["fr", "en"])


def test_unique_citations_suffix_repeats_within_the_length_cap():
    citations = UniqueCitations(max_len=11)
    assert citations.claim("Chapter 1") == "Chapter 1"
    assert citations.claim("Chapter 1") == "Chapter (2)"
    assert citations.claim("Chapter 1") == "Chapter (3)"
    plain = UniqueCitations()
    assert [plain.claim("DT 1"), plain.claim("DT 1")] == ["DT 1", "DT 1 (2)"]
