-- 0007 — drop schema objects nothing reads or writes (code audit, dead code).
--
--   view current_legal_texts   no reader in any package, UI or doc
--   column instruments.in_force  never written; unit versions are the truth
--
-- Kept on purpose: resolve_rag_uri() (the documented rag:// contract with the
-- parameter JSON format), fetch_snapshots.storage_ref (large-PDF object store,
-- an open deployment question), fts_de (German texts, BE).
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0007_drop_unused_objects.sql
--
-- Idempotent.

DROP VIEW IF EXISTS current_legal_texts;
ALTER TABLE instruments DROP COLUMN IF EXISTS in_force;
