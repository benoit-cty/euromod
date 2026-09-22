"""Environment-driven configuration for the worker.

Every knob is an env var with a ``WORKER_`` prefix; ``.env`` is read from the
repo root (and ``Nomoscope-agentic-workflow/.env``, which overrides it), the
same two places the pipeline's ``load_config`` reads, so a developer's
existing keys work unchanged when the worker runs on the host.
"""

from __future__ import annotations

import os
import socket
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_DATABASE_URL = "postgresql://jrc:jrc@localhost:5434/legislation"
BGE_M3_MODEL = "BAAI/bge-m3"
EMBEDDING_MODEL_NAME = "bge-m3"

# Sub-project directories, relative to the repo root.
INGEST_SUBDIR = Path("Nomotheca-RAG") / "ingest"
PIPELINE_SUBDIR = Path("Nomoscope-agentic-workflow") / "pipeline"
EVAL_SUBDIR = Path("Nomokrisis-evaluation_pipeline")
WORKER_SUBDIR = Path("Nomergon-worker")


def find_repo_root(start: Path | None = None) -> Path:
    """Locate the euromod checkout: ``NOMOS_REPO_ROOT`` or the ancestor holding ``Nomergon-worker/``.

    Walking up from this file works for an editable install (the source tree
    lives under ``Nomergon-worker/src``); the env override is for a wheel
    install or a container where the checkout lives elsewhere.
    """
    override = os.environ.get("NOMOS_REPO_ROOT")
    if override:
        return Path(override).resolve()
    here = (start or Path(__file__)).resolve()
    for ancestor in here.parents:
        if (ancestor / WORKER_SUBDIR / "pyproject.toml").is_file():
            return ancestor
    msg = "could not locate the euromod repo root (set NOMOS_REPO_ROOT)"
    raise RuntimeError(msg)


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


def _float_env(name: str, default: float) -> float:
    return float(_env(name, str(default)))


def _int_env(name: str, default: int) -> int:
    return int(_env(name, str(default)))


@dataclass(slots=True)
class WorkerConfig:
    """All runtime knobs of one worker process."""

    repo_root: Path
    database_url: str = DEFAULT_DATABASE_URL
    #: Provider-prefixed LLM names this worker publishes; the first is the default.
    models: list[str] = field(default_factory=list)
    embedding_model_path: str = BGE_M3_MODEL
    poll_seconds: float = 1.0
    encode_poll_seconds: float = 0.05
    heartbeat_seconds: float = 10.0
    stale_seconds: float = 60.0
    event_retention_days: int = 30
    worker_id: str = ""

    @property
    def default_model(self) -> str | None:
        """The LLM a job runs on when its payload names none."""
        return self.models[0] if self.models else None

    @property
    def ingest_dir(self) -> Path:
        return self.repo_root / INGEST_SUBDIR

    @property
    def pipeline_dir(self) -> Path:
        return self.repo_root / PIPELINE_SUBDIR

    @property
    def eval_dir(self) -> Path:
        return self.repo_root / EVAL_SUBDIR


def default_worker_id() -> str:
    return f"{socket.gethostname()}-{os.getpid()}"


def default_embedding_model_path(repo_root: Path) -> str:
    """The local BGE-M3 checkout when the ingest package holds one, else the Hub id."""
    local = repo_root / INGEST_SUBDIR / "models" / "bge-m3"
    if (local / "config.json").is_file():
        return str(local)
    return BGE_M3_MODEL


def load_config(repo_root: Path | None = None) -> WorkerConfig:
    """Build the config from ``.env`` files and the process environment."""
    root = repo_root or find_repo_root()
    load_dotenv(root / ".env")
    load_dotenv(root / "Nomoscope-agentic-workflow" / ".env", override=True)

    database_url = _env("WORKER_DATABASE_URL", "") or _env("WORKFLOW_DATABASE_URL", DEFAULT_DATABASE_URL)
    models = [name.strip() for name in _env("WORKER_MODELS", "").split(",") if name.strip()]
    return WorkerConfig(
        repo_root=root,
        database_url=database_url,
        models=models,
        embedding_model_path=_env("WORKER_EMBEDDING_MODEL_PATH", "") or default_embedding_model_path(root),
        poll_seconds=_float_env("WORKER_POLL_SECONDS", 1.0),
        encode_poll_seconds=_float_env("WORKER_ENCODE_POLL_SECONDS", 0.05),
        heartbeat_seconds=_float_env("WORKER_HEARTBEAT_SECONDS", 10.0),
        stale_seconds=_float_env("WORKER_STALE_SECONDS", 60.0),
        event_retention_days=_int_env("WORKER_EVENT_RETENTION_DAYS", 30),
        worker_id=_env("WORKER_ID", "") or default_worker_id(),
    )
