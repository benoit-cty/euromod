-- Activity 4 evaluation results, stored in the existing legislation DB (port 5434)
-- under a dedicated "eval" schema. Applied idempotently by `nomokrisis-eval init-db`.

CREATE SCHEMA IF NOT EXISTS eval;

-- One row per evaluation run: a pinned (model, prompt, agent, dataset) combination.
CREATE TABLE IF NOT EXISTS eval.runs (
    id              bigserial PRIMARY KEY,
    run_id          text UNIQUE NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    as_of           date NOT NULL,
    model_provider  text NOT NULL,          -- e.g. 'anthropic', 'openai', 'mock'
    model_name      text NOT NULL,          -- e.g. 'claude-sonnet-5'
    prompt_version  text NOT NULL,
    agent_version   text NOT NULL,
    eval_version    text NOT NULL,
    dataset_version text NOT NULL,          -- content hash of the golden set
    git_commit      text,
    countries       text[] NOT NULL DEFAULT '{}',
    notes           text
);

-- One row per golden case per run.
CREATE TABLE IF NOT EXISTS eval.results (
    id               bigserial PRIMARY KEY,
    run_pk           bigint NOT NULL REFERENCES eval.runs(id) ON DELETE CASCADE,
    case_id          text NOT NULL,
    country          text NOT NULL,
    language         text NOT NULL,          -- source-legislation language: per-language KPIs
    model_target     text,
    difficulty       text,                   -- ladder: verbatim | combine | derive | table
    hazards          text[] NOT NULL DEFAULT '{}',  -- income_year, cross_instrument, ...
    source_class     text,
    routing_expected text NOT NULL,
    routing_actual   text,
    routing_correct  boolean,
    value_correct    boolean,                -- NULL = KPI not exercised by this case
    date_correct     boolean,
    citation_correct boolean,
    extract_verbatim boolean,               -- mechanical verbatim-quote check alone
    supportedness    boolean,               -- verbatim check AND the critique model's judgement
    critique_pass    boolean,
    hallucination    boolean NOT NULL DEFAULT false,
    retrieval_hit    boolean,
    abstained        boolean NOT NULL DEFAULT false,  -- refused rather than guessed
    guidance_only    boolean NOT NULL DEFAULT false,  -- every citation was guidance, not legislation
    corpus_available boolean,               -- false: the source act is not ingested yet
    readiness        text,                   -- ready | no_corpus | undocumented
    confidence       real,
    latency_ms       integer,
    error            text,
    details          jsonb,                  -- full CaseResult for drill-down in the UI
    phoenix_trace_id  text,                  -- exact link to the case's Phoenix trace
    llm_calls         integer,               -- LLM spans in that trace (NULL for mock runs)
    tokens_prompt     integer,
    tokens_completion integer,
    energy_kwh        double precision,      -- EcoLogits midpoint estimates (see impact.py)
    gwp_kgco2eq       double precision,
    impact_estimated  boolean,               -- false: model absent from the EcoLogits registry
    UNIQUE (run_pk, case_id)
);

-- Environmental-impact columns were added after the first deploys; CREATE TABLE
-- IF NOT EXISTS does not alter existing tables, so migrate them explicitly.
ALTER TABLE eval.results
    ADD COLUMN IF NOT EXISTS phoenix_trace_id  text,
    ADD COLUMN IF NOT EXISTS llm_calls         integer,
    ADD COLUMN IF NOT EXISTS tokens_prompt     integer,
    ADD COLUMN IF NOT EXISTS tokens_completion integer,
    ADD COLUMN IF NOT EXISTS energy_kwh        double precision,
    ADD COLUMN IF NOT EXISTS gwp_kgco2eq       double precision,
    ADD COLUMN IF NOT EXISTS extract_verbatim  boolean,
    ADD COLUMN IF NOT EXISTS critique_pass     boolean,
    ADD COLUMN IF NOT EXISTS abstained         boolean NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS corpus_available  boolean,
    ADD COLUMN IF NOT EXISTS readiness         text,
    ADD COLUMN IF NOT EXISTS hazards           text[] NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS guidance_only     boolean NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS impact_estimated  boolean;

