-- 0001 — source-trust class on every instrument (ADR 0001).
--
-- Fresh volumes get the column from schema.sql; a database that already holds a
-- corpus gets it from here, so a running installation needs no volume reset:
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0001_instrument_source_trust_class.sql
--
-- Idempotent: re-running it is a no-op.

BEGIN;

ALTER TABLE instruments
    ADD COLUMN IF NOT EXISTS source_trust_class text;

-- Backfill: Country Reports describe the EUROMOD model and are context; every
-- other instrument in a pre-feature database came from a country adapter, i.e.
-- national legislation, and is evidence.
UPDATE instruments
SET source_trust_class = CASE
        WHEN instrument_type = 'country_report' THEN 'context'
        ELSE 'evidence'
    END
WHERE source_trust_class IS NULL;

ALTER TABLE instruments
    ALTER COLUMN source_trust_class SET DEFAULT 'evidence',
    ALTER COLUMN source_trust_class SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'instruments_source_trust_class_check'
    ) THEN
        ALTER TABLE instruments
            ADD CONSTRAINT instruments_source_trust_class_check
            CHECK (source_trust_class IN ('evidence','guidance','context'));
    END IF;
END
$$;

COMMIT;
