-- 0005 — a partial HNSW index for every registered embedding model (code audit D16).
--
-- Until 16 Nov 2026 only models 1 and 99 had one (seed.sql); `embeddings build
-- --model <key>` inserted the registry row and nothing else. The ingest now
-- creates the index with the row (core/embeddings.ensure_embedding_model);
-- this backfills the models registered before that. Note that the sanctioned
-- search shape (search_chunks) ranks exactly over the filtered candidates and
-- does not walk the index; it is kept for scale-out (pgvector iterative scans).
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0005_hnsw_every_model.sql
--
-- Idempotent.

DO $$
DECLARE m smallint;
BEGIN
    FOR m IN SELECT id FROM embedding_models ORDER BY id LOOP
        EXECUTE format(
            'CREATE INDEX IF NOT EXISTS emb_hnsw_m%s ON embeddings '
            'USING hnsw (embedding halfvec_cosine_ops) WITH (m = 16, ef_construction = 200) '
            'WHERE model_id = %s', m, m);
    END LOOP;
END $$;
