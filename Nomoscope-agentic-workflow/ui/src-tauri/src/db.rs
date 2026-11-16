//! Read-only access to the legislation DB (Nomotheca-RAG/db/schema.sql) for the
//! Database tab (corpus statistics, article search) and to the `eval`
//! schema (Nomokrisis-evaluation_pipeline/db/eval_schema.sql) for the Evaluation tab.

use crate::pg::{connect, describe};
use postgres::Client;
use serde_json::{json, Value};

/// The login the UI connected with: the reviewer identity everywhere
/// (`decide_review_item`, `ops.jobs.submitted_by`, golden verdicts).
pub fn current_user(db_url: &str) -> Result<String, String> {
    let mut client = connect(db_url)?;
    client
        .query_one("SELECT current_user", &[])
        .map_err(describe)
        .map(|row| row.get::<_, String>(0))
}

/// Corpus totals, per-jurisdiction breakdown, embedding coverage and the
/// per-country readiness of the two non-legislative inputs (Country Report,
/// enriched parameter store).
pub fn stats(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;

    let totals = client
        .query_one(
            "SELECT (SELECT count(*) FROM jurisdictions WHERE parent_id IS NULL) AS jurisdictions,
                    (SELECT count(*) FROM instruments)          AS instruments,
                    (SELECT count(*) FROM legal_units)          AS legal_units,
                    (SELECT count(*) FROM legal_unit_versions)  AS versions,
                    (SELECT count(*) FROM legal_unit_versions
                      WHERE upper_inf(validity))                AS versions_in_force,
                    (SELECT count(*) FROM unit_texts)           AS unit_texts,
                    (SELECT count(*) FROM chunks)               AS chunks,
                    (SELECT count(*) FROM embeddings)           AS embeddings,
                    (SELECT count(*) FROM citation_registry)    AS citations_registered",
            &[],
        )
        .map_err(describe)?;

    let by_country = client
        .query(
            "SELECT coalesce(p.code, j.code) AS code, coalesce(p.name, j.name) AS name,
                    count(DISTINCT i.id)::bigint  AS instruments,
                    count(DISTINCT u.id)::bigint  AS legal_units,
                    count(DISTINCT v.id)::bigint  AS versions,
                    count(DISTINCT v.id) FILTER (WHERE upper_inf(v.validity))::bigint AS in_force,
                    count(DISTINCT t.id)::bigint  AS texts,
                    count(DISTINCT v.id) FILTER (WHERE t.id IS NOT NULL)::bigint  AS text_versions,
                    count(DISTINCT v.id) FILTER (WHERE t.lang = 'en')::bigint     AS en_versions,
                    count(DISTINCT t.id) FILTER (WHERE t.authenticity = 'authentic')::bigint            AS authentic,
                    count(DISTINCT t.id) FILTER (WHERE t.authenticity = 'official_translation')::bigint AS official_translation,
                    count(DISTINCT t.id) FILTER (WHERE t.authenticity = 'machine_translation')::bigint  AS machine_translation,
                    count(DISTINCT c.id)::bigint  AS chunks,
                    count(DISTINCT e.chunk_id)::bigint AS embedded_chunks
             FROM jurisdictions j
             LEFT JOIN jurisdictions p       ON p.id = j.parent_id
             LEFT JOIN instruments i         ON i.jurisdiction_id = j.id
             LEFT JOIN legal_units u         ON u.instrument_id = i.id
             LEFT JOIN legal_unit_versions v ON v.legal_unit_id = u.id
             LEFT JOIN unit_texts t          ON t.version_id = v.id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id
             LEFT JOIN embeddings e          ON e.chunk_id = c.id
             -- Child jurisdictions (Spain's autonomous communities, ADR 0003)
             -- roll up into their country: one row per country the UI and the
             -- Ingest tab's jurisdiction picker know about.
             GROUP BY 1, 2 ORDER BY 1",
            &[],
        )
        .map_err(describe)?;

    let models = client
        .query(
            "SELECT m.id::int, m.name, m.provider, m.stored_dim::int, m.is_default,
                    count(e.chunk_id)::bigint AS embedded_chunks
             FROM embedding_models m
             LEFT JOIN embeddings e ON e.model_id = m.id
             GROUP BY m.id, m.name, m.provider, m.stored_dim, m.is_default
             ORDER BY m.id",
            &[],
        )
        .map_err(describe)?;

    // The languages the store is configured to index. The Contributed-document
    // form offers these and nothing else: a text stored under a language with
    // no FTS config is invisible to full-text search.
    let languages = client
        .query("SELECT lang FROM lang_fts_config ORDER BY lang", &[])
        .map_err(describe)?;

    // Non-legislative inputs the pipeline needs beside the law corpus: the
    // EUROMOD Country Report (instrument_type = 'country_report', a separate
    // corpus class excluded from evidence retrieval) and the enriched
    // parameter store loaded by `ingest-params`. Shown per country so a
    // missing one is visible before a run silently under-performs.
    let country_reports = client
        .query(
            "SELECT coalesce(p.code, j.code) AS code,
                    count(DISTINCT i.id)::bigint       AS reports,
                    count(DISTINCT c.id)::bigint       AS chunks,
                    count(DISTINCT e.chunk_id)::bigint AS embedded_chunks,
                    max(i.created_at)::date::text      AS ingested_on,
                    string_agg(DISTINCT i.national_id, ', ') AS ids
             FROM jurisdictions j
             LEFT JOIN jurisdictions p       ON p.id = j.parent_id
             LEFT JOIN instruments i         ON i.jurisdiction_id = j.id
                                            AND i.instrument_type = 'country_report'
             LEFT JOIN legal_units u         ON u.instrument_id = i.id
             LEFT JOIN legal_unit_versions v ON v.legal_unit_id = u.id
             LEFT JOIN unit_texts t          ON t.version_id = v.id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id
             LEFT JOIN embeddings e          ON e.chunk_id = c.id
             GROUP BY 1 ORDER BY 1",
            &[],
        )
        .map_err(describe)?;

    // The params schema lives in this same DB but is created by
    // `nomoscope-workflow init-param-db`; absent it, report "not initialised"
    // rather than failing the whole stats call.
    let params_schema: bool = client
        .query_one("SELECT to_regclass('params.parameters') IS NOT NULL", &[])
        .map_err(describe)?
        .get(0);

    let params_by_country = if params_schema {
        client
            .query(
                "SELECT p.country,
                        count(DISTINCT p.id)::bigint AS parameters,
                        count(v.id)::bigint          AS model_values,
                        count(DISTINCT p.id) FILTER (WHERE p.temporal_basis = 'income_year')::bigint
                                                     AS income_year,
                        max(p.ingested_at)::date::text AS ingested_on,
                        string_agg(DISTINCT p.source_file, ', ') AS source_files
                 FROM params.parameters p
                 LEFT JOIN params.model_values v ON v.parameter_id = p.id
                 GROUP BY p.country ORDER BY p.country",
                &[],
            )
            .map_err(describe)?
    } else {
        Vec::new()
    };

    // Merge on country code, keyed off the jurisdictions list so a country
    // with neither input still shows a row.
    let mut inputs: Vec<Value> = country_reports
        .iter()
        .map(|r| {
            let code = r.get::<_, String>("code");
            let p = params_by_country
                .iter()
                .find(|pr| pr.get::<_, String>("country") == code);
            json!({
                "code": code,
                "country_report": {
                    "reports": r.get::<_, i64>("reports"),
                    "chunks": r.get::<_, i64>("chunks"),
                    "embedded_chunks": r.get::<_, i64>("embedded_chunks"),
                    "ingested_on": r.get::<_, Option<String>>("ingested_on"),
                    "ids": r.get::<_, Option<String>>("ids"),
                },
                "parameters": p.map(|pr| json!({
                    "parameters": pr.get::<_, i64>("parameters"),
                    "model_values": pr.get::<_, i64>("model_values"),
                    "income_year": pr.get::<_, i64>("income_year"),
                    "ingested_on": pr.get::<_, Option<String>>("ingested_on"),
                    "source_files": pr.get::<_, Option<String>>("source_files"),
                })),
            })
        })
        .collect();

    // Parameters ingested for a country that has no jurisdictions row yet.
    let known: Vec<String> = country_reports
        .iter()
        .map(|r| r.get::<_, String>("code"))
        .collect();
    for pr in params_by_country
        .iter()
        .filter(|pr| !known.contains(&pr.get::<_, String>("country")))
    {
        inputs.push(json!({
            "code": pr.get::<_, String>("country"),
            "country_report": null,
            "parameters": {
                "parameters": pr.get::<_, i64>("parameters"),
                "model_values": pr.get::<_, i64>("model_values"),
                "income_year": pr.get::<_, i64>("income_year"),
                "ingested_on": pr.get::<_, Option<String>>("ingested_on"),
                "source_files": pr.get::<_, Option<String>>("source_files"),
            },
        }));
    }

    Ok(json!({
        "totals": {
            "jurisdictions": totals.get::<_, i64>("jurisdictions"),
            "instruments": totals.get::<_, i64>("instruments"),
            "legal_units": totals.get::<_, i64>("legal_units"),
            "versions": totals.get::<_, i64>("versions"),
            "versions_in_force": totals.get::<_, i64>("versions_in_force"),
            "unit_texts": totals.get::<_, i64>("unit_texts"),
            "chunks": totals.get::<_, i64>("chunks"),
            "embeddings": totals.get::<_, i64>("embeddings"),
            "citations_registered": totals.get::<_, i64>("citations_registered"),
        },
        "by_country": by_country.iter().map(|r| json!({
            "code": r.get::<_, String>("code"),
            "name": r.get::<_, Option<String>>("name"),
            "instruments": r.get::<_, i64>("instruments"),
            "legal_units": r.get::<_, i64>("legal_units"),
            "versions": r.get::<_, i64>("versions"),
            "in_force": r.get::<_, i64>("in_force"),
            "texts": r.get::<_, i64>("texts"),
            "text_versions": r.get::<_, i64>("text_versions"),
            "en_versions": r.get::<_, i64>("en_versions"),
            "authentic": r.get::<_, i64>("authentic"),
            "official_translation": r.get::<_, i64>("official_translation"),
            "machine_translation": r.get::<_, i64>("machine_translation"),
            "chunks": r.get::<_, i64>("chunks"),
            "embedded_chunks": r.get::<_, i64>("embedded_chunks"),
        })).collect::<Vec<_>>(),
        "languages": languages.iter().map(|r| r.get::<_, String>("lang")).collect::<Vec<_>>(),
        "embedding_models": models.iter().map(|r| json!({
            "id": r.get::<_, i32>(0),
            "name": r.get::<_, String>("name"),
            "provider": r.get::<_, Option<String>>("provider"),
            "stored_dim": r.get::<_, i32>("stored_dim"),
            "is_default": r.get::<_, bool>("is_default"),
            "embedded_chunks": r.get::<_, i64>("embedded_chunks"),
        })).collect::<Vec<_>>(),
        "model_inputs": {
            "params_schema": params_schema,
            "by_country": inputs,
        },
    }))
}

/// All evaluation runs with whole-run KPI rates (averaged across languages).
/// Errors with a hint if `nomokrisis-eval init-db` has not been run yet.
pub fn eval_runs(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT r.id, r.run_id, r.created_at::text AS created_at, r.as_of::text AS as_of,
                    r.model_provider, r.model_name, r.prompt_version, r.agent_version,
                    r.eval_version, r.dataset_version, r.git_commit, r.countries, r.notes,
                    count(res.id)::bigint                                        AS cases,
                    count(res.id) FILTER (WHERE res.error IS NOT NULL)::bigint   AS errors,
                    (100 * avg(res.routing_correct::int))::float8   AS routing_pct,
                    (100 * avg(res.value_correct::int))::float8     AS value_pct,
                    (100 * avg(res.date_correct::int))::float8      AS date_pct,
                    (100 * avg(res.citation_correct::int))::float8  AS citation_pct,
                    (100 * avg(res.supportedness::int))::float8     AS supportedness_pct,
                    (100 * avg(res.hallucination::int))::float8     AS hallucination_pct,
                    (100 * avg(res.retrieval_hit::int))::float8     AS retrieval_recall_pct,
                    avg(res.latency_ms)::float8                     AS avg_latency_ms,
                    sum(res.energy_kwh)::float8                     AS energy_kwh,
                    sum(res.gwp_kgco2eq)::float8                    AS gwp_kgco2eq
             FROM eval.runs r
             LEFT JOIN eval.results res ON res.run_pk = r.id
             GROUP BY r.id
             ORDER BY r.created_at DESC",
            &[],
        )
        .map_err(|e| {
            let msg = describe(e);
            if msg.contains("eval.runs") {
                format!("{msg} — has `nomokrisis-eval init-db` been run?")
            } else {
                msg
            }
        })?;

    Ok(json!({
        "runs": rows.iter().map(|r| json!({
            "id": r.get::<_, i64>("id"),
            "run_id": r.get::<_, String>("run_id"),
            "created_at": r.get::<_, String>("created_at"),
            "as_of": r.get::<_, String>("as_of"),
            "model_provider": r.get::<_, String>("model_provider"),
            "model_name": r.get::<_, String>("model_name"),
            "prompt_version": r.get::<_, String>("prompt_version"),
            "agent_version": r.get::<_, String>("agent_version"),
            "eval_version": r.get::<_, String>("eval_version"),
            "dataset_version": r.get::<_, String>("dataset_version"),
            "git_commit": r.get::<_, Option<String>>("git_commit"),
            "countries": r.get::<_, Vec<String>>("countries"),
            "notes": r.get::<_, Option<String>>("notes"),
            "cases": r.get::<_, i64>("cases"),
            "errors": r.get::<_, i64>("errors"),
            "routing_pct": r.get::<_, Option<f64>>("routing_pct"),
            "value_pct": r.get::<_, Option<f64>>("value_pct"),
            "date_pct": r.get::<_, Option<f64>>("date_pct"),
            "citation_pct": r.get::<_, Option<f64>>("citation_pct"),
            "supportedness_pct": r.get::<_, Option<f64>>("supportedness_pct"),
            "hallucination_pct": r.get::<_, Option<f64>>("hallucination_pct"),
            "retrieval_recall_pct": r.get::<_, Option<f64>>("retrieval_recall_pct"),
            "avg_latency_ms": r.get::<_, Option<f64>>("avg_latency_ms"),
            "energy_kwh": r.get::<_, Option<f64>>("energy_kwh"),
            "gwp_kgco2eq": r.get::<_, Option<f64>>("gwp_kgco2eq"),
        })).collect::<Vec<_>>(),
    }))
}

