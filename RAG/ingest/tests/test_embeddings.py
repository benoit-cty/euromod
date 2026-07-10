"""Tests for embedding build helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest

from euromod_ingest.core.embeddings import (
    BGE_M3_DIM,
    EMBEDDING_BACKENDS,
    EmbeddingProgressCallback,
    SentenceTransformerBackend,
    embedding_input,
    embedding_input_hash,
    halfvec_literal,
    processor_kwargs_for,
    sentence_transformer_load_kwargs,
)


def load_openvino_export_script() -> ModuleType:
    """Load the standalone OpenVINO export script for helper tests."""
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "optimize_bge_m3_openvino.py"
    spec = importlib.util.spec_from_file_location("optimize_bge_m3_openvino", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_sentence_transformer_backend_sets_tokenizer_regex_fix(monkeypatch: pytest.MonkeyPatch) -> None:
    """Runtime model loading carries explicit processor kwargs only when requested."""
    captured: dict[str, object] = {}

    class FakeSentenceTransformer:
        def __init__(self, model_path: str, **kwargs: object) -> None:
            captured["model_path"] = model_path
            captured.update(kwargs)

    fake_module = ModuleType("sentence_transformers")
    fake_module.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)

    SentenceTransformerBackend(
        model_path="models/mistral-openvino",
        device="cpu",
        backend="openvino",
        fix_mistral_regex=True,
        slow_tokenizer=True,
    )

    assert captured["model_path"] == "models/mistral-openvino"
    assert captured["backend"] == "openvino"
    assert captured["device"] == "cpu"
    assert captured["model_kwargs"] == {"device": "CPU"}
    assert captured["processor_kwargs"] == {"fix_mistral_regex": True, "use_fast": False}


def test_processor_kwargs_default_empty_for_bge_m3() -> None:
    """BGE-M3 should not opt in to the Mistral regex flag by default."""
    assert processor_kwargs_for() == {}


def test_sentence_transformer_backend_rejects_mistral_fix_for_bge_m3() -> None:
    """The Mistral regex flag currently breaks BGE-M3's XLM-R tokenizer."""
    with pytest.raises(ValueError, match="Do not use fix_mistral_regex with BGE-M3"):
        SentenceTransformerBackend(model_path="models/bge-m3-openvino", fix_mistral_regex=True)


def test_openvino_export_uses_openvino_device_kwargs() -> None:
    """OpenVINO export must not pass NPU as the Torch wrapper device."""
    export_script = load_openvino_export_script()

    assert export_script.TORCH_EXPORT_DEVICE == "cpu"
    assert export_script.OPENVINO_EXPORT_DEVICE == "CPU"
    assert export_script.openvino_export_model_kwargs() == {"export": True, "device": "CPU", "compile": False}
    assert export_script.openvino_validation_model_kwargs("npu") == {"device": "NPU"}


def test_openvino_runtime_uses_model_kwargs_for_npu() -> None:
    """OpenVINO runtime devices are forwarded below the Torch wrapper."""
    assert sentence_transformer_load_kwargs(backend="openvino", device="NPU") == {
        "device": "cpu",
        "model_kwargs": {"device": "NPU"},
    }
    assert sentence_transformer_load_kwargs(backend="torch", device="cpu") == {"device": "cpu"}


def test_openvino_npu_compiler_loader_failure_is_explained() -> None:
    """Known Linux OpenVINO NPU packaging issue gets a compact warning."""
    export_script = load_openvino_export_script()

    detail = export_script._validation_failure_detail(
        RuntimeError("cannot load libopenvino_intel_npu_compiler_loader.so")
    )

    assert "missing libopenvino_intel_npu_compiler_loader.so" in detail
    assert "openvino/issues/36374" in detail


def test_embedding_progress_event_shape() -> None:
    """Progress callbacks receive compact state updates from the builder."""
    events: list[dict[str, int | str]] = []
    callback: EmbeddingProgressCallback = events.append

    callback({"phase": "encoding", "scanned": 32, "embedded": 16, "batch_size": 16})

    assert events == [{"phase": "encoding", "scanned": 32, "embedded": 16, "batch_size": 16}]