"""Environment-driven configuration, mirroring agentic-workflow's config.py."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Nomokrisis-evaluation_pipeline/ (this file lives in src/nomokrisis_eval/).
EVAL_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = EVAL_ROOT.parent


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(slots=True)
class EvalConfig:
    #: The golden set, the runs and their results all live in this database
    #: (schema `eval`, ADR 0004) — nothing runtime is on disk any more.
    database_url: str = ""
    #: Provider-prefixed drafting model for `build-dataset` (`anthropic/…`,
    #: `azure_openai/…`, `jrc/…`); `mock/` is refused — a drafted ground truth
    #: from a mock would be a fabricated golden case.
    builder_model: str = ""
    #: Model for the workflow's critique step during an evaluation run. Empty
    #: means "the model under test grades itself", which is fine for tracking
    #: one model over time but not for comparing models (Activity 5): a lenient
    #: critic reports better supportedness for the same proposals. Pin a single
    #: judge with EVAL_CRITIQUE_MODEL to make those columns comparable.
    critique_model: str = ""
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
        builder_model=_env("EVAL_BUILDER_MODEL", "anthropic/claude-fable-5"),
        critique_model=_env("EVAL_CRITIQUE_MODEL", ""),
        phoenix_project=_env("EVAL_PHOENIX_PROJECT", "nomokrisis-evaluation"),
    )
