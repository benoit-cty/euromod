//! The UI's only channel to the worker: rows in `ops.jobs` (ADR 0004).
//!
//! The UI never spawns a process. It describes a job (`submit_job`), polls its
//! status and log lines (`job_status`, `job_events`, by last-seen event id) and
//! may ask for its own job to be cancelled (`cancel_job`, which the worker
//! honours by killing the child). The worker publishes its heartbeat and the
//! models it serves in `ops.workers` / `ops.worker_models`; the model pickers
//! read that list and offer nothing else.
//!
//! `encode_query` is the one synchronous use: the Database tab's query vector
//! is an `encode` job on the worker's priority lane, polled every 100 ms.
//!
//! Everything stays loosely typed (serde_json::Value) so the payloads can
//! evolve worker-side (nomergon/jobs.py validates them) without a lockstep
//! release of the UI.

use postgres::{Client, NoTls};
use serde::Deserialize;
use serde_json::{json, Value};
use std::time::{Duration, Instant};

/// A worker whose heartbeat is older than this is presumed dead.
const HEARTBEAT_STALE_SECS: i64 = 60;
const ENCODE_POLL: Duration = Duration::from_millis(100);
const ENCODE_TIMEOUT: Duration = Duration::from_secs(60);
pub const ENCODE_PRIORITY: i16 = 100;

#[derive(Deserialize)]
pub struct SubmitPayload {
    pub db_url: String,
    pub job_type: String,
    pub payload: Option<Value>,
    pub priority: Option<i16>,
}

#[derive(Deserialize)]
pub struct JobPayload {
    pub db_url: String,
    pub id: i64,
}

#[derive(Deserialize)]
pub struct EventsPayload {
    pub db_url: String,
    pub id: i64,
    /// Last event id already seen; 0 for everything.
    pub after: Option<i64>,
}

#[derive(Deserialize)]
pub struct ListPayload {
    pub db_url: String,
    pub limit: Option<i64>,
}

#[derive(Deserialize)]
pub struct EncodePayload {
    pub db_url: String,
    pub query: String,
    pub sentences: Option<Vec<String>>,
}

fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {e}"))
}

/// The columns every job read returns, in one place so status/list agree.
const JOB_COLUMNS: &str = "id, job_type, status, submitted_by,
        submitted_at::text AS submitted_at, started_at::text AS started_at,
        finished_at::text AS finished_at, worker_id, cancel_requested,
        priority, payload, progress, result, error";

fn job_row(r: &postgres::Row) -> Value {
    json!({
        "id": r.get::<_, i64>("id"),
        "job_type": r.get::<_, String>("job_type"),
        "status": r.get::<_, String>("status"),
        "submitted_by": r.get::<_, String>("submitted_by"),
        "submitted_at": r.get::<_, Option<String>>("submitted_at"),
        "started_at": r.get::<_, Option<String>>("started_at"),
        "finished_at": r.get::<_, Option<String>>("finished_at"),
        "worker_id": r.get::<_, Option<String>>("worker_id"),
        "cancel_requested": r.get::<_, bool>("cancel_requested"),
        "priority": r.get::<_, i16>("priority"),
        "payload": r.get::<_, Value>("payload"),
        "progress": r.get::<_, Option<Value>>("progress"),
        "result": r.get::<_, Option<Value>>("result"),
        "error": r.get::<_, Option<String>>("error"),
    })
}

/// Insert one job request. `submitted_by` is never set here: its default is
/// `current_user`, which is also what the reviewer role's RLS policy checks.
pub fn submit(client: &mut Client, job_type: &str, payload: &Value, priority: i16) -> Result<i64, String> {
    let row = client
        .query_one(
            "INSERT INTO ops.jobs (job_type, payload, priority) VALUES ($1, $2, $3) RETURNING id",
            &[&job_type, payload, &priority],
        )
        .map_err(|e| format!("job submit failed: {e}"))?;
    Ok(row.get(0))
}

