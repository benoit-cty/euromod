-- 0004 — one hybrid search for every caller (code audit 2.1, D2, D9).
--
-- Before this, hybrid retrieval was written four times (workflow, eval, review
-- UI, MCP server) and the copies had drifted: the MCP copy returned Country
-- Report chunks as citable, the UI and MCP copies ANDed every query term, used
-- plain RRF, no live-version filter, and ordered by `embedding <=> q` beside
-- filters (the shape that walks the HNSW index over the whole corpus and
-- filters the 40 nearest afterwards). All four now call search_chunks().
--
-- Fresh volumes get these from schema.sql; an existing database from here:
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0004_search_chunks.sql
--
-- Idempotent: CREATE OR REPLACE.

-- OR of the distinct words of two characters or more, in websearch syntax.
-- A framed query is long and often bilingual; websearch_to_tsquery ANDs every
-- term, so no chunk satisfies it. OR them and let ts_rank_cd surface the
-- chunks matching most of them. A query with no word is returned as given.
CREATE OR REPLACE FUNCTION fts_or_query(q text) RETURNS text
LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
$$
    SELECT coalesce(string_agg(DISTINCT w, ' OR '), q)
    FROM (SELECT (regexp_matches(lower(q), '\w{2,}', 'g'))[1] AS w) words
    WHERE w <> 'or'
$$;

-- A country and its child jurisdictions (Spain's autonomous communities,
-- ADR 0003) — the scope of a search that names a country but no region. A
-- child code is its own scope.
CREATE OR REPLACE FUNCTION jurisdiction_tree(code text) RETURNS text[]
LANGUAGE sql STABLE PARALLEL SAFE AS
$$
    SELECT array_agg(j.code ORDER BY j.parent_id NULLS FIRST, j.code)
    FROM jurisdictions j
    WHERE j.code = upper($1)
       OR j.parent_id = (SELECT id FROM jurisdictions WHERE jurisdictions.code = upper($1))
$$;

-- Hybrid search: FTS top-N || vector top-N, fused by Reciprocal Rank Fusion
-- (k = 60) plus a guaranteed slot for the vector top 3 (ts_rank_cd has no IDF,
-- so common fiscal terms let long amending acts crowd the FTS leg, and a chunk
-- ranked first by the vector leg alone would otherwise lose the fusion).
--
--   p_qvec NULL         FTS only;  p_use_fts false: vector only
--   p_jurisdictions     exact codes (see jurisdiction_tree); NULL = all
--   p_langs             NULL = every language
--   p_as_of             the version in force that day, one per unit (the one
--                       with the latest start: Legifrance can leave two open
--                       versions of one article side by side); NULL = every
--                       version
--   p_include_context   'context' corpora (Country Reports) are never
--                       evidence (ADR 0001); only a browsing UI may ask for them
--
-- The vector leg ranks inside a window function over the filtered candidates,
-- never by `ORDER BY embedding <=> q` beside filters: that shape lets the
-- planner walk a model's HNSW index over the whole corpus and filter the 40
-- nearest afterwards (2 Lithuanian rows out of 15).
CREATE OR REPLACE FUNCTION search_chunks(
    p_query           text,
    p_qvec            halfvec(1024),
    p_model_id        integer,
    p_jurisdictions   text[]  DEFAULT NULL,
    p_langs           text[]  DEFAULT NULL,
    p_as_of           date    DEFAULT NULL,
    p_k               integer DEFAULT 8,
    p_use_fts         boolean DEFAULT true,
    p_include_context boolean DEFAULT false,
    p_candidates      integer DEFAULT 50
) RETURNS TABLE (chunk_id uuid, score float8, fts_rank bigint, fts_score float8,
                 vec_rank bigint, vec_distance float8)
LANGUAGE sql STABLE PARALLEL SAFE AS
$$
WITH live_version AS MATERIALIZED (
    SELECT DISTINCT ON (i.id, coalesce(u.citation, u.id::text),
                        CASE WHEN p_as_of IS NULL THEN v.id END)
           v.id AS version_id
    FROM legal_unit_versions v
    JOIN legal_units u   ON u.id = v.legal_unit_id
    JOIN instruments i   ON i.id = u.instrument_id
    JOIN jurisdictions j ON j.id = i.jurisdiction_id
    WHERE (p_as_of IS NULL OR v.validity @> p_as_of)
      AND (p_jurisdictions IS NULL OR j.code = ANY(p_jurisdictions))
      AND (p_include_context OR i.source_trust_class <> 'context')
    ORDER BY i.id, coalesce(u.citation, u.id::text),
             CASE WHEN p_as_of IS NULL THEN v.id END, lower(v.validity) DESC
),
candidate AS MATERIALIZED (
    SELECT c.id AS chunk_id, c.tsv, c.search_config
    FROM chunks c
    JOIN unit_texts t    ON t.id = c.unit_text_id
    JOIN live_version lv ON lv.version_id = t.version_id
    WHERE p_langs IS NULL OR t.lang = ANY(p_langs)
),
fts AS (
    SELECT chunk_id, row_number() OVER (ORDER BY s DESC, chunk_id) AS r, s
    FROM (
        -- 1|32: log-length normalisation, then rank/(rank+1). Without the
        -- length term, long amending acts that repeat common fiscal words
        -- outrank the short implementing act that actually sets the value.
        SELECT chunk_id,
               ts_rank_cd(tsv, websearch_to_tsquery(search_config, fts_or_query(p_query)), 1|32)::float8 AS s
        FROM candidate
        WHERE p_use_fts AND tsv @@ websearch_to_tsquery(search_config, fts_or_query(p_query))
    ) ranked
    ORDER BY r
    LIMIT greatest(p_candidates, p_k)
),
vec AS (
    SELECT chunk_id, row_number() OVER (ORDER BY d, chunk_id) AS r, d
    FROM (
        SELECT e.chunk_id, (e.embedding <=> p_qvec)::float8 AS d
        FROM embeddings e
        JOIN candidate USING (chunk_id)
        WHERE p_qvec IS NOT NULL AND e.model_id = p_model_id
    ) ranked
    ORDER BY r
    LIMIT greatest(p_candidates, p_k)
)
SELECT chunk_id,
       (coalesce(1.0 / (60 + fts.r), 0) + coalesce(1.0 / (60 + vec.r), 0)
        + CASE WHEN vec.r <= 3 THEN 1.0 ELSE 0 END)::float8 AS score,
       fts.r, fts.s, vec.r, vec.d
FROM fts FULL OUTER JOIN vec USING (chunk_id)
ORDER BY 2 DESC, chunk_id
LIMIT p_k
$$;
