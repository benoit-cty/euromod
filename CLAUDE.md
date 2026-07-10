# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A JRC (EU Joint Research Centre) expert-contract prototype that partially automates updating and validating **EUROMOD** fiscal parameters from legislation. The mission (see [00_project-overview.md](00_project-overview.md)): a temporally-aware, multilingual **RAG** over the fiscal legislation of 5 pilot member states → an **agentic workflow** that proposes structured parameter updates → a **validation UI** where a human accepts/rejects → an **evaluation pipeline** that scores the whole thing against a golden set.

The numbered top-level docs (`00_`–`07_`) are the contract plan; `01_`–`05_` map to the five deliverable "Activities". The three code subprojects each implement one Activity and depend on each other in a line: **ingest → agentic-workflow → evaluation_pipeline**, all reading/writing one shared Postgres.

## Architecture: one database, three Python packages, one desktop app

Everything centers on a single Postgres 17 + pgvector instance (see [docker-compose.yml](docker-compose.yml)):

- **`RAG/ingest`** (`euromod-ingest`) — Activity 2. Archive-first legislation ingester. Fetches → snapshots → parses → chunks → loads the `legislation` DB, then builds BGE-M3 vector embeddings and translates non-English texts to English. Country-agnostic `core/` (~80%) + per-country adapters under `countries/<cc>/` (fetcher, parser, resolver). Adding a country is an adapter, not a rewrite; adapters are resolved via `countries/registry.py::get_adapter`. Library-first: the CLI and a future cache-miss workflow both call the same `ingest_citation` / `ingest_instrument` functions. See [RAG/12_ingestion-architecture.md](RAG/12_ingestion-architecture.md) for the shared/adapter boundary.
- **`agentic-workflow/pipeline`** (`euromod-workflow`) — Activity 3. A **LangGraph** pipeline (not a free-roaming agent): `frame → retrieve → propose → critique → diff → enqueue`, one run per `(country, parameter, as_of)`. `propose` and `critique` are the only LLM steps; everything else is deterministic code/SQL. Writes `ReviewItem` JSON to `data/queue/`. The **anti-hallucination rule is mechanical**: an LLM's `supporting_extract` must be found character-for-character inside the cited chunk or the critique fails. Export-first — nothing writes into EUROMOD files; a human accepts in the UI.
- **`agentic-workflow/ui`** — Activity 3. **Tauri 2 (Rust) + Svelte 5** desktop validation UI. Reads/writes the review queue (loosely typed in Rust so the item schema can evolve pipeline-side), appends decisions to `data/decisions.jsonl`, and has a read-only Database tab straight against the legislation DB.
- **`evaluation_pipeline`** (`euromod-eval`) — Activity 4. Runs the agentic workflow (imported as an editable dependency) over a git-versioned golden set, scores KPIs with **pure deterministic code (no LLM judge)**, and stores results in an `eval` schema in the same Postgres, keyed by prompt/agent version, model, and language so per-language model comparisons (Activity 5) are a SQL view.

**Observability:** every LLM run is traced to **Arize Phoenix** (OTLP) at http://localhost:6006, storage in a `phoenix` DB in the same Postgres. Mock runs trace identically to real LLM runs. No LangSmith — `grep -ri langsmith` returns nothing by design.

**Data contract between the pieces:** the Activity 1 parameter JSON format ([Param_Schema/](Param_Schema/)). Ingest fills the legislation DB; the workflow's citations carry `jrc_database_id = chunks.id` with offsets into `unit_texts.content`; the eval golden cases are the same parameter files plus an `expected` block.

## Running things

**Everything needs the stack up first** (from repo root):

```bash
docker compose up -d          # Postgres:5434 + pgAdmin:5050 + Phoenix:6006
                              # auto-applies RAG/db/schema.sql then seed.sql
docker compose down -v        # full reset (schema re-applied on next up)
```

