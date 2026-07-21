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
from pathlib import Path

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


def _start() -> subprocess.Popen:
    directory = ingest_dir()
    if directory is None:
        raise RuntimeError("could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR)")
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    process = subprocess.Popen(
        ["uv", "run", "--extra", "embeddings", "python", "-m", "nomotheca_ingest.query_embeddings"],
        cwd=directory,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    ready = json.loads(process.stdout.readline() or "{}")
    if not ready.get("ready"):
        process.kill()
        raise RuntimeError(f"encoder failed to initialize: {ready}")
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
