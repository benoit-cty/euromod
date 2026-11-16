-- 0008 — record which migrations a database has (code audit 2.3).
--
-- schema.sql builds a fresh database at the latest state and records every
-- migration as applied; an existing database runs `make migrate`, which
-- applies, in order, each migrations/*.sql not yet in this table and records
-- it. This file records 0001–0008 for databases that applied them by hand.
--
-- Idempotent.

CREATE TABLE IF NOT EXISTS schema_migrations (
    name       text PRIMARY KEY,
    applied_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO schema_migrations (name) VALUES
  ('0001_instrument_source_trust_class'),
  ('0002_es_autonomous_communities'),
  ('0003_fr_kali_source'),
  ('0004_search_chunks'),
  ('0005_hnsw_every_model'),
  ('0006_translation_source_hash'),
  ('0007_drop_unused_objects'),
  ('0008_schema_migrations')
ON CONFLICT (name) DO NOTHING;
