//! Run the `nomotheca_ingest` CLI scripts (ingestion, embeddings, translation)
//! from the UI, streaming their stdout/stderr back to the frontend as
//! `ingest-log` events and supporting cancellation.
//!
//! Each supported command maps to `uv run [--extra X] python -m
//! nomotheca_ingest.cli <subcommand...>`, executed with `Nomotheca-RAG/ingest` as the
//! working directory so `uv` resolves the project there. The spawned process
//! inherits this app's environment, so provider API keys (for `translate`) and
//! any sourced `.env` are visible to the child.

use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::process::Stdio;
use std::sync::Mutex;

use serde::Deserialize;
use serde_json::{json, Value};
use tauri::{AppHandle, Emitter, State};
use tokio::io::{AsyncBufReadExt, AsyncRead, BufReader};
use tokio::process::Command;
use tokio::sync::oneshot;

/// Managed state: in-flight runs keyed by `run_id`, each holding a cancel
/// sender the `stop_ingest` command fires to kill the child process.
#[derive(Default)]
pub struct IngestState {
    cancels: Mutex<HashMap<String, oneshot::Sender<()>>>,
}

#[derive(Deserialize)]
pub struct IngestPayload {
    /// Frontend-generated id used to tag log events and to target cancellation.
    pub run_id: String,
    /// One of: instrument, citation, embeddings, translate.
    pub command: String,
    pub db_url: String,
    /// Extra CLI arguments (positionals and options) built by the frontend form.
    pub args: Vec<String>,
}

/// Locate the `Nomotheca-RAG/ingest` project directory by walking up from the current
/// directory, or honour an explicit `EUROMOD_INGEST_DIR` override.
pub(crate) fn ingest_dir() -> Option<PathBuf> {
    if let Ok(dir) = std::env::var("EUROMOD_INGEST_DIR") {
        return Some(PathBuf::from(dir));
    }
    let cwd = std::env::current_dir().ok()?;
    for ancestor in cwd.ancestors() {
        let candidate = ancestor.join("Nomotheca-RAG").join("ingest");
        if candidate.join("pyproject.toml").is_file() {
            return Some(candidate);
        }
    }
    None
}

/// Map a UI command to its `uv` extras and the CLI subcommand tokens.
fn command_spec(command: &str) -> Option<(Vec<&'static str>, Vec<&'static str>)> {
    match command {
        "instrument" => Some((vec![], vec!["instrument"])),
        "citation" => Some((vec![], vec!["citation"])),
        // BGE-M3 picks its extra at spawn time: see `embedding_environment`.
        "embeddings" => Some((vec![], vec!["embeddings", "build"])),
        "translate" => Some((vec!["--extra", "translate"], vec!["translate", "run"])),
        _ => None,
    }
}

pub(crate) const EMBEDDING_EXTRA: &str = "embeddings";
pub(crate) const CUDA_EXTRA: &str = "embeddings-cuda";
pub(crate) const CUDA_ENVIRONMENT: &str = ".venv-cuda";

/// Pick the `uv` extra, and project environment, that runs BGE-M3 in `dir`.
///
/// CUDA and CPU torch are conflicting extras in the ingest package, so its GPU
/// build lives in a second environment (`UV_PROJECT_ENVIRONMENT=.venv-cuda uv
/// sync --extra embeddings-cuda`). Where an operator has installed it, point
/// `uv` there and BGE-M3 runs on the GPU; otherwise nothing changes and the
/// default `.venv` (CPU torch + OpenVINO) is used.
pub(crate) fn embedding_environment(dir: &Path) -> (&'static str, Option<PathBuf>) {
    let environment = dir.join(CUDA_ENVIRONMENT);
    if environment.join("pyvenv.cfg").is_file() {
        (CUDA_EXTRA, Some(environment))
    } else {
        (EMBEDDING_EXTRA, None)
    }
}

fn emit_log(app: &AppHandle, run_id: &str, stream: &str, line: &str) {
    let _ = app.emit(
        "ingest-log",
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
    state: State<'_, IngestState>,
    payload: IngestPayload,
) -> Result<Value, String> {
    let (extras, subcommand) = command_spec(&payload.command)
        .ok_or_else(|| format!("unknown ingest command: {}", payload.command))?;
    let dir =
        ingest_dir().ok_or_else(|| "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR)".to_string())?;

    let mut argv: Vec<String> = vec!["run".into()];
    argv.extend(extras.into_iter().map(String::from));
    let project_environment = if payload.command == "embeddings" {
        let (extra, environment) = embedding_environment(&dir);
        argv.push("--extra".into());
        argv.push(extra.into());
        environment
    } else {
        None
    };
    argv.push("python".into());
    argv.push("-m".into());
    argv.push("nomotheca_ingest.cli".into());
    argv.extend(subcommand.into_iter().map(String::from));
    argv.extend(payload.args.iter().cloned());
    argv.push("--database-url".into());
    argv.push(payload.db_url.clone());

    emit_log(&app, &payload.run_id, "system", &format!("$ uv {}", argv.join(" ")));
    emit_log(&app, &payload.run_id, "system", &format!("cwd: {}", dir.display()));

    let mut command = Command::new("uv");
    command
        .args(&argv)
        // Drop any inherited VIRTUAL_ENV so `uv` uses Nomotheca-RAG/ingest's own `.venv`
        // instead of warning that an unrelated active venv doesn't match.
        .env_remove("VIRTUAL_ENV")
        // Python block-buffers stdout when piped; unbuffered keeps log and
        // `@progress` lines streaming live instead of arriving in bursts.
        .env("PYTHONUNBUFFERED", "1")
        .current_dir(&dir)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped());
    if let Some(environment) = &project_environment {
        command.env("UV_PROJECT_ENVIRONMENT", environment);
        emit_log(
            &app,
            &payload.run_id,
            "system",
            &format!("UV_PROJECT_ENVIRONMENT: {} (GPU)", environment.display()),
        );
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

pub fn stop(state: State<'_, IngestState>, run_id: String) -> Result<Value, String> {
    let sender = state.cancels.lock().unwrap().remove(&run_id);
    match sender {
        Some(tx) => {
            let _ = tx.send(());
            Ok(json!({ "stopped": true }))
        }
        None => Ok(json!({ "stopped": false })),
    }
}

#[cfg(test)]
mod tests {
    use super::{embedding_environment, CUDA_EXTRA, EMBEDDING_EXTRA};

    #[test]
    fn embedding_environment_defaults_to_the_cpu_venv() {
        let dir = tempfile::tempdir().unwrap();

        let (extra, environment) = embedding_environment(dir.path());

        assert_eq!(extra, EMBEDDING_EXTRA);
        assert!(environment.is_none());
    }

    #[test]
    fn embedding_environment_prefers_an_installed_cuda_venv() {
        let dir = tempfile::tempdir().unwrap();
        let cuda = dir.path().join(".venv-cuda");
        std::fs::create_dir(&cuda).unwrap();
        std::fs::write(cuda.join("pyvenv.cfg"), "home = /usr/bin\n").unwrap();

        let (extra, environment) = embedding_environment(dir.path());

        assert_eq!(extra, CUDA_EXTRA);
        assert_eq!(environment.unwrap(), cuda);
    }
}
