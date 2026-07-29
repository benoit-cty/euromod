# Agentic Workflow + Validation UI (Activity 3) — working prototype

Implements the architecture of [03_activity3_agentic-workflow.md](../03_activity3_agentic-workflow.md):
a **structured pipeline with LLM steps, not a free-roaming agent**, plus a
desktop validation UI. Human validation is the product, not a fallback.

```
Nomoscope-agentic-workflow/
├── pipeline/        Python (uv): frame → retrieve → propose → critique → diff → enqueue
├── ui/              Tauri 2 (Rust) + Svelte 5 validation UI
├── data/
│   ├── parameters/  input records (Activity 1 JSON, git-versioned) — 3 FR demo params
│   ├── queue/       review items written by the pipeline, read/written by the UI
│   ├── decisions.jsonl  append-only audit log (future training/validation data)
│   └── export/      accepted records, Activity 1 format (export-first write-back)
├── observability.md decision document: why Arize Phoenix
└── .env.example     all configuration knobs
```

## Quick start

```bash
docker compose up -d                     # repo root: legislation DB + pgAdmin + Phoenix

cd Nomoscope-agentic-workflow/pipeline
uv sync
uv run nomoscope-workflow run-all --as-of 2025-06-01    # mock model — no API key needed
uv run nomoscope-workflow queue

cd ../ui
# OR
cd Nomoscope-agentic-workflow/ui
npm install
npm run tauri dev
# WSL:
LIBGL_ALWAYS_SOFTWARE=1 npm run tauri dev
```

Traces: http://localhost:6006 → project `nomoscope-agentic-workflow`.
The three demo parameters exercise the three routing outcomes against the seed
corpus: barème IR → `changed` (2025 thresholds), top marginal rate →
`unchanged`, CDHR → `not_found` (article absent from corpus).

Real LLM: `uv run nomoscope-workflow run-all --as-of 2025-06-01 --force --model anthropic/claude-sonnet-5`
(or `azure_openai/…`, `openai/…`, `openrouter/…`, `together/…` — see `.env.example`).

## 1. Workflow, step by step

One run = one `(country, parameter, as_of)`. Steps are plain functions driven
by an explicit control flow
([pipeline/src/nomoscope_workflow/pipeline.py](pipeline/src/nomoscope_workflow/pipeline.py)):

| Step | Kind | Input → output | Failure mode & handling |
|---|---|---|---|
| **derived check** | code | current value / raw EUROMOD string scanned for `$parameter` references (`$PSS * 4`) | referenced → routing `derived`, no retrieval/LLM spent: legislation never states formula values, only their anchor parameter |
| **frame** | code | Activity 1 record → search query + known citations | no labels → falls back to model_target |
| **retrieve** | SQL | citation fast path (pg_trgm, similarity > 0.55) then hybrid FTS ∥ vector merged by RRF k=60 (vector top-3 guaranteed into the result: ts_rank_cd has no IDF, so common fiscal terms would otherwise crowd out the semantically-best chunk), all pre-filtered by `validity @> as_of`, jurisdiction, lang. FTS ORs the query terms; vector = BGE-M3 via the ingest package's query encoder (`WORKFLOW_EMBEDDING_MODEL_ID=1`), FTS-only fallback when unavailable | no hits → skip straight to diff, routing `not_found` |
| **propose** | **LLM** | record + retrieved chunks → `ProposalDraft` (structured output: value, valid_from, legal_status, chunk_id, verbatim extract, quote + translation, confidence) | model can return `found=false`; never guesses |
| **critique** | code + **LLM** | mechanical checks: extract is a verbatim quote of the cited chunk (offsets computed against `unit_texts.content`), dates consistent, units/brackets sane, schema-valid — then an LLM pass for semantic issues | verdict `fail` → one LLM retry, then goes to the human with the failed critique attached |
| **scout** | **LLM** + web + ingest | on `not_found` (`WORKFLOW_SCOUT=llm\|tavily`): the LLM names the official act that sets the value; Tavily searches official domains only (FR: legifrance.gouv.fr) and instrument ids (FR: `JORFTEXT…`) are harvested from result URLs, LLM-ranked against the result titles, then **archive-first ingested** via `nomotheca_ingest` (+ incremental BGE-M3 embedding) before one retrieval retry | web text is never evidence — only discovery; quotes still verify against the DB. Ingested ids and queries are recorded on the review item |
| **diff** | code | proposal vs current value → routing `unchanged \| changed \| new \| not_found \| national_team_source \| derived` | national-team-sourced values are never overwritten by the pipeline |
| **enqueue** | code | full `ReviewItem` (side-by-side values, critique, retrieval trace incl. source texts, merged candidate record with `lineage`) → `data/queue/*.json` | re-runs never clobber an already-reviewed item (unless `--force`) |

