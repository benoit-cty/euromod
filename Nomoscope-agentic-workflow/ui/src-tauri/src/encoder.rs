//! Long-lived BGE-M3 query encoder used by the Database tab.

use std::process::Stdio;

use serde_json::{json, Value};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader, Lines};
use tokio::process::{Child, ChildStdin, ChildStdout, Command};
use tokio::sync::Mutex;

use crate::ingest::{embedding_environment, ingest_dir};

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
    /// Encode a retrieval query as a pgvector `halfvec` literal.
    pub async fn encode(&self, query: &str) -> Result<String, String> {
        let response = self.request(query, json!({ "query": query })).await?;
        parse_halfvec(&response)
    }

    /// Cosine similarity of each sentence against the query, in order. One
    /// encoder batch per call, so callers should group the sentences of
    /// several hits into a single request.
    pub async fn score_sentences(&self, query: &str, sentences: &[String]) -> Result<Vec<f64>, String> {
        if sentences.is_empty() {
            return Ok(Vec::new());
        }
        let response = self
            .request(query, json!({ "query": query, "sentences": sentences }))
            .await?;
        parse_similarities(&response, sentences.len())
    }

    /// Send one JSON-lines request, restarting a dead encoder process once.
    async fn request(&self, query: &str, request: Value) -> Result<Value, String> {
        if query.trim().is_empty() {
            return Err("query must not be empty".to_string());
        }

        let mut process = self.process.lock().await;
        for attempt in 0..2 {
            if process.is_none() {
                *process = Some(spawn_encoder().await?);
            }
            let result = exchange(process.as_mut().expect("encoder initialized"), &request).await;
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
    // Runs on the GPU where the ingest package's CUDA environment is installed.
    let (extra, project_environment) = embedding_environment(&dir);
    let mut command = Command::new("uv");
    command
        .args([
            "run",
            "--extra",
            extra,
            "python",
            "-m",
            "nomotheca_ingest.query_embeddings",
        ])
        .env_remove("VIRTUAL_ENV")
        .env("PYTHONUNBUFFERED", "1")
        .current_dir(dir)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        // The encoder reports its resolved device (CPU/GPU) on stderr.
        .stderr(Stdio::inherit());
    if let Some(environment) = project_environment {
        command.env("UV_PROJECT_ENVIRONMENT", environment);
    }

    let mut child = command
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

async fn exchange(process: &mut EncoderProcess, request: &Value) -> Result<Value, String> {
    let request = serde_json::to_string(request).map_err(|e| e.to_string())?;
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
        .map_err(|error| format!("failed to read query encoder response: {error}"))?
        .ok_or("query encoder exited unexpectedly")?;
    parse_response(&response)
}

fn parse_response(response: &str) -> Result<Value, String> {
    let message: Value = serde_json::from_str(response)
        .map_err(|error| format!("invalid query encoder response: {error}"))?;
    if let Some(error) = message.get("error").and_then(Value::as_str) {
        return Err(format!("query encoder error: {error}"));
    }
    Ok(message)
}

fn parse_halfvec(message: &Value) -> Result<String, String> {
    let halfvec = message
        .get("halfvec")
        .and_then(Value::as_str)
        .ok_or("query encoder response has no halfvec")?;
    if !halfvec.starts_with('[') || !halfvec.ends_with(']') {
        return Err("query encoder returned an invalid halfvec".to_string());
    }
    Ok(halfvec.to_string())
}

fn parse_similarities(message: &Value, expected: usize) -> Result<Vec<f64>, String> {
    let similarities = message
        .get("similarities")
        .and_then(Value::as_array)
        .ok_or("query encoder response has no similarities")?;
    if similarities.len() != expected {
        return Err(format!(
            "query encoder returned {} similarities for {expected} sentences",
            similarities.len()
        ));
    }
    similarities
        .iter()
        .map(|v| v.as_f64().ok_or_else(|| "query encoder returned a non-numeric similarity".to_string()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::{parse_halfvec, parse_response, parse_similarities};

    #[test]
    fn parses_halfvec_response() {
        let message = parse_response(r#"{"halfvec":"[0.1,-0.2]"}"#).unwrap();
        assert_eq!(parse_halfvec(&message).unwrap(), "[0.1,-0.2]");
    }

    #[test]
    fn parses_similarities_in_order() {
        let message = parse_response(r#"{"similarities":[0.9,0.1,0.5]}"#).unwrap();
        assert_eq!(parse_similarities(&message, 3).unwrap(), vec![0.9, 0.1, 0.5]);
        let error = parse_similarities(&message, 2).unwrap_err();
        assert!(error.contains("3 similarities for 2 sentences"));
    }

    #[test]
    fn surfaces_encoder_error() {
        let error = parse_response(r#"{"error":"model unavailable"}"#).unwrap_err();
        assert!(error.contains("model unavailable"));
    }
}
