# Code audit — Nómos monorepo

Date: 15 November 2026, on the working tree of `main` at `1880a77` (plus uncommitted changes to the Makefile, compose file, worker Dockerfile and READMEs).

## Scope and method

The audit looks for four things: missing factorization, files and functions that are too large, weak or wrong design patterns, and dead code. It covers the five Python packages, the SQL schemas, the two Tauri/Svelte apps and the repository layout. `08 - EUROMOD Triangulator` was inventoried, not audited.

How it was done:

- Every source module of the five packages and both apps was read. `ruff` (rules F, C901, PLR09xx) and `vulture` were used as leads only.
- Each dead-code claim was confirmed by a repo-wide grep excluding `.venv*`, `node_modules` and `target`.
- `cargo check --all-targets` was run on both Tauri crates (0 warnings). Three ingest findings were checked with read-only `SELECT`s on the dev database.
- No test suite, build or application was run. Findings marked *by reading* were not reproduced.

Paths are relative to the repository root. Line numbers are those of the working tree on the date above. Severity: **high** = causes wrong results or blocks change; **medium** = recurring maintenance cost; **low** = tidy-up.

Section 1 lists behaviour defects found along the way. They are outside the four categories asked for, but several are more urgent than any refactoring.

---

## Summary

The architecture described in `CLAUDE.md` holds where it matters: the verbatim-quote rule ends in one function on every path, evidence SQL filters on the trust class, the UI spawns nothing and writes only through the sanctioned functions, and no SQL is built from user input. The code is mostly free of commented-out blocks and TODO debris.

The problems are concentrated in six places:

1. **Hybrid search exists in four diverged copies** (pipeline, eval, UI, MCP server). The MCP copy returns Country Report chunks as citable, and the UI and MCP copies use the HNSW query shape `CLAUDE.md` forbids.
2. **The pipeline's steps are closures inside one 619-line function.** `critique`, 283 lines, enforces the anti-hallucination rule and has no direct test.
3. **The quote-verification sequence is written three times** (main citation, derivation operands, chat), and the chat copy is weaker.
4. **Country adapters repeat each other.** Four fetchers carry the same retry loop, three adapters the same `expand()`, and the TUI re-implements the ingest pipeline.
5. **Shared front-end code is copied between the two apps** while the Rust is shared through `#[path]`. Inside the review UI, "run a job and show its progress" is built three times.
6. **The repository carries a lot of dead weight**: a non-importable MCP package, 234 files of retired file-era data, and the Triangulator at 73 % of tracked files.

Largest files and functions:

| File | Lines | Largest function |
|---|---|---|
| `Nomoscope-agentic-workflow/pipeline/src/nomoscope_workflow/pipeline.py` | 1 756 | `build_workflow` 619, of which `critique` 283 |
| `…/nomoscope_workflow/retrieval.py` | 1 491 | `locate_named_units` 117 |
| `Nomokrisis-evaluation_pipeline/src/nomokrisis_eval/cli.py` | 1 182 | `report` 93 |
| `…/nomoscope_workflow/paramdb.py` | 1 150 | `load_group_record` 113 |
| `Nomoscope-agentic-workflow/ui/src-tauri/src/db.rs` | 1 066 | `stats` 220 |
| `Nomotheca-RAG/ingest/src/nomotheca_ingest/cli.py` | 944 | `build_chunk_embeddings` 157, 19 parameters |
| `…/nomoscope_workflow/scout.py` | 940 | `run` 132 |
| `…/nomotheca_ingest/core/contributed.py` | 804 | `ingest_document` 151 |
| `…/ui/src/lib/components/DetailPanel.svelte` | 780 | — |
| `…/ui/src/lib/components/IngestTab.svelte` | 714 | — |

---

## 1. Defects found along the way

These are behaviour problems, listed first because they outrank the refactoring.