/// Per-(language, country) KPI breakdown plus all case results for one run.
pub fn eval_run_detail(db_url: &str, run_pk: i64) -> Result<Value, String> {
    let mut client = connect(db_url)?;

    let summary = client
        .query(
            "SELECT language, country, cases::bigint AS cases, errors::bigint AS errors,
                    routing_pct::float8, value_pct::float8, date_pct::float8,
                    citation_pct::float8, supportedness_pct::float8,
                    hallucination_pct::float8, retrieval_recall_pct::float8,
                    avg_latency_ms::float8, energy_kwh::float8, gwp_kgco2eq::float8
             FROM eval.run_summary
             WHERE run_pk = $1
             ORDER BY language, country",
            &[&run_pk],
        )
        .map_err(describe)?;

    let cases = client
        .query(
            "SELECT case_id, country, language, model_target, difficulty, source_class,
                    routing_expected, routing_actual, routing_correct,
                    value_correct, date_correct, citation_correct, supportedness,
                    hallucination, retrieval_hit, confidence, latency_ms, error, details
             FROM eval.results
             WHERE run_pk = $1
             ORDER BY country, case_id",
            &[&run_pk],
        )
        .map_err(describe)?;

    Ok(json!({
        "summary": summary.iter().map(|r| json!({
            "language": r.get::<_, String>("language"),
            "country": r.get::<_, String>("country"),
            "cases": r.get::<_, i64>("cases"),
            "errors": r.get::<_, i64>("errors"),
            "routing_pct": r.get::<_, Option<f64>>("routing_pct"),
            "value_pct": r.get::<_, Option<f64>>("value_pct"),
            "date_pct": r.get::<_, Option<f64>>("date_pct"),
            "citation_pct": r.get::<_, Option<f64>>("citation_pct"),
            "supportedness_pct": r.get::<_, Option<f64>>("supportedness_pct"),
            "hallucination_pct": r.get::<_, Option<f64>>("hallucination_pct"),
            "retrieval_recall_pct": r.get::<_, Option<f64>>("retrieval_recall_pct"),
            "avg_latency_ms": r.get::<_, Option<f64>>("avg_latency_ms"),
            "energy_kwh": r.get::<_, Option<f64>>("energy_kwh"),
            "gwp_kgco2eq": r.get::<_, Option<f64>>("gwp_kgco2eq"),
        })).collect::<Vec<_>>(),
        "cases": cases.iter().map(|r| json!({
            "case_id": r.get::<_, String>("case_id"),
            "country": r.get::<_, String>("country"),
            "language": r.get::<_, String>("language"),
            "model_target": r.get::<_, Option<String>>("model_target"),
            "difficulty": r.get::<_, Option<String>>("difficulty"),
            "source_class": r.get::<_, Option<String>>("source_class"),
            "routing_expected": r.get::<_, String>("routing_expected"),
            "routing_actual": r.get::<_, Option<String>>("routing_actual"),
            "routing_correct": r.get::<_, Option<bool>>("routing_correct"),
            "value_correct": r.get::<_, Option<bool>>("value_correct"),
            "date_correct": r.get::<_, Option<bool>>("date_correct"),
            "citation_correct": r.get::<_, Option<bool>>("citation_correct"),
            "supportedness": r.get::<_, Option<bool>>("supportedness"),
            "hallucination": r.get::<_, bool>("hallucination"),
            "retrieval_hit": r.get::<_, Option<bool>>("retrieval_hit"),
            "confidence": r.get::<_, Option<f32>>("confidence"),
            "latency_ms": r.get::<_, Option<i32>>("latency_ms"),
            "error": r.get::<_, Option<String>>("error"),
            "details": r.get::<_, Option<Value>>("details"),
        })).collect::<Vec<_>>(),
    }))
}

