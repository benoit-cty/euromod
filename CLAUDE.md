# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A JRC (EU Joint Research Centre) expert-contract prototype that partially automates updating and validating **EUROMOD** fiscal parameters from legislation. The mission (see [00_project-overview.md](00_project-overview.md)): a temporally-aware, multilingual **RAG** over the fiscal legislation of 5 pilot member states → an **agentic workflow** that proposes structured parameter updates → a **validation UI** where a human accepts/rejects → an **evaluation pipeline** that scores the whole thing against a golden set.

**Naming:** the project codename is **Nómos**. Its three code subprojects are prefixed with their codenames on disk — `Nomotheca-RAG/` (legislation DB + ingestion, "Nomosync"), `Nomoscope-agentic-workflow/` (agentic pipeline + validation UI), `Nomokrisis-evaluation_pipeline/` (evaluation) — kept alongside the original descriptive names for readability.

The numbered top-level docs (`00_`–`07_`) are the contract plan; `01_`–`05_` map to the five deliverable "Activities". The three code subprojects each implement one Activity and depend on each other in a line: **ingest → agentic-workflow → evaluation_pipeline**, all reading/writing one shared Postgres.

## Architecture: one database, three Python packages, one desktop app

Everything centers on a single Postgres 17 + pgvector instance (see [docker-compose.yml](docker-compose.yml)):

- **`Nomotheca-RAG/ingest`** (`nomotheca-ingest`) — Activity 2. Archive-first legislation ingester. Fetches → snapshots → parses → chunks → loads the `legislation` DB, then builds BGE-M3 vector embeddings and translates non-English texts to English. Country-agnostic `core/` (~80%) + per-country adapters under `countries/<cc>/` (fetcher, parser, resolver). Adding a country is an adapter, not a rewrite; adapters are resolved via `countries/registry.py::get_adapter`. Library-first: the CLI and a future cache-miss workflow both call the same `ingest_citation` / `ingest_instrument` functions. See [Nomotheca-RAG/12_ingestion-architecture.md](Nomotheca-RAG/12_ingestion-architecture.md) for the shared/adapter boundary.
- **`Nomoscope-agentic-workflow/pipeline`** (`nomoscope-workflow`) — Activity 3. A deterministic step pipeline with **PydanticAI** LLM calls (not a free-roaming agent): `frame → retrieve → propose → critique → diff → enqueue`, one run per `(country, parameter, system year)` (`--year`; `--as-of` is a deprecated alias). `propose` and `critique` are the only LLM steps (PydanticAI structured output); everything else is deterministic code/SQL. Writes `ReviewItem` JSON to `data/queue/`. The **anti-hallucination rule is mechanical**: an LLM's `supporting_extract` must be found character-for-character inside the cited chunk or the critique fails. Export-first — nothing writes into EUROMOD files; a human accepts in the UI.
- **`Nomoscope-agentic-workflow/ui`** — Activity 3. **Tauri 2 (Rust) + Svelte 5** desktop validation UI. Reads/writes the review queue (loosely typed in Rust so the item schema can evolve pipeline-side), records decisions in `params.review_decisions` (with `data/decisions.jsonl` as a redundant local copy), and has a read-only Database tab straight against the legislation DB.
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
uv run nomoscope-workflow run-targets group:FR:tinkt_fr:tin_schedule 'euromod://FR/tin_fr/def_const/$tinrt_cdhr' --year 2025
                                                        # mock model — no API key needed; one run = one system year
uv run nomoscope-workflow run-all --params-dir data/parameters/db --year 2025   # every parameter materialized so far
uv run nomoscope-workflow queue
uv run nomoscope-workflow migrate-queue-ids --apply    # one-off: date-keyed → system-year queue ids
uv run nomoscope-workflow run-all --params-dir data/parameters/db --year 2025 --force --model anthropic/claude-sonnet-5

# Validation UI (Nomoscope-agentic-workflow/ui)
npm install
npm run tauri dev                                       # WSL: prefix LIBGL_ALWAYS_SOFTWARE=1

# Evaluation (Nomokrisis-evaluation_pipeline)
uv run nomokrisis-eval init-db                             # create eval schema
uv run nomokrisis-eval build-openfisca-dataset --year 2025  # draft golden cases from the OpenFisca corpus
uv run nomokrisis-eval verify <case-id> --reviewer ben     # or the UI's "Golden set" tab
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor   # offline smoke run (one progress line per case)
uv run nomokrisis-eval resume                              # continue an interrupted run (list-runs shows them)
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

