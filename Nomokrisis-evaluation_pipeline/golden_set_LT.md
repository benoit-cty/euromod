# LT golden set — selection and build guide

Lithuania's golden set: 10 parameters in increasing pipeline difficulty, from the PIT rate
schedule up to cases the current pipeline cannot solve (Government resolutions not yet
ingested, indexation-derived amounts, a statutory step schedule, and the ready-made
`national_team` trap). The machine-readable selection lives in
[golden_sources/lt.json](golden_sources/lt.json); this document is the rationale and the
build procedure.

## Why LT cannot be built the FR way

**Lithuania has no OpenFisca package**, so there is no corpus drafter: expected values in
`golden_sources/lt.json` are hand-curated from the six ingested anchor acts (cross-checked
against `LT_Y16.md` — the Country Report is context, never evidence) and every drafted case
stays `verified: false` until a human confirms it. LT is the multilingual test proper: the
authentic texts are Lithuanian, so the translate leg and per-language KPI split (Activity 5)
get real data here.

Corpus status (see `Nomotheca-RAG/Lithuania_sources_analysis.md`): all six anchor acts
ingested via the data.gov.lt Spinta API — GPMĮ (PIT, IX-1007), VSDĮ (social insurance,
I-1336), LMSDĮ, IVĮ (child benefits, I-621), PSPĮ (health insurance), NSDĮ — ~2,900 chunks,
with `galioja_nuo/galioja_iki` mapping natively onto versioned validity (full point-in-time,
better than IE). **Not ingested yet**: Government *nutarimai* (MMA/BSI/SPB amounts) — open
point §5.2 of the sources analysis, and exactly what the hard tier of this set measures.

## Build procedure

```bash
# 1. Materialize LT parameter records AND apply the curation overlay (order matters:
#    ingest-params replaces model_values rows, the overlay follows it)
cd ../Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow ingest-params
uv run nomoscope-workflow curate-params curation/LT.curation.yaml

# 2. Draft the 10 cases from golden_sources/lt.json (no LLM: the expected values are the
#    curated ones, the parameter under test comes from the params DB). The PIT schedule
#    case uses group_id LT:ConstDef_lt:tin_schedule (the LT export is the new schema and
#    carries a groups block, unlike IE).
cd ../../Nomokrisis-evaluation_pipeline
uv run nomokrisis-eval build-curated-dataset --country LT --year 2025

# 3. Human-verify (the freeze gate)
uv run nomokrisis-eval verify <case-id> --reviewer ben

# 4. Run
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor   # smoke
```

### Prerequisites and gaps (status at 2026-09-01)

- ✅ **Scout**: LT already in `scout.COUNTRY_SOURCES` (e-seimas/e-tar domains, TAR id pattern,
  `/asr` consolidation-index suffix) with *nutarimai* in its `act_kinds` — case 7 exercises it.
- ✅ **Curation**: `curation/LT.curation.yaml` exists and flags the `xcc_lt` family
  `national_team` (case 10). Must be applied after every `ingest-params`.
- ❌ **Percent-string scoring gap**: 59 LT parameters store rates as `'20%'`-style strings with
  `value: null`; `normalise_value` has no `%` branch, so they fall back to strict string
  equality and `route_against_current` refuses to draft routings for them. The selection file
  sets explicit routings and string-form expected values as the workaround (cases 1, 4).
- ⚠️ **The export projects values to 2027** (uprating projections): drafting must read the
  value in force at `as_of`, never the last row.
- ⚠️ **The `tin_schedule` group is rates-only** — thresholds come out of
  `paramdb.load_group_record` as 0.0. Check the assembled record before writing the
  `list[Bracket]` expectation; the 60-VDU threshold is case 6's job instead.

## The 10 cases

