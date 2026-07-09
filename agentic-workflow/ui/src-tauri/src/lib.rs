//! Tauri command layer for the EUROMOD parameter-review UI.
//!
//! Command pattern (from tauri_outdated_parameters_app): a single `payload`
//! JSON argument, deserialised into a typed struct, returning
//! `Result<serde_json::Value, String>` so the frontend gets either data or a
//! rejected promise with the error string.

mod db;
mod store;

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
    item_id: String,
    action: String,
    reviewer: String,
    note: Option<String>,
    edited_value: Option<Value>,
}

#[derive(Deserialize)]
struct DecisionsPayload {
    data_dir: String,
    limit: Option<usize>,
}

#[derive(Deserialize)]
struct DbPayload {
    db_url: String,
}

#[derive(Deserialize)]
struct SearchPayload {
    db_url: String,
    query: String,
    country: Option<String>,
    as_of: Option<String>,
    limit: Option<i64>,
}

/// Default data dir: $WORKFLOW_DATA_DIR, else the nearest `data/queue` or
/// `agentic-workflow/data` walking up from the current directory.
fn default_data_dir() -> Option<PathBuf> {
    if let Ok(dir) = std::env::var("WORKFLOW_DATA_DIR") {
        return Some(PathBuf::from(dir));
    }
    let cwd = std::env::current_dir().ok()?;
    for ancestor in cwd.ancestors() {
        for candidate in [ancestor.join("data"), ancestor.join("agentic-workflow").join("data")] {
            if candidate.join("queue").is_dir() || candidate.join("parameters").is_dir() {
                return Some(candidate);
            }
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
    Ok(json!({
        "data_dir": default_data_dir().map(|p| p.display().to_string()),
        "reviewer": reviewer,
        "db_url": db_url,
    }))
}

#[tauri::command]
fn load_queue(payload: DataDirPayload) -> Result<Value, String> {
    store::load_queue(Path::new(&payload.data_dir))
}

#[tauri::command]
fn save_decision(payload: DecisionPayload) -> Result<Value, String> {
    store::save_decision(
        Path::new(&payload.data_dir),
        &payload.item_id,
        &payload.action,
        &payload.reviewer,
        payload.note.as_deref(),
        payload.edited_value.as_ref(),
    )
}

#[tauri::command]
fn load_decisions(payload: DecisionsPayload) -> Result<Value, String> {
    let entries = store::load_decisions(Path::new(&payload.data_dir), payload.limit.unwrap_or(200))?;
    Ok(json!({ "decisions": entries }))
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
async fn search_articles(payload: SearchPayload) -> Result<Value, String> {
    tauri::async_runtime::spawn_blocking(move || {
        db::search_articles(
            &payload.db_url,
            &payload.query,
            payload.country.as_deref(),
            payload.as_of.as_deref(),
            payload.limit.unwrap_or(25),
        )
    })
    .await
    .map_err(|e| e.to_string())?
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
        .invoke_handler(tauri::generate_handler![
            get_env_config,
            load_queue,
            save_decision,
            load_decisions,
            export_accepted,
            pick_data_dir,
            db_stats,
            search_articles,
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
