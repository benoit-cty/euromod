//! Tauri command layer for the EUROMOD parameter-review UI.
//!
//! Command pattern (from tauri_outdated_parameters_app): a single `payload`
//! JSON argument where the command needs input, deserialised into a typed
//! struct, returning `Result<serde_json::Value, String>` so the frontend gets
//! either data or a rejected promise with the error string.
//!
//! The UI is fully remote (ADR 0004): it spawns nothing and reads no data
//! directory. Its one credential is the analyst's Postgres login, which lives
//! in Tauri state ([pool::Db]) and never travels through the webview: every
//! command takes a pooled connection from it, and `set_db_url` is the one way
//! to point the app at another database. Everything that needs a model or the
//! internet is a row in `ops.jobs` (jobs.rs) that the worker picks up. The
//! only file it ever writes is the EUROMOD export. Besides decisions and jobs,
//! the one thing it changes in the database is a parameter's metadata,
//! through `params.edit_parameter` (ADR 0005).

mod db;
mod golden;
mod jobs;
mod pg;
mod pool;
mod store;

use golden::GoldenVerifyPayload;
use jobs::{EncodePayload, EventsPayload, JobPayload, ListPayload, SubmitPayload};
use pool::Db;

use serde::Deserialize;
use serde_json::{json, Value};
use tauri::State;

