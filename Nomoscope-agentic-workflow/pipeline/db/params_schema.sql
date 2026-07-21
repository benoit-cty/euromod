-- ============================================================================
-- EUROMOD parameter store — "params" schema in the legislation DB (port 5434)
-- ============================================================================
-- Implements Param_Schema/08_schema-proposal-for-validation.md §10:
--   parameters, model_values, parameter_usage, proposals, references,
--   extraction_runs, review_decisions.
-- ("references" is a reserved SQL keyword, so that table is named
--  proposal_references.)
--
-- Data ownership follows the doc's stages:
--   Stage A (received)      -> parameters, model_values, parameter_usage.
--     Ingested from extracted_parameters/enriched/<CC>.enriched.json and
--     treated as read-only source data: re-ingest replaces, nothing else
--     writes here.
--   Stage B (deterministic) -> normalized columns on those tables
--     (value_numeric, value_kind, model_release, system_year, parsed
--     model_address parts). Raw received fields are always preserved.
--   Stage C (agent)         -> extraction_runs, proposals, proposal_references.
--     One extraction_runs row per (country, parameter, as_of) pipeline run;
--     phoenix_trace_id links it to the full agent trace in Phoenix
--     (http://localhost:6006), which shares this Postgres instance.
--   Stage D (human)         -> review_decisions, append-only.
--
-- Applied idempotently by `nomoscope-workflow init-param-db`.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS params;

-- ----------------------------------------------------------------------------
-- parameters — one row per exported EUROMOD constant (received + normalized)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.parameters (
    id                      bigserial PRIMARY KEY,
    country                 text NOT NULL,             -- received information.country
    model_target            text NOT NULL UNIQUE,      -- canonical id: euromod://FR/tinkt_fr/def_const/$tin_upthres1
    parameter_key           text,                      -- received information.parameter_id (export >= 0.2.0): 'FR:tinkt_fr:def_const:$tin_upthres1'
    -- Stage B: structured model_address parsed from model_target (doc §4)
    policy                  text,                      -- 'tinkt_fr'
    function                text,                      -- 'def_const'
    name                    text,                      -- '$tin_upthres1'
    spine_order             text,
    value_type              text NOT NULL,             -- 'scalar' throughout the FR export
    unit                    text,                      -- received, authoritative (null for 5 FR params; never corrected)
    unit_structured         jsonb,                     -- Stage B convenience view {quantity,currency,period,euromod_suffix}
    label                   jsonb,                     -- language-keyed, as received
    short_label             jsonb,
    description             jsonb,
    explanation             jsonb,
    classification          jsonb,                     -- received enrichment {category,confidence,reason,classifier}
    coicop                  jsonb,                     -- {code,label,version,param_type}: 227 consumption-tax parameters
    last_confirmed_valid_on date,
    enrichment_lineage      jsonb,                     -- received enrichment provenance
    parameter_group         jsonb,                     -- optional display hint (doc §7); EUROMOD-team-validated only
    source_file             text NOT NULL,             -- provenance of the ingest
    ingested_at             timestamptz NOT NULL DEFAULT now()
);
-- Additive migration for databases created before export 0.2.0 support
-- (CREATE TABLE IF NOT EXISTS does not add columns to an existing table).
ALTER TABLE params.parameters ADD COLUMN IF NOT EXISTS parameter_key text;
CREATE INDEX IF NOT EXISTS parameters_country_idx ON params.parameters (country);
CREATE INDEX IF NOT EXISTS parameters_policy_idx  ON params.parameters (country, policy);
CREATE UNIQUE INDEX IF NOT EXISTS parameters_key_idx ON params.parameters (parameter_key)
    WHERE parameter_key IS NOT NULL;

-- ----------------------------------------------------------------------------
-- parameter_groups — received group definitions (export >= 0.2.0; doc §7).
-- Display/retrieval hints validated by the EUROMOD team; components reference
-- parameters by their received parameter_key.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.parameter_groups (
    id          bigserial PRIMARY KEY,
    group_id    text NOT NULL UNIQUE,      -- 'FR:tscse_fr:sched_schedule'
    country     text NOT NULL,
    kind        text,                      -- 'bracket_schedule', ...
    policy      text,
    instances   jsonb NOT NULL DEFAULT '[]',
    components  jsonb NOT NULL DEFAULT '[]',  -- [{parameter_id, role, band_index}, ...]
    source_file text NOT NULL,
    ingested_at timestamptz NOT NULL DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- model_values — received values[] history. NEVER overwritten by proposals
-- (doc §5): the agent writes to proposals, the reviewer decides.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.model_values (
    id                    bigserial PRIMARY KEY,
    parameter_id          bigint NOT NULL REFERENCES params.parameters(id) ON DELETE CASCADE,
    seq                   integer NOT NULL,            -- position in the received values[] array
    -- received value, verbatim (jsonb preserves number vs string): 11496 | "n/a" | "$PSS * 4"
    value_raw             jsonb NOT NULL,
    -- Stage B normalization (doc §6): null means "no normalized scalar", not zero
    value_numeric         double precision,
    value_kind            text NOT NULL CHECK (value_kind IN ('numeric','n_a','expression')),
    raw_euromod_value     text,                        -- lineage.model_answer: '11496#y', '1801.80#m'
    model_release         text,                        -- Stage B: 'J2.19' parsed from lineage.model
    system_year           integer,                     -- Stage B: only for single-year model intervals
    valid_from            date NOT NULL,               -- model applicability interval, NOT a legal date (doc §5)
    valid_to              date,
    legal_status          text,
    source_type           text,                        -- 'national_team' here routes around the pipeline
    official_journal_date date,
    received_references   jsonb NOT NULL DEFAULT '[]',
    lineage               jsonb NOT NULL DEFAULT '{}', -- received lineage, verbatim
    UNIQUE (parameter_id, seq)
);
CREATE INDEX IF NOT EXISTS model_values_param_idx ON params.model_values (parameter_id, valid_from);

-- ----------------------------------------------------------------------------
-- parameter_usage — received usage graph, stored separately (doc §9 option 2)
-- so agent/UI payloads stay compact. One row per edge.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.parameter_usage (
    id                bigserial PRIMARY KEY,
    parameter_id      bigint NOT NULL REFERENCES params.parameters(id) ON DELETE CASCADE,
    relation          text NOT NULL CHECK (relation IN ('defined_in','used_by')),
    policy            text NOT NULL,
    function          text NOT NULL,
    function_comment  text,
    group_name        text,                    -- defined_in rows
    used_in_parameter text,                    -- used_by rows: the consuming parameter's name
    systems           text[] NOT NULL DEFAULT '{}',
    source            text                     -- e.g. 'spine'
);
CREATE INDEX IF NOT EXISTS parameter_usage_param_idx ON params.parameter_usage (parameter_id);

-- ----------------------------------------------------------------------------
-- parameter_texts — derived language renderings of received label/description
-- fields (Stage B enrichment; see Param_Schema/openfisca_france_usage.md §5).
-- The received jsonb on params.parameters stays untouched; rows here carry
-- provenance. Retrieval prefers the law-language rendering when present so
-- the FTS leg of hybrid search stops being cross-language.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.parameter_texts (
    id           bigserial PRIMARY KEY,
    parameter_id bigint NOT NULL REFERENCES params.parameters(id) ON DELETE CASCADE,
    lang         text NOT NULL,               -- BCP-47 primary tag: 'fr','nl',...
    field        text NOT NULL CHECK (field IN ('label','short_label','description')),
    content      text NOT NULL,
    origin       text NOT NULL CHECK (origin IN ('machine_translation','openfisca','manual')),
    engine       text,                        -- provider-prefixed model for machine_translation
    created_at   timestamptz NOT NULL DEFAULT now(),
    UNIQUE (parameter_id, lang, field, origin)
);
CREATE INDEX IF NOT EXISTS parameter_texts_param_idx ON params.parameter_texts (parameter_id, lang);

-- ----------------------------------------------------------------------------
-- external_* — curated external parameter corpora (OpenFisca country packages
-- and compatible sources; see Param_Schema/openfisca_france_usage.md).
-- Stored under their own corpus-native identity: NO mapping to EUROMOD is
-- required at ingest time. parameter_links carries the sparse, human-validated
-- mapping and is initially empty.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.external_corpora (
    id          bigserial PRIMARY KEY,
    kind        text NOT NULL,                  -- 'openfisca'
    country     text NOT NULL,
    repo_url    text,
    commit_sha  text,                           -- pinned for reproducibility
    license     text,
    ingested_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (kind, country)
);

CREATE TABLE IF NOT EXISTS params.external_parameters (
    id          bigserial PRIMARY KEY,
    corpus_id   bigint NOT NULL REFERENCES params.external_corpora(id) ON DELETE CASCADE,
    path        text NOT NULL,                  -- dotted corpus path: 'impot_revenu.bareme_ir_depuis_1945.bareme'
    value_kind  text NOT NULL CHECK (value_kind IN ('scalar','bracket_schedule')),
    description text,
    short_label text,
    unit        text,
    metadata    jsonb NOT NULL DEFAULT '{}',    -- received metadata minus reference (stored relationally)
    UNIQUE (corpus_id, path)
);

-- One row per (component, date): scalars use component 'value'; scales store
-- each band part separately ('brackets[2].rate'), which is exactly the grain
-- EUROMOD scalar constants are matched against (value-fingerprint matching).
CREATE TABLE IF NOT EXISTS params.external_values (
    id                    bigserial PRIMARY KEY,
    external_parameter_id bigint NOT NULL REFERENCES params.external_parameters(id) ON DELETE CASCADE,
    component             text NOT NULL DEFAULT 'value',
    valid_from            date NOT NULL,
    value_numeric         double precision,     -- NULL = expired/no scalar
    value_raw             jsonb,
    UNIQUE (external_parameter_id, component, valid_from)
);
CREATE INDEX IF NOT EXISTS external_values_numeric_idx ON params.external_values (value_numeric)
    WHERE value_numeric IS NOT NULL;            -- fingerprint-matching probe

CREATE TABLE IF NOT EXISTS params.external_references (
    id                    bigserial PRIMARY KEY,
    external_parameter_id bigint NOT NULL REFERENCES params.external_parameters(id) ON DELETE CASCADE,
    valid_from            date,                 -- NULL for undated references
    title                 text,
    href                  text,
    national_id           text,                 -- LEGIARTI/JORFTEXT/... parsed from href
    official_journal_date text                  -- raw; occasionally lists several dates
);
CREATE INDEX IF NOT EXISTS external_references_natid_idx ON params.external_references (national_id)
    WHERE national_id IS NOT NULL;

-- Sparse EUROMOD <-> external mapping. Automated methods only ever suggest;
-- a row counts as validated once validated_by is set.
CREATE TABLE IF NOT EXISTS params.parameter_links (
    id                    bigserial PRIMARY KEY,
    parameter_id          bigint NOT NULL REFERENCES params.parameters(id) ON DELETE CASCADE,
    external_parameter_id bigint NOT NULL REFERENCES params.external_parameters(id) ON DELETE CASCADE,
    component             text NOT NULL DEFAULT 'value',  -- external component matched
    match_method          text NOT NULL CHECK (match_method IN
                            ('manual','fingerprint','structure','embedding_suggested','llm_suggested')),
    score                 real,
    validated_by          text,
    validated_at          timestamptz,
    created_at            timestamptz NOT NULL DEFAULT now(),
    UNIQUE (parameter_id, external_parameter_id, component)
);

-- ----------------------------------------------------------------------------
-- extraction_runs — one row per agentic pipeline run for one
-- (country, parameter, as_of). phoenix_trace_id is the OTel trace id
-- (32 hex chars) of the run's root span: the link from a proposal to the
-- full agent process (frame -> retrieve -> propose -> critique -> diff)
-- in Phoenix. NULL when tracing was disabled or Phoenix was down.
-- Soft link: `docker compose down -v` wipes Phoenix traces but not the
-- durable evidence (supporting extract + chunk id on proposal_references).
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.extraction_runs (
    id               bigserial PRIMARY KEY,
    run_id           text NOT NULL UNIQUE,       -- pipeline run id: '2026-07-15T10:02Z#fr-a1b2c3'
    parameter_id     bigint REFERENCES params.parameters(id),  -- NULL if the target isn't ingested
    country          text NOT NULL,
    model_target     text NOT NULL,
    as_of            date NOT NULL,
    model            text NOT NULL,              -- provider-prefixed: 'anthropic/...', 'mock/extractor'
    critique_model   text,
    prompt_version   text,
    agent_version    text,
    phoenix_project  text,
    phoenix_trace_id text,                       -- lower-case 32-hex OTel trace id
    routing          text,                       -- unchanged|changed|new|not_found|national_team_source|derived
    critique_verdict text,                       -- pass|fail
    item_id          text,                       -- review-queue file id (data/queue/<item_id>.json)
    retrieval_trace  jsonb,                      -- chunk ids/scores, content stripped
    started_at       timestamptz NOT NULL,
    finished_at      timestamptz
);
CREATE INDEX IF NOT EXISTS extraction_runs_target_idx ON params.extraction_runs (model_target, as_of);
CREATE INDEX IF NOT EXISTS extraction_runs_trace_idx  ON params.extraction_runs (phoenix_trace_id)
    WHERE phoenix_trace_id IS NOT NULL;

-- ----------------------------------------------------------------------------
-- proposals — agent-generated candidate values (Stage C). A proposal never
-- touches model_values; proposed_value NULL = the agent abstained.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.proposals (
    id                     bigserial PRIMARY KEY,
    proposal_id            text NOT NULL UNIQUE,   -- '<run_id>/<item_id>'
    run_pk                 bigint NOT NULL REFERENCES params.extraction_runs(id) ON DELETE CASCADE,
    parameter_id           bigint REFERENCES params.parameters(id),
    model_target           text NOT NULL,
    proposed_value         jsonb,                  -- scalar | bracket list | bool | string
    proposed_value_numeric double precision,       -- normalized scalar when applicable
    effective_from         date,                   -- LEGAL dates, only when the source establishes them (doc §5)
    effective_to           date,
    legal_status           text,                   -- doc §8 lifecycle vocabulary
    source_class           text NOT NULL,          -- legislation|administrative_guidance|official_statistics|national_team|other
    official_journal_date  date,
    confidence             real,
    reasoning              text,                   -- agent's own account; evidence lives in proposal_references
    created_at             timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS proposals_target_idx ON params.proposals (model_target);
CREATE INDEX IF NOT EXISTS proposals_param_idx  ON params.proposals (parameter_id)
    WHERE parameter_id IS NOT NULL;

-- ----------------------------------------------------------------------------
-- proposal_references — evidence attached to a proposal (doc §8: "references").
-- For legislation-sourced proposals the anti-hallucination rule is mechanical:
-- supporting_extract occurs character-for-character in the cited chunk
-- (public.chunks.id = jrc_chunk_id), offsets into unit_texts.content.
-- jrc_chunk_id is a soft reference; retention of cited chunks is enforced by
-- public.citation_registry, not by an FK here.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.proposal_references (
    id                 bigserial PRIMARY KEY,
    proposal_pk        bigint NOT NULL REFERENCES params.proposals(id) ON DELETE CASCADE,
    title              text NOT NULL,             -- canonical citation: 'CGI, art. 197'
    href               text,
    legal_unit_ref     text,
    jrc_chunk_id       uuid,                      -- public.chunks.id (a.k.a. jrc_database_id)
    supporting_extract text,
    extract_start      integer,                   -- offsets into unit_texts.content
    extract_end        integer,
    reviewer_note      text
);
CREATE INDEX IF NOT EXISTS proposal_references_proposal_idx ON params.proposal_references (proposal_pk);

-- ----------------------------------------------------------------------------
-- review_decisions — Stage D, append-only. Rows are only ever inserted;
-- an empty set for a proposal means "pending". Mirrors data/decisions.jsonl.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS params.review_decisions (
    id          bigserial PRIMARY KEY,
    proposal_pk bigint REFERENCES params.proposals(id),
    item_id     text,                             -- review-queue id, for decisions on abstain/not_found items
    action      text NOT NULL CHECK (action IN
                  ('accepted','rejected','edited','escalated','needs_revision')),
    reviewer    text,
    note        text,
    decided_at  timestamptz,
    logged_at   timestamptz NOT NULL DEFAULT now(),
    CHECK (proposal_pk IS NOT NULL OR item_id IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS review_decisions_proposal_idx ON params.review_decisions (proposal_pk)
    WHERE proposal_pk IS NOT NULL;

-- ----------------------------------------------------------------------------
-- proposal_review — the read surface for the validation UI: proposal next to
-- the current model value, with the Phoenix trace id for "view agent process".
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW params.proposal_review AS
SELECT
    pr.id                 AS proposal_pk,
    pr.proposal_id,
    pr.model_target,
    p.country,
    p.short_label ->> 'en'  AS short_label,
    p.unit,
    mv.value_raw          AS current_model_value,
    mv.raw_euromod_value  AS current_raw_euromod_value,
    mv.system_year        AS current_system_year,
    pr.proposed_value,
    pr.proposed_value_numeric,
    pr.effective_from,
    pr.effective_to,
    pr.legal_status,
    pr.source_class,
    pr.confidence,
    r.run_id,
    r.as_of,
    r.model,
    r.routing,
    r.critique_verdict,
    r.phoenix_project,
    r.phoenix_trace_id,
    (SELECT count(*) FROM params.review_decisions d WHERE d.proposal_pk = pr.id) AS decisions,
    pr.created_at
FROM params.proposals pr
JOIN params.extraction_runs r ON r.id = pr.run_pk
LEFT JOIN params.parameters p ON p.id = pr.parameter_id
LEFT JOIN LATERAL (
    SELECT * FROM params.model_values mv
    WHERE mv.parameter_id = p.id
      AND mv.valid_from <= r.as_of
      AND (mv.valid_to IS NULL OR mv.valid_to >= r.as_of)
    ORDER BY mv.valid_from DESC
    LIMIT 1
) mv ON true;
