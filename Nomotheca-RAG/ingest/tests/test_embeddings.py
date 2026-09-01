"""Tests for embedding build helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest

from nomotheca_ingest.core.embeddings import (
    BGE_M3_DIM,
    EMBEDDING_BACKENDS,
    EmbeddingProgressCallback,
    SentenceTransformerBackend,
    arch_list_supports,
    build_embeddings,
    cuda_dtype_for,
    embedding_input,
    embedding_input_hash,
    halfvec_literal,
    processor_kwargs_for,
    raise_for_unsupported_cuda_arch,
    resolve_torch_device,
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


class _FakeCursor:
    """Cursor stub serving the candidate scan and recording embedding inserts."""

    def __init__(self, conn: "_FakeConn", *, dict_rows: bool) -> None:
        self._conn = conn
        self._dict_rows = dict_rows
        self._rows: list[dict[str, object]] = []
        self.rowcount = -1

    def __enter__(self) -> "_FakeCursor":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> None:
        if "FROM chunks c" in sql and sql.lstrip().startswith("SELECT"):
            self._rows = list(self._conn.candidates)
        elif "INSERT INTO embeddings" in sql:
            chunk_id = params[-1]
            self.rowcount = 1 if chunk_id in self._conn.live_chunk_ids else 0
            if self.rowcount:
                self._conn.inserted.append(chunk_id)
        else:
            self._rows = []

    def __iter__(self):
        return iter(self._rows)


class _FakeConn:
    """Connection stub with a candidate list and a set of still-live chunks."""

    def __init__(self, candidates: list[dict[str, object]], live_chunk_ids: set[str]) -> None:
        self.candidates = candidates
        self.live_chunk_ids = live_chunk_ids
        self.inserted: list[object] = []

    def cursor(self, row_factory: object = None) -> _FakeCursor:
        return _FakeCursor(self, dict_rows=row_factory is not None)

    def transaction(self) -> _FakeCursor:
        return _FakeCursor(self, dict_rows=False)

    def commit(self) -> None:
        return None


class _ConstantBackend:
    """Backend stub returning one fixed vector per input."""

    def encode(self, inputs: list[str]) -> list[list[float]]:
        return [[0.1] * BGE_M3_DIM for _ in inputs]


def test_build_embeddings_skips_chunks_removed_by_a_concurrent_ingest() -> None:
    """A chunk re-chunked mid-run is skipped, not a foreign-key failure."""
    candidates = [
        {"id": "live-chunk", "context_header": "Code > Art. 1", "content": "un", "input_hash": None},
        {"id": "vanished-chunk", "context_header": "Code > Art. 2", "content": "deux", "input_hash": None},
    ]
    conn = _FakeConn(candidates, live_chunk_ids={"live-chunk"})

    stats = build_embeddings(conn, _ConstantBackend(), batch_size=2)

    assert stats.scanned == 2
    assert stats.embedded == 1
    assert stats.skipped == 1
    assert conn.inserted == ["live-chunk"]


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


class _FakeOutOfMemoryError(RuntimeError):
    """Stand-in for torch.cuda.OutOfMemoryError."""


class _FakeCuda:
    """torch.cuda stub describing one GPU, with a recorded empty_cache count."""

    OutOfMemoryError = _FakeOutOfMemoryError

    def __init__(
        self,
        available: bool = True,
        capability: tuple[int, int] = (6, 1),
        arch_list: tuple[str, ...] = ("sm_50", "sm_60", "sm_61", "sm_70", "compute_70"),
        name: str = "NVIDIA GeForce GTX 1080 Ti",
    ) -> None:
        self._available = available
        self._capability = capability
        self._arch_list = arch_list
        self._name = name
        self.emptied = 0

    def is_available(self) -> bool:
        return self._available

    def get_device_capability(self, device: object = None) -> tuple[int, int]:
        return self._capability

    def get_arch_list(self) -> list[str]:
        return list(self._arch_list)

    def get_device_name(self, device: object = None) -> str:
        return self._name

    def get_device_properties(self, device: object = None) -> SimpleNamespace:
        return SimpleNamespace(
            name=self._name,
            total_memory=11 * 1024**3,
            major=self._capability[0],
            minor=self._capability[1],
        )

    def empty_cache(self) -> None:
        self.emptied += 1


def _install_fake_torch(monkeypatch: pytest.MonkeyPatch, cuda: _FakeCuda) -> _FakeCuda:
    """Register a torch stub so device resolution runs without a real install."""
    fake_torch = ModuleType("torch")
    fake_torch.cuda = cuda
    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    return cuda


class _FakeVector:
    """Minimal stand-in for the numpy rows SentenceTransformer.encode returns."""

    def __init__(self, values: list[float]) -> None:
        self._values = values

    def astype(self, _dtype: object) -> "_FakeVector":
        return self

    def tolist(self) -> list[float]:
        return self._values


def test_resolve_torch_device_prefers_cuda_when_available(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unset device puts the torch backend on the GPU when there is one."""
    _install_fake_torch(monkeypatch, _FakeCuda(available=True))

    assert resolve_torch_device(None, backend="torch") == "cuda"
    assert resolve_torch_device("auto", backend="torch") == "cuda"
    assert resolve_torch_device("cpu", backend="torch") == "cpu"


