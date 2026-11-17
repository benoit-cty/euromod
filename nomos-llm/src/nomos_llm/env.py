"""The repo-root .env — the one config file — and the default database URL."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

#: The dev stack's database (docker compose, host port 5434) — the one default.
DEFAULT_DATABASE_URL = "postgresql://jrc:jrc@localhost:5434/legislation"


def repo_root() -> Path:
    """The checkout: NOMOS_REPO_ROOT, else the workspace root above this package."""
    override = os.environ.get("NOMOS_REPO_ROOT")
    return Path(override) if override else Path(__file__).resolve().parents[3]


def load_env_file() -> None:
    """Load the repo-root .env without overriding the process environment."""
    load_dotenv(repo_root() / ".env")