| # | Target | 2025 value | Difficulty | Expected routing | Source |
|---|--------|-----------|------------|------------------|--------|
| 1 | group `LT:ConstDef_lt:tin_schedule` | 20% / 32% | table | unchanged | GPMĮ 6 str. |
| 2 | `$tinta_basic_WithdRate_Higher` | 0.50 → **0.49** | easy | changed | GPMĮ 20 str. |
| 3 | `$tinta_max_amt` | 747 €/m (no 2025 change) | medium | unchanged | GPMĮ 20 str. |
| 4 | `$tsceepi_rate` | '8.72%' (since 2019) | medium | unchanged | VSDĮ |
| 5 | `$bchnm_coef` | 1.75 (since 2021) | medium-hard | unchanged | IVĮ 6 str. |
| 6 | `$tin_MaxLimit_coef3` | 60 (VDU multiple) | hard (combine) | unchanged | GPMĮ 6 str. / VSDĮ |
| 7 | `$MMS` | 924 → **1,038** €/m | hard — `not_found` today | changed | Vyriausybės nutarimas (NOT ingested) |
| 8 | `$BasicPens` | 269.77 → **298.45** €/m | impossible today | changed | indexation resolution (NOT ingested) |
| 9 | `$PensionAgeFemale` | 64.66 (= 64 y 8 m) | impossible today | changed | VSPĮ I-549 (step schedule) |
| 10 | `xcc_lt/$xcc_amt1` | 2.6 €/working day | impossible by design | national_team_source | none (municipal resolutions) |

Rationale per tier:

1–2. **The GPMĮ happy path.** The rate schedule is LT's answer to the FR barème, assembled
from the export's own `groups` block — unchanged for 2025 (the 25% middle band only enters
with the 2026 reform: `$tin_HigherRate`'s first value row is 2026-01-01, so the 2025 schedule
has two live bands — a subtle table-shape trap). The NPD withdrawal coefficient 0.5 → 0.49 is
the genuine numeric change stated verbatim in GPMĮ art. 20.

3–5. **Unchanged traps of increasing subtlety.** Maximum NPD: EUROMOD stores `8964#y`, the
law states €747/month — expected `747#m`, exercising the y↔m conversion — and 2025 brought
*no* change to a parameter that usually moves yearly (the lag-warning scenario: only the act
proves `unchanged` is right). The pension SIC rate adds the percent-string gap. The child
benefit coefficient tests that the pipeline extracts the *legislated* quantity — the law
states benefits as coefficients of the basic social allowance (1.75 × BSA), so the euro
amount changes when the BSA nutarimas changes even though the legislated coefficient does not.

6. **The combine case.** The law says "60 average wages"; EUROMOD stores the bare 60 and
computes the euro cap as `$AMS × 60 / 12` — LT's counterpart of FR's PSS ×3/×4/×8 cases.

7–9. **The impossible tier, each marking a different capability gap.** MMA (€1,038): set by
an annual Government nutarimas, an instrument class not yet ingested — the scout is armed for
LT, so this case *is* the nutarimai-ingestion metric. Basic pension (€298.45): the law states
the indexation *formula*, the number exists only in the annual indexation resolution — pure
extraction can never produce it; measures a future compute-from-formula or
resolution-ingestion step. Pension age (64.66): the statute states a step schedule (+4
months/year to 65 in 2026), so the per-year value must be *derived* and month-fractions
converted to EUROMOD's decimal convention — derivation-not-extraction, plus a representation
trap (64.66 vs 64.67).

10. **The refusal case.** Municipal pre-school meal fees have no national legal source; the
curation overlay already routes them `national_team` — the golden case checks the pipeline
honours it (`national_team_source`, never `not_found`, never an overwrite proposal). The FR
set has zero such traps.

## What this fixes in the FR set's blind spots

FR: 42/47 `unchanged`, all plain/codified, zero `national_team` / `new` / `not_found` /
`derived` routings, one table case. LT adds: a second bracket-schedule case with a
band-count trap, coefficient-vs-euro extraction, four honest-failure cases each tied to a
specific named improvement (nutarimai ingest, indexation computation, schedule derivation,
percent-string normalisation), and the repo's first ready-made `national_team_source` trap —
plus the whole set runs on Lithuanian-language evidence, giving the per-language KPI split
its first real non-French data point.
