//! Phoenix (the trace store, its own `phoenix` database in the same Postgres)
//! for trace deep-links.

use crate::pg::{connect, describe};
use serde_json::{json, Value};

/// Replace the database name in a Postgres URL, preserving any `?options`.
fn swap_database(db_url: &str, dbname: &str) -> String {
    let (base, query) = match db_url.split_once('?') {
        Some((b, q)) => (b, Some(q)),
        None => (db_url, None),
    };
    let swapped = match base.rsplit_once('/') {
        // Guard against URLs with no db path: the part after the last '/'
        // must look like a db name, not `host:port` or `user@host`.
        Some((head, tail)) if !tail.contains('@') && !tail.contains(':') && !head.ends_with(':') => {
            format!("{head}/{dbname}")
        }
        _ => format!("{base}/{dbname}"),
    };
    match query {
        Some(q) => format!("{swapped}?{q}"),
        None => swapped,
    }
}

/// Phoenix project name -> GraphQL global id (base64 of "Project:<id>"), read
/// from the `phoenix` database that shares this Postgres instance. The GID is
/// what Phoenix's trace deep-links use:
///   <endpoint>/projects/<gid>/traces/<trace_id>
pub fn phoenix_projects(db_url: &str) -> Result<Value, String> {
    use base64::engine::general_purpose::STANDARD;
    use base64::Engine;

    let mut client = connect(&swap_database(db_url, "phoenix"))?;
    let rows = client
        .query("SELECT id, name FROM projects", &[])
        .map_err(|e| format!("phoenix projects query failed: {}", describe(e)))?;
    Ok(json!({
        "projects": rows.iter().map(|r| {
            let id: i32 = r.get("id");
            json!({
                "name": r.get::<_, String>("name"),
                "gid": STANDARD.encode(format!("Project:{id}")),
            })
        }).collect::<Vec<_>>(),
    }))
}

#[cfg(test)]
mod tests {
    #[test]
    fn swap_database_keeps_host_and_options() {
        assert_eq!(
            super::swap_database("postgresql://jrc:jrc@localhost:5434/legislation", "phoenix"),
            "postgresql://jrc:jrc@localhost:5434/phoenix"
        );
        assert_eq!(
            super::swap_database("postgresql://jrc:jrc@localhost:5434/legislation?sslmode=disable", "phoenix"),
            "postgresql://jrc:jrc@localhost:5434/phoenix?sslmode=disable"
        );
        assert_eq!(
            super::swap_database("postgresql://jrc:jrc@localhost:5434", "phoenix"),
            "postgresql://jrc:jrc@localhost:5434/phoenix"
        );
    }
}
