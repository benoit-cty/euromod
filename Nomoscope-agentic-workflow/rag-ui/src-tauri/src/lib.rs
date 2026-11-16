//! Tauri command layer for the Nomoscope RAG chat.
//!
//! A deliberately small sibling of the review UI (`../ui`), under the same
//! rule (ADR 0004): it spawns nothing, holds no key and loads no model. Its
//! one credential is the analyst's Postgres login. A chat turn is a `chat`
//! job the worker answers (tools: legislation search, article read, official
//! web search); the direct search box reads the legislation DB like the
//! review UI's Database tab; ingesting an act found on the web is an
//! `ingest` job followed by an `embed` job, submitted by the analyst.
//!
//! The job channel and the article search are the review UI's own modules,
//! compiled in from `../ui/src-tauri/src` so the two apps cannot drift.

#[allow(dead_code)]
#[path = "../../../ui/src-tauri/src/db.rs"]
mod db;
#[allow(dead_code)]
#[path = "../../../ui/src-tauri/src/jobs.rs"]
mod jobs;
#[path = "../../../ui/src-tauri/src/pg.rs"]
mod pg;

mod conversations;

use jobs::{EventsPayload, JobPayload, SubmitPayload};

use serde::Deserialize;
use serde_json::{json, Value};

#[derive(Deserialize)]
struct DbPayload {
    db_url: String,
}

#[derive(Deserialize)]
struct ChunkPayload {
    db_url: String,
    chunk_id: String,
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

/// The database URL and the login it connects as (`current_user`).
#[tauri::command]
async fn get_env_config() -> Result<Value, String> {
    let db_url = std::env::var("WORKFLOW_DATABASE_URL")
        .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
    let url = db_url.clone();
    let user = blocking(move || db::current_user(&url)).await;
    let (user, db_error) = match user {
        Ok(user) => (Some(user), None),
        Err(e) => (None, Some(e)),
    };
    Ok(json!({ "user": user, "db_error": db_error, "db_url": db_url }))
}

/// Workers (alive or not) and the models they publish; the model picker
/// offers exactly that list.
#[tauri::command]
async fn worker_status(payload: DbPayload) -> Result<Value, String> {
    blocking(move || jobs::worker_status(&payload.db_url)).await
}

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
async fn list_conversations(payload: conversations::ListPayload) -> Result<Value, String> {
    blocking(move || conversations::list(&payload)).await
}

#[tauri::command]
async fn conversation_turns(payload: conversations::ConversationPayload) -> Result<Value, String> {
    blocking(move || conversations::turns(&payload)).await
}

/// Every language rendering of the version a chunk belongs to.
#[tauri::command]
async fn chunk_renderings(payload: ChunkPayload) -> Result<Value, String> {
    blocking(move || db::chunk_renderings(&payload.db_url, &payload.chunk_id)).await
}

/// Direct article search, no LLM: the review UI's own `db::search`.
#[tauri::command]
async fn search_articles(payload: db::SearchPayload) -> Result<Value, String> {
    blocking(move || db::search(&payload, 20)).await
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            get_env_config,
            worker_status,
            submit_job,
            job_status,
            job_events,
            cancel_job,
            list_conversations,
            conversation_turns,
            chunk_renderings,
            search_articles,
        ])
        .run(tauri::generate_context!())
        .expect("error while running the RAG chat");
}
