-- ============================================================================
-- EU Tax Legislation Database — PostgreSQL schema
-- ============================================================================
-- Legislation-only store backing the EUROMOD lazy, agent-populated RAG.
-- Policy parameters live OUTSIDE this database (JSON files in git); they cite
-- legal text through stable UUIDs (jrc_database_id) and rag:// URIs resolved
-- by resolve_rag_uri() below. See RAG/11_database-model.md for the design doc.
--
-- Target: PostgreSQL 16+ with pgvector >= 0.7 (halfvec).
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;      -- embeddings (halfvec + HNSW)
CREATE EXTENSION IF NOT EXISTS pg_trgm;     -- fuzzy citation / identifier matching
CREATE EXTENSION IF NOT EXISTS btree_gist;  -- uuid equality inside GiST exclusion
CREATE EXTENSION IF NOT EXISTS unaccent;    -- diacritics-insensitive FTS
CREATE EXTENSION IF NOT EXISTS ltree;       -- legal hierarchy paths

-- ----------------------------------------------------------------------------
-- Text search configurations: built-in stemmers + unaccent.
-- Languages without a PostgreSQL stemmer (lt, ga) start from 'simple';
-- upgrading them to a hunspell dictionary later is an ALTER here plus an
-- UPDATE of lang_fts_config — zero schema change.
-- ----------------------------------------------------------------------------
CREATE TEXT SEARCH CONFIGURATION fts_fr (COPY = french);
ALTER  TEXT SEARCH CONFIGURATION fts_fr
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, french_stem;

CREATE TEXT SEARCH CONFIGURATION fts_nl (COPY = dutch);
ALTER  TEXT SEARCH CONFIGURATION fts_nl
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, dutch_stem;

CREATE TEXT SEARCH CONFIGURATION fts_es (COPY = spanish);
ALTER  TEXT SEARCH CONFIGURATION fts_es
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, spanish_stem;

CREATE TEXT SEARCH CONFIGURATION fts_de (COPY = german);
ALTER  TEXT SEARCH CONFIGURATION fts_de
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, german_stem;

CREATE TEXT SEARCH CONFIGURATION fts_en (COPY = english);
ALTER  TEXT SEARCH CONFIGURATION fts_en
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, english_stem;

CREATE TEXT SEARCH CONFIGURATION fts_lt (COPY = simple);   -- no built-in Lithuanian stemmer
ALTER  TEXT SEARCH CONFIGURATION fts_lt
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, simple;

CREATE TEXT SEARCH CONFIGURATION fts_ga (COPY = simple);   -- no built-in Irish stemmer
ALTER  TEXT SEARCH CONFIGURATION fts_ga
  ALTER MAPPING FOR hword, hword_part, word WITH unaccent, simple;

-- Language -> regconfig mapping, read by fetch skills at insert time.
CREATE TABLE lang_fts_config (
    lang    text PRIMARY KEY,               -- BCP-47 primary tag: 'fr','nl','lt',...
    config  regconfig NOT NULL,
    notes   text
);

INSERT INTO lang_fts_config (lang, config, notes) VALUES
  ('fr', 'fts_fr', 'french stemmer + unaccent'),
  ('nl', 'fts_nl', 'dutch stemmer + unaccent'),
  ('es', 'fts_es', 'spanish stemmer + unaccent'),
  ('de', 'fts_de', 'german stemmer + unaccent'),
  ('en', 'fts_en', 'english stemmer + unaccent'),
  ('lt', 'fts_lt', 'simple fallback; upgrade path = hunspell lt_LT dictionary'),
  ('ga', 'fts_ga', 'simple fallback; upgrade path = hunspell ga_IE dictionary');

-- Concatenate the values of a language-keyed JSONB title for trgm indexing.
CREATE FUNCTION jsonb_text_values(j jsonb) RETURNS text
LANGUAGE sql IMMUTABLE PARALLEL SAFE AS
$$ SELECT string_agg(value, ' ' ORDER BY key) FROM jsonb_each_text(j) $$;

