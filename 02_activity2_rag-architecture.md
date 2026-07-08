# Activity 2 — Multilingual RAG Architecture (100 units, deadline 15 Nov 2026)

**Deliverable:** an architecture proposal document serving as basis for implementation (with the JRC.B.2 IT team). Gates the interim payment together with Activity 1.

Contractual requirements to satisfy explicitly:
1. Multilingual, extensible in legal domain and member states.
2. Parses fiscal law into a machine-digestible format.
3. **Tracks law over time**; answers questions about fiscal law *at specific points in time*.
4. Documented; versioned in JRC GitLab.

---

## 1. Proposed architecture layers (to defend in the document)

### 1.1 Ingestion — one adapter per country/source type
- No common EU API exists for national tax/benefit law → per-country adapters (PDF gazette parsers, HTML portal scrapers, official APIs where they exist).
- Adapter output normalises into a common **legal document model**: instrument → article → paragraph, with metadata (ELI identifier where available, publication date, entry-into-force date, amending/amended relations).
- France: Légifrance/DILA (LEGI consolidated base is the natural target — consolidated versions carry effective dates natively); note the Tricoteuses/Canutes + Anubis anti-bot lesson: prefer official bulk downloads (DILA open data dumps) over scraping.
- Ireland: electronic Irish Statute Book (eISB) + Revenue guidance; align with Hannes's JSON DB experiment.
- Decide per pilot country during kick-off; document the adapter interface so a new country = a new adapter, nothing else changes.

### 1.2 Normalisation & temporal model
- **Chunk by legal unit** (article/paragraph), never by token window.
- Temporal design decision to argue in the proposal: store **consolidated versions with validity intervals** (`valid_from`/`valid_to` per unit) rather than diff-chains of amendments. Point-in-time query = filter on interval, then retrieve. Amendment lineage kept as metadata for provenance, not as the primary query path.
- Store original-language text always; machine translation (into EN) stored *alongside*, flagged as derived, for cross-lingual retrieval and for economists' review.

### 1.3 Storage
- Baseline recommendation: **PostgreSQL + pgvector + native full-text search** — one system for structured metadata, vectors, BM25-style lexical search, and temporal filtering. Contrast with MongoDB in the proposal (weaker for relational temporal queries and hybrid search); acknowledge Hannes's JSON-DB test as a schema-shape input rather than a storage-engine decision.
- Schema outline: `instruments`, `legal_units` (with validity intervals), `chunks` (unit-aligned), `embeddings`, `sources` (provenance), `translations`.

### 1.4 Retrieval
- **Hybrid retrieval**: BM25/lexical + dense embeddings + reranker. Legal text demands exact matching of statute numbers and defined terms; pure semantic search fails there.
- Multilingual strategy to compare in the report (this doubles as evaluation material for Activity 5):
  - (a) query in EN → retrieve on translations,
  - (b) multilingual embedding model over original text,
  - (c) query translation into target language.
- Point-in-time parameter: every retrieval call takes an `as_of` date; filter before ranking.
- Secondary **structured extraction pass** for numeric tables/schedules (rates, brackets) — semantic retrieval alone won't reliably read a rate table; a dedicated extraction step feeds Activity 1's format.

### 1.5 The hybrid-source principle (RAG ≠ whole truth)
- Explicitly architect for parameters with **no formal legislative source** (set by national teams, or voted but not yet published): a structured database fed by national-team input sits beside the RAG, unified under the Activity 1 provenance schema. The proposal should present this as a feature, not a caveat — it's what makes the system honest about traceability.

## 2. Non-functional requirements to pin down with the IT team

- Hosting & compute (JRC infra? AWS Bedrock availability inside JRC? GPU access for embedding/reranking?)
- Allowed model endpoints (embedding models, rerankers, LLMs) and data-residency constraints for legal texts (public data, but check policy anyway).
- GitLab CI expectations, code review process, licence for produced code.
- Corpus size estimates per country → storage/index sizing.

## 3. Document outline (the deliverable)

1. Requirements restated (functional + non-functional)
2. Reference architecture diagram (ingestion → normalisation → storage → retrieval → API)
3. Temporal model design & justification
4. Multilingual strategy & alternatives compared
5. Country adapter specifications (per pilot country: sources, format, access method, known frictions)
6. Storage schema
7. Retrieval pipeline (hybrid + rerank + as_of)
8. Integration contract with the agentic workflow (API surface)
9. Implementation plan & division of work (expert ↔ IT team)
10. Risks & open questions

## 4. Sequencing within the activity (Jul–Nov)

- Jul–Aug: source survey per candidate country (feeds country selection), adapter interface draft.
- Sep: architecture draft v1 → **Seville visit** for whiteboarding with IT team.
- Oct: prototype-informed revisions (a thin vertical slice on France + Ireland de-risks the proposal).
- Early Nov: final proposal, acceptance, interim payment claim.

## 5. Key risks

- Source access friction (anti-bot, PDFs of scanned gazettes, OCR quality) — mitigate via official bulk/open-data channels first.
- Temporal consolidation availability varies by country: some publish consolidated versions (FR LEGI), others only amendment acts → adapter effort asymmetry; pick pilot countries with eyes open.
- Scope creep from "extensible to all EU law" — extensibility is an architectural property to demonstrate, not 27 adapters to build.
