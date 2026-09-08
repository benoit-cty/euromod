# Agentic Workflow + Validation UI (Activity 3) — working prototype

Implements the architecture of [03_activity3_agentic-workflow.md](../03_activity3_agentic-workflow.md):
a **structured pipeline with LLM steps, not a free-roaming agent**, plus a
desktop validation UI. Human validation is the product, not a fallback.

```
Nomoscope-agentic-workflow/
├── pipeline/        Python (uv): frame → retrieve → propose → critique → diff → enqueue
├── ui/              Tauri 2 (Rust) + Svelte 5 validation UI
├── data/
│   ├── parameters/  Activity 1 records materialized FROM the params DB — derived,
│   │                never hand-authored: db/ (run-targets), eval/ (golden set)
│   ├── queue/       review items written by the pipeline, read/written by the UI
│   │                one file per (parameter, system year): <country>_<target>_<year>.json
│   ├── queue_superseded/  older runs collapsed by `migrate-queue-ids` (kept, never read)
│   ├── decisions.jsonl  redundant local copy of the audit log; the log itself
│   │                    is params.review_decisions in Postgres
│   └── export/      accepted records, Activity 1 format (export-first write-back)
├── observability.md decision document: why Arize Phoenix
└── .env.example     all configuration knobs
```

## Quick start

