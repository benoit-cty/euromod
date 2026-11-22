"""CLI: build the golden dataset, run evaluations, report KPIs.

  uv run nomokrisis-eval init-db
  uv run nomokrisis-eval import-golden            # seed a fresh DB: dataset/, dataset_embedding/, golden_sources/ -> eval.*
  uv run nomokrisis-eval build-openfisca-dataset --year 2025 --country FR
  uv run nomokrisis-eval build-curated-dataset --year 2025 --country IE
  uv run nomokrisis-eval build-dataset notes.md --country FR --as-of 2025-06-01 --target 'euromod://FR/…'
  uv run nomokrisis-eval list-cases
  uv run nomokrisis-eval selections                 # the selection rows (what golden_sources/ used to be)
  uv run nomokrisis-eval selection-export ES --out es.json   # edit the JSON, then:
  uv run nomokrisis-eval selection-import es.json            # ... and rebuild
  uv run nomokrisis-eval run --as-of 2025-06-01 --model anthropic/claude-sonnet-5
  uv run nomokrisis-eval run-benchmark FR --year 2025 --model mock/extractor --sample 20 --seed 1
  uv run nomokrisis-eval benchmark-report <run-id>   # EUROMOD Y-1 -> Y change matrix, OpenFisca arbitration
  uv run nomokrisis-eval resume            # continue the last interrupted run
  uv run nomokrisis-eval list-runs
  uv run nomokrisis-eval report
  uv run nomokrisis-eval build-embedding-cases     # golden cases -> retrieval cases (the workflow's own query)
  uv run nomokrisis-eval run-embeddings --embedding-model-id 2 --verified-only --k 15
  uv run nomokrisis-eval compare-embeddings        # latest run of every embedding model, side by side

Everything lives in the eval schema of the shared Postgres (ADR 0004): there
is no dataset directory, no run directory and no `--no-db`. Commands a worker
job wraps end with one `@result {json}` line on stdout.

The commands live in `commands/` — `golden` (schema, selections, drafting,
verifying), `runs` (evaluation runs and their reports) and `embeddings` (the
retrieval eval) — and register on the one app in `commands.common`.
"""

from __future__ import annotations

from .commands import embeddings, golden, runs  # noqa: F401 - registration order is help order
from .commands.common import app

__all__ = ["app"]

if __name__ == "__main__":
    app()