ALTER TABLE eval.runs
    ADD COLUMN IF NOT EXISTS critique_model    text,
    -- what the provider layer actually called (azure_openai/: the deployment)
    ADD COLUMN IF NOT EXISTS resolved_model    text,
    ADD COLUMN IF NOT EXISTS resolved_critique_model text;

CREATE INDEX IF NOT EXISTS eval_results_run_idx ON eval.results (run_pk);
CREATE INDEX IF NOT EXISTS eval_results_lang_idx ON eval.results (language, country);

-- eval.results plus `readiness_eff`, the single definition of "can this case
-- measure a model at all" that every view below shares. Rows written before the
-- readiness column existed carry NULL: they still know corpus_available, so they
-- fall back to the coarser corpus split rather than claiming to be ready.
-- Mirrors runner.readiness_of — keep the two in step.
DROP VIEW IF EXISTS eval.run_hazards;
DROP VIEW IF EXISTS eval.run_difficulty;
DROP VIEW IF EXISTS eval.run_summary;
DROP VIEW IF EXISTS eval.scored_results;
CREATE VIEW eval.scored_results AS
SELECT
    res.*,
    coalesce(
        res.readiness,
        CASE WHEN res.corpus_available IS FALSE THEN 'no_corpus' ELSE 'ready' END
    ) AS readiness_eff,
    -- A proposal the pipeline's own critique rejected; routing/value/date are
    -- already scored False for it (scoring.score_item), this only counts them.
    -- Read from the JSON dump so the column needs no table migration.
    coalesce((res.details ->> 'rejected')::boolean, false) AS rejected
FROM eval.results res;

-- KPI rates per (run, language): the read surface for the Tauri UI and the KPI report.
-- avg() ignores NULLs, so each rate is computed only over the cases that exercise it.
--
-- Dropped and recreated rather than CREATE OR REPLACE'd: replace refuses to
-- rename or reorder existing columns, which forced every new KPI to be appended
-- at the end regardless of where it belongs. Nothing depends on this view but
-- read queries (the UI and `nomokrisis-eval report`, both by column name), so
-- rebuilding it costs nothing and keeps the column list readable.
CREATE VIEW eval.run_summary AS
SELECT
    r.id            AS run_pk,
    r.run_id,
    r.created_at,
    r.as_of,
    r.model_provider,
    r.model_name,
    r.prompt_version,
    r.agent_version,
    r.dataset_version,
    r.critique_model,
    r.resolved_model,
    r.resolved_critique_model,
    res.language,
    res.country,
    count(*)                                              AS cases,
    count(*) FILTER (WHERE res.error IS NOT NULL)         AS errors,
    round(100 * avg(res.routing_correct::int), 1)         AS routing_pct,
    round(100 * avg(res.value_correct::int), 1)           AS value_pct,
    round(100 * avg(res.date_correct::int), 1)            AS date_pct,
    round(100 * avg(res.citation_correct::int), 1)        AS citation_pct,
    round(100 * avg(res.supportedness::int), 1)           AS supportedness_pct,
    round(100 * avg(res.hallucination::int), 1)           AS hallucination_pct,
    round(100 * avg(res.retrieval_hit::int), 1)           AS retrieval_recall_pct,
    -- Evidence legs kept apart: extract_verbatim is the mechanical verbatim
    -- check alone (no LLM), supportedness folds in the critique model's
    -- judgement, critique_pass is its overall verdict. Only extract_verbatim is
    -- comparable across models when the run let the model grade itself.
    round(100 * avg(res.extract_verbatim::int), 1)        AS extract_verbatim_pct,
    round(100 * avg(res.critique_pass::int), 1)           AS critique_pass_pct,
    -- Model quality, separated from golden-set readiness: the same rates over
    -- the cases that can measure a model at all. A case whose source act is not
    -- ingested (no_corpus) cannot be answered by ANY model; a case with no
    -- ground-truth citation (undocumented) leaves retrieval unscorable and
    -- never established where the answer lives. Folding either into the
    -- headline reports dataset gaps as if they were LLM accuracy.
    count(*) FILTER (WHERE res.readiness_eff = 'no_corpus')    AS cases_no_corpus,
    count(*) FILTER (WHERE res.readiness_eff = 'undocumented') AS cases_undocumented,
    count(*) FILTER (WHERE res.abstained)                 AS abstentions,
    -- Guidance-only proposals, per language and model: not a quality KPI but
    -- the evidence base for revisiting the equal-ranking decision (ADR 0001).
    count(*) FILTER (WHERE res.guidance_only)             AS guidance_only_cases,
    round(100 * avg(res.guidance_only::int), 1)           AS guidance_only_pct,
    count(*) FILTER (WHERE res.rejected)                  AS rejections,
    round(100 * avg(res.routing_correct::int)
          FILTER (WHERE res.readiness_eff = 'ready'), 1)  AS routing_pct_ready,
    round(100 * avg(res.value_correct::int)
          FILTER (WHERE res.readiness_eff = 'ready'), 1)  AS value_pct_ready,
    round(100 * avg(res.citation_correct::int)
          FILTER (WHERE res.readiness_eff = 'ready'), 1)  AS citation_pct_ready,
    round(avg(res.latency_ms))                            AS avg_latency_ms,
    -- Environmental impact (EcoLogits over Phoenix token counts): sums ignore
    -- NULLs and are NULL for pure-mock runs.
    sum(res.tokens_prompt)                                AS tokens_prompt,
    sum(res.tokens_completion)                            AS tokens_completion,
    sum(res.energy_kwh)                                   AS energy_kwh,
    sum(res.gwp_kgco2eq)                                  AS gwp_kgco2eq
