-- ============================================================================
-- Seed data — reference rows every database needs
-- ============================================================================
--   * the embedding model registry (1 = bge-m3, 99 = the in-SQL placeholder
--     the demo corpus and some tests use) and their HNSW indexes;
--   * placeholder_embedding(), the deterministic demo embedder;
--   * jurisdictions (with Spain's autonomous communities) and sources.
-- The demo corpus that used to sit here (a hand-written CGI art. 197, BE CIR 92
-- art. 130, one article per country) is now db/demo.sql, applied only on
-- request: in a real database it competed with the ingested texts (code audit
-- 2.3). Load it with
--   docker exec -i nomotheca-legislation-db psql -U jrc -d legislation < Nomotheca-RAG/db/demo.sql
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Embedding model registry + HNSW indexes
-- ----------------------------------------------------------------------------
INSERT INTO embedding_models (id, name, provider, native_dim, stored_dim, normalize, is_default, config) VALUES
  (1,  'bge-m3',           'self-hosted', 1024, 1024, true, true,  '{"context": 8192}'),
  (99, 'placeholder-demo', 'seed',        1024, 1024, true, false, '{"note": "deterministic md5-based vectors, DEMO ONLY"}');

CREATE INDEX emb_hnsw_m1 ON embeddings
    USING hnsw (embedding halfvec_cosine_ops)
    WITH (m = 16, ef_construction = 200)
    WHERE model_id = 1;

CREATE INDEX emb_hnsw_m99 ON embeddings
    USING hnsw (embedding halfvec_cosine_ops)
    WITH (m = 16, ef_construction = 200)
    WHERE model_id = 99;

-- Deterministic pseudo-embedding: 1024 fp16 components derived from md5(seed, i).
-- DEMO ONLY — replace with a real encoder in any evaluation.
CREATE FUNCTION placeholder_embedding(seed text) RETURNS halfvec(1024)
LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
$$
SELECT ('[' || string_agg(
           ((('x' || substr(md5(seed || ':' || i::text), 1, 8))::bit(32)::int)::double precision
             / 2147483648.0)::text,
           ',' ORDER BY i)
        || ']')::halfvec(1024)
FROM generate_series(1, 1024) AS i
$$;

-- ----------------------------------------------------------------------------
-- Jurisdictions & sources
-- ----------------------------------------------------------------------------
INSERT INTO jurisdictions (code, name, official_langs, metadata) VALUES
  ('FR', 'France',      '{fr}',       '{}'),
  ('NL', 'Netherlands', '{nl}',       '{}'),
  ('LT', 'Lithuania',   '{lt}',       '{}'),
  ('ES', 'Spain',       '{es}',       '{"regional_note": "comunidades autonomas are child jurisdictions (ISO 3166-2 codes, parent_id = ES); see the rows below and ADR 0003"}'),
  ('IE', 'Ireland',     '{en,ga}',    '{}'),
  ('BE', 'Belgium',     '{fr,nl,de}', '{"authenticity_note": "federal law is authentic in fr and nl (de for some texts)"}');

-- Spain's autonomous communities: child jurisdictions of ES, ISO 3166-2 codes.
-- A regional act is ingested under its community, so evidence retrieval can
-- scope a regional EUROMOD parameter — NUTS-2 code in its name, e.g.
-- $bsarg_rg24_* = ES24 = ES-AR — to state law plus that community's law and
-- nothing else (ADR 0003). metadata: nuts2 (the parameter-side key), eli (the
-- ELI jurisdiction segment BOE uses), boe_departamento (BOE's name for the
-- enacting body). Mirror of ingest/src/nomotheca_ingest/countries/es/regions.py;
-- ingest/tests/test_es_regions.py fails when the two drift apart.
INSERT INTO jurisdictions (code, parent_id, name, official_langs, metadata) VALUES
  ('ES-AN', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Andalucía', '{es}', '{"nuts2": "ES61", "eli": "es-an", "boe_departamento": "Comunidad Autónoma de Andalucía"}'),
  ('ES-AR', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Aragón', '{es}', '{"nuts2": "ES24", "eli": "es-ar", "boe_departamento": "Comunidad Autónoma de Aragón"}'),
  ('ES-AS', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Principado de Asturias', '{es}', '{"nuts2": "ES12", "eli": "es-as", "boe_departamento": "Comunidad Autónoma del Principado de Asturias"}'),
  ('ES-CB', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Cantabria', '{es}', '{"nuts2": "ES13", "eli": "es-cb", "boe_departamento": "Comunidad Autónoma de Cantabria"}'),
  ('ES-CL', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Castilla y León', '{es}', '{"nuts2": "ES41", "eli": "es-cl", "boe_departamento": "Comunidad de Castilla y León"}'),
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
  ('ES-ML', (SELECT id FROM jurisdictions WHERE code = 'ES'), 'Melilla', '{es}', '{"nuts2": "ES64", "eli": "es-ml", "boe_departamento": "Ciudad de Melilla"}');

INSERT INTO sources (jurisdiction_id, code, name, base_url, id_system, supports_eli, supports_point_in_time, fetch_skill, terms) VALUES
  ((SELECT id FROM jurisdictions WHERE code = 'FR'), 'FR-LEGI',   'Légifrance / DILA (base LEGI)',            'https://www.legifrance.gouv.fr', 'legi',           true,  true,  'skills/fr-legifrance', '{"bulk": "DILA open-data dumps preferred over scraping (Anubis anti-bot)"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'FR'), 'FR-KALI',   'Légifrance / DILA (base KALI, conventions collectives)', 'https://www.legifrance.gouv.fr', 'kali', false, true, 'skills/fr-legifrance', '{"bulk": "DILA open-data dumps only (global + daily increments); collective agreements are evidence (ADR 0006)"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'NL'), 'NL-BWB',    'wetten.overheid.nl (BWB)',                 'https://wetten.overheid.nl',     'bwb_juriconnect', false, true,  'skills/nl-bwb',        '{"note": "Juriconnect identifiers, geldigheidsdatum for point-in-time"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'NL'), 'NL-STCRT',  'Staatscourant (officielebekendmakingen.nl)', 'https://zoek.officielebekendmakingen.nl', 'stcrt', false, false, 'skills/nl-bwb',        '{"note": "publications as published, one XML per stcrt id; regulations and notices only. A later notice replaces the amounts without marking the older one. The explanatory note is filed as a guidance instrument"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'LT'), 'LT-TAR',    'e-seimas / Teisės aktų registras (TAR)',   'https://www.e-tar.lt',           'tar',            true,  true,  'skills/lt-tar',        '{"note": "suvestines redakcijos = dated consolidations"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'ES'), 'ES-BOE',    'Boletín Oficial del Estado (consolidado)', 'https://www.boe.es',             'boe',            true,  true,  'skills/es-boe',        '{}'),
  ((SELECT id FROM jurisdictions WHERE code = 'IE'), 'IE-EISB',   'electronic Irish Statute Book',            'https://www.irishstatutebook.ie','eisb',           true,  false, 'skills/ie-eisb',       '{"note": "as-enacted text only; no consolidation and no query API. LRC Revised Acts do not cover the Taxes Consolidation Act 1997 at all (verified 2026-08-04)"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'IE'), 'IE-LRC',    'Law Reform Commission, Revised Acts',      'https://revisedacts.lawreform.ie','eisb',          true,  false, 'skills/ie-eisb',       '{"note": "administrative consolidation of about 580 acts, one HTML page per act, current state only; a section is dated by its latest F-note. Covers the Social Welfare Consolidation Act 2005, not the Taxes Consolidation Act 1997"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'IE'), 'IE-OIREACHTAS', 'Houses of the Oireachtas Open Data API', 'https://api.oireachtas.ie',    'oireachtas',     true,  false, 'skills/ie-eisb',       '{"note": "resolver only: act year/title -> actNo + statutebookURI (the eISB ELI). Serves no legal text."}'),
  ((SELECT id FROM jurisdictions WHERE code = 'BE'), 'BE-JUSTEL', 'Justel / Moniteur belge',                  'https://www.ejustice.just.fgov.be','justel_numac',   false, false, 'skills/be-justel',     '{"note": "numac identifiers; ELI partially deployed"}');