def test_resolve_torch_device_falls_back_to_cpu(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without a usable GPU the torch backend stays on CPU, and OpenVINO is untouched."""
    _install_fake_torch(monkeypatch, _FakeCuda(available=False))

    assert resolve_torch_device(None, backend="torch") == "cpu"
    assert resolve_torch_device("NPU", backend="openvino") == "NPU"
    assert resolve_torch_device(None, backend="openvino") is None


def test_cuda_dtype_keeps_fp32_on_pascal(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pascal runs fp16 at 1/64 of its fp32 rate, so half precision is not requested."""
    fake_torch = ModuleType("torch")
    fake_torch.cuda = _FakeCuda(capability=(6, 1))
    assert cuda_dtype_for(fake_torch, "cuda") is None

    fake_torch.cuda = _FakeCuda(capability=(8, 6))
    assert cuda_dtype_for(fake_torch, "cuda") == "float16"


def test_load_kwargs_forward_dtype_only_when_set() -> None:
    """The dtype reaches transformers through model_kwargs, and only when chosen."""
    assert sentence_transformer_load_kwargs(backend="torch", device="cuda") == {"device": "cuda"}
    assert sentence_transformer_load_kwargs(backend="torch", device="cuda", torch_dtype="float16") == {
        "device": "cuda",
        "model_kwargs": {"dtype": "float16"},
    }


def test_arch_list_supports_pascal_kernels() -> None:
    """sm_61 needs same-major cubins or older PTX; cu128-style builds have neither."""
    assert arch_list_supports((6, 1), ["sm_50", "sm_60", "sm_61", "sm_90"])
    assert arch_list_supports((6, 1), ["sm_60"])  # binary compatible upward within a major
    assert arch_list_supports((6, 1), ["compute_60"])  # PTX JITs forward
    assert not arch_list_supports((6, 1), ["sm_75", "sm_80", "sm_90", "compute_90"])
    assert not arch_list_supports((6, 1), ["sm_62"])  # newer minor, not backward compatible


def test_unsupported_cuda_arch_names_the_cuda_extra(monkeypatch: pytest.MonkeyPatch) -> None:
    """A torch wheel without Pascal kernels fails at load with the install hint."""
    fake_torch = ModuleType("torch")
    fake_torch.cuda = _FakeCuda(capability=(6, 1), arch_list=("sm_75", "sm_90", "compute_90"))

    with pytest.raises(RuntimeError, match="embeddings-cuda"):
        raise_for_unsupported_cuda_arch(fake_torch, "cuda")


def test_backend_encodes_on_cuda_with_pascal_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """The GPU path loads in fp32, caps the forward pass, and reports the device."""
    captured: dict[str, object] = {}

    class FakeSentenceTransformer:
        def __init__(self, model_path: str, **kwargs: object) -> None:
            captured["model_path"] = model_path
            captured.update(kwargs)

        def encode(self, texts: list[str], **kwargs: object) -> list[_FakeVector]:
            captured["batch_size"] = kwargs["batch_size"]
            return [_FakeVector([0.1] * BGE_M3_DIM) for _ in texts]

    fake_module = ModuleType("sentence_transformers")
    fake_module.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)
    _install_fake_torch(monkeypatch, _FakeCuda(available=True))

    backend = SentenceTransformerBackend(model_path="BAAI/bge-m3", encode_batch_size=8)
    vectors = backend.encode(["un", "deux"])

    assert backend.device == "cuda"
    assert captured["device"] == "cuda"
    assert "model_kwargs" not in captured  # fp32 stays the transformers default on sm_61
    assert captured["batch_size"] == 2  # never larger than the batch actually given
    assert len(vectors) == 2
    assert "GTX 1080 Ti" in backend.description
    assert "sm_61" in backend.description


def test_backend_halves_the_batch_after_a_cuda_oom(monkeypatch: pytest.MonkeyPatch) -> None:
    """An out-of-memory batch is retried smaller, and the smaller size sticks."""
    attempts: list[int] = []

    class FakeSentenceTransformer:
        def __init__(self, model_path: str, **kwargs: object) -> None:
            return None

        def encode(self, texts: list[str], **kwargs: object) -> list[_FakeVector]:
            batch_size = int(kwargs["batch_size"])
            attempts.append(batch_size)
            if batch_size > 4:
                raise _FakeOutOfMemoryError("CUDA out of memory")
            return [_FakeVector([0.1] * BGE_M3_DIM) for _ in texts]

    fake_module = ModuleType("sentence_transformers")
    fake_module.SentenceTransformer = FakeSentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)
    cuda = _install_fake_torch(monkeypatch, _FakeCuda(available=True))

    backend = SentenceTransformerBackend(model_path="BAAI/bge-m3", encode_batch_size=16)
    vectors = backend.encode(["texte"] * 16)

    assert attempts == [16, 8, 4]
    assert len(vectors) == 16
    assert backend.encode_batch_size == 4
    assert cuda.emptied == 2


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