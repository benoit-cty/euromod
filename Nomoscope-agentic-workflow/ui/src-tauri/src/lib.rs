//! Tauri command layer for the EUROMOD parameter-review UI.
//!
//! Command pattern (from tauri_outdated_parameters_app): a single `payload`
//! JSON argument, deserialised into a typed struct, returning
//! `Result<serde_json::Value, String>` so the frontend gets either data or a
//! rejected promise with the error string.

mod db;
mod encoder;
mod golden;
mod ingest;
mod store;
mod workflow;

use encoder::EmbeddingState;
use golden::{GoldenPayload, GoldenVerifyPayload};
use ingest::{IngestPayload, IngestState};
use workflow::{ImpactPayload, WorkflowPayload, WorkflowState};

use serde::Deserialize;
use serde_json::{json, Value};
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
struct DataDirPayload {
    data_dir: String,
}

#[derive(Deserialize)]
struct DecisionPayload {
    data_dir: String,
    db_url: String,
    item_id: String,
    action: String,
    reviewer: String,
    note: Option<String>,
    edited_value: Option<Value>,
    /// Patch of the other reviewer-editable proposal fields (validity dates,
    /// legal/source status, references). `None` = leave them as proposed.
    edited_fields: Option<Value>,
}

#[derive(Deserialize)]
struct DecisionsPayload {
    data_dir: String,
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
struct SearchPayload {
    db_url: String,
    query: String,
    country: Option<String>,
    as_of: Option<String>,
    languages: Option<Vec<String>>,
    mode: Option<String>,
    limit: Option<i64>,
}

/// Default data dir: $WORKFLOW_DATA_DIR, else the nearest `data/queue` or
/// `Nomoscope-agentic-workflow/data` walking up from the current directory.
fn default_data_dir() -> Option<PathBuf> {
    if let Ok(dir) = std::env::var("WORKFLOW_DATA_DIR") {
        return Some(PathBuf::from(dir));
    }
    let cwd = std::env::current_dir().ok()?;
    for ancestor in cwd.ancestors() {
        for candidate in [ancestor.join("data"), ancestor.join("Nomoscope-agentic-workflow").join("data")] {
            if candidate.join("queue").is_dir() || candidate.join("parameters").is_dir() {
                return Some(candidate);
            }
        }
    }
    None
}

/// Default golden-set location: $EVAL_DATASET_DIR, else the eval package's
/// `dataset/` next to the workflow package (same walk as [default_data_dir]).
fn default_dataset_dir() -> Option<PathBuf> {
    if let Ok(dir) = std::env::var("EVAL_DATASET_DIR") {
        return Some(PathBuf::from(dir));
    }
    let cwd = std::env::current_dir().ok()?;
    for ancestor in cwd.ancestors() {
        let candidate = ancestor
            .join("Nomokrisis-evaluation_pipeline")
            .join("dataset");
        if candidate.is_dir() {
            return Some(candidate);
        }
    }
    None
}

#[tauri::command]
fn get_env_config() -> Result<Value, String> {
    let reviewer = std::env::var("REVIEWER")
        .or_else(|_| std::env::var("USER"))
        .or_else(|_| std::env::var("USERNAME"))
        .unwrap_or_else(|_| "reviewer".to_string());
    let db_url = std::env::var("WORKFLOW_DATABASE_URL")
        .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
    let phoenix_endpoint = std::env::var("PHOENIX_COLLECTOR_ENDPOINT")
        .unwrap_or_else(|_| "http://localhost:6006".to_string());
    // same default as the pipeline's config.py, so trace deep-links resolve
    let phoenix_project = std::env::var("PHOENIX_PROJECT_NAME")
        .unwrap_or_else(|_| "nomoscope-agentic-workflow".to_string());
    Ok(json!({
        "data_dir": default_data_dir().map(|p| p.display().to_string()),
        "dataset_dir": default_dataset_dir().map(|p| p.display().to_string()),
        "reviewer": reviewer,
        "db_url": db_url,
        "phoenix_endpoint": phoenix_endpoint.trim_end_matches('/'),
        "phoenix_project": phoenix_project,
    }))
}

#[tauri::command]
fn golden_cases(payload: GoldenPayload) -> Result<Value, String> {
    golden::load_cases(Path::new(&payload.dataset_dir))
}

#[tauri::command]
fn set_golden_verified(payload: GoldenVerifyPayload) -> Result<Value, String> {
    golden::set_verified(&payload)
}

#[tauri::command]
fn load_queue(payload: DataDirPayload) -> Result<Value, String> {
    store::load_queue(Path::new(&payload.data_dir))
}

/// Record a reviewer decision. params.review_decisions is the system of record,
/// so it commits first; the queue item and the decisions.jsonl mirror are
/// written only once it has accepted the entry.
///
/// An unreachable database therefore fails the whole decision, leaving the item
/// pending and nothing written to disk. That is deliberate: a decision the audit
/// log never received must not look accepted in the UI.
#[tauri::command]
async fn save_decision(payload: DecisionPayload) -> Result<Value, String> {
    let data_dir = PathBuf::from(&payload.data_dir);
    let (item, entry) = store::prepare_decision(
        &data_dir,
        &payload.item_id,
        &payload.action,
        &payload.reviewer,
        payload.note.as_deref(),
        payload.edited_value.as_ref(),
        payload.edited_fields.as_ref(),
    )?;

    let db_url = payload.db_url.clone();
    let for_db = entry.clone();
    let decision = tauri::async_runtime::spawn_blocking(move || db::insert_decision(&db_url, &for_db))
        .await
        .map_err(|e| e.to_string())?
        .map_err(|e| {
            // The two ways this fails look very different to a reviewer: a
            // stopped container, or a database that never had the params
            // schema applied (fresh stack / after `docker compose down -v`).
            let hint = if e.contains("params.review_decisions") || e.contains("schema \"params\"") {
                "the params schema is missing — run `nomoscope-workflow init-param-db`"
            } else {
                "the database is unreachable — check it is running, then take the decision again"
            };
            format!("Decision not recorded, so nothing was changed: the audit log lives in the database and {hint}. ({e})")
        })?;

    // Recorded in the audit log. A disk failure from here on leaves the queue
    // item stale rather than the decision lost, which is the safe direction.
    store::commit_decision(&data_dir, &payload.item_id, &item, &entry)?;
    Ok(json!({ "item": item, "decision": decision }))
}

/// The audit log from params.review_decisions, falling back to the local
/// mirror when the DB is unreachable (so the tab still shows this session's
/// decisions offline). `source` tells the UI which one it got.
#[tauri::command]
async fn load_decisions(payload: DecisionsPayload) -> Result<Value, String> {
    let limit = payload.limit.unwrap_or(200);
    let db_url = payload.db_url.clone();
    let from_db =
        tauri::async_runtime::spawn_blocking(move || db::load_decisions(&db_url, limit as i64))
            .await
            .map_err(|e| e.to_string())?;
    match from_db {
        Ok(mut value) => {
            value["source"] = json!("database");
            Ok(value)
        }
        Err(db_error) => {
            let entries = store::load_decisions(Path::new(&payload.data_dir), limit)?;
            Ok(json!({ "decisions": entries, "source": "file", "db_error": db_error }))
        }
    }
}

#[tauri::command]
fn export_accepted(payload: DataDirPayload) -> Result<Value, String> {
    store::export_accepted(Path::new(&payload.data_dir))
}

#[tauri::command]
async fn db_stats(payload: DbPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || db::stats(&payload.db_url))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn eval_runs(payload: DbPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || db::eval_runs(&payload.db_url))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn eval_run_detail(payload: EvalRunPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || db::eval_run_detail(&payload.db_url, payload.run_pk))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn search_articles(
    state: tauri::State<'_, EmbeddingState>,
    payload: SearchPayload,
) -> Result<Value, String> {
    let mode = db::SearchMode::parse(payload.mode.as_deref().unwrap_or("hybrid"))?;
    let query_vector = if mode.uses_vector() {
        Some(state.encode(&payload.query).await?)
    } else {
        None
    };
    tauri::async_runtime::spawn_blocking(move || {
        db::search_articles(
            &payload.db_url,
            &payload.query,
            payload.country.as_deref(),
            payload.as_of.as_deref(),
            payload.languages.as_deref(),
            mode,
            query_vector.as_deref(),
            payload.limit.unwrap_or(25),
        )
    })
    .await
    .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn params_list(payload: DbPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || db::params_list(&payload.db_url))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn chunk_renderings(payload: ChunkPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || {
        db::chunk_renderings(&payload.db_url, &payload.chunk_id)
    })
    .await
    .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn phoenix_projects(payload: DbPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || db::phoenix_projects(&payload.db_url))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn run_workflow(
    app: tauri::AppHandle,
    state: tauri::State<'_, WorkflowState>,
    payload: WorkflowPayload,
) -> Result<Value, String> {
    workflow::run(app, state, payload).await
}

#[tauri::command]
fn stop_workflow(state: tauri::State<'_, WorkflowState>, run_id: String) -> Result<Value, String> {
    workflow::stop(state, run_id)
}

#[tauri::command]
async fn impact_report(payload: ImpactPayload) -> Result<Value, String> {
    workflow::impact_report(payload).await
}

#[tauri::command]
async fn run_ingest(
    app: tauri::AppHandle,
    state: tauri::State<'_, IngestState>,
    payload: IngestPayload,
) -> Result<Value, String> {
    ingest::run(app, state, payload).await
}

#[tauri::command]
fn stop_ingest(state: tauri::State<'_, IngestState>, run_id: String) -> Result<Value, String> {
    ingest::stop(state, run_id)
}

#[tauri::command]
async fn pick_data_dir(app_handle: tauri::AppHandle) -> Result<Value, String> {
    use tauri_plugin_dialog::DialogExt;
    let (tx, rx) = tokio::sync::oneshot::channel();
    app_handle.dialog().file().pick_folder(move |folder| {
        let _ = tx.send(folder);
    });
    match rx.await.map_err(|e| e.to_string())? {
        Some(path) => Ok(json!({ "canceled": false, "path": path.to_string() })),
        None => Ok(json!({ "canceled": true })),
    }
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .manage(EmbeddingState::default())
        .manage(IngestState::default())
        .manage(WorkflowState::default())
        .invoke_handler(tauri::generate_handler![
            get_env_config,
            load_queue,
            save_decision,
            load_decisions,
            export_accepted,
            pick_data_dir,
            db_stats,
            search_articles,
            eval_runs,
            eval_run_detail,
            golden_cases,
            set_golden_verified,
            run_ingest,
            stop_ingest,
            params_list,
            chunk_renderings,
            phoenix_projects,
            run_workflow,
            stop_workflow,
            impact_report,
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
