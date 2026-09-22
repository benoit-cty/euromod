//! The review queue as rows (`params.review_queue`, ADR 0004) and the
//! EUROMOD export, the only file the UI ever writes.
//!
//! A reviewer decision is computed here ([compute_decision], pure) and
//! recorded by ONE database call, `params.decide_review_item(item_id, item,
//! entry)`: the audit row in `params.review_decisions` and the updated queue
//! item land in the same transaction, and a decision the database refuses
//! changes nothing anywhere — the item stays pending and the reviewer takes it
//! again. There is no local mirror: `params.review_decisions` is the record.
//!
//! Items stay loosely typed (serde_json::Value) so the queue schema can evolve
//! in the pipeline without lockstep releases of the UI.

use chrono::Utc;
use postgres::{Client, NoTls};
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Serialize)]
pub struct Facets {
    pub countries: Vec<String>,
    pub routings: Vec<String>,
    pub statuses: Vec<String>,
    pub row_count: usize,
}

fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {e}"))
}

/// `postgres::Error` displays as a bare "db error"; the server's message (a
/// RAISE in decide_review_item, a missing relation) is what the reviewer needs.
fn describe(e: postgres::Error) -> String {
    match e.as_db_error() {
        Some(db) => format!("{}: {}", e, db.message()),
        None => e.to_string(),
    }
}

fn str_field(value: &Value, key: &str) -> String {
    value
        .get(key)
        .and_then(Value::as_str)
        .unwrap_or_default()
        .to_string()
}

/// Every queue item, newest first, with the filter facets the list offers.
pub fn load_queue(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT item_id, status, item FROM params.review_queue ORDER BY created_at DESC, item_id",
            &[],
        )
        .map_err(describe)
        .map_err(|e| {
            let hint = if e.contains("review_queue") {
                " (the params schema is missing or outdated — run `nomoscope-workflow init-param-db`)"
            } else {
                ""
            };
            format!("review queue query failed{hint}: {e}")
        })?;
    let items: Vec<Value> = rows
        .iter()
        .map(|r| {
            let mut item: Value = r.get("item");
            // The row is authoritative for identity and status: the worker
            // wrote the item, decide_review_item keeps both in step.
            if item.get("id").and_then(Value::as_str).is_none() {
                item["id"] = json!(r.get::<_, String>("item_id"));
            }
            item["status"] = json!(r.get::<_, String>("status"));
            item
        })
        .collect();
    Ok(queue_with_facets(items))
}

fn queue_with_facets(items: Vec<Value>) -> Value {
    let mut countries = BTreeSet::new();
    let mut routings = BTreeSet::new();
    let mut statuses = BTreeSet::new();
    for item in &items {
        countries.insert(str_field(item, "country"));
        routings.insert(str_field(item, "routing"));
        statuses.insert(str_field(item, "status"));
    }
    let facets = Facets {
        countries: countries.into_iter().collect(),
        routings: routings.into_iter().collect(),
        statuses: statuses.into_iter().collect(),
        row_count: items.len(),
    };
    json!({ "items": items, "facets": facets })
}

/// Patch one value envelope in place: the scalar/bracket value, then any other
/// reviewer-edited fields (valid_from, valid_to, legal_status, references, …).
fn apply_edits(target: &mut Value, edited_value: Option<&Value>, edited_fields: Option<&Value>) {
    if !target.is_object() {
        return;
    }
    if let Some(value) = edited_value {
        target["value"] = value.clone();
    }
    if let Some(Value::Object(fields)) = edited_fields {
        for (key, value) in fields {
            // lineage stays owned by the pipeline / the review bookkeeping below
            if key == "lineage" {
                continue;
            }
            target[key.as_str()] = value.clone();
        }
    }
}

