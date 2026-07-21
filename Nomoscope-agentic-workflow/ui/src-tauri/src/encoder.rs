//! Long-lived BGE-M3 query encoder used by the Database tab.

use std::process::Stdio;

use serde_json::{json, Value};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader, Lines};
use tokio::process::{Child, ChildStdin, ChildStdout, Command};
use tokio::sync::Mutex;

use crate::ingest::ingest_dir;

struct EncoderProcess {
    child: Child,
    stdin: ChildStdin,
    stdout: Lines<BufReader<ChildStdout>>,
}

impl Drop for EncoderProcess {
    fn drop(&mut self) {
        let _ = self.child.start_kill();
    }
}

#[derive(Default)]
pub struct EmbeddingState {
    process: Mutex<Option<EncoderProcess>>,
}

impl EmbeddingState {
    pub async fn encode(&self, query: &str) -> Result<String, String> {
        if query.trim().is_empty() {
            return Err("query must not be empty".to_string());
        }

        let mut process = self.process.lock().await;
        for attempt in 0..2 {
            if process.is_none() {
                *process = Some(spawn_encoder().await?);
            }
            let result = encode_once(process.as_mut().expect("encoder initialized"), query).await;
            if result.is_ok() || attempt == 1 {
                return result;
            }
            if let Some(mut failed) = process.take() {
                let _ = failed.child.kill().await;
            }
        }
        unreachable!()
    }
}

async fn spawn_encoder() -> Result<EncoderProcess, String> {
    let dir = ingest_dir()
        .ok_or_else(|| "could not locate Nomotheca-RAG/ingest (set EUROMOD_INGEST_DIR)".to_string())?;
    let mut child = Command::new("uv")
        .args([
            "run",
            "--extra",
            "embeddings",
            "python",
            "-m",
            "nomotheca_ingest.query_embeddings",
        ])
        .env_remove("VIRTUAL_ENV")
        .env("PYTHONUNBUFFERED", "1")
        .current_dir(dir)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit())
        .spawn()
        .map_err(|error| format!("failed to start BGE-M3 query encoder: {error}"))?;

    let stdin = child.stdin.take().ok_or("encoder stdin unavailable")?;
    let stdout = child.stdout.take().ok_or("encoder stdout unavailable")?;
    let mut lines = BufReader::new(stdout).lines();
    let ready = lines
        .next_line()
        .await
        .map_err(|error| format!("failed to read encoder startup: {error}"))?
        .ok_or("query encoder exited during startup")?;
    let message: Value = serde_json::from_str(&ready)
        .map_err(|error| format!("invalid encoder startup response: {error}"))?;
    if message.get("ready").and_then(Value::as_bool) != Some(true) {
        return Err(format!("query encoder failed to initialize: {message}"));
    }

    Ok(EncoderProcess {
        child,
        stdin,
        stdout: lines,
    })
}

async fn encode_once(process: &mut EncoderProcess, query: &str) -> Result<String, String> {
    let request = serde_json::to_string(&json!({ "query": query })).map_err(|e| e.to_string())?;
    process
        .stdin
        .write_all(format!("{request}\n").as_bytes())
        .await
        .map_err(|error| format!("failed to send query to encoder: {error}"))?;
    process
        .stdin
        .flush()
        .await
        .map_err(|error| format!("failed to flush encoder query: {error}"))?;
    let response = process
        .stdout
        .next_line()
        .await
        .map_err(|error| format!("failed to read query embedding: {error}"))?
        .ok_or("query encoder exited unexpectedly")?;
    parse_response(&response)
}

fn parse_response(response: &str) -> Result<String, String> {
    let message: Value = serde_json::from_str(response)
        .map_err(|error| format!("invalid query encoder response: {error}"))?;
    if let Some(error) = message.get("error").and_then(Value::as_str) {
        return Err(format!("query encoder error: {error}"));
    }
    let halfvec = message
        .get("halfvec")
        .and_then(Value::as_str)
        .ok_or("query encoder response has no halfvec")?;
    if !halfvec.starts_with('[') || !halfvec.ends_with(']') {
        return Err("query encoder returned an invalid halfvec".to_string());
    }
    Ok(halfvec.to_string())
}

#[cfg(test)]
mod tests {
    use super::parse_response;

    #[test]
    fn parses_halfvec_response() {
        assert_eq!(
            parse_response(r#"{"halfvec":"[0.1,-0.2]"}"#).unwrap(),
            "[0.1,-0.2]"
        );
    }

    #[test]
    fn surfaces_encoder_error() {
        let error = parse_response(r#"{"error":"model unavailable"}"#).unwrap_err();
        assert!(error.contains("model unavailable"));
    }
}