/// Instruments a contributed document could be said to implement.
///
/// Read-only, matching a fragment of the title or of the national id. Context
/// instruments are excluded: a Country Report describes the EUROMOD model, so
/// nothing implements one.
pub fn search_instruments(
    db_url: &str,
    country: &str,
    query: &str,
    limit: i64,
) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let pattern = format!("%{}%", query.trim());
    let rows = client
        .query(
            "SELECT i.national_id,
                    i.instrument_type,
                    i.source_trust_class,
                    i.title_search           AS title,
                    i.publication_date::text AS publication_date
             FROM instruments i
             JOIN jurisdictions j ON j.id = i.jurisdiction_id
             WHERE (j.code = upper($1)
                    OR j.parent_id = (SELECT id FROM jurisdictions WHERE code = upper($1)))
               AND i.source_trust_class <> 'context'
               AND i.national_id IS NOT NULL
               AND (i.title_search ILIKE $2 OR i.national_id ILIKE $2)
             ORDER BY (i.national_id ILIKE $2) DESC, i.publication_date DESC NULLS LAST
             LIMIT $3",
            &[&country, &pattern, &limit],
        )
        .map_err(|e| format!("instrument search failed: {}", describe(e)))?;

    Ok(json!({
        "instruments": rows.iter().map(|r| json!({
            "national_id": r.get::<_, String>("national_id"),
            "instrument_type": r.get::<_, String>("instrument_type"),
            "source_trust_class": r.get::<_, String>("source_trust_class"),
            "title": r.get::<_, Option<String>>("title"),
            "publication_date": r.get::<_, Option<String>>("publication_date"),
        })).collect::<Vec<_>>()
    }))
}

