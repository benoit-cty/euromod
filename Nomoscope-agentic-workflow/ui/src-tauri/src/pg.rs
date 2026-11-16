//! The Postgres connection, error rendering and row-to-JSON mapping every
//! module of both desktop apps uses (the RAG chat compiles this file in with
//! `#[path]`).

use postgres::types::Type;
use postgres::{Client, NoTls, Row};
use serde_json::{Map, Value};

/// A row as a JSON object, one key per column in SELECT order, each value
/// mapped by the column's Postgres type. SQL NULL is JSON null for every
/// type, so a column that can be NULL never panics the way `Row::get` into a
/// non-`Option` does. For queries that return their columns as the UI reads
/// them: rename and cast in SQL (`x::text AS x`), not in a `json!` block.
///
/// Dates, timestamps, ranges and uuids are not mapped: cast them `::text` in
/// the query. An unmapped type is an error naming the column, never a guess.
pub fn row_to_json(row: &Row) -> Result<Value, String> {
    let mut object = Map::with_capacity(row.len());
    for (i, column) in row.columns().iter().enumerate() {
        object.insert(column.name().to_string(), cell(row, i, column.type_(), column.name())?);
    }
    Ok(Value::Object(object))
}

/// [row_to_json] over every row.
pub fn rows_to_json(rows: &[Row]) -> Result<Vec<Value>, String> {
    rows.iter().map(row_to_json).collect()
}

fn cell(row: &Row, i: usize, ty: &Type, name: &str) -> Result<Value, String> {
    fn get<'a, T: postgres::types::FromSql<'a>>(row: &'a Row, i: usize, name: &str) -> Result<Option<T>, String> {
        row.try_get::<_, Option<T>>(i).map_err(|e| format!("column {name}: {e}"))
    }
    let value = match *ty {
        Type::BOOL => get::<bool>(row, i, name)?.map(Value::from),
        Type::INT2 => get::<i16>(row, i, name)?.map(Value::from),
        Type::INT4 => get::<i32>(row, i, name)?.map(Value::from),
        Type::INT8 => get::<i64>(row, i, name)?.map(Value::from),
        Type::FLOAT4 => get::<f32>(row, i, name)?.map(|v| Value::from(f64::from(v))),
        Type::FLOAT8 => get::<f64>(row, i, name)?.map(Value::from),
        Type::TEXT | Type::VARCHAR | Type::BPCHAR | Type::NAME => get::<String>(row, i, name)?.map(Value::from),
        Type::JSON | Type::JSONB => get::<Value>(row, i, name)?,
        Type::TEXT_ARRAY | Type::VARCHAR_ARRAY => get::<Vec<Option<String>>>(row, i, name)?.map(Value::from),
        Type::INT2_ARRAY => get::<Vec<Option<i16>>>(row, i, name)?.map(Value::from),
        Type::INT4_ARRAY => get::<Vec<Option<i32>>>(row, i, name)?.map(Value::from),
        Type::INT8_ARRAY => get::<Vec<Option<i64>>>(row, i, name)?.map(Value::from),
        _ => return Err(format!("column {name}: type {ty} is not mapped to JSON (cast it ::text)")),
    };
    Ok(value.unwrap_or(Value::Null))
}

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
    use serde_json::json;

    /// Every mapped type, NULL included, against the live stack (skipped when
    /// the database is down).
    #[test]
    fn row_to_json_maps_by_type_and_null_is_null() {
        let url = std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string());
        let Ok(mut client) = super::connect(&url) else { return };
        let row = client
            .query_one(
                "SELECT true AS b, 2::int2 AS s, 3::int4 AS i, 4::int8 AS l,
                        0.5::float4 AS f, 1.25::float8 AS d, 'x'::text AS t, 'ab'::char(2) AS c,
                        '{\"k\": [1]}'::jsonb AS j, ARRAY['a', NULL] AS ta, ARRAY[1, 2] AS ia,
                        NULL::text AS nt, NULL::int8 AS nl, NULL::jsonb AS nj, NULL::bool AS nb",
                &[],
            )
            .unwrap();
        assert_eq!(
            super::row_to_json(&row).unwrap(),
            json!({
                "b": true, "s": 2, "i": 3, "l": 4, "f": 0.5, "d": 1.25, "t": "x", "c": "ab",
                "j": { "k": [1] }, "ta": ["a", null], "ia": [1, 2],
                "nt": null, "nl": null, "nj": null, "nb": null,
            })
        );
        let unmapped = client.query_one("SELECT now() AS at", &[]).unwrap();
        let error = super::row_to_json(&unmapped).unwrap_err();
        assert!(error.contains("column at"), "{error}");
    }

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