/// Compute a reviewer decision over a queue item without touching anything:
/// the updated item (review fields mirrored into the exported record's
/// lineage) and the audit entry `params.decide_review_item` records.
///
/// `reviewer` only fills the item's own `decision` block for display; the
/// database stamps the audit row with `current_user` and ignores the entry's
/// `reviewer` key. Decided items stay editable — re-deciding overwrites the
/// item and appends a new audit entry.
pub fn compute_decision(
    mut item: Value,
    item_id: &str,
    action: &str,
    reviewer: &str,
    note: Option<&str>,
    edited_value: Option<&Value>,
    edited_fields: Option<&Value>,
) -> Result<(Value, Value), String> {
    let review_status = match action {
        "accepted" | "edited" => "accepted",
        "rejected" => "rejected",
        "escalated" => "needs_revision",
        other => return Err(format!("unknown action: {other}")),
    };
    let now = Utc::now().to_rfc3339();

    item["status"] = json!(action);
    item["decision"] = json!({
        "action": action,
        "reviewer": reviewer,
        "note": note,
        "decided_at": now,
    });
    if let Some(proposed) = item.get_mut("proposed_value") {
        apply_edits(proposed, edited_value, edited_fields);
    }
    if let Some(lineage) = item
        .get_mut("proposed_value")
        .and_then(|v| v.get_mut("lineage"))
        .filter(|l| !l.is_null())
    {
        lineage["reviewed_by"] = json!(reviewer);
        lineage["review_status"] = json!(review_status);
        lineage["reviewed_at"] = json!(now);
        lineage["review_note"] = json!(note);
    }
    // The exported record's last value is the proposed one: keep it in sync.
    if let Some(values) = item
        .get_mut("proposed_record")
        .and_then(|r| r.get_mut("values"))
        .and_then(Value::as_array_mut)
    {
        if let Some(last) = values.last_mut() {
            apply_edits(last, edited_value, edited_fields);
            if let Some(lineage) = last.get_mut("lineage").filter(|l| !l.is_null()) {
                lineage["reviewed_by"] = json!(reviewer);
                lineage["review_status"] = json!(review_status);
                lineage["reviewed_at"] = json!(now);
                lineage["review_note"] = json!(note);
            }
        }
    }
    let log_entry = json!({
        "logged_at": now,
        // decided_at is the (item, instant) dedupe key the DB replays on — it
        // must be the same instant that went into the item's decision block.
        "decided_at": now,
        "item_id": item_id,
        "action": action,
        "reviewer": reviewer,
        "note": note,
        "edited_value": edited_value,
        "edited_fields": edited_fields,
        "routing": item.get("routing"),
        "model_target": item.get("model_target"),
        "as_of": item.get("as_of"),
        "run_id": item.get("run_id"),
        "confidence": item.pointer("/proposed_value/lineage/confidence"),
        "critique_verdict": item.pointer("/critique/verdict"),
    });
    Ok((item, log_entry))
}

fn read_item(client: &mut Client, item_id: &str) -> Result<Value, String> {
    let row = client
        .query_opt("SELECT item FROM params.review_queue WHERE item_id = $1", &[&item_id])
        .map_err(|e| format!("review item read failed: {}", describe(e)))?
        .ok_or_else(|| format!("review item {item_id} is not in the queue"))?;
    Ok(row.get("item"))
}

/// Read the item from the queue and compute the decision ([compute_decision]).
#[allow(clippy::too_many_arguments)]
pub fn prepare_decision(
    db_url: &str,
    item_id: &str,
    action: &str,
    reviewer: &str,
    note: Option<&str>,
    edited_value: Option<&Value>,
    edited_fields: Option<&Value>,
) -> Result<(Value, Value), String> {
    let mut client = connect(db_url)?;
    let item = read_item(&mut client, item_id)?;
    compute_decision(item, item_id, action, reviewer, note, edited_value, edited_fields)
}

/// Record the decision: one call, one transaction, audit row + queue item.
/// Returns the audit row id, or null when that exact decision (item,
/// decided_at) was already recorded — a replay is a no-op.
pub fn commit_decision(db_url: &str, item_id: &str, item: &Value, entry: &Value) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let row = client
        .query_one(
            "SELECT params.decide_review_item($1, $2::jsonb, $3::jsonb)",
            &[&item_id, item, entry],
        )
        .map_err(|e| format!("decision refused: {}", describe(e)))?;
    let id: Option<i64> = row.get(0);
    Ok(json!({ "id": id }))
}

