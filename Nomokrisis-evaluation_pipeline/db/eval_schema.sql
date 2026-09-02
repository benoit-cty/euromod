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
    difficulty       text,
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
    corpus_available boolean,               -- false: the source act is not ingested yet
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
    ADD COLUMN IF NOT EXISTS impact_estimated  boolean;

ALTER TABLE eval.runs
    ADD COLUMN IF NOT EXISTS critique_model    text;

CREATE INDEX IF NOT EXISTS eval_results_run_idx ON eval.results (run_pk);
CREATE INDEX IF NOT EXISTS eval_results_lang_idx ON eval.results (language, country);

-- KPI rates per (run, language): the read surface for the Tauri UI and the KPI report.
-- avg() ignores NULLs, so each rate is computed only over the cases that exercise it.
--
-- Dropped and recreated rather than CREATE OR REPLACE'd: replace refuses to
-- rename or reorder existing columns, which forced every new KPI to be appended
-- at the end regardless of where it belongs. Nothing depends on this view but
-- read queries (the UI and `nomokrisis-eval report`, both by column name), so
-- rebuilding it costs nothing and keeps the column list readable.
DROP VIEW IF EXISTS eval.run_summary;
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
    -- Model quality, separated from corpus coverage: the same rates over the
    -- cases whose ground-truth source is actually ingested. A case with
    -- corpus_available = false cannot be answered by ANY model, so folding it
    -- into the headline reports ingest breadth as if it were LLM accuracy.
    count(*) FILTER (WHERE res.corpus_available IS FALSE) AS cases_no_corpus,
    count(*) FILTER (WHERE res.abstained)                 AS abstentions,
    round(100 * avg(res.routing_correct::int)
          FILTER (WHERE res.corpus_available IS NOT FALSE), 1) AS routing_pct_in_corpus,
    round(100 * avg(res.value_correct::int)
          FILTER (WHERE res.corpus_available IS NOT FALSE), 1) AS value_pct_in_corpus,
    round(avg(res.latency_ms))                            AS avg_latency_ms,
    -- Environmental impact (EcoLogits over Phoenix token counts): sums ignore
    -- NULLs and are NULL for pure-mock runs. New columns are appended at the
    -- end so CREATE OR REPLACE VIEW stays valid against the existing view.
    sum(res.tokens_prompt)                                AS tokens_prompt,
    sum(res.tokens_completion)                            AS tokens_completion,
    sum(res.energy_kwh)                                   AS energy_kwh,
    sum(res.gwp_kgco2eq)                                  AS gwp_kgco2eq
FROM eval.runs r
JOIN eval.results res ON res.run_pk = r.id
GROUP BY r.id, res.language, res.country;