```bash
docker compose up -d                     # repo root: legislation DB + pgAdmin + Phoenix

cd Nomoscope-agentic-workflow/pipeline
uv sync
uv run nomoscope-workflow run-targets group:FR:tinkt_fr:tin_schedule 'euromod://FR/tin_fr/def_const/$tinrt_cdhr' --year 2025
                                                        # mock model — no API key needed; one run = one system year
uv run nomoscope-workflow run-all --params-dir data/parameters/db --year 2025   # re-run everything materialized so far
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
The two demo targets exercise distinct routing outcomes against the seed
corpus: the barème IR schedule (assembled from the export's own parameter group)
routes `changed` for `--year 2024` and `provisional` for `--year 2025` when the
corpus holds only the LF-2025 consolidation (= 2024-income values); CDHR routes
`not_found` while its article is absent from the corpus.

Parameters always come from the parameter store — `data/parameters/` holds only
records materialized from it, so ingest first (`ingest-params` + `curate-params`,
see below) and reach for `run-targets` rather than adding a file by hand.

Real LLM: add `--force --model anthropic/claude-sonnet-5` to either command
(or `azure_openai/…`, `openai/…`, `openrouter/…`, `together/…` — see `.env.example`).

## 1. Workflow, step by step

One run = one `(country, parameter, system year)` — mirroring EUROMOD’s
one-software-version-per-year model (`--year 2025`; `--as-of` is a deprecated
alias, only its year matters). Before running, the CLI prints a **corpus
readiness banner**: which finance-act vintages (for Y and for Y+1) are in the
corpus and how many of their chunks are embedded, so “N income-year parameters
will be provisional” is said once, up front. Steps are plain functions driven
by an explicit control flow
([pipeline/src/nomoscope_workflow/pipeline.py](pipeline/src/nomoscope_workflow/pipeline.py)):

| Step | Kind | Input → output | Failure mode & handling |
|---|---|---|---|
| **derived check** | code | current value / raw EUROMOD string scanned for `$parameter` references (`$PSS * 4`) | referenced → routing `derived`, no retrieval/LLM spent: legislation never states formula values, only their anchor parameter |
| **frame** | code | Activity 1 record → search query + known citations | no labels → falls back to model_target |
| **retrieve** | SQL | citation fast path (pg_trgm, similarity > 0.55) then hybrid FTS ∥ vector merged by RRF k=60 (vector top-3 guaranteed into the result: ts_rank_cd has no IDF, so common fiscal terms would otherwise crowd out the semantically-best chunk), all pre-filtered by `validity @> as_of`, jurisdiction, lang, and reduced to **one version per article** (`DISTINCT ON (instrument, citation)` keeping the latest `lower(validity)`: the same article can exist twice — a new consolidation per amendment, and a different structural path when fetched standalone — leaving two open-ended `in_force` versions where the superseded text can outrank its replacement). FTS ORs the query terms; vector = BGE-M3 via the ingest package's query encoder (`WORKFLOW_EMBEDDING_MODEL_ID=1`), FTS-only fallback when unavailable | no hits → skip straight to diff, routing `not_found` |
| **propose** | **LLM** | record + retrieved chunks → `ProposalDraft` (structured output: value, valid_from, legal_status, chunk_id, verbatim extract, quote + translation, confidence) | model can return `found=false`; never guesses |
| **critique** | code + **LLM** | mechanical checks: extract is a verbatim quote of the cited chunk (offsets computed against `unit_texts.content`), dates consistent, units/brackets sane, schema-valid — then an LLM pass for semantic issues | verdict `fail` → one LLM retry, then goes to the human with the failed critique attached |
| **scout** (gap-fill) | **LLM** + web + ingest | when the corpus is missing the establishing text (`WORKFLOW_SCOUT=llm\|tavily`, see *Gap-fill* below): the LLM names the official act, **steered by what the proposal said it lacked** (`ProposalDraft.missing_sources`) and told which citations we already hold; Tavily searches official domains only and instrument ids are harvested from result URLs (per-country rules in `scout.COUNTRY_SOURCES` — FR: legifrance.gouv.fr / `JORFTEXT…`, LT: e-seimas.lrs.lt / `TAR.…`), LLM-ranked against the result titles, then **archive-first ingested** via `nomotheca_ingest` (+ incremental BGE-M3 embedding), then retrieval and the proposal run again. Repeats up to `WORKFLOW_SCOUT_MAX_ROUNDS` times | web text is never evidence — only discovery; quotes still verify against the DB. Every round's needs, queries and ingested ids are recorded on the review item. A country absent from `COUNTRY_SOURCES` cannot gap-fill at all |
| **diff** | code | proposal vs current value → routing `unchanged \| changed \| new \| not_found \| provisional \| national_team_source \| derived`. On `unchanged` the proposal keeps the validity window already in force: the citation re-confirms the value, it does not restart it, so no new `valid_from` is proposed. `provisional` (income-year params whose enacting act is missing) keeps the found value visible but no `proposed_record` — nothing acceptable to export | national-team-sourced values are never overwritten by the pipeline |
| **enqueue** | code | full `ReviewItem` (side-by-side values, critique, retrieval trace incl. source texts, merged candidate record with `lineage`) → `data/queue/<country>_<target>_<system year>.json` | re-runs of the same system year overwrite that item; an already-reviewed one is never clobbered (unless `--force`) |

The anti-hallucination rule from the activity doc is mechanical, not prompt-only:
`supporting_extract` must be found character-for-character (whitespace-insensitive)
inside the cited chunk, or `citation_verified=false` and the critique fails.

### Income-year parameters (`temporal_basis: income_year`)

EUROMOD's system year **is** the income year, but for the FR income-tax family
(barème, top rate, CDHR…) the enacting finance act is published months *after*
the income year it governs: the barème for 2025 income sits in the act
consolidated around February 2026. Retrieving the version in force *at* `as_of`
would therefore silently return the **previous** year's schedule. Parameters
tagged `"temporal_basis": "income_year"` get three behaviours.

The flag is **curated — the EUROMOD export does not carry it** (0 of 702
parameters in `FR.enriched.json`), and that export is read-only: never edit it.
The versioned source of truth is [`pipeline/curation/FR.curation.yaml`](pipeline/curation/FR.curation.yaml),
applied onto `params.parameters.temporal_basis` after ingest:

```bash
uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/FR.enriched.json
uv run nomoscope-workflow curate-params curation/FR.curation.yaml   # idempotent
```

The ingest upsert never touches the column, so the flag also survives a
re-ingest of a new export; the overlay is what makes it survive
`docker compose down -v`, and it records *why* each parameter is tagged. The
three behaviours:

The income year is **not** the system year: France assesses in year Y the
income of year Y−1 («impôt 2025 sur les revenus 2024»), so system year 2025
means income year 2024. That mapping is decided once, in
`schema.income_year_for` (`INCOME_YEAR_OFFSET = -1`), and every behaviour below
derives from it rather than re-deriving `as_of.year ± 1`. The
three behaviours:

- **retrieve/scout** use a shifted date — versions in force on 1 July of the
  year *following* the income year (mid-2025 for income year 2024, when
  LF 2025 is consolidated) — so the retroactive act is the one selected;
- **propose** back-dates `valid_from` to 1 January of the income year (the
  OpenFisca convention); publication after the income year is expected, not an
  inconsistency;
- **critique** replaces the in-force date check with two mechanical ones:
  `valid_from` must fall inside the income year, and the cited version must have
  entered into force on/after 1 December of the income year (the budget-act
  window — LF 2025 slipped to Feb 2025 and still passes), **unless the cited
  text itself names the income year**: an applicability clause ("à compter de
  l'imposition des revenus de l'année 2025") proves its own vintage however
  early it was enacted — the CDHR was instituted by LF 2025 (Feb 2025) *for*
  2025 income, and consolidated code articles drop such clauses, so the
  propose prompt steers citations toward the year-naming finance-act article.
  A version older than the window with no year named means *likely the
  previous year's value / act not yet in the corpus*:
  the item routes to **`provisional`** (a normal state of the world, distinct
  from `not_found`), the scout gap-fill gets a chance to ingest the missing
  act, no LLM retry is spent (it is a corpus state, not a proposal defect),
  and the UI blocks Accept with an explanation.

The one-year offset of EUROMOD *datasets* (FR_2024_b1 holds 2023 incomes) is an
input-data/uprating concern and deliberately plays no role in parameter dating.

### Gap-fill: ingesting more law when the corpus falls short

The corpus is never complete, and pre-ingesting everything is not an option —
so the agent fetches what it turns out to need, mid-run. This is the scout, and
it is a loop, not a single shot:

```
retrieve → propose → critique
     ↑                   │  still missing the establishing text?
     │                   ↓
     └──── ingest ← scout (LLM + official-domain web search)
