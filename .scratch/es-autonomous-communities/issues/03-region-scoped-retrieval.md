# 03 — Scope retrieval to one region for regional parameters

Status: resolved
Blocked by: 02

## What

Implement whatever issue 02's ADR decides, in `retrieval.py` and the parameter
→ region resolution that feeds it.

## Acceptance

- A run for `$bsarg_rg24_basic_amt` (Aragón) retrieves Aragón's acts and the
  state-level acts, and **cannot** retrieve Asturias's or Canarias's.
- A run for a non-regional ES parameter is unchanged — same candidates, same
  ranking as before the change. Verify against a stored run, not by eye.
- The other four countries are unaffected: FR/IE/LT/NL retrieval results are
  byte-identical before and after.

## Test that must exist

The adversarial one: give the proposer a regional parameter while the corpus
holds the *wrong* region's decree with a near-identical amount, and assert the
run routes `not_found` rather than proposing the neighbouring region's value.
This is the false positive the mechanical extract check cannot catch, so it
needs a test of its own.

## Answer (2026-09-08)

Implemented per ADR 0003:

- `nomoscope_workflow/regions.py` — `region_key(country, model_target)` reads the
  NUTS-2 digits off the constant name (`rg24`/`reg24`/`…rg24`, validated against
  the country's 19 codes; digits that are not a region, or a country without a
  regional layer, give `None`).
- `retrieval.jurisdiction_scope(conn, country, region)` → `[country]` or
  `[country, child]`, the child looked up by `jurisdictions.metadata->>'nuts2'`;
  an unknown region falls back to the country alone (safe side).
- `retrieval._LIVE_VERSION_CTE` filters `j.code = ANY(%(jurisdictions)s::text[])`;
  `citation_fast_path` / `hybrid_search` / `retrieve` take a scope where they took
  a country string (every old caller still passes a string). The Country Report
  search stays country-wide on purpose.
- `pipeline.retrieve` computes the scope, records it on the span
  (`retrieval.jurisdictions`) and in the state (`jurisdictions`); the proposal
  prompt names the region for a regional parameter (`PROMPT_VERSION` 0.6.0 → 0.7.0).
- Mirrors: `nomokrisis_eval.embedding_eval` (optional `region` on
  `EmbeddingCase`), UI `db.rs` (children roll up into their country; instrument
  and chunk search include children), MCP `search.py`.

### Acceptance

- **Aragón cannot retrieve Asturias or Canarias** —
  `tests/test_regional_scope_live.py` (skips without the DB): the Aragón scope
  returns only `ES`/`ES-AR` chunks for an Asturias-worded query *and* when the
  Asturias citation is named outright; the Asturias scope does return `ES-AS`
  (so the test is not vacuous); the national scope returns no regional chunk.
  4 passed against the live corpus.
- **Non-regional ES runs**: verified by stored results, not by eye —
  `scratchpad/baseline_before.json` vs `baseline_after.json` (citation fast path
  + FTS leg, 12 queries, 5 countries). The only differences are the ES national
  queries **losing Galicia chunks** (`DL 1/2011 Galicia Artículo 4 bis` for
  «mínimo del contribuyente», arts. 14/15 for «tipo de gravamen del ahorro»):
  the pre-existing false positive, now excluded by design.
- **FR/IE/LT/NL byte-identical** in the same diff.

### The adversarial test, and what the first real run taught

The retrieval-layer test above is the mechanical guarantee. A full run was also
made for `$bsarg_rg24_basic_amt` (Aragón), `$tin_rg11_rate1` (Galicia) and
`$bsarg_rg63_basic_amt` (Ceuta) — note: with the configured default model
`azure_openai/gpt-5.6-luna`, not the mock. Results:

- Aragón: scope `[ES, ES-AR]` held — no sibling cited. But the run proposed
  **522 €** citing `Ley 3/2021 Aragón Artículo 4` with a valid extract: the
  framework law's 2021 amount, which the consolidated text never updates
  because the yearly figure arrives by budget law (not consolidated, issue 06).
  A second trap, *inside* the scope; recorded in golden case 14.
- Galicia: `not_found` in that first run — art. 4 (the 9,00 % row) was absent
  from the hybrid top-15 because the 2 377 regional chunks were **not yet
  embedded** (the vector leg was blind to them). After `embeddings build`
  (1 627 chunks on the 1080 Ti) a mock re-run retrieves `DL 1/2011 Galicia
  Artículo 4` as the **top hit**; the mock extractor still abstains (it does
  not read a rate out of a table row), which is what golden case 13 measures.
  Lesson recorded in `golden_set_ES.md`: embed after every regional ingest.
- Ceuta: `not_found`, correctly.
