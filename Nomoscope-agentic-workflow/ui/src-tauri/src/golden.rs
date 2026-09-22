//! Golden-set review: the human gate on drafted evaluation ground truth.
//!
//! Cases are rows in `eval.golden_cases` (ADR 0004): the GoldenCase in the
//! `case` column, the verdict in its own columns (`verified`, `reviewed_by`,
//! `reviewed_at`, `review_note`) so the reviewer role can be granted UPDATE
//! on exactly those. Loading merges the two into the one object the Golden
//! tab has always shown, and pairs each case with the parameter record it will
//! run against (from the params DB) so the reviewer sees the drafted value
//! next to the value EUROMOD holds.
//!
//! Cases stay loosely typed (serde_json::Value) for the same reason queue items
//! do: the dataset schema evolves in the Python package and the UI must not
//! need a lockstep release.

use postgres::{Client, NoTls};
use serde::Deserialize;
use serde_json::{json, Value};

#[derive(Deserialize)]
pub struct GoldenVerifyPayload {
    pub db_url: String,
    pub id: String,
    pub verified: bool,
    pub note: Option<String>,
}

fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {e}"))
}

/// One case object from a row: the stored `case` with the identity and
/// verdict columns laid over it (the columns win — they are what the eval
/// run and the reviewer grant key on).
pub fn merge_case(case: Value, id: &str, country: &str, language: &str, as_of: &str, verified: bool,
    reviewed_by: Option<&str>, reviewed_at: Option<&str>, review_note: Option<&str>) -> Value {
    let mut merged = if case.is_object() { case } else { json!({}) };
    merged["id"] = json!(id);
    merged["country"] = json!(country);
    merged["language"] = json!(language);
    merged["as_of"] = json!(as_of);
    merged["verified"] = json!(verified);
    merged["reviewed_by"] = json!(reviewed_by);
    merged["reviewed_at"] = json!(reviewed_at);
    match review_note.map(str::trim).filter(|n| !n.is_empty()) {
        Some(note) => merged["review_note"] = json!(note),
        None => {
            merged.as_object_mut().map(|o| o.remove("review_note"));
        }
    }
    merged
}

const CASE_COLUMNS: &str = "id, country, language, as_of::text AS as_of, \"case\", verified,
        reviewed_by, reviewed_at::text AS reviewed_at, review_note";

fn case_row(r: &postgres::Row) -> Value {
    merge_case(
        r.get("case"),
        &r.get::<_, String>("id"),
        &r.get::<_, String>("country"),
        &r.get::<_, String>("language"),
        &r.get::<_, String>("as_of"),
        r.get("verified"),
        r.get::<_, Option<String>>("reviewed_by").as_deref(),
        r.get::<_, Option<String>>("reviewed_at").as_deref(),
        r.get::<_, Option<String>>("review_note").as_deref(),
    )
}

