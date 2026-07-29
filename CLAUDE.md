# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A JRC (EU Joint Research Centre) expert-contract prototype that partially automates updating and validating **EUROMOD** fiscal parameters from legislation. The mission (see [00_project-overview.md](00_project-overview.md)): a temporally-aware, multilingual **RAG** over the fiscal legislation of 5 pilot member states → an **agentic workflow** that proposes structured parameter updates → a **validation UI** where a human accepts/rejects → an **evaluation pipeline** that scores the whole thing against a golden set.

**Naming:** the project codename is **Nómos**. Its three code subprojects are prefixed with their codenames on disk — `Nomotheca-RAG/` (legislation DB + ingestion, "Nomosync"), `Nomoscope-agentic-workflow/` (agentic pipeline + validation UI), `Nomokrisis-evaluation_pipeline/` (evaluation) — kept alongside the original descriptive names for readability.

The numbered top-level docs (`00_`–`07_`) are the contract plan; `01_`–`05_` map to the five deliverable "Activities". The three code subprojects each implement one Activity and depend on each other in a line: **ingest → agentic-workflow → evaluation_pipeline**, all reading/writing one shared Postgres.

## Architecture: one database, three Python packages, one desktop app

Everything centers on a single Postgres 17 + pgvector instance (see [docker-compose.yml](docker-compose.yml)):

- **`Nomotheca-RAG/ingest`** (`nomotheca-ingest`) — Activity 2. Archive-first legislation ingester. Fetches → snapshots → parses → chunks → loads the `legislation` DB, then builds BGE-M3 vector embeddings and translates non-English texts to English. Country-agnostic `core/` (~80%) + per-country adapters under `countries/<cc>/` (fetcher, parser, resolver). Adding a country is an adapter, not a rewrite; adapters are resolved via `countries/registry.py::get_adapter`. Library-first: the CLI and a future cache-miss workflow both call the same `ingest_citation` / `ingest_instrument` functions. See [Nomotheca-RAG/12_ingestion-architecture.md](Nomotheca-RAG/12_ingestion-architecture.md) for the shared/adapter boundary.
- **`Nomoscope-agentic-workflow/pipeline`** (`nomoscope-workflow`) — Activity 3. A deterministic step pipeline with **PydanticAI** LLM calls (not a free-roaming agent): `frame → retrieve → propose → critique → diff → enqueue`, one run per `(country, parameter, as_of)`. `propose` and `critique` are the only LLM steps (PydanticAI structured output); everything else is deterministic code/SQL. Writes `ReviewItem` JSON to `data/queue/`. The **anti-hallucination rule is mechanical**: an LLM's `supporting_extract` must be found character-for-character inside the cited chunk or the critique fails. Export-first — nothing writes into EUROMOD files; a human accepts in the UI.
- **`Nomoscope-agentic-workflow/ui`** — Activity 3. **Tauri 2 (Rust) + Svelte 5** desktop validation UI. Reads/writes the review queue (loosely typed in Rust so the item schema can evolve pipeline-side), appends decisions to `data/decisions.jsonl`, and has a read-only Database tab straight against the legislation DB.
- **`Nomokrisis-evaluation_pipeline`** (`nomokrisis-eval`) — Activity 4. Runs the agentic workflow (imported as an editable dependency) over a git-versioned golden set, scores KPIs with **pure deterministic code (no LLM judge)**, and stores results in an `eval` schema in the same Postgres, keyed by prompt/agent version, model, and language so per-language model comparisons (Activity 5) are a SQL view.

**Observability:** every LLM run is traced to **Arize Phoenix** (OTLP) at http://localhost:6006, storage in a `phoenix` DB in the same Postgres. Mock runs trace identically to real LLM runs. No LangSmith — `grep -ri langsmith` returns nothing by design.

**Data contract between the pieces:** the Activity 1 parameter JSON format ([Param_Schema/](Param_Schema/)). Ingest fills the legislation DB; the workflow's citations carry `jrc_database_id = chunks.id` with offsets into `unit_texts.content`; the eval golden cases are the same parameter files plus an `expected` block.

## Running things

**Everything needs the stack up first** (from repo root):

```bash
docker compose up -d          # Postgres:5434 + pgAdmin:5050 + Phoenix:6006
                              # auto-applies Nomotheca-RAG/db/schema.sql then seed.sql
docker compose down -v        # full reset (schema re-applied on next up)
```

Postgres is on host port **5434** (not 5432, to avoid clashing with a local PG). Default DB URL: `postgresql://jrc:jrc@localhost:5434/legislation`. pgAdmin admin@euromod.eu / admin.

Python packages use **`uv`**. Run commands with `uv run` from inside each package dir:

```bash
# Ingest (Nomotheca-RAG/ingest)
uv run python -m nomotheca_ingest.cli tui                 # interactive Textual ingestion monitor
uv run python -m nomotheca_ingest.cli fr instrument JORFTEXT000051168007
uv run python -m nomotheca_ingest.cli country-report FR ../country_reports/Y16_CR_FR.md   # non-legislative corpus
uv sync --extra embeddings                              # then: cli embeddings build --backend torch|openvino
uv sync --extra embeddings --extra translate            # then: cli translate run --model openrouter/...

# Agentic workflow (Nomoscope-agentic-workflow/pipeline)
uv sync
uv run nomoscope-workflow run-all --as-of 2025-06-01      # mock model — no API key needed
uv run nomoscope-workflow queue
uv run nomoscope-workflow run-all --as-of 2025-06-01 --force --model anthropic/claude-sonnet-5

# Validation UI (Nomoscope-agentic-workflow/ui)
npm install
npm run tauri dev                                       # WSL: prefix LIBGL_ALWAYS_SOFTWARE=1

# Evaluation (Nomokrisis-evaluation_pipeline)
uv run nomokrisis-eval init-db                             # create eval schema
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor   # offline smoke run
uv run nomokrisis-eval report
```

## Tests

```bash
cd Nomoscope-agentic-workflow/pipeline && uv run --with pytest pytest    # extraction, diff, queue (mock)
cd Nomoscope-agentic-workflow/ui/src-tauri && cargo test                 # decision/export round-trip
cd Nomotheca-RAG/ingest && uv run pytest                                 # testpaths=tests
cd Nomokrisis-evaluation_pipeline && uv run --extra test pytest
```

Run a single test with `uv run pytest tests/test_cli.py::test_name` (or `-k pattern`). All packages set `pythonpath=["src"]` and `testpaths=["tests"]` in `pyproject.toml`.

## Debugging a workflow run from a Phoenix trace id

Given a trace id (or "why did this run fail?"), use the **`/debug-phoenix-trace`** skill ([.claude/skills/debug-phoenix-trace/SKILL.md](.claude/skills/debug-phoenix-trace/SKILL.md)): it inspects the trace's spans straight in the `phoenix` DB inside the shared Postgres container, cross-checks corpus/embedding coverage in the `legislation` DB, and lists the known failure modes. Rule of thumb: most `not_found` runs are corpus problems (act not ingested, or ingested but not yet embedded), not LLM problems.

## LLM provider configuration

Models everywhere are **provider-prefixed strings**: `anthropic/…`, `openai/…`, `azure_openai/…`, `openrouter/…`, `together/…`, plus `mock/…` for key-less demos and deterministic tests. **Nothing in the pipeline knows the provider** — endpoint flexibility is a hard contractual requirement (Activity 5 compares multiple LLMs). The shared connection lives in [Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/llm.py](Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/llm.py); `nomotheca_ingest` and `nomokrisis_eval` both reuse it.

API keys come from `.env`. `load_config()` auto-loads `.env` only from the `euromod` repo root and `Nomoscope-agentic-workflow/`. If keys live elsewhere, `set -a; source path/to/.env; set +a` before the command. See [Nomoscope-agentic-workflow/.env.example](Nomoscope-agentic-workflow/.env.example) for all knobs.

## Key constraints when changing things

- **The workflow is export-first and human-gated.** Never make the pipeline write back into EUROMOD parameter files; accepted values are exported, and only after a human Accept in the UI. Reviewed queue items are immutable to re-runs (unless `--force`); `decisions.jsonl` is append-only.
- **The verbatim-quote rule is mechanical, not prompt-only.** If you touch `propose`/`critique`, keep the character-for-character extract check against the cited chunk — it's the anti-hallucination guarantee.
- **Country Reports are context, never evidence.** EUROMOD Country Reports are ingested with `instrument_type='country_report'` (a separate corpus class); Nomoscope's evidence retrieval SQL excludes that type, and `retrieval.country_report_search()` is the only sanctioned way to read them (query framing, UI display). Never let `propose`/`critique` cite a CR chunk — the CR describes the model, so citing it as support is circular.
- **`national_team_source` values route around the pipeline** and are never overwritten — not every EUROMOD parameter is legislation-derivable.
- **`temporal_basis: income_year` parameters (FR income-tax family) retrieve a year ahead.** EUROMOD system year = income year, but the enacting finance act is consolidated the following year, so retrieval/scout use 1 July of `as_of.year+1`, proposals back-date `valid_from` to the income-year start, and the critique's budget-act-window check flags versions older than 1 December of the income year as the previous year's value. The flag is curated (JSON `information` block + `params.parameters.temporal_basis`, preserved by re-ingest) — never derive it from the export, and don't let legal in-force dates in the legislation DB be rewritten to compensate.
- **Value scoring must normalise, not string-match.** EUROMOD stores mid-year changes as weighted averages, ~75% of FR params as formula strings (`$PSS * 4`), and period suffixes (`#m #y …`) with fixed conversion factors. Compare normalised annualised values. See the detailed "what we can/cannot do" findings at the bottom of [Nomokrisis-evaluation_pipeline/README.md](Nomokrisis-evaluation_pipeline/README.md).
- **Embeddings on the target workstation (Intel Ultra 7 265H) prefer OpenVINO over ONNX** on the local CPU path. BGE-M3 with the `fix_mistral_regex` flag is a known breakage — leave it off (details in [Nomotheca-RAG/ingest/README.md](Nomotheca-RAG/ingest/README.md)).