/// All parameters in the `params` schema, each with its most recent model
/// value and its most recent agentic extraction run (Parameters tab).
pub fn params_list(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT p.country, p.model_target, p.policy, p.function, p.name,
                    p.value_type, p.unit, p.parameter_key,
                    coalesce(p.short_label->>'en', p.label->>'en') AS label,
                    jsonb_build_object('label', p.label, 'short_label', p.short_label,
                                       'description', p.description,
                                       'explanation', p.explanation) AS texts,
                    (SELECT count(*) FROM params.parameter_edits e
                      WHERE e.model_target = p.model_target) AS edit_count,
                    p.description->>'en'            AS description,
                    p.classification->>'category'   AS category,
                    p.parameter_group               AS groups,
                    mv.value_raw                    AS current_value,
                    mv.raw_euromod_value            AS current_raw,
                    mv.valid_from::text             AS current_valid_from,
                    mv.source_type                  AS current_source_type,
                    r.run_id                        AS last_run_id,
                    r.as_of::text                   AS last_as_of,
                    r.model                         AS last_model,
                    r.routing                       AS last_routing,
                    r.critique_verdict              AS last_verdict,
                    r.phoenix_project               AS last_phoenix_project,
                    r.phoenix_trace_id              AS last_trace_id,
                    r.item_id                       AS last_item_id,
                    r.finished_at::text             AS last_finished_at
             FROM params.parameters p
             LEFT JOIN LATERAL (
                 SELECT * FROM params.model_values v
                 WHERE v.parameter_id = p.id
                 ORDER BY v.valid_from DESC LIMIT 1
             ) mv ON true
             LEFT JOIN LATERAL (
                 SELECT * FROM params.extraction_runs er
                 WHERE er.model_target = p.model_target
                 ORDER BY er.started_at DESC LIMIT 1
             ) r ON true
             ORDER BY p.country, p.policy, p.name",
            &[],
        )
        .map_err(|e| {
            format!("params query failed (has `nomoscope-workflow ingest-params` been run?): {}", describe(e))
        })?;

    // The EUROMOD system years each country actually defines. The run form must
    // offer these and nothing else: anchoring a run on today's date verifies a
    // system that does not exist, and every parameter then comes back `changed`
    // against the newest value on file rather than against real evidence.
    let year_rows = client
        .query(
            "SELECT p.country,
                    array_agg(DISTINCT v.system_year ORDER BY v.system_year) AS years
             FROM params.model_values v
             JOIN params.parameters p ON p.id = v.parameter_id
             WHERE v.system_year IS NOT NULL
             GROUP BY p.country",
            &[],
        )
        .map_err(|e| format!("system-year query failed: {}", describe(e)))?;
    let mut system_years = serde_json::Map::new();
    for r in &year_rows {
        system_years.insert(
            r.get::<_, String>("country"),
            json!(r.get::<_, Vec<i32>>("years")),
        );
    }

    Ok(json!({
        "system_years": system_years,
        "parameters": rows.iter().map(|r| json!({
            "country": r.get::<_, String>("country"),
            "model_target": r.get::<_, String>("model_target"),
            "policy": r.get::<_, Option<String>>("policy"),
            "function": r.get::<_, Option<String>>("function"),
            "name": r.get::<_, Option<String>>("name"),
            "value_type": r.get::<_, String>("value_type"),
            "unit": r.get::<_, Option<String>>("unit"),
            "parameter_key": r.get::<_, Option<String>>("parameter_key"),
            "label": r.get::<_, Option<String>>("label"),
            // the full language-keyed texts, for the metadata editor
            "texts": r.get::<_, Value>("texts"),
            "edit_count": r.get::<_, i64>("edit_count"),
            "description": r.get::<_, Option<String>>("description"),
            "category": r.get::<_, Option<String>>("category"),
            // group memberships: [{id, kind, role, index}, …] or null
            "groups": r.get::<_, Option<Value>>("groups"),
            "current_value": r.get::<_, Option<Value>>("current_value"),
            "current_raw": r.get::<_, Option<String>>("current_raw"),
            "current_valid_from": r.get::<_, Option<String>>("current_valid_from"),
            "current_source_type": r.get::<_, Option<String>>("current_source_type"),
            "last_run_id": r.get::<_, Option<String>>("last_run_id"),
            "last_as_of": r.get::<_, Option<String>>("last_as_of"),
            "last_model": r.get::<_, Option<String>>("last_model"),
            "last_routing": r.get::<_, Option<String>>("last_routing"),
            "last_verdict": r.get::<_, Option<String>>("last_verdict"),
            "last_phoenix_project": r.get::<_, Option<String>>("last_phoenix_project"),
            "last_trace_id": r.get::<_, Option<String>>("last_trace_id"),
            "last_item_id": r.get::<_, Option<String>>("last_item_id"),
            "last_finished_at": r.get::<_, Option<String>>("last_finished_at"),
        })).collect::<Vec<_>>(),
    }))
}