pub fn submit_job(payload: &SubmitPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let body = payload.payload.clone().unwrap_or_else(|| json!({}));
    let id = submit(&mut client, &payload.job_type, &body, payload.priority.unwrap_or(0))?;
    Ok(json!({ "id": id }))
}

fn status_row(client: &mut Client, id: i64) -> Result<Value, String> {
    let row = client
        .query_opt(&format!("SELECT {JOB_COLUMNS} FROM ops.jobs WHERE id = $1"), &[&id])
        .map_err(|e| format!("job status query failed: {e}"))?
        .ok_or_else(|| format!("job {id} does not exist"))?;
    Ok(job_row(&row))
}

pub fn job_status(payload: &JobPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    status_row(&mut client, payload.id)
}

fn events_after(client: &mut Client, job_id: i64, after: i64) -> Result<Vec<Value>, String> {
    let rows = client
        .query(
            "SELECT id, at::text AS at, stream, line, data
             FROM ops.job_events WHERE job_id = $1 AND id > $2 ORDER BY id",
            &[&job_id, &after],
        )
        .map_err(|e| format!("job events query failed: {e}"))?;
    Ok(rows
        .iter()
        .map(|r| {
            json!({
                "id": r.get::<_, i64>("id"),
                "at": r.get::<_, String>("at"),
                "stream": r.get::<_, String>("stream"),
                "line": r.get::<_, String>("line"),
                "data": r.get::<_, Option<Value>>("data"),
            })
        })
        .collect())
}

pub fn job_events(payload: &EventsPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let events = events_after(&mut client, payload.id, payload.after.unwrap_or(0))?;
    Ok(json!({ "events": events }))
}

/// Ask the worker to stop a job that has not finished. Under the reviewer
/// role's RLS this only reaches the caller's own rows; `cancelled` says whether
/// a row was flagged at all.
pub fn cancel_job(payload: &JobPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let n = client
        .execute(
            "UPDATE ops.jobs SET cancel_requested = true
             WHERE id = $1 AND status IN ('queued', 'running')",
            &[&payload.id],
        )
        .map_err(|e| format!("job cancel failed: {e}"))?;
    Ok(json!({ "id": payload.id, "cancelled": n > 0 }))
}

pub fn list_jobs(payload: &ListPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let limit = payload.limit.unwrap_or(100).clamp(1, 1000);
    let rows = client
        .query(
            &format!("SELECT {JOB_COLUMNS} FROM ops.jobs ORDER BY id DESC LIMIT $1"),
            &[&limit],
        )
        .map_err(|e| format!("job list query failed: {e}"))?;
    let me: String = client
        .query_one("SELECT current_user", &[])
        .map_err(|e| e.to_string())?
        .get(0);
    Ok(json!({
        "current_user": me,
        "jobs": rows.iter().map(job_row).collect::<Vec<_>>(),
    }))
}