/// Accepted/edited items' Activity 1 records, grouped by country — what the
/// export writes (write-back is export-first: nothing touches EUROMOD files).
pub fn export_records(db_url: &str) -> Result<BTreeMap<String, Vec<Value>>, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT country, item -> 'proposed_record' AS record
             FROM params.review_queue
             WHERE status IN ('accepted', 'edited') AND item ? 'proposed_record'
             ORDER BY country, model_target, system_year, item_id",
            &[],
        )
        .map_err(|e| format!("export query failed: {}", describe(e)))?;
    let mut groups: BTreeMap<String, Vec<Value>> = BTreeMap::new();
    for r in &rows {
        let record: Value = r.get("record");
        if record.is_null() {
            continue;
        }
        groups.entry(r.get::<_, String>("country")).or_default().push(record);
    }
    Ok(groups)
}

/// Write `<CC>_accepted_<date>.json` per country into `dir`: one JSON array of
/// records each. Returns the paths written.
pub fn write_export(dir: &Path, groups: &BTreeMap<String, Vec<Value>>, date: &str) -> Result<Vec<String>, String> {
    let mut paths = Vec::new();
    for (country, records) in groups {
        let path: PathBuf = dir.join(format!("{country}_accepted_{date}.json"));
        let text = serde_json::to_string_pretty(&Value::Array(records.clone())).map_err(|e| e.to_string())?;
        fs::write(&path, text + "\n").map_err(|e| format!("{}: {e}", path.display()))?;
        paths.push(path.display().to_string());
    }
    Ok(paths)
}

