//! The `eval` schema (Nomokrisis-evaluation_pipeline/db/eval_schema.sql) for
//! the Evaluation tab: runs with whole-run KPI rates, and one run's breakdown
//! and case results. Read-only.

use crate::pg::{describe, rows_to_json};
use postgres::Client;
use serde_json::{json, Value};

/// All evaluation runs with whole-run KPI rates (averaged across languages).
/// Errors with a hint if `nomokrisis-eval init-db` has not been run yet.
pub fn eval_runs(client: &mut Client) -> Result<Value, String> {
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
        "runs": rows_to_json(&rows)?,
    }))
}

/// Per-(language, country) KPI breakdown plus all case results for one run.
pub fn eval_run_detail(client: &mut Client, run_pk: i64) -> Result<Value, String> {

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
        "summary": rows_to_json(&summary)?,
        "cases": rows_to_json(&cases)?,
    }))
}

#[cfg(test)]
mod tests {
    fn url() -> String {
        std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string())
    }

    /// Exercises the eval queries and row→JSON type mappings against the live
    /// stack; silently skipped when the DB is down or `init-db` hasn't run.
    #[test]
    fn eval_queries_smoke() {
        let Ok(mut client) = crate::pg::connect(&url()) else { return };
        let runs = match super::eval_runs(&mut client) {
            Ok(v) => v,
            Err(e) if e.contains("init-db") => return,
            Err(e) => panic!("eval_runs failed: {e}"),
        };
        if let Some(first) = runs["runs"].as_array().unwrap().first() {
            let pk = first["id"].as_i64().unwrap();
            let detail = super::eval_run_detail(&mut client, pk).unwrap();
            assert!(detail["summary"].is_array());
            assert!(detail["cases"].is_array());
        }
    }
}