/// What the review queue item does not carry about its parameter — its
/// EUROMOD texts, its law-language texts and the values EUROMOD has held —
/// for the hand-off prompt to an external assistant. A `group:<id>` target
/// returns every member of that bracket schedule, in schedule order.
pub fn parameter_context(db_url: &str, model_target: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let group = model_target.strip_prefix("group:");
    let rows = client
        .query(
            "SELECT p.model_target, p.policy, p.function, p.name, p.unit,
                    p.temporal_basis::text AS temporal_basis,
                    jsonb_build_object('label', p.label, 'short_label', p.short_label,
                                       'description', p.description,
                                       'explanation', p.explanation) AS texts,
                    coalesce((SELECT jsonb_agg(jsonb_build_object(
                                  'lang', t.lang, 'field', t.field,
                                  'origin', t.origin, 'content', t.content)
                                ORDER BY t.lang, t.field, t.origin)
                              FROM params.parameter_texts t
                              WHERE t.parameter_id = p.id), '[]'::jsonb) AS law_texts,
                    coalesce((SELECT jsonb_agg(jsonb_build_object(
                                  'system_year', v.system_year,
                                  'valid_from', v.valid_from::text,
                                  'valid_to', v.valid_to::text,
                                  'value', v.value_raw,
                                  'raw', v.raw_euromod_value)
                                ORDER BY v.valid_from)
                              FROM params.model_values v
                              WHERE v.parameter_id = p.id), '[]'::jsonb) AS history,
                    (SELECT g->>'role' || ' ' || (g->>'index')
                       FROM jsonb_array_elements(coalesce(p.parameter_group, '[]'::jsonb)) g
                      WHERE g->>'id' = $2 LIMIT 1) AS group_role
             FROM params.parameters p
             WHERE ($2::text IS NULL AND p.model_target = $1)
                OR ($2::text IS NOT NULL
                    AND p.parameter_group @> jsonb_build_array(jsonb_build_object('id', $2::text)))
             ORDER BY group_role NULLS FIRST, p.name",
            &[&model_target, &group],
        )
        .map_err(|e| format!("parameter context query failed: {}", describe(e)))?;
    Ok(json!({
        "parameters": rows.iter().map(|r| json!({
            "model_target": r.get::<_, String>("model_target"),
            "policy": r.get::<_, Option<String>>("policy"),
            "function": r.get::<_, Option<String>>("function"),
            "name": r.get::<_, Option<String>>("name"),
            "unit": r.get::<_, Option<String>>("unit"),
            "temporal_basis": r.get::<_, Option<String>>("temporal_basis"),
            "texts": r.get::<_, Value>("texts"),
            "law_texts": r.get::<_, Value>("law_texts"),
            "history": r.get::<_, Value>("history"),
            "group_role": r.get::<_, Option<String>>("group_role"),
        })).collect::<Vec<_>>(),
    }))
}

/// One parameter's metadata edits (`params.parameter_edits`), newest first.
pub fn parameter_edits(db_url: &str, model_target: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT id, field, value, previous, reviewer, note, edited_at::text AS edited_at
             FROM params.parameter_edits WHERE model_target = $1
             ORDER BY edited_at DESC, id DESC",
            &[&model_target],
        )
        .map_err(|e| format!("edit history query failed (run `nomoscope-workflow init-param-db`?): {}", describe(e)))?;
    Ok(json!(rows.iter().map(|r| json!({
        "id": r.get::<_, i64>("id"),
        "field": r.get::<_, String>("field"),
        "value": r.get::<_, Option<Value>>("value"),
        "previous": r.get::<_, Option<Value>>("previous"),
        "reviewer": r.get::<_, String>("reviewer"),
        "note": r.get::<_, Option<String>>("note"),
        "edited_at": r.get::<_, String>("edited_at"),
    })).collect::<Vec<_>>()))
}

