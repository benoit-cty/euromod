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

mod conversations;

use jobs::{EncodePayload, EventsPayload, JobPayload, SubmitPayload};

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

/// Direct article search, no LLM: the same SQL as the review UI's Database
/// tab. Hybrid and vector modes encode the query on the worker; with no
/// worker alive the search degrades to full text and says so in `notice`.
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
            payload.limit.unwrap_or(20),
        )?;
        result["notice"] = json!(notice);
        Ok(result)
    })
    .await
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