/// The parameter record's identity plus the value it holds at the case's
/// `as_of` — the "before" the drafted expectation is the "after" of. Same
/// columns the Parameters tab lists (db.rs::params_list), but the value in
/// force at `as_of` rather than the newest. A `group:<id>` target has no
/// single parameter row: it is reported as such.
fn parameter_summary(client: &mut Client, case: &Value) -> Result<Value, String> {
    let Some(target) = case.get("parameter_target").and_then(Value::as_str) else {
        return Ok(Value::Null);
    };
    if let Some(group) = target.strip_prefix("group:") {
        return Ok(json!({ "group": group, "model_target": target }));
    }
    let as_of = case.get("as_of").and_then(Value::as_str).unwrap_or("");
    let params_schema: bool = client
        .query_one("SELECT to_regclass('params.parameters') IS NOT NULL", &[])
        .map_err(|e| e.to_string())?
        .get(0);
    if !params_schema {
        return Ok(json!({ "missing": target }));
    }
    let row = client
        .query_opt(
            "SELECT p.model_target, p.label, p.short_label, p.description, p.unit,
                    p.temporal_basis,
                    (SELECT count(*) FROM params.model_values v WHERE v.parameter_id = p.id) AS values,
                    mv.value_raw, mv.raw_euromod_value, mv.system_year,
                    mv.valid_from::text AS valid_from, mv.valid_to::text AS valid_to,
                    mv.source_type
             FROM params.parameters p
             LEFT JOIN LATERAL (
                 SELECT * FROM params.model_values v
                 WHERE v.parameter_id = p.id
                   AND ($2::text = '' OR (v.valid_from <= $2::text::date
                        AND (v.valid_to IS NULL OR v.valid_to >= $2::text::date)))
                 ORDER BY v.valid_from DESC LIMIT 1
             ) mv ON true
             WHERE p.model_target = $1",
            &[&target, &as_of],
        )
        .map_err(|e| format!("parameter lookup failed: {e}"))?;
    let Some(r) = row else {
        return Ok(json!({ "missing": target }));
    };
    let current = r.get::<_, Option<Value>>("value_raw").map(|value| {
        json!({
            "value": value,
            "raw_euromod_value": r.get::<_, Option<String>>("raw_euromod_value"),
            "system_year": r.get::<_, Option<i32>>("system_year"),
            "valid_from": r.get::<_, Option<String>>("valid_from"),
            "valid_to": r.get::<_, Option<String>>("valid_to"),
            "source_type": r.get::<_, Option<String>>("source_type"),
        })
    });
    Ok(json!({
        "model_target": r.get::<_, String>("model_target"),
        "label": r.get::<_, Option<Value>>("label"),
        "short_label": r.get::<_, Option<Value>>("short_label"),
        "description": r.get::<_, Option<Value>>("description"),
        "unit": r.get::<_, Option<String>>("unit"),
        "temporal_basis": r.get::<_, Option<String>>("temporal_basis"),
        "current": current,
        "values": r.get::<_, i64>("values"),
    }))
}

pub fn load_cases(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            &format!("SELECT {CASE_COLUMNS} FROM eval.golden_cases ORDER BY country, id"),
            &[],
        )
        .map_err(|e| format!("golden cases query failed (has `nomokrisis-eval init-db` been run?): {e}"))?;
    let mut cases = Vec::with_capacity(rows.len());
    for r in &rows {
        let mut case = case_row(r);
        let summary = parameter_summary(&mut client, &case)?;
        case["_parameter"] = summary;
        cases.push(case);
    }
    let reviewed = cases
        .iter()
        .filter(|c| c.get("reviewed_by").is_some_and(|v| !v.is_null()))
        .count();
    let verified = cases
        .iter()
        .filter(|c| c.get("verified").and_then(Value::as_bool).unwrap_or(false))
        .count();
    Ok(json!({ "cases": cases, "reviewed": reviewed, "verified": verified }))
}

