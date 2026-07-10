//! File-backed review queue, decision log and export.
//!
//! Same layout as the Python side (pipeline/src/euromod_workflow/queue_store.py):
//!   <data>/queue/*.json    one ReviewItem per file
//!   <data>/decisions.jsonl append-only audit log
//!   <data>/export/*.json   accepted records, Activity 1 format
//!
//! Items stay loosely typed (serde_json::Value) so the queue schema can evolve
//! in the pipeline without lockstep releases of the UI.

use chrono::Utc;
use serde::Serialize;
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Serialize)]
pub struct Facets {
    pub countries: Vec<String>,
    pub routings: Vec<String>,
    pub statuses: Vec<String>,
    pub row_count: usize,
}

fn read_json(path: &Path) -> Result<Value, String> {
    let text = fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
    serde_json::from_str(&text).map_err(|e| format!("{}: {e}", path.display()))
}

fn write_json(path: &Path, value: &Value) -> Result<(), String> {
    let text = serde_json::to_string_pretty(value).map_err(|e| e.to_string())?;
    fs::write(path, text + "\n").map_err(|e| format!("{}: {e}", path.display()))
}

fn str_field(value: &Value, key: &str) -> String {
    value
        .get(key)
        .and_then(Value::as_str)
        .unwrap_or_default()
        .to_string()
}

pub fn load_queue(data_dir: &Path) -> Result<Value, String> {
    let queue = data_dir.join("queue");
    let mut items: Vec<Value> = Vec::new();
    if queue.is_dir() {
        let mut paths: Vec<PathBuf> = fs::read_dir(&queue)
            .map_err(|e| e.to_string())?
            .filter_map(|entry| entry.ok().map(|e| e.path()))
            .filter(|p| p.extension().is_some_and(|ext| ext == "json"))
            .collect();
        paths.sort();
        for path in paths {
            items.push(read_json(&path)?);
        }
    }
    items.sort_by_key(|item| std::cmp::Reverse(str_field(item, "created_at")));

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
    Ok(json!({ "items": items, "facets": facets, "data_dir": data_dir }))
}

/// Apply a reviewer decision: update the queue item, mirror the review fields
/// into the exported record's lineage, and append to the audit log.
pub fn save_decision(
    data_dir: &Path,
    item_id: &str,
    action: &str,
    reviewer: &str,
    note: Option<&str>,
    edited_value: Option<&Value>,
) -> Result<Value, String> {
    let review_status = match action {
        "accepted" | "edited" => "accepted",
        "rejected" => "rejected",
        "escalated" => "needs_revision",
        other => return Err(format!("unknown action: {other}")),
    };
    let path = data_dir.join("queue").join(format!("{item_id}.json"));
    let mut item = read_json(&path)?;
    let now = Utc::now().to_rfc3339();

    item["status"] = json!(action);
    item["decision"] = json!({
        "action": action,
        "reviewer": reviewer,
        "note": note,
        "decided_at": now,
    });
    if let Some(value) = edited_value {
        item["proposed_value"]["value"] = value.clone();
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
            if let Some(value) = edited_value {
                last["value"] = value.clone();
            }
            if let Some(lineage) = last.get_mut("lineage").filter(|l| !l.is_null()) {
                lineage["reviewed_by"] = json!(reviewer);
                lineage["review_status"] = json!(review_status);
                lineage["reviewed_at"] = json!(now);
                lineage["review_note"] = json!(note);
            }
        }
    }
    write_json(&path, &item)?;

    let log_entry = json!({
        "logged_at": now,
        "item_id": item_id,
        "action": action,
        "reviewer": reviewer,
        "note": note,
        "edited_value": edited_value,
        "routing": item.get("routing"),
        "model_target": item.get("model_target"),
        "as_of": item.get("as_of"),
        "run_id": item.get("run_id"),
        "confidence": item.pointer("/proposed_value/lineage/confidence"),
        "critique_verdict": item.pointer("/critique/verdict"),
    });
    append_decision(data_dir, &log_entry)?;
    Ok(item)
}

