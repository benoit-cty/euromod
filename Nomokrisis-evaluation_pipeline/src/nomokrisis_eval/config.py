"""Environment-driven configuration, mirroring agentic-workflow's config.py."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

# Nomokrisis-evaluation_pipeline/ (this file lives in src/nomokrisis_eval/).
EVAL_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = EVAL_ROOT.parent


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(slots=True)
class EvalConfig:
    database_url: str = ""
    dataset_dir: Path = field(default_factory=lambda: EVAL_ROOT / "dataset")
    embedding_dataset_dir: Path = field(default_factory=lambda: EVAL_ROOT / "dataset_embedding")
    runs_dir: Path = field(default_factory=lambda: EVAL_ROOT / ".eval_runs")
    builder_model: str = ""
    phoenix_project: str = ""


def load_eval_config() -> EvalConfig:
    """Build the config from .env (repo root, then Nomokrisis-evaluation_pipeline/) and the process env."""
    load_dotenv(REPO_ROOT / ".env")
    load_dotenv(EVAL_ROOT / ".env", override=True)
    return EvalConfig(
        database_url=_env(
            "EVAL_DATABASE_URL",
            _env("WORKFLOW_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation"),
        ),
        dataset_dir=Path(_env("EVAL_DATASET_DIR", str(EVAL_ROOT / "dataset"))),
        embedding_dataset_dir=Path(
            _env("EVAL_EMBEDDING_DATASET_DIR", str(EVAL_ROOT / "dataset_embedding"))
        ),
        runs_dir=Path(_env("EVAL_RUNS_DIR", str(EVAL_ROOT / ".eval_runs"))),
        builder_model=_env("EVAL_BUILDER_MODEL", "claude-fable-5"),
        phoenix_project=_env("EVAL_PHOENIX_PROJECT", "nomokrisis-evaluation"),
    )
