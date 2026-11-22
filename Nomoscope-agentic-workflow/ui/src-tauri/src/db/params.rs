//! The `params` schema (pipeline/db/params_schema.sql), read side: every
//! parameter with its latest value and run (Parameters tab), one parameter's
//! texts and history (the review page's hand-off prompt), its metadata edits,
//! and the decision audit log. Decisions are written only by
//! `params.decide_review_item` and edits only by `params.edit_parameter`
//! (store.rs); this module never writes.

use crate::pg::{describe, rows_to_json};
use postgres::Client;
use serde_json::{json, Value};

/// All parameters in the `params` schema, each with its most recent model
/// value and its most recent agentic extraction run (Parameters tab).
pub fn params_list(client: &mut Client) -> Result<Value, String> {
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
            format!(
                "params query failed (has `nomoscope-workflow ingest-params` been run?): {}",
                describe(e)
            )
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
        "parameters": rows_to_json(&rows)?,
    }))
}

/// What the review queue item does not carry about its parameter — its
/// EUROMOD texts, its law-language texts and the values EUROMOD has held —
/// for the hand-off prompt to an external assistant. A `group:<id>` target
/// returns every member of that bracket schedule, in schedule order.
pub fn parameter_context(client: &mut Client, model_target: &str) -> Result<Value, String> {
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
        "parameters": rows_to_json(&rows)?,
    }))
}

/// One parameter's metadata edits (`params.parameter_edits`), newest first.
pub fn parameter_edits(client: &mut Client, model_target: &str) -> Result<Value, String> {
    let rows = client
        .query(
            "SELECT id, field, value, previous, reviewer, note, edited_at::text AS edited_at
             FROM params.parameter_edits WHERE model_target = $1
             ORDER BY edited_at DESC, id DESC",
            &[&model_target],
        )
        .map_err(|e| {
            format!(
                "edit history query failed (run `nomoscope-workflow init-param-db`?): {}",
                describe(e)
            )
        })?;
    Ok(json!(rows_to_json(&rows)?))
}

/// The audit log (`params.review_decisions`, the system of record), newest
/// first: the History tab's data source.
pub fn load_decisions(client: &mut Client, limit: i64) -> Result<Value, String> {
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
        "decisions": rows_to_json(&rows)?,
    }))
}

#[cfg(test)]
mod tests {
    fn url() -> String {
        std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string())
    }

    /// The params reads' row→JSON mapping against the live stack; skipped
    /// when the database is down or the params schema is absent.
    #[test]
    fn params_reads_smoke() {
        let Ok(mut client) = crate::pg::connect(&url()) else {
            return;
        };
        if client
            .execute("SELECT 1 FROM params.review_decisions LIMIT 0", &[])
            .is_err()
        {
            return;
        }
        let listed = super::params_list(&mut client).unwrap();
        assert!(listed["system_years"].is_object());
        if let Some(first) = listed["parameters"].as_array().unwrap().first() {
            let target = first["model_target"].as_str().unwrap().to_string();
            assert!(
                super::parameter_context(&mut client, &target).unwrap()["parameters"].is_array()
            );
            assert!(super::parameter_edits(&mut client, &target)
                .unwrap()
                .is_array());
        }
        assert!(super::load_decisions(&mut client, 5).unwrap()["decisions"].is_array());
    }
}
