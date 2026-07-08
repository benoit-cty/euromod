# Activity 4 — Validation Dataset & KPIs (35 units, deadline 15 Dec 2026)

**Deliverable:** a validation dataset + KPI report documenting agentic-workflow performance against defined KPIs. The expert *oversees* dataset creation and *organises/documents* the validation process.

---

## 1. Validation dataset design

**Golden set** per pilot country: parameters with known correct values, legal references, and effective dates — the natural source is **past EUROMOD updates** (e.g. system year Y → Y+1 transitions), because the national teams already validated them. EUROMOD Country Reports give the instrument↔parameter mapping.

Composition targets (to agree with JRC):
- ~30–60 parameters per country, stratified by:
  - type (scalar / bracket schedule / eligibility rule),
  - difficulty (value stated plainly in one article vs. requires combining provisions vs. table extraction),
  - source class (codified law / gazette / national-team-only — the last class tests the *routing*, i.e. the system should say "not derivable from legislation", not invent a citation).
- Include **negative/no-change cases** (parameter unchanged between years) — a system that flags changes everywhere is useless.
- Include a few **temporal traps** (value changed mid-year; retroactive application) to test the `as_of` logic.

Dataset format: the Activity 1 schema itself, plus an `expected_*` block. Stored and versioned in GitLab.

## 2. KPI framework (to define in the report)

**End-to-end (per parameter):**
- Value accuracy: exact match rate (scalars), structure+cell accuracy (bracket tables).
- Effective-date accuracy.
- Citation accuracy: pinpoint correct (instrument + article), and *supportedness* (does the cited text actually state the value?).
- Routing accuracy: correct classification into changed / unchanged / not-derivable.
- Hallucination rate: proposals citing non-existent or non-supporting provisions.

**Component-level:**
- Retrieval: recall@k of the ground-truth legal unit (the single most diagnostic number; if retrieval misses, nothing downstream can succeed).
- Extraction: table/schedule extraction accuracy.

**Operational:**
- Cost and latency per parameter; human review time per record (from UI decision log).
- Reviewer overturn rate (accept-as-is vs. edited vs. rejected) — the practical "trust" metric.

**Cross-cutting comparisons** (feeds Activity 5 directly): by country, by language strategy, by LLM.

## 3. Process to organise

- Freeze golden set *before* running comparative evaluations (no tuning on the test set; keep a small dev set separate).
- Every evaluation run: pinned model versions, prompts, retrieval config → run manifest committed to GitLab; results reproducible.
- Human adjudication protocol for ambiguous cases (who decides, how disagreement is recorded) — likely national-team colleagues or Hannes/Luis/Hugo for pilot countries.

## 4. Sequencing

- Start golden-set collection **during Activity 2** (Sep–Oct): it requires no working system, only past EUROMOD versions and country reports, and it forces early clarity on what "correct" means.
- Nov–Dec: evaluation runs interleaved with Activity 3 iteration; KPI report drafted from run manifests.

## 5. Open questions for JRC

- Can past EUROMOD parameter files (multiple system years) be exported for the pilot countries as ground truth?
- Who adjudicates disputed ground truth per country?
- Target thresholds: does JRC want *a priori* acceptance thresholds (e.g. retrieval recall ≥ X) or a descriptive first report? (Recommend descriptive for the pilot, thresholds for phase 2.)
