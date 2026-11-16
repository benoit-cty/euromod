"""Query encoding for the vector leg of hybrid retrieval.

The query must be encoded by the model that embedded the corpus being searched:
`encode(query, model_id=N)` asks for embedding model N of the ingest registry
(nomotheca_ingest.core.embedding_models; 1 = BGE-M3, the default), with that
model's query prompt. One encoder process per model id, started on demand.

Two ways to get a query vector, chosen by `WORKFLOW_ENCODER`:

- `subprocess` (default): reuse the ingest package's long-lived JSON-lines
  encoder (nomotheca_ingest.query_embeddings), so the pipeline carries no ML
  dependencies of its own. The process starts lazily on the first query and
  is reused for every subsequent parameter in the run.
- `db`: submit an `encode` job to the worker's `ops.jobs` table and poll
  (encode_client) — the worker keeps the model warm and runs workflow jobs
  with this mode, so the subprocess never loads the model itself.

A failure degrades that query to FTS-only (its hybrid hits carry
method="fts", so the review item and the eval record it). An encoder that
cannot start, or an unknown mode, disables the vector leg for the rest of the
process; any other failure (a 60 s timeout while the GPU is busy, a dead
subprocess) only pauses it for `WORKFLOW_ENCODER_COOLDOWN` seconds (default
30), after which the next query tries again. Until 16 Nov 2026 one timeout
latched the whole process, and an eval run (one process, hundreds of cases)
went FTS-only for good with nothing recording it (code audit D5).

The subprocess encoders are shared by every thread of the process (an eval
run with -j 4): each request/response pair holds that process's lock, so two
cases can never read each other's vector (code audit D4).

Subprocess spawns honour `NOMOS_PYTHON`: when set (the worker sets it to its
own interpreter), the command is `[NOMOS_PYTHON, -m, module, …]` run in the
current directory — no `uv`, no ingest-dir walk.
"""

from __future__ import annotations

import json
import os
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

from . import encode_client

EMBEDDING_EXTRA = "embeddings"
CUDA_EXTRA = "embeddings-cuda"
CUDA_ENVIRONMENT = ".venv-cuda"

DEFAULT_DATABASE_URL = "postgresql://jrc:jrc@localhost:5434/legislation"

DEFAULT_MODEL_ID = 1

DEFAULT_COOLDOWN_SECONDS = 30.0


@dataclass(slots=True)
class _Channel:
    """One long-lived JSON-lines subprocess and the lock its I/O holds."""

    process: subprocess.Popen | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)


_channels: dict[int, _Channel] = {}
_channels_lock = threading.Lock()
_disabled = False
_paused_until = 0.0
#: Queries answered without a vector since the process started (FTS-only).
fts_only_queries = 0


class EncoderStartError(RuntimeError):
    """The encoder process could not start: retrying will not help."""


def _channel(registry: dict, key) -> _Channel:
    with _channels_lock:
        return registry.setdefault(key, _Channel())


def cooldown_seconds() -> float:
    """WORKFLOW_ENCODER_COOLDOWN, read at call time (after any .env is loaded)."""
    try:
        return float(os.environ.get("WORKFLOW_ENCODER_COOLDOWN", DEFAULT_COOLDOWN_SECONDS))
    except ValueError:
        return DEFAULT_COOLDOWN_SECONDS


def encoder_mode() -> str:
    """`subprocess` (default) or `db` — see WORKFLOW_ENCODER."""
    return os.environ.get("WORKFLOW_ENCODER", "subprocess").strip().lower() or "subprocess"


def nomos_python() -> str | None:
    """The interpreter every spawned subprocess must use, when the worker sets it."""
    return os.environ.get("NOMOS_PYTHON") or None


def ingest_dir() -> Path | None:
    """Locate Nomotheca-RAG/ingest (EUROMOD_INGEST_DIR overrides the repo walk)."""
    override = os.environ.get("EUROMOD_INGEST_DIR")
    if override:
        path = Path(override)
        return path if (path / "pyproject.toml").is_file() else None
    for ancestor in Path(__file__).resolve().parents:
        candidate = ancestor / "Nomotheca-RAG" / "ingest"
        if (candidate / "pyproject.toml").is_file():
            return candidate
    return None


@dataclass(frozen=True, slots=True)
class EmbeddingProcess:
    """How to spawn one of the ingest package's BGE-M3 subprocesses."""

    command: list[str]
    env: dict[str, str]
    cuda: bool
    cwd: Path


def embedding_process(directory: Path | None, module: str, *args: str) -> EmbeddingProcess:
    """Build the invocation for an ingest embedding subprocess.

    With `NOMOS_PYTHON` set the spawn is that interpreter, `-m module`, in the
    current working directory, env unchanged (minus VIRTUAL_ENV) — the worker's
    own environment already holds the ingest package and its ML wheels.

    Otherwise it is `uv run` inside the ingest package. The GPU wheels live in
    their own environment because CUDA and CPU torch are conflicting extras in
    the ingest package: if the operator has run
    `UV_PROJECT_ENVIRONMENT=$PWD/.venv-cuda uv sync --package
    nomotheca-legislation-ingest --extra embeddings-cuda` there,
    point uv at it and BGE-M3 runs on the GPU (roughly 20x the CPU rate);
    otherwise nothing changes and the CPU/OpenVINO `.venv` is used.
    """
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    python = nomos_python()
    if python:
        return EmbeddingProcess(
            command=[python, "-m", module, *args], env=env, cuda=False, cwd=Path.cwd()
        )
    if directory is None:
        raise RuntimeError("could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR or NOMOS_PYTHON)")
    cuda_environment = directory / CUDA_ENVIRONMENT
    cuda = (cuda_environment / "pyvenv.cfg").is_file()
    if cuda:
        env["UV_PROJECT_ENVIRONMENT"] = str(cuda_environment)
    extra = CUDA_EXTRA if cuda else EMBEDDING_EXTRA
    command = ["uv", "run", "--extra", extra, "python", "-m", module, *args]
    return EmbeddingProcess(command=command, env=env, cuda=cuda, cwd=directory)


