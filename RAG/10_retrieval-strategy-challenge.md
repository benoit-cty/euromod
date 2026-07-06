# Retrieval Strategy — Challenging the Full RAG (Decision Document)

*For discussion with JRC.B.2 before/at kick-off. This challenges the default reading of Activity 2 and proposes a leaner architecture compatible with the contract. Companion questions in §5.*

---

## 1. The insight that changes the problem

Parameter updating is **mostly lookup, not open-ended search**:

- For the vast majority of updates, we start from an existing parameter that already carries a legal citation (last year's reference: instrument + article).
- The retrieval task is then: *"give me the consolidated text of that article, as applicable on date X"* — a deterministic fetch, not a semantic search.
- Open-ended semantic retrieval is only needed for a minority of cases: brand-new instruments, renumbered/moved articles, parameters with no prior citation, "where is concept Y codified?" questions.

Embedding-based RAG is engineered for the minority case. Building its full ingestion pipeline (per-country parsers, OCR, chunking, embedding, refresh jobs) for 5 countries upfront is the single most expensive item in the project — and 20 expert-days cannot absorb it.

## 2. Three candidate architectures

### A. Full upfront RAG (default reading of the contract)
Ingest the fiscal law of 5 countries → normalize → chunk → embed → hybrid retrieval.
- ✅ Complete corpus asset; best for open-ended questions; reproducible.
- ❌ Ingestion cost dominates the project; refresh pipeline needed forever; most of the corpus never queried; OCR/parsing quality battles for hard-access countries.

### B. Pure agentic retrieval ("agent with country skills", no corpus)
An agent with one **skill per country** (instructions + scripts: endpoints, search strategy, consolidation quirks — cf. Hugo's scraper/skills exploration) fetches live from official sources at run time.
- ✅ Near-zero ingestion; always current; effort scales with usage, not corpus size; per-country skills map 1:1 to the contract's "accessibility comparison" axis.
- ❌ **Fails the contract's point-in-time requirement** wherever portals only serve current consolidations (FR LEGI supports as-of dates natively; most countries don't). Non-reproducible evaluation runs (live web changes between runs). Anti-bot friction (Anubis-type) moves from ingestion time to run time = unpredictable mid-run failures. No corpus asset delivered to JRC.

### C. **Lazy, agent-populated RAG (recommended)**
Country skills define *how to fetch*; every fetched legal unit is **archived** into the PostgreSQL legal-unit store (with validity interval, source URL, retrieval date, original text). Retrieval order:
1. **Citation lookup** in the cache (exact instrument+article+date match);
2. **Lexical search** (Postgres full-text / BM25) over the cache;
3. **Agentic fetch** via the country skill on cache miss → result archived → answer served;
4. **Embeddings: deferred.** Added later *only if* retrieval KPIs show lexical+lookup failing on real cases. Architecture reserves the slot (pgvector column), implementation waits for evidence.

- ✅ Point-in-time capability: snapshots accumulate with validity dates — the cache **is** the temporal store the contract demands. Reproducibility: eval runs hit the frozen cache. Anti-bot friction handled once, at first fetch. JRC still receives a corpus (built where it matters, i.e., where parameters actually live). Ingestion effort ≈ 0 upfront. Same golden set and KPIs apply unchanged.
- ❌ Corpus coverage is demand-driven, not exhaustive (must be stated honestly in the proposal); first-query latency; skills require per-country maintenance (but so would ingestion parsers — skills are the cheaper adapter).

## 3. Why C is still, contractually, a RAG

Activity 2's requirements → how C satisfies them:
- *"Parse fiscal law in a machine-digestible format"* → the legal-unit store (per-article records, metadata, validity intervals).
- *"Track the law over time / answer at specific points in time"* → validity-dated snapshots in the cache; as-of queries filter the cache.
- *"Multilingual, extensible in domain and member states"* → new country = new skill file; skills are cheaper adapters, same extension model.
- *"Architecture proposal documented, GitLab"* → unchanged; the proposal simply specifies lazy population and evidence-gated embeddings.

Framing for JRC: not "no RAG" but **"retrieval-first RAG with on-demand corpus construction"** — retrieval-augmented generation does not mandate a pre-built vector index.

## 4. What this buys the 20-day budget

- Eliminates the bulk-ingestion workstream (the largest item in plan v1) — several days recovered.
- The per-country skill for France can seed from existing Légifrance/DILA knowledge (Tricoteuses/Canutes lessons); Ireland aligns with Hannes's prototype; Hugo's skills exploration becomes mainline work, not a side track.
- Embedding/reranking infrastructure (GPU, model choice, chunk tuning) drops out of the critical path entirely.
- The vertical slice becomes achievable end-to-end in ~2–3 days: known parameter → citation lookup → skill fetch → proposal → review.

## 5. Questions to validate with the team

1. ⭐ Does JRC expect an **exhaustive corpus** as a deliverable/asset in itself, or is a demand-driven cache acceptable? (This is the fork between A and C — everything else follows.)
2. ⭐ Hugo — state of the scraper/skills exploration: which countries covered, what interface, can it be promoted to the official country-adapter mechanism?
3. For the pilot countries: which official portals support historical/point-in-time consolidations natively (FR: yes via LEGI)? Where they don't, is lazy snapshotting from now on acceptable, accepting thin history for past dates?
4. What share of pilot parameters have a prior citation in EUROMOD Country Reports? (If >80%, the lookup-first argument is empirically settled — checkable in an afternoon.)
5. ⭐ Is "embeddings only if KPIs demand it" acceptable in the Deliverable 2 architecture, with the pgvector slot reserved? (Keeps the multilingual-embedding comparison available for the report if activated.)
6. Rate limits / ToS / robots policies of the official portals for agentic fetching — any JRC constraint on automated access from its infrastructure?
7. Reproducibility rule for Activity 4: freeze the cache before comparative runs (proposed) — agreed?
8. Does the interim-payment reviewer agree this reading satisfies Activity 2's wording? (Get this in writing before building.)

## 6. Recommendation

Adopt **C** as the baseline in the Deliverable 2 proposal; present **A** as the documented scale-up path (bulk-ingest a country when usage justifies it) and **B** as rejected-with-reasons. Decision to be recorded as D-007 in the decision log.