/// Every language rendering of the legal-unit version a cited chunk belongs to.
///
/// A chunk hangs off one `unit_texts` row = one language rendering of one
/// version; the sibling renderings (authentic BE fr/nl, official or machine
/// translations) are the other `unit_texts` rows of the same `version_id`.
/// Translations are chunked independently, so the sibling chunk is matched on
/// `seq` and we fall back to the full version text when there is none.
pub fn chunk_renderings(db_url: &str, chunk_id: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    client
        .batch_execute(
            "SET default_transaction_read_only = on;
             SET statement_timeout = '15s';",
        )
        .map_err(describe)?;
    let rows = client
        .query(
            "SELECT t.id::text                     AS unit_text_id,
                    t.lang,
                    t.authenticity,
                    t.mt_engine,
                    t.source_lang,
                    c.id::text                     AS chunk_id,
                    c.seq,
                    coalesce(c.content, t.content) AS content,
                    (c.id IS NOT NULL)             AS aligned,
                    (t.id = src_text.id)           AS is_cited,
                    u.citation,
                    v.validity::text               AS validity
             FROM chunks src
             JOIN unit_texts src_text        ON src_text.id = src.unit_text_id
             JOIN unit_texts t               ON t.version_id = src_text.version_id
             JOIN legal_unit_versions v      ON v.id = t.version_id
             JOIN legal_units u              ON u.id = v.legal_unit_id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id AND c.seq = src.seq
             WHERE src.id = ($1::text)::uuid
             ORDER BY (t.id = src_text.id) DESC,
                      (t.authenticity = 'authentic') DESC,
                      t.lang",
            &[&chunk_id],
        )
        .map_err(|e| format!("chunk renderings query failed: {}", describe(e)))?;

    Ok(json!({
        "chunk_id": chunk_id,
        "renderings": rows.iter().map(|r| json!({
            "unit_text_id": r.get::<_, String>("unit_text_id"),
            "lang": r.get::<_, String>("lang"),
            "authenticity": r.get::<_, String>("authenticity"),
            "mt_engine": r.get::<_, Option<String>>("mt_engine"),
            "source_lang": r.get::<_, Option<String>>("source_lang"),
            "chunk_id": r.get::<_, Option<String>>("chunk_id"),
            "seq": r.get::<_, Option<i32>>("seq"),
            "content": r.get::<_, String>("content"),
            // false = no chunk with this seq in that language: full text shown
            "aligned": r.get::<_, bool>("aligned"),
            "is_cited": r.get::<_, bool>("is_cited"),
            "citation": r.get::<_, Option<String>>("citation"),
            "validity": r.get::<_, Option<String>>("validity"),
        })).collect::<Vec<_>>(),
    }))
}

/// Replace the database name in a Postgres URL, preserving any `?options`.
fn swap_database(db_url: &str, dbname: &str) -> String {
    let (base, query) = match db_url.split_once('?') {
        Some((b, q)) => (b, Some(q)),
        None => (db_url, None),
    };
    let swapped = match base.rsplit_once('/') {
        // Guard against URLs with no db path: the part after the last '/'
        // must look like a db name, not `host:port` or `user@host`.
        Some((head, tail)) if !tail.contains('@') && !tail.contains(':') && !head.ends_with(':') => {
            format!("{head}/{dbname}")
        }
        _ => format!("{base}/{dbname}"),
    };
    match query {
        Some(q) => format!("{swapped}?{q}"),
        None => swapped,
    }
}

/// Phoenix project name -> GraphQL global id (base64 of "Project:<id>"), read
/// from the `phoenix` database that shares this Postgres instance. The GID is
// ---------------------------------------------------------------------------
// Stage D — reviewer decisions. params.review_decisions is the system of
// record, written only by params.decide_review_item (store.rs); this side
// just reads it for the Audit tab.
// ---------------------------------------------------------------------------

/// The audit log, newest first — the Audit tab's data source.
pub fn load_decisions(db_url: &str, limit: i64) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT id, proposal_pk, item_id, run_id, model_target, as_of::text AS as_of,
                    routing, action, reviewer, note, edited_value, edited_fields,
                    confidence, critique_verdict,
                    decided_at::text AS decided_at, logged_at::text AS logged_at
             FROM params.review_decisions
             ORDER BY coalesce(decided_at, logged_at) DESC, id DESC
             LIMIT $1",
            &[&limit],
        )
        .map_err(|e| format!("decisions query failed: {}", describe(e)))?;
    Ok(json!({
        "decisions": rows.iter().map(|r| json!({
            "id": r.get::<_, i64>("id"),
            "proposal_pk": r.get::<_, Option<i64>>("proposal_pk"),
            "item_id": r.get::<_, Option<String>>("item_id"),
            "run_id": r.get::<_, Option<String>>("run_id"),
            "model_target": r.get::<_, Option<String>>("model_target"),
            "as_of": r.get::<_, Option<String>>("as_of"),
            "routing": r.get::<_, Option<String>>("routing"),
            "action": r.get::<_, String>("action"),
            "reviewer": r.get::<_, Option<String>>("reviewer"),
            "note": r.get::<_, Option<String>>("note"),
            "edited_value": r.get::<_, Option<Value>>("edited_value"),
            "edited_fields": r.get::<_, Option<Value>>("edited_fields"),
            "confidence": r.get::<_, Option<f32>>("confidence"),
            "critique_verdict": r.get::<_, Option<String>>("critique_verdict"),
            "decided_at": r.get::<_, Option<String>>("decided_at"),
            "logged_at": r.get::<_, Option<String>>("logged_at"),
        })).collect::<Vec<_>>(),
    }))
}

/// what Phoenix's trace deep-links use:
///   <endpoint>/projects/<gid>/traces/<trace_id>
pub fn phoenix_projects(db_url: &str) -> Result<Value, String> {
    use base64::engine::general_purpose::STANDARD;
    use base64::Engine;

    let mut client = connect(&swap_database(db_url, "phoenix"))?;
    let rows = client
        .query("SELECT id, name FROM projects", &[])
        .map_err(|e| format!("phoenix projects query failed: {}", describe(e)))?;
    Ok(json!({
        "projects": rows.iter().map(|r| {
            let id: i32 = r.get("id");
            json!({
                "name": r.get::<_, String>("name"),
                "gid": STANDARD.encode(format!("Project:{id}")),
            })
        }).collect::<Vec<_>>(),
    }))
}

