"""Environment-driven configuration for the workflow pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# Nomoscope-agentic-workflow/ directory (this file lives in pipeline/src/nomoscope_workflow/).
WORKFLOW_ROOT = Path(__file__).resolve().parents[3]


def _env(name: str, default: str) -> str:
    """Read an env var with a default."""
    return os.environ.get(name, default)


from nomos_llm.env import DEFAULT_DATABASE_URL, load_env_file  # noqa: E402  (re-exported)

#: The in-SQL deterministic embedder of the seed demo corpus (seed.sql's
#: `placeholder_embedding`): queries are embedded in SQL, never by an encoder.
PLACEHOLDER_MODEL_ID = 99
#: The model the corpus is embedded with (BGE-M3, embedding_models.is_default).
DEFAULT_EMBEDDING_MODEL_ID = 1
#: The key-less, deterministic model every default falls back to.
DEFAULT_MODEL = "mock/extractor"


@dataclass(slots=True)
class WorkflowConfig:
    """All runtime knobs; every field has an env-var override."""

    database_url: str = ""
    model: str = ""
    critique_model: str = ""
    embedding_model_id: int = DEFAULT_EMBEDDING_MODEL_ID
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
    """Build the config from the repo-root .env (the one config file) and the process env.

    The process environment wins, so the worker's per-job switches and a
    container's env_file are never overridden by a stray file on disk.
    """
    load_env_file()
    database_url = _env("WORKFLOW_DATABASE_URL", DEFAULT_DATABASE_URL)
    return WorkflowConfig(
        database_url=database_url,
        model=_env("WORKFLOW_MODEL", DEFAULT_MODEL),
        critique_model=_env("WORKFLOW_CRITIQUE_MODEL", "") or _env("WORKFLOW_MODEL", DEFAULT_MODEL),
        # 1 (BGE-M3) like every other package; it was 99, the demo placeholder.
        embedding_model_id=int(_env("WORKFLOW_EMBEDDING_MODEL_ID", str(DEFAULT_EMBEDDING_MODEL_ID))),
        retrieval_k=int(_env("WORKFLOW_RETRIEVAL_K", "15")),
        phoenix_endpoint=_env("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006"),
        phoenix_project=_env("PHOENIX_PROJECT_NAME", "nomoscope-agentic-workflow"),
        phoenix_database_url=_env("PHOENIX_DATABASE_URL", database_url.rsplit("/", 1)[0] + "/phoenix"),
        electricity_mix_zone=_env("ECOLOGITS_ELECTRICITY_MIX_ZONE", "EEE"),
        tracing_enabled=_env("WORKFLOW_TRACING", "true").lower() != "false",
        scout=_env("WORKFLOW_SCOUT", "off").lower(),
        tavily_api_key=_env("TAVILY_API_KEY", ""),
        scout_max_ingest=int(_env("WORKFLOW_SCOUT_MAX_INGEST", "2")),
        scout_max_rounds=max(1, int(_env("WORKFLOW_SCOUT_MAX_ROUNDS", "2"))),
    )
