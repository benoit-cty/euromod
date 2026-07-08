# EU Tax Legislation Database — Model, Full-Text Search & Vector Search

*Design document for the PostgreSQL legislation store backing the lazy, agent-populated RAG (see `10_retrieval-strategy-challenge.md`). Pilot countries: **FR, NL, LT, ES, IE, BE**; designed to extend to all 27 member states and to be reusable by other JRC services. Runnable prototype in [`db/`](db/) (schema, seed for all six countries, demo queries, docker-compose).*

---

## 1. Scope and boundary decisions

**In the database:** legislation only — instruments, their hierarchical units, dated consolidated versions, language texts, retrieval chunks, embeddings, and full fetch provenance.

**Not in the database:** policy parameters. They live as JSON files outside the DB (git-versioned, per the Activity 1 format). The linkage is **by reference, one-directional**: the parameter JSON cites legal text through stable identifiers this DB guarantees —

- `jrc_database_id` → a UUID of a `chunks` row (preferred), a `legal_unit_versions` row, or a `legal_units` row;
- `legal_unit_ref` → a `rag://` URI resolved by the SQL function `resolve_rag_uri()`:
  - `rag://chunk/{uuid}` — exact chunk,
  - `rag://version/{uuid}` — a specific consolidated version,
  - `rag://unit/{uuid}` — the unit's version in force today,
  - `rag://unit/{uuid}@YYYY-MM-DD` — the version in force at a date.

Two consequences the DB enforces:

1. **Identifiers are permanent.** UUIDs are never reissued; a renumbered article is a *new* unit, not a mutated one.
2. **Cited rows are never hard-deleted.** The optional `citation_registry` table records which external references (e.g. `euromod://FR/tin_fr/def_const/$tinsc_bareme`) cite which version/chunk; its plain foreign keys double as the retention lock, and it answers the impact question *"which parameters depend on this article?"* when a law changes. No parameter content is ever stored there.

## 2. Entity model

```
jurisdictions ──< sources ──< fetch_runs ──< fetch_snapshots     (append-only provenance)
      │                                            │
      └──< instruments ──< legal_units ──< legal_unit_versions ──< unit_texts ──< chunks ──< embeddings
                │            (ltree tree)    (daterange validity)   (per language)            (chunk × model)
                └──< instrument_relations   (amends/repeals — metadata only)

citation_registry   (external parameter refs → version/chunk UUIDs, reference only)
lang_fts_config     (language → text-search configuration)
embedding_models    (model registry for the contractual multi-model comparison)
```

The three-level split is the core idea:

| Level | Table | Answers | Identity rule |
|---|---|---|---|
| Structure | `legal_units` | "Article 197 CGI" as a timeless slot | Never mutated; renumbering = new row + `instrument_relations` lineage |
| Time | `legal_unit_versions` | "what did it say between 2024-01-01 and 2025-01-01?" | `daterange` validity; **GiST exclusion constraint** forbids overlapping consolidations of one unit |
| Language | `unit_texts` | "…in French / Dutch / machine-translated English?" | One row per version × language × authenticity |

Point-in-time queries are a filter, not archaeology: `WHERE validity @> :as_of::date`. The exclusion constraint is the load-bearing integrity rule — a fetch skill *physically cannot* insert two contradictory consolidations for the same date; superseding a version means shrinking the old row's range in the same transaction (version *text* is immutable, only the range closes).

### 2.1 How each pilot country's reality is absorbed

| Country | Peculiarity | Where it lands |
|---|---|---|
| FR | LEGI consolidations with native as-of dates, `LEGIARTI…` version ids, ELI | `source_version_id`, `eli`/`eli_version`, `supports_point_in_time` on the source |
| NL | No ELI; BWB/Juriconnect identifiers; artikel/lid structure | `national_id` (nothing assumes ELI exists), free `unit_type` vocabulary |
| LT | Lithuanian has no built-in PostgreSQL stemmer | `lang_fts_config` maps `lt` → `simple`-based config; hunspell upgrade path, zero schema change |
| ES | Regional dimension (comunidades autónomas) may matter later | `jurisdictions.parent_id` self-reference: `ES-CT` becomes a child of `ES` — rows, not DDL |
| IE | Common-law drafting (Acts/sections, SIs); English + Irish | Free `unit_type` vocabulary; `official_langs {en,ga}` |
| BE | Texts **authentic in several languages simultaneously** (fr + nl, some de) | `unit_texts.authenticity`: a version may carry *multiple* `authentic` rows — no "one original language" assumption anywhere |

