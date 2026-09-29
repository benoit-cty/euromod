"""Build vector embeddings for retrieval chunks."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from importlib import import_module
import sys
from types import ModuleType
from typing import Any, Protocol
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from nomotheca_ingest.core.embedding_models import (
    DEFAULT_MODEL,
    STORED_DIM,
    EmbeddingModelSpec,
    fit_dimension,
    get_model,
)


BGE_M3_MODEL = DEFAULT_MODEL.hf_id
BGE_M3_DIM = STORED_DIM
EMBEDDING_BACKENDS = ("torch", "openvino")
PRECISIONS = ("auto", "fp32", "fp16", "bf16")
TORCH_WRAPPER_DEVICE = "cpu"
AUTO_DEVICE = "auto"
# `auto` only picks half precision from Volta (sm_70) on. Pascal's native fp16
# ALUs run at 1/64 of fp32. A bare 4096² fp16 matmul does run fast on the GTX
# 1080 Ti (sm_61; cuBLAS computes it in fp32: 8.3 TFLOPS vs 5.1), but a whole
# model does not: BGE-M3 embedded 1.7 real chunks/s in fp16 against 7.5 in fp32
# (vectors agree to cosine 0.9997), so Pascal stays fp32.
CUDA_FP16_MIN_CAPABILITY = (7, 0)
CUDA_BF16_MIN_CAPABILITY = (8, 0)
#: Longest input fed to the model, in tokens. Chunks are articles (the longest
#: is a few thousand tokens); a 32k window would only let one outlier allocate
#: an attention matrix the card cannot hold.
DEFAULT_MAX_SEQ_LENGTH = 8192
CUDA_INSTALL_HINT = (
    "Install the CUDA build in its own environment: "
    "UV_PROJECT_ENVIRONMENT=.venv-cuda uv sync --extra embeddings-cuda"
)


@dataclass(frozen=True, slots=True)
class ChunkForEmbedding:
    """A chunk row and the text that should be embedded."""

    id: UUID
    input_text: str
    input_hash: str


@dataclass(frozen=True, slots=True)
class EmbeddingBuildStats:
    """Counts returned by an embedding build run."""

    scanned: int = 0
    embedded: int = 0
    skipped: int = 0


EmbeddingProgressCallback = Callable[[dict[str, int | str]], None]


class EmbeddingBackend(Protocol):
    """Minimal interface used by the database embedding builder."""

    def encode(self, inputs: Sequence[str]) -> list[list[float]]:
        """Return one 1024-dimensional passage embedding per input string."""


class SentenceTransformerBackend:
    """Local sentence-transformers backend for any registry model (BGE-M3 by default)."""

    def __init__(
        self,
        model_path: str | None = None,
        device: str | None = None,
        backend: str = "torch",
        fix_mistral_regex: bool = False,
        slow_tokenizer: bool = False,
        encode_batch_size: int | None = None,
        spec: EmbeddingModelSpec | None = None,
        precision: str = "auto",
        max_seq_length: int | None = DEFAULT_MAX_SEQ_LENGTH,
    ) -> None:
        """Load a registry model, from a local path or its Hugging Face id.

        `spec` says which model this is (prompts, dimension); `model_path` only
        overrides where its weights come from (a local or OpenVINO export).
        With the torch backend and no explicit device, an available CUDA GPU is
        used; `encode_batch_size` caps how many texts reach the GPU at once,
        independently of the caller's database batch size.
        """
        self.spec = spec or DEFAULT_MODEL
        model_path = model_path or self.spec.hf_id
        if precision not in PRECISIONS:
            msg = f"precision must be one of {', '.join(PRECISIONS)}"
            raise ValueError(msg)
        if backend not in EMBEDDING_BACKENDS:
            msg = f"Unsupported embedding backend: {backend}"
            raise ValueError(msg)
        if fix_mistral_regex and _looks_like_bge_m3(model_path):
            msg = "Do not use fix_mistral_regex with BGE-M3; it breaks the XLM-R tokenizer in this stack."
            raise ValueError(msg)
        try:
            sentence_transformers = import_module("sentence_transformers")
        except ImportError as exc:  # pragma: no cover - exercised by operator environment
            msg = "Install embedding dependencies with: uv sync --extra embeddings"
            raise RuntimeError(msg) from exc

        self.backend = backend
        self.device = resolve_torch_device(device, backend=backend)
        self.encode_batch_size = encode_batch_size
        self._torch = torch_module() if is_cuda_device(self.device) else None
        torch_dtype: str | None = None
        if self._torch is not None:
            raise_for_unsupported_cuda_arch(self._torch, self.device)
            torch_dtype = cuda_dtype_for(self._torch, self.device, precision=precision, spec=self.spec)

        processor_kwargs = processor_kwargs_for(
            fix_mistral_regex=fix_mistral_regex,
            slow_tokenizer=slow_tokenizer,
        )
        load_kwargs = sentence_transformer_load_kwargs(
            backend=backend,
            device=self.device,
            torch_dtype=torch_dtype,
        )
        if self.spec.trust_remote_code:
            load_kwargs["trust_remote_code"] = True
        self.model = sentence_transformers.SentenceTransformer(
            model_path,
            backend=backend,
            **load_kwargs,
            processor_kwargs=processor_kwargs,
        )
        if max_seq_length:
            self.model.max_seq_length = min(max_seq_length, self.spec.max_seq_length)
        self.description = f"model={self.spec.key} " + describe_backend(
            backend=backend,
            device=self.device,
            torch_dtype=torch_dtype,
            torch=self._torch,
        )

    def encode(self, inputs: Sequence[str]) -> list[list[float]]:
        """Encode passages (chunks) as normalised STORED_DIM vectors."""
        return self._encode(inputs, self.spec.document_prompt)

    def encode_queries(self, inputs: Sequence[str]) -> list[list[float]]:
        """Encode search queries: same model, the registry's query prompt."""
        return self._encode(inputs, self.spec.query_prompt)

    def _encode(self, inputs: Sequence[str], prompt: str) -> list[list[float]]:
        texts = [prompt + text for text in inputs] if prompt else list(inputs)
        batch_size = min(self.encode_batch_size, len(texts)) if self.encode_batch_size else len(texts)
        vectors = self._encode_with_oom_backoff(texts, batch_size)
        return [fit_dimension(vector.astype(float).tolist(), self.spec) for vector in vectors]

    def _encode_with_oom_backoff(self, texts: list[str], batch_size: int) -> Any:
        """Encode, halving the GPU batch until it fits in VRAM.

        Chunk lengths vary a lot, so a batch size that fits most of the corpus
        can still overflow an 11 GB card on a run of long articles. The reduced
        size sticks for the rest of the run: the next batch would fail the same
        way, and re-raising would throw away work the run already committed.
        """
        while True:
            try:
                return self.model.encode(
                    texts,
                    batch_size=batch_size,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )
            except cuda_oom_errors(self._torch):
                if batch_size <= 1:
                    raise
                batch_size = max(1, batch_size // 2)
                self.encode_batch_size = batch_size
                print(
                    f"warning: CUDA out of memory; retrying with encode batch size {batch_size}",
                    file=sys.stderr,
                )
                self._torch.cuda.empty_cache()


def torch_module() -> ModuleType | None:
    """Import torch, or return None when only the OpenVINO path is installed."""
    try:
        return import_module("torch")
    except ImportError:  # pragma: no cover - exercised by operator environment
        return None


def is_cuda_device(device: str | None) -> bool:
    """Return whether a resolved device string targets a CUDA GPU."""
    return bool(device) and device.lower().startswith("cuda")


def resolve_torch_device(device: str | None, *, backend: str = "torch") -> str | None:
    """Resolve the requested device, defaulting the torch backend to CUDA when present.

    OpenVINO device names (CPU/GPU/NPU) mean something else entirely and are
    handed through untouched; only the torch backend auto-detects.
    """
    if backend != "torch":
        return device
    if device and device.lower() != AUTO_DEVICE:
        return device
    torch = torch_module()
    if torch is not None and torch.cuda.is_available():
        return "cuda"
    return "cpu"


def cuda_dtype_for(
    torch: Any,
    device: str,
    *,
    precision: str = "auto",
    spec: EmbeddingModelSpec | None = None,
) -> str | None:
    """Return the model dtype for a CUDA device, or None to keep the fp32 default.

    `auto`: bf16 on Ampere+ for models that are not fp16-safe (bf16-trained
    decoders such as Qwen3 overflow in fp16), fp16 from Volta on for the rest,
    fp32 below. An explicit precision is honoured as asked.
    """
    if precision == "fp32":
        return None
    if precision == "fp16":
        return "float16"
    if precision == "bf16":
        return "bfloat16"
    capability = tuple(torch.cuda.get_device_capability(device))
    fp16_safe = spec.fp16_safe if spec is not None else True
    if not fp16_safe:
        return "bfloat16" if capability >= CUDA_BF16_MIN_CAPABILITY else None
    if capability >= CUDA_FP16_MIN_CAPABILITY:
        return "float16"
    return None


def cuda_oom_errors(torch: Any) -> tuple[type[BaseException], ...]:
    """Return the exception types signalling exhausted VRAM."""
    return (torch.cuda.OutOfMemoryError,) if torch is not None else ()


def arch_list_supports(capability: tuple[int, int], arch_list: Sequence[str]) -> bool:
    """Return whether a torch build carries kernels runnable on this GPU.

    A cubin runs on the same major version from its minor version up (sm_60
    code runs on the 1080 Ti's sm_61), and embedded PTX from any older arch
    can be JIT-compiled forward.
    """
    for arch in arch_list:
        kind, _, version = arch.partition("_")
        digits = "".join(character for character in version if character.isdigit())
        if len(digits) < 2:
            continue
        arch_capability = (int(digits[:-1]), int(digits[-1]))
        if kind == "compute" and arch_capability <= capability:
            return True
        if kind == "sm" and arch_capability[0] == capability[0] and arch_capability[1] <= capability[1]:
            return True
    return False


def raise_for_unsupported_cuda_arch(torch: Any, device: str) -> None:
    """Fail before model load when the installed wheel has no kernels for this GPU.

    PyTorch's cu128 and CUDA 13 wheels dropped Pascal, and the failure they
    produce mid-run ("no kernel image is available for execution on the
    device") does not say which wheel to install instead.
    """
    capability = tuple(torch.cuda.get_device_capability(device))
    arch_list = list(torch.cuda.get_arch_list())
    if arch_list_supports(capability, arch_list):
        return
    name = torch.cuda.get_device_name(device)
    msg = (
        f"This PyTorch build has no CUDA kernels for {name} "
        f"(compute capability {capability[0]}.{capability[1]}); it ships: {', '.join(arch_list)}. "
        f"{CUDA_INSTALL_HINT}, or run with --device cpu."
    )
    raise RuntimeError(msg)


def describe_backend(*, backend: str, device: str | None, torch_dtype: str | None, torch: Any) -> str:
    """Return a one-line operator-facing description of the loaded backend."""
    description = f"backend={backend} device={device or 'default'}"
    if torch is None or not is_cuda_device(device):
        return description
    properties = torch.cuda.get_device_properties(device)
    return (
        f"{description} gpu={properties.name} "
        f"vram={properties.total_memory / 1024**3:.1f}GiB "
        f"sm_{properties.major}{properties.minor} dtype={torch_dtype or 'float32'}"
    )


def processor_kwargs_for(*, fix_mistral_regex: bool = False, slow_tokenizer: bool = False) -> dict[str, bool]:
    """Build tokenizer/processor kwargs for sentence-transformers."""
    kwargs: dict[str, bool] = {}
    if fix_mistral_regex:
        kwargs["fix_mistral_regex"] = True
    if slow_tokenizer:
        kwargs["use_fast"] = False
    return kwargs


def sentence_transformer_load_kwargs(
    *,
    backend: str,
    device: str | None = None,
    torch_dtype: str | None = None,
) -> dict[str, object]:
    """Build SentenceTransformer load kwargs without passing OpenVINO devices to Torch."""
    if backend == "openvino":
        kwargs: dict[str, object] = {"device": TORCH_WRAPPER_DEVICE}
        if device:
            kwargs["model_kwargs"] = {"device": device.upper()}
        return kwargs
    kwargs = {"device": device} if device else {}
    if torch_dtype:
        kwargs["model_kwargs"] = {"dtype": torch_dtype}
    return kwargs


def _looks_like_bge_m3(model_path: str) -> bool:
    """Return whether a model path/id appears to be BGE-M3."""
    return "bge-m3" in model_path.lower()


def build_embeddings(
    conn: Connection,
    backend: EmbeddingBackend,
    *,
    model_id: int = 1,
    batch_size: int = 16,
    limit: int | None = None,
    dry_run: bool = False,
    progress: EmbeddingProgressCallback | None = None,
    commit_each_batch: bool = False,
    authentic_only: bool = False,
    langs: Sequence[str] | None = None,
    in_force_on: Sequence[date] | None = None,
) -> EmbeddingBuildStats:
    """Embed chunks missing a fresh row for the requested model.

    With commit_each_batch, every embedded batch is committed as it lands so a
    killed or timed-out run keeps the vectors already computed — embedding is
    minutes of CPU work, and the input-hash check makes re-runs resume cleanly.

    `authentic_only` / `langs` / `in_force_on` narrow the build to what
    evidence retrieval searches (the law's own text, in the country's
    language, on the dates asked): a candidate model under evaluation does not
    need the ~16k machine-translated chunks nor every superseded version.
    """
    if not dry_run:
        ensure_embedding_model(conn, get_model(model_id))
        if commit_each_batch:
            conn.commit()  # the model row must survive even if the first batch doesn't

    stats = EmbeddingBuildStats()
    batch: list[ChunkForEmbedding] = []

    chunks = iter_chunks_needing_embeddings(
        conn,
        model_id=model_id,
        limit=limit,
        authentic_only=authentic_only,
        langs=langs,
        in_force_on=in_force_on,
    )
    for chunk in chunks:
        stats = EmbeddingBuildStats(stats.scanned + 1, stats.embedded, stats.skipped)
        batch.append(chunk)
        _emit_progress(progress, "candidate", stats, len(batch))
        if len(batch) >= batch_size:
            _emit_progress(progress, "encoding", stats, len(batch))
            embedded, skipped = _embed_batch(conn, backend, batch, model_id=model_id, dry_run=dry_run)
            if commit_each_batch and not dry_run:
                conn.commit()
            stats = EmbeddingBuildStats(stats.scanned, stats.embedded + embedded, stats.skipped + skipped)
            _emit_progress(progress, "embedded", stats, embedded)
            batch = []

    if batch:
        _emit_progress(progress, "encoding", stats, len(batch))
        embedded, skipped = _embed_batch(conn, backend, batch, model_id=model_id, dry_run=dry_run)
        stats = EmbeddingBuildStats(stats.scanned, stats.embedded + embedded, stats.skipped + skipped)
        _emit_progress(progress, "embedded", stats, embedded)

    _emit_progress(progress, "done", stats)

    return stats


def _emit_progress(
    progress: EmbeddingProgressCallback | None,
    phase: str,
    stats: EmbeddingBuildStats,
    batch_size: int = 0,
) -> None:
    """Emit a progress event if a callback is registered."""
    if progress is None:
        return
    progress({"phase": phase, "scanned": stats.scanned, "embedded": stats.embedded, "batch_size": batch_size})


_SCOPE_FILTER = """
  AND (NOT %(authentic_only)s OR t.authenticity <> 'machine_translation')
  AND (%(langs)s::text[] IS NULL OR t.lang = ANY(%(langs)s::text[]))
  AND (%(in_force_on)s::date[] IS NULL OR EXISTS (
        SELECT 1 FROM legal_unit_versions v, unnest(%(in_force_on)s::date[]) AS d(day)
        WHERE v.id = t.version_id AND v.validity @> d.day))
"""


def _scope_params(
    model_id: int,
    authentic_only: bool,
    langs: Sequence[str] | None,
    in_force_on: Sequence[date] | None = None,
) -> dict[str, object]:
    return {
        "model_id": model_id,
        "authentic_only": authentic_only,
        "langs": list(langs) if langs else None,
        "in_force_on": list(in_force_on) if in_force_on else None,
    }


def iter_chunks_needing_embeddings(
    conn: Connection,
    *,
    model_id: int = 1,
    limit: int | None = None,
    authentic_only: bool = False,
    langs: Sequence[str] | None = None,
    in_force_on: Sequence[date] | None = None,
) -> Iterable[ChunkForEmbedding]:
    """Yield chunks whose embedding row is missing or stale."""
    yielded = 0
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            f"""
            SELECT c.id, c.context_header, c.content, e.input_hash
            FROM chunks c
            JOIN unit_texts t ON t.id = c.unit_text_id
            LEFT JOIN embeddings e ON e.chunk_id = c.id AND e.model_id = %(model_id)s
            WHERE true {_SCOPE_FILTER}
            ORDER BY c.id
            """,
            _scope_params(model_id, authentic_only, langs, in_force_on),
        )
        for row in cur:
            input_text = embedding_input(row["context_header"], row["content"])
            input_hash = embedding_input_hash(input_text)
            if row["input_hash"] == input_hash:
                continue
            yield ChunkForEmbedding(id=row["id"], input_text=input_text, input_hash=input_hash)
            yielded += 1
            if limit is not None and yielded >= limit:
                return


