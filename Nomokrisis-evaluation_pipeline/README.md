# evaluation_pipeline — Activity 4 (validation dataset + KPIs)

Evaluates the agentic workflow (`Nomoscope-agentic-workflow/pipeline`) against a **golden set** of
parameters with known correct values, and stores KPI results in the existing Postgres
(`legislation` DB, port 5434) under a dedicated `eval` schema — keyed by
`prompt_version`, `agent_version`, `model_provider`, `model_name` and **language**, so
per-language model comparisons (Activity 5) fall out of a SQL view.

Design goal: *simple*. Scoring is pure deterministic code (no LLM judge), storage is
two tables + one view, and the workflow under test is reused as-is (same retrieval,
prompts, critique and Phoenix tracing).

```
dataset/<country>/*.json     golden cases (git-versioned; the frozen test set)
dataset_embedding/<cc>/*.json  embedding/retrieval cases (query → relevant citations)
golden_sources/openfisca_<cc>.json  curated EUROMOD ↔ OpenFisca pairs the drafter starts from
src/nomokrisis_eval/
  schema.py                  GoldenCase / Expected / CaseResult / RunManifest (+ EmbeddingCase)
  dataset.py                 load/save cases + content-hash dataset_version
  build_dataset.py           Claude Fable drafts cases from a trusted document
  openfisca_golden.py        drafts cases from the ingested OpenFisca corpus (no LLM)
  scoring.py                 KPI scoring (pure functions)
  runner.py                  drives nomoscope_workflow.run_parameter over the set
  embedding_eval.py          ranks golden chunks under fts / vector / hybrid search
  db.py                      Postgres persistence (eval.runs / eval.results)
  cli.py                     nomokrisis-eval init-db | build-dataset | build-openfisca-dataset
                             | list-cases | verify | run | report
                             | list-embedding-cases | run-embeddings
db/eval_schema.sql           tables + eval.run_summary view (the UI read surface)
.eval_runs/<run_id>/         scratch queue + manifest.json + results.json per run (gitignored)
```

## Quick start

```bash
cd evaluation_pipeline
uv run nomokrisis-eval init-db                                  # create eval schema (DB must be up)
uv run nomokrisis-eval list-cases                               # inspect the golden set
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor    # offline smoke run
uv run nomokrisis-eval run --as-of 2025-06-01 --model anthropic/claude-sonnet-5
uv run nomokrisis-eval run --as-of 2025-06-01 --model openai/gpt-5 --language fr
uv run nomokrisis-eval report                                   # KPI summary per (run, language)
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
uv run nomokrisis-eval build-dataset docs/fr_country_report_2025.md --country FR --as-of 2025-06-01
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

### Building it from OpenFisca-France

`build-openfisca-dataset` drafts cases from the **OpenFisca corpus already
ingested into `params.external_*`** (`nomoscope-workflow ingest-openfisca`;
2,836 FR parameters, 19,391 value points, 16,788 references at a pinned git
commit). OpenFisca is a human-curated parameter database with per-date values
*and* per-date `LEGIARTI`/`JORFTEXT` references — exactly the
`(value, effective date, citation)` triple a golden case needs, at scale and
with no LLM in the loop.

```bash
# 0. the parameter store must hold the parameters under test (once per DB reset)
cd ../Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/FR.enriched.json
uv run nomoscope-workflow ingest-params ../../extracted_parameters/curated/FR.in_function.json
uv run nomoscope-workflow curate-params curation/FR.curation.yaml

# 1. suggest EUROMOD <-> OpenFisca links (workflow package, writes params.parameter_links)
uv run nomoscope-workflow match-openfisca --seed ../../Nomokrisis-evaluation_pipeline/golden_sources/openfisca_fr.json

