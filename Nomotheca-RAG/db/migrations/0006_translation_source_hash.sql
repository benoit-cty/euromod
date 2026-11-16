-- 0006 — machine translations remember which state of their source they translate
-- (code audit D10).
--
-- `translate run` now stamps every machine translation with
-- metadata.source_content_hash = its source text's content_hash, and treats a
-- translation whose stamp differs from the source's current hash as stale (a
-- `reparse` changed the source). This stamps the rows written before that with
-- their source's CURRENT hash: a translation that was already stale on
-- 16 Nov 2026 cannot be told apart and is not re-translated by this; every
-- later source change is.
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0006_translation_source_hash.sql
--
-- Idempotent.

UPDATE unit_texts e
   SET metadata = e.metadata || jsonb_build_object('source_content_hash', s.content_hash)
  FROM unit_texts s
 WHERE e.translation_of = s.id
   AND e.authenticity = 'machine_translation'
   AND NOT e.metadata ? 'source_content_hash';