The anti-hallucination rule from the activity doc is mechanical, not prompt-only:
`supporting_extract` must be found character-for-character (whitespace-insensitive)
inside the cited chunk, or `citation_verified=false` and the critique fails.

## 2. Orchestrator: plain Python + PydanticAI (thin)

- The step sequence (retry loop, not-found short-circuit) is explicit Python
  control flow — no orchestration framework. LLM steps are **PydanticAI**
  agents with structured output straight into the Pydantic schemas. Every step
  is an ordinary function, so swapping the orchestration style is cheap if the
  comparison in the deliverable concludes otherwise.
- **Multi-provider by config string** (`WORKFLOW_MODEL=<provider>/<model>`):
  anthropic, openai, azure_openai, openrouter, together — plus `mock/` for
  key-less demos and deterministic tests. Endpoint flexibility is the hard
  requirement from Activity 5; nothing in the pipeline knows the provider.
- **ALOHA**: positioned as a possible orchestration host with this pipeline
  inside; its OpenAI-only endpoints are covered by the `azure_openai/`/`openai/`
  providers. **MCP** stays the tool-interface layer for the national-team DB
  integration (see the reference implementation in `leximpact_mcp_server`).

## 3. Data contracts

- **In**: Activity 1 parameter records ([../Param_Schema/](../Param_Schema/)),
  pydantic-validated ([schema.py](pipeline/src/nomoscope_workflow/schema.py)).
- **Retrieval**: the legislation DB ([../Nomotheca-RAG/db/schema.sql](../Nomotheca-RAG/db/schema.sql));
  citations carry `jrc_database_id` = `chunks.id`, offsets refer to
  `unit_texts.content`. Vector leg encodes queries with real BGE-M3
  (`WORKFLOW_EMBEDDING_MODEL_ID=1`, reusing the ingest package's OpenVINO
  query-encoder subprocess); the seed's placeholder embedder (model 99,
  embedded in SQL) remains for key-less demos.
- **Out**: the same Activity 1 JSON with the new dated value appended, the
  previous open-ended value closed, and `lineage` fully machine-filled
  (run_id, prompt_version, agent_version, model, confidence, retrieval_trace,
  review fields). Export-first: nothing writes into EUROMOD files.

## 4. Validation UI (ui/)

Tauri 2 + Svelte 5. Rust command layer follows the pattern proven in
`tauri_outdated_parameters_app` (single JSON `payload` → typed struct →
`Result<Value, String>`); the queue stays loosely typed in Rust so the item
schema can evolve pipeline-side without lockstep releases.

- **Review queue** — filterable by country / routing / status / text; shows
  critique verdict and confidence per row.
- **Parameters** — every parameter in the `params` schema (see
  `ingest-params`), filterable by country / policy / run state / text, with
  the current model value and the latest agentic run per row. Select
  parameters and **launch an agentic update from the UI**: it spawns
  `nomoscope-workflow run-targets <model_target>… --as-of …` (each target is
  materialized from the DB as an Activity 1 file under
  `data/parameters/db/`), streams the CLI output live, then refreshes.
  Each run row links to the **review-queue item** and deep-links to the
  run's **trace in Phoenix** (`/projects/<gid>/traces/<trace_id>`; the
  project gid is resolved from the `phoenix` DB in the shared Postgres).
- **Record detail** — side-by-side current vs proposed (bracket-level diff
  highlighting), critique checklist, verbatim quote, **citation viewer** with
  the supporting extract highlighted inside the retrieved legal text, full
  provenance (run, model, prompt version, confidence) and a deep link to the
  run's Phoenix trace.
- **Language switcher on the cited text** — each retrieved hit lists the
  language renderings the DB actually holds for that legal-unit version
  (authentic originals, official translations, BGE-M3-pipeline machine
  translations with their engine), resolved on demand from `unit_texts` and
  matched to the sibling chunk on `seq` (falling back to the full version text
  when a translation chunks differently). The verbatim highlight stays on the
  cited rendering only — a translated text is reading aid, not evidence.
