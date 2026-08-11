//! Golden-set review: the human gate on drafted evaluation ground truth.
//!
//! Cases live one-JSON-per-file under
//! Nomokrisis-evaluation_pipeline/dataset/<country>/, drafted by
//! `nomokrisis-eval build-openfisca-dataset` with `verified: false`. This
//! module reads them, pairs each with the parameter record it will run against
//! (so the reviewer sees the drafted value next to the value EUROMOD holds
//! today), and writes the reviewer's verdict back into the same file.
//!
//! Cases stay loosely typed (serde_json::Value) for the same reason queue items
//! do: the dataset schema evolves in the Python package and the UI must not
//! need a lockstep release. Only the three review fields are ever written —
//! `verified`, `reviewed_by`, `review_note` — so a field this build has never
//! heard of survives a round trip untouched.

use serde::Deserialize;
use serde_json::{json, Value};
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
pub struct GoldenPayload {
    pub dataset_dir: String,
}

#[derive(Deserialize)]
pub struct GoldenVerifyPayload {
    /// Absolute path of the case file, as returned by `load_cases`.
    pub path: String,
    pub verified: bool,
    pub reviewer: String,
    pub note: Option<String>,
}

fn read_json(path: &Path) -> Result<Value, String> {
    let text = fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
    serde_json::from_str(&text).map_err(|e| format!("{}: {e}", path.display()))
}

fn write_json(path: &Path, value: &Value) -> Result<(), String> {
    let text = serde_json::to_string_pretty(value).map_err(|e| e.to_string())?;
    fs::write(path, text + "\n").map_err(|e| format!("{}: {e}", path.display()))
}

/// Repo root for resolving a case's `parameter_file`, which is stored relative
/// to it. Walk up from the dataset directory looking for the sibling packages.
fn repo_root(dataset_dir: &Path) -> Option<PathBuf> {
    dataset_dir
        .ancestors()
        .find(|dir| dir.join("Nomoscope-agentic-workflow").is_dir())
        .map(Path::to_path_buf)
}

fn json_files(dir: &Path, out: &mut Vec<PathBuf>) {
    let Ok(entries) = fs::read_dir(dir) else { return };
    let mut paths: Vec<PathBuf> = entries.filter_map(|e| e.ok().map(|e| e.path())).collect();
    paths.sort();
    for path in paths {
        if path.is_dir() {
            json_files(&path, out);
        } else if path.extension().is_some_and(|ext| ext == "json") {
            out.push(path);
        }
    }
}

/// The parameter record's identity plus the value it holds at the case's
/// `as_of` — the "before" the drafted expectation is the "after" of.
fn parameter_summary(repo: Option<&PathBuf>, case: &Value) -> Value {
    let Some(relative) = case.get("parameter_file").and_then(Value::as_str) else {
        return Value::Null;
    };
    let Some(root) = repo else { return Value::Null };
    let Ok(record) = read_json(&root.join(relative)) else {
        return json!({ "missing": relative });
    };
    let info = record.get("information").cloned().unwrap_or(Value::Null);
    let as_of = case.get("as_of").and_then(Value::as_str).unwrap_or("");
    let current = record
        .get("values")
        .and_then(Value::as_array)
        .and_then(|values| {
            values.iter().find(|value| {
                let from = value.get("valid_from").and_then(Value::as_str).unwrap_or("");
                let to = value.get("valid_to").and_then(Value::as_str);
                from <= as_of && to.is_none_or(|to| to >= as_of)
            })
        })
        .cloned();
    json!({
        "model_target": info.get("model_target"),
        "label": info.get("label"),
        "short_label": info.get("short_label"),
        "description": info.get("description"),
        "unit": info.get("unit"),
        "temporal_basis": info.get("temporal_basis"),
        "current": current,
        "values": record.get("values").and_then(Value::as_array).map(Vec::len),
    })
}