- **The workflow is export-first and human-gated.** Never make the pipeline write back into EUROMOD parameter files; accepted values are exported, and only after a human Accept in the UI. A queue item is keyed `<country>_<target>_<system year>` (`queue_store.item_id`), so re-running a year replaces its review instead of piling up near-duplicates — the UI collapses the remaining per-year runs to one row and navigates between them in the detail panel. Reviewed queue items are immutable to re-runs (unless `--force`); `params.review_decisions` is append-only and is the system of record for human decisions. **A decision the DB refuses fails outright** — `store::prepare_decision` computes, the DB insert gates, `store::commit_decision` writes, in that order, so an unreachable Postgres leaves the item pending with nothing on disk. Never reorder that to write the queue item first. `data/decisions.jsonl` is a redundant local copy, replayable with `nomoscope-workflow sync-decisions`.
- **The verbatim-quote rule is mechanical, not prompt-only.** If you touch `propose`/`critique`, keep the character-for-character extract check against the cited chunk — it's the anti-hallucination guarantee.
- **Country Reports are context, never evidence.** EUROMOD Country Reports are ingested with `instrument_type='country_report'` (a separate corpus class); Nomoscope's evidence retrieval SQL excludes that type, and `retrieval.country_report_search()` is the only sanctioned way to read them (query framing, UI display). Never let `propose`/`critique` cite a CR chunk — the CR describes the model, so citing it as support is circular.
- **`national_team_source` values route around the pipeline** and are never overwritten — not every EUROMOD parameter is legislation-derivable.
- **The parameter store is the source; parameter files are materialized from it.** `extracted_parameters/enriched/<CC>.enriched.json` is the EUROMOD-delivered ground truth and is read-only; everything else the DB needs arrives through the same `ingest-params` + `curate-params` path — `extracted_parameters/curated/<CC>.in_function.json` for parameters EUROMOD defines inside functions (the connector cannot export them; FR CDHR), and the export's own `groups` block for bracket schedules, reassembled into one record by `paramdb.load_group_record` (FR barème = `FR:tinkt_fr:tin_schedule`). Runtime inputs under `data/parameters/db|eval/` are derived artifacts, regenerated from the DB — never hand-edit one, and never let a golden case or a run depend on a hand-authored parameter file.
- **OpenFisca corroborates, it never evidences.** The ingested OpenFisca corpus (`params.external_*`, commit-pinned) is a *curated secondary source*: it can suggest links (`nomoscope-workflow match-openfisca` → `params.parameter_links`, suggestions until `validated_by` is set) and draft evaluation ground truth (`nomokrisis-eval build-openfisca-dataset` → `verified: false` cases reviewed in the UI's Golden set tab), but it can never be a `supporting_extract` for a proposal. Golden cases re-derive the expected value from the parameter's `temporal_basis`, not from the link's year alignment: `income_year` → the OpenFisca value keyed `<system year>-01-01` (the same income-year convention the pipeline back-dates to), `in_force` → the value in force at `as_of`. OpenFisca stores change points only, so "the value at D" is always the latest entry at or before D.
- **`temporal_basis: income_year` parameters (FR income-tax family) are dated by income year, not system year.** France assesses in year Y the income of year Y−1 («impôt 2025 sur les revenus 2024»), so **EUROMOD system year Y states the value for income year Y−1** — the mapping lives in exactly one place, `schema.income_year_for` (offset `INCOME_YEAR_OFFSET = -1`), and four things derive from it: retrieval/scout target 1 July of the year *after* the income year, proposals back-date `valid_from` to the income-year start, the critique's budget-act window opens 1 December of the income year (older versions route `provisional` — Accept is blocked in the UI; distinct from `not_found`), and golden cases read the OpenFisca entry at `income_year_for(year)-01-01`. Never re-derive `as_of.year ± 1` at a call site. Note the FR Country Report's Table 2.77 heads its column "Taxation 2025 (income 2025)" — that label is wrong, its values are the income-year-2024 barème. The flag itself is curated (JSON `information` block + `params.parameters.temporal_basis`, preserved by re-ingest) — never derive it from the export, and don't let legal in-force dates in the legislation DB be rewritten to compensate.
- **Value scoring must normalise, not string-match.** EUROMOD stores mid-year changes as weighted averages, ~75% of FR params as formula strings (`$PSS * 4`), and period suffixes (`#m #y …`) with fixed conversion factors. Implemented in `nomokrisis_eval.scoring.normalise_value` / `values_equal`: formulas evaluated, `$const` refs resolved via a constants map, cross-period comparison on the monthly basis, relative tolerance 1e-6 (tight enough that the FR barème 1-€ erratum still scores as a difference). See the detailed "what we can/cannot do" findings at the bottom of [Nomokrisis-evaluation_pipeline/README.md](Nomokrisis-evaluation_pipeline/README.md).
- **Embeddings on the target workstation (Intel Ultra 7 265H) prefer OpenVINO over ONNX** on the local CPU path. On the NVIDIA box (GTX 1080 Ti) OpenVINO is not an option at all — its GPU plugin is Intel-only — so that machine runs `--backend torch` on CUDA from a separate environment (`UV_PROJECT_ENVIRONMENT=.venv-cuda uv sync --extra embeddings-cuda`, cu126 wheels because Pascal is sm_61, fp32 because Pascal fp16 is 1/64 rate). The default `.venv` stays CPU+OpenVINO so the UI and `scout.py` keep working. BGE-M3 with the `fix_mistral_regex` flag is a known breakage — leave it off (details in [Nomotheca-RAG/ingest/README.md](Nomotheca-RAG/ingest/README.md)).

## Agent skills

### Issue tracker

Issues and specs live as local markdown files under `.scratch/<feature-slug>/` in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles use their default names (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), recorded as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
