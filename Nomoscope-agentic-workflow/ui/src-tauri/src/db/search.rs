//! Article search and a hit's language renderings, for both desktop apps: the
//! review UI's Database tab and the RAG chat's search panel and source cards
//! (the chat compiles this file in with `#[path]`, so the two cannot drift).
//! Read-only.

use crate::pg::{connect, describe, rows_to_json};
use postgres::Client;
use serde_json::{json, Value};

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum SearchMode {
    Hybrid,
    FullText,
    Vector,
}

impl SearchMode {
    pub fn parse(value: &str) -> Result<Self, String> {
        match value {
            "hybrid" => Ok(Self::Hybrid),
            "full_text" => Ok(Self::FullText),
            "vector" => Ok(Self::Vector),
            _ => Err(format!("unsupported search mode: {value}")),
        }
    }

    pub fn uses_vector(self) -> bool {
        matches!(self, Self::Hybrid | Self::Vector)
    }

    fn uses_full_text(self) -> bool {
        matches!(self, Self::Hybrid | Self::FullText)
    }

    fn as_str(self) -> &'static str {
        match self {
            Self::Hybrid => "hybrid",
            Self::FullText => "full_text",
            Self::Vector => "vector",
        }
    }
}

/// What the Database tab (and the RAG chat's search box) sends.
#[derive(serde::Deserialize)]
pub struct SearchPayload {
    pub db_url: String,
    pub query: String,
    pub country: Option<String>,
    pub as_of: Option<String>,
    pub languages: Option<Vec<String>>,
    pub mode: Option<String>,
    pub limit: Option<i64>,
}

/// The embedding model the corpus is searched with (`embedding_models.is_default`).
pub fn default_model_id(client: &mut Client) -> Result<i32, String> {
    client
        .query_opt(
            "SELECT id::int FROM embedding_models WHERE is_default ORDER BY id LIMIT 1",
            &[],
        )
        .map_err(|e| format!("embedding model lookup failed: {}", describe(e)))?
        .map(|row| row.get::<_, i32>(0))
        .ok_or_else(|| "no default embedding model in embedding_models".to_string())
}

/// Article search for both desktop apps. Vector and hybrid modes need the
/// query encoded by the worker (an `encode` job, with the corpus's default
/// model); when no worker is alive the search degrades to full text and says
/// so in `notice`, rather than failing.
pub fn search(payload: &SearchPayload, default_limit: i64) -> Result<Value, String> {
    let mut mode = SearchMode::parse(payload.mode.as_deref().unwrap_or("hybrid"))?;
    let model_id = default_model_id(&mut connect(&payload.db_url)?)?;
    let mut notice: Option<String> = None;
    let query_vector = if mode.uses_vector() {
        match crate::jobs::encode_query(&crate::jobs::EncodePayload {
            db_url: payload.db_url.clone(),
            query: payload.query.clone(),
            sentences: None,
            model_id: Some(model_id),
        }) {
            Ok(result) => Some(
                result
                    .get("halfvec")
                    .and_then(Value::as_str)
                    .filter(|v| v.starts_with('[') && v.ends_with(']'))
                    .ok_or("encode job returned no halfvec")?
                    .to_string(),
            ),
            Err(e) if e == crate::jobs::NO_WORKER => {
                notice = Some(format!("{e}; showing full-text results instead"));
                mode = SearchMode::FullText;
                None
            }
            Err(e) => return Err(e),
        }
    } else {
        None
    };
    let mut result = search_articles(
        &payload.db_url,
        &payload.query,
        payload.country.as_deref(),
        payload.as_of.as_deref(),
        payload.languages.as_deref(),
        mode,
        query_vector.as_deref(),
        model_id,
        payload.limit.unwrap_or(default_limit),
    )?;
    result["notice"] = json!(notice);
    Ok(result)
}

