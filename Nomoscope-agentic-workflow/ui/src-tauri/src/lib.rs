//! Tauri command layer for the EUROMOD parameter-review UI.
//!
//! Command pattern (from tauri_outdated_parameters_app): a single `payload`
//! JSON argument, deserialised into a typed struct, returning
//! `Result<serde_json::Value, String>` so the frontend gets either data or a
//! rejected promise with the error string.
//!
//! The UI is fully remote (ADR 0004): it spawns nothing and reads no data
//! directory. Its one credential is the analyst's Postgres login; everything
//! that needs a model or the internet is a row in `ops.jobs` (jobs.rs) that
//! the worker picks up. The only file it ever writes is the EUROMOD export.

mod db;
mod golden;
mod jobs;
mod store;

use golden::GoldenVerifyPayload;
use jobs::{EncodePayload, EventsPayload, JobPayload, ListPayload, SubmitPayload};

use serde::Deserialize;
use serde_json::{json, Value};

#[derive(Deserialize)]
struct DecisionPayload {
    db_url: String,
    item_id: String,
    action: String,
    /// Shown in the item's own `decision` block; the audit row is stamped with
    /// the server's `current_user` regardless.
    reviewer: Option<String>,
    note: Option<String>,
    edited_value: Option<Value>,
    /// Patch of the other reviewer-editable proposal fields (validity dates,
    /// legal/source status, references). `None` = leave them as proposed.
    edited_fields: Option<Value>,
}

#[derive(Deserialize)]
struct DecisionsPayload {
    db_url: String,
    limit: Option<usize>,
}

#[derive(Deserialize)]
struct DbPayload {
    db_url: String,
}

#[derive(Deserialize)]
struct ChunkPayload {
    db_url: String,
    chunk_id: String,
}

#[derive(Deserialize)]
struct EvalRunPayload {
    db_url: String,
    run_pk: i64,
}

#[derive(Deserialize)]
struct InstrumentSearchPayload {
    db_url: String,
    country: String,
    query: String,
    limit: Option<i64>,
}

#[derive(Deserialize)]
struct SearchPayload {
    db_url: String,
    query: String,
    country: Option<String>,
    as_of: Option<String>,
    languages: Option<Vec<String>>,
    mode: Option<String>,
    limit: Option<i64>,
}

#[derive(Deserialize)]
struct SentenceScorePayload {
    db_url: String,
    query: String,
    sentences: Vec<String>,
}

async fn blocking<T, F>(f: F) -> Result<T, String>
where
    T: Send + 'static,
    F: FnOnce() -> Result<T, String> + Send + 'static,
{
    tauri::async_runtime::spawn_blocking(f)
        .await
        .map_err(|e| e.to_string())?
}

/// Connection settings plus the reviewer identity, which is the database's
/// `current_user` (the per-analyst login), never an environment guess.
#[tauri::command]
async fn get_env_config() -> Result<Value, String> {
    let db_url = std::env::var("WORKFLOW_DATABASE_URL")
        .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
    let phoenix_endpoint = std::env::var("PHOENIX_COLLECTOR_ENDPOINT")
        .unwrap_or_else(|_| "http://localhost:6006".to_string());
    // same default as the pipeline's config.py, so trace deep-links resolve
    let phoenix_project = std::env::var("PHOENIX_PROJECT_NAME")
        .unwrap_or_else(|_| "nomoscope-agentic-workflow".to_string());
    let url = db_url.clone();
    let reviewer = blocking(move || db::current_user(&url)).await;
    let (reviewer, db_error) = match reviewer {
        Ok(user) => (Some(user), None),
        Err(e) => (None, Some(e)),
    };
    Ok(json!({
        "reviewer": reviewer,
        "db_error": db_error,
        "db_url": db_url,
        "phoenix_endpoint": phoenix_endpoint.trim_end_matches('/'),
        "phoenix_project": phoenix_project,
    }))
}

#[tauri::command]
async fn golden_cases(payload: DbPayload) -> Result<Value, String> {
    blocking(move || golden::load_cases(&payload.db_url)).await
}

#[tauri::command]
async fn set_golden_verified(payload: GoldenVerifyPayload) -> Result<Value, String> {
    blocking(move || golden::set_verified(&payload)).await
}

#[tauri::command]
async fn load_queue(payload: DbPayload) -> Result<Value, String> {
    blocking(move || store::load_queue(&payload.db_url)).await
}