#[derive(Deserialize)]
struct DecisionPayload {
    item_id: String,
    /// The run of the item the reviewer had on screen (`item.run_id`). A
    /// decision on an item re-run since then is refused (code audit D7).
    run_id: Option<String>,
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
struct EditPayload {
    model_target: String,
    /// unit | source_type | label | short_label | description | explanation;
    /// anything else (identity, values) is refused by the database.
    field: String,
    value: Value,
    note: Option<String>,
}

#[derive(Deserialize)]
struct TargetPayload {
    model_target: String,
}

#[derive(Deserialize)]
struct DecisionsPayload {
    limit: Option<usize>,
}

#[derive(Deserialize)]
struct UrlPayload {
    db_url: String,
}

#[derive(Deserialize)]
struct ChunkPayload {
    chunk_id: String,
}

#[derive(Deserialize)]
struct EvalRunPayload {
    run_pk: i64,
}

#[derive(Deserialize)]
struct InstrumentSearchPayload {
    country: String,
    query: String,
    limit: Option<i64>,
}

#[derive(Deserialize)]
struct SentenceScorePayload {
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

/// Connection settings plus the reviewer identity, which is the database's
/// `current_user` (the per-analyst login), never an environment guess. The
/// URL is shown with its password masked.
#[tauri::command]
async fn get_env_config(db: State<'_, Db>) -> Result<Value, String> {
    let phoenix_endpoint = std::env::var("PHOENIX_COLLECTOR_ENDPOINT")
        .unwrap_or_else(|_| "http://localhost:6006".to_string());
    // same default as the pipeline's config.py, so trace deep-links resolve
    let phoenix_project = std::env::var("PHOENIX_PROJECT_NAME")
        .unwrap_or_else(|_| "nomoscope-agentic-workflow".to_string());
    let db_url = pool::redact(&db.url());
    let (reviewer, db_error) = match with_client(db, pg::current_user).await {
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

/// Point the whole app at another database. The URL may keep the masked
/// password it was shown with (the current one is kept behind the mask). It
/// is checked first: a database that does not answer changes nothing.
#[tauri::command]
async fn set_db_url(db: State<'_, Db>, payload: UrlPayload) -> Result<Value, String> {
    let db = db.inner().clone();
    blocking(move || {
        let url = pool::unredact(payload.db_url.trim(), &db.url());
        let reviewer = pg::current_user(&mut pg::connect(&url)?)?;
        db.set_url(url.clone());
        Ok(json!({ "db_url": pool::redact(&url), "reviewer": reviewer }))
    })
    .await
}

#[tauri::command]
async fn golden_cases(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, golden::load_cases).await
}

#[tauri::command]
async fn set_golden_verified(
    db: State<'_, Db>,
    payload: GoldenVerifyPayload,
) -> Result<Value, String> {
    with_client(db, move |client| golden::set_verified(client, &payload)).await
}

#[tauri::command]
async fn load_queue(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, store::load_queue).await
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
async fn save_decision(db: State<'_, Db>, payload: DecisionPayload) -> Result<Value, String> {
    with_client(db, move |client| {
        let reviewer = payload.reviewer.clone().unwrap_or_else(|| "reviewer".to_string());
        let (item, entry) = store::prepare_decision(
            client,
            &payload.item_id,
            payload.run_id.as_deref(),
            &payload.action,
            &reviewer,
            payload.note.as_deref(),
            payload.edited_value.as_ref(),
            payload.edited_fields.as_ref(),
        )?;
        let decision = store::commit_decision(client, &payload.item_id, &item, &entry).map_err(|e| {
            // The ways this fails look very different to a reviewer: a
            // stopped container, or a database that never had the params
            // schema applied (fresh stack / after `docker compose down -v`).
            let hint = if e.contains("decide_review_item") || e.contains("schema \"params\"") {
                "the params schema is missing or outdated — run `nomoscope-workflow init-param-db`"
            } else if e.contains("not in the queue") {
                "the item is no longer in the review queue — reload it"
            } else if e.contains("re-run since it was opened") {
                "the parameter was re-run after you opened it — reload the queue and review the new proposal"
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
async fn load_decisions(db: State<'_, Db>, payload: DecisionsPayload) -> Result<Value, String> {
    let limit = payload.limit.unwrap_or(200) as i64;
    with_client(db, move |client| db::params::load_decisions(client, limit)).await
}

/// Correct one metadata field of a parameter (ADR 0005). One database call
/// validates, audits (reviewer = current_user) and applies it; a refused edit
/// changes nothing.
#[tauri::command]
async fn edit_parameter(db: State<'_, Db>, payload: EditPayload) -> Result<Value, String> {
    with_client(db, move |client| {
        store::edit_parameter(
            client,
            &payload.model_target,
            &payload.field,
            &payload.value,
            payload.note.as_deref().filter(|n| !n.trim().is_empty()),
        )
    })
    .await
}

/// A parameter's metadata edit history, newest first.
#[tauri::command]
async fn parameter_edits(db: State<'_, Db>, payload: TargetPayload) -> Result<Value, String> {
    with_client(db, move |client| {
        db::params::parameter_edits(client, &payload.model_target)
    })
    .await
}

/// A parameter's texts and EUROMOD value history (or a schedule's members'),
/// for the review page's hand-off prompt. Read-only.
#[tauri::command]
async fn parameter_context(db: State<'_, Db>, payload: TargetPayload) -> Result<Value, String> {
    with_client(db, move |client| {
        db::params::parameter_context(client, &payload.model_target)
    })
    .await
}

/// Export the change set for EUROMOD — metadata edits and accepted value
/// changes only — one JSON file per country, into a folder the reviewer picks.
/// The only file the UI writes.
#[tauri::command]
async fn export_changes(app_handle: tauri::AppHandle, db: State<'_, Db>) -> Result<Value, String> {
    use tauri_plugin_dialog::DialogExt;
    let groups = with_client(db, store::export_records).await?;
    if groups.is_empty() {
        return Ok(json!({ "count": 0, "paths": [], "canceled": false }));
    }
    let count: usize = groups.values().map(Vec::len).sum();
    let picked = tauri::async_runtime::spawn_blocking(move || {
        app_handle
            .dialog()
            .file()
            .set_title("Export changes for EUROMOD — choose a folder")
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
async fn db_stats(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, db::corpus::stats).await
}

#[tauri::command]
async fn eval_runs(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, db::eval::eval_runs).await
}

#[tauri::command]
async fn eval_run_detail(db: State<'_, Db>, payload: EvalRunPayload) -> Result<Value, String> {
    with_client(db, move |client| {
        db::eval::eval_run_detail(client, payload.run_pk)
    })
    .await
}

/// Article search (`db::search::search`: encode on the worker, then `search_chunks`).
#[tauri::command]
async fn search_articles(
    db: State<'_, Db>,
    payload: db::search::SearchPayload,
) -> Result<Value, String> {
    with_client(db, move |client| db::search::search(client, &payload, 25)).await
}

/// Cosine of each sentence against the query, one BGE-M3 batch on the
/// worker. The Database tab uses it to tint, inside a hit, the sentence that
/// most likely answers.
#[tauri::command]
async fn score_sentences(
    db: State<'_, Db>,
    payload: SentenceScorePayload,
) -> Result<Vec<f64>, String> {
    if payload.sentences.is_empty() {
        return Ok(Vec::new());
    }
    let expected = payload.sentences.len();
    with_client(db, move |client| {
        let model_id = db::search::default_model_id(client)?;
        let result = jobs::encode_query(
            client,
            &EncodePayload {
                query: payload.query,
                sentences: Some(payload.sentences),
                model_id: Some(model_id),
            },
        )?;
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
            .map(|v| {
                v.as_f64()
                    .ok_or_else(|| "encode job returned a non-numeric similarity".to_string())
            })
            .collect()
    })
    .await
}

#[tauri::command]
async fn search_instruments(
    db: State<'_, Db>,
    payload: InstrumentSearchPayload,
) -> Result<Value, String> {
    with_client(db, move |client| {
        db::corpus::search_instruments(
            client,
            &payload.country,
            &payload.query,
            payload.limit.unwrap_or(20),
        )
    })
    .await
}

#[tauri::command]
async fn params_list(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, db::params::params_list).await
}

#[tauri::command]
async fn chunk_renderings(db: State<'_, Db>, payload: ChunkPayload) -> Result<Value, String> {
    with_client(db, move |client| {
        db::search::chunk_renderings(client, &payload.chunk_id)
    })
    .await
}

/// Phoenix lives in its own database on the same server, so this one
/// connects by URL rather than through the pool.
#[tauri::command]
async fn phoenix_projects(db: State<'_, Db>) -> Result<Value, String> {
    let url = db.url();
    blocking(move || db::phoenix::phoenix_projects(&url)).await
}

// ---------------------------------------------------------------- jobs ----

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
async fn list_jobs(db: State<'_, Db>, payload: ListPayload) -> Result<Value, String> {
    with_client(db, move |client| jobs::list_jobs(client, &payload)).await
}

#[tauri::command]
async fn worker_status(db: State<'_, Db>) -> Result<Value, String> {
    with_client(db, jobs::worker_status).await
}

pub fn run() {
    tauri::Builder::default()
        .manage(Db::from_env())
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            get_env_config,
            set_db_url,
            load_queue,
            save_decision,
            load_decisions,
            export_changes,
            edit_parameter,
            parameter_edits,
            parameter_context,
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