/// Search law chunks with the database's `search_chunks()` — the one hybrid
/// search the workflow, the eval and the MCP server use too (live version on
/// `as_of`, OR-of-terms FTS, RRF + vector top-3 slot, vector leg ranked over
/// the filtered set, never through HNSW). This page browses, so Country
/// Reports are included; every hit carries its `source_trust_class`.
#[allow(clippy::too_many_arguments)]
pub fn search_articles(
    db_url: &str,
    query: &str,
    country: Option<&str>,
    as_of: Option<&str>,
    languages: Option<&[String]>,
    mode: SearchMode,
    query_vector: Option<&str>,
    model_id: i32,
    limit: i64,
) -> Result<Value, String> {
    if query.trim().is_empty() {
        return Err("query must not be empty".to_string());
    }
    if !(1..=50).contains(&limit) {
        return Err("limit must be between 1 and 50".to_string());
    }
    if mode.uses_vector() && query_vector.is_none() {
        return Err(format!("{} search requires a query vector", mode.as_str()));
    }

    let mut client = connect(db_url)?;
    client
        .batch_execute(
            "SET default_transaction_read_only = on;
             SET statement_timeout = '30s';",
        )
        .map_err(describe)?;
    let language_filter = languages.map(|values| values.to_vec());
    let use_full_text = mode.uses_full_text();
    let use_vector = mode.uses_vector();
    let vector = if use_vector { query_vector } else { None };
    let rows = client
        .query(
            "WITH found AS (
                SELECT s.*, t.version_id, ch.seq,
                       row_number() OVER (
                           PARTITION BY t.version_id, ch.seq
                           ORDER BY s.score DESC, s.chunk_id
                       ) AS rendering_rank
                FROM search_chunks(
                        $1, $5::text::halfvec(1024), $8,
                        CASE WHEN $2::text IS NULL THEN NULL ELSE jurisdiction_tree($2) END,
                        $4::text[], ($3::text)::date, ($7::bigint * 4)::int, $6, true) s
                JOIN chunks ch    ON ch.id = s.chunk_id
                JOIN unit_texts t ON t.id = ch.unit_text_id
             )
             SELECT d.chunk_id::text, u.citation, ch.context_header, ch.content,
                    CASE WHEN $6 THEN ts_headline(ch.search_config, ch.content,
                              websearch_to_tsquery(ch.search_config, fts_or_query($1)),
                              'StartSel=<<HL>>, StopSel=<</HL>>, HighlightAll=true')
                    END AS headline,
                    t.lang, t.authenticity, v.validity::text, v.version_status,
                    j.code AS country, i.title AS instrument_title, i.source_trust_class,
                    d.score,
                    d.fts_rank AS full_text_rank,
                    d.fts_score AS full_text_score,
                    coalesce(1.0 / (60 + d.fts_rank), 0)::float8 AS full_text_contribution,
                    d.vec_rank AS vector_rank,
                    d.vec_distance AS vector_distance,
                    coalesce(1.0 / (60 + d.vec_rank), 0)::float8 AS vector_contribution
             FROM found d
             JOIN chunks ch             ON ch.id = d.chunk_id
             JOIN unit_texts t          ON t.id = ch.unit_text_id
             JOIN legal_unit_versions v ON v.id = t.version_id
             JOIN legal_units u         ON u.id = v.legal_unit_id
             JOIN instruments i         ON i.id = u.instrument_id
             JOIN jurisdictions j       ON j.id = i.jurisdiction_id
             WHERE d.rendering_rank = 1
             ORDER BY d.score DESC, d.chunk_id
             LIMIT $7::bigint",
            &[
                &query,
                &country,
                &as_of,
                &language_filter,
                &vector,
                &use_full_text,
                &limit,
                &model_id,
            ],
        )
        .map_err(describe)?;

    Ok(json!({
        "query": query,
        "mode": mode.as_str(),
        "model_id": if use_vector { Some(model_id) } else { None },
        "ranking": if mode == SearchMode::Hybrid {
            "RRF(k=60) over full-text and vector ranks, vector top 3 guaranteed"
        } else if mode == SearchMode::Vector {
            "vector rank"
        } else {
            "full-text rank"
        },
        "filters": {
            "country": country,
            "as_of": as_of,
            "languages": language_filter,
        },
        // `headline` is `content` with every query lexeme wrapped in
        // <<HL>>…<</HL>> (null in vector-only mode); the UI turns the markers
        // into marks.
        "results": rows_to_json(&rows)?,
    }))
}