#[cfg(test)]
mod tests {
    #[test]
    fn swap_database_keeps_host_and_options() {
        assert_eq!(
            super::swap_database("postgresql://jrc:jrc@localhost:5434/legislation", "phoenix"),
            "postgresql://jrc:jrc@localhost:5434/phoenix"
        );
        assert_eq!(
            super::swap_database("postgresql://jrc:jrc@localhost:5434/legislation?sslmode=disable", "phoenix"),
            "postgresql://jrc:jrc@localhost:5434/phoenix?sslmode=disable"
        );
        assert_eq!(
            super::swap_database("postgresql://jrc:jrc@localhost:5434", "phoenix"),
            "postgresql://jrc:jrc@localhost:5434/phoenix"
        );
    }

    /// Exercises the eval queries and row→JSON type mappings against the live
    /// stack; silently skipped when the DB is down or `init-db` hasn't run.
    #[test]
    fn eval_queries_smoke() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        if super::connect(&url).is_err() {
            return;
        }
        let runs = match super::eval_runs(&url) {
            Ok(v) => v,
            Err(e) if e.contains("init-db") => return,
            Err(e) => panic!("eval_runs failed: {e}"),
        };
        if let Some(first) = runs["runs"].as_array().unwrap().first() {
            let pk = first["id"].as_i64().unwrap();
            let detail = super::eval_run_detail(&url, pk).unwrap();
            assert!(detail["summary"].is_array());
            assert!(detail["cases"].is_array());
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum SearchMode {
    Hybrid,
    FullText,
    Vector,
}

impl SearchMode {
    pub fn parse(value: &str) -> Result<Self, String> {
        match value {
            "hybrid" => Ok(Self::Hybrid),
            "full_text" => Ok(Self::FullText),
            "vector" => Ok(Self::Vector),
            _ => Err(format!("unsupported search mode: {value}")),
        }
    }

    pub fn uses_vector(self) -> bool {
        matches!(self, Self::Hybrid | Self::Vector)
    }

    fn uses_full_text(self) -> bool {
        matches!(self, Self::Hybrid | Self::FullText)
    }

    fn as_str(self) -> &'static str {
        match self {
            Self::Hybrid => "hybrid",
            Self::FullText => "full_text",
            Self::Vector => "vector",
        }
    }
}

/// What the Database tab (and the RAG chat's search box) sends.
#[derive(serde::Deserialize)]
pub struct SearchPayload {
    pub db_url: String,
    pub query: String,
    pub country: Option<String>,
    pub as_of: Option<String>,
    pub languages: Option<Vec<String>>,
    pub mode: Option<String>,
    pub limit: Option<i64>,
}

/// The embedding model the corpus is searched with (`embedding_models.is_default`).
pub fn default_model_id(client: &mut Client) -> Result<i32, String> {
    client
        .query_opt(
            "SELECT id::int FROM embedding_models WHERE is_default ORDER BY id LIMIT 1",
            &[],
        )
        .map_err(|e| format!("embedding model lookup failed: {}", describe(e)))?
        .map(|row| row.get::<_, i32>(0))
        .ok_or_else(|| "no default embedding model in embedding_models".to_string())
}

/// Article search for both desktop apps. Vector and hybrid modes need the
/// query encoded by the worker (an `encode` job, with the corpus's default
/// model); when no worker is alive the search degrades to full text and says
/// so in `notice`, rather than failing.
pub fn search(payload: &SearchPayload, default_limit: i64) -> Result<Value, String> {
    let mut mode = SearchMode::parse(payload.mode.as_deref().unwrap_or("hybrid"))?;
    let model_id = default_model_id(&mut connect(&payload.db_url)?)?;
    let mut notice: Option<String> = None;
    let query_vector = if mode.uses_vector() {
        match crate::jobs::encode_query(&crate::jobs::EncodePayload {
            db_url: payload.db_url.clone(),
            query: payload.query.clone(),
            sentences: None,
            model_id: Some(model_id),
        }) {
            Ok(result) => Some(
                result
                    .get("halfvec")
                    .and_then(Value::as_str)
                    .filter(|v| v.starts_with('[') && v.ends_with(']'))
                    .ok_or("encode job returned no halfvec")?
                    .to_string(),
            ),
            Err(e) if e == crate::jobs::NO_WORKER => {
                notice = Some(format!("{e}; showing full-text results instead"));
                mode = SearchMode::FullText;
                None
            }
            Err(e) => return Err(e),
        }
    } else {
        None
    };
    let mut result = search_articles(
        &payload.db_url,
        &payload.query,
        payload.country.as_deref(),
        payload.as_of.as_deref(),
        payload.languages.as_deref(),
        mode,
        query_vector.as_deref(),
        model_id,
        payload.limit.unwrap_or(default_limit),
    )?;
    result["notice"] = json!(notice);
    Ok(result)
}

/// Search law chunks with the database's `search_chunks()` — the one hybrid
/// search the workflow, the eval and the MCP server use too (live version on
/// `as_of`, OR-of-terms FTS, RRF + vector top-3 slot, vector leg ranked over
/// the filtered set, never through HNSW). This page browses, so Country
/// Reports are included; every hit carries its `source_trust_class`.
#[allow(clippy::too_many_arguments)]
pub fn search_articles(
    db_url: &str,
    query: &str,
    country: Option<&str>,
    as_of: Option<&str>,
    languages: Option<&[String]>,
    mode: SearchMode,
    query_vector: Option<&str>,
    model_id: i32,
    limit: i64,
) -> Result<Value, String> {
    if query.trim().is_empty() {
        return Err("query must not be empty".to_string());
    }
    if !(1..=50).contains(&limit) {
        return Err("limit must be between 1 and 50".to_string());
    }
    if mode.uses_vector() && query_vector.is_none() {
        return Err(format!("{} search requires a query vector", mode.as_str()));
    }

    let mut client = connect(db_url)?;
    client
        .batch_execute(
            "SET default_transaction_read_only = on;
             SET statement_timeout = '30s';",
        )
        .map_err(describe)?;
    let language_filter = languages.map(|values| values.to_vec());
    let use_full_text = mode.uses_full_text();
    let use_vector = mode.uses_vector();
    let vector = if use_vector { query_vector } else { None };
    let rows = client
        .query(
            "WITH found AS (
                SELECT s.*, t.version_id, ch.seq,
                       row_number() OVER (
                           PARTITION BY t.version_id, ch.seq
                           ORDER BY s.score DESC, s.chunk_id
                       ) AS rendering_rank
                FROM search_chunks(
                        $1, $5::text::halfvec(1024), $8,
                        CASE WHEN $2::text IS NULL THEN NULL ELSE jurisdiction_tree($2) END,
                        $4::text[], ($3::text)::date, ($7::bigint * 4)::int, $6, true) s
                JOIN chunks ch    ON ch.id = s.chunk_id
                JOIN unit_texts t ON t.id = ch.unit_text_id
             )
             SELECT d.chunk_id::text, u.citation, ch.context_header, ch.content,
                    CASE WHEN $6 THEN ts_headline(ch.search_config, ch.content,
                              websearch_to_tsquery(ch.search_config, fts_or_query($1)),
                              'StartSel=<<HL>>, StopSel=<</HL>>, HighlightAll=true')
                    END AS headline,
                    t.lang, t.authenticity, v.validity::text, v.version_status,
                    j.code AS country, i.title AS instrument_title, i.source_trust_class,
                    d.score,
                    d.fts_rank AS full_text_rank,
                    d.fts_score AS full_text_score,
                    coalesce(1.0 / (60 + d.fts_rank), 0)::float8 AS full_text_contribution,
                    d.vec_rank AS vector_rank,
                    d.vec_distance AS vector_distance,
                    coalesce(1.0 / (60 + d.vec_rank), 0)::float8 AS vector_contribution
             FROM found d
             JOIN chunks ch             ON ch.id = d.chunk_id
             JOIN unit_texts t          ON t.id = ch.unit_text_id
             JOIN legal_unit_versions v ON v.id = t.version_id
             JOIN legal_units u         ON u.id = v.legal_unit_id
             JOIN instruments i         ON i.id = u.instrument_id
             JOIN jurisdictions j       ON j.id = i.jurisdiction_id
             WHERE d.rendering_rank = 1
             ORDER BY d.score DESC, d.chunk_id
             LIMIT $7::bigint",
            &[
                &query,
                &country,
                &as_of,
                &language_filter,
                &vector,
                &use_full_text,
                &limit,
                &model_id,
            ],
        )
        .map_err(describe)?;