| # | Severity | Defect | Where | Status |
|---|---|---|---|---|
| D1 | high | A failed ingest leaves no trace. The `failed` status is written inside the transaction that psycopg rolls back when the exception is re-raised, so the run row and every snapshot of that run disappear. The dev database holds 3 965 `succeeded` runs and not one `failed`. Archive-first does not hold on failure. | `nomotheca_ingest/core/pipeline.py:85-104`, `core/country_reports.py:127-165`, `core/contributed.py:636-729` | **Fixed** — `core/db.fetch_run()` keeps the run row and snapshots on an autocommit connection and loads on its own; used by the pipeline, Country Reports, contributed documents and the TUI. Test: `tests/test_fetch_run.py` |
| D2 | high | The MCP search has no `source_trust_class <> 'context'` filter and does not return the class. Country Report chunks come back as "citable fiscal legislation". | `mcp-server/src/nomotheca_mcp/search.py:38-57, 202-224` | **Fixed** — the MCP search calls `search_chunks()`, which excludes `context`; `source_trust_class` is returned. Live test `test_country_reports_are_never_returned` |
| D3 | high | `readiness.py` still uses the pre-offset income-year model: it checks the finance act for Y+1 for system year Y. The banner announces "N income-year parameters will be provisional" when LF 2026 is missing for a 2025 run, which is false. | `nomoscope_workflow/readiness.py:3-7, 81` against `schema.py:57-72` | **Fixed** — `readiness.vintages_for` derives the income-year vintage from `schema.income_year_for`; for 2025 it probes LF 2025 only, for both families. Test: `tests/test_readiness.py` |
| D4 | high | With `-j 4` on the host, eval threads share one query-encoder subprocess pipe with no lock. Two cases can read each other's query vector. Inside the worker (`WORKFLOW_ENCODER=db`) the path is not taken. | `nomoscope_workflow/query_encoder.py:139-148`, `nomokrisis_eval/runner.py:293` | **Fixed** — each subprocess (encoder and reranker) has a lock held for its request/response pair. Test: `test_threads_never_read_each_others_vector` |
| D5 | high | One encode failure (a 60 s timeout while the GPU is busy is enough) sets `_disabled` for the rest of the process. An eval run is one process with hundreds of cases, so the rest of the run is FTS-only and nothing in `eval.results` records it. | `query_encoder.py:160-174` | **Fixed** — only an encoder that cannot start disables the leg; any other failure pauses it `WORKFLOW_ENCODER_COOLDOWN` s (30) and the next query retries. FTS-only hits now carry `method="fts"`, and `CaseResult.vector_leg` / the summary's `fts_only` count record it per case |
| D6 | high | The worker image and the package test environments run different dependency versions. Tests run on pydantic-ai 2.14.1, openai 2.46, anthropic 0.116, transformers 4.57; the image runs 2.47.0, 3.17.0, 1.7.0 and 5.0.0. | the five `uv.lock` files | **Fixed** — one uv workspace (root `pyproject.toml`) and one root `uv.lock`, seeded from the worker's lock so the versions the image ran are kept; the image installs from it (`uv sync --package nomergon-worker`). Image rebuilt, worker recreated, mock workflow jobs run |
| D7 | medium/high | Accept can record a proposal the reviewer never saw. `save_decision` sends only `item_id`; the item is re-read and `params.decide_review_item` overwrites it with no check on `run_id`. A re-run between load and click is signed off unseen. | `ui/src-tauri/src/store.rs:224-226`, `pipeline/db/params_schema.sql:501-506` | **Fixed** — the UI sends the `run_id` on screen; `store::check_seen_run` refuses a re-run item, and `decide_review_item` locks the row (`FOR UPDATE`) and raises when the queued run is not the entry's. Tests: `a_rerun_since_opening_is_refused`, `decision_round_trip_smoke` |
| D8 | medium | Database errors reach the user as "db error". `postgres::Error`'s `Display` prints only the kind; `store.rs` has a `describe()` helper for this and no other module uses it. Two error-string matches (`db.rs:273`, `db.rs:790`) can therefore never fire. | `ui/src-tauri/src/db.rs`, `jobs.rs`, `golden.rs`, `rag-ui/…/conversations.rs` | **Fixed** — new `ui/src-tauri/src/pg.rs` (`connect` + `describe`, compiled into both apps) replaces the five `connect()` copies; every Postgres error goes through `describe`, so the two string matches fire |
| D9 | medium | The UI and MCP vector legs use `ORDER BY e.embedding <=> q LIMIT n` beside filters, the shape that walks HNSW and filters afterwards. Both hard-code `model_id = 1`. | `ui/src-tauri/src/db.rs:899-911`, `mcp-server/src/nomotheca_mcp/search.py:81-86` | **Fixed** — both call `search_chunks()` (vector leg ranked in a window function) with the default model from `embedding_models.is_default`, and send that `model_id` in the encode payload. `retrieval._ACT_NEAREST_SQL` hardened the same way |
| D10 | medium | Machine translations go stale. A version counts as translated when any target-language row exists, and nothing stores the source text's hash. After `reparse`, the English row and its chunks keep the old text. | `nomotheca_ingest/core/translate.py:179-200, 269-289` | **Fixed** — each machine translation stores `metadata.source_content_hash`; a differing source hash makes the version pending again, and the new translation replaces the row in place. `migrations/0006` stamped the 25 721 existing rows with their source's current hash (already-stale rows cannot be detected). Test: `tests/test_translate_staleness.py` |
| D11 | medium | Cancelling a job signals only the direct child. A grandchild started by the scout (an ingest or an embeddings build) keeps running, possibly on the GPU and holding the advisory lock, while the job reads `cancelled`. | `nomergon/runner.py:175-186, 285-296` | **Fixed** — the job runs in its own session; cancel/stop SIGTERMs then SIGKILLs the process group, and the group is swept when the job ends. Test: `test_cancel_also_stops_what_the_job_started` |
| D12 | medium | The worker's encode lane opens one connection and never reconnects. After a Postgres restart it logs a traceback every second while the heartbeat still reports a live worker. | `nomergon/encoder.py:77-93` | **Fixed** — the lane drops a broken connection and reconnects with back-off (1 s → 30 s); waits use the stop event. Test: `tests/test_encode_lane.py` |
| D13 | medium | `save_drafted_case` commits the new ground truth, then resets the verdict in a second statement. A crash between the two leaves a changed expectation with the old approval. | `nomokrisis_eval/golden_store.py:183-203` | **Fixed** — `save_drafted_case` locks the row and writes the case and the verdict reset in one transaction. Test: `test_a_failed_verdict_reset_leaves_the_old_ground_truth` |
| D14 | medium | An eval run passes `manifest.as_of` for every case and ignores each case's own `as_of`. Golden builders also anchor on 1 June while production `--year` runs anchor on 1 July. | `nomokrisis_eval/runner.py:248-250`, `cli.py:256, 288` | **Fixed** — each case runs and is scored (constants included) on its own `as_of`; `schema.system_year_anchor` (1 July) is the one anchor for `--year`, the benchmark and both golden builders. A verdict survives an anchor move inside the same system year when the expectation is unchanged |
| D15 | medium | The static system prompts still say `valid_from` is "1 January of the reference year (the income year)", while the parameter block demands 1 January of Y−1. | `nomoscope_workflow/prompts.py:52-53, 124-125` | **Fixed** — both system prompts now say 1 January of the income year the parameter block names (the year before the system year); `PROMPT_VERSION` 0.14.1. Test: `test_static_prompts_agree_with_the_income_year_offset` |
| D16 | medium | Partial HNSW indexes exist only for models 1 and 99. Models 2, 5, 6 and 8 hold 14 482 vectors each with no index; `ensure_embedding_model` inserts the row only. | `nomotheca_ingest/core/embeddings.py:511-535`, `Nomotheca-RAG/db/schema.sql:328` | **Fixed** — `ensure_embedding_model` creates `emb_hnsw_m<id>` with the row; `db/migrations/0005_hnsw_every_model.sql` backfilled 2, 5, 6, 8 (applied to the dev DB) |
| D17 | low | `JobsTab` parses Postgres timestamps with `Date.parse`, which `labels.js:65-74` says WebKit refuses. | `ui/src/lib/components/JobsTab.svelte:96-97` | **Fixed** — `duration()` uses `labels.parseTimestamp` |
| D18 | low | `DetailPanel` re-seeds its form on the `item` object identity, so the ribbon's Refresh discards unsaved corrections and the note. | `ui/src/lib/components/DetailPanel.svelte:133-141` | **Fixed** — the form re-seeds on a content key (item id, run, status, decision time), not on object identity, so Refresh keeps unsaved edits |

---

## 2. Cross-package findings

### 2.1 Concepts defined more than once

| Concept | Definition sites | Kept in step by a test? | Severity |
|---|---|---|---|
| Hybrid search SQL | `nomoscope_workflow/retrieval.py:164-275`; `nomokrisis_eval/embedding_eval.py:75-106, 310-322`; `ui/src-tauri/src/db.rs:868-921`; `mcp-server/src/nomotheca_mcp/search.py:38-108` | **Fixed**: one SQL function `search_chunks()` (+ `fts_or_query`, `jurisdiction_tree`) in `schema.sql` / `migrations/0004_search_chunks.sql`, called by all four. Verified hit-for-hit against the old pipeline SQL on FR/LT/ES/NL/IE queries (only tie order differs, now deterministic) | high |
| Quote matching | `retrieval.py:1411-1458` (`verify_extract`, `quote_span`); `chat.py:412-417` (`_contains`); `rag-ui/src/lib/chat.js:81-93` (`locateExtract`) | **Fixed** (Python): `nomoscope_workflow/quotes.py` holds `verify_extract`, `quote_span`, `closest_passage`, the resolve/re-point helpers and `check_quote`, used by the main citation, every operand and the chat; the JS `locateExtract` port is tracked with the desktop-app work | high |
| Value parsing | `nomokrisis_eval/scoring.py:176-243`; `paramdb.py:85-126`; `pipeline.py:1229-1293` (a second AST evaluator); `benchmark.py:61-126` | No. `8,17%` parses in `paramdb` only; `100%*$MMS` in `scoring` only | medium |
| Encode-job submit-and-poll | `nomergon/client.py:25-63`; `nomoscope_workflow/encode_client.py:21-41`; `nomotheca_mcp/encoder.py:97-149`; `ui/src-tauri/src/jobs.rs:247-264` | No. Priority 100 is a literal in each | medium |
| Job types | `Nomergon-worker/db/ops_schema.sql:21-23` and again `:51-53`; `nomergon/jobs.py:24-35, 206-217, 230-239, 260-372, 449-455`; `nomergon/cli.py:102`; `Home.svelte:71-80`; literals in `IngestTab.svelte:270-296` | **Fixed** (Python ↔ SQL): `JOB_SPECS` + `tests/test_job_specs.py`; `job_types.json` for the UI | medium |
| Country tables | `countries/registry.py:13-19`; `core/contributed.py:96-133`; `scout.py:78-155, 205-225, 247`; `retrieval.py:31`; `readiness.py:29`; `ui/src/lib/labels.js:38-45`; `handoff.js:15-23`; `rag-ui/src/lib/chat.js:4` | Scout ↔ adapters and ES regions only | medium |
| "Value EUROMOD holds on a date" | `pipeline.py:450-455`; `nomokrisis_eval/build_dataset.py:78-82` (byte-identical); `paramdb.py:641, 822`; `benchmark.py:79-86`; `curated_golden.py:65-70` | No | medium |
| Units and source types | `paramdb.py:262-274`; `schema.py:85-92`; `params_schema.sql:638-646`; `ParameterEditor.svelte:15-24`; `DetailPanel.svelte:41-49` | Python ⊆ SQL only, and only with a live DB | low |
| Default DSN literal | 5 Python sites, 1 worker constant, 2 Rust sites, about 8 Rust test sites | — | low |
| Placeholder model id `99` | `config.py:27, 62`; `retrieval.py:260, 319`; `chat.py:245`; `scout.py:778`; `embedding_eval.py:250, 254` | **Fixed**: `config.PLACEHOLDER_MODEL_ID` at every site | low |