- **Decisions** — the proposal is **always shown as an editable form** (validity
  dates, legal/source status, value, and each reference with its chunk id and
  supporting extract), so the reviewer sees field by field what they are signing
  off on. Accept / Reject / Escalate to national team, plus Revert edits;
  accepting a modified proposal is recorded as `edited`. Items stay editable
  **after** a decision — re-deciding overwrites the item and appends a new audit
  entry. The **Accept button enforces the acceptance-gated tier** (doc 08 §4) on
  the edited form: `valid_from` + `legal_status` + at least one reference with a
  `supporting_extract` (or national-team source), so filling a gap in the form
  unblocks Accept. Hand-editing an extract drops its verified `extract_offsets`.
  Every decision is appended to `decisions.jsonl` and mirrored into the record's
  `lineage`.
- **Audit log** — the decision log rendered as a table.
- **Database** — corpus statistics (totals, per-jurisdiction, embedding
  coverage) and point-in-time article search straight against the legislation
  DB. Search modes are language-aware FTS, multilingual BGE-M3 vectors, or
  RRF-fused hybrid retrieval, with country / language / as-of filters and a
  per-result score breakdown. Tauri owns a long-lived OpenVINO query-encoder
  subprocess, so the first vector search loads the model and later searches
  reuse it; full-text-only searches do not start the model.

Stack note for the kick-off discussion: the Rust side is ~500 lines over plain
files + Postgres; porting it to a small web service for a multi-user JRC
deployment does not affect the pipeline or the data contracts.

## 5. Observability — Arize Phoenix (replaces the LangSmith approach)

Decision rationale in [observability.md](observability.md). Implementation
([tracing.py](pipeline/src/nomoscope_workflow/tracing.py)):

- One **trace per run** with nested spans `frame → retrieve → propose →
  critique → diff → enqueue`; retrieval spans carry the candidate chunks and
  scores, the root span carries run_id / model / prompt_version — the KPI
  slicing axes for Activities 4–5.
- PydanticAI agent runs are instrumented natively (`Agent.instrument_all()`)
  and mapped to OpenInference spans by
  `openinference-instrumentation-pydantic-ai`; pipeline steps use plain OTel
  spans, so **mock runs trace identically to LLM runs** and no LangSmith-style
  vendor env vars exist anywhere (`grep -ri langsmith` returns nothing).
- Exit strategy: everything is OTLP; pointing `PHOENIX_COLLECTOR_ENDPOINT`
  elsewhere re-homes the traces without re-instrumentation. Phoenix down ≠
  pipeline down (tracing degrades to no-op with a console note).
- **Environmental impact** ([impact.py](pipeline/src/nomoscope_workflow/impact.py)):
  `uv run nomoscope-workflow impact` estimates energy/CO₂eq of all traced LLM
  calls with [EcoLogits](https://ecologits.ai) over the Phoenix span token
  counts — offline, retroactive, no hot-path instrumentation; the UI's
  **Impact tab** shows the same report (`impact --json` under the hood), and
  evaluation runs store per-case energy/CO₂eq next to the KPIs (Activity 5
  accuracy-vs-impact comparisons). Models missing from the EcoLogits registry
  are listed as not-estimated, never silently dropped. Knobs:
  `PHOENIX_DATABASE_URL`, `ECOLOGITS_ELECTRICITY_MIX_ZONE` (default `EEE`).

## 6. Security & guardrails

- Schema enforcement at every LLM boundary (structured output into pydantic).
- Verbatim-quote rule checked mechanically against the corpus.
- The gap-fill scout never uses web text as evidence: search results only
  nominate official instrument ids, the text enters through Nomotheca's
  archive-first ingest, and quotes verify against the database as always.
- No write-back without human acceptance; export-first even then.
- Reviewed queue items are immutable to re-runs; the decision log is
  append-only; national-team values route around the pipeline entirely.

## 7. Testing

```bash
cd Nomoscope-agentic-workflow/pipeline && uv run --with pytest pytest   # mock extraction, diff, queue
cd Nomoscope-agentic-workflow/ui/src-tauri && cargo test                # decision/export round-trip
```
