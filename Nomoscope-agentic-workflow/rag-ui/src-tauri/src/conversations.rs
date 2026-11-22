//! Chat history is rows, not files: every turn is one `chat` job in `ops.jobs`
//! whose payload carries the conversation so far (and a `conversation_id`)
//! and whose result is the answer. Listing and reopening a conversation is a
//! read of the caller's own jobs; there is no local copy to keep in sync.

use crate::pg::{describe, rows_to_json};
use postgres::Client;
use serde::Deserialize;
use serde_json::{json, Value};

#[derive(Deserialize)]
pub struct ListPayload {
    pub limit: Option<i64>,
}

#[derive(Deserialize)]
pub struct ConversationPayload {
    pub conversation_id: String,
}

/// The caller's conversations, newest first: first question, turn count, last activity.
pub fn list(client: &mut Client, payload: &ListPayload) -> Result<Value, String> {
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
               -- not `payload ? 'conversation_id'`: a JSON null passes that
               -- test and ->> then yields SQL NULL
               AND payload->>'conversation_id' IS NOT NULL
             GROUP BY 1
             ORDER BY max(submitted_at) DESC
             LIMIT $1",
            &[&limit],
        )
        .map_err(|e| format!("conversation list query failed: {}", describe(e)))?;
    Ok(json!({
        "conversations": rows_to_json(&rows)?,
    }))
}

/// Every turn of one conversation, oldest first: the question (the last
/// message of that job's payload), the job's status, and its result.
pub fn turns(client: &mut Client, payload: &ConversationPayload) -> Result<Value, String> {
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
        .map_err(|e| format!("conversation query failed: {}", describe(e)))?;
    Ok(json!({
        "conversation_id": payload.conversation_id,
        "turns": rows.iter().map(|r| {
            let body: Value = r.get::<_, Option<Value>>("payload").unwrap_or(Value::Null);
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
                "submitted_at": r.get::<_, Option<String>>("submitted_at"),
            })
        }).collect::<Vec<_>>(),
    }))
}

#[cfg(test)]
mod tests {
    /// The listing's row→JSON mapping against the live stack; a chat job whose
    /// payload says `"conversation_id": null` is left out instead of failing
    /// the whole list. Skipped when the database or `ops` is absent.
    #[test]
    fn list_skips_a_null_conversation_id() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let Ok(mut client) = crate::pg::connect(&url) else {
            return;
        };
        let Ok(row) = client.query_one(
            "INSERT INTO ops.jobs (job_type, payload, status)
             VALUES ('chat', '{\"conversation_id\": null, \"_test\": \"zz_null_conversation\"}', 'cancelled')
             RETURNING id",
            &[],
        ) else {
            return;
        };
        let id: i64 = row.get(0);
        let listed = super::list(&mut client, &super::ListPayload { limit: Some(200) });
        client
            .execute("DELETE FROM ops.jobs WHERE id = $1", &[&id])
            .unwrap();
        assert!(listed.unwrap()["conversations"]
            .as_array()
            .unwrap()
            .iter()
            .all(|c| c["conversation_id"].is_string()));
    }
}