pub fn today() -> String {
    Utc::now().format("%Y-%m-%d").to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn seed_item() -> Value {
        json!({
            "id": "fr_test_2025",
            "created_at": "2026-07-09T00:00:00Z",
            "country": "FR",
            "routing": "changed",
            "status": "pending",
            "model_target": "euromod://FR/test",
            "system_year": 2025,
            "as_of": "2025-06-01",
            "run_id": "run-1",
            "proposed_value": {
                "value": 0.2,
                "valid_from": "2025-01-01",
                "valid_to": null,
                "legal_status": null,
                "references": [],
                "lineage": { "review_status": "pending", "confidence": 0.9 }
            },
            "proposed_record": { "information": {}, "values": [ { "value": 0.2, "valid_from": "2025-01-01", "lineage": { "review_status": "pending" } } ] },
            "critique": { "verdict": "pass" }
        })
    }

    fn decide(
        item: Value,
        action: &str,
        note: Option<&str>,
        edited_value: Option<&Value>,
        edited_fields: Option<&Value>,
    ) -> (Value, Value) {
        compute_decision(item, "fr_test_2025", action, "ben", note, edited_value, edited_fields).unwrap()
    }

    #[test]
    fn decision_mirrors_review_into_item_and_entry() {
        let (updated, entry) = decide(seed_item(), "accepted", Some("looks right"), None, None);
        assert_eq!(updated["status"], "accepted");
        assert_eq!(updated["decision"]["reviewer"], "ben");
        assert_eq!(updated.pointer("/proposed_value/lineage/review_status").unwrap(), "accepted");
        assert_eq!(updated.pointer("/proposed_record/values/0/lineage/reviewed_by").unwrap(), "ben");
        // the entry carries the keys decide_review_item reads, keyed on the
        // same instant as the item's decision block
        assert_eq!(entry["action"], "accepted");
        assert_eq!(entry["item_id"], "fr_test_2025");
        assert_eq!(entry["decided_at"], updated["decision"]["decided_at"]);
        assert_eq!(entry["run_id"], "run-1");
        assert_eq!(entry["as_of"], "2025-06-01");
        assert_eq!(entry["confidence"], json!(0.9));
        assert_eq!(entry["critique_verdict"], "pass");
        assert_eq!(entry["note"], "looks right");
    }

    #[test]
    fn unknown_action_is_refused() {
        let error = compute_decision(seed_item(), "x", "maybe", "ben", None, None, None).unwrap_err();
        assert!(error.contains("maybe"));
    }

    #[test]
    fn edited_value_replaces_proposal() {
        let (updated, entry) = decide(seed_item(), "edited", None, Some(&json!(0.25)), None);
        assert_eq!(updated.pointer("/proposed_value/value").unwrap(), &json!(0.25));
        assert_eq!(updated.pointer("/proposed_record/values/0/value").unwrap(), &json!(0.25));
        assert_eq!(updated.pointer("/proposed_value/lineage/review_status").unwrap(), "accepted");
        assert_eq!(entry["edited_value"], json!(0.25));
    }

    #[test]
    fn edited_fields_patch_dates_and_references() {
        let fields = json!({
            "value": 0.3,
            "valid_from": "2026-01-01",
            "valid_to": "2026-12-31",
            "legal_status": "enacted_in_force",
            "references": [ { "title": "JORF, art. 1", "supporting_extract": "le taux est de 30 %" } ],
            "lineage": { "review_status": "spoofed" },
        });
        let (updated, _) = decide(seed_item(), "edited", None, Some(&json!(0.3)), Some(&fields));

        for base in ["/proposed_value", "/proposed_record/values/0"] {
            assert_eq!(updated.pointer(&format!("{base}/valid_from")).unwrap(), "2026-01-01");
            assert_eq!(updated.pointer(&format!("{base}/valid_to")).unwrap(), "2026-12-31");
            assert_eq!(updated.pointer(&format!("{base}/legal_status")).unwrap(), "enacted_in_force");
            assert_eq!(updated.pointer(&format!("{base}/references/0/title")).unwrap(), "JORF, art. 1");
            assert_eq!(updated.pointer(&format!("{base}/value")).unwrap(), &json!(0.3));
            // lineage is bookkeeping, never patched from the form
            assert_eq!(updated.pointer(&format!("{base}/lineage/review_status")).unwrap(), "accepted");
        }
    }

    #[test]
    fn decided_item_can_be_edited_again() {
        let (rejected, _) = decide(seed_item(), "rejected", None, None, None);
        let (updated, _) = decide(
            rejected,
            "edited",
            Some("second look"),
            Some(&json!(0.4)),
            Some(&json!({ "legal_status": "enacted_in_force" })),
        );
        assert_eq!(updated["status"], "edited");
        assert_eq!(updated.pointer("/proposed_value/value").unwrap(), &json!(0.4));
        assert_eq!(updated["decision"]["note"], "second look");
    }

    #[test]
    fn facets_come_from_the_items() {
        let mut second = seed_item();
        second["country"] = json!("ES");
        second["status"] = json!("accepted");
        let queue = queue_with_facets(vec![seed_item(), second]);
        assert_eq!(queue["facets"]["row_count"], 2);
        assert_eq!(queue["facets"]["countries"], json!(["ES", "FR"]));
        assert_eq!(queue["facets"]["statuses"], json!(["accepted", "pending"]));
    }

    #[test]
    fn export_writes_one_array_per_country() {
        let dir = tempfile::tempdir().unwrap();
        let mut groups: BTreeMap<String, Vec<Value>> = BTreeMap::new();
        groups.insert("FR".into(), vec![json!({ "information": { "country": "FR" } }), json!({ "b": 2 })]);
        groups.insert("ES".into(), vec![json!({ "information": { "country": "ES" } })]);
        let paths = write_export(dir.path(), &groups, "2026-09-22").unwrap();
        assert_eq!(paths.len(), 2);
        assert!(paths[0].ends_with("ES_accepted_2026-09-22.json"));
        let fr: Value = serde_json::from_str(&fs::read_to_string(dir.path().join("FR_accepted_2026-09-22.json")).unwrap()).unwrap();
        assert_eq!(fr.as_array().unwrap().len(), 2);
        assert_eq!(fr[0]["information"]["country"], "FR");
    }

    /// The decide path against the live stack: a `zz_` item goes into the
    /// queue, one call records the decision and updates the row, a replay of
    /// the same entry is a no-op. Skipped when the DB is down or the params
    /// schema does not yet have the queue table.
    #[test]
    fn decision_round_trip_smoke() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let Ok(mut client) = connect(&url) else { return };
        if client.execute("SELECT 1 FROM params.review_queue LIMIT 0", &[]).is_err() {
            return; // `nomoscope-workflow init-param-db` not run (or old schema)
        }
        let item_id = "zz_store_decision_round_trip";
        let cleanup = |client: &mut Client| {
            client.execute("DELETE FROM params.review_decisions WHERE item_id = $1", &[&item_id]).unwrap();
            client.execute("DELETE FROM params.review_queue WHERE item_id = $1", &[&item_id]).unwrap();
        };
        cleanup(&mut client);
        let mut seeded = seed_item();
        seeded["id"] = json!(item_id);
        seeded["country"] = json!("ZZ");
        client
            .execute(
                "INSERT INTO params.review_queue
                     (item_id, country, model_target, system_year, routing, status, run_id, created_at, item)
                 VALUES ($1, 'ZZ', 'euromod://ZZ/test', 2025, 'changed', 'pending', 'run-1', now(), $2)",
                &[&item_id, &seeded],
            )
            .unwrap();

        // the queue lists it, pending
        let queue = load_queue(&url).unwrap();
        let listed = queue["items"].as_array().unwrap().iter().find(|i| i["id"] == item_id).unwrap();
        assert_eq!(listed["status"], "pending");

        let (item, entry) =
            prepare_decision(&url, item_id, "edited", "cargo-test", Some("smoke"), Some(&json!(0.25)), None).unwrap();
        // nothing recorded yet
        let pending: String = client
            .query_one("SELECT status FROM params.review_queue WHERE item_id = $1", &[&item_id])
            .unwrap()
            .get(0);
        assert_eq!(pending, "pending");

        let first = commit_decision(&url, item_id, &item, &entry).unwrap();
        assert!(first["id"].is_i64(), "first decision writes an audit row: {first}");
        let again = commit_decision(&url, item_id, &item, &entry).unwrap();
        assert!(again["id"].is_null(), "replaying the same decision is a no-op");

        let row = client
            .query_one("SELECT status, item FROM params.review_queue WHERE item_id = $1", &[&item_id])
            .unwrap();
        assert_eq!(row.get::<_, String>("status"), "edited");
        let stored: Value = row.get("item");
        assert_eq!(stored.pointer("/proposed_value/value").unwrap(), &json!(0.25));

        let decisions = client
            .query(
                "SELECT action, reviewer, note, edited_value FROM params.review_decisions WHERE item_id = $1",
                &[&item_id],
            )
            .unwrap();
        assert_eq!(decisions.len(), 1);
        assert_eq!(decisions[0].get::<_, String>("action"), "edited");
        assert_eq!(decisions[0].get::<_, Option<String>>("note").as_deref(), Some("smoke"));
        // the server stamps current_user, whatever the entry said
        let me: String = client.query_one("SELECT current_user", &[]).unwrap().get(0);
        assert_eq!(decisions[0].get::<_, Option<String>>("reviewer").as_deref(), Some(me.as_str()));
        assert_eq!(decisions[0].get::<_, Option<Value>>("edited_value"), Some(json!(0.25)));

        // the export sees it, under its country
        let groups = export_records(&url).unwrap();
        assert!(groups.get("ZZ").is_some_and(|records| records.len() == 1));

        // a vanished item fails outright
        cleanup(&mut client);
        let error = commit_decision(&url, item_id, &item, &entry).unwrap_err();
        assert!(error.contains("not in the queue"), "{error}");
    }
}