Hierarchy depth varies wildly (code→livre→titre→chapitre→article→alinéa vs act→part→section). `legal_units` therefore uses a self-referencing `parent_id` plus an `ltree path` (`liv_1.art_197`) — any depth, zero fixed columns, indexed subtree queries ("everything under Chapter X").

### 2.2 Provenance — the lazy cache made trustworthy

Every `legal_unit_versions.fetch_snapshot_id` is `NOT NULL`: **no legal text exists in the corpus without a provable origin** (URL, HTTP status, retrieval timestamp, sha256, raw payload inline or an object-store ref for large PDFs). Snapshots are append-only and deduplicated by content hash. `fetch_runs.frozen_label` (e.g. `eval-2026-09`) marks the snapshot set an evaluation ran against — the reproducibility mechanism promised in the retrieval-strategy doc.

### 2.3 JSONB discipline

Same rule as the parameter schema (`Param_Schema/08`, §5.1): typed columns for anything filtered, joined, integrity-constrained, or part of the retrieval contract (`validity`, `lang`, `authenticity`, identifiers, provenance FK). `metadata jsonb DEFAULT '{}'` on every entity for country idiosyncrasies nobody queries relationally yet (Juriconnect sub-addressing, LEGI `etat` codes, Justel page refs). Promotion path: when a JSONB field shows up in a third country's skill, it graduates to a real column in a migration.

## 3. Full-text search

- **One GIN index serves all languages.** Each text/chunk row stores its own `search_config regconfig`; the `tsv` column is `GENERATED` from it (the two-argument `to_tsvector(regconfig, text)` is immutable, so this is legal). Queries pass the config for the *query* language: `tsv @@ websearch_to_tsquery('fts_fr', :q)`.
- **Custom configs with `unaccent`** (`fts_fr`, `fts_nl`, `fts_es`, `fts_de`, `fts_en`) so user-typed queries survive missing diacritics ("superieure" finds "supérieure").
- **Lithuanian & Irish**: no built-in stemmer → `fts_lt`/`fts_ga` start from `simple` + unaccent (exact-form matching; acceptable for statute language, which repeats terms verbatim). Upgrade = attach a hunspell dictionary (`lt_LT`, `ga_IE`) to the config and update the `lang_fts_config` row — zero schema change.
- **Weighted chunks**: `context_header` ("Code général des impôts > Art. 197 (vig. 2024-01-01)") at weight A, body at B — "article 197 impôt" hits the header hard, which is right for legal lookup. Ranking via length-normalized `ts_rank_cd(tsv, q, 32)`.
- **`pg_trgm`** GIN indexes on `legal_units.citation`, `instruments.national_id`, `instruments.title_search` power the **citation fast path**: tolerant matching of "CGI art 197", "art. 197 CGI", "TCA 1997 s.15", "LEGIARTI000038836775".
- Cross-lingual *lexical* search is deliberately not attempted: an EN query searches machine-translated EN chunks lexically; original-language semantics is the vector leg's job.

## 4. Embeddings & vector search

**Model registry, not a hardcoded model.** `embeddings` is keyed `(chunk_id, model_id)` with one **partial HNSW index per model** (`m=16, ef_construction=200`, `halfvec_cosine_ops`). The contract requires comparing models; N models sit side by side with identical query shapes, and dropping one is a `DELETE`. Stored dimension is fixed at **1024 `halfvec`** (fp16 — half the storage, negligible recall loss); API models with bigger native dims are Matryoshka-truncated to 1024 for fair comparison (`native_dim` vs `stored_dim` recorded).

**Default model: BGE-M3** (open weights, MIT, 1024-dim, 8k context, 100+ languages).

