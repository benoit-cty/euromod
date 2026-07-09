//! Read-only access to the legislation DB (RAG/db/schema.sql) for the
//! Database tab: corpus statistics and article search.

use postgres::{Client, NoTls};
use serde_json::{json, Value};

fn connect(db_url: &str) -> Result<Client, String> {
    Client::connect(db_url, NoTls).map_err(|e| format!("DB connection failed: {e}"))
}

/// Corpus totals, per-jurisdiction breakdown and embedding coverage.
pub fn stats(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;

    let totals = client
        .query_one(
            "SELECT (SELECT count(*) FROM jurisdictions)        AS jurisdictions,
                    (SELECT count(*) FROM instruments)          AS instruments,
                    (SELECT count(*) FROM legal_units)          AS legal_units,
                    (SELECT count(*) FROM legal_unit_versions)  AS versions,
                    (SELECT count(*) FROM legal_unit_versions
                      WHERE upper_inf(validity))                AS versions_in_force,
                    (SELECT count(*) FROM unit_texts)           AS unit_texts,
                    (SELECT count(*) FROM chunks)               AS chunks,
                    (SELECT count(*) FROM embeddings)           AS embeddings,
                    (SELECT count(*) FROM citation_registry)    AS citations_registered",
            &[],
        )
        .map_err(|e| e.to_string())?;

    let by_country = client
        .query(
            "SELECT j.code, j.name,
                    count(DISTINCT i.id)::bigint  AS instruments,
                    count(DISTINCT u.id)::bigint  AS legal_units,
                    count(DISTINCT v.id)::bigint  AS versions,
                    count(DISTINCT v.id) FILTER (WHERE upper_inf(v.validity))::bigint AS in_force,
                    count(DISTINCT t.id)::bigint  AS texts,
                    count(DISTINCT c.id)::bigint  AS chunks
             FROM jurisdictions j
             LEFT JOIN instruments i         ON i.jurisdiction_id = j.id
             LEFT JOIN legal_units u         ON u.instrument_id = i.id
             LEFT JOIN legal_unit_versions v ON v.legal_unit_id = u.id
             LEFT JOIN unit_texts t          ON t.version_id = v.id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id
             GROUP BY j.code, j.name ORDER BY j.code",
            &[],
        )
        .map_err(|e| e.to_string())?;

    let models = client
        .query(
            "SELECT m.id::int, m.name, m.provider, m.stored_dim::int, m.is_default,
                    count(e.chunk_id)::bigint AS embedded_chunks
             FROM embedding_models m
             LEFT JOIN embeddings e ON e.model_id = m.id
             GROUP BY m.id, m.name, m.provider, m.stored_dim, m.is_default
             ORDER BY m.id",
            &[],
        )
        .map_err(|e| e.to_string())?;

    Ok(json!({
        "totals": {
            "jurisdictions": totals.get::<_, i64>("jurisdictions"),
            "instruments": totals.get::<_, i64>("instruments"),
            "legal_units": totals.get::<_, i64>("legal_units"),
            "versions": totals.get::<_, i64>("versions"),
            "versions_in_force": totals.get::<_, i64>("versions_in_force"),
            "unit_texts": totals.get::<_, i64>("unit_texts"),
            "chunks": totals.get::<_, i64>("chunks"),
            "embeddings": totals.get::<_, i64>("embeddings"),
            "citations_registered": totals.get::<_, i64>("citations_registered"),
        },
        "by_country": by_country.iter().map(|r| json!({
            "code": r.get::<_, String>("code"),
            "name": r.get::<_, Option<String>>("name"),
            "instruments": r.get::<_, i64>("instruments"),
            "legal_units": r.get::<_, i64>("legal_units"),
            "versions": r.get::<_, i64>("versions"),
            "in_force": r.get::<_, i64>("in_force"),
            "texts": r.get::<_, i64>("texts"),
            "chunks": r.get::<_, i64>("chunks"),
        })).collect::<Vec<_>>(),
        "embedding_models": models.iter().map(|r| json!({
            "id": r.get::<_, i32>(0),
            "name": r.get::<_, String>("name"),
            "provider": r.get::<_, Option<String>>("provider"),
            "stored_dim": r.get::<_, i32>("stored_dim"),
            "is_default": r.get::<_, bool>("is_default"),
            "embedded_chunks": r.get::<_, i64>("embedded_chunks"),
        })).collect::<Vec<_>>(),
    }))
}

/// Find law articles by citation (pg_trgm) or full text (FTS), optionally
/// filtered by country and point-in-time validity.
pub fn search_articles(
    db_url: &str,
    query: &str,
    country: Option<&str>,
    as_of: Option<&str>,
    limit: i64,
) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let rows = client
        .query(
            "SELECT ch.id::text AS chunk_id, u.citation, ch.context_header,
                    ch.content, t.lang, v.validity::text AS validity, v.version_status,
                    j.code AS country, i.title AS instrument_title,
                    GREATEST(
                      similarity(u.citation, $1),
                      coalesce(ts_rank_cd(ch.tsv, websearch_to_tsquery(ch.search_config, $1), 32), 0)
                    )::float8 AS score
             FROM chunks ch
             JOIN unit_texts t          ON t.id = ch.unit_text_id
             JOIN legal_unit_versions v ON v.id = t.version_id
             JOIN legal_units u         ON u.id = v.legal_unit_id
             JOIN instruments i         ON i.id = u.instrument_id
             JOIN jurisdictions j       ON j.id = i.jurisdiction_id
             WHERE (u.citation % $1
                    OR ch.tsv @@ websearch_to_tsquery(ch.search_config, $1))
               AND ($2::text IS NULL OR j.code = $2)
               AND ($3::text IS NULL OR v.validity @> ($3::text)::date)
             ORDER BY score DESC, u.citation, lower(v.validity)
             LIMIT $4",
            &[&query, &country, &as_of, &limit],
        )
        .map_err(|e| e.to_string())?;

    Ok(json!({
        "query": query,
        "results": rows.iter().map(|r| json!({
            "chunk_id": r.get::<_, String>("chunk_id"),
            "citation": r.get::<_, Option<String>>("citation"),
            "context_header": r.get::<_, Option<String>>("context_header"),
            "content": r.get::<_, String>("content"),
            "lang": r.get::<_, String>("lang"),
            "validity": r.get::<_, String>("validity"),
            "version_status": r.get::<_, Option<String>>("version_status"),
            "country": r.get::<_, String>("country"),
            "instrument_title": r.get::<_, Value>("instrument_title"),
            "score": r.get::<_, f64>("score"),
        })).collect::<Vec<_>>(),
    }))
}