-- ----------------------------------------------------------------------------
-- jurisdictions — member states now, regional layers (ES-CT, ...) later
-- ----------------------------------------------------------------------------
CREATE TABLE jurisdictions (
    id             smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code           text NOT NULL UNIQUE,        -- ISO 3166-1 alpha-2 or 3166-2
    parent_id      smallint REFERENCES jurisdictions(id),
    name           text NOT NULL,
    official_langs text[] NOT NULL,             -- BE: {fr,nl,de}; IE: {en,ga}
    metadata       jsonb NOT NULL DEFAULT '{}'
);

-- ----------------------------------------------------------------------------
-- sources — one row per official portal/base a fetch skill talks to
-- ----------------------------------------------------------------------------
CREATE TABLE sources (
    id                     smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    jurisdiction_id        smallint NOT NULL REFERENCES jurisdictions(id),
    code                   text NOT NULL UNIQUE,     -- 'FR-LEGI', 'BE-JUSTEL', ...
    name                   text NOT NULL,
    base_url               text,
    id_system              text NOT NULL,            -- 'legi','bwb_juriconnect','tar','boe','eisb','justel_numac',...
    supports_eli           boolean NOT NULL DEFAULT false,
    supports_point_in_time boolean NOT NULL DEFAULT false,
    fetch_skill            text,                     -- e.g. 'skills/fr-legifrance'
    terms                  jsonb NOT NULL DEFAULT '{}'  -- rate limits, ToS, bulk dumps
);

-- ----------------------------------------------------------------------------
-- fetch_runs / fetch_snapshots — provenance of the lazy cache (append-only)
-- ----------------------------------------------------------------------------
CREATE TABLE fetch_runs (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id     smallint NOT NULL REFERENCES sources(id),
    skill_version text NOT NULL,
    trigger       text NOT NULL DEFAULT 'cache_miss'
                  CHECK (trigger IN ('cache_miss','refresh','bulk_seed','eval_freeze','manual')),
    started_at    timestamptz NOT NULL DEFAULT now(),
    finished_at   timestamptz,
    status        text NOT NULL DEFAULT 'running'
                  CHECK (status IN ('running','succeeded','failed','partial')),
    frozen_label  text,                       -- e.g. 'eval-2026-09': reproducibility marker
    stats         jsonb NOT NULL DEFAULT '{}'
);

CREATE TABLE fetch_snapshots (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id        uuid NOT NULL REFERENCES fetch_runs(id),
    source_id     smallint NOT NULL REFERENCES sources(id),
    url           text NOT NULL,
    http_status   integer,
    retrieved_at  timestamptz NOT NULL DEFAULT now(),
    content_type  text,
    content_hash  text NOT NULL,              -- sha256 of the raw payload
    raw_content   bytea,                      -- inline for HTML/JSON/XML ...
    storage_ref   text,                       -- ... or object-store path for large PDFs
    parser_version text,
    metadata      jsonb NOT NULL DEFAULT '{}',
    CHECK ((raw_content IS NULL) <> (storage_ref IS NULL))  -- exactly one
);
CREATE INDEX fetch_snapshots_url  ON fetch_snapshots (source_id, url, retrieved_at DESC);
CREATE INDEX fetch_snapshots_hash ON fetch_snapshots (content_hash);

