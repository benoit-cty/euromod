# IE golden set — selection and build guide

Ireland's golden set: 10 parameters in increasing pipeline difficulty, from the standard-rate
band (the happy path) up to cases the current pipeline cannot solve, kept in the set on purpose
so future improvements show up as KPI deltas instead of anecdotes. The machine-readable
selection lives in [golden_sources/ie.json](golden_sources/ie.json); this document is the
rationale and the build procedure.

## Why IE cannot be built the FR way

The FR set was drafted by `build-openfisca-dataset` from the OpenFisca-France corpus.
**Ireland has no OpenFisca package**, so there is no corpus drafter: expected values in
`golden_sources/ie.json` are hand-curated from the acts themselves and every drafted case
stays `verified: false` until a human confirms it (`nomokrisis-eval verify <id> --reviewer …`
or the UI's Golden set tab). Ireland compensates with two advantages: the legislation is
English (the project's control case for the multilingual claim), and the annual Finance /
Social Welfare Acts state parameter values verbatim — Finance Act 2024 s. 3 alone carries
essentially the whole PIT parameter set for 2025.

Corpus status (see `Nomotheca-RAG/Ireland_sources_analysis.md`): 15 acts ingested end-to-end
(TCA 1997 and SWCA 2005 as closed-validity baselines, plus the Finance and Social Welfare
Acts 2022–2025), ~2,600 chunks. Ireland has **no consolidation**: values arrive via annual
amending acts that are never repealed, so evidence retrieval must prefer the amending act row
with the greatest validity start ≤ `as_of`.

## Build procedure

```bash
# 1. Materialize IE parameter records from the store (golden cases must point at
#    data/parameters/eval/, never a hand-authored file)
cd ../Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow ingest-params            # loads extracted_parameters/enriched/IE.enriched.json

# 2. Draft the 10 cases from golden_sources/ie.json (no LLM: the expected values are the
#    curated ones, the parameter under test comes from the params DB). Routing is never
#    decided by a model; ie.json sets it explicitly, and the drafter cross-checks it
#    against what EUROMOD holds and reports every disagreement.
cd ../../Nomokrisis-evaluation_pipeline
uv run nomokrisis-eval build-curated-dataset --country IE --year 2025

# 3. Human-verify each case (the freeze gate — run evaluates verified-only)
uv run nomokrisis-eval verify <case-id> --reviewer ben

# 4. Run
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor   # smoke
```

### Prerequisites and gaps (status at 2026-09-01)

- ✅ **Scout**: IE added to `scout.COUNTRY_SOURCES` / `ID_HINTS` (domain `irishstatutebook.ie`,
  id pattern `<year>/act/<no>` — the eISB ELI act id, which is also `instruments.national_id`).
  Acts only; statutory instruments (`/eli/<year>/si/<no>`) are not ingestible yet.
- ❌ **`curation/IE.curation.yaml` does not exist.** Needed for (a) the `national_team` flag on
  the `tco_ie` consumption-tax family (case 10), (b) recording that IE PIT parameters are
  `in_force` — the Finance Act's "year of assessment 2025" *is* the system year, no FR-style
  income-year offset.
- ❌ **Two scoring gaps** in `src/nomokrisis_eval/scoring.py::normalise_value`:
  percent strings (`'4.1%'`) don't normalise and fall back to strict string equality (case 7),
  and `'140#m*$sw_weeks'` silently truncates at `#` because it parses as a Python comment
  (case 9). Fix or keep string-form expected values.
- ⚠️ **The IE export is the old schema** (bare JSON list, no `groups` block), so no
  bracket-schedule (`table`) case can be assembled — band/rate scalars stand in for it until a
  re-export or a curated group definition exists.

## The 10 cases

| # | Target | 2025 value | Difficulty | Expected routing | Source |
|---|--------|-----------|------------|------------------|--------|
| 1 | `$tin_StdSingleband_lim` | 42,000 → **44,000** | easy | changed | FA 2024 s. 3 / TCA s. 15 |
| 2 | `$tin_high_rate` | 0.40 (since 2015) | easy | unchanged | TCA s. 15 |
| 3 | `$tin_PersTC_amt` | 1,875 → **2,000** | easy-medium | changed | FA 2024 s. 3 / TCA s. 461 |
| 4 | `txcin_ie/$txcin_rate3` | 0.04 → **0.03** | medium | changed | FA 2024 s. 2 / TCA s. 531AN |
| 5 | `$txcin_upthres2` | **27,382** (law) vs 27,383 (EUROMOD) | medium | changed | FA 2024 s. 2 / TCA s. 531AN |
| 6 | `bunct_ie/$bunct_Rate1` | 109.50 €/week | medium-hard | changed | SW Act 2024 / SWCA Sch. 2 |
| 7 | `tscee_ie/$tscee_prsiA_rate1` | '4.1%' (→ 4.2% on 1 Oct) | hard | changed (explicit) | SWCA s. 13 |
| 8 | `benergy_cred_ie/$benergy_amt` | 125 | hard — `not_found` today | changed | Electricity Costs Emergency Measures Acts (NOT ingested) |
| 9 | `bch_ie/$bch_amt1` | `140#m*$sw_weeks` | impossible today | derived | SWCA Sch. 4 |
| 10 | `tco_ie/$tco_t_01131` | n/a | impossible forever | national_team_source | none (HBS statistics) |

Rationale per tier:

1–3. **The happy path plus its mirror.** The band the JRC will ask about first, a genuine
change stated verbatim in an ingested English act; the higher rate as the no-change trap
(the surrounding bands move every year — the pipeline must not infer a change it cannot
quote); the personal credit from the *same* section, testing multi-parameter extraction from
one dense amending section.

4–5. **USC.** The middle-rate cut is a clean numeric change. The 2% ceiling is the set's
deliberate discrepancy case: **the law says €27,382** (€12,012 + €15,370), EUROMOD stores
€27,383. Decision (2026-09-01): keep the **law's value as golden**, mirroring the FR barème
1-€ erratum precedent — the 1e-6 tolerance keeps the difference visible, and the EUROMOD-side
off-by-one goes to the economists team as a finding, not into the ground truth.

6–7. **Weekly-basis welfare and PRSI.** IE's dominant period is `#w` (105 parameters), so the
×4.34 cross-period conversion gets real coverage that FR never gave it. The Jobseeker's
graduated rate lives in a schedule *table* of the annual act, not prose. PRSI adds the
mid-year trap: the rate steps every 1 October (4.0 → 4.1 → 4.2 through 2028 per the 2024
roadmap act), the exact ambiguity `route_against_current` refuses to draft on its own —
routing is set explicitly in the selection file.

8. **The scout case.** The Budget 2025 electricity credit's acts are not among the 15
ingested — today this is an honest `not_found`; after scout gap-fill (now enabled for IE) and
ingest it should flip to `changed`. This case *is* the metric for that improvement.

9–10. **The impossible tier.** Child Benefit is stored as `140#m*$sw_weeks`, so the derived
check short-circuits before retrieval even though €140/month sits plainly in SWCA Sch. 4 —
expected routing pins today's contract (`derived`, value unscored); the future
anchor-resolution capability flips the expectation to a scored value. The `tco_ie` implicit
consumption-tax rate has no legislative source at all (Household Budget Survey statistics):
correct behaviour is a `national_team_source` refusal, which needs the missing
`IE.curation.yaml` — the FR set has zero such traps.

## What this fixes in the FR set's blind spots

FR: 42/47 `unchanged`, all plain/codified, zero `national_team` / `new` / `not_found` /
`derived` routings. IE adds: schedule-table retrieval, heavy `#w` conversion, a mid-year
(October) rate step, an honest `not_found` with a measurable path to green, a `derived`
short-circuit, and a `national_team_source` refusal.
