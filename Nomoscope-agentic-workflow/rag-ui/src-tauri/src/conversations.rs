//! Chat history is rows, not files: every turn is one `chat` job in `ops.jobs`
//! whose payload carries the conversation so far (and a `conversation_id`)
//! and whose result is the answer. Listing and reopening a conversation is a
//! read of the caller's own jobs; there is no local copy to keep in sync.

use postgres::{Client, NoTls};
use serde::Deserialize;
use serde_json::{json, Value};

#[derive(Deserialize)]
pub struct ListPayload {
    pub db_url: String,
    pub limit: Option<i64>,
}

#[derive(Deserialize)]
pub struct ConversationPayload {
    pub db_url: String,
    pub conversation_id: String,
}

fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {e}"))
}

/// The caller's conversations, newest first: first question, turn count, last activity.
pub fn list(payload: &ListPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let limit = payload.limit.unwrap_or(40).clamp(1, 200);
    let rows = client
        .query(
            "SELECT payload->>'conversation_id' AS conversation_id,
                    count(*)::bigint AS turns,
                    max(submitted_at)::text AS last_at,
                    (array_agg(payload->'messages'->0->>'content' ORDER BY id))[1] AS title,
                    (array_agg(payload->>'country' ORDER BY id DESC))[1] AS country
             FROM ops.jobs
             WHERE job_type = 'chat' AND submitted_by = current_user
               AND payload ? 'conversation_id'
             GROUP BY 1
             ORDER BY max(submitted_at) DESC
             LIMIT $1",
            &[&limit],
        )
        .map_err(|e| format!("conversation list query failed: {e}"))?;
    Ok(json!({
        "conversations": rows.iter().map(|r| json!({
            "conversation_id": r.get::<_, String>("conversation_id"),
            "turns": r.get::<_, i64>("turns"),
            "last_at": r.get::<_, String>("last_at"),
            "title": r.get::<_, Option<String>>("title"),
            "country": r.get::<_, Option<String>>("country"),
        })).collect::<Vec<_>>(),
    }))
}

/// Every turn of one conversation, oldest first: the question (the last
/// message of that job's payload), the job's status, and its result.
pub fn turns(payload: &ConversationPayload) -> Result<Value, String> {
    let mut client = connect(&payload.db_url)?;
    let rows = client
        .query(
            "SELECT id, status, payload, result, error,
                    submitted_at::text AS submitted_at
             FROM ops.jobs
             WHERE job_type = 'chat' AND submitted_by = current_user
               AND payload->>'conversation_id' = $1
             ORDER BY id",
            &[&payload.conversation_id],
        )
        .map_err(|e| format!("conversation query failed: {e}"))?;
    Ok(json!({
        "conversation_id": payload.conversation_id,
        "turns": rows.iter().map(|r| {
            let body: Value = r.get("payload");
            let question = body["messages"]
                .as_array()
                .and_then(|m| m.last())
                .and_then(|m| m["content"].as_str())
                .unwrap_or_default()
                .to_string();
            json!({
                "job_id": r.get::<_, i64>("id"),
                "status": r.get::<_, String>("status"),
                "question": question,
                "settings": {
                    "country": body["country"],
                    "as_of": body["as_of"],
                    "model": body["model"],
                    "web": body["web"],
                },
                "result": r.get::<_, Option<Value>>("result"),
                "error": r.get::<_, Option<String>>("error"),
                "submitted_at": r.get::<_, String>("submitted_at"),
            })
        }).collect::<Vec<_>>(),
    }))
}