Suggested fixes, in order of value:

- **Search.** Put the candidate set and ranking in one SQL function in `schema.sql` (for example `search_chunks(scope, lang, as_of, qvec, …)`) and call it from all four places. At minimum, add the trust-class predicate and column to the MCP copy now.
- **Quotes.** Move `quote_span`, `verify_extract`, `closest_passage`, `_resolve_chunk_by_extract`, `_repoint_misquoted` and `_resolve_chunk_id` into one `nomoscope_workflow/quotes.py`. Use it from `pipeline.py` and `chat.py`, and port its two tolerance rules to `locateExtract`.
- **Values.** One `nomoscope_workflow/values.py` holding `NormalisedValue`, the period table and a single safe arithmetic evaluator. The derivation check adds its constant whitelist on top; the eval already depends on the workflow.
- **Job types.** One `JobSpec(name, payload_model, cwd, argv, result, priority, singleton)` table in `nomergon/jobs.py`, a test that compares it with the SQL `CHECK`, and exported JSON Schemas checked in the UI's `npm test`.

### 2.2 Dependency direction and configuration

- **The base package is the workflow, not ingest** (medium). Ingest imports `nomoscope_workflow.llm` and `.config` (`nomotheca_ingest/cli.py:619`, `core/translate.py:94-95`), and the workflow calls ingest by subprocess (`scout.py:546, 607`, `query_encoder.py:123, 187`). That is a runtime cycle across two mechanisms. Extracting `llm.py` and config loading into a small shared package would let the scout import `ingest_instrument` directly and remove the `EUROMOD_INGEST_DIR` / `NOMOS_PYTHON` / `.venv-cuda` discovery code.
- **Config loading is not one `load_config()`** (medium). There are three dotenv loaders (workflow, eval, worker). Ingest and the MCP server have none. Five environment names address the same database: `WORKFLOW_`, `EVAL_`, `WORKER_`, `EUROMOD_DATABASE_URL` and bare `DATABASE_URL`. `EUROMOD_DATABASE_URL` is not in `.env.example`.
- **Fixed** — `WORKFLOW_MODEL` defaults to `mock/extractor` in the workflow, eval and worker; the embedding model id defaults to 1 everywhere (`config.DEFAULT_EMBEDDING_MODEL_ID`; `.env.example` too). — **Defaults disagree** (medium). `WORKFLOW_MODEL` defaults to `mock/extractor` in the workflow and to `""` in the eval and the worker. The embedding model id defaults to 99 in `config.py` and to 1 in six other places.
- **Fixed** (`tracing.progress_enabled()`, `scout.embed_timeout()` read at call time) — **Two environment variables are read at import**, before any `.env` is loaded, so setting them in `.env` has no effect: `WORKFLOW_SCOUT_EMBED_TIMEOUT` (`scout.py:46`) and `WORKFLOW_PROGRESS` (`tracing.py:31`). *By reading.*
- **Fixed** — the eval imports `routing.derived_refs`, `derivation.extract_states`, `temporal.retrieval_as_of`; chat uses `scout.web_search` / `scout.known_instruments`. — **The eval and chat reach into private names** (medium). `pipeline._extract_states`, `_current_value`, `_derived_refs`, `_retrieval_as_of` are imported by the eval; `scout._web_search_unavailable`, `_tavily_search`, `_known_instruments` by `chat.py:331-342`. They are public API under private names.

### 2.3 Schemas

- **Fixed** (`schema_migrations` table, `make migrate`, a test that schema.sql records every migration) — **Two migration styles and no version tracking** (medium). `Nomotheca-RAG/db/schema.sql` is non-idempotent and applied only by initdb, with hand-run files under `db/migrations/`. The other three schemas are idempotent files with `ALTER … IF NOT EXISTS` inlined.
- **Fixed** — the five commands call `paramdb.require_schema` (refuse with a hint) instead of applying the schema; only `init-param-db` applies it. — **Schema application is a side effect of ordinary commands** (medium). `paramdb.apply_schema` runs inside `ingest-params`, `curate-params`, `ingest-openfisca`, `match-openfisca` and `translate-params` (`nomoscope_workflow/cli.py:324, 347, 373, 406, 453`). Each run drops and re-adds a constraint and replaces the `SECURITY DEFINER` functions. Under `roles.sql`, where the worker has DML only, this would fail. *By reading.*
- **Fixed** — `seed.sql` keeps the reference rows; the demo corpus moved to the opt-in `db/demo.sql`. — **`seed.sql` mixes required reference rows with a demo corpus** (medium): Belgium/Justel, the placeholder model 99 and a hand-written CGI art. 197 sit in every fresh database (`Nomotheca-RAG/db/seed.sql:96-298`). Split into `reference.sql` and an opt-in `demo.sql`.
- **Fixed** — both count `euromod_discrepancy` and FTS-only cases; a live test keeps the Python summary and `eval.run_summary` in step. — **The KPI summary is defined in Python and in SQL** (medium): `nomokrisis_eval/runner.py:461-558` and the views in `db/eval_schema.sql:99-225`, with a "keep the two in step" comment. `euromod_discrepancy` is in neither.

### 2.4 Tooling

- **No shared lint, format, type-check or CI configuration** (medium). There is no `[tool.ruff]`, mypy, pyright, pre-commit or workflow file. The Makefile has no `test` or `lint` target; eight suites are run by hand from eight directories. 28 skip sites depend on a live database. **Partly fixed**: `make test` (and `make sync`) runs all eight suites; tests that raced a live worker now skip when one is alive.
- **Fixed** — **Five independent `uv.lock` files** (high, see D6). A uv workspace with one root lock removes the drift.
- **Packages only work as editable installs** (low): SQL files, curation YAML and the repo root are found by walking up from `__file__`.
- **Fixed** — `pytest` and `textual` are runtime dependencies of ingest, so both ship in the worker image. Now: `pytest` in the dev group, `textual` in a `tui` extra (and the dev group); the CLI imports the TUI lazily.

---

## 3. Ingest — `Nomotheca-RAG/ingest`

### Missing factorization

