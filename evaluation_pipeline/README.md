# evaluation_pipeline — Activity 4 (validation dataset + KPIs)

Evaluates the agentic workflow (`agentic-workflow/pipeline`) against a **golden set** of
parameters with known correct values, and stores KPI results in the existing Postgres
(`legislation` DB, port 5434) under a dedicated `eval` schema — keyed by
`prompt_version`, `agent_version`, `model_provider`, `model_name` and **language**, so
per-language model comparisons (Activity 5) fall out of a SQL view.

Design goal: *simple*. Scoring is pure deterministic code (no LLM judge), storage is
two tables + one view, and the workflow under test is reused as-is (same retrieval,
prompts, critique and Phoenix tracing).

```
dataset/<country>/*.json     golden cases (git-versioned; the frozen test set)
src/euromod_eval/
  schema.py                  GoldenCase / Expected / CaseResult / RunManifest
  dataset.py                 load/save cases + content-hash dataset_version
  build_dataset.py           Claude Fable drafts cases from a trusted document
  scoring.py                 KPI scoring (pure functions)
  runner.py                  drives euromod_workflow.run_parameter over the set
  db.py                      Postgres persistence (eval.runs / eval.results)
  cli.py                     euromod-eval init-db | build-dataset | list-cases | run | report
db/eval_schema.sql           tables + eval.run_summary view (the UI read surface)
.eval_runs/<run_id>/         scratch queue + manifest.json + results.json per run (gitignored)
```

## Quick start

```bash
cd evaluation_pipeline
uv run euromod-eval init-db                                  # create eval schema (DB must be up)
uv run euromod-eval list-cases                               # inspect the golden set
uv run euromod-eval run --as-of 2025-06-01 --model mock/extractor    # offline smoke run
uv run euromod-eval run --as-of 2025-06-01 --model anthropic/claude-sonnet-5
uv run euromod-eval run --as-of 2025-06-01 --model openai/gpt-5 --language fr
uv run euromod-eval report                                   # KPI summary per (run, language)
```

Every run writes a reproducibility manifest (`.eval_runs/<run_id>/manifest.json`) with
pinned model, prompt/agent versions, dataset content-hash and git commit — the "run
manifest" required by `04_activity4_validation.md`.

## Golden dataset

One JSON file per case: the Activity 1 parameter file to run, the `as_of` date, and an
`expected` block (routing, value, valid_from, acceptable citations). Composition follows
the Activity 4 plan: stratify by type (scalar / bracket), difficulty (`plain` / `combine`
/ `table`), and source class; include **no-change cases** (`routing: unchanged`) and
`not_found` / `national_team_source` routing traps.

### Building it with Claude Fable

`build-dataset` drafts cases from a *trusted* source document (EUROMOD country report
excerpt, national-team notes, or a pasted consolidated article):

```bash
uv run euromod-eval build-dataset docs/fr_country_report_2025.md --country FR --as-of 2025-06-01
```

- One Fable call per parameter file; the model extracts value / valid_from / citations
  **only from the document** (structured output, JSON-schema enforced).
- Expected *routing* is computed deterministically by diffing against the parameter
  file's recorded value — the model never decides routing.
- Drafts are saved with `"verified": false`. A human flips `verified` to `true` after
  checking; `run` evaluates verified cases only (default) — that's the freeze.
- Model: `claude-fable-5` (override with `--model` / `EVAL_BUILDER_MODEL`). Server-side
  refusal fallback to `claude-opus-4-8` is enabled, so a classifier false-positive
  degrades gracefully instead of failing the batch. Needs `ANTHROPIC_API_KEY` (loaded
  from the repo-root `.env`).

## KPIs (per case, aggregated per language in `eval.run_summary`)

| KPI | Meaning |
|---|---|
| `routing_pct` | changed / unchanged / new / not_found / national_team_source classified correctly |
| `value_pct` | exact scalar match (1e-9 tolerance) or bracket structure+cell match |
| `date_pct` | proposed `valid_from` equals the expected effective date |
| `citation_pct` | pinpoint citation (instrument + article) matches an accepted one |
| `supportedness_pct` | cited text verbatim-contains the supporting extract (workflow's mechanical check) |
| `hallucination_pct` | value proposed whose citation does **not** support it (lower is better) |
| `retrieval_recall_pct` | ground-truth citation present in the retrieval trace (recall@k — the most diagnostic number) |
| `avg_latency_ms` | wall-clock per parameter |

KPIs a case doesn't exercise are stored as `NULL` and excluded from the rate (e.g. no
`value_pct` contribution from a `not_found` case).

## Does Phoenix help?

Yes — and it's already running (`docker compose up -d`, http://localhost:6006). The
division of labour is:

- **Phoenix = traces** (debugging): the eval runner reuses the workflow's OTel tracing,
  so every eval case produces a full retrieve→propose→critique trace under the
  `euromod-evaluation` project. When a KPI drops, open the trace for that case.
- **Postgres = scores** (the KPI record): versioned, queryable, joins with the rest of
  the stack, and directly readable by the Tauri app. This is what the KPI report and
  Activity 5 comparisons are built from.

Phoenix also has its own datasets/experiments feature; we deliberately don't use it for
scoring to keep the pipeline simple and the results in one place. Revisit only if we
later want LLM-judge evals.

## Displaying results in the Tauri app

`eval.run_summary` is designed as the UI read surface. The app already has read-only
Postgres access (`agentic-workflow/ui/src-tauri/src/db.rs`); an "Evaluation" tab needs:

1. a Rust command à la `db_stats` running
   `SELECT * FROM eval.run_summary ORDER BY created_at DESC` (and
   `SELECT details FROM eval.results WHERE run_pk = $1` for drill-down),
2. an entry in `src/lib/api.js`,
3. a Svelte component listing runs (model, language, KPI columns) with per-case detail.

## Configuration (env vars, `.env` at repo root or here)

| Var | Default | |
|---|---|---|
| `EVAL_DATABASE_URL` | falls back to `WORKFLOW_DATABASE_URL`, then `postgresql://jrc:jrc@localhost:5434/legislation` | where eval results go |
| `EVAL_DATASET_DIR` | `evaluation_pipeline/dataset` | golden set location |
| `EVAL_RUNS_DIR` | `evaluation_pipeline/.eval_runs` | scratch + manifests |
| `EVAL_BUILDER_MODEL` | `claude-fable-5` | dataset drafting model |
| `EVAL_PHOENIX_PROJECT` | `euromod-evaluation` | Phoenix project for eval traces |

## Tests

```bash
uv run --extra test pytest
```

## Limitations: what we can (and cannot) do with EUROMOD parameters

Findings from the FR deep-dive (`RAG/country_reports/FR_parameter_matching.md`, matching
`extracted_parameters/FR.policy.json` — 702 parameters — against the Y16 country report).
They bound what this pipeline can honestly evaluate.

### 1. The extraction only sees named constants

Every `model_target` is a `def_const` constant. Parameters defined *inside* EUROMOD
functions never appear — for FR that includes the **IRPP bracket schedule, the quotient
familial ceilings, BMAF and the 2025 CDHR minimum tax**: the most politically salient,
yearly-updated numbers in the system. Until the connector exports in-function parameters,
golden cases can only cover what `def_const` exposes; the headline tax schedule is
untestable through the JSON.

### 2. Stored values are not legal values

- **Mid-year changes are stored as weighted averages** (FYA), e.g. SMIC 2024 =
  `(1766.92*10+1801.80*2)/12#m`. The averaged number appears in **no legal text**; a RAG
  that retrieves both décrets correctly still won't string-match the stored value.
- **~75 % of FR parameters (530/702) hold formula strings**, some referencing other
  constants (`$PSS * 4`) — a dependency graph, not a flat list.
- Values carry **period suffixes** (`#m #y #q #w #d #l #s #c`) with fixed conversion
  factors (yearly ÷12, weekly ×4.34, daily ×30.5, labour day ×21.73…).

⇒ `value_pct` scoring must compare **normalised annualised values** (evaluate formulas,
resolve constant refs, apply period conversion) — never raw strings. A correct legal
answer can differ from the stored value for representation reasons alone.

### 3. Not every "policy" parameter is derivable from legislation

The classifier marked all 702 as `policy`, but the set mixes provenance classes:

| Class | FR examples | Can a legislation RAG answer it? |
|---|---|---|
| Statutory value | SMIC, RSA base, tax thresholds | yes — the core use case |
| Admin statistic | `$mc_yse_amt` (avg Covid self-employed compensation, "from official statistics") | no — needs admin publications |
| Behavioural calibration | `$bsa00_BTA_rate` (RSA 20 % non-take-up) | no — national-team judgment |
| Uprating index | Annex 1 factors (HICP, AMECO, INSEE series) | no — statistical sources |

⇒ the golden set needs a **source-class field**, and `not_found` /
`national_team_source` routing traps; scoring a RAG on non-legislative parameters
measures nothing.

### 4. Metadata quality is too poor to key on

`unit` is wrong for rates (stored as `currency`), labels are often maintenance notes
("FYA: annual increase takes place in July 2022…") or empty, `description` is empty,
classification is a single un-reviewed Haiku pass. Key everything on `model_target`;
treat labels as hints only.

### 5. Provenance slots are empty — that is the job, and the baseline is zero

`references`, `official_journal_date`, `legal_status` are empty on **all** value rows;
`review_status` is `pending` everywhere. There is no existing citation ground truth to
compare against — accepted citations for golden cases must be curated by hand (or from
the country report), which is exactly what `build-dataset` + human verification does.

### 6. Temporal coverage is uneven

Only ~183/702 FR parameters have a 2025 value; 231 series are closed (abolished
instruments like PPE, hard-dated excises); PAJE keeps three parallel cohort-split
parameter sets ending in different years. ⇒ include **unchanged** and **dead-parameter
abstention** cases, and don't read "no 2025 row" as "needs update" — it may be dormant
by design.

### 7. The country report is strong but not infallible ground truth

The Y16 FR report contradicts itself at least once (Table 2.3 SMIC/PSS uprating
percentages vs. narrative). CR-sourced golden values should be cross-checked against a
second source before `verified: true` — and per-instrument "EUROMOD modelling" caveats
(non-take-up adjustments, n-2 income assumptions, receipt-restricted simulation) explain
why a legally-correct value can still be "wrong" for the model.

### Consequences already reflected in this pipeline's design

- deterministic value scoring with tolerance + normalisation (no string match);
- routing classes include `not_found` and `national_team_source`;
- human verification gate before a case enters the frozen set;
- per-case NULL KPIs so abstention cases don't pollute `value_pct`.

Still open: formula/FYA-aware value normalisation in `scoring.py` (evaluate
`(a*n+b*m)/12`-style expressions and `$const` references before comparing), and a
source-class stratum in the dataset builder.