/// Record a reviewer decision: read the item, compute the decided item and
/// the audit entry, and hand both to `params.decide_review_item`, which
/// writes the audit row and the queue item in one transaction.
///
/// A refused decision (database unreachable, item vanished, schema missing)
/// therefore changes nothing: the item is still pending and the reviewer
/// takes it again. That is deliberate — a decision the audit log never
/// received must not look accepted in the UI.
#[tauri::command]
async fn save_decision(payload: DecisionPayload) -> Result<Value, String> {
    blocking(move || {
        let reviewer = payload.reviewer.clone().unwrap_or_else(|| "reviewer".to_string());
        let (item, entry) = store::prepare_decision(
            &payload.db_url,
            &payload.item_id,
            &payload.action,
            &reviewer,
            payload.note.as_deref(),
            payload.edited_value.as_ref(),
            payload.edited_fields.as_ref(),
        )?;
        let decision = store::commit_decision(&payload.db_url, &payload.item_id, &item, &entry).map_err(|e| {
            // The ways this fails look very different to a reviewer: a
            // stopped container, or a database that never had the params
            // schema applied (fresh stack / after `docker compose down -v`).
            let hint = if e.contains("decide_review_item") || e.contains("schema \"params\"") {
                "the params schema is missing or outdated — run `nomoscope-workflow init-param-db`"
            } else if e.contains("not in the queue") {
                "the item is no longer in the review queue — reload it"
            } else {
                "the database is unreachable — check it is running, then take the decision again"
            };
            format!("Decision not recorded, so nothing was changed: {hint}. ({e})")
        })?;
        Ok(json!({ "item": item, "decision": decision }))
    })
    .await
}

/// The audit log from params.review_decisions.
#[tauri::command]
async fn load_decisions(payload: DecisionsPayload) -> Result<Value, String> {
    let limit = payload.limit.unwrap_or(200);
    blocking(move || db::load_decisions(&payload.db_url, limit as i64)).await
}

/// Export accepted/edited items' Activity 1 records, one JSON file per
/// country, into a folder the reviewer picks. The only file the UI writes.
#[tauri::command]
async fn export_accepted(app_handle: tauri::AppHandle, payload: DbPayload) -> Result<Value, String> {
    use tauri_plugin_dialog::DialogExt;
    let groups = blocking(move || store::export_records(&payload.db_url)).await?;
    if groups.is_empty() {
        return Ok(json!({ "count": 0, "paths": [], "canceled": false }));
    }
    let count: usize = groups.values().map(Vec::len).sum();
    let picked = tauri::async_runtime::spawn_blocking(move || {
        app_handle
            .dialog()
            .file()
            .set_title("Export accepted records — choose a folder")
            .blocking_pick_folder()
    })
    .await
    .map_err(|e| e.to_string())?;
    let Some(folder) = picked else {
        return Ok(json!({ "count": count, "paths": [], "canceled": true }));
    };
    let dir = folder
        .into_path()
        .map_err(|e| format!("folder picker returned an unusable path: {e}"))?;
    let paths = blocking(move || store::write_export(&dir, &groups, &store::today())).await?;
    Ok(json!({ "count": count, "paths": paths, "canceled": false }))
}

#[tauri::command]
async fn db_stats(payload: DbPayload) -> Result<Value, String> {
    blocking(move || db::stats(&payload.db_url)).await
}

#[tauri::command]
async fn eval_runs(payload: DbPayload) -> Result<Value, String> {
    blocking(move || db::eval_runs(&payload.db_url)).await
}

#[tauri::command]
async fn eval_run_detail(payload: EvalRunPayload) -> Result<Value, String> {
    blocking(move || db::eval_run_detail(&payload.db_url, payload.run_pk)).await
}

