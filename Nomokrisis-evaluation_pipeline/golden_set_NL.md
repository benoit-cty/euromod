# NL golden set — selection and build guide

The Netherlands' golden set: 15 parameters in increasing pipeline difficulty, from the second
Box 1 threshold (the happy path) up to cases the current pipeline cannot solve — a threshold
whose base is the minimum wage in an act that is not ingested, a cost-sharing norm whose
statutory formula the parser dropped, the minimum wage and the AOW premium rate themselves
(stated by instruments outside the corpus), a `$`-reference and a national-team assumption.
The machine-readable selection lives in [golden_sources/nl.json](golden_sources/nl.json);
this document is the rationale and the build procedure.

## Why NL is built the IE/LT/ES way

**The store has no OpenFisca corpus for the Netherlands** (`params.external_corpora` holds
only openfisca-france), so there is no corpus drafter: expected values in
`golden_sources/nl.json` are hand-curated from the fourteen ingested acts, every one located
in the corpus at `as_of` 2025-06-01 before being written down, and every drafted case stays
`verified: false` until a human confirms it (`nomokrisis-eval verify <id> --reviewer …` or
the UI's Golden set tab). The Country Report (`08 - EUROMOD Triangulator/country-reports/
Y16/NL_Y16.md`, *Main policy changes between 2024 and 2025*) was used to find where 2025
moved; it is context, never evidence — and for NL it is also the source of the set's
sharpest trap (the 35.82 % combined rate, see case 2).

Corpus status (see `Nomotheca-RAG/Netherlands_sources_analysis.md` §7): fourteen acts
ingested through `countries/nl/` from the KOOP BWB repository — Wet IB 2001
(`BWBR0011353`), Wet LB 1964, AWIR, Wet op de zorgtoeslag, Wet op de huurtoeslag, WKB, AKW,
Participatiewet, AOW, Wet kinderopvang, WW, Wfsv, Anw, Wazo — 2 865 Dutch chunks, all
embedded, **not translated**. BWB is bitemporal and the adapter samples one *toestand* per
policy date (1 January), so each article's validity is its true `inwerking` date but the
1 July indexation versions are not in the corpus. **Not ingested**: the Wet minimumloon
(`BWBR0002638`), the Zorgverzekeringswet, the annual *Regeling premiepercentages* and
*maximumdagloon* regelingen, the toeslagen AMvBs, and the VAT/excise acts.

## Build procedure

```bash
# 1. Materialize NL parameter records AND apply the curation overlay (order matters:
#    ingest-params replaces model_values rows, the overlay follows it)
cd ../Nomoscope-agentic-workflow/pipeline
uv run nomoscope-workflow ingest-params ../../extracted_parameters/enriched/NL.enriched.json
uv run nomoscope-workflow curate-params curation/NL.curation.yaml

# 2. Draft the 15 cases from golden_sources/nl.json (no LLM: the expected values are the
#    curated ones, the parameter under test comes from the params DB)
cd ../../Nomokrisis-evaluation_pipeline
uv run nomokrisis-eval build-curated-dataset --country NL --year 2025

# 3. Human-verify (the freeze gate)
uv run nomokrisis-eval verify <case-id> --reviewer ben

# 4. Run
uv run nomokrisis-eval run --as-of 2025-06-01 --model mock/extractor --country NL   # smoke
```

### Prerequisites and gaps (status at 2026-09-08)

- ✅ **Scout**: NL in `scout.COUNTRY_SOURCES` / `ID_HINTS` (domain `wetten.overheid.nl`,
  id pattern `BWBR\d{7}`, treaties excluded) — cases 12 and 13 exercise it.
- ✅ **Curation**: `curation/NL.curation.yaml` created with this set. It flags `$xcc_amt`
  (assumed weekly childcare cost) and the 296 per-COICOP `$tco_t_*` implicit consumption-tax
  rates `national_team`, curates the 23 rate parameters the export delivers as `/100` to
  `/1` (their values are percent literals, exactly like their `/1` siblings — the proposal
  prompt's percent normalisation and the critique's range check key on `/1`), records that
  every NL parameter is `in_force`, and records the tax-rate basis decision the sources
  analysis asked for: `$tin_br1` holds the statutory tax component (8,17 %), the premiums
  are modelled in `peoplesic_nl`, so no combined-rate constant exists to flag. Must be
  applied after every `ingest-params`.
- ❌ **Translation not run**: 108 `en` chunks in the whole NL corpus (61 of them the Country
  Report, 47 Wet IB 2001) against 2 865 `nl`. The English query leg of retrieval has
  nothing to hit; every NL case measures the native-language leg only until
  `nomotheca_ingest.cli translate run` is done over NL.
- ❌ **No `table` case**: all eleven NL `bracket_schedule` groups assemble with `rate=None`
  for 2025 (`NL:tin_nl:tin_b_schedule` comes out as one empty bracket) because the group
  loader does not read the percent literals the export stores the rates as. The scalar
  cases 1–4 stand in for the Box 1 schedule. Flip: teach `paramdb.load_group_record` the
  percent-literal spelling (or a fixed export), then add `NL:tin_nl:tin_b_schedule` against
  art. 2.10's table.
- ⚠️ **1 July versions are not in the corpus.** Exactly one NL article version starts on
  2025-07-01 across the corpus; AKW art. 12 and Participatiewet art. 21 run
  `[2025-01-01,2026-01-01)`. The semi-annual indexation of the WML, AKW, bijstandsnormen,
  AOW and Anw is therefore invisible to retrieval — hazard `mid_year_change` on cases
  6, 9, 10, 12. EUROMOD holds the 1 January value, so the cases are right as drafted; the
  gap is that a pipeline cannot *see* that the value changed mid-year (sources analysis
  §6.1: sampling every `datum_inwerkingtreding` is a one-line change at ~13× the bytes).
- ⚠️ **The parser drops formula elements.** Participatiewet art. 22a's kostendelersnorm
  formula `((40 % + A × 30 %) / A) × B` is a `<formule>` element in the BWB XML; the chunk
  reads "is de norm per kalendermaand voor de belanghebbende: Hierbij staat: • A voor …".
  Case 10 is the metric for this: it cannot pass until the NL parser renders formulas and
  `reparse NL --url-like BWBR0015703` replays the snapshot.
- ⚠️ **Scoring gap on derived ratios.** Case 8 expects EUROMOD's four-decimal 1.2143 for a
  quotient the law gives as two amounts (347,83 / 286,45 = 1.214278…); the 1e-6 relative
  tolerance rejects the exact quotient. Same shape as ES's solidarity contribution: derived
  values need a rounding-aware comparison, or the pipeline has to round to EUROMOD's
  precision. Recorded, not absorbed — the case scores 0 on the value leg until one of
  those exists.
- ⚠️ **No genuinely stale scalar in the 2025 export**: every corpus-verifiable 2025 value
  EUROMOD holds matches the law (the three-band schedule, 3.068 / 5.599 / 2.035 credits,
  the 2.470 zelfstandigenaftrek, 12,7 % MKB-vrijstelling, the 1.330.000 villa threshold,
  286,45 AKW, 1.922,07 Participatiewet, 2.511 / 703 / 936 / 3.389 / 7,10 % WKB). So the set
  has zero `changed` routings, on purpose. A `changed` case is available by construction the
  moment the set is drafted for `--year 2026` against this export: the corpus already holds
  the 2026 versions of Wet IB 2001 art. 2.10 and art. 8.11 (8,324 % / € 996 / € 11.965).
- ⚠️ **Label drafter and Dutch pinpoints.** `labels.instrument_of` only recognised
  `art`/`article` after the comma, so "WKB, artikel 1" and "WKB, artikel 2" counted as two
  instruments and every two-pinpoint NL case drafted `combine` + `cross_instrument`. Fixed
  with this set (`artikel`, `artículo` added, test in `tests/test_labels.py`); the
  explicit labels on cases 8–10 are still set in the selection so a reviewer sees why.
- ⚠️ **EUROMOD-side findings, for the economists team, not the ground truth:**
  - four `bsanet_nl` values carry a stray space inside the number
    (`$bsa_single_lone_nonret_amt`, `$bsa_loneparent_nonret_amt`,
    `$bsa_loneparent_lone_nonret_amt` = `'1345. 45#m'`; `$bsa_couple_noch_youth1_amt` =
    `'1293. 21#m'`) — unparseable by `normalise_value`; the law says € 1.345,45;
  - `$EI_maxpremwag` = 75 860 (2024: 71 624) where the maximum premieloon fixed by the
    annual regeling is 75 864 (71 628) — 290,67 × 261 = 75 864,87; the regeling is not
    ingested, so this is a check request, not a golden value;
  - 23 rate parameters are delivered `/100` and 17 siblings `/1` with identical percent-
    literal spelling (`$tin_br1` `/1` next to `$tin_br2` `/100` in one schedule);
  - `$tin_br1`'s enriched description says the band "combines income tax with national
    insurance contributions" while its value is the statutory tax component (8,17 %,
    9,32 % in 2024) — the value is right, the description is not.

## The 15 cases

| # | Target | 2025 value | Difficulty | Expected routing | Source |
|---|--------|-----------|------------|------------------|--------|
| 1 | `$tin_bandlim2` | 76 817 €/y | verbatim (EASY) | unchanged | Wet IB 2001 art. 2.10 (table) |
| 2 | `tin_nl/$tin_br1` | 8,17 % (tax only; CR says 35,82) | verbatim (EASY-MEDIUM) | unchanged | Wet IB 2001 art. 2.10 |
| 3 | `tin_nl/$tin_br3` | 49,50 % (since 2020) | verbatim (EASY, no-change trap) | unchanged | Wet IB 2001 art. 2.10 |
| 4 | `$tin_bandlim1a` | 40 502 €/y (born < 1946) | verbatim (MEDIUM, near-miss article) | unchanged | Wet IB 2001 art. 2.10a |
| 5 | `tin_nl/$impr_band5` | 1 330 000 € | verbatim (MEDIUM, table row) | unchanged | Wet IB 2001 art. 3.112 |
| 6 | `bfa_nl/$bfa_bchqtr_amt` | 286,45 €/q (law's "base" is 409,21) | verbatim + `mid_year_change` (MEDIUM) | unchanged | AKW art. 12(3)(a) |
| 7 | `constdef_nl/$PenAge` | 67 | verbatim (EASY-MEDIUM, year table) | unchanged | AOW art. 7a(1)(n) |
| 8 | `bfa_nl/$bfa_mult2` | 1.2143 (= 347,83 / 286,45) | derive (HARD) | unchanged | AKW art. 12(3) |
| 9 | `chall_nl/$chall_B2` | 37 545 €/y (= 1.08 × 12 × WML + 9 139) | combine + `cross_instrument` (HARD) | unchanged | WKB art. 2(8) + art. 1(1)(d) + WML (NOT ingested) |
| 10 | `bsanet_nl/$bsa_couple_nonret_amt` | 1 922,07 €/m | verbatim + `mid_year_change` (MEDIUM) | unchanged | Participatiewet art. 21(b) |
| 11 | `bsanet_nl/$bsa_single_nonret_amt` | 961,04 €/m (= 50 % × 1 922,07) | combine + `mid_year_change` (IMPOSSIBLE today — formula dropped) | unchanged | Participatiewet art. 21(b) + art. 22a |
| 12 | `constdef_nl/$MinWage_m` | 2 191,80 €/m | verbatim + `mid_year_change` (HARD — not_found today) | unchanged | WML art. 8(1)(b), `BWBR0002638` (NOT ingested) |
| 13 | `peoplesic_nl/$peoplesic_aow_rate` | 17,9 % (Wfsv states only "ten hoogste 18,25") | IMPOSSIBLE today — not_found | unchanged | Regeling premiepercentages (NOT ingested) |
| 14 | `tschl_nl/$tschl_uplim` | `$EI_Maxpremwag` | derive | derived | Wfsv art. 17 |
| 15 | `xcc_nl/$xcc_amt` | 400 €/w | IMPOSSIBLE by design | national_team_source | none (team assumption) |

Rationale per tier:

1–5. **The Box 1 schedule as scalars, and the CALS-table parser risk in the open.** The
Dutch tariff is a four-column table inside art. 2.10, rendered by the NL parser as
pipe-delimited rows; every `supporting_extract` on cases 1–4 has to be matched
character-for-character against `| € 38.441 | € 76.817 | € 3.140 | 37,48% |`. Case 2 is
the trap the sources analysis flagged before any parameter was mapped: the statute's 8,17 %
and the Country Report's 35,82 % are *both correct* on their own basis, and the export holds
the statutory one. Case 3 is the no-change trap inside a reform year; case 4 the derogating
article (born before 1946) whose table looks exactly like the general one; case 5 the
eigenwoningforfait's six-row WOZ table, where the value appears twice in the same row.

6–7. **Benefit amounts stated by the act itself.** Unlike the toeslagen (fixed by AMvB),
the AKW and AOW carry their amounts and tables in the consolidated text. Child benefit is
the "which one is the base" trap: AKW art. 12(1) calls the 12–17 amount the
*basiskinderbijslagbedrag*, EUROMOD calls the 0–5 amount its base and scales up. The
pension age is the LT step-schedule case with the derivation already done by the
legislature — pick the 2025 row from a fifteen-row table that carries two ages per row.

8–9. **The first scorable `derive` case in NL, and the cross-instrument combine.** AKW
art. 12(3) states three amounts; EUROMOD stores their ratio to four decimals, and nothing
in the law says "1.2143". The child-budget threshold for couples is fixed by two provisions
of the WKB (a € 9.139 uplift over the *drempelinkomen*, itself 108 % of twelve times the
WML's January monthly amount) plus one act that is not in the corpus — the coefficients are
readable, the base is not, the ES `bsa00_amt` shape. The same chain without the uplift is
28 406, which Wet IB 2001 art. 8.10 happens to state verbatim: the near-miss is *in* the
corpus.

10–11. **Bijstand, and an ingest finding made into a case.** The couple norm is verbatim
in Participatiewet art. 21(b) and carries the semi-annual-indexation hazard the corpus
cannot see. The single norm EUROMOD uses is the kostendelersnorm for two sharers, whose
formula art. 22a states as a `<formule>` element the parser does not render — so both
provisions are in the corpus and the case is still impossible until the parser changes.
That is exactly the kind of "one change that flips it" the ladder exists to name.

12–13. **The scout tier.** The minimum wage is the value the JRC asks about by name; the
WML is not ingested, and the corpus itself betrays the amount (28 406 / 12 / 1,08). The AOW
premium rate is sharper: Wfsv art. 11 *is* ingested and states a ceiling of 18,25 %, which
a retrieval-first pipeline will quote as the rate. Both are honest `not_found` today; one
`nomotheca_ingest.cli nl instrument BWBR0002638` flips case 12 (and gives case 9 its base),
ingesting the annual *Regeling premiepercentages* flips case 13.

14–15. **The routing traps.** `$tschl_uplim` is stored as `$EI_Maxpremwag` and pins the
`derived` short-circuit (Wfsv art. 17 gives the rule, the regeling the amount — where the
export's 75 860 looks four euros short). The childcare cost has no legal source at all;
the new overlay routes it `national_team_source`, and the plausible wrong answer — the
toeslag's maximum hourly price — is in the orbit of an ingested act.

## Smoke run (2026-09-08, `mock/extractor`, `--include-drafts --no-db`)

15 cases load and materialize from `data/parameters/eval/`; the `derived` and
`national_team_source` cases route correctly without an LLM (routing ✓ on both); `report`
splits 12 ready / 2 `no_corpus` / 1 `undocumented`; the 13 LLM-dependent cases return
`not_found` as the mock must; retrieval hit 64 % over the Dutch chunks with no English leg.
Difficulty slices in the report: verbatim 8, combine 2, derive 2 (ready cases only).

## What this fixes in the existing sets' blind spots

FR: 42/47 `unchanged`, all verbatim, one table. IE/LT/ES: hand-curated ladders with one
scorable `derive` (ES) and translated corpora (ES, IE native). NL adds: the first
untranslated Germanic corpus, so the per-language KPI split gets a native-only data point
and the translation gap becomes measurable rather than assumed; tables as the *primary*
carrier of fiscal values (CALS rows, not prose), which no other pilot country has; a
combined-vs-statutory rate trap where the wrong value comes from the Country Report itself
(2); a base-vs-multiplier trap where the law and the model disagree on which amount is
"basic" (6); a `derive` case whose stating act is ingested and whose quotient exposes the
tolerance rule (8); a cross-instrument combine whose near-miss is stated verbatim elsewhere
in the corpus (9); an ingest defect turned into a measurable case (11, the dropped formula);
and the semi-annual indexation hazard the sampling design cannot see (6, 10–12).