```

**What starts a round** (`pipeline._needs_gap_fill`) — three situations, all
meaning *fetch more law and try again*:

- no proposal at all, or the analyst returned `found=false`;
- the item routed `provisional` (the act for this income year has not reached
  the corpus, so only last year's value was found);
- a proposal exists but the critique failed **for a source-availability
  reason** — the cited chunk was not among the hits, or nothing ties the cited
  article to the income year.

A proposal that survives the critique never starts a round, and neither does
one the critique rejected on its own merits: fetching more law cannot fix a
unit error, and spending an ingest on it would be waste.

**What the scout hunts.** Not the parameter label — *what the analyst just said
it was missing*. `ProposalDraft.missing_sources` is a structured list of the
documents needed, named in the law's own words ("l'arrêté fixant le plafond
annuel de la sécurité sociale pour 2025", "article L. 241-3 du code de la
sécurité sociale"); the prose `reasoning` is the fallback, and the critique's
own issues are the last resort. The scout is also given the citations already
in the database, so it does not spend its ingest budget re-fetching them. The
model routinely knows exactly which act it lacks — this is what makes that
knowledge actionable rather than prose in a trace.

**Why more than one round.** Values hide behind chains of cross-reference: the
code article names an implementing order, which names another. Each round is
driven by what the *previous* round's proposal still lacked, so the chain
resolves one hop at a time instead of stopping after the first. The loop ends
as soon as a proposal survives the critique, when a round ingests nothing new
(another round would ask the same question), or at the round cap.

**Budget.** `WORKFLOW_SCOUT_MAX_ROUNDS` (default 2) rounds, each ingesting at
most `WORKFLOW_SCOUT_MAX_INGEST` (default 2) instruments. Ids already tried in
this run — ingested or failed — are never retried in a later round. Each round
costs an ingest plus an incremental embedding pass, which is why the defaults
are low; raise them for a backfill, not for an interactive run.

**What does not change.** Web search and the LLM only ever *discover* which
official document to fetch. The text itself always enters through Nomotheca's
archive-first ingest (fetch → snapshot → parse → chunk), and the proposal's
`supporting_extract` is still verified character-for-character against the
database. Nothing the scout reads on the web can become evidence, and
`missing_sources` names documents, never values.

### Parameters no legislation states (`source_type: national_team`)

Not every EUROMOD parameter is legislation-derivable. Lithuanian childcare fees
(`xcc_lt`) are the clean case: the fee for a municipal pre-school place and the
discounts on it are set by each municipal council, so no national act exists to
cite, and the EUROMOD values are the national team's assumption over those
schedules. Left unflagged, such a parameter costs a full retrieve → propose →
critique → scout round *per year* and lands as `not_found` every time — a
corpus gap that can never be filled, reported as if it could.

The export leaves `source_type` empty, so this too is curated, in the same
overlay and applied by the same idempotent command
([`pipeline/curation/LT.curation.yaml`](pipeline/curation/LT.curation.yaml)):

```yaml
source_type:
  - type: national_team
    note: why this quantity has no legal source
    targets: [euromod://LT/xcc_lt/def_const/$xcc_amt1, …]
```

It applies to **every** value of the target — what makes a quantity
national-team-sourced is a property of the quantity, not of one version of it.
The run then short-circuits before retrieval (like formula parameters) and
routes `national_team_source`: the value stays visible in the queue and is never
overwritten. Re-run `curate-params` after every `ingest-params`, which replaces
the country's `model_values` rows.

### Units the export gets wrong (`unit: "/1"`)

The FR export delivers every parameter named `*rate*` — 146 of them, all
holding fractions — with unit `currency`, while using `"/1"` for 215 other
rate-like parameters. The unit is a hint on every LLM call: the proposal prompt
normalises "11 %" to 0.11 only for `"/1"`, and the critique's `values_sane`
range-checks only a `"/1"`. Under `currency` one model refused the barème's 0 %
band as "a currency amount" and another had every rate it proposed rejected as
implausible. The export is read-only and `ingest-params` rewrites `unit`, so the
correction is a third overlay rule, in the same file and applied by the same
command ([`pipeline/curation/FR.curation.yaml`](pipeline/curation/FR.curation.yaml)):

```yaml
unit:
  - unit: "/1"
    note: why the export's unit is wrong, and how membership was decided
    targets: [euromod://FR/tinkt_fr/def_const/$tin_rate3, …]
```

The unit must be one the export itself uses (`/1`, `currency`,
`currency/{day,week,month,year}`); anything else is rejected as a typo.
Materialized parameter files carry the unit, so rebuild them after curating
(`run-targets` for `data/parameters/db/`, `nomokrisis-eval build-*-dataset`
for the golden set). The defect itself is reported to the economists team — the
overlay is a bridge until a corrected export lands, not a replacement for one.

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
  `nomoscope-workflow run-targets <model_target>… --year …` (each target is
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
  Every decision is recorded in `params.review_decisions` — append-only, linked
  to its proposal row — and mirrored into the record's `lineage`. **The database
  write gates the decision:** it commits first, and only then are the queue item
  and the `data/decisions.jsonl` copy written. If Postgres is unreachable the
  decision fails with an explanatory error and the item stays pending, rather
  than looking accepted in a log that never received it. `nomoscope-workflow
  sync-decisions` replays the local copy (idempotently) if the two ever drift.
- **Contributed documents** (Ingest tab) — a reviewer pastes a URL or picks a
  file (PDF, HTML, Markdown, text) and states the jurisdiction, the language
  (constrained to the languages the store indexes), the title, the document's
  kind and the date it is in force from; the run streams and cancels like an
  instrument run, and on success chains an embeddings build so the document is
  retrievable by the time they are back at the queue. On entering an input the
  tab calls the ingester's `route` mode and reacts to what comes back:
  *contributed* prefills the title and date from the document itself;
  *adapter* announces "recognised as &lt;source&gt;, switching to the
  legislation ingester", hides the contributed fields and ingests the act by
  national id (Légifrance ELI URLs are resolved to their `JORFTEXT` id first);
  *refused* shows the hint — a whole Légifrance code is not one document. Run
  stays disabled until the required fields are set, and a missing validity date
  is refused rather than invented. The **kind** is stated in the country's own
  words (loi, décret, arrêté, circulaire, doctrine, other for FR) and the
  **source-trust class follows from it mechanically** — nobody states a trust
  level, and `other` is never evidence (ADR 0001). Optionally the reviewer
  searches the instruments already ingested and picks the one this document
  implements; "none" is a valid answer, and the statute can be ingested from
  the same tab. Fields, routing outcomes and the class table:
  [Nomotheca-RAG/ingest/README.md](../Nomotheca-RAG/ingest/README.md).
- **Guidance on proposals** — when every citation on a proposal comes from a
  `guidance` instrument (a circular, a doctrine page) the critique records an
  informational "supported by guidance only" finding, the detail panel shows a
  **guidance only** badge on the item and the class on each citation, and
  **Accept stays available**: for a circular-governed scheme the circular *is*
  the operative text. The finding never changes the verdict or the routing, and
  guidance ranks equal to legislation in retrieval — the evaluation counts
  guidance-only cases per language and model so that choice can be revisited on
  data (ADR 0001).
- **Audit log** — `params.review_decisions` rendered as a table, falling back to
  the local mirror (flagged in the header) when the DB is unreachable.
- **Golden set** — the human gate on drafted *evaluation* ground truth
  (`Nomokrisis-evaluation_pipeline/dataset/`, drafted from the OpenFisca corpus
  by `nomokrisis-eval build-openfisca-dataset` with `verified: false`). Each
  case shows the parameter under test, the value EUROMOD holds next to the value
  OpenFisca states, the expected routing/date/citations, and Legifrance
  deep-links. Accept sets `verified: true`; Reject stamps `reviewed_by` and
  leaves it false, so "a human said no" stays distinct from "nobody has looked".
  Only those three fields are written back, straight into the case file — this
  tab touches the eval dataset, never the review queue.
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
