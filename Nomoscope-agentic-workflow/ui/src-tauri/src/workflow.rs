//! Run the `nomoscope-workflow` CLI (the agentic pipeline) from the UI,
//! streaming its stdout/stderr back to the frontend as `workflow-log` events
//! and supporting cancellation. Mirrors ingest.rs.
//!
//! The frontend builds the argument vector (e.g. `run-targets <model_target>…
//! --as-of 2025-06-01 [--model …] [--force]`); only a whitelisted set of
//! subcommands may be launched. The child runs with
//! `Nomoscope-agentic-workflow/pipeline` as the working directory so `uv`
//! resolves the project there, and inherits this app's environment (provider
//! API keys, PHOENIX_*, WORKFLOW_* knobs).

use std::collections::HashMap;
use std::path::PathBuf;
use std::process::Stdio;
use std::sync::Mutex;

use serde::Deserialize;
use serde_json::{json, Value};
use tauri::{AppHandle, Emitter, State};
use tokio::io::{AsyncBufReadExt, AsyncRead, BufReader};
use tokio::process::Command;
use tokio::sync::oneshot;

/// Managed state: in-flight runs keyed by `run_id`, each holding a cancel
/// sender the `stop_workflow` command fires to kill the child process.
#[derive(Default)]
pub struct WorkflowState {
    cancels: Mutex<HashMap<String, oneshot::Sender<()>>>,
}

#[derive(Deserialize)]
pub struct WorkflowPayload {
    /// Frontend-generated id used to tag log events and to target cancellation.
    pub run_id: String,
    /// CLI tokens, subcommand first: ["run-targets", "euromod://…", "--as-of", …].
    pub args: Vec<String>,
    /// Exported as WORKFLOW_DATABASE_URL for the child (a
    /// Nomoscope-agentic-workflow/.env can still override it).
    pub db_url: Option<String>,
}

const ALLOWED_SUBCOMMANDS: [&str; 4] = ["run-targets", "run", "run-all", "queue"];

/// Locate the `Nomoscope-agentic-workflow/pipeline` project directory by
/// walking up from the current directory, or honour an explicit
/// `EUROMOD_WORKFLOW_DIR` override.
fn pipeline_dir() -> Option<PathBuf> {
    if let Ok(dir) = std::env::var("EUROMOD_WORKFLOW_DIR") {
        return Some(PathBuf::from(dir));
    }
    let cwd = std::env::current_dir().ok()?;
    for ancestor in cwd.ancestors() {
        for candidate in [
            ancestor.join("pipeline"),
            ancestor.join("Nomoscope-agentic-workflow").join("pipeline"),
        ] {
            if candidate.join("pyproject.toml").is_file() {
                return Some(candidate);
            }
        }
    }
    None
}

fn emit_log(app: &AppHandle, run_id: &str, stream: &str, line: &str) {
    let _ = app.emit(
        "workflow-log",
        json!({ "run_id": run_id, "stream": stream, "line": line }),
    );
}

/// Read a piped stream line-by-line, emitting each line as a log event.
fn spawn_reader<R>(
    app: AppHandle,
    run_id: String,
    stream: &'static str,
    reader: R,
) -> tokio::task::JoinHandle<()>
where
    R: AsyncRead + Unpin + Send + 'static,
{
    tokio::spawn(async move {
        let mut lines = BufReader::new(reader).lines();
        while let Ok(Some(line)) = lines.next_line().await {
            emit_log(&app, &run_id, stream, &line);
        }
    })
}

pub async fn run(
    app: AppHandle,
    state: State<'_, WorkflowState>,
    payload: WorkflowPayload,
) -> Result<Value, String> {
    let sub = payload.args.first().map(String::as_str).unwrap_or("");
    if !ALLOWED_SUBCOMMANDS.contains(&sub) {
        return Err(format!("workflow subcommand not allowed: {sub:?}"));
    }
    let dir = pipeline_dir().ok_or_else(|| {
        "could not locate Nomoscope-agentic-workflow/pipeline (set EUROMOD_WORKFLOW_DIR)".to_string()
    })?;

    let mut argv: Vec<String> = vec!["run".into(), "nomoscope-workflow".into()];
    argv.extend(payload.args.iter().cloned());

    emit_log(&app, &payload.run_id, "system", &format!("$ uv {}", argv.join(" ")));
    emit_log(&app, &payload.run_id, "system", &format!("cwd: {}", dir.display()));

    let mut command = Command::new("uv");
    command
        .args(&argv)
        // Drop any inherited VIRTUAL_ENV so `uv` uses the pipeline's own
        // `.venv` instead of warning that an unrelated active venv mismatches.
        .env_remove("VIRTUAL_ENV")
        // Python block-buffers stdout when piped; unbuffered keeps the
        // per-parameter result lines streaming live.
        .env("PYTHONUNBUFFERED", "1")
        .current_dir(&dir)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    if let Some(db_url) = &payload.db_url {
        command.env("WORKFLOW_DATABASE_URL", db_url);
    }
    let mut child = command
        .spawn()
        .map_err(|e| format!("failed to spawn `uv` (is it on PATH?): {e}"))?;

    let stdout = child.stdout.take().expect("stdout piped");
    let stderr = child.stderr.take().expect("stderr piped");
    let out_task = spawn_reader(app.clone(), payload.run_id.clone(), "stdout", stdout);
    let err_task = spawn_reader(app.clone(), payload.run_id.clone(), "stderr", stderr);

    let (cancel_tx, cancel_rx) = oneshot::channel::<()>();
    state
        .cancels
        .lock()
        .unwrap()
        .insert(payload.run_id.clone(), cancel_tx);

    let result = tokio::select! {
        status = child.wait() => match status {
            Ok(s) => Ok(json!({ "canceled": false, "success": s.success(), "code": s.code() })),
            Err(e) => Err(format!("process error: {e}")),
        },
        _ = cancel_rx => {
            let _ = child.kill().await;
            let _ = child.wait().await;
            emit_log(&app, &payload.run_id, "system", "run canceled");
            Ok(json!({ "canceled": true, "success": false, "code": Value::Null }))
        }
    };

    state.cancels.lock().unwrap().remove(&payload.run_id);
    let _ = out_task.await;
    let _ = err_task.await;
    result
}

pub fn stop(state: State<'_, WorkflowState>, run_id: String) -> Result<Value, String> {
    let sender = state.cancels.lock().unwrap().remove(&run_id);
    match sender {
        Some(tx) => {
            let _ = tx.send(());
            Ok(json!({ "stopped": true }))
        }
        None => Ok(json!({ "stopped": false })),
    }
}