# 2. draft the golden set from those links
cd -
uv run nomokrisis-eval build-openfisca-dataset --year 2025            # 50 drafts, verified=false
uv run nomokrisis-eval build-openfisca-dataset --year 2025 --curated-only
```

- **Linking** is value-fingerprint matching plus a curated seed file
  ([golden_sources/openfisca_fr.json](golden_sources/openfisca_fr.json)):
  both sides hold multi-year numeric histories, so a link is proposed when the
  same value appears in the same year on both sides at least three times. The
  seed file pins the families that no fingerprint can find on its own — the
  ones the JRC asked for by name (barème IR, CDHR, CEHR, SMIC, PSS) and
  EUROMOD's derived constants (`$tsc_group2_lim` is 3× the monthly PSS, carried
  as `factor`).
- **The parameter under test always comes from the parameter store**, never
  from a hand-authored file: `model_target` for a single parameter, `group_id`
  for a bracket schedule assembled from `params.parameter_groups` (the FR barème
  is 4 thresholds + 5 rates in the export; its `groups` block is the only place
  it exists as an object — `paramdb.load_group_record`). Parameters EUROMOD
  defines *inside functions* rather than as named constants, which the connector
  cannot export at all (CDHR), reach the store through
  [extracted_parameters/curated/FR.in_function.json](../extracted_parameters/curated/FR.in_function.json)
  via the ordinary `ingest-params` + `curate-params` path. Records are
  materialized under `data/parameters/eval/` because the workflow entry point
  takes a path — a derived artifact regenerated on every build, like
  `run-targets`' `data/parameters/db/`.
- **Ground truth** is re-derived from the parameter's own `temporal_basis`,
  never from the link: `income_year` parameters expect the OpenFisca value keyed
  `<year>-01-01` (income year, which is also the pipeline's back-dated
  `valid_from`), `in_force` ones the value in force at `as_of`. OpenFisca stores
  change points only, so "the value at D" always means the latest entry at or
  before D.
- **Routing** is computed by comparing that value against what EUROMOD holds at
  `as_of` — the model never decides it. A parameter whose EUROMOD value is a
  formula or FYA weighted average is *skipped with a reason* rather than guessed
  (see §2 of the limitations below).
- **Citations** are resolved against the legislation DB: an OpenFisca reference
  id that maps to a `legal_units.citation` becomes the expected citation; an
  instrument-level id that is not ingested yet is kept anyway (the case then
  scores an honest retrieval miss); an article-level id of an act we do not hold
  is recorded as provenance only, because no string the pipeline could produce
  would match it.
- Every case is `verified: false` with its provenance in `notes` (OpenFisca
  path, component, scale, the reference titles, what did not resolve).
  **OpenFisca is curated, not the law** — it is occasionally wrong or lagging,
  which is why nothing counts until a human accepts it.

### Reviewing drafts (validation UI → *Golden set* tab)

The UI reads the dataset directory straight off disk and writes the verdict
back into the case file:

```bash
cd ../Nomoscope-agentic-workflow/ui && npm run tauri dev    # WSL: prefix LIBGL_ALWAYS_SOFTWARE=1
```

Each case shows the parameter under test, **the value EUROMOD holds next to the
value OpenFisca states**, the expected routing/date/citations, Legifrance
deep-links for every cited act, and the draft's provenance. *Accept* sets
`verified: true`; *Reject* leaves it false but stamps `reviewed_by`, so
"a human said no" stays distinct from "nobody has looked yet". Both write only
those three fields, so the rest of the case survives untouched — commit the
file to freeze it into the set.

Same thing without the GUI:

```bash
uv run nomokrisis-eval verify fr_constdef_pss_2025-06-01 --reviewer ben
uv run nomokrisis-eval verify fr_tinkt_tin_rate1_2025-06-01 --unverify
```

## Embedding (retrieval) evaluation dataset

`retrieval_recall_pct` above measures retrieval only through a full workflow run.
`dataset_embedding/` isolates the Activity 2 retrieval layer: one JSON per case
with a search **query** and the exact `legal_units.citation` string(s) of the
chunk(s) a correct retriever must surface. No LLM, no parameter files — each
case is ranked under three methods over the same as-of/country/lang candidate
pool the production pipeline uses (Country Reports excluded):

- `fts` — FTS-only leg (is BM25-ish text search enough?)
- `vector` — pure cosine ranking over `embeddings` (**the embedding eval proper**:
  this is the number that moves when the embedding model or backend changes)
- `hybrid` — the production RRF fusion (what the workflow actually retrieves with)

```bash
uv run nomokrisis-eval list-embedding-cases
uv run nomokrisis-eval run-embeddings                           # BGE-M3 (model_id 1); spawns the ingest query encoder
uv run nomokrisis-eval run-embeddings --embedding-model-id 99   # in-SQL placeholder embedder, no encoder needed
uv run nomokrisis-eval run-embeddings --country FR --k 20
```

Metrics per (query language, method): `hit@1`, `hit@k`, `MRR`. Per-case output
also shows the candidate-pool size and how much of it is embedded — "ingested
but not embedded" is the most common cause of a vector miss (same failure mode
as `/debug-phoenix-trace`). Results go to `.eval_runs/embeval-*/` as JSON; no
`eval`-schema tables yet (add them if/when embedding-model comparisons need to
be queryable next to the workflow KPIs).

Case-design rules:

- `expected_citations` are matched with **strict normalised equality** (not the
  golden set's containment match) so `art. 2` never claims `art. 20` — write
  them exactly as stored in `legal_units.citation`.
- `language` is the query language, `corpus_lang` the searched texts (defaults
  to `language`); set both for **cross-lingual** cases (en query over the fr
  corpus) — BGE-M3's multilingual space is exactly what those test.
- Paraphrase, don't quote: a query copied verbatim from the chunk hands the win
  to FTS and measures nothing about embeddings.
- Same human gate as the golden set (`verified: false` drafts → review → flip),
  but `run-embeddings` includes drafts by default: this eval is diagnostic
  tooling, not the contractual KPI freeze.

The seed set (10 cases) has real discriminative power only for FR (~1,200-chunk
pool, incl. one cross-lingual and one amending-act needle); the BE/ES/IE/NL/LT
cases are single-chunk smoke tests until those corpora are ingested for real.

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
  `nomokrisis-evaluation` project. When a KPI drops, open the trace for that case.
- **Postgres = scores** (the KPI record): versioned, queryable, joins with the rest of
  the stack, and directly readable by the Tauri app. This is what the KPI report and
  Activity 5 comparisons are built from.

Phoenix also has its own datasets/experiments feature; we deliberately don't use it for
scoring to keep the pipeline simple and the results in one place. Revisit only if we
later want LLM-judge evals.

## Displaying results in the Tauri app

`eval.run_summary` is designed as the UI read surface. The app already has read-only
Postgres access (`Nomoscope-agentic-workflow/ui/src-tauri/src/db.rs`); an "Evaluation" tab needs:

1. a Rust command à la `db_stats` running
   `SELECT * FROM eval.run_summary ORDER BY created_at DESC` (and
   `SELECT details FROM eval.results WHERE run_pk = $1` for drill-down),
2. an entry in `src/lib/api.js`,
3. a Svelte component listing runs (model, language, KPI columns) with per-case detail.

## Configuration (env vars, `.env` at repo root or here)

| Var | Default | |
|---|---|---|
| `EVAL_DATABASE_URL` | falls back to `WORKFLOW_DATABASE_URL`, then `postgresql://jrc:jrc@localhost:5434/legislation` | where eval results go |
| `EVAL_DATASET_DIR` | `Nomokrisis-evaluation_pipeline/dataset` | golden set location |
| `EVAL_EMBEDDING_DATASET_DIR` | `Nomokrisis-evaluation_pipeline/dataset_embedding` | embedding/retrieval case location |
| `EVAL_RUNS_DIR` | `Nomokrisis-evaluation_pipeline/.eval_runs` | scratch + manifests |
| `EVAL_BUILDER_MODEL` | `claude-fable-5` | dataset drafting model |
| `EVAL_PHOENIX_PROJECT` | `nomokrisis-evaluation` | Phoenix project for eval traces |

## Tests

```bash
uv run --extra test pytest
```

## Limitations: what we can (and cannot) do with EUROMOD parameters

Findings from the FR deep-dive (`Nomotheca-RAG/country_reports/FR_parameter_matching.md`, matching
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
