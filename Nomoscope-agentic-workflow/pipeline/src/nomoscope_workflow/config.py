"""Environment-driven configuration for the workflow pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Nomoscope-agentic-workflow/ directory (this file lives in pipeline/src/nomoscope_workflow/).
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
    # 8 was too tight: the correct CGI art. 197 consolidation ranked #11 behind
    # amending finance-act articles that repeat the same fiscal vocabulary.
    retrieval_k: int = 15
    phoenix_endpoint: str = ""
    phoenix_project: str = ""
    phoenix_database_url: str = ""  # phoenix DB in the same Postgres (impact reports)
    electricity_mix_zone: str = "EEE"  # EcoLogits zone; EEE = Europe, WOR = world
    tracing_enabled: bool = True
    scout: str = "off"  # off | llm | tavily — gap-fill source discovery on not_found
    tavily_api_key: str = ""
    scout_max_ingest: int = 2
    #: How many gap-fill rounds one parameter may run. Each round is
    #: scout -> ingest -> re-retrieve -> re-propose, and each is driven by what
    #: the previous round's proposal said it still lacked — so >1 lets the agent
    #: follow a chain of cross-references (the code article names an implementing
    #: order, which names another) instead of giving up after one hop. Each round
    #: costs an ingest + an embedding pass, hence the low default.
    scout_max_rounds: int = 2


def load_config() -> WorkflowConfig:
    """Build the config from .env (repo root, then Nomoscope-agentic-workflow/) and the process env."""
    load_dotenv(WORKFLOW_ROOT.parent / ".env")
    load_dotenv(WORKFLOW_ROOT / ".env", override=True)
    database_url = _env(
        "WORKFLOW_DATABASE_URL", "postgresql://jrc:jrc@localhost:5434/legislation"
    )
    return WorkflowConfig(
        database_url=database_url,
        model=_env("WORKFLOW_MODEL", "mock/extractor"),
        critique_model=_env("WORKFLOW_CRITIQUE_MODEL", "") or _env("WORKFLOW_MODEL", "mock/extractor"),
        embedding_model_id=int(_env("WORKFLOW_EMBEDDING_MODEL_ID", "99")),
        retrieval_k=int(_env("WORKFLOW_RETRIEVAL_K", "15")),
        phoenix_endpoint=_env("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006"),
        phoenix_project=_env("PHOENIX_PROJECT_NAME", "nomoscope-agentic-workflow"),
        phoenix_database_url=_env(
            "PHOENIX_DATABASE_URL", database_url.rsplit("/", 1)[0] + "/phoenix"
        ),
        electricity_mix_zone=_env("ECOLOGITS_ELECTRICITY_MIX_ZONE", "EEE"),
        tracing_enabled=_env("WORKFLOW_TRACING", "true").lower() != "false",
        scout=_env("WORKFLOW_SCOUT", "off").lower(),
        tavily_api_key=_env("TAVILY_API_KEY", ""),
        scout_max_ingest=int(_env("WORKFLOW_SCOUT_MAX_INGEST", "2")),
        scout_max_rounds=max(1, int(_env("WORKFLOW_SCOUT_MAX_ROUNDS", "2"))),
    )