-- ----------------------------------------------------------------------------
-- instruments — a law / code / act / SI as a citable whole
-- ----------------------------------------------------------------------------
CREATE TABLE instruments (
    id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_id  smallint NOT NULL REFERENCES jurisdictions(id),
    source_id        smallint NOT NULL REFERENCES sources(id),
    instrument_type  text NOT NULL,           -- 'code','loi','wet','act','statutory_instrument',
                                              -- 'ley','istatymas','royal_decree',... per-country vocab
    eli              text,                    -- ELI URI when the source mints one
    national_id      text,                    -- LEGITEXT..., BWBR..., TAR reg no, BOE-A-..., numac, act no/year
    title            jsonb NOT NULL,          -- language-keyed: BE carries two authentic titles
    title_search     text GENERATED ALWAYS AS (jsonb_text_values(title)) STORED,
    adoption_date    date,
    publication_date date,
    in_force         daterange,               -- coarse instrument lifetime; unit versions are the truth
    metadata         jsonb NOT NULL DEFAULT '{}',
    created_at       timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, national_id)
);
CREATE UNIQUE INDEX instruments_eli ON instruments (eli) WHERE eli IS NOT NULL;
CREATE INDEX instruments_title_trgm ON instruments USING gin (title_search gin_trgm_ops);
CREATE INDEX instruments_natid_trgm ON instruments USING gin (national_id gin_trgm_ops);
CREATE INDEX instruments_jur_type   ON instruments (jurisdiction_id, instrument_type);

-- ----------------------------------------------------------------------------
-- legal_units — structural identity (timeless slot: "Article 197 CGI")
-- ----------------------------------------------------------------------------
CREATE TABLE legal_units (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    instrument_id uuid NOT NULL REFERENCES instruments(id),
    parent_id     uuid REFERENCES legal_units(id),
    unit_type     text NOT NULL,       -- 'livre','titre','chapitre','article','alinea',
                                       -- 'hoofdstuk','artikel','lid','part','section',
                                       -- 'straipsnis','articulo','annex',... per-country vocab
    ordinal       integer NOT NULL DEFAULT 0,          -- sibling sort order
    path          ltree NOT NULL,      -- sanitized labels: 'liv_1.tit_1.chap_1.art_197'
    citation      text NOT NULL,       -- canonical human citation: 'CGI, art. 197'
    eli           text,                -- unit-level ELI where minted
    national_id   text,                -- FR LEGIARTI parent id, NL Juriconnect base, 'TCA1997-s15'
    is_container  boolean NOT NULL DEFAULT false,      -- true for book/title/chapter levels
    metadata      jsonb NOT NULL DEFAULT '{}',
    created_at    timestamptz NOT NULL DEFAULT now(),
    UNIQUE (instrument_id, path)
);
CREATE INDEX legal_units_path_gist     ON legal_units USING gist (path);
CREATE INDEX legal_units_citation_trgm ON legal_units USING gin (citation gin_trgm_ops);
CREATE INDEX legal_units_national_id   ON legal_units (national_id) WHERE national_id IS NOT NULL;
CREATE UNIQUE INDEX legal_units_eli    ON legal_units (eli) WHERE eli IS NOT NULL;

-- ----------------------------------------------------------------------------
-- legal_unit_versions — one consolidated state with a validity interval.
-- THE temporal truth: point-in-time = WHERE validity @> :as_of.
-- A renumbered article is a NEW legal_units row, never a mutated one.
-- ----------------------------------------------------------------------------
CREATE TABLE legal_unit_versions (
    id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    legal_unit_id     uuid NOT NULL REFERENCES legal_units(id),
    validity          daterange NOT NULL,      -- '[)' convention; unbounded upper = in force
    version_status    text NOT NULL DEFAULT 'in_force'
                      CHECK (version_status IN
                        ('in_force','repealed','not_yet_in_force','suspended','unknown')),
    source_version_id text,                    -- FR LEGIARTI000038836775, NL Juriconnect versioned ref, ...
    eli_version       text,                    -- versioned ELI if minted
    citation_label    text,                    -- display label at that time (renumbering-safe)
    fetch_snapshot_id uuid NOT NULL REFERENCES fetch_snapshots(id),  -- no text without origin
    amendment_note    jsonb NOT NULL DEFAULT '{}',   -- amending act refs — metadata, not a diff chain
    metadata          jsonb NOT NULL DEFAULT '{}',
    created_at        timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT validity_not_empty CHECK (NOT isempty(validity)),
    -- Load-bearing integrity rule: one unit cannot have two overlapping
    -- consolidated states. A skill closing/replacing a version must shrink the
    -- old row's validity in the same transaction.
    CONSTRAINT legal_unit_versions_no_overlap
        EXCLUDE USING gist (legal_unit_id WITH =, validity WITH &&)
);
CREATE INDEX luv_validity_gist  ON legal_unit_versions USING gist (validity);
CREATE INDEX luv_unit           ON legal_unit_versions (legal_unit_id);
CREATE INDEX luv_source_version ON legal_unit_versions (source_version_id)
    WHERE source_version_id IS NOT NULL;

