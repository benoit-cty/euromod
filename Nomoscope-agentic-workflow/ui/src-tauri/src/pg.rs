//! The Postgres connection and error rendering every module of both desktop
//! apps uses (the RAG chat compiles this file in with `#[path]`).

use postgres::{Client, NoTls};

pub fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {}", describe(e)))
}

/// The login the app connected with: the reviewer identity everywhere
/// (`decide_review_item`, `ops.jobs.submitted_by`, golden verdicts).
pub fn current_user(db_url: &str) -> Result<String, String> {
    let mut client = connect(db_url)?;
    client
        .query_one("SELECT current_user", &[])
        .map_err(describe)
        .map(|row| row.get::<_, String>(0))
}

/// `postgres::Error` displays as a bare "db error"; the server's message (a
/// RAISE in decide_review_item, a missing relation, a refused privilege) is
/// what the analyst needs.
pub fn describe(e: postgres::Error) -> String {
    match e.as_db_error() {
        Some(db) => match db.detail() {
            Some(detail) => format!("{}: {} ({detail})", e, db.message()),
            None => format!("{}: {}", e, db.message()),
        },
        None => e.to_string(),
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn describe_carries_the_server_message() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let Ok(mut client) = super::connect(&url) else { return };
        let err = client.query("SELECT * FROM no_such_relation_zz", &[]).unwrap_err();
        let text = super::describe(err);
        assert!(text.contains("no_such_relation_zz"), "{text}");
    }
}