pub fn load_cases(dataset_dir: &Path) -> Result<Value, String> {
    if !dataset_dir.is_dir() {
        return Err(format!("no golden dataset directory at {}", dataset_dir.display()));
    }
    let repo = repo_root(dataset_dir);
    let mut paths = Vec::new();
    json_files(dataset_dir, &mut paths);
    let mut cases = Vec::new();
    for path in paths {
        let mut case = read_json(&path)?;
        let summary = parameter_summary(repo.as_ref(), &case);
        if let Some(object) = case.as_object_mut() {
            object.insert("_path".into(), json!(path.display().to_string()));
            object.insert("_parameter".into(), summary);
        }
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
    Ok(json!({
        "cases": cases,
        "dataset_dir": dataset_dir.display().to_string(),
        "reviewed": reviewed,
        "verified": verified,
    }))
}

/// Record a verdict on one drafted case. Accepting sets `verified: true`;
/// rejecting leaves it false but stamps `reviewed_by`, so an evaluation run
/// (verified-only by default) skips it either way while the audit trail keeps
/// "a human said no" distinct from "nobody has looked".
pub fn set_verified(payload: &GoldenVerifyPayload) -> Result<Value, String> {
    let path = PathBuf::from(&payload.path);
    let mut case = read_json(&path)?;
    let object = case
        .as_object_mut()
        .ok_or_else(|| format!("{}: not a JSON object", path.display()))?;
    object.insert("verified".into(), json!(payload.verified));
    object.insert("reviewed_by".into(), json!(payload.reviewer));
    match payload.note.as_deref().map(str::trim).filter(|n| !n.is_empty()) {
        Some(note) => object.insert("review_note".into(), json!(note)),
        None => object.remove("review_note"),
    };
    write_json(&path, &case)?;
    if let Some(object) = case.as_object_mut() {
        object.insert("_path".into(), json!(path.display().to_string()));
    }
    Ok(json!({ "case": case }))
}

#[cfg(test)]
mod tests {
    use super::*;

    fn seed(dir: &Path) -> PathBuf {
        // A repo-shaped tree: the case's parameter_file is relative to the root
        // that holds both packages.
        let params = dir.join("Nomoscope-agentic-workflow/data/parameters");
        let dataset = dir.join("Nomokrisis-evaluation_pipeline/dataset/fr");
        fs::create_dir_all(&params).unwrap();
        fs::create_dir_all(&dataset).unwrap();
        write_json(
            &params.join("fr_test.json"),
            &json!({
                "information": {
                    "model_target": "euromod://FR/tin_fr/def_const/$test",
                    "unit": "/1",
                    "temporal_basis": "income_year",
                    "label": { "en": "Test rate" }
                },
                "values": [
                    { "value": 0.1, "valid_from": "2024-01-01", "valid_to": "2024-12-31" },
                    { "value": 0.2, "valid_from": "2025-01-01", "valid_to": null }
                ]
            }),
        )
        .unwrap();
        write_json(
            &dataset.join("fr_test_2025-06-01.json"),
            &json!({
                "id": "fr_test_2025-06-01",
                "country": "FR",
                "language": "fr",
                "parameter_file": "Nomoscope-agentic-workflow/data/parameters/fr_test.json",
                "as_of": "2025-06-01",
                "expected": { "routing": "changed", "value": 0.25 },
                "verified": false,
                "drafted_by": "openfisca@abc1234"
            }),
        )
        .unwrap();
        dataset.parent().unwrap().to_path_buf()
    }

    #[test]
    fn loads_cases_with_the_parameter_value_in_force() {
        let tmp = std::env::temp_dir().join(format!("golden-load-{}", std::process::id()));
        let _ = fs::remove_dir_all(&tmp);
        let dataset_dir = seed(&tmp);
        let result = load_cases(&dataset_dir).unwrap();
        let cases = result["cases"].as_array().unwrap();
        assert_eq!(cases.len(), 1);
        let case = &cases[0];
        assert!(case["_path"].as_str().unwrap().ends_with("fr_test_2025-06-01.json"));
        // The value in force at as_of, not the first or the last on record.
        assert_eq!(case["_parameter"]["current"]["value"], json!(0.2));
        assert_eq!(case["_parameter"]["temporal_basis"], json!("income_year"));
        assert_eq!(result["verified"], json!(0));
        fs::remove_dir_all(&tmp).unwrap();
    }

    #[test]
    fn accept_and_reject_are_distinguishable_and_lossless() {
        let tmp = std::env::temp_dir().join(format!("golden-verdict-{}", std::process::id()));
        let _ = fs::remove_dir_all(&tmp);
        let dataset_dir = seed(&tmp);
        let path = dataset_dir
            .join("fr")
            .join("fr_test_2025-06-01.json")
            .display()
            .to_string();

        let rejected = set_verified(&GoldenVerifyPayload {
            path: path.clone(),
            verified: false,
            reviewer: "ben".into(),
            note: Some("threshold looks like the previous year".into()),
        })
        .unwrap();
        assert_eq!(rejected["case"]["verified"], json!(false));
        assert_eq!(rejected["case"]["reviewed_by"], json!("ben"));
        // Rejected is not the same as unreviewed, and nothing else is touched.
        assert_eq!(rejected["case"]["drafted_by"], json!("openfisca@abc1234"));
        assert_eq!(rejected["case"]["expected"]["value"], json!(0.25));

        let accepted = set_verified(&GoldenVerifyPayload {
            path,
            verified: true,
            reviewer: "ben".into(),
            note: None,
        })
        .unwrap();
        assert_eq!(accepted["case"]["verified"], json!(true));
        // An emptied note is cleared, not left stale from the previous verdict.
        assert!(accepted["case"].get("review_note").is_none());
        assert_eq!(load_cases(&dataset_dir).unwrap()["verified"], json!(1));
        fs::remove_dir_all(&tmp).unwrap();
    }
}
