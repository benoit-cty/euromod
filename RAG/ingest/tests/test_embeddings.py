"""Tests for embedding build helpers."""

from __future__ import annotations

import pytest

from euromod_ingest.core.embeddings import BGE_M3_DIM, EMBEDDING_BACKENDS, embedding_input, embedding_input_hash, halfvec_literal


def test_embedding_input_hash_uses_exact_model_input() -> None:
    """The staleness hash follows the context-header plus content model input."""
    input_text = embedding_input("Code > Art. 197", "Le texte fiscal")

    assert input_text == "Code > Art. 197\nLe texte fiscal"
    assert embedding_input_hash(input_text) == embedding_input_hash("Code > Art. 197\nLe texte fiscal")


def test_halfvec_literal_serializes_bge_m3_dimension() -> None:
    """Vectors are serialized in pgvector literal form for halfvec casting."""
    literal = halfvec_literal([0.125] * BGE_M3_DIM)

    assert literal.startswith("[0.125,0.125")
    assert literal.endswith("]")


def test_halfvec_literal_rejects_wrong_dimension() -> None:
    """BGE-M3 embeddings must be 1024-dimensional before insertion."""
    with pytest.raises(ValueError, match="Expected 1024 dimensions"):
        halfvec_literal([0.1, 0.2])


def test_supported_embedding_backends_are_explicit() -> None:
    """The CLI exposes only backends supported by sentence-transformers here."""
    assert EMBEDDING_BACKENDS == ("torch", "openvino")