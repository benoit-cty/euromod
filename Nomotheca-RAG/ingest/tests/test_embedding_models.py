"""Embedding-model registry: ids stay stable, every model lands in the 1024-d column."""

from __future__ import annotations

import pytest

from nomotheca_ingest.core.embedding_models import (
    DEFAULT_MODEL,
    MODELS,
    STORED_DIM,
    fit_dimension,
    get_model,
)


def test_bge_m3_is_id_1_and_the_default():
    # Every stored vector and WORKFLOW_EMBEDDING_MODEL_ID=1 depend on this.
    assert DEFAULT_MODEL.id == 1 and DEFAULT_MODEL.key == "bge-m3"
    assert get_model(1) is get_model("1") is get_model("bge-m3")


def test_ids_and_keys_are_unique_and_99_stays_the_placeholder():
    assert len({m.id for m in MODELS}) == len(MODELS)
    assert len({m.key for m in MODELS}) == len(MODELS)
    assert 99 not in {m.id for m in MODELS}


def test_unknown_model_names_the_known_ones():
    with pytest.raises(KeyError, match="1=bge-m3"):
        get_model("no-such-model")


def test_smaller_vectors_are_zero_padded_without_changing_cosines():
    spec = get_model("gte-multilingual-base")
    a = fit_dimension([0.6, 0.8] + [0.0] * 766, spec)
    b = fit_dimension([0.8, 0.6] + [0.0] * 766, spec)
    assert len(a) == STORED_DIM
    assert sum(x * y for x, y in zip(a, b)) == pytest.approx(0.96)


def test_larger_matryoshka_vectors_are_truncated_and_renormalised():
    vector = fit_dimension([1.0] * 2560, get_model("qwen3-embedding-4b"))
    assert len(vector) == STORED_DIM
    assert sum(x * x for x in vector) == pytest.approx(1.0)


def test_only_matryoshka_models_may_be_truncated():
    with pytest.raises(ValueError, match="not Matryoshka"):
        fit_dimension([0.1] * 2048, get_model("bge-m3"))


def test_query_prompts_only_on_the_query_side_for_asymmetric_models():
    qwen = get_model("qwen3-embedding-0.6b")
    assert qwen.query_prompt.startswith("Instruct: ") and qwen.document_prompt == ""
    assert get_model("bge-m3").query_prompt == ""
