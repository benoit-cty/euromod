"""Command-line entry points for the ingestion package.

`nomotheca-ingest` and `python -m nomotheca_ingest.cli` both run `app`.
Commands live by kind: `cli.ingest` (fetch, reparse and route acts and
documents) and `cli.batch` (embeddings and translation backlogs).
"""

from __future__ import annotations

from nomotheca_ingest.cli import batch, ingest  # noqa: F401 - registers the commands
from nomotheca_ingest.cli._app import app, embeddings_app, translate_app
from nomotheca_ingest.core.progress import PROGRESS_PREFIX

__all__ = ["PROGRESS_PREFIX", "app", "embeddings_app", "translate_app"]
