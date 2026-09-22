# Risk Register & Decision Log

## 1. Risk register (initial)

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|------------|
| R1 | LLM endpoint constraints (e.g. OpenAI-only via ALOHA) block the contractual multi-LLM comparison | M | H | Resolve endpoint question at kick-off (Q10); fallback = open-weight models on JRC/Bedrock infra |
| R2 | Source-access friction (anti-bot middleware à la Anubis/Tricoteuses, scanned PDFs, OCR) delays ingestion | H | M | Prefer official bulk/open-data channels (DILA dumps, eISB); pick pilot countries with source survey done *before* committing |
| R3 | Activity 1 deadline (4 weeks incl. kick-off) too tight | M | M | Pre-draft schema before kick-off; scope to pilot needs only |
| R4 | Temporal consolidation unavailable for some countries (only amendment acts published) | M | H | Country selection criterion; adapter effort asymmetry documented in D2 |
| R5 | Hallucinated/unsupported citations undermine trust of modelling teams | M | H | Critique step, verbatim-quote rule, supportedness KPI, human-in-the-loop UI |
| R6 | Golden-set ground truth disputed or unavailable (past EUROMOD exports) | M | H | Request exports at kick-off (Q5); adjudication protocol with country experts |
| R7 | Scope creep: "extensible to all EU law / 27 countries" read as build-it-now | M | M | Architecture demonstrates extensibility; pilot delivers 5 adapters max, thin slices |
| R8 | JRC report clearance slower than 31 Dec deadline | M | M | Draft continuously; near-final by early Dec; clarify "draft vs cleared" at kick-off (Q19) |
| R9 | IT-team availability/bandwidth mismatch on shared activities (2 & 3 UI) | M | M | Explicit division of labour at kick-off (Q15); interfaces specified so work parallelises |
| R10 | Non-codified parameters treated as RAG failures instead of a distinct source class | L | M | Provenance schema from Activity 1; routing KPI in Activity 4 |
| R11 | JRC insists on exhaustive upfront corpus (reading Activity 2 as "full RAG"), blowing the 20-day budget | M | H | Decision doc `10_retrieval-strategy-challenge.md`; get reviewer's written agreement on "lazy RAG" reading at kick-off (Q3b); fallback = bulk-ingest only 1–2 easy countries, lazy for the rest |
| R12 | Live agentic fetching hits anti-bot/rate limits at run time | M | M | Cache-first design (each source hit once); official bulk endpoints preferred; freeze cache before eval runs |

## 2. Decision log (template — append as decisions land)

| # | Date | Decision | Options considered | Rationale | Owner |
|---|------|----------|--------------------|-----------|-------|
| D-001 | (kick-off) | Pilot countries: … | … | accessibility × language spread | joint |
| D-002 | | Storage engine: PostgreSQL+pgvector vs MongoDB | | | |
| D-003 | | Orchestrator: LangGraph / ALOHA / other | | | |
| D-004 | | Temporal model: consolidated-with-intervals vs amendment-diff-chain | | | |
| D-005 | | UI stack: Tauri+Svelte vs web app on JRC infra | | | |
| D-006 | | LLM set for comparison: … | | | |

## 3. Assumptions to verify

- A1: Contract start ≈ early July 2026 (D1 deadline 1 Aug = start + 4 weeks).
- A2: "Implementation" in Activity 2 means a working vertical slice + proposal doc, not production system for 5 countries.
- A3: Write-back to EUROMOD files is export-based, not direct modification.
- A4: National legal texts are public data and may be sent to external LLM APIs (verify, Q13).