FROM eval.runs r
JOIN eval.scored_results res ON res.run_pk = r.id
GROUP BY r.id, res.language, res.country;

-- The two breakdowns that explain a headline, both restricted to ready cases:
-- an unready case fails for a reason that has nothing to do with its rung, so
-- letting it into a difficulty bucket would make every rung look equally bad.

-- KPI rates per (run, difficulty rung).
CREATE VIEW eval.run_difficulty AS
SELECT
    r.id            AS run_pk,
    r.run_id,
    r.model_provider,
    r.model_name,
    res.language,
    coalesce(res.difficulty, 'unlabelled')          AS difficulty,
    count(*)                                        AS cases,
    round(100 * avg(res.routing_correct::int), 1)   AS routing_pct,
    round(100 * avg(res.value_correct::int), 1)     AS value_pct,
    round(100 * avg(res.citation_correct::int), 1)  AS citation_pct,
    round(100 * avg(res.extract_verbatim::int), 1)  AS extract_verbatim_pct,
    round(100 * avg(res.retrieval_hit::int), 1)     AS retrieval_recall_pct
FROM eval.runs r
JOIN eval.scored_results res ON res.run_pk = r.id
WHERE res.readiness_eff = 'ready'
GROUP BY r.id, res.language, coalesce(res.difficulty, 'unlabelled');

-- KPI rates per (run, hazard flag). Hazards are multi-valued, so a case with
-- two flags is counted under both and the buckets do NOT sum to the case total.
CREATE VIEW eval.run_hazards AS
SELECT
    r.id            AS run_pk,
    r.run_id,
    r.model_provider,
    r.model_name,
    res.language,
    hazard,
    count(*)                                        AS cases,
    round(100 * avg(res.routing_correct::int), 1)   AS routing_pct,
    round(100 * avg(res.value_correct::int), 1)     AS value_pct,
    round(100 * avg(res.citation_correct::int), 1)  AS citation_pct,
    round(100 * avg(res.retrieval_hit::int), 1)     AS retrieval_recall_pct
