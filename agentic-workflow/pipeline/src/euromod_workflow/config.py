"""Environment-driven configuration for the workflow pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# agentic-workflow/ directory (this file lives in pipeline/src/euromod_workflow/).
WORKFLOW_ROOT = Path(__file__).resolve().parents[3]


def _env(name: str, default: str) -> str:
    """Read an env var with a default."""
    return os.environ.get(name, default)


@dataclass(slots=True)
class WorkflowConfig:
    """All runtime knobs; every field has an env-var override."""

    database_url: str = ""
    model: str = ""
    critique_model: str = ""
    embedding_model_id: int = 99
    retrieval_k: int = 8
    data_dir: Path = field(default_factory=lambda: WORKFLOW_ROOT / "data")
    phoenix_endpoint: str = ""
    phoenix_project: str = ""
    tracing_enabled: bool = True


def load_config() -> WorkflowConfig:
    """Build the config from .env (repo root, then agentic-workflow/) and the process env."""
    load_dotenv(WORKFLOW_ROOT.parent / ".env")
    load_dotenv(WORKFLOW_ROOT / ".env", override=True)
    return WorkflowConfig(
        database_url=_env(
            "WORKFLOW_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation"
        ),
        model=_env("WORKFLOW_MODEL", "mock/extractor"),
        critique_model=_env("WORKFLOW_CRITIQUE_MODEL", "") or _env("WORKFLOW_MODEL", "mock/extractor"),
        embedding_model_id=int(_env("WORKFLOW_EMBEDDING_MODEL_ID", "99")),
        retrieval_k=int(_env("WORKFLOW_RETRIEVAL_K", "8")),
        data_dir=Path(_env("WORKFLOW_DATA_DIR", str(WORKFLOW_ROOT / "data"))),
        phoenix_endpoint=_env("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006"),
        phoenix_project=_env("PHOENIX_PROJECT_NAME", "euromod-agentic-workflow"),
        tracing_enabled=_env("WORKFLOW_TRACING", "true").lower() != "false",
    )
