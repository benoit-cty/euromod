//! Read-only access to the legislation DB (Nomotheca-RAG/db/schema.sql) for the
//! Database tab (corpus statistics, article search) and to the `eval`
//! schema (Nomokrisis-evaluation_pipeline/db/eval_schema.sql) for the Evaluation tab.

use postgres::{Client, NoTls};
use serde_json::{json, Value};

fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {e}"))
}

/// Corpus totals, per-jurisdiction breakdown and embedding coverage.
pub fn stats(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;

    let totals = client
        .query_one(
            "SELECT (SELECT count(*) FROM jurisdictions)        AS jurisdictions,
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
        .map_err(|e| e.to_string())?;

    let by_country = client
        .query(
            "SELECT j.code, j.name,
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
             LEFT JOIN instruments i         ON i.jurisdiction_id = j.id
             LEFT JOIN legal_units u         ON u.instrument_id = i.id
             LEFT JOIN legal_unit_versions v ON v.legal_unit_id = u.id
             LEFT JOIN unit_texts t          ON t.version_id = v.id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id
             LEFT JOIN embeddings e          ON e.chunk_id = c.id
             GROUP BY j.code, j.name ORDER BY j.code",
            &[],
        )
        .map_err(|e| e.to_string())?;

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
        .map_err(|e| e.to_string())?;

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
        "embedding_models": models.iter().map(|r| json!({
            "id": r.get::<_, i32>(0),
            "name": r.get::<_, String>("name"),
            "provider": r.get::<_, Option<String>>("provider"),
            "stored_dim": r.get::<_, i32>("stored_dim"),
            "is_default": r.get::<_, bool>("is_default"),
            "embedded_chunks": r.get::<_, i64>("embedded_chunks"),
        })).collect::<Vec<_>>(),
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
            let msg = e.to_string();
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
        .map_err(|e| e.to_string())?;

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
        .map_err(|e| e.to_string())?;

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

/// All parameters in the `params` schema, each with its most recent model
/// value and its most recent agentic extraction run (Parameters tab).
pub fn params_list(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT p.country, p.model_target, p.policy, p.function, p.name,
                    p.value_type, p.unit,
                    coalesce(p.short_label->>'en', p.label->>'en') AS label,
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
            format!("params query failed (has `nomoscope-workflow ingest-params` been run?): {e}")
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
        .map_err(|e| format!("system-year query failed: {e}"))?;
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
            "label": r.get::<_, Option<String>>("label"),
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
        .map_err(|e| e.to_string())?;
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
        .map_err(|e| format!("chunk renderings query failed: {e}"))?;

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
/// what Phoenix's trace deep-links use:
///   <endpoint>/projects/<gid>/traces/<trace_id>
pub fn phoenix_projects(db_url: &str) -> Result<Value, String> {
    use base64::engine::general_purpose::STANDARD;
    use base64::Engine;

    let mut client = connect(&swap_database(db_url, "phoenix"))?;
    let rows = client
        .query("SELECT id, name FROM projects", &[])
        .map_err(|e| format!("phoenix projects query failed: {e}"))?;
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

/// Search law chunks using FTS, BGE-M3 vectors, or RRF-fused hybrid ranking.
pub fn search_articles(
    db_url: &str,
    query: &str,
    country: Option<&str>,
    as_of: Option<&str>,
    languages: Option<&[String]>,
    mode: SearchMode,
    query_vector: Option<&str>,
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
             SET statement_timeout = '30s';
             SET hnsw.ef_search = 100;",
        )
        .map_err(|e| e.to_string())?;
    let language_filter = languages.map(|values| values.to_vec());
    let use_full_text = mode.uses_full_text();
    let use_vector = mode.uses_vector();
    let rows = client
        .query(
            "WITH candidate AS MATERIALIZED (
                SELECT ch.id AS chunk_id, ch.tsv, ch.search_config, ch.seq,
                       t.version_id, t.lang, t.authenticity,
                       v.validity, v.version_status, u.citation,
                       i.title AS instrument_title, j.code AS country
                FROM chunks ch
                JOIN unit_texts t          ON t.id = ch.unit_text_id
                JOIN legal_unit_versions v ON v.id = t.version_id
                JOIN legal_units u         ON u.id = v.legal_unit_id
                JOIN instruments i         ON i.id = u.instrument_id
                JOIN jurisdictions j       ON j.id = i.jurisdiction_id
                WHERE ($2::text IS NULL OR j.code = upper($2))
                  AND ($3::text IS NULL OR v.validity @> ($3::text)::date)
                  AND ($4::text[] IS NULL OR t.lang = ANY($4::text[]))
             ),
             fts AS (
                SELECT chunk_id,
                       row_number() OVER (ORDER BY rank_score DESC, chunk_id) AS rank,
                       rank_score
                FROM (
                    SELECT chunk_id,
                           ts_rank_cd(tsv, websearch_to_tsquery(search_config, $1), 32) AS rank_score
                    FROM candidate
                    WHERE $6 AND tsv @@ websearch_to_tsquery(search_config, $1)
                ) ranked_fts
                ORDER BY rank_score DESC
                LIMIT 50
             ),
             vec AS (
                SELECT chunk_id,
                       row_number() OVER (ORDER BY distance, chunk_id) AS rank,
                       distance
                FROM (
                    SELECT e.chunk_id, e.embedding <=> $5::text::halfvec AS distance
                    FROM embeddings e
                    JOIN candidate USING (chunk_id)
                    WHERE $7 AND e.model_id = 1
                    ORDER BY e.embedding <=> $5::text::halfvec
                    LIMIT 50
                ) ranked_vec
             ),
             scored AS (
                SELECT c.*,
                       (coalesce(1.0 / (60 + f.rank), 0) +
                        coalesce(1.0 / (60 + ve.rank), 0))::float8 AS score,
                       f.rank AS full_text_rank,
                       f.rank_score::float8 AS full_text_score,
                       coalesce(1.0 / (60 + f.rank), 0)::float8 AS full_text_contribution,
                       ve.rank AS vector_rank,
                       ve.distance::float8 AS vector_distance,
                       coalesce(1.0 / (60 + ve.rank), 0)::float8 AS vector_contribution
                FROM fts f
                FULL OUTER JOIN vec ve USING (chunk_id)
                JOIN candidate c USING (chunk_id)
             ),
             deduplicated AS (
                SELECT scored.*,
                       row_number() OVER (
                           PARTITION BY version_id, seq
                           ORDER BY score DESC, chunk_id
                       ) AS rendering_rank
                FROM scored
             )
             SELECT d.chunk_id::text, d.citation, ch.context_header, ch.content,
                    d.lang, d.authenticity, d.validity::text, d.version_status,
                    d.country, d.instrument_title, d.score,
                    d.full_text_rank, d.full_text_score, d.full_text_contribution,
                    d.vector_rank, d.vector_distance, d.vector_contribution
             FROM deduplicated d
             JOIN chunks ch ON ch.id = d.chunk_id
             WHERE d.rendering_rank = 1
             ORDER BY d.score DESC, d.chunk_id
             LIMIT $8",
            &[
                &query,
                &country,
                &as_of,
                &language_filter,
                &query_vector,
                &use_full_text,
                &use_vector,
                &limit,
            ],
        )
        .map_err(|e| e.to_string())?;

    Ok(json!({
        "query": query,
        "mode": mode.as_str(),
        "model_id": if use_vector { Some(1) } else { None },
        "ranking": if mode == SearchMode::Hybrid {
            "RRF(k=60) over full-text and BGE-M3 vector ranks"
        } else if mode == SearchMode::Vector {
            "BGE-M3 vector rank"
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
            "lang": r.get::<_, String>("lang"),
            "authenticity": r.get::<_, String>("authenticity"),
            "validity": r.get::<_, String>("validity"),
            "version_status": r.get::<_, String>("version_status"),
            "country": r.get::<_, String>("country"),
            "instrument_title": r.get::<_, Value>("instrument_title"),
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
                5,
            )
            .unwrap_or_else(|error| panic!("{} search failed: {error}", mode.as_str()));
            assert!(result["results"].is_array());
        }
    }
}