| Severity | Finding | Where |
|---|---|---|
| high | The TUI re-implements the ingest pipeline instead of calling it. The copies have diverged: the TUI files a KALI id under `FR-LEGI`, uses `source_type="direct_id"` and writes a trigger value that is not in `Trigger`. **Fixed**: the TUI calls `core.pipeline.ingest` / `run_database_ingest` with an `on_fetch` callback; its two identical modes became one, and the source code defaults to the adapter's. | `tui.py:205-328` against `core/pipeline.py:67-105, 205-222` |
| high | The fetch-run lifecycle is pasted four times and `LoadStats` summing five times. A `fetch_run()` context manager in `core/db.py` would also fix D1 in one place. **Fixed**: `fetch_run()` and `LoadStats.total()`. | `core/pipeline.py:85-104`, `core/country_reports.py:137-165`, `core/contributed.py:646-729`, `tui.py:213-323` |
| high | Four fetchers define the same `_RETRY_STATUSES`, attempt count and back-off loop; the FR fetcher has no retry. `tenacity` is already a dependency. **Fixed**: one `core.snapshots.get_with_retries` (every attempt archived, per-country attempt count), used by all five fetchers, FR included. | `countries/{es,ie,lt,nl}/fetcher.py` |
| high | `expand()` is byte-identical in the FR, LT and NL adapters, and IE differs by two fields. The parser hands children over as untyped dicts with magic keys. **Fixed**: one `BaseAdapter.expand` (IE overrides `child_metadata`/`child_reason`); the child dicts remain. | `countries/fr/adapter.py:88-104`, `lt/adapter.py:48-64`, `nl/adapter.py:49-65` |
| medium | `store_translation` duplicates the loader's text and chunk inserts, with a different conflict rule. This divergence is the cause of D10. **Fixed**: chunks go through `LegislationLoader.write_chunks` (stable ids, cited chunks retained); the text row is upserted on the same key as the loader's. | `core/translate.py:269-333` against `core/loader.py:334-368, 433-466` |
| medium | The embeddings and translation commands are twins: the same Rich progress skeleton, JSON adapter and stats class. | `cli.py:726-901`, `core/embeddings.py:410-419`, `core/translate.py:159-176` |
| medium | Small helpers are repeated across parsers: the ltree token (6 copies), accent folding (3, inside one country), table rendering (3), sha256 of text (6), month tables (3). The unique-citation rule, behind two recorded incidents, is enforced separately in four places. | `countries/*/parser.py`, `core/documents.py` |
| medium | ES keeps its act aliases twice; the resolver imports `KNOWN_ACTS` and never uses it. NL and LT derive theirs from the one table. **Fixed**: `_ALIASES` = every `KNOWN_ACTS` label (folded) + `_EXTRA_ALIASES` for synonyms (57 → 35 hand-kept). | `countries/es/resolver.py:25-97`, `es/parser.py:38-67` |
| low | Two reparse paths, two headless-browser launchers, two identical extras (`legifrance`, `browser`). | `core/pipeline.py:119-183`, `core/contributed.py:733-804` |

### Size

- **`cli.py`** (944 lines) holds ingest commands, the embedding advisory lock, the batch commands and progress rendering. The lock is a correctness rule living in the CLI layer, so `build_embeddings` called as a library takes no lock. Split into `cli/ingest.py`, `cli/batch.py`, `core/progress.py`, and move the lock into `core/embeddings.py`.
- **`core/contributed.py`** (804 lines) holds the kinds tables, value objects, HTTP and browser fetching, `ingest_document` and `reparse_documents`. Split into `kinds`, `fetch` and `ingest`.
- **`core/embeddings.py`** (599 lines) is two modules: model loading and hardware (`:51-342`), and the database build loop (`:345-599`).
- **`build_document`** (`core/documents.py:253`, 174 lines, 19 parameters) does five jobs in sequence.
- **`es/parser.py`** (565 lines) is two parsers, consolidated API and daily gazette, with the `InstrumentIR` construction and the container-stack loop duplicated between them.

### Design

