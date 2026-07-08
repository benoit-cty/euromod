-- ============================================================================
-- Seed data — demo corpus for the 6 pilot countries (FR, NL, LT, ES, IE, BE)
-- ============================================================================
-- Purposes:
--   * FR Art. 197 CGI with TWO dated versions -> point-in-time demo, matching
--     the thresholds used in Param_Schema/parameter_sample.jsonc (11 294 / 11 497).
--   * BE Art. 130 CIR 92 with FR + NL AUTHENTIC texts -> multilingual-authentic demo.
--   * One representative income-tax-rate article per remaining country.
--   * Deterministic PLACEHOLDER embeddings (model 99) so vector/hybrid queries
--     run without an embedding service. Real embeddings go under model 1 (bge-m3).
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
  ('ES', 'Spain',       '{es}',       '{"regional_note": "comunidades autonomas join later as child jurisdictions (ISO 3166-2)"}'),
  ('IE', 'Ireland',     '{en,ga}',    '{}'),
  ('BE', 'Belgium',     '{fr,nl,de}', '{"authenticity_note": "federal law is authentic in fr and nl (de for some texts)"}');

INSERT INTO sources (jurisdiction_id, code, name, base_url, id_system, supports_eli, supports_point_in_time, fetch_skill, terms) VALUES
  ((SELECT id FROM jurisdictions WHERE code = 'FR'), 'FR-LEGI',   'Légifrance / DILA (base LEGI)',            'https://www.legifrance.gouv.fr', 'legi',           true,  true,  'skills/fr-legifrance', '{"bulk": "DILA open-data dumps preferred over scraping (Anubis anti-bot)"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'NL'), 'NL-BWB',    'wetten.overheid.nl (BWB)',                 'https://wetten.overheid.nl',     'bwb_juriconnect', false, true,  'skills/nl-bwb',        '{"note": "Juriconnect identifiers, geldigheidsdatum for point-in-time"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'LT'), 'LT-TAR',    'e-seimas / Teisės aktų registras (TAR)',   'https://www.e-tar.lt',           'tar',            true,  true,  'skills/lt-tar',        '{"note": "suvestines redakcijos = dated consolidations"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'ES'), 'ES-BOE',    'Boletín Oficial del Estado (consolidado)', 'https://www.boe.es',             'boe',            true,  true,  'skills/es-boe',        '{}'),
  ((SELECT id FROM jurisdictions WHERE code = 'IE'), 'IE-EISB',   'electronic Irish Statute Book',            'https://www.irishstatutebook.ie','eisb',           true,  false, 'skills/ie-eisb',       '{"note": "revised acts via Law Reform Commission; historical consolidation limited"}'),
  ((SELECT id FROM jurisdictions WHERE code = 'BE'), 'BE-JUSTEL', 'Justel / Moniteur belge',                  'https://www.ejustice.just.fgov.be','justel_numac',   false, false, 'skills/be-justel',     '{"note": "numac identifiers; ELI partially deployed"}');

-- ----------------------------------------------------------------------------
-- Fetch provenance (one bulk_seed run per source; one snapshot per fetched page)
-- ----------------------------------------------------------------------------
INSERT INTO fetch_runs (id, source_id, skill_version, trigger, finished_at, status, frozen_label) VALUES
  ('f0000000-0000-4000-8000-000000000001', (SELECT id FROM sources WHERE code = 'FR-LEGI'),   'seed-demo-0.1', 'bulk_seed', now(), 'succeeded', 'seed-demo'),
  ('f0000000-0000-4000-8000-000000000002', (SELECT id FROM sources WHERE code = 'NL-BWB'),    'seed-demo-0.1', 'bulk_seed', now(), 'succeeded', 'seed-demo'),
  ('f0000000-0000-4000-8000-000000000003', (SELECT id FROM sources WHERE code = 'LT-TAR'),    'seed-demo-0.1', 'bulk_seed', now(), 'succeeded', 'seed-demo'),
  ('f0000000-0000-4000-8000-000000000004', (SELECT id FROM sources WHERE code = 'ES-BOE'),    'seed-demo-0.1', 'bulk_seed', now(), 'succeeded', 'seed-demo'),
  ('f0000000-0000-4000-8000-000000000005', (SELECT id FROM sources WHERE code = 'IE-EISB'),   'seed-demo-0.1', 'bulk_seed', now(), 'succeeded', 'seed-demo'),
  ('f0000000-0000-4000-8000-000000000006', (SELECT id FROM sources WHERE code = 'BE-JUSTEL'), 'seed-demo-0.1', 'bulk_seed', now(), 'succeeded', 'seed-demo');

INSERT INTO fetch_snapshots (id, run_id, source_id, url, http_status, content_type, content_hash, raw_content) VALUES
  ('a0000000-0000-4000-8000-000000000001', 'f0000000-0000-4000-8000-000000000001', (SELECT id FROM sources WHERE code = 'FR-LEGI'),   'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047850595', 200, 'text/html', encode(sha256(convert_to('demo FR art197 v2024', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8')),
  ('a0000000-0000-4000-8000-000000000002', 'f0000000-0000-4000-8000-000000000001', (SELECT id FROM sources WHERE code = 'FR-LEGI'),   'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051200000', 200, 'text/html', encode(sha256(convert_to('demo FR art197 v2025', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8')),
  ('a0000000-0000-4000-8000-000000000003', 'f0000000-0000-4000-8000-000000000002', (SELECT id FROM sources WHERE code = 'NL-BWB'),    'https://wetten.overheid.nl/BWBR0011353/2025-01-01#Hoofdstuk2_Artikel2.10', 200, 'text/html', encode(sha256(convert_to('demo NL art2.10', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8')),
  ('a0000000-0000-4000-8000-000000000004', 'f0000000-0000-4000-8000-000000000003', (SELECT id FROM sources WHERE code = 'LT-TAR'),    'https://www.e-tar.lt/portal/lt/legalAct/TAR.C677663D2202/asr', 200, 'text/html', encode(sha256(convert_to('demo LT 6str', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8')),
  ('a0000000-0000-4000-8000-000000000005', 'f0000000-0000-4000-8000-000000000004', (SELECT id FROM sources WHERE code = 'ES-BOE'),    'https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764#a63', 200, 'text/html', encode(sha256(convert_to('demo ES art63', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8')),
  ('a0000000-0000-4000-8000-000000000006', 'f0000000-0000-4000-8000-000000000005', (SELECT id FROM sources WHERE code = 'IE-EISB'),   'https://www.irishstatutebook.ie/eli/1997/act/39/section/15/enacted/en/html', 200, 'text/html', encode(sha256(convert_to('demo IE s15', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8')),
  ('a0000000-0000-4000-8000-000000000007', 'f0000000-0000-4000-8000-000000000006', (SELECT id FROM sources WHERE code = 'BE-JUSTEL'), 'https://www.ejustice.just.fgov.be/eli/loi/1992/04/10/1992003455/justel#Art.130', 200, 'text/html', encode(sha256(convert_to('demo BE art130', 'UTF8')), 'hex'), convert_to('demo snapshot payload', 'UTF8'));

-- ----------------------------------------------------------------------------
-- Instruments
-- ----------------------------------------------------------------------------
INSERT INTO instruments (id, jurisdiction_id, source_id, instrument_type, eli, national_id, title, publication_date, metadata) VALUES
  ('b0000000-0000-4000-8000-000000000001', (SELECT id FROM jurisdictions WHERE code = 'FR'), (SELECT id FROM sources WHERE code = 'FR-LEGI'),
   'code', NULL, 'LEGITEXT000006069577',
   '{"fr": "Code général des impôts", "en": "General Tax Code"}', '1950-04-30',
   '{"legi_nature": "CODE"}'),
  ('b0000000-0000-4000-8000-000000000002', (SELECT id FROM jurisdictions WHERE code = 'BE'), (SELECT id FROM sources WHERE code = 'BE-JUSTEL'),
   'code', 'https://www.ejustice.just.fgov.be/eli/loi/1992/04/10/1992003455', '1992003455',
   '{"fr": "Code des impôts sur les revenus 1992", "nl": "Wetboek van de inkomstenbelastingen 1992"}', '1992-07-30',
   '{"numac": "1992003455"}'),
  ('b0000000-0000-4000-8000-000000000003', (SELECT id FROM jurisdictions WHERE code = 'NL'), (SELECT id FROM sources WHERE code = 'NL-BWB'),
   'wet', NULL, 'BWBR0011353',
   '{"nl": "Wet inkomstenbelasting 2001", "en": "Income Tax Act 2001"}', '2000-05-11',
   '{"juriconnect": "jci1.3:c:BWBR0011353"}'),
  ('b0000000-0000-4000-8000-000000000004', (SELECT id FROM jurisdictions WHERE code = 'LT'), (SELECT id FROM sources WHERE code = 'LT-TAR'),
   'istatymas', 'https://www.e-tar.lt/portal/lt/legalAct/TAR.C677663D2202', 'IX-1007',
   '{"lt": "Gyventojų pajamų mokesčio įstatymas", "en": "Law on Personal Income Tax"}', '2002-07-02',
   '{}'),
  ('b0000000-0000-4000-8000-000000000005', (SELECT id FROM jurisdictions WHERE code = 'ES'), (SELECT id FROM sources WHERE code = 'ES-BOE'),
   'ley', 'https://www.boe.es/eli/es/l/2006/11/28/35/con', 'BOE-A-2006-20764',
   '{"es": "Ley 35/2006 del Impuesto sobre la Renta de las Personas Físicas", "en": "Personal Income Tax Act 35/2006"}', '2006-11-29',
   '{}'),
  ('b0000000-0000-4000-8000-000000000006', (SELECT id FROM jurisdictions WHERE code = 'IE'), (SELECT id FROM sources WHERE code = 'IE-EISB'),
   'act', 'https://www.irishstatutebook.ie/eli/1997/act/39', '1997/39',
   '{"en": "Taxes Consolidation Act 1997"}', '1997-11-30',
   '{}'),
  -- amending act used by instrument_relations
  ('b0000000-0000-4000-8000-000000000007', (SELECT id FROM jurisdictions WHERE code = 'FR'), (SELECT id FROM sources WHERE code = 'FR-LEGI'),
   'loi', NULL, 'JORFTEXT000051168139',
   '{"fr": "Loi n° 2025-127 du 14 février 2025 de finances pour 2025"}', '2025-02-15',
   '{}');

-- ----------------------------------------------------------------------------
-- Legal units (structural identity)
-- ----------------------------------------------------------------------------
INSERT INTO legal_units (id, instrument_id, parent_id, unit_type, ordinal, path, citation, national_id, is_container) VALUES
  -- FR: one container level + the article, to demo ltree subtree queries
  ('c0000000-0000-4000-8000-000000000001', 'b0000000-0000-4000-8000-000000000001', NULL,
   'livre', 1, 'liv_1', 'CGI, Livre premier', NULL, true),
  ('c0000000-0000-4000-8000-000000000002', 'b0000000-0000-4000-8000-000000000001', 'c0000000-0000-4000-8000-000000000001',
   'article', 197, 'liv_1.art_197', 'CGI, art. 197', 'LEGIARTI000006308305', false),
  ('c0000000-0000-4000-8000-000000000003', 'b0000000-0000-4000-8000-000000000002', NULL,
   'article', 130, 'art_130', 'CIR 92, art. 130', '1992003455-A130', false),
  ('c0000000-0000-4000-8000-000000000004', 'b0000000-0000-4000-8000-000000000003', NULL,
   'artikel', 210, 'art_2_10', 'Wet IB 2001, artikel 2.10', 'BWBR0011353-2.10', false),
  ('c0000000-0000-4000-8000-000000000005', 'b0000000-0000-4000-8000-000000000004', NULL,
   'straipsnis', 6, 'str_6', 'GPMĮ 6 straipsnis', 'IX-1007-6', false),
  ('c0000000-0000-4000-8000-000000000006', 'b0000000-0000-4000-8000-000000000005', NULL,
   'articulo', 63, 'art_63', 'Ley 35/2006, artículo 63', 'BOE-A-2006-20764-63', false),
  ('c0000000-0000-4000-8000-000000000007', 'b0000000-0000-4000-8000-000000000006', NULL,
   'section', 15, 'sec_15', 'TCA 1997, s. 15', '1997/39-s15', false);

-- ----------------------------------------------------------------------------
-- Versions (validity intervals; '[)' convention)
-- ----------------------------------------------------------------------------
INSERT INTO legal_unit_versions (id, legal_unit_id, validity, version_status, source_version_id, citation_label, fetch_snapshot_id, amendment_note) VALUES
  -- FR art. 197: 2024 barème then 2025 barème (matches parameter_sample.jsonc)
  ('d0000000-0000-4000-8000-000000000001', 'c0000000-0000-4000-8000-000000000002',
   daterange('2024-01-01', '2025-01-01', '[)'), 'repealed', 'LEGIARTI000047850595', 'CGI, art. 197',
   'a0000000-0000-4000-8000-000000000001',
   '{"amended_by": "Loi n° 2023-1322 de finances pour 2024"}'),
  ('d0000000-0000-4000-8000-000000000002', 'c0000000-0000-4000-8000-000000000002',
   daterange('2025-01-01', NULL, '[)'), 'in_force', 'LEGIARTI000051200000', 'CGI, art. 197',
   'a0000000-0000-4000-8000-000000000002',
   '{"amended_by": "Loi n° 2025-127 de finances pour 2025", "jorf": "2025-02-15"}'),
  ('d0000000-0000-4000-8000-000000000003', 'c0000000-0000-4000-8000-000000000003',
   daterange('2023-01-01', NULL, '[)'), 'in_force', NULL, 'CIR 92, art. 130',
   'a0000000-0000-4000-8000-000000000007', '{}'),
  ('d0000000-0000-4000-8000-000000000004', 'c0000000-0000-4000-8000-000000000004',
   daterange('2025-01-01', NULL, '[)'), 'in_force', 'jci1.3:c:BWBR0011353&artikel=2.10&z=2025-01-01', 'Wet IB 2001, artikel 2.10',
   'a0000000-0000-4000-8000-000000000003', '{}'),
  ('d0000000-0000-4000-8000-000000000005', 'c0000000-0000-4000-8000-000000000005',
   daterange('2024-01-01', NULL, '[)'), 'in_force', NULL, 'GPMĮ 6 straipsnis',
   'a0000000-0000-4000-8000-000000000004', '{}'),
  ('d0000000-0000-4000-8000-000000000006', 'c0000000-0000-4000-8000-000000000006',
   daterange('2023-01-01', NULL, '[)'), 'in_force', NULL, 'Ley 35/2006, artículo 63',
   'a0000000-0000-4000-8000-000000000005', '{}'),
  ('d0000000-0000-4000-8000-000000000007', 'c0000000-0000-4000-8000-000000000007',
   daterange('2020-01-01', NULL, '[)'), 'in_force', NULL, 'TCA 1997, s. 15',
   'a0000000-0000-4000-8000-000000000006', '{}');

-- ----------------------------------------------------------------------------
-- Texts (search_config + content_hash computed from lang_fts_config/content)
-- ----------------------------------------------------------------------------
INSERT INTO unit_texts (id, version_id, lang, authenticity, content, translation_of, mt_engine, search_config, content_hash)
SELECT v.id, v.version_id, v.lang, v.authenticity, v.content,
       v.translation_of::uuid, v.mt_engine,
       (SELECT config FROM lang_fts_config WHERE lang = v.lang),
       encode(sha256(convert_to(v.content, 'UTF8')), 'hex')
FROM (VALUES
  -- FR art. 197, 2024 barème — authentic + EN machine translation
  ('e0000000-0000-4000-8000-000000000001'::uuid, 'd0000000-0000-4000-8000-000000000001'::uuid, 'fr', 'authentic',
   'I. – En ce qui concerne les contribuables visés à l''article 4 B, il est fait application des règles suivantes pour le calcul de l''impôt sur le revenu : 1. L''impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède 11 294 € le taux de : 11 % pour la fraction supérieure à 11 294 € et inférieure ou égale à 28 797 € ; 30 % pour la fraction supérieure à 28 797 € et inférieure ou égale à 82 341 € ; 41 % pour la fraction supérieure à 82 341 € et inférieure ou égale à 177 106 € ; 45 % pour la fraction supérieure à 177 106 €.',
   NULL, NULL),
  ('e0000000-0000-4000-8000-000000000002'::uuid, 'd0000000-0000-4000-8000-000000000001'::uuid, 'en', 'machine_translation',
   'I. – For taxpayers referred to in Article 4 B, income tax is computed by applying to the fraction of each income share exceeding EUR 11,294 the rate of: 11% for the fraction above EUR 11,294 and up to EUR 28,797; 30% for the fraction above EUR 28,797 and up to EUR 82,341; 41% for the fraction above EUR 82,341 and up to EUR 177,106; 45% for the fraction above EUR 177,106.',
   'e0000000-0000-4000-8000-000000000001', 'demo-mt'),
  -- FR art. 197, 2025 barème — authentic + EN machine translation
  ('e0000000-0000-4000-8000-000000000003'::uuid, 'd0000000-0000-4000-8000-000000000002'::uuid, 'fr', 'authentic',
   'I. – En ce qui concerne les contribuables visés à l''article 4 B, il est fait application des règles suivantes pour le calcul de l''impôt sur le revenu : 1. L''impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède 11 497 € le taux de : 11 % pour la fraction supérieure à 11 497 € et inférieure ou égale à 29 315 € ; 30 % pour la fraction supérieure à 29 315 € et inférieure ou égale à 83 823 € ; 41 % pour la fraction supérieure à 83 823 € et inférieure ou égale à 180 294 € ; 45 % pour la fraction supérieure à 180 294 €.',
   NULL, NULL),
  ('e0000000-0000-4000-8000-000000000004'::uuid, 'd0000000-0000-4000-8000-000000000002'::uuid, 'en', 'machine_translation',
   'I. – For taxpayers referred to in Article 4 B, income tax is computed by applying to the fraction of each income share exceeding EUR 11,497 the rate of: 11% for the fraction above EUR 11,497 and up to EUR 29,315; 30% for the fraction above EUR 29,315 and up to EUR 83,823; 41% for the fraction above EUR 83,823 and up to EUR 180,294; 45% for the fraction above EUR 180,294.',
   'e0000000-0000-4000-8000-000000000003', 'demo-mt'),
  -- BE art. 130 — TWO authentic languages (the Belgian case)
  ('e0000000-0000-4000-8000-000000000005'::uuid, 'd0000000-0000-4000-8000-000000000003'::uuid, 'fr', 'authentic',
   'L''impôt de base est calculé selon le barème suivant : 25 p.c. pour la tranche de revenu de 0,01 EUR à 15 820 EUR ; 40 p.c. pour la tranche de 15 820 EUR à 27 920 EUR ; 45 p.c. pour la tranche de 27 920 EUR à 48 320 EUR ; 50 p.c. pour la tranche supérieure à 48 320 EUR.',
   NULL, NULL),
  ('e0000000-0000-4000-8000-000000000006'::uuid, 'd0000000-0000-4000-8000-000000000003'::uuid, 'nl', 'authentic',
   'De basisbelasting wordt berekend volgens het volgende tarief : 25 pct. voor de inkomensschijf van 0,01 EUR tot 15 820 EUR ; 40 pct. voor de schijf van 15 820 EUR tot 27 920 EUR ; 45 pct. voor de schijf van 27 920 EUR tot 48 320 EUR ; 50 pct. voor de schijf boven 48 320 EUR.',
   NULL, NULL),
  -- NL artikel 2.10
  ('e0000000-0000-4000-8000-000000000007'::uuid, 'd0000000-0000-4000-8000-000000000004'::uuid, 'nl', 'authentic',
   'De belasting op het belastbare inkomen uit werk en woning wordt bepaald aan de hand van de volgende tabel : bij een belastbaar inkomen uit werk en woning van niet meer dan 38 441 euro bedraagt de belasting 35,82%; boven 38 441 euro en niet meer dan 76 817 euro : 37,48%; boven 76 817 euro : 49,50%.',
   NULL, NULL),
  -- LT 6 straipsnis
  ('e0000000-0000-4000-8000-000000000008'::uuid, 'd0000000-0000-4000-8000-000000000005'::uuid, 'lt', 'authentic',
   'Pajamų mokesčio tarifas – 20 procentų, taikomas metinei pajamų daliai, neviršijančiai 60 vidutinių šalies darbo užmokesčių dydžio sumos, ir 32 procentai – šią sumą viršijančiai metinei pajamų daliai.',
   NULL, NULL),
  -- ES artículo 63
  ('e0000000-0000-4000-8000-000000000009'::uuid, 'd0000000-0000-4000-8000-000000000006'::uuid, 'es', 'authentic',
   'La parte de la base liquidable general será gravada con arreglo a la siguiente escala : hasta 12 450,00 euros, tipo aplicable del 9,50 por ciento ; de 12 450,00 a 20 200,00 euros, 12,00 por ciento ; de 20 200,00 a 35 200,00 euros, 15,00 por ciento ; de 35 200,00 a 60 000,00 euros, 18,50 por ciento ; de 60 000,00 a 300 000,00 euros, 22,50 por ciento ; en adelante, 24,50 por ciento.',
   NULL, NULL),
  -- IE section 15
  ('e0000000-0000-4000-8000-000000000010'::uuid, 'd0000000-0000-4000-8000-000000000007'::uuid, 'en', 'authentic',
   'Income tax shall be charged for each year of assessment at the rate of tax specified in this section : the standard rate of 20 per cent on income up to the standard rate cut-off point, and the higher rate of 40 per cent on the remainder of taxable income.',
   NULL, NULL)
) AS v(id, version_id, lang, authenticity, content, translation_of, mt_engine);

-- ----------------------------------------------------------------------------
-- Chunks: whole-unit chunks (seq 0) generated from every text row.
-- context_header = instrument title (text language, else first title) > citation (vig. <start>)
-- ----------------------------------------------------------------------------
INSERT INTO chunks (unit_text_id, seq, char_start, char_end, content, context_header, search_config, token_count)
SELECT t.id, 0, 0, length(t.content), t.content,
       coalesce(i.title ->> t.lang, jsonb_text_values(i.title))
         || ' > ' || u.citation
         || ' (vig. ' || coalesce(lower(v.validity)::text, '…') || ')',
       t.search_config,
       ceil(length(t.content) / 4.0)::int
FROM unit_texts t
JOIN legal_unit_versions v ON v.id = t.version_id
JOIN legal_units u ON u.id = v.legal_unit_id
JOIN instruments i ON i.id = u.instrument_id;

-- ----------------------------------------------------------------------------
-- Placeholder embeddings for every chunk (model 99). Real pipeline: model 1.
-- ----------------------------------------------------------------------------
INSERT INTO embeddings (chunk_id, model_id, embedding, input_hash)
SELECT c.id, 99,
       placeholder_embedding(c.context_header || E'\n' || c.content),
       encode(sha256(convert_to(c.context_header || c.content, 'UTF8')), 'hex')
FROM chunks c;

-- ----------------------------------------------------------------------------
-- Amendment lineage (metadata only): LF 2025 amends CGI art. 197
-- ----------------------------------------------------------------------------
INSERT INTO instrument_relations (from_instrument_id, to_instrument_id, to_unit_id, relation_type, effective_date, metadata) VALUES
  ('b0000000-0000-4000-8000-000000000007', 'b0000000-0000-4000-8000-000000000001',
   'c0000000-0000-4000-8000-000000000002', 'amends', '2025-01-01',
   '{"jorf": "2025-02-15", "note": "barème IR indexé"}');

-- ----------------------------------------------------------------------------
-- Citation registry: the EXTERNAL parameter JSON (income-tax schedule) cites
-- both dated versions of CGI art. 197. Reference only — no parameter content.
-- ----------------------------------------------------------------------------
INSERT INTO citation_registry (cited_version_id, cited_chunk_id, external_ref, external_kind) VALUES
  ('d0000000-0000-4000-8000-000000000001',
   (SELECT id FROM chunks WHERE unit_text_id = 'e0000000-0000-4000-8000-000000000001' AND seq = 0),
   'euromod://FR/tin_fr/def_const/$tinsc_bareme', 'euromod_parameter'),
  ('d0000000-0000-4000-8000-000000000002',
   (SELECT id FROM chunks WHERE unit_text_id = 'e0000000-0000-4000-8000-000000000003' AND seq = 0),
   'euromod://FR/tin_fr/def_const/$tinsc_bareme', 'euromod_parameter');

ANALYZE;