/// `ops.workers` with an `alive` flag, and the models the worker serves.
pub fn worker_status_with(client: &mut Client) -> Result<Value, String> {
    let workers = client
        .query(
            "SELECT worker_id, hostname, started_at::text AS started_at,
                    heartbeat_at::text AS heartbeat_at,
                    extract(epoch FROM now() - heartbeat_at)::float8 AS heartbeat_age,
                    heartbeat_at > now() - make_interval(secs => $1::float8) AS alive,
                    current_job_id, device, version
             FROM ops.workers ORDER BY heartbeat_at DESC",
            &[&(HEARTBEAT_STALE_SECS as f64)],
        )
        .map_err(|e| format!("workers query failed: {e}"))?;
    let models = client
        .query(
            "SELECT model, kind, is_default, published_by, published_at::text AS published_at
             FROM ops.worker_models ORDER BY kind, is_default DESC, model",
            &[],
        )
        .map_err(|e| format!("worker models query failed: {e}"))?;
    Ok(json!({
        "workers": workers.iter().map(|r| json!({
            "worker_id": r.get::<_, String>("worker_id"),
            "hostname": r.get::<_, String>("hostname"),
            "started_at": r.get::<_, String>("started_at"),
            "heartbeat_at": r.get::<_, String>("heartbeat_at"),
            "heartbeat_age": r.get::<_, f64>("heartbeat_age"),
            "alive": r.get::<_, bool>("alive"),
            "current_job_id": r.get::<_, Option<i64>>("current_job_id"),
            "device": r.get::<_, Option<String>>("device"),
            "version": r.get::<_, Option<String>>("version"),
        })).collect::<Vec<_>>(),
        "models": models.iter().map(|r| json!({
            "model": r.get::<_, String>("model"),
            "kind": r.get::<_, String>("kind"),
            "is_default": r.get::<_, bool>("is_default"),
            "published_by": r.get::<_, String>("published_by"),
            "published_at": r.get::<_, String>("published_at"),
        })).collect::<Vec<_>>(),
    }))
}

pub fn worker_status(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    worker_status_with(&mut client)
}

fn any_worker_alive(client: &mut Client) -> Result<bool, String> {
    let row = client
        .query_one(
            "SELECT EXISTS (SELECT 1 FROM ops.workers
                            WHERE heartbeat_at > now() - make_interval(secs => $1::float8))",
            &[&(HEARTBEAT_STALE_SECS as f64)],
        )
        .map_err(|e| format!("workers query failed: {e}"))?;
    Ok(row.get(0))
}

pub const NO_WORKER: &str = "no worker is running (ops.workers heartbeat stale)";