FROM eval.runs r
JOIN eval.scored_results res ON res.run_pk = r.id
CROSS JOIN LATERAL unnest(res.hazards) AS hazard
WHERE res.readiness_eff = 'ready'
GROUP BY r.id, res.language, hazard;

-- ----------------------------------------------------------------------------
-- The golden set lives here, not in git (ADR 0004). A golden *selection* is
-- what used to be golden_sources/<cc>.json (curated, per country) or
-- golden_sources/openfisca_<cc>.json: the header and its entries, verbatim.
-- A golden *case* is one built case; the review verdict is in columns so the
-- reviewer role can be granted UPDATE on exactly those, and `case` holds the
-- rest of the GoldenCase (never the verdict — loading merges the two).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS eval.golden_selections (
    country    text NOT NULL,
    kind       text NOT NULL CHECK (kind IN ('openfisca', 'curated')),
    header     jsonb NOT NULL DEFAULT '{}'::jsonb,
    entries    jsonb NOT NULL DEFAULT '[]'::jsonb,
    updated_at timestamptz NOT NULL DEFAULT now(),
    updated_by text NOT NULL DEFAULT current_user,
    PRIMARY KEY (country, kind)
);

CREATE TABLE IF NOT EXISTS eval.golden_cases (
    id           text PRIMARY KEY,
    country      text NOT NULL,
    language     text NOT NULL,
    as_of        date NOT NULL,
    "case"       jsonb NOT NULL,          -- GoldenCase minus verified/reviewed_by/review_note
    verified     boolean NOT NULL DEFAULT false,
    reviewed_by  text,
    reviewed_at  timestamptz,
    review_note  text,
    drafted_at   timestamptz NOT NULL DEFAULT now(),
    updated_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS golden_cases_country_idx ON eval.golden_cases (country, verified);

-- Retrieval-only cases (dataset_embedding/), same treatment.
CREATE TABLE IF NOT EXISTS eval.embedding_cases (
    id          text PRIMARY KEY,
    country     text NOT NULL,
    language    text NOT NULL,
    "case"      jsonb NOT NULL,
    verified    boolean NOT NULL DEFAULT false,
    reviewed_by text,
    reviewed_at timestamptz,
    review_note text,
    updated_at  timestamptz NOT NULL DEFAULT now()
);

-- A run is resumable from the database alone: its frozen case list and every
-- result scored so far are rows, appended as they land. eval.runs.status
-- replaces the on-disk manifest/results.jsonl pair; `golden_set_hash` is the
-- content hash of exactly the cases in eval.run_cases (dataset_version keeps
-- its old name for the views).
ALTER TABLE eval.runs
    ADD COLUMN IF NOT EXISTS model        text,           -- full provider-prefixed string
    ADD COLUMN IF NOT EXISTS status       text NOT NULL DEFAULT 'complete'
        CHECK (status IN ('running', 'complete', 'failed')),
    ADD COLUMN IF NOT EXISTS submitted_by text,
    ADD COLUMN IF NOT EXISTS finished_at  timestamptz;

CREATE TABLE IF NOT EXISTS eval.run_cases (
    run_pk  bigint NOT NULL REFERENCES eval.runs(id) ON DELETE CASCADE,
    case_id text NOT NULL,
    "case"  jsonb NOT NULL,
    PRIMARY KEY (run_pk, case_id)
);

-- The ReviewItem the pipeline produced for the case, so `rescore` can re-apply
-- a scoring change without spending tokens (was <run dir>/queue/<item>.json).
ALTER TABLE eval.results ADD COLUMN IF NOT EXISTS review_item jsonb;

-- Retrieval-eval runs (was .eval_runs/<id>/manifest.json + results.json).
CREATE TABLE IF NOT EXISTS eval.embedding_runs (
    id         bigserial PRIMARY KEY,
    run_id     text UNIQUE NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    manifest   jsonb NOT NULL,
    results    jsonb NOT NULL
);
