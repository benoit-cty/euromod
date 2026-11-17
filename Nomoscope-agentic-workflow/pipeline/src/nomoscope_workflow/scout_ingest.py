"""The scout's side effects on the corpus: archive-first ingest and embedding.

The scout reaches the Nomotheca ingester by subprocess (the dependency between
the two packages runs one way only), one ingest at a time per process, and
then embeds the new chunks so the vector leg of the retry covers them.
"""

from __future__ import annotations

import os
import subprocess
import threading
from pathlib import Path

from .config import WorkflowConfig
from .query_encoder import EmbeddingProcess, embedding_process, ingest_dir, nomos_python

INGEST_TIMEOUT = 600  # a single arrêté is seconds; a loi de finances, minutes
# The embedding pass covers the whole backlog of unembedded chunks, not just the
# scouted instrument (the CLI has no per-instrument scope), and BGE-M3 on CPU
# runs at roughly one chunk per second — a freshly ingested loi de finances
# alone is ~10 minutes (roughly 20x faster when the .venv-cuda GPU environment
# is installed). The build commits per batch, so even a timeout here keeps the
# vectors computed so far; the retry then resumes where it stopped.
def embed_timeout() -> int:
    """WORKFLOW_SCOUT_EMBED_TIMEOUT, read at call time so a .env value counts
    (it was read at import, before any .env was loaded)."""
    return int(os.environ.get("WORKFLOW_SCOUT_EMBED_TIMEOUT", "1800"))


def known_instruments(cfg: WorkflowConfig, ids: list[str], rules: dict) -> set[str]:
    """Ids already in the legislation DB — re-ingesting them cannot add chunks.

    Article-level ids (FR LEGIARTI…/JORFARTI…) are stored as legal_units under
    their parent code instrument, not as instruments — check both tables, or
    every re-run re-ingests the same article forever. Where the scouted id is
    not the stored national_id at all (LT keys instruments by official number
    and files the TAR id under metadata.dokumento_id), `known_key` says which
    metadata key to match instead.
    """
    import psycopg

    sql = (
        "SELECT national_id FROM instruments WHERE national_id = ANY(%(ids)s) "
        "UNION SELECT national_id FROM legal_units WHERE national_id = ANY(%(ids)s)"
    )
    if rules.get("known_key"):
        sql += (
            " UNION SELECT metadata->>%(key)s FROM instruments "
            "WHERE metadata->>%(key)s = ANY(%(ids)s)"
        )
    # No except: a database error used to return the empty set, so every
    # candidate was re-ingested (code audit 4). The ingest needs the same DB.
    with psycopg.connect(cfg.database_url) as conn:
        rows = conn.execute(sql, {"ids": ids, "key": rules.get("known_key")}).fetchall()
    return {row[0] for row in rows}


def _proc_failure(what: str, proc: subprocess.CompletedProcess) -> str:
    """Failure text with exit code and the tail of BOTH streams.

    stderr alone is not enough: the benign BGE-M3 tokenizer warning always
    lands there and would mask the real error when it went to stdout, and a
    negative returncode (killed by a signal, e.g. memory pressure) leaves no
    traceback at all — the exit code is then the only evidence.
    """
    parts = []
    for stream, text in (("stderr", proc.stderr), ("stdout", proc.stdout)):
        lines = (text or "").strip().splitlines()
        if lines:
            parts.append(f"{stream}: {' | '.join(lines[-4:])}")
    detail = "; ".join(parts) or "no output"
    signal_hint = " — killed by a signal, likely memory pressure" if proc.returncode < 0 else ""
    return f"{what} failed (exit {proc.returncode}{signal_hint}): {detail}"


_NO_INGEST_DIR = "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR or NOMOS_PYTHON)"


def _launch(spec: EmbeddingProcess, what: str, timeout: int, timeout_note: str = "") -> str | None:
    """Run one ingest-package subprocess to completion; error text on failure.

    The one launcher of the scout: a non-zero exit becomes `_proc_failure`, a
    timeout `"<what> timed out after <n>s<note>"`.
    """
    try:
        proc = subprocess.run(
            spec.command, cwd=spec.cwd, env=spec.env, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return f"{what} timed out after {timeout}s{timeout_note}"
    if proc.returncode != 0:
        return _proc_failure(what, proc)
    return None


def instrument_args(cfg: WorkflowConfig, country: str, instrument_id: str) -> list[str]:
    """The Nomotheca CLI arguments that ingest one instrument, archive-first."""
    return ["instrument", country.lower(), instrument_id, "--database-url", cfg.database_url]


#: One scout ingest at a time per process: an eval runs several cases in
#: threads, and two of them may scout the same act — two loaders writing one
#: instrument at once would trip the version/chunk constraints.
_INGEST_LOCK = threading.Lock()


def run_ingest_cli(cfg: WorkflowConfig, args: list[str], what: str) -> str | None:
    """Run one Nomotheca CLI command; error text on failure.

    Inside the worker (`NOMOS_PYTHON` set) the CLI runs from that interpreter
    in the current directory; otherwise through `uv run` in the ingest package.
    """
    env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
    env["PYTHONUNBUFFERED"] = "1"
    python = nomos_python()
    if python:
        command, cwd = [python, "-m", "nomotheca_ingest.cli", *args], Path.cwd()
    else:
        cwd = ingest_dir()
        if cwd is None:
            return _NO_INGEST_DIR
        command = ["uv", "run", "python", "-m", "nomotheca_ingest.cli", *args]
    spec = EmbeddingProcess(command=command, env=env, cuda=False, cwd=cwd)
    with _INGEST_LOCK:
        return _launch(spec, f"{what}: ingest", INGEST_TIMEOUT)


def build_embeddings(cfg: WorkflowConfig) -> str | None:
    """Embed chunks that are missing vectors (incremental) so the vector leg
    of the retrieval retry covers what the scout just ingested."""
    directory = ingest_dir()
    if nomos_python():
        # The worker's interpreter, current directory: no local model export to
        # point at, so the CLI falls back to the Hugging Face id and its own
        # device selection.
        model_args: list[str] = []
    elif directory is None:
        return _NO_INGEST_DIR
    else:
        model_args = _embedding_model_args(directory, cuda=_cuda_available(directory))
    spec = embedding_process(
        directory,
        "nomotheca_ingest.cli",
        "embeddings",
        "build",
        "--database-url",
        cfg.database_url,
        # Rich's live progress is noise in captured output and can bury the
        # real error; the per-batch commits do not depend on it.
        "--no-progress",
        *model_args,
    )
    return _launch(spec, "embeddings build", embed_timeout(), " (partial vectors kept)")


def _cuda_available(directory: Path) -> bool:
    """Return whether the ingest package has its GPU environment installed."""
    return embedding_process(directory, "nomotheca_ingest.cli").cuda


def _embedding_model_args(directory: Path, *, cuda: bool) -> list[str]:
    """Pick the local model for the environment we are about to run in.

    The OpenVINO IR only loads under the OpenVINO backend, so on the GPU we ask
    for the Torch export if one was downloaded and otherwise let the CLI fall
    back to the Hugging Face id (device selection is the CLI's own job).
    """
    if cuda:
        torch_model = directory / "models" / "bge-m3"
        if (torch_model / "config.json").is_file():
            return ["--model-path", "models/bge-m3"]
        return []
    if (directory / "models" / "bge-m3-openvino").is_dir():
        return ["--backend", "openvino", "--model-path", "models/bge-m3-openvino"]
    return []
