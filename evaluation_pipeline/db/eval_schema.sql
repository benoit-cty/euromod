-- Activity 4 evaluation results, stored in the existing legislation DB (port 5434)
-- under a dedicated "eval" schema. Applied idempotently by `euromod-eval init-db`.

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
    supportedness    boolean,
    hallucination    boolean NOT NULL DEFAULT false,
    retrieval_hit    boolean,
    confidence       real,
    latency_ms       integer,
    error            text,
    details          jsonb,                  -- full CaseResult for drill-down in the UI
    UNIQUE (run_pk, case_id)
);

CREATE INDEX IF NOT EXISTS eval_results_run_idx ON eval.results (run_pk);
CREATE INDEX IF NOT EXISTS eval_results_lang_idx ON eval.results (language, country);

-- KPI rates per (run, language): the read surface for the Tauri UI and the KPI report.
-- avg() ignores NULLs, so each rate is computed only over the cases that exercise it.
CREATE OR REPLACE VIEW eval.run_summary AS
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
    round(avg(res.latency_ms))                            AS avg_latency_ms
FROM eval.runs r
JOIN eval.results res ON res.run_pk = r.id
GROUP BY r.id, res.language, res.country;
