//! The legislation DB (Nomotheca-RAG/db/schema.sql) as a library: corpus
//! statistics and per-country readiness, and the instruments a contributed
//! document can be said to implement. Read-only.

use crate::pg::{connect, describe, row_to_json, rows_to_json};
use serde_json::{json, Value};

/// Corpus totals, per-jurisdiction breakdown, embedding coverage and the
/// per-country readiness of the two non-legislative inputs (Country Report,
/// enriched parameter store).
pub fn stats(db_url: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;

    let totals = client
        .query_one(
            "SELECT (SELECT count(*) FROM jurisdictions WHERE parent_id IS NULL) AS jurisdictions,
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
        .map_err(describe)?;

    let by_country = client
        .query(
            "SELECT coalesce(p.code, j.code) AS code, coalesce(p.name, j.name) AS name,
                    count(DISTINCT i.id)::bigint  AS instruments,
                    count(DISTINCT u.id)::bigint  AS legal_units,
                    count(DISTINCT v.id)::bigint  AS versions,
                    count(DISTINCT v.id) FILTER (WHERE upper_inf(v.validity))::bigint AS in_force,
                    count(DISTINCT t.id)::bigint  AS texts,
                    count(DISTINCT v.id) FILTER (WHERE t.id IS NOT NULL)::bigint  AS text_versions,
                    count(DISTINCT v.id) FILTER (WHERE t.lang = 'en')::bigint     AS en_versions,
                    count(DISTINCT t.id) FILTER (WHERE t.authenticity = 'authentic')::bigint            AS authentic,
                    count(DISTINCT t.id) FILTER (WHERE t.authenticity = 'official_translation')::bigint AS official_translation,
                    count(DISTINCT t.id) FILTER (WHERE t.authenticity = 'machine_translation')::bigint  AS machine_translation,
                    count(DISTINCT c.id)::bigint  AS chunks,
                    count(DISTINCT e.chunk_id)::bigint AS embedded_chunks
             FROM jurisdictions j
             LEFT JOIN jurisdictions p       ON p.id = j.parent_id
             LEFT JOIN instruments i         ON i.jurisdiction_id = j.id
             LEFT JOIN legal_units u         ON u.instrument_id = i.id
             LEFT JOIN legal_unit_versions v ON v.legal_unit_id = u.id
             LEFT JOIN unit_texts t          ON t.version_id = v.id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id
             LEFT JOIN embeddings e          ON e.chunk_id = c.id
             -- Child jurisdictions (Spain's autonomous communities, ADR 0003)
             -- roll up into their country: one row per country the UI and the
             -- Ingest tab's jurisdiction picker know about.
             GROUP BY 1, 2 ORDER BY 1",
            &[],
        )
        .map_err(describe)?;

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
        .map_err(describe)?;

    // The languages the store is configured to index. The Contributed-document
    // form offers these and nothing else: a text stored under a language with
    // no FTS config is invisible to full-text search.
    let languages = client
        .query("SELECT lang FROM lang_fts_config ORDER BY lang", &[])
        .map_err(describe)?;

    // Non-legislative inputs the pipeline needs beside the law corpus: the
    // EUROMOD Country Report (instrument_type = 'country_report', a separate
    // corpus class excluded from evidence retrieval) and the enriched
    // parameter store loaded by `ingest-params`. Shown per country so a
    // missing one is visible before a run silently under-performs.
    let country_reports = client
        .query(
            "SELECT coalesce(p.code, j.code) AS code,
                    count(DISTINCT i.id)::bigint       AS reports,
                    count(DISTINCT c.id)::bigint       AS chunks,
                    count(DISTINCT e.chunk_id)::bigint AS embedded_chunks,
                    max(i.created_at)::date::text      AS ingested_on,
                    string_agg(DISTINCT i.national_id, ', ') AS ids
             FROM jurisdictions j
             LEFT JOIN jurisdictions p       ON p.id = j.parent_id
             LEFT JOIN instruments i         ON i.jurisdiction_id = j.id
                                            AND i.instrument_type = 'country_report'
             LEFT JOIN legal_units u         ON u.instrument_id = i.id
             LEFT JOIN legal_unit_versions v ON v.legal_unit_id = u.id
             LEFT JOIN unit_texts t          ON t.version_id = v.id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id
             LEFT JOIN embeddings e          ON e.chunk_id = c.id
             GROUP BY 1 ORDER BY 1",
            &[],
        )
        .map_err(describe)?;

    // The params schema lives in this same DB but is created by
    // `nomoscope-workflow init-param-db`; absent it, report "not initialised"
    // rather than failing the whole stats call.
    let params_schema: bool = client
        .query_one("SELECT to_regclass('params.parameters') IS NOT NULL", &[])
        .map_err(describe)?
        .get(0);

    let params_by_country = if params_schema {
        client
            .query(
                "SELECT p.country,
                        count(DISTINCT p.id)::bigint AS parameters,
                        count(v.id)::bigint          AS model_values,
                        count(DISTINCT p.id) FILTER (WHERE p.temporal_basis = 'income_year')::bigint
                                                     AS income_year,
                        max(p.ingested_at)::date::text AS ingested_on,
                        string_agg(DISTINCT p.source_file, ', ') AS source_files
                 FROM params.parameters p
                 LEFT JOIN params.model_values v ON v.parameter_id = p.id
                 GROUP BY p.country ORDER BY p.country",
                &[],
            )
            .map_err(describe)?
    } else {
        Vec::new()
    };

    // Merge on country code, keyed off the jurisdictions list so a country
    // with neither input still shows a row; then the parameters of a country
    // that has no jurisdictions row yet.
    let mut parameters: Vec<(String, Value)> = Vec::new();
    for row in &params_by_country {
        let (code, rest) = split_key(row_to_json(row)?, "country");
        parameters.push((code, rest));
    }
    let mut inputs: Vec<Value> = Vec::new();
    for row in &country_reports {
        let (code, report) = split_key(row_to_json(row)?, "code");
        let params = parameters.iter().find(|(c, _)| *c == code).map(|(_, p)| p.clone());
        inputs.push(json!({ "code": code, "country_report": report, "parameters": params }));
    }
    for (code, params) in parameters {
        if !inputs.iter().any(|i| i["code"] == code.as_str()) {
            inputs.push(json!({ "code": code, "country_report": null, "parameters": params }));
        }
    }

    Ok(json!({
        "totals": row_to_json(&totals)?,
        "by_country": rows_to_json(&by_country)?,
        "languages": languages.iter().map(|r| r.get::<_, String>("lang")).collect::<Vec<_>>(),
        "embedding_models": rows_to_json(&models)?,
        "model_inputs": {
            "params_schema": params_schema,
            "by_country": inputs,
        },
    }))
}

/// Take `key` out of a row object: (its text, the rest of the row).
fn split_key(mut row: Value, key: &str) -> (String, Value) {
    let code = row
        .as_object_mut()
        .and_then(|o| o.remove(key))
        .and_then(|v| v.as_str().map(str::to_string))
        .unwrap_or_default();
    (code, row)
}

/// Instruments a contributed document could be said to implement.
///
/// Read-only, matching a fragment of the title or of the national id. Context
/// instruments are excluded: a Country Report describes the EUROMOD model, so
/// nothing implements one.
pub fn search_instruments(
    db_url: &str,
    country: &str,
    query: &str,
    limit: i64,
) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    let pattern = format!("%{}%", query.trim());
    let rows = client
        .query(
            "SELECT i.national_id,
                    i.instrument_type,
                    i.source_trust_class,
                    i.title_search           AS title,
                    i.publication_date::text AS publication_date
             FROM instruments i
             JOIN jurisdictions j ON j.id = i.jurisdiction_id
             WHERE (j.code = upper($1)
                    OR j.parent_id = (SELECT id FROM jurisdictions WHERE code = upper($1)))
               AND i.source_trust_class <> 'context'
               AND i.national_id IS NOT NULL
               AND (i.title_search ILIKE $2 OR i.national_id ILIKE $2)
             ORDER BY (i.national_id ILIKE $2) DESC, i.publication_date DESC NULLS LAST
             LIMIT $3",
            &[&country, &pattern, &limit],
        )
        .map_err(|e| format!("instrument search failed: {}", describe(e)))?;

    Ok(json!({ "instruments": rows_to_json(&rows)? }))
}

#[cfg(test)]
mod tests {
    fn url() -> String {
        std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string())
    }

    /// The statistics' row→JSON mapping against the live stack.
    #[test]
    fn stats_smoke() {
        if super::connect(&url()).is_err() {
            return;
        }
        let stats = match super::stats(&url()) {
            Ok(stats) => stats,
            // a container whose /dev/shm is too small for the parallel joins
            Err(e) if e.contains("shared memory") => return eprintln!("skipped: {e}"),
            Err(e) => panic!("stats failed: {e}"),
        };
        assert!(stats["totals"]["chunks"].is_i64());
        assert!(stats["by_country"].is_array());
        assert!(stats["model_inputs"]["by_country"].is_array());
    }

    #[test]
    fn instrument_search_excludes_context_instruments() {
        if super::connect(&url()).is_err() {
            return;
        }
        let result = super::search_instruments(&url(), "FR", "", 50).unwrap();

        let classes: Vec<String> = result["instruments"]
            .as_array()
            .unwrap()
            .iter()
            .map(|row| row["source_trust_class"].as_str().unwrap().to_string())
            .collect();
        assert!(!classes.contains(&"context".to_string()), "{classes:?}");
    }
}
