"""BGE-M3 query encoding for the vector leg of hybrid retrieval.

Reuses the ingest package's long-lived JSON-lines encoder
(nomotheca_ingest.query_embeddings — the same subprocess the validation UI
spawns), so the pipeline carries no ML dependencies of its own. The process
starts lazily on the first query and is reused for every subsequent
parameter in the run; any failure disables the vector leg for the rest of
the process and retrieval degrades to FTS-only with a console note.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

EMBEDDING_EXTRA = "embeddings"
CUDA_EXTRA = "embeddings-cuda"
CUDA_ENVIRONMENT = ".venv-cuda"

_process: subprocess.Popen | None = None
_disabled = False


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


def embedding_process(directory: Path, module: str, *args: str) -> EmbeddingProcess:
    """Build the `uv run` invocation for an ingest embedding subprocess.

    The GPU wheels live in their own environment because CUDA and CPU torch are
    conflicting extras in the ingest package: if the operator has run
    `UV_PROJECT_ENVIRONMENT=.venv-cuda uv sync --extra embeddings-cuda` there,
    point uv at it and BGE-M3 runs on the GPU (roughly 20x the CPU rate);
    otherwise nothing changes and the CPU/OpenVINO `.venv` is used.
    """
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    cuda_environment = directory / CUDA_ENVIRONMENT
    cuda = (cuda_environment / "pyvenv.cfg").is_file()
    if cuda:
        env["UV_PROJECT_ENVIRONMENT"] = str(cuda_environment)
    extra = CUDA_EXTRA if cuda else EMBEDDING_EXTRA
    command = ["uv", "run", "--extra", extra, "python", "-m", module, *args]
    return EmbeddingProcess(command=command, env=env, cuda=cuda)


def _start() -> subprocess.Popen:
    directory = ingest_dir()
    if directory is None:
        raise RuntimeError("could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR)")
    spec = embedding_process(directory, "nomotheca_ingest.query_embeddings")
    load_note = "GPU" if spec.cuda else "expect high CPU"
    print(
        f"[retrieval] starting BGE-M3 query encoder (first query — model load can take minutes, {load_note})…",
        flush=True,
    )
    started = time.monotonic()
    process = subprocess.Popen(
        spec.command,
        cwd=directory,
        env=spec.env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    ready = json.loads(process.stdout.readline() or "{}")
    if not ready.get("ready"):
        process.kill()
        raise RuntimeError(f"encoder failed to initialize: {ready}")
    print(f"[retrieval] query encoder ready ({time.monotonic() - started:.0f}s)", flush=True)
    return process


def encode(query: str) -> str | None:
    """halfvec literal for a query, or None when the encoder is unavailable."""
    global _process, _disabled
    if _disabled:
        return None
    try:
        if _process is None or _process.poll() is not None:
            _process = _start()
        _process.stdin.write(json.dumps({"query": query}) + "\n")
        _process.stdin.flush()
        response = json.loads(_process.stdout.readline() or "{}")
        if "halfvec" not in response:
            raise RuntimeError(response.get("error", "no halfvec in encoder response"))
        return response["halfvec"]
    except Exception as exc:
        _disabled = True
        print(f"[retrieval] vector leg disabled ({exc.__class__.__name__}: {exc})")
        return None
