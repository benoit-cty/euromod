# ES golden set — selection and build guide

Spain's golden set: 12 parameters in increasing pipeline difficulty, from the personal
minimum (the happy path) up to cases the current pipeline cannot solve — a value fixed by
reference to an act that is not ingested, a retroactive provision the corpus only holds from
July, the budget-law value that no act in the corpus states, and two refusal cases, one of
them with the *wrong* answer sitting in the corpus. The machine-readable selection lives in
[golden_sources/es.json](golden_sources/es.json); this document is the rationale and the
build procedure.

## Why ES is built the IE/LT way

**The store has no OpenFisca corpus for Spain** (`params.external_corpora` holds only
openfisca-france), so there is no corpus drafter: expected values in `golden_sources/es.json`
are hand-curated from the six ingested acts, every one located in the corpus at
`as_of` 2025-06-01 before being written down, and every drafted case stays
`verified: false` until a human confirms it (`nomokrisis-eval verify <id> --reviewer …` or
the UI's Golden set tab). The Country Report (`08 - EUROMOD Triangulator/country-reports/
Y16/ES_Y16.md`, *Main policy changes between 2024-2025*) was used to find where 2025 moved;
it is context, never evidence.

Corpus status (see `Nomotheca-RAG/Spain_sources_analysis.md` §6): six acts ingested through
`countries/es/` via the BOE `legislacion-consolidada` API — LIRPF (Ley 35/2006,
`BOE-A-2006-20764`), RIRPF, LGSS (RDL 8/2015, `BOE-A-2015-11724`), Ley IMV (19/2021,
`BOE-A-2021-21007`), SMI RD 87/2025, DL 1/2011 Galicia — 2 786 chunks, all embedded, all
translated to English. BOE versions **per provision** with `fecha_vigencia`, the closest
native fit to `legal_unit_versions` of any pilot country. **Not ingested**: the budget law
(Ley 31/2022, prorogued through 2025), the annual pension-revalorisation instrument, the
annual Orden de cotización, the VAT/excise acts, and every regional PIT law but Galicia's.

## Build procedure

```bash
# 1. Materialize ES parameter records AND apply the curation overlay (order matters:
#    ingest-params replaces model_values rows, the overlay follows it)
cd ../Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/ES.enriched.json
uv run nomoscope-workflow curate-params curation/ES.curation.yaml

# 2. Draft the 12 cases from golden_sources/es.json (no LLM: the expected values are the
#    curated ones, the parameter under test comes from the params DB). The savings-scale
#    case uses group_id ES:tin_cons_es:tin_capinc_schedule.
cd ../../Nomokrisis-evaluation_pipeline
uv run nomokrisis-eval build-curated-dataset --country ES --year 2025

# 3. Human-verify (the freeze gate)
uv run nomokrisis-eval verify <case-id> --reviewer ben

# 4. Run
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor --country ES   # smoke
```

### Prerequisites and gaps (status at 2026-09-08)

- ✅ **Scout**: ES in `scout.COUNTRY_SOURCES` / `ID_HINTS` (domain `boe.es`, id pattern
  `BOE-A-YYYY-NNNNN`, `act_kinds` covering ordinary laws and decree-laws because the LPGE was
  prorogued) — cases 10 and 5 exercise it.
- ✅ **Curation**: `curation/ES.curation.yaml` created with this set. It flags `$SMI2`
  (deliberately frozen at 2018), the `xcc_es` family (regional dining fees) and the 198
  `$tco_t_*` implicit consumption-tax rates `national_team`. No `temporal_basis` section:
  every ES parameter is `in_force` (the IRPF *período impositivo* is the calendar year).
  Must be applied after every `ingest-params`.
- ✅ **Translation**: the ES corpus is translated (2 771 `en` chunks for 2 786 `es`), so the
  English query leg has something to hit — unlike NL today.
- ⚠️ **The general PIT scale cannot be a case**: the export's `$tin_rate1..7` hold `'n/a'`
  ("rates approved in July: applied retroactively"), so `ES:tin_cons_es:tin_schedule`
  assembles thresholds with no rates. The savings scale stands in for it.
- ⚠️ **The savings-scale group is one band short**: the groups block defines
  `tin_capinc_schedule` from `natrate1-4` / `lim1-3` although `$tin_capinc_natrate5` (0.15,
  2025) and `$tin_capinc_lim4` (300 000, 2023) exist in the same export. Case 8 expects the
  law's five bands and therefore routes `changed` — a finding about the group definition.
- ⚠️ **Effect date ≠ in-force date**: BOE's `fecha_vigencia` is legal entry into force
  (savings scale `[2024-12-22,)`, work credit `[2025-07-26,)`), while both apply "con
  efectos desde el 1 de enero de 2025". `expected_valid_from` is the effect date, stated in
  prose in the amendment trail at the end of each version.
- ⚠️ **No genuinely stale scalar in the 2025 export**: every corpus-verifiable 2025 value
  EUROMOD holds matches the law (the new 15 % band, the 0.13-point MEI, the 340 € credit,
  the 5 550 € minimum). The two `changed` routings in the set are an 8-cent rounding (case 5)
  and the stale group definition (case 8). A stale-scalar `changed` case is available by
  construction the moment the set is drafted for `--year 2026` against this export: LIRPF
  DA 61.ª's 2026 version (from 2026-02-20) raises the work credit to 590,89 €.
- ⚠️ **The Ley IMV citations carry a non-breaking space** (`Ley IMV Artículo 13`, bytes
  `c2a0`), the LIRPF and LGSS ones a plain space. `citation_matches` is one-way containment,
  so the selection file spells the IMV citation with the NBSP; a plain-space copy silently
  scores citation 0 % on that case. Check bytes, not eyes, when adding an IMV citation.
- ⚠️ **State share vs total**: LIRPF art. 63/66 state the state half of the PIT scales,
  art. 74/76 the regional half; EUROMOD's `*_natrate*` hold the state half and
  `*_ratrate*`/`*_totrate*` the sum. Art. 66.2 (residents abroad) carries the full 30 % —
  the near-miss citation. Every rate entry says which quantity it holds.

## The 12 cases

| # | Target | 2025 value | Difficulty | Expected routing | Source |
|---|--------|-----------|------------|------------------|--------|
| 1 | `$tin_perall_amt1` | 5 550 €/y | verbatim (EASY) | unchanged | LIRPF art. 57 |
| 2 | `$tin_capinc_natrate5` | 15 % (state half, new band) | verbatim (EASY-MEDIUM) | unchanged | LIRPF art. 66 |
| 3 | `$tscft_ee_rate4` | 0.13 points (MEI, worker) | verbatim + `unit_conversion` (MEDIUM) | unchanged | LGSS DT 43.ª |
| 4 | `$tin_capinc_ratrate5` | 30 % (= 15 + 15) | combine (MEDIUM-HARD) | unchanged | LIRPF art. 66 + art. 76 |
| 5 | `bsa00_es/$bsa00_amt` | **7 905,80** €/y (law) vs 7 905,72 (EUROMOD) | combine + `cross_instrument` (HARD) | changed | Ley IMV art. 13 (+ revalorisation, NOT ingested) |
| 6 | `$tscft_ee_rate5` | 0.15 % (= 0.92 % × 4.70/28.30) | derive + `cross_instrument` (HARD) | unchanged | LGSS art. 19 bis + DT 42.ª |
| 7 | `$tscag_ee_rate5` | `$tscft_ee_rate5` | derive | derived | LGSS art. 19 bis |
| 8 | group `ES:tin_cons_es:tin_capinc_schedule` | 5 bands 9,5 … 15 % | table | changed (group has 4) | LIRPF art. 66 |
| 9 | `$tin_wkintc_amt` | 340 €/y | verbatim + `budget_act_window` (HARD — not_found today) | unchanged | LIRPF DA 61.ª (version from 2025-07-26) |
| 10 | `$IPREM` | 600 €/m | IMPOSSIBLE today — not_found | unchanged | Ley 31/2022 DA 90.ª (NOT ingested, prorogued) |
| 11 | `$SMI2` | 735,90 (frozen 2018) vs 1 184 in the corpus | IMPOSSIBLE by design | national_team_source | none (RD 87/2025 is the trap) |
| 12 | `xcc_es/$xcc_amt` | 96 €/m | IMPOSSIBLE by design | national_team_source | none (regional calls) |

Rationale per tier:

1–3. **The happy path and two traps of increasing subtlety.** The personal minimum is one
ingested article, one literal amount, unchanged since 2015. The 15 % savings band is new for
2025 and EUROMOD already carries it — a correct pipeline re-confirms it with a citation
rather than inferring a change, and must return the *state* half (art. 66.1), not the 30 %
that sits in the same article's paragraph 2 or in the Country Report. The MEI worker share
is stated as `0,13 puntos porcentuales` inside a 2023-2050 year table: pick the row, read
points as a fraction.

4–5. **The combine rung.** The total savings rate is nowhere stated for residents: it is the
sum of the state scale (art. 66) and the regional scale (art. 76), both in the same act, so
`difficulty: combine` is set explicitly (the label drafter counts instruments, not
provisions). The IMV guaranteed income is fixed by reference — 100 % of the annual
non-contributory pension — and the euro amount lives in the revalorisation instrument, which
is not ingested: the coefficient is readable, the base is not, the FR `$PSS * 4` shape
without a `$`. EUROMOD's value is 8 cents below the law's (a monthly figure truncated then
annualised); on the IE 27 382/27 383 precedent the law's value is golden and the difference
goes to the economists team.

6–7. **The first scorable `derive` case in any country, and its `derived` sibling.** The
solidarity contribution is new for 2025; LGSS art. 19 bis gives the rule (split in the same
proportion as contingencias comunes), DT 42.ª the 2025 total for the first band (0,92 %),
and nothing states the worker's 0,15 %: it is `0.92 × 4.70 / 28.30`, rounded as the
Tesorería publishes it. The agricultural-regime copy is stored as `$tscft_ee_rate5` and pins
the `derived` short-circuit exactly as FR's `$csg_red_thres` does.

8. **The table.** The state savings scale, assembled from the export's own groups block —
which is one band short of the law. Expecting the law's five bands makes the case route
`changed` today and `unchanged` once the group definition is fixed, while continuing to
test every-bracket-right either way.

9–10. **The impossible tier, each marking a different capability gap.** The 340 € work
credit is verbatim in the corpus but in a provision *added in July 2025 with effect from
1 January*: at `as_of` 2025-06-01 no version is in force, so point-in-time retrieval — doing
exactly what it should — cannot see it. This is the `budget_act_window` hazard made
concrete; the flip is retrieval that admits a later-enacted version whose stated effect date
covers `as_of`. The IPREM is the LPGE-prorogation trap: fixed by Ley 31/2022 and unchanged
since because no budget law passed, referenced by the LGSS but stated by no ingested act —
today an honest `not_found`, and the metric for ingesting the budget law through the scout.

11–12. **The refusal cases.** `$SMI2` is the sharper of the two: RD 87/2025 art. 1 *is* in
the corpus and says 1 184 €/month, so a pipeline that ignores `source_type` will confidently
propose "correcting" a constant that is frozen at 735,90 on purpose. The school dining fee
has no national source at all (LT's `xcc_amt1` counterpart). Both are routed by the new
overlay; correct behaviour is `national_team_source`, never `not_found`, never a proposal.

## What this fixes in the existing sets' blind spots

FR: 42/47 `unchanged`, all verbatim, one table, no scorable `derive`. IE/LT: hand-curated
ladders, but their `derive` cases are all `$`-referenced (recognition only) or have their
stating act missing. ES adds: the first `derive` case whose arithmetic can actually be
checked against ingested text (case 6); a state-vs-total rate trap with the wrong answer in
the same article (2, 4); a retroactive provision that defeats point-in-time retrieval by
design (9); a refusal case where the corpus offers a confident wrong value (11); a
by-reference value whose base is outside the corpus (5); and a bracket-schedule case that
doubles as a group-definition check (8). Together with FR it is the second Romance-language
corpus, so the per-language KPI split gets a third data point with a translated corpus.