- **Fixed** — **The adapter protocol is not what core relies on** (high). `CountryAdapter` now declares everything core calls, `BaseAdapter` supplies the defaults (and the one `expand()`), core has no `getattr`; `write_snapshot` stores the `SourceRef` in `fetch_snapshots.metadata` and `reparse` replays it for any country (FR's URL rebuild remains for older snapshots). Original finding: `countries/base.py:54-72` declares five methods. Core reads four more by `getattr`: `url_source`, `source_code_for`, `default_source_code`, `source_ref_from_url`. Only FR implements the last, so `reparse` works for one country of five, by reverse-engineering the id from the snapshot URL. `fetch_snapshots.metadata` exists and is never written; storing the `SourceRef` there removes the per-country code.
- **Country specifics in core** (medium): `KINDS_BY_JURISDICTION` in `core/contributed.py:96-150`, French month names in `core/extract.py:58-69` and `core/documents.py:131-135`, a CGI special case in `fr/parser.py:294`. There are no `if cc == "FR"` branches.
- **No error taxonomy** (medium). `cli.py:280-282` catches `ValueError` around the whole of `ingest_document` and reports it as a reviewer-facing refusal, so a parser `ValueError` reads as a badly filled form.
- **Fixed** — **The loader never revises an existing version** (medium). `_revise_version` now shortens a held version to a later-learned end, records a non-in-force status and the new provenance snapshot (only ever shortening, so no overlap). Test: `tests/test_loader_versions.py`. Original finding: A known `source_version_id` returns the row untouched, dropping a later-learned `valid_to`; otherwise a version is matched by start date alone and its text overwritten (`core/loader.py:284-307`). *By reading.*
- **Stringly-typed vocabularies** (medium): `mode`, about ten free-text `SourceRef.source_type` values that no parser dispatches on, run status literals in four files.
- **Low**: nine connection sites with no helper; a new `httpx.Client` per request (`core/snapshots.py:51`); `tui.py` imported eagerly by every CLI call (**fixed**: lazy import); `commit_each_batch` is always `True`.

### Dead code

| Severity | Item | Where |
|---|---|---|
| medium | `_probe_backend_kwargs.py`, `_probe_tokenizer.py`: each is one docstring, "Deprecated temporary probe; safe to delete." **Fixed (deleted).** | `Nomotheca-RAG/ingest/` |
| medium | `canary_facts()` in five adapters, `CanaryFact` and the protocol method: about 130 lines that no runner calls. **Fixed by use**: `core/canary.py` + `cli canary [CC…]` check every fact against the corpus (exact folded citation, not trigram); 11/11 OK on the dev DB; live test `tests/test_canary.py`. | `countries/*/resolver.py`, `core/ir.py:200-207` |
| medium | `FrResolver`, a placeholder whose `resolve` raises `NotImplementedError`; `cli citation FR …` cannot work. **Fixed**: resolves what a reviewer can paste (DILA id, Legifrance/ELI URL, NOR) through `resolve_legifrance_url` and refuses free text by name. | `countries/fr/resolver.py:222-232` |
| low | TUI modes "bill" and "direct" behave identically; `PipelineTui._log_snapshots` has no caller. **Fixed** (merged into one mode; method removed). | `tui.py:134, 392-399` |
| low | Test-only functions: `es/fetcher.html_url`, `es/regions.by_nuts2`, `contributed.trust_class_for`. The last means the guidance-publisher test checks a helper, not the production property. **Fixed**: the first two deleted; `ContributedFields.source_trust_class` now goes through `trust_class_for`. | — |
| low | Fields never set or read: `CitationRef.instrument_id`, `.article_number`, `SourceRef.url`, `DocumentResult.fetch_run_id`, `.snapshot_id`, `EmbeddingModelSpec.extra`. **Fixed**: four removed; `fetch_run_id` and `snapshot_id` are now printed by `cli document` (provenance). | `core/ir.py`, `core/contributed.py`, `core/embedding_models.py` |
| low | Schema objects with no reader or writer: view `current_legal_texts`, function `resolve_rag_uri`, `fetch_snapshots.storage_ref/parser_version/metadata`, `instruments.in_force`, `fts_de`. **Fixed**: the view and the column dropped (`migrations/0007`). Kept on purpose: `resolve_rag_uri` (the documented rag:// contract), `storage_ref` (large-PDF store, open deployment question), `fts_de` (BE German). `metadata` is now written (section 3, design). | `Nomotheca-RAG/db/schema.sql` |
| low | Stale docstrings: `core/embeddings.py:567-572`, `core/contributed.py:6-7`, `db/schema.sql:5`. **Fixed.** | — |

---

## 4. Agentic workflow — `Nomoscope-agentic-workflow/pipeline`

### Missing factorization

| Severity | Finding | Where |
|---|---|---|
| high | The resolve → repoint → verify → hint sequence runs twice, once for the main citation and once per operand, with different messages. `_MISQUOTE_ISSUE` needs four alternatives to recognise them. **Fixed**: one `quotes.check_quote` returns a structured `QuoteCheck`; the two callers only word the issue. | `pipeline.py:622-655` and `1462-1487` |
| high | A third, weaker copy of the quote rule lives in chat. **Fixed**: `chat.resolve_quote` goes through `quotes.check_quote` (split-ligature and edge-punctuation rules included). | `chat.py:388-417` |
| high | The `RetrievalHit` column list is pasted 14 times and the five-table join about 15. Adding a field to `RetrievalHit` means editing 14 SQL strings. **Fixed** for every query that selects a plain hit: `retrieval.HIT_COLUMNS` and `CHUNK_JOINS` (7 column lists, 3 joins); the remaining variants (DISTINCT ON, alias-renamed units) stay explicit. | `retrieval.py` (e.g. `:106, 142, 416, 656, 1017, 1273`) |
| medium | Cursor boilerplate about 17 times; the "skip seen, wrap as located, stop at cap" loop six times; the `rsplit("art. ")` idiom four times. | `retrieval.py`, `scout.py:915-939` |
| medium | Scope, language and query vector are derived again at each entry point. | `pipeline.py:565-567`, `scout.py:901-904`, `retrieval.py:313`, `chat.py:250, 279` |
| medium | The scout has two ingest loops and two subprocess launchers; `query_encoder._start` and `_start_reranker` are copies. **Partly fixed**: one `query_encoder._spawn_ready` launches both (tested live with the subprocess encoder); the scout's loops remain. | `scout.py:535-551, 759-774, 853-874`, `query_encoder.py:114-211` |
| medium | Tavily access and the 432 latch are duplicated between scout and chat, and both sniff `"432" in str(exc)`. **Fixed**: one `scout.web_search` with one latch keyed on the HTTP status (`WebSearchUnavailable`), used by discovery, guidance search and chat. | `scout.py:735-744`, `chat.py:331-342` |
| low | `next(h for h in hits if h.chunk_id == x)` eight times; half-up quantisation three times (**fixed**: `derivation.round_half_up`); two `connect()` helpers with different row factories; `critique` opens up to five connections per call. | `pipeline.py`, `paramdb.py:53`, `retrieval.py:185` |

### Size

- **Fixed** (pipeline.py 1 756 → 948 lines: `framing.py`, `temporal.py`, `derivation.py`, `routing.py` extracted; `quotes.py` earlier; pipeline re-exports the old names) — **`pipeline.py`** (1 756 lines) splits into:
  - `framing.py` — query cleaning and `frame_query`;
  - `temporal.py` — reference dates, the income-year checks, `_consolidated_in_force`;
  - `quotes.py` — see section 2.1;
  - `derivation.py` — the evaluator, operand checks and rounding, about 380 lines, pure and already the best-tested part;
  - `routing.py` — value comparison and record merging;
  - `pipeline.py` — the steps and `run_parameter`.
- **`critique`** is four checks in one function: citation, derivation, income-year vintage (about 120 lines, three levels of nesting, three DB round trips) and in-force dates, then the LLM merge. Each should return `(issues, notes, flags)`.
- **`retrieval.py`** (1 491 lines) splits into `corpus.py`, `search.py`, `crossrefs.py` (about 650 lines), `locate.py` and `country_report.py`.
- **`scout.py`** (940 lines) holds static per-country tables, discovery prompts, a Tavily client, subprocess launchers and the corpus-side `locate`, which touches neither web nor ingest.
- **`tests/test_workflow.py`** is 1 396 lines and 78 tests on unrelated subjects, with a second import block mid-file and about 20 private names imported.

### Design

- **Fixed** — **The steps are closures** (high). The steps are module-level `step(ctx, state)` functions; `StepContext` injects the proposer and the critic (LLM or mock), which replaced the four `is_mock` branches; `tests/test_steps.py` calls `critique` and `diff` directly. Original finding: `frame`, `retrieve`, `propose`, `critique`, `diff` and `enqueue` are nested in `build_workflow` (`pipeline.py:533-1151`) and cannot be imported. No test calls `critique` or `diff`; the only end-to-end tests take the national-team short-circuit, which skips retrieve, propose and critique. Module-level `step(ctx, state) -> delta` functions with an injected proposer and critic would also remove the four `is_mock` branches.
- **Fixed** — `issues.py` holds the wording of every routed issue and `code_of` (built from the same constants) classifies them; `_needs_gap_fill` and `misquoted_only` route on `IssueCode` sets. — **Control flow is keyed on free-text issue strings** (medium). `_SOURCE_GAP_ISSUES` (`pipeline.py:349-353`) and `_MISQUOTE_ISSUE` (`:1377-1382`) decide scout rounds and extra attempts by matching message text; `note:` and `model:` prefixes are a protocol. Rewording a message changes routing. Use `Issue(code, text, blocking)`.
- **State handling is inconsistent** (medium). `WorkflowState` is a `TypedDict(total=False)`; most steps return a delta, but `scout_step`, `locate_step`, `critique` and `_round_like_held` mutate their inputs.
- **French legal idiom sits in generic modules** (medium). `_CODE_ARTICLE_REF`, `"même code"`, `_SAME_ACT_REF`, the `"art. "` convention, chapter inference, `_APPLICABILITY` and `_NUMBER_WORDS` run for every country and simply do not match elsewhere. Ingest has `countries/<cc>/` adapters; the workflow has none.
- **Fixed** — DB errors in `_known_instruments` and the income-year check now fail the run instead of silently changing it; LLM calls retry only transient errors (not ValueError/KeyError/TypeError/UserError). — **Broad `except Exception` changes results** (medium). A DB error in `scout._known_instruments` (`scout.py:491`) returns an empty set, so everything is re-ingested. A DB error during the income-year check (`pipeline.py:701, 709, 763`) can flip a correct proposal to `provisional`. `llm.py:203, 224` retries a missing-key error three times with back-off.
- **Fixed** (the prompt shows `routing.current_value(record, as_of)`, the latest only when nothing is held; prompt 0.14.3) — **Two definitions of "current value"** (low/medium). The prompt shows `record.values[-1]` (`prompts.py:224`); `diff` routes against `_current_value(record, as_of)` (`pipeline.py:896`).
- **Low**: `COUNTRY_SOURCES` and `GUIDANCE_PUBLISHERS` are dicts of dicts; `temporal_basis` is compared to string literals (**fixed**: `TemporalBasis`); `llm.run_agent` adds `timeout` after `model_settings()`; `impact.py:31-55` is a second place that parses provider strings.

### Dead code

| Severity | Item | Where |
|---|---|---|
| medium | `paramdb.record_decision`: no caller, no test. **Removed.** | `paramdb.py:1093-1150` |
| medium | **Removed** (fields, prompt line, `sibling_text`, `translation_lookup`; prompt 0.14.2) — `ProposalDraft.original_language_quote` and `english_translation` are requested from the model and read nowhere. Every real proposal pays output tokens for them. `retrieval.sibling_text` and the `translation_lookup` plumbing exist only to fill them. | `schema.py:291-292`, `prompts.py:103-104`, `retrieval.py:1394-1408` |
| medium | Stale schema comments about `data/decisions.jsonl`, `sync-decisions` and `data/queue/<item_id>.json`. **Fixed.** | `pipeline/db/params_schema.sql:26-27, 273, 335-336, 371, 449` |
| low/medium | View `params.proposal_review` has no reader; table `params.proposal_references` is written on every run and read only by that view. **Fixed**: view dropped; the table kept and documented as the per-run evidence history (the queue keeps only the latest run). | `params_schema.sql:379…`, `paramdb.py:1039-1060` |
| low | `impact.phoenix_url_from`; `encode_client.score_via_jobs` and `queue_store.load_item` (tests only; **removed**, the latter now a test helper); unused imports `CritiqueFindings`, `ItemStatus` (**removed**); `RetrievalHit.method` value `"fts"` never produced. | — |
| low | Deprecated `--as-of` alias on `run-targets` and `run-country`; legacy `parameter_file` validation alias. **Removed** (no queue row carries the old key). | `cli.py:49-68`, `schema.py:398-400` |

---

## 5. Evaluation — `Nomokrisis-evaluation_pipeline`

### Missing factorization

- **Fixed** (`golden_drafting.golden_case_id`/`entry_case_id`) — **The case-id rule exists four times and one copy disagrees** (medium): `build_dataset.py:143-148`, `openfisca_golden.py:506`, `curated_golden.py:207-212`, `openfisca_golden.py:644-652`. For an OpenFisca group entry without an explicit `id`, the stale draft would never be retired; the one such entry today sets `id`.
- **Fixed** (one public `golden_drafting` module; output byte-identical on the 115 live entries) — **The two golden builders duplicate their second half** (medium): record loading, the `corpus_available` override, label drafting, case construction and the "ground truth changed" warning. `curated_golden.py:51-58` imports five private helpers from `openfisca_golden`.
- **Fixed** — **`embedding_eval.py` repeats the candidate join three times** and has drifted from production (see 2.1). One `_CANDIDATE_CTE` following `search_chunks`' live-version rule; vector leg through `search_chunks`.
- **Fixed** — **Low**: `_git_commit` twice; `GROUP_PREFIX` twice; the `--verbose` and `-j` option blocks three times; the 35-column `upsert_result` written out three times while `details` already stores the full result (`db.py:117-215`).

### Size

| Function | Where | Lines |
|---|---|---|
| `draft_case` (OpenFisca) | `openfisca_golden.py:348-529` | 182 |
| `draft_case` (curated) | `curated_golden.py:106-250` | 145 |
| `score_item` | `scoring.py:285-413` | 129 |
| `execute_run` | `runner.py:204-321` | 118 |
| `run_embedding_eval` | `embedding_eval.py:183-281` | 99 |

**Fixed**: `cli.py` is a thin entry point over `commands/{golden,runs,embeddings}.py`; `parameter_store.py` holds `db_constants`, `route_against_current`, `load_case_record`; summarisation moved to `summary.py`. Original: `cli.py` (1 182 lines, 22 commands) splits into golden, runs and embeddings command modules. `openfisca_golden.py` mixes corpus readers, `db_constants` and `route_against_current` (used by three other modules), the drafter and stale-case retirement. `runner.py` holds both execution and summarisation.

### Design

- **Fixed** (`0.2.0+scoring.<sha256[:8] of scoring.py>` recorded per run) — **`EVAL_VERSION` is still `"0.1.0"`** (medium) while `scoring.py` has changed on eight dates, including the tolerance change. `eval.runs.eval_version` cannot tell which scoring rules produced a row. Bump it, or store a hash of `scoring.py`.
- **Fixed** (`parameter_store.country_targets`, `runner.golden_set_drift`) — **Business logic in command functions** (low): country target enumeration SQL in `cli.py:206-211`, the golden-hash drift check in `cli.py:660-666`.
- The `-j` loop in `execute_run` is sound in itself: everything touching the connection stays on the main thread. The hazards are in what the threads call (D4, D5).

### Dead code

- **Fixed by decision**: kept as documented seed fixtures for a fresh database; `test_import_golden` skips without them; excluded from the worker image. — **The retired file-based golden set is still tracked** (medium): `dataset/` (106 files), `dataset_embedding/` (10), `golden_sources/` (6). `tests/test_import_golden.py:25-26, 46, 52` reads them without a skip guard, and the worker image copies them in. `import_golden.py` (245 lines), `golden_store.restore_verdict` and the `_legacy_parameter_file` validator exist only for that one-off import.
  - Caveat: after `docker compose down -v`, `import-golden` from these files is the only in-repo way to rebuild the golden set. Decide between "seed fixtures, documented as such" and deletion plus a dump/restore target.
- **Fixed** (deleted / a crashed run is now marked `failed` / columns dropped / `.gitignore` cleaned) — **Low**: `runner.run_evaluation` has no caller; `Expected.legal_status` is never set or scored; run status `'failed'` is never written; `eval.embedding_cases.reviewed_*` are never used; `.gitignore` still lists `.eval_runs/`.

---

## 6. Worker — `Nomergon-worker`

- **Fixed** — **One job type is spelled in seven places** (medium, see 2.1). `jobs.JOB_SPECS` is the one table; a test checks the SQL lists against it; `nomergon job-types --write` emits `Nomergon-worker/job_types.json` for the UI.
- **Fixed** — **`build_command`** (`jobs.py:246-372`, 127 lines, complexity 36) is one `match` arm per type of hand-built argv. Each payload model now owns `to_argv()`.
- **Fixed** — **`_run_subprocess`** (`runner.py:161-274`, 114 lines) mixes the pump loop, the cancel poll and outcome mapping. Split into `_start_child`, `_ChildOutput`, `_Capture`, `_Interrupt`, `_outcome`.
- **Fixed** — typed per sub-command; the UI's legacy `{command, args}` form is read through an allow-list (no `--database-url`, `--trigger`, extra positionals). A document/route source must be an http(s) URL or a file under `WORKER_DOCUMENT_DIR` (a pasted path could otherwise ingest `/proc/self/environ`). — **The `ingest` payload is an opaque argv** (medium): `args: list[str]` passed straight through (`jobs.py:77-80, 278`). It is the only job type the worker does not model, so the UI owns part of the ingest CLI contract and any flag is reachable from the reviewer role.
- **Low**:
  - **Fixed** — `finish_job` has no `AND status = 'running'` guard (`db.py:143-156`).
  - **Fixed** — `JobSlot.run` opens its first connection outside the `try` (`worker.py:159`).
  - **Fixed** — `impact` and `ingest route` return "the last JSON line among the last 20 stdout lines" instead of an `@result` line (`jobs.py:453-470`). Both print `@result` now.
  - **Fixed** — URL redaction is written twice (`runner.py:299-307`, `cli.py:30-35`). One `config.redact_url`.
- **Fixed (removed)** — **Dead**: `db.set_worker_device` (`db.py:225-226`), `EncodeLane.ready` (`encoder.py:74`), and the `scratch_dir is None` branches reached only by tests (`jobs.py:414-416, 426-428`).
- `worker.py`, `db.py` and `client.py` are well sized. The claim path, the heartbeat reconnect and the `@progress` / `@result` protocol are sound and tested.

---

## 7. MCP server — `mcp-server`

- **Fixed** — **`src/euromod_mcp/` is dead and cannot import** (medium). Deleted; `.env.example` trimmed. It is not in the wheel (`pyproject.toml:24`), not tested, and `encoder.py:9` imports `euromod_ingest`, a package that no longer exists. Its `search.py` is byte-identical to the live one. It is also the pre-ADR-0004 design, loading BGE-M3 in the server process. Delete the directory and trim `mcp-server/.env.example`, which still lists three variables the live package never reads.
- **Fixed** (calls `search_chunks()`) — **The search is a third implementation of hybrid retrieval** (medium), with unweighted RRF, different `ts_rank_cd` normalisation, no `live_version` and whole-tree jurisdiction scope. `ARCHITECTURE.md` says it "makes the RAG retriever reusable"; the code does not reuse it. See D2 and D9.
- **Fixed** — **The model id is hard-coded** (`server.py:21`) and the encode payload carries no `model_id`. Now the default model from the DB, sent in the payload.
- `nomotheca_mcp/encoder.py` is clean: injectable clock and connection, worker liveness check, clear errors.

---

## 8. Desktop apps — `Nomoscope-agentic-workflow/ui` and `rag-ui`

### Missing factorization

| Severity | Finding | Where |
|---|---|---|
| high | `rag-ui` copies the front-end it shares with `ui`, while the Rust is shared. `styles.css` lines 1–346 are a copy (four diff lines); `Icon.svelte`, `jobs.js` and `api.js` are forks; about 110 lines of shell CSS and the ribbon markup are duplicated. The `rag-ui` copy of `jobs.js` has no tests. | `rag-ui/src/styles.css`, `rag-ui/src/lib/`, both `App.svelte` |
| high | "Run a job and show its progress" is built three times, each with the same state, clock, progress bar, technical log and scoped CSS. | `IngestTab.svelte:100-118, 318-375, 628-665`; `ParamsTab.svelte:57-82, 251-333, 533-575`; `JobsTab.svelte:60-78, 209-259` |
| medium | `search_articles` and its payload structs are copied verbatim into `rag-ui`'s command layer, which is the drift `#[path]` was meant to prevent. **Fixed**: `db::search` + `db::SearchPayload`, called by both apps. | `rag-ui/src-tauri/src/lib.rs:121-163` against `ui/src-tauri/src/lib.rs:283-325` |
| medium | Worker status and the model picker are fetched and rendered in five places, with different defaults. | `App.svelte:137-149`, `ParamsTab.svelte:205-212`, `IngestTab.svelte:147-154`, `JobsTab.svelte:28`, `rag-ui/src/App.svelte:87-98` |
| medium | Row-to-JSON mapping: 207 `r.get::<_, T>("col")` calls in 27 `json!` blocks, every column named in SQL and again in the mapping. `connect()` is defined five times, identically. (`connect()` **fixed**: one `pg.rs`.) | `ui/src-tauri/src/db.rs`; `db.rs:8`, `jobs.rs:63`, `store.rs:31`, `golden.rs:27`, `conversations.rs:22` |
| medium | Component `<style>` blocks re-declare global rules: `.row`/`.grow`/`.spacer` in seven tabs, `.error` in five, cards in three. Errors are shown as `callout err` in four tabs and `p.error` in six. | `ui/src/lib/components/*.svelte` |
| medium/low | `dbStats` fetched by three tabs (it runs two 7-table `count(DISTINCT)` joins); duration formatting three times; number formatting four times; keyboard list navigation twice; `SOURCE_TYPES` twice; the `<<HL>>` parser twice. | `Home`, `DatabaseTab`, `IngestTab`, `QueueList`, `GoldenTab` |

Suggested fixes: a `shared/` directory (or a Vite alias) for `styles.css`, `Icon.svelte`, `jobs.js`, an api core and an `AppShell.svelte`; a `createJobRun()` rune module with `<JobProgress>` and `<JobLog>`; one polled worker state with a `<ModelPicker>`; one `format.js`.

### Size

- **`db.rs`** (1 066 lines). Its module doc says "read-only access to the legislation DB … and the eval schema"; it also holds the params queries and Phoenix. The damage shows: a doc comment cut in two by an inserted block (lines 695-696 and 740-741), and a `mod tests` in the middle of the file. Split into `corpus`, `search`, `eval`, `params` and `phoenix` modules. `rag-ui` could then include only `search` and `corpus`, and drop its blanket `#[allow(dead_code)]` and its `base64` dependency.
- **`DetailPanel.svelte`** (780 lines) mixes six concerns: run switcher, hand-off prompt, critique summary, proposal editor, accept gate (pure, testable) and decision bar.
- **`IngestTab.svelte`** (714 lines) is four unrelated forms sharing about 35 prefixed `$state` variables (`doc*`, `ing*`, `emb*`, `tr*`).
- **`ParamsTab.svelte`** (639 lines): filters, table, row detail, run bar. Its progress parser reads the CLI's console text (`[i/N]`, `routing=`) where `IngestTab` uses structured `@progress` events.
- **`App.svelte`** in both apps (581 and 601 lines): shell chrome, page state and 110–150 lines of shell CSS.
- **`DatabaseTab.svelte`** (529 lines): article search and library status are unrelated.

### Design

- **`db_url`, password included, round-trips through the webview on every call**, and every command opens a fresh connection (medium). `save_decision` opens two; `golden::load_cases` runs two extra queries per case. The URL is editable in `DatabaseTab` and `EvalTab`, so those tabs can point at a different database from the rest of the app. Both apps set `"csp": null`. Keep the URL and a pool in `tauri::State`.
- **`Row::get` is an unchecked unwrap** (medium): about 280 calls that panic on NULL into a non-`Option`. `conversations.rs:48` is fragile today, since a JSON `null` passes the `?` filter and `->>` yields SQL NULL.
- **Enums rendered raw instead of through `labels.js`** (medium). `trustLabel` and `verdictLabel` exist and are used nowhere; the pages roll their own.
  - Everyday pages: `DetailPanel.svelte:460, 574`; `IngestTab.svelte:518-524, 557`; `SourceViewer.svelte:92`; `ParamsTab.svelte:346-351, 367, 446, 450`; `ParameterEditor.svelte:146, 190`; `AuditLog.svelte:49`; `Home.svelte:71-87`.
  - `rag-ui` has no `labels.js` at all.
- **Runes** (low/medium). There is no legacy syntax and every interval is cleaned up. Weak spots:
  - props mirrored into state by `$effect` (`DatabaseTab:49-51`, `EvalTab:29-31`, `IngestTab:120-122`, `ChunkCard:26-28`);
  - `dbUrl` drilled into every component;
  - seven tabs driven through `bind:this` and an exported `reload()`;
  - `JobsTab.refresh` not guarded against overlap.
- **Swallowed errors** (low/medium): `cancelJob` handlers with no try/catch; `.catch(() => {})` at `IngestTab.svelte:136-137, 167` leaves the kind select on "waiting for the worker…" forever; `alert()` at `DetailPanel.svelte:282`.

### Dead code

- **Fixed (removed)** — **Tauri command `encode_query`** is registered and wrapped by `api.encodeQuery`, which nothing calls (`ui/src-tauri/src/lib.rs:420-423, 455`; `ui/src/lib/api.js:68`). All other 35 commands have a caller.
- **JS**: `verdictLabel`, `trustLabel` and their tables are unused. Use them rather than delete them.
- **CSS**: `tr.selectable`, `--button-cancel`, and in `rag-ui` the copied rules it never uses (`.segmented`, `.joblog`, `.bar`, `.field`, the routing and status badges).
- **Icons**: `moon` and `sun` in `ui`; 17 of the copied paths in `rag-ui`.
- **Dependencies**: `@tauri-apps/plugin-dialog` is never imported in JS, and the `dialog:default` capability is unneeded since the dialog is opened from Rust; `chrono`'s `serde` feature; `base64` in `rag-ui`.

---

## 9. Repository dead weight

| Severity | Item | Detail |
|---|---|---|
| high (weight) | `08 - EUROMOD Triangulator/` | 1 853 of 2 533 tracked files (73 %) and about 345 of 422 MB. 251 MB is scraped `legislation/<CC>/raw/*.html`. No code reads it. The live input is `country-reports/Y16/*.md`, referenced by skills and the source-analysis docs. |
| high (licence) | Three vendored Anthropic skills in the Triangulator | `docx`, `xlsx`, `pdf`: 127 files whose `LICENSE.txt` reads "© 2025 Anthropic, PBC. All rights reserved". That does not fit redistribution under the root EUPL-1.2 licence. Worth settling before delivery to JRC. |
| medium | `Nomoscope-agentic-workflow/data/` | 112 tracked files (`decisions.jsonl`, `queue/`, `parameters/`), read by no source file. |
| medium | Retired golden-set directories | 122 files, see section 5. |
| medium | `CLAUDE.md` contradicts itself | Line 18 says the pipeline "writes `ReviewItem` JSON to `data/queue/`" and line 117 mentions `manifest.json`; the code and the rest of the file say rows. The numbered docs it links at the root live in `docs/`. |
| low | Root and scratch files | A tracked chat transcript (`2026-11-03-161253-…txt`); two empty `package-lock.json` files with no `package.json`; `Nomotheca-RAG/country_reports/_extract_tmp.py` with absolute `/home/…` paths; `Nomotheca-RAG/database_exploration.sql`; a tracked `.claude/settings.local.json`. |
| low | Binaries and duplicates | A 13.9 MB `.mp4` under `docs/`; PDFs tracked beside their Markdown; two diverged copies of `01_activity1_parameter-format.md`. |
| low | Stale documentation | `Nomoscope-agentic-workflow/README.md:47, 254, 304`; `Nomokrisis-evaluation_pipeline/README.md:203-205`; `golden_set_{ES,IE,LT,NL}.md`; `.gitignore` entries for `data/queue/`, `.eval_runs/`. |

Suggested handling of the Triangulator: move `country-reports/Y16/` under `Nomotheca-RAG/country_reports/`, remove the three vendored skills, and move the rest to its own repository or an archive branch.

---

## 10. What was found sound

- **The verbatim rule.** Every path that accepts a quote ends in `retrieval.verify_extract` against the chunk finally named. Resolution and re-pointing never bypass it.
- **The derivation evaluator** is a strict AST whitelist with no `eval`.
- **Trust class and scope.** All evidence SQL in the workflow filters `source_trust_class <> 'context'` and takes a jurisdiction array. Country Reports are read only through `country_report_search`.
- **ADR 0004 in the apps.** No process spawn, no key read, no model load. The only file write is the export behind the folder picker. The only SQL writes are the sanctioned functions, the job insert, the cancel flag and the golden verdict columns.
- **SQL injection.** None found. The few formatted statements interpolate module constants; all values are bound.
- **The Azure deployment rule** holds: the environment variable is only a default for a bare prefix.
- **Scoring** matches the documented rules: 1e-9 tolerance, the law-versus-EUROMOD finding, period completion, any-of citations.
- **Well-factored modules**: ingest's `core/routing.py`, `core/ir.py`, `core/chunker.py`, the embedding and reranker registries, `es/regions.py`, `fr/kali.py`; the workflow's `config.py`, `queue_store.py`, `regions.py`; the UI's `store.rs` with its pure `compute_decision`.
- **No circular imports, no `sys.path` edits, no DDL in Python or Rust strings.**

---

## 11. Suggested order of work

1. **Fix the result-affecting defects**: D1 (ingest rollback), D2 (MCP trust class), D3 (readiness), D4 and D5 (encoder lock and latch), D6 (one lockfile).
2. **Delete what is plainly dead**: `mcp-server/src/euromod_mcp/`, the two probe files, `paramdb.record_decision`, the two unused proposal fields and their plumbing, `canary_facts`, the `encode_query` command, the root scratch files.
3. **Extract `quotes.py`** and use it from the pipeline and the chat. This removes two copies and makes the anti-hallucination rule testable in one place.
4. **Lift the pipeline steps out of `build_workflow`** and add direct tests of `critique` and `diff`. Split `derivation.py` and `temporal.py` out at the same time.
5. **Unify hybrid search** behind one SQL function used by the pipeline, the eval, the UI and the MCP server.
6. **Ingest**: `fetch_run()` context manager, `SnapshotClient.get_ok()`, a `BaseAdapter` with the default `expand()`, and the TUI calling the pipeline.
7. **Front-end**: shared directory for the two apps, the job-run module, then the component splits.
8. **Repository**: decide the fate of the Triangulator and the retired data directories; add a root `ruff.toml`, a `make test` and a minimal CI job.

## 13. Found while fixing (16 November 2026)

| # | Severity | Finding | Status |
|---|---|---|---|
| N1 | medium | `locate_named_units` picked acts by title similarity alone. Ley 18/1991 «del Impuesto sobre la Renta de las Personas Físicas», ingested since the test was written, scored 0.72 against a need naming «Ley 35/2006» (0.47), so LIRPF art. 66 was not located (`test_locate_live` red). | **Fixed** — an act number the need spells out (`retrieval.act_numbers`: «35/2006», «n° 2025-127») selects that act outright |
| N2 | medium | Repealed ES acts loaded through the BOE daily-gazette fallback carry `estatus_derogacion: N` and open-ended versions: Ley 18/1991 (140 versions) and Ley 40/1998 (133) are «in force» on every date, so retrieval can quote a repealed IRPF article as current law. | Open — needs the repeal date from BOE (the consolidated record's `fecha_derogacion`, or the repealing act) |

## 12. Not checked

- No test suite was run and test bodies were mostly skimmed. Claims about missing coverage rest on test names and imports.
- Defects marked *by reading* were not reproduced. No `EXPLAIN` was run for the HNSW findings.
- Not read in full: `openfisca.py`, `openfisca_match.py`, the function bodies of `params_schema.sql`, `handoff.js`, `highlight.js`, the worker and eval READMEs, `roles.sql`.
- The Triangulator's scripts and the provenance of its scraped HTML were not audited.
- Git history was not searched for large deleted blobs or secrets.