Postgres is on host port **5434** (not 5432, to avoid clashing with a local PG). Default DB URL: `postgresql://jrc:jrc@localhost:5434/legislation`. pgAdmin admin@euromod.eu / admin.

Python packages use **`uv`**. Run commands with `uv run` from inside each package dir:

```bash
# Ingest (RAG/ingest)
uv run python -m euromod_ingest.cli tui                 # interactive Textual ingestion monitor
uv run python -m euromod_ingest.cli fr instrument JORFTEXT000051168007
uv sync --extra embeddings                              # then: cli embeddings build --backend torch|openvino
uv sync --extra embeddings --extra translate            # then: cli translate run --model openrouter/...

# Agentic workflow (agentic-workflow/pipeline)
uv sync
uv run euromod-workflow run-all --as-of 2025-06-01      # mock model — no API key needed
uv run euromod-workflow queue
uv run euromod-workflow run-all --as-of 2025-06-01 --force --model anthropic/claude-sonnet-5

# Validation UI (agentic-workflow/ui)
npm install
npm run tauri dev                                       # WSL: prefix LIBGL_ALWAYS_SOFTWARE=1

# Evaluation (evaluation_pipeline)
uv run euromod-eval init-db                             # create eval schema
uv run euromod-eval run --as-of 2025-06-01 --model mock/extractor   # offline smoke run
uv run euromod-eval report
```

## Tests

```bash
cd agentic-workflow/pipeline && uv run --with pytest pytest    # extraction, diff, queue (mock)
cd agentic-workflow/ui/src-tauri && cargo test                 # decision/export round-trip
cd RAG/ingest && uv run pytest                                 # testpaths=tests
cd evaluation_pipeline && uv run --extra test pytest
```

Run a single test with `uv run pytest tests/test_cli.py::test_name` (or `-k pattern`). All packages set `pythonpath=["src"]` and `testpaths=["tests"]` in `pyproject.toml`.

## LLM provider configuration

Models everywhere are **provider-prefixed strings**: `anthropic/…`, `openai/…`, `azure_openai/…`, `openrouter/…`, `together/…`, plus `mock/…` for key-less demos and deterministic tests. **Nothing in the pipeline knows the provider** — endpoint flexibility is a hard contractual requirement (Activity 5 compares multiple LLMs). The shared connection lives in [agentic-workflow/pipeline/src/euromod_workflow/llm.py](agentic-workflow/pipeline/src/euromod_workflow/llm.py); `euromod_ingest` and `euromod_eval` both reuse it.

API keys come from `.env`. `load_config()` auto-loads `.env` only from the `euromod` repo root and `agentic-workflow/`. If keys live elsewhere, `set -a; source path/to/.env; set +a` before the command. See [agentic-workflow/.env.example](agentic-workflow/.env.example) for all knobs.

## Key constraints when changing things

- **The workflow is export-first and human-gated.** Never make the pipeline write back into EUROMOD parameter files; accepted values are exported, and only after a human Accept in the UI. Reviewed queue items are immutable to re-runs (unless `--force`); `decisions.jsonl` is append-only.
- **The verbatim-quote rule is mechanical, not prompt-only.** If you touch `propose`/`critique`, keep the character-for-character extract check against the cited chunk — it's the anti-hallucination guarantee.
- **`national_team_source` values route around the pipeline** and are never overwritten — not every EUROMOD parameter is legislation-derivable.
- **Value scoring must normalise, not string-match.** EUROMOD stores mid-year changes as weighted averages, ~75% of FR params as formula strings (`$PSS * 4`), and period suffixes (`#m #y …`) with fixed conversion factors. Compare normalised annualised values. See the detailed "what we can/cannot do" findings at the bottom of [evaluation_pipeline/README.md](evaluation_pipeline/README.md).
- **Embeddings on the target workstation (Intel Ultra 7 265H) prefer OpenVINO over ONNX** on the local CPU path. BGE-M3 with the `fix_mistral_regex` flag is a known breakage — leave it off (details in [RAG/ingest/README.md](RAG/ingest/README.md)).
