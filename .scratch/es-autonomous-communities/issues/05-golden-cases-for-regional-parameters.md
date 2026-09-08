# 05 — Golden cases for regional parameters

Status: resolved — 5 cases drafted, verified:false; the positive pair waits on 06
Blocked by: 03, 04

## What

Add regional cases to the ES golden set once retrieval can scope them. They
cover a difficulty tier no current case reaches: correct evidence exists, but
in a *sibling* document that must not be cited.

Suggested cases:
- One straightforward regional amount whose decree is ingested → expect a
  correct proposal citing that region's act.
- One region whose act BOE does not consolidate (from issue 01's table) →
  expect `not_found`, and it must stay `not_found`, never a proposal off a
  neighbouring region.
- One adversarial pair: two regions with near-identical amounts, both
  ingested. Expect each to cite its own decree.

## Note

Do not fold these into the existing ES selection file until issue 03's
acceptance tests pass. A golden case that depends on unbuilt retrieval scoring
as a model failure is exactly the artifact `/review-eval` exists to catch.

## Answer (2026-09-08)

Five entries added to `golden_sources/es.json` and built into `dataset/es/`
(`build-curated-dataset --country ES --year 2025`; all `verified: false`, rationale
in `golden_set_ES.md` § "The regional tier"):

| Case | Expected | Role |
|---|---|---|
| `tin_rg11_rate1` (Galicia) | 0.09, `DL 1/2011 Galicia Artículo 4` | the one straightforward positive available today |
| `bsarg_rg24_basic_amt` (Aragón) | `not_found`, hazard `sibling_region` | value in an unconsolidated decree; siblings out of scope; own framework law stale (522) |
| `bsarg_rg63_basic_amt` (Ceuta) | `not_found` | no BOE form at all — the regional IPREM |
| `bsarg_rg53_amt1` (Balears) / `bsarg_rg70_amt1` (Canarias) | `not_found` each, hazard `sibling_region` | the adversarial pair: identical 733,60 €; after issue 06 each must cite its own act |

Deviations from the suggestion above, and why:

- The "straightforward regional amount whose decree is ingested" is a **regional
  IRPF** constant, not a `bsarg_es` one: issue 01 showed the consolidated
  framework laws state none of the 2025 minimum-income amounts. The Galicia
  decree is the only ingested regional act that states a current EUROMOD value
  verbatim, and it proves the same pattern (region-scoped retrieval, region-
  qualified citation).
- The adversarial pair is drafted as **two abstentions** today, not two positives
  — neither act states the amount. It is kept because it is exactly the pair to
  flip to positives once issue 06 lands the budget-law text, and because the
  abstention itself is adversarial: Balears' scope holds a *2016* schedule
  (429,20) and Aragón's a *2021* amount (522) that a model will happily cite.
- `not_found` is stated with `expected_value: null` (so a borrowed value scores
  as a routing failure), and a new hazard `sibling_region` was added to the
  eval schema.
- A `region` field was added to `EmbeddingCase` so retrieval-only cases can be
  scoped the same way; none written yet.

Not folded into anything until verified — the drafts are `verified:false` and
the existing 12 ES cases were re-drafted by the same build (`git diff dataset/es`
shows the exact change; see the summary before committing).