fn append_decision(data_dir: &Path, entry: &Value) -> Result<(), String> {
    use std::io::Write;
    let path = data_dir.join("decisions.jsonl");
    let mut file = fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(&path)
        .map_err(|e| format!("{}: {e}", path.display()))?;
    writeln!(file, "{entry}").map_err(|e| e.to_string())
}

pub fn load_decisions(data_dir: &Path, limit: usize) -> Result<Vec<Value>, String> {
    let path = data_dir.join("decisions.jsonl");
    if !path.exists() {
        return Ok(Vec::new());
    }
    let text = fs::read_to_string(&path).map_err(|e| e.to_string())?;
    let mut entries: Vec<Value> = text
        .lines()
        .filter(|line| !line.trim().is_empty())
        .filter_map(|line| serde_json::from_str(line).ok())
        .collect();
    entries.reverse();
    entries.truncate(limit);
    Ok(entries)
}

/// Export accepted/edited items' full Activity 1 records (write-back is export-first).
pub fn export_accepted(data_dir: &Path) -> Result<Value, String> {
    let out = data_dir.join("export");
    fs::create_dir_all(&out).map_err(|e| e.to_string())?;
    let queue = load_queue(data_dir)?;
    let mut written: Vec<String> = Vec::new();
    for item in queue["items"].as_array().unwrap_or(&Vec::new()) {
        let status = str_field(item, "status");
        if (status == "accepted" || status == "edited") && !item["proposed_record"].is_null() {
            let path = out.join(format!("{}.json", str_field(item, "id")));
            write_json(&path, &item["proposed_record"])?;
            written.push(path.display().to_string());
        }
    }
    Ok(json!({ "count": written.len(), "paths": written }))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn seed_item(dir: &Path) {
        let queue = dir.join("queue");
        fs::create_dir_all(&queue).unwrap();
        let item = json!({
            "id": "fr_test_2025-06-01",
            "created_at": "2026-07-09T00:00:00Z",
            "country": "FR",
            "routing": "changed",
            "status": "pending",
            "model_target": "euromod://FR/test",
            "as_of": "2025-06-01",
            "run_id": "run-1",
            "proposed_value": { "value": 0.2, "lineage": { "review_status": "pending", "confidence": 0.9 } },
            "proposed_record": { "information": {}, "values": [ { "value": 0.2, "lineage": { "review_status": "pending" } } ] },
            "critique": { "verdict": "pass" }
        });
        write_json(&queue.join("fr_test_2025-06-01.json"), &item).unwrap();
    }

    #[test]
    fn decision_roundtrip_and_export() {
        let dir = tempfile::tempdir().unwrap();
        seed_item(dir.path());

        let updated = save_decision(
            dir.path(),
            "fr_test_2025-06-01",
            "accepted",
            "ben",
            Some("looks right"),
            None,
        )
        .unwrap();
        assert_eq!(updated["status"], "accepted");
        assert_eq!(
            updated
                .pointer("/proposed_value/lineage/review_status")
                .unwrap(),
            "accepted"
        );
        assert_eq!(
            updated
                .pointer("/proposed_record/values/0/lineage/reviewed_by")
                .unwrap(),
            "ben"
        );

        let decisions = load_decisions(dir.path(), 10).unwrap();
        assert_eq!(decisions.len(), 1);
        assert_eq!(decisions[0]["action"], "accepted");

        let export = export_accepted(dir.path()).unwrap();
        assert_eq!(export["count"], 1);

        let queue = load_queue(dir.path()).unwrap();
        assert_eq!(queue["facets"]["row_count"], 1);
        assert_eq!(queue["items"][0]["status"], "accepted");
    }

    #[test]
    fn edited_value_replaces_proposal() {
        let dir = tempfile::tempdir().unwrap();
        seed_item(dir.path());
        let updated = save_decision(
            dir.path(),
            "fr_test_2025-06-01",
            "edited",
            "ben",
            None,
            Some(&json!(0.25)),
        )
        .unwrap();
        assert_eq!(
            updated.pointer("/proposed_value/value").unwrap(),
            &json!(0.25)
        );
        assert_eq!(
            updated.pointer("/proposed_record/values/0/value").unwrap(),
            &json!(0.25)
        );
        assert_eq!(
            updated
                .pointer("/proposed_value/lineage/review_status")
                .unwrap(),
            "accepted"
        );
    }
}