def _spawn_ready(module: str, *args: str, what: str) -> subprocess.Popen:
    """Start one JSON-lines subprocess of the ingest package and wait for its
    {"ready": true} line — the one launcher of the encoder and the reranker."""
    spec = embedding_process(ingest_dir(), module, *args)
    process = subprocess.Popen(
        spec.command, cwd=spec.cwd, env=spec.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
    )
    ready = json.loads(process.stdout.readline() or "{}")
    if not ready.get("ready"):
        process.kill()
        raise EncoderStartError(f"{what} failed to initialize: {ready}")
    return process


def _start(model_id: int = DEFAULT_MODEL_ID) -> subprocess.Popen:
    cuda = (ingest_dir() or Path(".")).joinpath(CUDA_ENVIRONMENT, "pyvenv.cfg").is_file()
    print(
        f"[retrieval] starting query encoder for embedding model {model_id} "
        f"(first query — model load can take minutes, {'GPU' if cuda else 'expect high CPU'})…",
        flush=True,
    )
    started = time.monotonic()
    process = _spawn_ready(
        "nomotheca_ingest.query_embeddings", "--model", str(model_id), what="encoder"
    )
    print(f"[retrieval] query encoder ready ({time.monotonic() - started:.0f}s)", flush=True)
    return process


def _encode_subprocess(query: str, model_id: int = DEFAULT_MODEL_ID) -> str:
    channel = _channel(_channels, model_id)
    with channel.lock:
        if channel.process is None or channel.process.poll() is not None:
            channel.process = _start(model_id)
        channel.process.stdin.write(json.dumps({"query": query}) + "\n")
        channel.process.stdin.flush()
        response = json.loads(channel.process.stdout.readline() or "{}")
    if "halfvec" not in response:
        raise RuntimeError(response.get("error", "no halfvec in encoder response"))
    return response["halfvec"]


def encode(
    query: str, database_url: str | None = None, model_id: int = DEFAULT_MODEL_ID
) -> str | None:
    """halfvec literal for a query under embedding model `model_id`, or None
    when the encoder is unavailable.

    `database_url` is only used by the `db` encoder mode (defaults to
    WORKFLOW_DATABASE_URL, same default as config.py).
    """
    global _disabled, _paused_until, fts_only_queries
    if _disabled or time.monotonic() < _paused_until:
        fts_only_queries += 1
        return None
    mode = encoder_mode()
    try:
        if mode == "db":
            url = database_url or os.environ.get("WORKFLOW_DATABASE_URL", DEFAULT_DATABASE_URL)
            return encode_client.encode_via_jobs(url, query, model_id=model_id)
        if mode != "subprocess":
            raise EncoderStartError(f"unknown WORKFLOW_ENCODER {mode!r} (subprocess | db)")
        return _encode_subprocess(query, model_id)
    except EncoderStartError as exc:
        _disabled = True
        fts_only_queries += 1
        print(f"[retrieval] vector leg disabled (encoder={mode}; {exc})", flush=True)
        return None
    except Exception as exc:
        pause = cooldown_seconds()
        _paused_until = time.monotonic() + pause
        fts_only_queries += 1
        print(
            f"[retrieval] vector leg paused {pause:.0f}s, this query FTS-only "
            f"(encoder={mode}; {exc.__class__.__name__}: {exc})",
            flush=True,
        )
        return None


# ---------------------------------------------------------------------------
# Cross-encoder reranking (evaluation only for now)
# ---------------------------------------------------------------------------

_rerankers: dict[str, _Channel] = {}


def _start_reranker(model: str) -> subprocess.Popen:
    print(f"[retrieval] starting reranker {model}…", flush=True)
    return _spawn_ready("nomotheca_ingest.rerank", "--model", model, what="reranker")


def rerank(query: str, passages: list[str], model: str) -> list[float]:
    """One cross-encoder score per passage (higher = more relevant).

    Unlike `encode`, a failure raises: nothing in a workflow run depends on a
    reranker yet, and the retrieval evaluation records the error per case.
    """
    channel = _channel(_rerankers, model)
    with channel.lock:
        if channel.process is None or channel.process.poll() is not None:
            channel.process = _start_reranker(model)
        channel.process.stdin.write(json.dumps({"query": query, "passages": passages}) + "\n")
        channel.process.stdin.flush()
        response = json.loads(channel.process.stdout.readline() or "{}")
    if "scores" not in response:
        raise RuntimeError(response.get("error", "no scores in reranker response"))
    return response["scores"]