def count_chunks_needing_embeddings(
    conn: Connection,
    *,
    model_id: int = 1,
    limit: int | None = None,
    authentic_only: bool = False,
    langs: Sequence[str] | None = None,
    in_force_on: Sequence[date] | None = None,
) -> int:
    """Count the chunks `iter_chunks_needing_embeddings` would yield.

    SQL twin of the iterator's staleness check: sha256(context_header + "\\n" +
    content) compared against the stored input_hash, so a progress display can
    know the total before the scan starts.
    """
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT count(*)
            FROM chunks c
            JOIN unit_texts t ON t.id = c.unit_text_id
            LEFT JOIN embeddings e ON e.chunk_id = c.id AND e.model_id = %(model_id)s
            WHERE e.input_hash IS DISTINCT FROM
                  encode(sha256(convert_to(c.context_header || chr(10) || c.content, 'UTF8')), 'hex')
            {_SCOPE_FILTER}
            """,
            _scope_params(model_id, authentic_only, langs, in_force_on),
        )
        total = int(cur.fetchone()[0])
    return min(total, limit) if limit is not None else total


def ensure_embedding_model(conn: Connection, spec: EmbeddingModelSpec) -> None:
    """Ensure the model's `embedding_models` row exists (BGE-M3 is the default).

    An existing row is left alone: `is_default` is an operator's decision and
    the seeded BGE-M3 row predates the registry's config keys.
    """
    row = spec.registry_row()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO embedding_models
              (id, name, provider, native_dim, stored_dim, normalize, is_default, config)
            VALUES (%s, %s, %s, %s, %s, true, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (
                row["id"],
                row["name"],
                row["provider"],
                row["native_dim"],
                row["stored_dim"],
                spec.id == DEFAULT_MODEL.id,
                Jsonb(row["config"]),
            ),
        )



def embedding_input(context_header: str, content: str) -> str:
    """Return the canonical text passed to the embedding model."""
    return f"{context_header}\n{content}"


def embedding_input_hash(input_text: str) -> str:
    """Hash the exact model input for stale-vector detection."""
    return sha256(input_text.encode("utf-8")).hexdigest()


def halfvec_literal(vector: Sequence[float]) -> str:
    """Serialize a vector for insertion into PostgreSQL halfvec."""
    if len(vector) != BGE_M3_DIM:
        msg = f"Expected {BGE_M3_DIM} dimensions, got {len(vector)}"
        raise ValueError(msg)
    return "[" + ",".join(f"{float(value):.8g}" for value in vector) + "]"


def _embed_batch(
    conn: Connection,
    backend: EmbeddingBackend,
    batch: Sequence[ChunkForEmbedding],
    *,
    model_id: int,
    dry_run: bool,
) -> tuple[int, int]:
    """Encode and persist a batch of chunks, returning (embedded, skipped).

    The candidate list is read before encoding, which takes minutes, so a
    concurrent ingest can retire a chunk id in between: `_replace_chunks`
    deletes and re-inserts a unit text's chunks with fresh UUIDs. Inserting
    against `chunks` instead of blind-inserting the id drops those vanished
    chunks rather than failing the run on the foreign key; the re-chunked rows
    are picked up by the next build.
    """
    if dry_run:
        return len(batch), 0

    vectors = backend.encode([chunk.input_text for chunk in batch])
    if len(vectors) != len(batch):
        msg = f"Backend returned {len(vectors)} vectors for {len(batch)} inputs"
        raise ValueError(msg)

    embedded = 0
    with conn.transaction():
        with conn.cursor() as cur:
            for chunk, vector in zip(batch, vectors, strict=True):
                cur.execute(
                    """
                    INSERT INTO embeddings (chunk_id, model_id, embedding, input_hash)
                    SELECT c.id, %s, %s::halfvec, %s
                    FROM chunks c
                    WHERE c.id = %s
                    ON CONFLICT (chunk_id, model_id) DO UPDATE
                    SET embedding = EXCLUDED.embedding,
                        input_hash = EXCLUDED.input_hash,
                        embedded_at = now()
                    """,
                    (model_id, halfvec_literal(vector), chunk.input_hash, chunk.id),
                )
                embedded += cur.rowcount
    return embedded, len(batch) - embedded