/// Record a verdict on one drafted case. Accepting sets `verified`;
/// rejecting leaves it false but stamps `reviewed_by` (always `current_user`),
/// so an evaluation run (verified-only by default) skips it either way while
/// the audit trail keeps "a human said no" distinct from "nobody has looked".
pub fn set_verified(payload: &GoldenVerifyPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let note = payload.note.as_deref().map(str::trim).filter(|n| !n.is_empty());
    let row = client
        .query_opt(
            &format!(
                "UPDATE eval.golden_cases
                    SET verified = $2, reviewed_by = current_user, reviewed_at = now(),
                        review_note = $3, updated_at = now()
                  WHERE id = $1
              RETURNING {CASE_COLUMNS}"
            ),
            &[&payload.id, &payload.verified, &note],
        )
        .map_err(|e| format!("golden verdict refused: {e}"))?
        .ok_or_else(|| format!("golden case {} does not exist", payload.id))?;
    Ok(json!({ "case": case_row(&row) }))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn merge_lays_the_verdict_columns_over_the_case() {
        let case = json!({
            "id": "stale", "expected": { "routing": "changed", "value": 0.25 },
            "drafted_by": "openfisca@abc1234", "review_note": "old"
        });
        let merged = merge_case(case, "fr_x_2025", "FR", "fr", "2025-06-01", false, Some("ben"), Some("2026-09-22 10:00:00+00"), None);
        assert_eq!(merged["id"], "fr_x_2025");
        assert_eq!(merged["as_of"], "2025-06-01");
        assert_eq!(merged["verified"], false);
        assert_eq!(merged["reviewed_by"], "ben");
        // an emptied note is cleared, not left stale from the previous verdict
        assert!(merged.get("review_note").is_none());
        // nothing else is touched
        assert_eq!(merged["expected"]["value"], json!(0.25));
        assert_eq!(merged["drafted_by"], "openfisca@abc1234");
    }

    /// Verdicts against the live stack: a `zz_` case is drafted, rejected,
    /// then accepted; reviewed_by is the server's current_user. Skipped when
    /// the DB is down or the eval schema lacks the table.
    #[test]
    fn verdict_round_trip_smoke() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let Ok(mut client) = connect(&url) else { return };
        if client.execute("SELECT 1 FROM eval.golden_cases LIMIT 0", &[]).is_err() {
            return; // `nomokrisis-eval init-db` not run (or old schema)
        }
        let id = "zz_golden_verdict_round_trip";
        let cleanup = |client: &mut Client| {
            client.execute("DELETE FROM eval.golden_cases WHERE id = $1", &[&id]).unwrap();
        };
        cleanup(&mut client);
        let case = json!({
            "parameter_target": "euromod://ZZ/none/def_const/$missing",
            "expected": { "routing": "changed", "value": 0.25 },
            "drafted_by": "cargo-test"
        });
        client
            .execute(
                "INSERT INTO eval.golden_cases (id, country, language, as_of, \"case\")
                 VALUES ($1, 'ZZ', 'zz', '2025-06-01', $2)",
                &[&id, &case],
            )
            .unwrap();

        let loaded = load_cases(&url).unwrap();
        let mine = loaded["cases"].as_array().unwrap().iter().find(|c| c["id"] == id).unwrap();
        assert_eq!(mine["verified"], false);
        assert!(mine["reviewed_by"].is_null());
        assert_eq!(mine["_parameter"]["missing"], "euromod://ZZ/none/def_const/$missing");

        let rejected = set_verified(&GoldenVerifyPayload {
            db_url: url.clone(),
            id: id.into(),
            verified: false,
            note: Some("threshold looks like the previous year".into()),
        })
        .unwrap();
        assert_eq!(rejected["case"]["verified"], false);
        let me: String = client.query_one("SELECT current_user", &[]).unwrap().get(0);
        assert_eq!(rejected["case"]["reviewed_by"], json!(me));
        assert_eq!(rejected["case"]["review_note"], "threshold looks like the previous year");
        assert_eq!(rejected["case"]["expected"]["value"], json!(0.25));

        let accepted = set_verified(&GoldenVerifyPayload {
            db_url: url.clone(),
            id: id.into(),
            verified: true,
            note: Some("  ".into()),
        })
        .unwrap();
        assert_eq!(accepted["case"]["verified"], true);
        assert!(accepted["case"].get("review_note").is_none());
        let stored: Option<String> = client
            .query_one("SELECT review_note FROM eval.golden_cases WHERE id = $1", &[&id])
            .unwrap()
            .get(0);
        assert!(stored.is_none());

        // a group target is reported as such
        client
            .execute(
                "UPDATE eval.golden_cases SET \"case\" = jsonb_set(\"case\", '{parameter_target}', '\"group:FR:tinkt_fr:tin_schedule\"') WHERE id = $1",
                &[&id],
            )
            .unwrap();
        let loaded = load_cases(&url).unwrap();
        let mine = loaded["cases"].as_array().unwrap().iter().find(|c| c["id"] == id).unwrap();
        assert_eq!(mine["_parameter"]["group"], "FR:tinkt_fr:tin_schedule");

        let missing = set_verified(&GoldenVerifyPayload { db_url: url.clone(), id: "zz_nope".into(), verified: true, note: None })
            .unwrap_err();
        assert!(missing.contains("does not exist"));
        cleanup(&mut client);
    }
}