- *Data residency*: self-hostable on JRC hardware while the endpoint policy question (kick-off Q9/Q10) is unresolved — no legal text leaves JRC.
- *Language coverage* includes Lithuanian and reasonable Irish — exactly the languages where the lexical leg is weakest.
- *8k context* fits whole articles as single chunks, aligned with unit-based chunking.
- Comparison set for the Activity 5 report (rows in `embedding_models`, no DDL): `multilingual-e5-large`, `jina-embeddings-v3` (license check needed), `text-embedding-3-large@1024` if API access is permitted.

**What gets embedded:** `context_header + "\n" + content`, for **original-language chunks** (strategy (b) of `02_activity2`) *and* for the MT-EN chunks (strategy (a)) — both exist as ordinary rows, so the (a)-vs-(b) comparison the contract asks for is a `WHERE lang` filter at query time, not a second pipeline.

**Freshness:** embedding can be asynchronous, because the FTS `tsv` is a generated column — **the lexical leg is searchable the instant a fetched row lands; it never lags the cache.** `embeddings.input_hash` detects stale vectors after re-fetches.

## 5. Retrieval pipeline

Order (from `10_retrieval-strategy-challenge.md` §2C, embeddings now included):

1. **Citation fast path** (the majority case — parameter updates start from last year's citation): trgm-resolve instrument/unit, then `WHERE legal_unit_id = :u AND validity @> :as_of`. One indexed lookup, no ranking.
2. **Hybrid search**: one SQL statement — a CTE filters candidates by `as_of` + jurisdiction + language *first*, then FTS top-50 and vector top-50 run over that set and merge by **Reciprocal Rank Fusion (k=60)**. Full runnable version: `db/demo_queries.sql` §(f). (Joining the candidate set into the HNSW scan trades index purity for as-of correctness; with pgvector ≥ 0.8 iterative scans this is fine at pilot scale — flagged as a tuning point for corpus growth.)
3. **Miss → agentic fetch**: the country skill fetches, archives snapshot → version → texts → chunks, and the query re-runs. First-query latency is the accepted cost of the lazy design.

## 6. Extensibility — the 7th country

Adding a member state costs **rows, not DDL**: one `jurisdictions` row, 1–2 `sources` rows, possibly one `lang_fts_config` row (worst case a `CREATE TEXT SEARCH CONFIGURATION`), plus the fetch skill itself. Nothing in the schema assumes ELI exists (NL), one original language (BE), or any particular hierarchy shape (IE vs FR). Regional layers arrive as child jurisdictions. This is the same extension model as the country-skill architecture: the adapter cost lives in the skill, the schema is invariant.

## 7. Running the prototype

```bash
cd RAG/db
docker compose up -d        # PostgreSQL 17 + pgvector on host port 5433; schema + seed auto-applied
docker exec -i euromod-legislation-db psql -U jrc -d legislation < demo_queries.sql
docker compose down -v      # full reset
```

(Windows note: run from WSL2 where Docker is installed; the repo path is reachable under `/mnt/c/Users/Ben/Documents/Euromod/Benoit/RAG/db`.)

The demo queries prove, against seeded data for all six countries: (a) point-in-time on the two dated versions of CGI art. 197 (thresholds match `Param_Schema/parameter_sample.jsonc`); (b) trgm citation fast path; (c) stemmed+unaccented French FTS; (d) Belgium's dual authentic texts; (e) vector top-k; (f) hybrid RRF; (g) `rag://` resolution; (h) parameter impact analysis via `citation_registry`; (i) full provenance chain with frozen labels; (j) ltree subtree queries; (k) a commented insert that must fail on the no-overlap exclusion constraint.

Seeded vectors use a deterministic placeholder model (`model_id 99`) so vector queries run without an embedding service; real embeddings go under `model_id 1` (bge-m3).

## 8. Open points for JRC review

1. Confirm the `rag://` URI scheme and `chunks.id` as the preferred `jrc_database_id` target (vs unit-version level).
2. `citation_registry` write path: does the parameter pipeline register citations at proposal time or at acceptance time?
3. Object storage for large PDF snapshots (`storage_ref`) — which store on JRC infra?
4. Hunspell dictionaries for `lt`/`ga`: worth installing in the pilot image, or defer until retrieval KPIs demand it?
5. Embedding endpoint policy (kick-off Q9/Q10) — gates whether the API models join the comparison set.