/// Every language rendering of the legal-unit version a cited chunk belongs to.
///
/// A chunk hangs off one `unit_texts` row = one language rendering of one
/// version; the sibling renderings (authentic BE fr/nl, official or machine
/// translations) are the other `unit_texts` rows of the same `version_id`.
/// Translations are chunked independently, so the sibling chunk is matched on
/// `seq` and we fall back to the full version text when there is none.
pub fn chunk_renderings(db_url: &str, chunk_id: &str) -> Result<Value, String> {
    let mut client = connect(db_url)?;
    client
        .batch_execute(
            "SET default_transaction_read_only = on;
             SET statement_timeout = '15s';",
        )
        .map_err(describe)?;
    let rows = client
        .query(
            "SELECT t.id::text                     AS unit_text_id,
                    t.lang,
                    t.authenticity,
                    t.mt_engine,
                    t.source_lang,
                    c.id::text                     AS chunk_id,
                    c.seq,
                    coalesce(c.content, t.content) AS content,
                    (c.id IS NOT NULL)             AS aligned,
                    (t.id = src_text.id)           AS is_cited,
                    u.citation,
                    v.validity::text               AS validity
             FROM chunks src
             JOIN unit_texts src_text        ON src_text.id = src.unit_text_id
             JOIN unit_texts t               ON t.version_id = src_text.version_id
             JOIN legal_unit_versions v      ON v.id = t.version_id
             JOIN legal_units u              ON u.id = v.legal_unit_id
             LEFT JOIN chunks c              ON c.unit_text_id = t.id AND c.seq = src.seq
             WHERE src.id = ($1::text)::uuid
             ORDER BY (t.id = src_text.id) DESC,
                      (t.authenticity = 'authentic') DESC,
                      t.lang",
            &[&chunk_id],
        )
        .map_err(|e| format!("chunk renderings query failed: {}", describe(e)))?;

    Ok(json!({
        "chunk_id": chunk_id,
        // `aligned` false = no chunk with this seq in that language: the full
        // version text is shown.
        "renderings": rows_to_json(&rows)?,
    }))
}

#[cfg(test)]
mod tests {
    use super::SearchMode;

    fn url() -> String {
        std::env::var("WORKFLOW_DATABASE_URL")
            .unwrap_or_else(|_| "postgresql://jrc:jrc@localhost:5434/legislation".to_string())
    }

    #[test]
    fn validates_search_modes() {
        assert_eq!(SearchMode::parse("hybrid").unwrap(), SearchMode::Hybrid);
        assert_eq!(
            SearchMode::parse("full_text").unwrap(),
            SearchMode::FullText
        );
        assert_eq!(SearchMode::parse("vector").unwrap(), SearchMode::Vector);
        assert!(SearchMode::parse("semantic").is_err());
    }

    #[test]
    fn search_queries_smoke() {
        let url = url();
        let Ok(mut client) = super::connect(&url) else {
            return;
        };
        let vector: String = client
            .query_one(
                "SELECT placeholder_embedding($1)::text",
                &[&"income tax brackets"],
            )
            .unwrap()
            .get(0);

        for mode in [SearchMode::FullText, SearchMode::Vector, SearchMode::Hybrid] {
            let query_vector = mode.uses_vector().then_some(vector.as_str());
            let result = super::search_articles(
                &url,
                "income tax brackets",
                None,
                Some("2025-06-01"),
                None,
                mode,
                query_vector,
                99,
                5,
            )
            .unwrap_or_else(|error| panic!("{} search failed: {error}", mode.as_str()));
            assert!(result["results"].is_array());
        }
    }
}
