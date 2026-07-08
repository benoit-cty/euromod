-- ============================================================================
-- Demo queries — exercises every retrieval capability of the schema.
-- Run:  docker exec -i euromod-legislation-db psql -U jrc -d legislation < demo_queries.sql
-- ============================================================================

\echo ''
\echo '=== (a) Point-in-time: FR CGI art. 197 as of 2024-06-01 vs 2025-06-01 ==='
SELECT '2024-06-01' AS as_of, v.source_version_id, left(t.content, 90) || '…' AS text_start
FROM legal_unit_versions v
JOIN unit_texts t ON t.version_id = v.id AND t.lang = 'fr'
WHERE v.legal_unit_id = 'c0000000-0000-4000-8000-000000000002'
  AND v.validity @> DATE '2024-06-01'
UNION ALL
SELECT '2025-06-01', v.source_version_id, left(t.content, 90) || '…'
FROM legal_unit_versions v
JOIN unit_texts t ON t.version_id = v.id AND t.lang = 'fr'
WHERE v.legal_unit_id = 'c0000000-0000-4000-8000-000000000002'
  AND v.validity @> DATE '2025-06-01';

\echo ''
\echo '=== (b) Citation fast path: fuzzy "CGI art 197" via pg_trgm, then as-of ==='
SELECT u.citation, similarity(u.citation, 'CGI art 197') AS sim,
       v.validity, v.source_version_id
FROM legal_units u
JOIN legal_unit_versions v ON v.legal_unit_id = u.id AND v.validity @> DATE '2025-06-01'
WHERE u.citation % 'CGI art 197'          -- trgm similarity operator
ORDER BY sim DESC
LIMIT 3;

\echo ''
\echo '=== (c) French FTS: stemmed + unaccented search over chunks ==='
SELECT u.citation, lower(v.validity) AS valid_from,
       ts_rank_cd(c.tsv, websearch_to_tsquery('fts_fr', 'fraction superieure impot revenu'), 32) AS rank
FROM chunks c
JOIN unit_texts t ON t.id = c.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u ON u.id = v.legal_unit_id
WHERE c.tsv @@ websearch_to_tsquery('fts_fr', 'fraction superieure impot revenu')
ORDER BY rank DESC;

\echo ''
\echo '=== (d) Belgium: both AUTHENTIC languages of CIR 92 art. 130 ==='
SELECT t.lang, t.authenticity, left(t.content, 80) || '…' AS text_start
FROM unit_texts t
WHERE t.version_id = 'd0000000-0000-4000-8000-000000000003'
ORDER BY t.lang;

\echo ''
\echo '=== (e) Vector top-5 (placeholder model 99; swap model_id=1 for bge-m3) ==='
SET hnsw.ef_search = 100;
SELECT u.citation, t.lang,
       (e.embedding <=> placeholder_embedding('tax brackets query'))::numeric(6,4) AS cos_dist
FROM embeddings e
JOIN chunks c ON c.id = e.chunk_id
JOIN unit_texts t ON t.id = c.unit_text_id
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u ON u.id = v.legal_unit_id
WHERE e.model_id = 99
ORDER BY e.embedding <=> placeholder_embedding('tax brackets query')
LIMIT 5;

\echo ''
\echo '=== (f) Hybrid retrieval: as_of + jurisdiction filter, FTS ∥ vector, RRF k=60 ==='
WITH candidate AS (
    SELECT c.id AS chunk_id, c.tsv
    FROM chunks c
    JOIN unit_texts t ON t.id = c.unit_text_id
    JOIN legal_unit_versions v ON v.id = t.version_id
    JOIN legal_units u ON u.id = v.legal_unit_id
    JOIN instruments i ON i.id = u.instrument_id
    JOIN jurisdictions j ON j.id = i.jurisdiction_id
    WHERE v.validity @> DATE '2025-06-01'
      AND j.code = 'FR'
      AND t.lang = 'fr'                       -- strategy (b): original-language leg
),
fts AS (
    SELECT chunk_id, row_number() OVER (ORDER BY
           ts_rank_cd(tsv, websearch_to_tsquery('fts_fr', 'barème impôt sur le revenu'), 32) DESC) AS r
    FROM candidate
    WHERE tsv @@ websearch_to_tsquery('fts_fr', 'barème impôt sur le revenu')
    LIMIT 50
),
vec AS (
    SELECT e.chunk_id, row_number() OVER (ORDER BY
           e.embedding <=> placeholder_embedding('barème impôt sur le revenu')) AS r
    FROM embeddings e
    JOIN candidate USING (chunk_id)
    WHERE e.model_id = 99
    LIMIT 50
)
SELECT ch.context_header,
       round((coalesce(1.0/(60+fts.r), 0) + coalesce(1.0/(60+vec.r), 0))::numeric, 5) AS rrf
FROM fts
FULL OUTER JOIN vec USING (chunk_id)
JOIN chunks ch ON ch.id = chunk_id
ORDER BY rrf DESC
LIMIT 5;

\echo ''
\echo '=== (g) rag:// URI resolution (the contract with the external parameter JSON) ==='
SELECT kind, citation, validity, lang, left(content, 60) || '…' AS content_start
FROM resolve_rag_uri('rag://unit/c0000000-0000-4000-8000-000000000002@2024-06-01');

SELECT kind, citation, lang, left(content, 60) || '…' AS content_start
FROM resolve_rag_uri('rag://chunk/' ||
       (SELECT id::text FROM chunks
        WHERE unit_text_id = 'e0000000-0000-4000-8000-000000000003' AND seq = 0));

\echo ''
\echo '=== (h) Impact analysis: which external parameters cite CGI art. 197? ==='
SELECT r.external_ref, r.external_kind, v.validity, u.citation
FROM citation_registry r
JOIN legal_unit_versions v ON v.id = r.cited_version_id
JOIN legal_units u ON u.id = v.legal_unit_id
WHERE u.id = 'c0000000-0000-4000-8000-000000000002';

\echo ''
\echo '=== (i) Provenance: every version traces to a snapshot; frozen labels ==='
SELECT u.citation, v.validity, s.url, s.retrieved_at::date, fr.frozen_label
FROM legal_unit_versions v
JOIN legal_units u ON u.id = v.legal_unit_id
JOIN fetch_snapshots s ON s.id = v.fetch_snapshot_id
JOIN fetch_runs fr ON fr.id = s.run_id
ORDER BY u.citation, v.validity;

\echo ''
\echo '=== (j) ltree subtree: everything under CGI Livre premier ==='
SELECT u.path, u.unit_type, u.citation
FROM legal_units u
WHERE u.path <@ 'liv_1'::ltree
ORDER BY u.path;

-- (k) Integrity demo — uncommenting this MUST fail with an exclusion violation:
-- a second consolidation of art. 197 overlapping 2024 cannot coexist.
-- INSERT INTO legal_unit_versions (legal_unit_id, validity, fetch_snapshot_id)
-- VALUES ('c0000000-0000-4000-8000-000000000002',
--         daterange('2024-06-01', '2024-12-31', '[)'),
--         'a0000000-0000-4000-8000-000000000001');
