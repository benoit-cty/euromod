# Activity 5 — Technical Report (30 units, deadline 31 Dec 2026)

**Deliverable:** co-authored technical report describing the RAG system and agentic workflow, evaluating performance across countries and across LLMs.

Strategy: this report should be ~80% assembled from artefacts produced anyway (Deliverables 1–4 + run manifests). Write it continuously; December is for editing, not writing.

---

## 1. Proposed skeleton

1. **Introduction & motivation** — EUROMOD update burden; traceability of parameters to law; why AI-assisted, why human-in-the-loop.
2. **Problem framing** — parameter taxonomy; the hybrid-source reality (legislation-derivable vs. national-team-sourced); temporal requirements.
3. **System description**
   - Policy parameter format (from D1)
   - RAG architecture: ingestion adapters, temporal model, storage, hybrid retrieval, multilingual strategy (from D2)
   - Agentic workflow & validation UI (from D3)
4. **Evaluation setup** — golden set construction, KPI definitions, run protocol (from D4).
5. **Results**
   - By country: accessibility/language effects (the contract's explicit comparison axis)
   - By LLM: value/citation accuracy, hallucination rate, cost
   - By retrieval strategy (lexical vs. hybrid vs. rerank; multilingual variants) — cheap ablations, high report value
   - Human-review metrics (overturn rate, review time)
6. **Discussion** — where the pipeline is trustworthy today; failure taxonomies (retrieval miss vs. extraction error vs. reasoning error); the non-codified-parameter problem as a structural finding.
7. **Roadmap** — scaling to 27 member states (adapter effort model), other fiscal models (EDGE-M3, DIRECT), other legal domains.
8. Annexes: schema, KPI tables, per-country adapter notes.

## 2. Co-authoring logistics to agree at kick-off

- Authorship & credit (expert + Hannes + others?); JRC technical-report template and publication channel (JRC Publications Repository? internal?); review/clearance timeline — JRC clearance can be slow, so a 31 Dec deadline means a near-final draft by **early December**.
- Language: English. Figures pipeline (architecture diagrams reused from D2/D3).

## 3. LLM comparison scope (needs early confirmation)

"Different LLMs" is contractual → confirm at kick-off which endpoints are actually usable (Bedrock models, Anthropic, OpenAI/Azure, open-weight). Budget eval runs accordingly; 2–3 models × golden set is enough for a credible comparison at pilot scale.