/// Article search. Vector and hybrid modes need the query encoded by the
/// worker (an `encode` job); when no worker is alive the search degrades to
/// full-text and says so in `notice`, rather than failing.
#[tauri::command]
async fn search_articles(payload: SearchPayload) -> Result<Value, String> {
    blocking(move || {
        let mut mode = db::SearchMode::parse(payload.mode.as_deref().unwrap_or("hybrid"))?;
        let mut notice: Option<String> = None;
        let query_vector = if mode.uses_vector() {
            match jobs::encode_query(&EncodePayload {
                db_url: payload.db_url.clone(),
                query: payload.query.clone(),
                sentences: None,
            }) {
                Ok(result) => Some(
                    result
                        .get("halfvec")
                        .and_then(Value::as_str)
                        .filter(|v| v.starts_with('[') && v.ends_with(']'))
                        .ok_or("encode job returned no halfvec")?
                        .to_string(),
                ),
                Err(e) if e == jobs::NO_WORKER => {
                    notice = Some(format!("{e}; showing full-text results instead"));
                    mode = db::SearchMode::FullText;
                    None
                }
                Err(e) => return Err(e),
            }
        } else {
            None
        };
        let mut result = db::search_articles(
            &payload.db_url,
            &payload.query,
            payload.country.as_deref(),
            payload.as_of.as_deref(),
            payload.languages.as_deref(),
            mode,
            query_vector.as_deref(),
            payload.limit.unwrap_or(25),
        )?;
        result["notice"] = json!(notice);
        Ok(result)
    })
    .await
}

/// Cosine of each sentence against the query, one BGE-M3 batch on the
/// worker. The Database tab uses it to tint, inside a hit, the sentence that
/// most likely answers.
#[tauri::command]
async fn score_sentences(payload: SentenceScorePayload) -> Result<Vec<f64>, String> {
    if payload.sentences.is_empty() {
        return Ok(Vec::new());
    }
    let expected = payload.sentences.len();
    blocking(move || {
        let result = jobs::encode_query(&EncodePayload {
            db_url: payload.db_url,
            query: payload.query,
            sentences: Some(payload.sentences),
        })?;
        let similarities = result
            .get("similarities")
            .and_then(Value::as_array)
            .ok_or("encode job returned no similarities")?;
        if similarities.len() != expected {
            return Err(format!(
                "encode job returned {} similarities for {expected} sentences",
                similarities.len()
            ));
        }
        similarities
            .iter()
            .map(|v| v.as_f64().ok_or_else(|| "encode job returned a non-numeric similarity".to_string()))
            .collect()
    })
    .await
}

#[tauri::command]
async fn search_instruments(payload: InstrumentSearchPayload) -> Result<Value, String> {
    blocking(move || {
        db::search_instruments(
            &payload.db_url,
            &payload.country,
            &payload.query,
            payload.limit.unwrap_or(20),
        )
    })
    .await
}

#[tauri::command]
async fn params_list(payload: DbPayload) -> Result<Value, String> {
    blocking(move || db::params_list(&payload.db_url)).await
}

#[tauri::command]
async fn chunk_renderings(payload: ChunkPayload) -> Result<Value, String> {
    blocking(move || db::chunk_renderings(&payload.db_url, &payload.chunk_id)).await
}

#[tauri::command]
async fn phoenix_projects(payload: DbPayload) -> Result<Value, String> {
    blocking(move || db::phoenix_projects(&payload.db_url)).await
}

// ---------------------------------------------------------------- jobs ----

#[tauri::command]
async fn submit_job(payload: SubmitPayload) -> Result<Value, String> {
    blocking(move || jobs::submit_job(&payload)).await
}

#[tauri::command]
async fn job_status(payload: JobPayload) -> Result<Value, String> {
    blocking(move || jobs::job_status(&payload)).await
}

#[tauri::command]
async fn job_events(payload: EventsPayload) -> Result<Value, String> {
    blocking(move || jobs::job_events(&payload)).await
}

#[tauri::command]
async fn cancel_job(payload: JobPayload) -> Result<Value, String> {
    blocking(move || jobs::cancel_job(&payload)).await
}

#[tauri::command]
async fn list_jobs(payload: ListPayload) -> Result<Value, String> {
    blocking(move || jobs::list_jobs(&payload)).await
}

#[tauri::command]
async fn worker_status(payload: DbPayload) -> Result<Value, String> {
    blocking(move || jobs::worker_status(&payload.db_url)).await
}

#[tauri::command]
async fn encode_query(payload: EncodePayload) -> Result<Value, String> {
    blocking(move || jobs::encode_query(&payload)).await
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            get_env_config,
            load_queue,
            save_decision,
            load_decisions,
            export_accepted,
            db_stats,
            search_articles,
            score_sentences,
            search_instruments,
            eval_runs,
            eval_run_detail,
            golden_cases,
            set_golden_verified,
            params_list,
            chunk_renderings,
            phoenix_projects,
            submit_job,
            job_status,
            job_events,
            cancel_job,
            list_jobs,
            worker_status,
            encode_query,
        ])
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
