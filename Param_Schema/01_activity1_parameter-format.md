# Activity 1 — Policy Parameter Format (15 units, deadline 1 Aug 2026) — v2

**Deliverable:** a document specifying the format of the policy parameters, consumable by the agentic pipeline and by the fiscal models' teams.

**Design decision (v2):** the canonical store is **relational (PostgreSQL)**, living in the same database as the RAG; **JSON is a serialization view** of it, defined by a versioned JSON Schema, for exchange with the EUROMOD team and the agentic pipeline. Prior art: the OpenFisca parameter model and the openfisca-france metadata-normalisation RFC (issue #1672).

---

## 1. Lessons imported from OpenFisca (issue #1672)

- Date-keyed value history, per-date legal references, `official_journal_date`, short/long labels, units — all proven concepts, reused.
- **Anti-lesson**: metadata as conventions in flat files → 19–60% fill rates and unenforceable quality. Fix: database constraints for the few mandatory fields; everything else optional.
- **Anti-lesson**: references attachable at parameter root *or* per value date → ambiguity. Fix: references always attach to a `(parameter, valid_from)` value row.
- **Gap to fix**: OpenFisca commits only enacted law (a repo *policy*, not a schema property), which blocks next-year projections. Our schema represents the full legal lifecycle via `legal_status`.

## 2. Mandatory-field philosophy (hard requirement from experience)

> **Only what the fiscal model needs to apply the value is mandatory.** Everything the *workflow* needs is enforced at workflow gates, not at insertion. Everything else is optional enrichment.

Three tiers:

| Tier | Enforced by | Fields |
|------|------------|--------|
| **T1 — Mandatory** (model can't run without it) | DB `NOT NULL` | parameter identity (country, model-target address), value + value type, unit, `valid_from` |
| **T2 — Acceptance-gated** (a human may not *accept* a proposal without it) | UI/workflow rule, not DB | `legal_status`; a reference **or** explicit `source_type = national_team`; `supporting_extract` when source is legislation |
| **T3 — Optional / machine-filled** | nothing / pipeline auto-fills | labels (EN/original), `official_journal_date`, signature date, notes, confidence detail, extraction lineage (run id, model, prompt version, chunks — auto-logged, zero human cost) |

Rationale: T2 keeps rigor where it matters (nothing enters the model unvalidated) without making the schema hostile to partial/manual entry. A value row *without* a reference is itself informative — it flags a national-team-sourced or not-yet-traced parameter.

## 3. Relational model (canonical)

Core tables (detailed in `08_schema-proposal-for-validation.md`):

- `parameters` — identity & addressing: country, model target (EUROMOD system/policy/function/parameter path), labels, unit, value type (scalar / bracket_schedule / boolean / formula), and `temporal_basis` (`in_force` default | `income_year`). `temporal_basis = income_year` marks parameters where the EUROMOD system year is the *income* year while the enacting act is published the following year (FR income-tax family: the barème for 2025 income sits in the finance act consolidated in early 2026). Value rows stay back-dated to the income-year start (`valid_from = Y-01-01`, the OpenFisca convention, which coincides with EUROMOD's system-year-equals-income-year rule); the workflow uses the flag to shift *retrieval* to versions in force mid-year Y+1 and to check the cited version against the budget-act window. Curated knowledge — never derivable from the EUROMOD export, never overwritten by re-ingest.
- `parameter_values` — one row per (parameter, `valid_from`): typed value, `valid_to` (nullable = still valid), `legal_status`, `source_type`, dates (effective / publication / signature, all distinct), confidence.
- `value_references` — 0..n per value row: instrument title, pinpoint (article), URL/ELI, `supporting_extract` (verbatim original-language sentence), optional FK + offsets into the RAG's `legal_units` chunks (enables automated supportedness checks).
- `extraction_runs` — lineage: run id, model, prompt version, retrieval trace; FK from value rows proposed by the pipeline.
- `review_decisions` — accept/reject/edit log from the validation UI.

`legal_status` enum: `enacted_in_force | enacted_not_yet_in_force | adopted_pending_publication | bill_proposed | announced | national_team_estimate`. Kept **distinct from `confidence`** (law lifecycle vs. extraction reliability).

## 4. JSON interchange view

- Versioned JSON Schema (semver) in GitLab; generated from the DB, round-trippable.
- Shape stays close to the OpenFisca YAML the team already reads (date-keyed `values`, `metadata.reference` per date) so economists recognize it — see worked CDHR example in doc 08.
- This is what the agentic pipeline emits/consumes and what EUROMOD-side tooling (Hannes's Ireland JSON DB) aligns with.

## 5. Deliverable package (1 Aug)

1. `08_schema-proposal-for-validation.md` — stakeholder-facing explainer (pre-kick-off draft, exists).
2. Annotated JSON Schema + SQL DDL sketch.
3. Worked examples: FR CDHR rate (scalar, legislation-sourced), FR income-tax scale (bracket schedule), one eligibility rule, one national-team-only parameter, one `bill_proposed` forward-looking parameter.
4. Mapping guide EUROMOD ↔ schema; note on OpenFisca ↔ schema (free, demonstrates extensibility).
5. Open questions & versioning policy.

## 6. Validation process before implementation

- Acceptance = JRC sign-off on doc 08's decision points; then freeze schema v1.0.

## 7. Inputs still needed from JRC

- EUROMOD parameter export (2 pilot countries, ≥2 system years) to validate the addressing model and value types against reality.
- Hannes's Ireland JSON prototype (align field names now, cheaply).
- Confirmation of who reviews/accepts this deliverable.