-- ----------------------------------------------------------------------------
-- unit_texts — one language rendering of one version.
-- Belgium: several rows with authenticity='authentic' (fr + nl [+ de]).
-- Machine translations are ordinary rows flagged as derived.
-- ----------------------------------------------------------------------------
CREATE TABLE unit_texts (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    version_id     uuid NOT NULL REFERENCES legal_unit_versions(id) ON DELETE CASCADE,
    lang           text NOT NULL REFERENCES lang_fts_config(lang),
    authenticity   text NOT NULL CHECK (authenticity IN
                     ('authentic','official_translation','machine_translation')),
    content        text NOT NULL,            -- plain text; canonical for character offsets
    content_html   text,                     -- optional original markup for display
    search_config  regconfig NOT NULL,       -- copied from lang_fts_config at insert
    tsv            tsvector GENERATED ALWAYS AS (to_tsvector(search_config, content)) STORED,
    translation_of uuid REFERENCES unit_texts(id),   -- MT/translation rows point at their source text row (if it's in this DB)
    source_lang    text REFERENCES lang_fts_config(lang),  -- language this row was translated FROM; NULL iff authenticity='authentic'
    mt_engine      text,                     -- NULL unless machine_translation
    content_hash   text NOT NULL,            -- sha256; idempotent re-fetch detection
    metadata       jsonb NOT NULL DEFAULT '{}',
    UNIQUE (version_id, lang, authenticity),
    CHECK ((authenticity = 'machine_translation') = (mt_engine IS NOT NULL)),
    -- 'authentic' rows ARE the original-language source, so they carry no source_lang;
    -- any translation (official or machine) must record what language it was rendered from.
    CHECK ((authenticity = 'authentic') = (source_lang IS NULL)),
    CHECK (source_lang IS NULL OR source_lang <> lang)
);
CREATE INDEX unit_texts_tsv     ON unit_texts USING gin (tsv);
CREATE INDEX unit_texts_version ON unit_texts (version_id);
CREATE INDEX unit_texts_lang    ON unit_texts (version_id, lang);

-- Keep source_lang consistent with translation_of whenever the source row is
-- present in this DB (translation_of is optional: some official translations
-- are fetched from a source with no in-DB original, e.g. an EU-level EN text).
CREATE FUNCTION unit_texts_check_source_lang() RETURNS trigger
LANGUAGE plpgsql AS
$$
DECLARE
    v_src_lang text;
BEGIN
    IF NEW.translation_of IS NOT NULL THEN
        SELECT lang INTO v_src_lang FROM unit_texts WHERE id = NEW.translation_of;
        IF v_src_lang IS NULL THEN
            RAISE EXCEPTION 'translation_of % not found', NEW.translation_of;
        END IF;
        IF NEW.source_lang IS DISTINCT FROM v_src_lang THEN
            RAISE EXCEPTION 'source_lang (%) does not match translation_of row''s lang (%)',
                NEW.source_lang, v_src_lang;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER unit_texts_source_lang_biu
    BEFORE INSERT OR UPDATE ON unit_texts
    FOR EACH ROW EXECUTE FUNCTION unit_texts_check_source_lang();

-- ----------------------------------------------------------------------------
-- chunks — the retrieval grain and THE citable target (jrc_database_id).
-- seq 0 = whole unit; large units split into seq 1..n with char offsets into
-- unit_texts.content, so parameter supporting_extract offsets verify mechanically.
-- ----------------------------------------------------------------------------
CREATE TABLE chunks (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_text_id   uuid NOT NULL REFERENCES unit_texts(id) ON DELETE CASCADE,
    seq            integer NOT NULL DEFAULT 0,
    char_start     integer NOT NULL,
    char_end       integer NOT NULL,
    content        text NOT NULL,            -- denormalized slice: retrieval without a join
    context_header text NOT NULL,            -- 'Code général des impôts > Art. 197 (vig. 2024-01-01)'
    search_config  regconfig NOT NULL,       -- copied from unit_texts
    tsv            tsvector GENERATED ALWAYS AS
                     (setweight(to_tsvector(search_config, context_header), 'A') ||
                      setweight(to_tsvector(search_config, content), 'B')) STORED,
    token_count    integer,
    UNIQUE (unit_text_id, seq),
    CHECK (char_end > char_start)
);
CREATE INDEX chunks_tsv ON chunks USING gin (tsv);     -- primary lexical index

-- ----------------------------------------------------------------------------
-- embedding_models / embeddings — N models side by side (contractual comparison)
-- ----------------------------------------------------------------------------
CREATE TABLE embedding_models (
    id         smallint PRIMARY KEY,
    name       text NOT NULL UNIQUE,      -- 'bge-m3', 'multilingual-e5-large', 'text-embedding-3-large@1024'
    provider   text NOT NULL,             -- 'self-hosted','openai',...
    native_dim integer NOT NULL,
    stored_dim integer NOT NULL DEFAULT 1024,   -- after Matryoshka truncation if any
    normalize  boolean NOT NULL DEFAULT true,
    is_default boolean NOT NULL DEFAULT false,
    config     jsonb NOT NULL DEFAULT '{}'      -- prompt prefixes ('query:'/'passage:'), pooling, ...
);

CREATE TABLE embeddings (
    chunk_id    uuid NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
    model_id    smallint NOT NULL REFERENCES embedding_models(id),
    embedding   halfvec(1024) NOT NULL,   -- fp16: half the storage, negligible recall loss
    input_hash  text NOT NULL,            -- sha256(context_header || content): staleness check
    embedded_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (chunk_id, model_id)
);
-- One partial HNSW index per active model; create it alongside the model row.
-- Query-time recall knob: SET hnsw.ef_search = 100;
-- (Index for the default model is created in seed.sql next to its registry row.)

-- ----------------------------------------------------------------------------
-- instrument_relations — amendment lineage as metadata. Never drives
-- point-in-time answers (validity intervals do); used for provenance display
-- and for skills to discover what to fetch next.
-- ----------------------------------------------------------------------------
CREATE TABLE instrument_relations (
    id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    from_instrument_id uuid NOT NULL REFERENCES instruments(id),
    to_instrument_id   uuid REFERENCES instruments(id),
    to_unit_id         uuid REFERENCES legal_units(id),
    to_ref_text        text,             -- unresolved target not yet in the lazy cache
    relation_type      text NOT NULL CHECK (relation_type IN
                         ('amends','repeals','inserts','renumbers','corrects',
                          'codifies','implements','cites')),
    effective_date     date,
    metadata           jsonb NOT NULL DEFAULT '{}',
    CHECK (to_instrument_id IS NOT NULL OR to_unit_id IS NOT NULL OR to_ref_text IS NOT NULL)
);
CREATE INDEX instrument_relations_from ON instrument_relations (from_instrument_id);
CREATE INDEX instrument_relations_to   ON instrument_relations (to_instrument_id)
    WHERE to_instrument_id IS NOT NULL;

-- ----------------------------------------------------------------------------
-- citation_registry — reference-only linkage to the EXTERNAL parameter JSON.
-- No parameter content lives here. The plain FKs (NO ACTION) double as the
-- retention rule: a cited version/chunk cannot be hard-deleted.
-- ----------------------------------------------------------------------------
CREATE TABLE citation_registry (
    id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    cited_version_id  uuid NOT NULL REFERENCES legal_unit_versions(id),
    cited_chunk_id    uuid REFERENCES chunks(id),
    external_ref      text NOT NULL,     -- e.g. 'euromod://FR/tin_fr/def_const/$tinsc_bareme'
    external_kind     text NOT NULL DEFAULT 'euromod_parameter',
    registered_at     timestamptz NOT NULL DEFAULT now(),
    metadata          jsonb NOT NULL DEFAULT '{}',
    UNIQUE (cited_version_id, cited_chunk_id, external_ref)
);
CREATE INDEX citation_registry_version ON citation_registry (cited_version_id);
CREATE INDEX citation_registry_ref     ON citation_registry (external_ref);

-- ----------------------------------------------------------------------------
-- rag:// URI resolver — the contract with the external parameter JSON.
--   rag://chunk/{uuid}                exact chunk
--   rag://version/{uuid}              specific consolidated version
--   rag://unit/{uuid}                 unit, version in force today
--   rag://unit/{uuid}@YYYY-MM-DD      unit, version in force at that date
-- Returns the resolved ids plus citation and text (preferring authentic texts).
-- ----------------------------------------------------------------------------
CREATE FUNCTION resolve_rag_uri(uri text)
RETURNS TABLE (kind text, unit_id uuid, version_id uuid, chunk_id uuid,
               citation text, validity daterange, lang text, content text)
LANGUAGE plpgsql STABLE AS
$$
DECLARE
    v_kind text := split_part(split_part(uri, 'rag://', 2), '/', 1);
    v_rest text := split_part(split_part(uri, 'rag://', 2), '/', 2);
    v_id   uuid;
    v_asof date := current_date;
BEGIN
    IF position('@' IN v_rest) > 0 THEN
        v_asof := split_part(v_rest, '@', 2)::date;
        v_rest := split_part(v_rest, '@', 1);
    END IF;
    v_id := v_rest::uuid;

    IF v_kind = 'chunk' THEN
        RETURN QUERY
        SELECT 'chunk'::text, u.id, v.id, c.id, u.citation, v.validity, t.lang, c.content
        FROM chunks c
        JOIN unit_texts t ON t.id = c.unit_text_id
        JOIN legal_unit_versions v ON v.id = t.version_id
        JOIN legal_units u ON u.id = v.legal_unit_id
        WHERE c.id = v_id;
    ELSIF v_kind = 'version' THEN
        RETURN QUERY
        SELECT 'version'::text, u.id, v.id, NULL::uuid, u.citation, v.validity, t.lang, t.content
        FROM legal_unit_versions v
        JOIN legal_units u ON u.id = v.legal_unit_id
        LEFT JOIN unit_texts t ON t.version_id = v.id AND t.authenticity = 'authentic'
        WHERE v.id = v_id;
    ELSIF v_kind = 'unit' THEN
        RETURN QUERY
        SELECT 'unit'::text, u.id, v.id, NULL::uuid, u.citation, v.validity, t.lang, t.content
        FROM legal_units u
        JOIN legal_unit_versions v ON v.legal_unit_id = u.id AND v.validity @> v_asof
        LEFT JOIN unit_texts t ON t.version_id = v.id AND t.authenticity = 'authentic'
        WHERE u.id = v_id;
    ELSE
        RAISE EXCEPTION 'unknown rag:// kind: %', v_kind;
    END IF;
END;
$$;

-- ----------------------------------------------------------------------------
-- Convenience view: units with their in-force version and authentic texts today
-- ----------------------------------------------------------------------------
CREATE VIEW current_legal_texts AS
SELECT j.code AS jurisdiction, i.title, u.citation, u.path,
       v.id AS version_id, v.validity, t.lang, t.authenticity, t.source_lang, t.content
FROM legal_units u
JOIN instruments i ON i.id = u.instrument_id
JOIN jurisdictions j ON j.id = i.jurisdiction_id
JOIN legal_unit_versions v ON v.legal_unit_id = u.id AND v.validity @> current_date
JOIN unit_texts t ON t.version_id = v.id
WHERE NOT u.is_container;
