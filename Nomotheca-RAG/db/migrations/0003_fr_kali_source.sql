-- 0003 — the KALI base (collective agreements) as an FR source (ADR 0006).
--
-- Fresh volumes get the row from seed.sql; a database that already holds a
-- corpus gets it from here:
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0003_fr_kali_source.sql
--
-- Idempotent: re-running it is a no-op.

INSERT INTO sources (jurisdiction_id, code, name, base_url, id_system, supports_eli, supports_point_in_time, fetch_skill, terms)
VALUES ((SELECT id FROM jurisdictions WHERE code = 'FR'), 'FR-KALI',
        'Légifrance / DILA (base KALI, conventions collectives)', 'https://www.legifrance.gouv.fr', 'kali',
        false, true, 'skills/fr-legifrance',
        '{"bulk": "DILA open-data dumps only (global + daily increments); collective agreements are evidence (ADR 0006)"}')
ON CONFLICT (code) DO NOTHING;
