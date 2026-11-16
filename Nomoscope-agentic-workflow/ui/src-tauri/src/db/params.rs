//! The `params` schema (pipeline/db/params_schema.sql), read side: every
//! parameter with its latest value and run (Parameters tab), one parameter's
//! texts and history (the review page's hand-off prompt), its metadata edits,
//! and the decision audit log. Decisions are written only by
//! `params.decide_review_item` and edits only by `params.edit_parameter`
//! (store.rs); this module never writes.

use crate::pg::{connect, describe};
use serde_json::{json, Value};

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

/// The audit log (`params.review_decisions`, the system of record), newest
/// first: the History tab's data source.
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
