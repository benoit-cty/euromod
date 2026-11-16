//! Tauri command layer for the Nomoscope RAG chat.
//!
//! A deliberately small sibling of the review UI (`../ui`), under the same
//! rule (ADR 0004): it spawns nothing, holds no key and loads no model. Its
//! one credential is the analyst's Postgres login, kept in Tauri state
//! ([pool::Db]) and never sent through the webview. A chat turn is a `chat`
//! job the worker answers (tools: legislation search, article read, official
//! web search); the direct search box reads the legislation DB like the
//! review UI's Database tab; ingesting an act found on the web is an
//! `ingest` job followed by an `embed` job, submitted by the analyst.
//!
//! The job channel, the connection pool and the article search are the
//! review UI's own modules, compiled in from `../ui/src-tauri/src` so the two
//! apps cannot drift. Only what the chat uses is compiled in: the search (not
//! the review UI's eval, params or Phoenix reads).

// The job channel is whole: the chat does not list jobs (`list_jobs`).
#[allow(dead_code)]
#[path = "../../../ui/src-tauri/src/jobs.rs"]
mod jobs;
#[path = "../../../ui/src-tauri/src/pg.rs"]
mod pg;
// The chat never changes its database (`set_url`), so the pool's setter is unused.
#[allow(dead_code)]
#[path = "../../../ui/src-tauri/src/pool.rs"]
mod pool;
#[path = "../../../ui/src-tauri/src/db/search.rs"]
mod search;

mod conversations;

use jobs::{EventsPayload, JobPayload, SubmitPayload};
use pool::Db;

use serde::Deserialize;
use serde_json::{json, Value};
use tauri::State;

#[derive(Deserialize)]
struct ChunkPayload {
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

/// Run `f` on a pooled connection of the app's database, off the async runtime.
async fn with_client<T, F>(db: State<'_, Db>, f: F) -> Result<T, String>
where
    T: Send + 'static,
    F: FnOnce(&mut postgres::Client) -> Result<T, String> + Send + 'static,
{
    let db = db.inner().clone();
    blocking(move || {
        let mut client = db.client()?;
        f(&mut client)
    })
    .await
}

/// The database (password masked) and the login it connects as (`current_user`).
#[tauri::command]
async fn get_env_config(db: State<'_, Db>) -> Result<Value, String> {
    let db_url = pool::redact(&db.url());
    let (user, db_error) = match with_client(db, |client| pg::current_user(client)).await {
        Ok(user) => (Some(user), None),
        Err(e) => (None, Some(e)),
    };
    Ok(json!({ "user": user, "db_error": db_error, "db_url": db_url }))
}

/// Workers (alive or not) and the models they publish; the model picker
/// offers exactly that list.
#[tauri::command]
async fn worker_status(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, jobs::worker_status).await
}

#[tauri::command]
async fn submit_job(db: State<'_, Db>, payload: SubmitPayload) -> Result<Value, String> {
    with_client(db, move |client| jobs::submit_job(client, &payload)).await
}

#[tauri::command]
async fn job_status(db: State<'_, Db>, payload: JobPayload) -> Result<Value, String> {
    with_client(db, move |client| jobs::job_status(client, &payload)).await
}

#[tauri::command]
async fn job_events(db: State<'_, Db>, payload: EventsPayload) -> Result<Value, String> {
    with_client(db, move |client| jobs::job_events(client, &payload)).await
}

#[tauri::command]
async fn cancel_job(db: State<'_, Db>, payload: JobPayload) -> Result<Value, String> {
    with_client(db, move |client| jobs::cancel_job(client, &payload)).await
}

#[tauri::command]
async fn list_conversations(db: State<'_, Db>, payload: conversations::ListPayload) -> Result<Value, String> {
    with_client(db, move |client| conversations::list(client, &payload)).await
}

#[tauri::command]
async fn conversation_turns(db: State<'_, Db>, payload: conversations::ConversationPayload) -> Result<Value, String> {
    with_client(db, move |client| conversations::turns(client, &payload)).await
}

/// Every language rendering of the version a chunk belongs to.
#[tauri::command]
async fn chunk_renderings(db: State<'_, Db>, payload: ChunkPayload) -> Result<Value, String> {
    with_client(db, move |client| search::chunk_renderings(client, &payload.chunk_id)).await
}

/// Direct article search, no LLM: the review UI's own `search::search`.
#[tauri::command]
async fn search_articles(db: State<'_, Db>, payload: search::SearchPayload) -> Result<Value, String> {
    with_client(db, move |client| search::search(client, &payload, 20)).await
}

pub fn run() {
    tauri::Builder::default()
        .manage(Db::from_env())
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