/// Encode a query (and optionally score sentences against it) on the worker:
/// submit an `encode` job on the priority lane and poll it every 100 ms, up to
/// 60 s. Refuses up front when no worker heartbeat is fresh, so the Database
/// tab can fall back to full-text search without waiting out the timeout.
///
/// Returns the job's `result`: `{"halfvec": "[…]"}` or `{"similarities": […]}`.
pub fn encode_query(payload: &EncodePayload) -> Result<Value, String> {
    if payload.query.trim().is_empty() {
        return Err("query must not be empty".to_string());
    }
    let mut client = connect(&payload.db_url)?;
    if !any_worker_alive(&mut client)? {
        return Err(NO_WORKER.to_string());
    }
    let body = match &payload.sentences {
        Some(sentences) => json!({ "query": payload.query, "sentences": sentences }),
        None => json!({ "query": payload.query }),
    };
    let id = submit(&mut client, "encode", &body, ENCODE_PRIORITY)?;
    let started = Instant::now();
    loop {
        let row = client
            .query_one(
                "SELECT status, result, error FROM ops.jobs WHERE id = $1",
                &[&id],
            )
            .map_err(|e| format!("encode job poll failed: {e}"))?;
        let status: String = row.get("status");
        match status.as_str() {
            "succeeded" => {
                let result: Option<Value> = row.get("result");
                return result.ok_or_else(|| "encode job succeeded without a result".to_string());
            }
            "failed" | "cancelled" => {
                let error: Option<String> = row.get("error");
                return Err(format!(
                    "encode job {id} {status}: {}",
                    error.unwrap_or_else(|| "no error recorded".to_string())
                ));
            }
            _ => {}
        }
        if started.elapsed() > ENCODE_TIMEOUT {
            let _ = client.execute(
                "UPDATE ops.jobs SET cancel_requested = true WHERE id = $1 AND status IN ('queued','running')",
                &[&id],
            );
            return Err(format!("encode job {id} did not finish within 60 s (status {status})"));
        }
        std::thread::sleep(ENCODE_POLL);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn test_client() -> Option<Client> {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let mut client = connect(&url).ok()?;
        // `ops` not applied yet (nomergon init-db) → skip
        client.execute("SELECT 1 FROM ops.jobs LIMIT 0", &[]).ok()?;
        Some(client)
    }

    fn url() -> String {
        std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string())
    }

    /// submit → status → events after a cursor → cancel, against the live
    /// stack. No worker is needed: the job stays queued and is cleaned up.
    #[test]
    fn job_round_trip_smoke() {
        let Some(mut client) = test_client() else { return };
        let db_url = url();

        let submitted = submit_job(&SubmitPayload {
            db_url: db_url.clone(),
            job_type: "impact".into(),
            payload: Some(json!({ "project": "", "zone": "EEE", "_test": "zz_jobs_smoke" })),
            priority: None,
        })
        .unwrap();
        let id = submitted["id"].as_i64().expect("submit returns the new id");

        let status = job_status(&JobPayload { db_url: db_url.clone(), id }).unwrap();
        assert_eq!(status["status"], "queued");
        assert_eq!(status["job_type"], "impact");
        assert_eq!(status["priority"], 0);
        assert!(status["submitted_by"].as_str().is_some_and(|u| !u.is_empty()));
        assert_eq!(status["payload"]["_test"], "zz_jobs_smoke");

        // events: cursor semantics — only rows after `after`, in id order
        let ids: Vec<i64> = ["one", "two", "three"]
            .iter()
            .map(|line| {
                client
                    .query_one(
                        "INSERT INTO ops.job_events (job_id, stream, line) VALUES ($1, 'stdout', $2) RETURNING id",
                        &[&id, line],
                    )
                    .unwrap()
                    .get(0)
            })
            .collect();
        let all = job_events(&EventsPayload { db_url: db_url.clone(), id, after: None }).unwrap();
        assert_eq!(all["events"].as_array().unwrap().len(), 3);
        let tail = job_events(&EventsPayload { db_url: db_url.clone(), id, after: Some(ids[0]) }).unwrap();
        let lines: Vec<&str> = tail["events"]
            .as_array()
            .unwrap()
            .iter()
            .map(|e| e["line"].as_str().unwrap())
            .collect();
        assert_eq!(lines, vec!["two", "three"]);

        let listed = list_jobs(&ListPayload { db_url: db_url.clone(), limit: Some(5) }).unwrap();
        assert_eq!(listed["jobs"][0]["id"], id, "newest first");

        let cancelled = cancel_job(&JobPayload { db_url: db_url.clone(), id }).unwrap();
        assert_eq!(cancelled["cancelled"], true);
        let status = job_status(&JobPayload { db_url: db_url.clone(), id }).unwrap();
        assert_eq!(status["cancel_requested"], true);

        // worker status reads even when nobody has ever published
        let ws = worker_status(&db_url).unwrap();
        assert!(ws["workers"].is_array());
        assert!(ws["models"].is_array());

        client.execute("DELETE FROM ops.jobs WHERE id = $1", &[&id]).unwrap();
    }

    /// Without a live worker, encode refuses immediately with the message the
    /// Database tab keys its full-text fallback on — and leaves no job behind.
    #[test]
    fn encode_refuses_without_a_worker() {
        let Some(mut client) = test_client() else { return };
        let alive = any_worker_alive(&mut client).unwrap();
        if alive {
            return; // a real worker is up: this test's premise does not hold
        }
        // Other tests in this binary insert jobs concurrently, so count only
        // the row this call would have written, not the whole table.
        let query = format!("zz_encode_refusal_{}", std::process::id());
        let error = encode_query(&EncodePayload { db_url: url(), query: query.clone(), sentences: None })
            .unwrap_err();
        assert_eq!(error, NO_WORKER);
        let left_behind: i64 = client
            .query_one(
                "SELECT count(*) FROM ops.jobs WHERE job_type = 'encode' AND payload->>'query' = $1",
                &[&query],
            )
            .unwrap()
            .get(0);
        assert_eq!(left_behind, 0);
    }
}