    Ok(json!({
        "query": query,
        "mode": mode.as_str(),
        "model_id": if use_vector { Some(model_id) } else { None },
        "ranking": if mode == SearchMode::Hybrid {
            "RRF(k=60) over full-text and vector ranks, vector top 3 guaranteed"
        } else if mode == SearchMode::Vector {
            "vector rank"
        } else {
            "full-text rank"
        },
        "filters": {
            "country": country,
            "as_of": as_of,
            "languages": language_filter,
        },
        "results": rows.iter().map(|r| json!({
            "chunk_id": r.get::<_, String>("chunk_id"),
            "citation": r.get::<_, Option<String>>("citation"),
            "context_header": r.get::<_, String>("context_header"),
            "content": r.get::<_, String>("content"),
            // `content` with every query lexeme wrapped in <<HL>>…<</HL>>
            // (null in vector-only mode); the UI turns the markers into marks.
            "headline": r.get::<_, Option<String>>("headline"),
            "lang": r.get::<_, String>("lang"),
            "authenticity": r.get::<_, String>("authenticity"),
            "validity": r.get::<_, String>("validity"),
            "version_status": r.get::<_, String>("version_status"),
            "country": r.get::<_, String>("country"),
            "instrument_title": r.get::<_, Value>("instrument_title"),
            "source_trust_class": r.get::<_, String>("source_trust_class"),
            "score": r.get::<_, f64>("score"),
            "full_text_rank": r.get::<_, Option<i64>>("full_text_rank"),
            "full_text_score": r.get::<_, Option<f64>>("full_text_score"),
            "full_text_contribution": r.get::<_, f64>("full_text_contribution"),
            "vector_rank": r.get::<_, Option<i64>>("vector_rank"),
            "vector_distance": r.get::<_, Option<f64>>("vector_distance"),
            "vector_contribution": r.get::<_, f64>("vector_contribution"),
        })).collect::<Vec<_>>(),
    }))
}

#[cfg(test)]
mod search_tests {
    use super::SearchMode;

    #[test]
    fn validates_search_modes() {
        assert_eq!(SearchMode::parse("hybrid").unwrap(), SearchMode::Hybrid);
        assert_eq!(
            SearchMode::parse("full_text").unwrap(),
            SearchMode::FullText
        );
        assert_eq!(SearchMode::parse("vector").unwrap(), SearchMode::Vector);
        assert!(SearchMode::parse("semantic").is_err());
    }

    #[test]
    fn instrument_search_excludes_context_instruments() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        if super::connect(&url).is_err() {
            return;
        }
        let result = super::search_instruments(&url, "FR", "", 50).unwrap();

        let classes: Vec<String> = result["instruments"]
            .as_array()
            .unwrap()
            .iter()
            .map(|row| row["source_trust_class"].as_str().unwrap().to_string())
            .collect();
        assert!(!classes.contains(&"context".to_string()), "{classes:?}");
    }

    #[test]
    fn search_queries_smoke() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let Ok(mut client) = super::connect(&url) else {
            return;
        };
        let vector: String = client
            .query_one(
                "SELECT placeholder_embedding($1)::text",
                &[&"income tax brackets"],
            )
            .unwrap()
            .get(0);

        for mode in [SearchMode::FullText, SearchMode::Vector, SearchMode::Hybrid] {
            let query_vector = mode.uses_vector().then_some(vector.as_str());
            let result = super::search_articles(
                &url,
                "income tax brackets",
                None,
                Some("2025-06-01"),
                None,
                mode,
                query_vector,
                99,
                5,
            )
            .unwrap_or_else(|error| panic!("{} search failed: {error}", mode.as_str()));
            assert!(result["results"].is_array());
        }
    }
}
