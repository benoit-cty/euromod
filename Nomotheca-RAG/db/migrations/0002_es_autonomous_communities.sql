-- 0002 — Spain's autonomous communities as child jurisdictions of ES (ADR 0003).
--
-- Fresh volumes get the rows from seed.sql; a database that already holds a
-- corpus gets them from here, so a running installation needs no volume reset:
--
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation \
--     < Nomotheca-RAG/db/migrations/0002_es_autonomous_communities.sql
--
-- Idempotent: re-running it is a no-op. The rows are generated from
-- ingest/src/nomotheca_ingest/countries/es/regions.py and checked against it
-- by ingest/tests/test_es_regions.py.

BEGIN;

INSERT INTO jurisdictions (code, parent_id, name, official_langs, metadata) VALUES
  ('ES-AN', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Andalucía', '{es}', '{"nuts2": "ES61", "eli": "es-an", "boe_departamento": "Comunidad Autónoma de Andalucía"}'),
  ('ES-AR', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Aragón', '{es}', '{"nuts2": "ES24", "eli": "es-ar", "boe_departamento": "Comunidad Autónoma de Aragón"}'),
  ('ES-AS', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Principado de Asturias', '{es}', '{"nuts2": "ES12", "eli": "es-as", "boe_departamento": "Comunidad Autónoma del Principado de Asturias"}'),
  ('ES-CB', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Cantabria', '{es}', '{"nuts2": "ES13", "eli": "es-cb", "boe_departamento": "Comunidad Autónoma de Cantabria"}'),
  ('ES-CL', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Castilla y León', '{es}', '{"nuts2": "ES41", "eli": "es-cl", "boe_departamento": "Comunidad Autónoma de Castilla y León"}'),
  ('ES-CM', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Castilla-La Mancha', '{es}', '{"nuts2": "ES42", "eli": "es-cm", "boe_departamento": "Comunidad Autónoma de Castilla-La Mancha"}'),
  ('ES-CN', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Canarias', '{es}', '{"nuts2": "ES70", "eli": "es-cn", "boe_departamento": "Comunidad Autónoma de Canarias"}'),
  ('ES-CT', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Cataluña', '{es,ca}', '{"nuts2": "ES51", "eli": "es-ct", "boe_departamento": "Comunidad Autónoma de Cataluña"}'),
  ('ES-EX', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Extremadura', '{es}', '{"nuts2": "ES43", "eli": "es-ex", "boe_departamento": "Comunidad Autónoma de Extremadura"}'),
  ('ES-GA', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Galicia', '{es,gl}', '{"nuts2": "ES11", "eli": "es-ga", "boe_departamento": "Comunidad Autónoma de Galicia"}'),
  ('ES-IB', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Illes Balears', '{es,ca}', '{"nuts2": "ES53", "eli": "es-ib", "boe_departamento": "Comunidad Autónoma de las Illes Balears"}'),
  ('ES-MC', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Región de Murcia', '{es}', '{"nuts2": "ES62", "eli": "es-mc", "boe_departamento": "Comunidad Autónoma de la Región de Murcia"}'),
  ('ES-MD', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Comunidad de Madrid', '{es}', '{"nuts2": "ES30", "eli": "es-md", "boe_departamento": "Comunidad de Madrid"}'),
  ('ES-NC', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Comunidad Foral de Navarra', '{es,eu}', '{"nuts2": "ES22", "eli": "es-nc", "boe_departamento": "Comunidad Foral de Navarra"}'),
  ('ES-PV', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'País Vasco', '{es,eu}', '{"nuts2": "ES21", "eli": "es-pv", "boe_departamento": "Comunidad Autónoma del País Vasco"}'),
  ('ES-RI', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'La Rioja', '{es}', '{"nuts2": "ES23", "eli": "es-ri", "boe_departamento": "Comunidad Autónoma de La Rioja"}'),
  ('ES-VC', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Comunitat Valenciana', '{es,ca}', '{"nuts2": "ES52", "eli": "es-vc", "boe_departamento": "Comunitat Valenciana"}'),
  ('ES-CE', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Ceuta', '{es}', '{"nuts2": "ES63", "eli": "es-ce", "boe_departamento": "Ciudad de Ceuta"}'),
  ('ES-ML', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Melilla', '{es}', '{"nuts2": "ES64", "eli": "es-ml", "boe_departamento": "Ciudad de Melilla"}')
ON CONFLICT (code) DO UPDATE
SET parent_id      = EXCLUDED.parent_id,
    name           = EXCLUDED.name,
    official_langs = EXCLUDED.official_langs,
    metadata       = jurisdictions.metadata || EXCLUDED.metadata;

UPDATE jurisdictions
SET metadata = metadata || '{"regional_note": "comunidades autonomas are child jurisdictions (ISO 3166-2 codes, parent_id = ES); see the rows below and ADR 0003"}'::jsonb
WHERE code = 'ES';

-- Re-home the autonomous-community acts a pre-feature database filed under ES
-- (the ES parser now places them at ingest time). Two keys, either suffices:
-- the ELI jurisdiction segment, or BOE's departamento text.
UPDATE instruments i
SET jurisdiction_id = c.id
FROM jurisdictions es, jurisdictions c
WHERE es.code = 'ES'
  AND c.parent_id = es.id
  AND i.jurisdiction_id = es.id
  AND (
        i.eli ILIKE 'https://www.boe.es/eli/' || (c.metadata->>'eli') || '/%'
     OR i.metadata->>'departamento' = c.metadata->>'boe_departamento'
  );

-- Loud, not silent: an act BOE labels Autonómico that is still under ES would
-- sit in the state-law scope of every Spanish run. Add its community to
-- regions.py (and here) instead of letting the migration pass.
DO $$
DECLARE
    stray text;
BEGIN
    SELECT string_agg(i.national_id || ' (' || coalesce(i.metadata->>'departamento', '?') || ')', ', ')
    INTO stray
    FROM instruments i
    JOIN jurisdictions es ON es.id = i.jurisdiction_id AND es.code = 'ES'
    WHERE i.metadata->>'ambito_codigo' = '2';
    IF stray IS NOT NULL THEN
        RAISE EXCEPTION 'autonomous-community acts still filed under ES: %', stray;
    END IF;
END
$$;

COMMIT;
