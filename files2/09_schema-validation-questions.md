# Schema Validation — Question Checklist for the JRC Team

Companion to `08_schema-proposal-for-validation.md`. Use in the validation meeting; record answers in the decision log (`07_risks-and-decisions.md`). ⭐ = blocks schema freeze.

## A. Model-side correctness (mostly Hannes + EUROMOD colleagues)

1. ⭐ Is `country + system/policy/function/parameter` a stable, unambiguous write-back address across EUROMOD system years? What breaks it (spine reordering, renamed policies, switches)?
2. ⭐ Value types: `scalar | bracket_schedule | boolean | formula` — show me 5 real parameters that *don't* fit. How are EUROMOD scales/bands structured exactly (thresholds inclusive/exclusive, per-band rates + amounts)?
3. Does the model need `currency` explicitly (national currency vs EUR conversions in non-euro member states — relevant to country selection)?
4. Units: adopt OpenFisca-style conventions (`/1` for rates, `currency-EUR`, `year`…) or an existing EUROMOD convention?
5. Are there parameters whose *validity* is not a date interval (e.g., income-year vs. tax-year semantics, retroactive application)? How does EUROMOD's system-year snapshot map onto continuous `valid_from/valid_to`?
6. ⭐ Minimal mandatory set (§4 of doc 08): confirm nothing else is strictly required to run the model.

## B. Workflow & lifecycle (Hannes + Hugo)

7. ⭐ `legal_status` enum: right granularity for projection work? Do you need `announced`? Should `national_team_estimate` be a status, a `source_type`, or both?
8. When a bill becomes law: update-in-place with status transition, or new value row? (Proposal: new row, keep the bill row as history — confirm.)
9. `last_confirmed_valid_on`: useful to you (it answers "when did we last check this is still current"), and who/what updates it?
10. Is a `supporting_extract` realistically available for most legislation-sourced parameters, or do many values only emerge from *combining* provisions (in which case: multiple extracts per reference)?

## C. Data & integration (Luis + Kosta + IT)

11. ⭐ Co-locate parameter tables in the RAG PostgreSQL: any objection (backup policies, access rights, environments)?
12. Luis — does DB-canonical + JSON-view fit the MCP interface you're exploring (MCP server reading the DB vs. serving JSON files)?
13. Kosta — does the `review_decisions` table give the UI what it needs (queue states, who-did-what audit)? What UI states are missing (e.g., `escalated_to_national_team`)?
14. JSON Schema versioning: semver in the same repo as the DDL, releases tagged — OK with GitLab conventions?
15. Hannes — Ireland JSON prototype: field-by-field mapping session; which of your names should win (cheapest moment to align is now)?

## D. Scope guards (everyone)

16. ⭐ Uprating/indexation formulas: v1 `formula` type or deferred to v2? (Recommendation: defer; store the formula as text + reference, don't parse it yet.)
17. Regional/sub-national parameters (ES, DE candidates): in scope for the pilot schema (add `jurisdiction`) or explicitly out?
18. Translations: is `label_en` + original label enough for v1, or do reviewers need translated extracts too? (Cost implication for the pipeline.)
19. Who formally accepts Deliverable 1, and does acceptance freeze v1.0 (changes after = semver + decision log)?

## E. Validation exercise (do this live, 30 min)

Pick **10 real parameters** across the pilot countries (mix: scalar, scale, eligibility, one national-team-only, one from a pending bill). For each, the team fills the schema by hand. Every friction point = a schema bug found before a single line of implementation. This exercise doubles as the seed of the Activity 4 golden set.
