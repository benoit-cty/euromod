# Matching `extracted_parameters/FR.policy.json` ↔ EUROMOD Country Report FR (Y16, 2022–2025)

Purpose: map the 702 machine-extracted FR parameters to the sections of `RAG/country_reports/Y16_CR_FR.pdf` (companion extraction: [Y16_CR_FR.md](Y16_CR_FR.md)), to decide **what the RAG must ingest** and **how to build the evaluation pipeline** (see `00_project-overview.md`, Activities 2 & 4).

---

## 1. Anatomy of `FR.policy.json`

Top level: a JSON **array of 702 parameter objects**, each `{information, values}`.

- `information.model_target` — URI of the form `euromod://FR/<policy_sheet>/def_const/$<ConstantName>` (e.g. `euromod://FR/SetDefault_fr/def_const/$MinWage`). **All 702 targets are `def_const`**: the extraction covers only *named constants* defined in DefConst functions of the FR model (EUROMOD master J2.19), not in-function scalar parameters.
- `information` also carries: `value_type` (always `scalar`), `unit`, `label.en` / `short_label` / `description` / `explanation.en` (EUROMOD function-group name), `last_confirmed_valid_on` (always null), and a `classification` block (`category` always `policy`, produced by a `haiku` classifier).
- `values[]` — a validity-dated time series: `value`, `valid_from`, `valid_to` (null = open-ended), plus empty provenance slots (`legal_status`, `source_type`, `official_journal_date`, `references`) and a `lineage` block (`proposed_by: pipeline`, `model: euromod-connector:EUROMOD_MASTER_VERSION_J2.19`, `model_answer` with the raw EUROMOD string, `review_status: pending`).

### 1.1 Value conventions (EUROMOD period suffixes)

`model_answer` strings carry a **period suffix** defining the time basis; the period can take on the following values:

| Suffix | Meaning | Conversion to monthly |
|---|---|---|
| `#m` | monthly | no conversion |
| `#y` | yearly | divided by 12 (more precisely multiplied by 0.0833333333333333) |
| `#q` | quarterly | divided by 3 (more precisely multiplied by 0.3333333333333333) |
| `#w` | weekly | multiplied by 4.34 (= 365/12/7) |
| `#d` | daily | multiplied by 30.5 |
| `#l` | labour day | multiplied by 21.73 |
| `#s` | labour day in a six-days week | multiplied by 26.07 |
| `#c` | capital | no conversion |

### 1.2 Value quirks the pipelines must handle

- **530 of 702 parameters have at least one formula-string value**, not a plain number. Two kinds:
  - **FYA (financial-year averaging) formulas** when legislation changes mid-year, e.g. `$MinWage` 2024 = `(1766.92*10+1801.80*2)/12#m` (SMIC raised in November). ⇒ *the EUROMOD stored value is a weighted average that never appears verbatim in any legal text* — an evaluation pipeline comparing "RAG-retrieved legal value" to "EUROMOD value" must reconstruct the averaging, not string-match.
  - **Cross-references to other constants**, e.g. `$csg_red_thres = $PSS * 4`, `$tsc_group2_lim = 3 × monthly PSS`. ⇒ parameters form a dependency graph, not a flat list.
- **Provenance is empty everywhere**: `references: []` on all 702 × all value rows, `review_status: pending`, classification confidence from a Haiku pass. ⇒ *filling `references` / `official_journal_date` with RAG-retrieved citations is exactly the value-add of the project, and `review_status` is the hook for the validation UI.*
- **Unit metadata is unreliable**: pure rates are stored with `unit: "currency"` (e.g. `$bho_Tf_rate1 = 0.0283`, CSG rates). Distribution: 544 `currency`, 74 `currency/month`, 68 `currency/year`, 8 `currency/day`, 3 `/1`, 5 null.
- **Labels are uneven**: some are real definitions, many are maintenance notes (e.g. 16 housing-benefit rent limits all labelled "FYA: annual increase takes place in July 2022 and October2023"), some empty. Sheet + constant name is often more informative than the label.
- **Cohort-split constants**: PAJE (`bchyc_fr`, 38 params) keeps three parallel parameter sets by child's birth date (before 04.2014 / 04.2014–03.2018 / after 04.2018); older cohorts' series end in 2018/2023 with latest value `n/a`.

### 1.3 Temporal coverage

| Statistic | Count |
|---|---|
| Parameters (all `def_const`, all scalar, all classified `policy`) | 702 |
| With a value row starting in 2025 | 183 |
| With a value row starting in 2024 | 186 |
| Last value row is open-ended (`valid_to: null`) | 471 |
| Series closed (`valid_to` set on last row — abolished or hard-dated) | 231 (of which all 229 `tco_fr` excises) |
| Last change before 2020 (stable constants or dormant/legacy) | 448 |

Only ~26 % of constants actually moved in 2025 — the yearly update workload is concentrated in the indexed instruments (housing benefit, PAJE/family benefits, RSA, Prime d'activité, income-tax thresholds, SMIC, PSS).

---

## 2. Sheet-by-sheet match to the Country Report

Columns: parameters in JSON / of which with a 2025 value; CR pages refer to Y16_CR_FR.pdf.

### 2.1 Benefits

| JSON policy sheet | Params | 2025 | Instrument | CR section (pages) |
|---|---|---|---|---|
| `bch00_fr` | 11 | 10 | Allocation familiale (AF), `bch00_s` | §2.5.1 (p27–31) |
| `bchyc_fr` | 38 | 16 | PAJE allocation de base, `bchyc_s` (cohort-split income limits) | §2.5.2.1 (p32–35) |
| `bchba_fr` | 2 | 1 | Prime de naissance (PAJE), `bchba_s` | §2.5.2.2 (p35–36) |
| `bchcc_fr` | 8 | 4 | PreParE, `bchcc_s` | §2.5.2.3 (p37–38) |
| `bched_fr` | 7 | 7 | Allocation de rentrée scolaire (ARS), `bched_s` | §2.5.3 (p39–40) |
| `bchor_fr` | 2 | 2 | Allocation de soutien familial (ASF), `bchor_s` | §2.5.4 (p40–41) |
| `bchlg_fr` | 9 | 9 | Complément familial (CF), `bchlg_s` | §2.5.5 (p42–43) |
| `bchlp_fr` | 7 | 0 | "Family minimum" amounts (lone-parent guarantee, ex-API) | no own CR section; feeds RSA §2.5.8 |
| `bdi_fr` | 7 | 3 | Allocation aux adultes handicapés (AAH), `bdi_s` | §2.5.6 (p44–46) |
| `bsa00_fr` | 20 | 15 | RSA, `bsa00_s` | §2.5.8 (p48–53) |
| `bsawk_fr` | 14 | 12 | Prime d'activité, `bsawk_s` | §2.5.9 (p54–57) |
| `bsaeccm_fr` | 2 | 0 | Covid exceptional solidarity aid (lump sums per TU/child) | §2.8 (extraordinary measures) |
| `bhoey_fr` | 20 | 0 | Chèque énergie, `bhoey_s` | §2.5.10 (p58–60) |
| `bsaoa_fr` | 2 | 2 | ASPA (minimum vieillesse), `bsaoa_s` | §2.5.11 (p60–61) |
| `bhotn_fr` | 43 | 29 | Housing benefits APL/AL, `bhotn_s` (R0, rent ceilings by zone, participation rates) | §2.5.12 (p61–69) |
| `bunmt_fr` | 6 | 0 | Allocation de solidarité spécifique (ASS), `bunmt_s` | §2.5.14 (p74–77) |
| `sickcomp_fr` | 18 | 18 | Sickness benefit qualifying periods/caps, `bhl` | §2.5.15.2 (p78–80) |
| `bmact_fr` | 2 | 0 | Maternity/paternity daily min/max, `bmact_s`/`bpact_s` | §2.5.15.3–5 (p80–83) |

### 2.2 Contributions & taxes

| JSON policy sheet | Params | 2025 | Instrument | CR section (pages) |
|---|---|---|---|---|
| `SetDefault_fr` | 2 | 2 | SMIC (monthly + hourly) | §1.1, used throughout |
| `ConstDef_fr` | 25 | 11 | Cross-cutting constants: `$PSS`, retirement ages, SIC bracket limits (`$tsc_group*`), **unemployment-insurance ARE `$UB_*`** (rates 40.4 %/57 %, floors, qualifying periods), ASS daily amount, **Covid wage compensation `$mc_*`**, overtime exemption limit | §2.6.1 (PSS), §2.5.13 ARE (p69–74), §2.8.1–2 Covid (p111–121) |
| `tscee_fr` | 16 | 0 | Employee SIC rates/ceilings, `tscee_s` | §2.6.1 (p84–86) |
| `tscer_fr` | 29 | 3 | Employer SIC incl. Réduction générale (Fillon), `tscer_s` | §2.6.2 (p86–91) |
| `tscse_fr` | 29 | 0 | Self-employed SIC, `tscse_s` | §2.6.3 (p92–94) |
| `tscxc_fr` | 8 | 0 | CSG rates, `tscxc_s` (RFR exemption thresholds sit in `tinty_fr` as `$tscxc_thres*`) | §2.6.4 (p94–96) |
| `tscdf_fr` | 1 | 0 | CRDS rate (0.5 %), `tscdf_s` | §2.6.5 (p97) |
| `tsckt_fr` | 4 | 0 | Social levies on capital income, `tsckt_s` | §2.6.6 (p97–98) |
| `tinty_fr` | 33 | 17 | Net-taxable-income parameters: 10 % deduction min/max, old-age/disabled allowances, pension deduction, CSG deductible shares, CSG RFR thresholds | §2.7.3–2.7.4 (p99–102) + §2.6.4 |
| `tinkt_fr` | 21 | 12 | Décote parameters + capital-income taxation (PFU) | §2.7.5 (p104–106), §2.7.4.6 (p102–104) |
| `tin_fr` | 5 | 0 | Contribution exceptionnelle sur les hauts revenus (CEHR) | §2.7.5 |
| `tintcot_fr` | 11 | 0 | Monetary tax credits/reductions (childcare cap, education deductions…) | §2.7.6 (p106–110) |
| `tintcee_fr` | 8 | 0 | Prime pour l'emploi (PPE) — **abolished 2016**, legacy | historical only |
| `xcc_fr` | 16 | 10 | Net childcare cost extension (hourly limits, 50 % credit) | §2.4 policy extensions (p25–26), §2.7.6 |
| `binps_fr` | 14 | 0 | 2023 purchasing-power bonus for public servants, `binps_s` | §2.8.4 (p122–123) |
| `tco_fr` | 229 | 0* | Consumption taxes: `$tco_v_*` VAT rates (13), `$tco_a_*` ad-valorem excises (17), `$tco_t_*` specific excises (198), COICOP-coded | §2.9 (p123–130) |
| `twl_fr` | 16 | 0 | Wealth tax brackets/rates (ISF) | §1.4 mention only (not simulated for 2022–25) |
| `trewl_fr` | 10 | 0 | Real-estate wealth tax (IFI) brackets | §1.4 mention only |
| `tpr_fr` | 7 | 0 | Property/housing tax rates & exemption thresholds (taxe d'habitation) | §1.4 mention only |

\* all 229 `tco_fr` series are hard-dated (`valid_to` set) rather than open-ended — a different maintenance convention from every other sheet.

### 2.3 In the CR but ABSENT from the JSON (extraction gaps)

These need either a second extraction pass (non-`def_const` parameters) or explicit exclusion from scope:

| Missing | CR section | Why it matters |
|---|---|---|
| **IRPP progressive schedule** (bracket thresholds + rates 11/30/41/45 %) | §2.7.5 (p104) | *The* headline yearly-updated parameter set; lives in a `SchedCalc`/in-function definition, not `def_const`. No `$tin` bracket constants exist (only wealth-tax `$twl_bracket*`). |
| **Quotient familial ceilings** (plafonnement) | §2.7.4.4 (p101) | Yearly-indexed, politically salient. |
| **BMAF** (base mensuelle des allocations familiales) | §2.5 intro | Most family-benefit amounts are legally defined as % of BMAF; the JSON stores only the resulting € amounts. A legislation-RAG will find BMAF percentages, not €. |
| Allocation veuvage (`bsuwd_s`) | §2.5.7 (p46–47) | No `bsuwd_fr` constants at all (the model has a `bsuwd_fr` policy switch, off in baseline — benefit taken from data). |
| **CDHR** — 2025 20 % minimum tax on high incomes (`tinto01_s`) | §2.7.5 | `tin_fr` covers only the CEHR (`$tinto_*`); the new 2025 CDHR (taper 250k–330k / 500k–660k) has no constants. |
| Unemployment insurance ARE — full parameter set | §2.5.13 | Only 7 `$UB_*` constants in `ConstDef_fr`; SJR rules, dégressivité, ceilings not present as constants. |
| Covid wage compensation details (`bwkmcee_s`, `bwkmcse_s`, `bseec_s`) | §2.8.1–2 | Only averaged `$mc_*` constants. |
| Indemnité inflation (`binxp_s`) | §2.8.3 | Absent. |
| Uprating factors (Annex 1) | p157–162 | Non-legislative (statistical indices); out of `def_const` scope but required by the update workflow. |

### 2.4 In the JSON but not (or barely) in the CR

- `twl_fr` / `trewl_fr` / `tpr_fr` (wealth & property taxes) — mentioned in CR §1.4 as *not simulated*; their constants are dormant (last values 2006–2018).
- `tintcee_fr` (PPE) — abolished instrument, historical series only.
- `bchlp_fr` family-minimum amounts — used inside RSA/ASF logic, no dedicated CR section.

---

## 3. Implications

### For RAG ingestion (Activity 2)

1. **The CR itself is a prime ingestion target**: it is the only document that links EUROMOD constant names ↔ French legal concepts ↔ values per year, with per-instrument "EUROMOD modelling" caveats. Chunk it by instrument section (§2.5.x / §2.6.x / §2.7.x), keeping tables intact.
2. **Legislation retrieval must be dependency- and period-aware**: values in law are often % of BMAF, % of PSS, or mid-year-dated (⇒ FYA averaging); a retrieved "legal value" rarely equals the stored EUROMOD value verbatim.
3. **Prioritise the ~186 parameters that actually change yearly** (housing, family, RSA/PA, tax thresholds, SMIC/PSS) — that is the recurring update workload; excises (`tco_fr`, 229 hard-dated series) are a distinct bulk-update problem with COICOP keys.
4. The empty `references[]` slots define the **output contract**: for each value row, the pipeline should propose `references` (legal citation ids), `official_journal_date`, `legal_status`, feeding `lineage.review_status` for the validation UI.

### For the evaluation pipeline (Activity 4)

1. **Ground truth**: the CR tables (2022–2025 values per instrument) are an authoritative, already-curated golden set — match them against `values[]` rows by `valid_from` year. The 2025 rows (183 params) are the natural held-out test year.
2. **Match metric must be value-equivalence, not string equality**: evaluate after (a) period-suffix normalisation (§1.1 table), (b) FYA-formula evaluation, (c) constant-reference resolution (`$PSS * 4`).
3. **Negative/abstention cases**: dormant sheets (`twl`, `tpr`, `tintcee`) and cohort-closed series (`bchyc` pre-2018 cohorts) test that the agent does *not* propose updates for dead parameters.
4. **Known-gap cases** (§2.3) test scope-detection: the agent should flag "parameter not in extraction" rather than hallucinate a target.
5. Unit/label noise (§1.2) means the eval should key on `model_target`, never on labels.
6. **The CR is not infallible ground truth**: the Y16 FR report contains at least one internal inconsistency (Table 2.3 SMIC/PSS uprating percentages vs. the narrative text — both recorded in [Y16_CR_FR.md](Y16_CR_FR.md) §1). Golden-set values should be cross-checked against a second source (legislation or admin publications) before being frozen.
7. **Not all "policy" constants are legislative**: e.g. `$bsa00_BTA_rate` (RSA 20 % non-take-up) is a behavioural calibration, and the `$mc_yse_*` Covid constants come from official *statistics*, not law. The eval taxonomy needs a provenance class (legislation / admin statistic / calibration) so the RAG is only scored on what legislation can actually answer.

---

## 4. Appendix — full parameter inventory by policy sheet

Generated from `FR.policy.json` (`jq`): constant, English label (truncated 80 chars), unit, number of value rows, first/last `valid_from` year, latest value.

### tco_fr (229 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tco_a_02111` | excise - specific - 02111 Ethyl alcohol (per 100 l of pure alcohol) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_02121` | excise - specific - 02121 Wine (per 100 l) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_02122` | excise - specific - 02122 Sparkling wine (per 100 l) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_02131` | excise - specific - 02131 Beer (per 100 L per Plato of finished product) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_02211` | excise - specific - 02211 Cigarettes (per 1000 pieces) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_02212` | excise - specific - 02212 Cigars (per 1000 pieces) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_02213` | excise - specific - 02213 Other tobacco (Fine cut, per kg) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_04511` | excise - specific - 04511 Electricty (per MWh) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_04521` | excise - specific - 04521 Natural Gas- Heating (per gigajoule) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_04522` | excise - specific - 04522 Liquefied hydrocarbons (per 1000 kg) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_04531` | excise - specific - 04531 Gas Oil- Heating (1000 L) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_04541` | excise - specific - 04541 Coal and Coke - Heating (per gigajoule, 1 GJ = 0.0316  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_07221` | specific excise - 07221 Car fuel (simple average) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_07221a` | excise - specific - 07221a Petrol-Leaded (1000 L) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_07221b` | excise - specific - 07221b Petrol-Unleaded <95 oct (1000 L) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_07221c` | excise - specific - 07221c Petrol-Unleaded (Unleaded substitute petrol) (1000 L) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_a_07221d` | excise - specific - 07221d Gas Oil- Propellant (1000 L) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_base_a_07221` | specific excise - 07221 Car fuel (simple average) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01111` | 01111 : 01 Food and nonalcoholic beverages  - 1 Food  - 1 Bread and cereals  - 1 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01112` | 01112 : 01 Food and nonalcoholic beverages  - 1 Food  - 1 Bread and cereals  - 2 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01113` | 01113 : 01 Food and nonalcoholic beverages  - 1 Food  - 1 Bread and cereals  - 3 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01114` | 01114 : 01 Food and nonalcoholic beverages  - 1 Food  - 1 Bread and cereals  - 4 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01115` | 01115 : 01 Food and nonalcoholic beverages  - 1 Food  - 1 Bread and cereals  - 5 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01116` | 01116 : 01 Food and nonalcoholic beverages  - 1 Food  - 1 Bread and cereals  - 6 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01121` | 01121 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 1 Fresh, chill | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01122` | 01122 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 2 Fresh, chill | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01123` | 01123 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 3 Fresh, chill | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01124` | 01124 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 4 Fresh, chill | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01125` | 01125 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 5 Dried, salte | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01126` | 01126 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 6 Other preser | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01127` | 01127 : 01 Food and nonalcoholic beverages  - 1 Food  - 2 Meat  - 7 Other fresh, | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01131` | 01131 : 01 Food and nonalcoholic beverages  - 1 Food  - 3 Fish  - 1 Fresh, chill | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01132` | 01132 : 01 Food and nonalcoholic beverages  - 1 Food  - 3 Fish  - 2 Fresh, chill | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01133` | 01133 : 01 Food and nonalcoholic beverages  - 1 Food  - 3 Fish  - 3 Dried, smoke | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01134` | 01134 : 01 Food and nonalcoholic beverages  - 1 Food  - 3 Fish  - 4 Other preser | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01141` | 01141 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01142` | 01142 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01143` | 01143 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01144` | 01144 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01145` | 01145 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01146` | 01146 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01147` | 01147 : 01 Food and nonalcoholic beverages  - 1 Food  - 4 Milk, cheese and eggs  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01151` | 01151 : 01 Food and nonalcoholic beverages  - 1 Food  - 5 Oils and fats  - 1 But | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01152` | 01152 : 01 Food and nonalcoholic beverages  - 1 Food  - 5 Oils and fats  - 2 Mar | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01153` | 01153 : 01 Food and nonalcoholic beverages  - 1 Food  - 5 Oils and fats  - 3 Oli | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01154` | 01154 : 01 Food and nonalcoholic beverages  - 1 Food  - 5 Oils and fats  - 4 Edi | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01155` | 01155 : 01 Food and nonalcoholic beverages  - 1 Food  - 5 Oils and fats  - 5 Oth | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01161` | 01161 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 1 Citrus frui | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01162` | 01162 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 2 Bananas (fr | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01163` | 01163 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 3 Apples (fre | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01164` | 01164 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 4 Pears (fres | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01165` | 01165 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 5 Stone fruit | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01166` | 01166 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 6 Berries (fr | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01167` | 01167 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 7 Other fresh | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01168` | 01168 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 8 Dried fruit | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01169` | 01169 : 01 Food and nonalcoholic beverages  - 1 Food  - 6 Fruit  - 9 Preserved f | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01171` | 01171 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 1 Leaf a | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01172` | 01172 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 2 Cabbag | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01173` | 01173 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 3 Vegeta | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01174` | 01174 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 4 Root c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01175` | 01175 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 5 Dried  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01176` | 01176 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 6 Other  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01177` | 01177 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 7 Potato | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01178` | 01178 : 01 Food and nonalcoholic beverages  - 1 Food  - 7 Vegetables  - 8 Other  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01181` | 01181 : 01 Food and nonalcoholic beverages  - 1 Food  - 8 Sugar, jam, honey, cho | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01182` | 01182 : 01 Food and nonalcoholic beverages  - 1 Food  - 8 Sugar, jam, honey, cho | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01183` | 01183 : 01 Food and nonalcoholic beverages  - 1 Food  - 8 Sugar, jam, honey, cho | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01184` | 01184 : 01 Food and nonalcoholic beverages  - 1 Food  - 8 Sugar, jam, honey, cho | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01185` | 01185 : 01 Food and nonalcoholic beverages  - 1 Food  - 8 Sugar, jam, honey, cho | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01186` | 01186 : 01 Food and nonalcoholic beverages  - 1 Food  - 8 Sugar, jam, honey, cho | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01191` | 01191 : 01 Food and nonalcoholic beverages  - 1 Food  - 9 Food products n.e.c.   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01192` | 01192 : 01 Food and nonalcoholic beverages  - 1 Food  - 9 Food products n.e.c.   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01193` | 01193 : 01 Food and nonalcoholic beverages  - 1 Food  - 9 Food products n.e.c.   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01194` | 01194 : 01 Food and nonalcoholic beverages  - 1 Food  - 9 Food products n.e.c.   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01211` | 01211 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 1 Cof | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01212` | 01212 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 1 Cof | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01213` | 01213 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 1 Cof | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01221` | 01221 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 2 Min | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01222` | 01222 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 2 Min | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01223` | 01223 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 2 Min | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_01224` | 01224 : 01 Food and nonalcoholic beverages  - 2 Non alcoholic beverages  - 2 Min | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02111` | 02111 : 02 Alcoholic beverages, tobacco and narcotics  - 1 Alcoholic  - 1 Spirit | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02121` | 02121 : 02 Alcoholic beverages, tobacco and narcotics  - 1 Alcoholic  - 2 Wine   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02122` | 02122 : 02 Alcoholic beverages, tobacco and narcotics  - 1 Alcoholic  - 2 Wine   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02131` | 02131 : 02 Alcoholic beverages, tobacco and narcotics  - 1 Alcoholic  - 3 Beer   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02211` | 02211 : 02 Alcoholic beverages, tobacco and narcotics  - 2 Tobacco  - 1 Tobacco  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02212` | 02212 : 02 Alcoholic beverages, tobacco and narcotics  - 2 Tobacco  - 1 Tobacco  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_02213` | 02213 : 02 Alcoholic beverages, tobacco and narcotics  - 2 Tobacco  - 1 Tobacco  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03111` | 03111 : 03 Clothing and footwear  - 1 Clothing  - 1 Clothing materials  - 1 Clot | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03121` | 03121 : 03 Clothing and footwear  - 1 Clothing  - 2 Garments  - 1 Garments for m | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03122` | 03122 : 03 Clothing and footwear  - 1 Clothing  - 2 Garments  - 2 Garments for w | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03123` | 03123 : 03 Clothing and footwear  - 1 Clothing  - 2 Garments  - 3 Garments for c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03131` | 03131 : 03 Clothing and footwear  - 1 Clothing  - 3 Other articles of clothing a | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03141` | 03141 : 03 Clothing and footwear  - 1 Clothing  - 4 Cleaning, repair and hire of | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03211` | 03211 : 03 Clothing and footwear  - 2 Footwear  - 1 Shoes and other footwear  -  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03212` | 03212 : 03 Clothing and footwear  - 2 Footwear  - 1 Shoes and other footwear  -  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03213` | 03213 : 03 Clothing and footwear  - 2 Footwear  - 1 Shoes and other footwear  -  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_03221` | 03221 : 03 Clothing and footwear  - 2 Footwear  - 2 Repair and hire of footwear  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04111` | 04111 : 04 Housing, water, electricity, gas and other fuels  - 1 Actual rentals  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04121` | 04121 : 04 Housing, water, electricity, gas and other fuels  - 1 Actual rentals  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04311` | 04311 : 04 Housing, water, electricity, gas and other fuels  - 3 Maintenance and | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04321` | 04321 : 04 Housing, water, electricity, gas and other fuels  - 3 Maintenance and | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04411` | 04411 : 04 Housing, water, electricity, gas and other fuels  - 4 Water supply an | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04421` | 04421 : 04 Housing, water, electricity, gas and other fuels  - 4 Water supply an | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04431` | 04431 : 04 Housing, water, electricity, gas and other fuels  - 4 Water supply an | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04441` | 04441 : 04 Housing, water, electricity, gas and other fuels  - 4 Water supply an | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04511` | 04511 : 04 Housing, water, electricity, gas and other fuels  - 5 Electricity, ga | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04521` | 04521 : 04 Housing, water, electricity, gas and other fuels  - 5 Electricity, ga | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04522` | 04522 : 04 Housing, water, electricity, gas and other fuels  - 5 Electricity, ga | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04531` | 04531 : 04 Housing, water, electricity, gas and other fuels  - 5 Electricity, ga | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04541` | 04541 : 04 Housing, water, electricity, gas and other fuels  - 5 Electricity, ga | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_04551` | 04551 : 04 Housing, water, electricity, gas and other fuels  - 5 Electricity, ga | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05111` | 05111 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05121` | 05121 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05131` | 05131 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05211` | 05211 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05311` | 05311 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05312` | 05312 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05313` | 05313 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05314` | 05314 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05315` | 05315 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05316` | 05316 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05317` | 05317 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05321` | 05321 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05331` | 05331 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05411` | 05411 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05412` | 05412 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05413` | 05413 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05414` | 05414 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05511` | 05511 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05521` | 05521 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05611` | 05611 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05612` | 05612 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05621` | 05621 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_05622` | 05622 : 05 Furnishings, household equipment and routine maintenance of the house | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06111` | 06111 : 06 Health  - 1 Medical products, appliances and equipment  - 1 Pharmaceu | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06121` | 06121 : 06 Health  - 1 Medical products, appliances and equipment  - 2 Other med | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06131` | 06131 : 06 Health  - 1 Medical products, appliances and equipment  - 3 Therapeut | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06211` | 06211 : 06 Health  - 2 Out-patient services  - 1 Medical Services  - 1 Medical S | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06221` | 06221 : 06 Health  - 2 Out-patient services  - 2 Dental services  - 1 Dental ser | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06231` | 06231 : 06 Health  - 2 Out-patient services  - 3 Paramedical services  - 1 Servi | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06232` | 06232 : 06 Health  - 2 Out-patient services  - 3 Paramedical services  - 2 Servi | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06233` | 06233 : 06 Health  - 2 Out-patient services  - 3 Paramedical services  - 3 Other | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_06311` | 063 : 06 Health  - 3 Hospital services  -    -  Hospital services | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07111` | 07111 : 07 Transport  - 1 Purchase of vehicles  - 1 Motor-cars  - 1 Purchase of  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07112` | 07112 : 07 Transport  - 1 Purchase of vehicles  - 1 Motor-cars  - 2 Purchase of  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07121` | 07121 : 07 Transport  - 1 Purchase of vehicles  - 2 Motor-cycles  - 1 Motor-cycl | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07131` | 07131 : 07 Transport  - 1 Purchase of vehicles  - 3 Bicycles  - 1 Bicycles | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07141` | 07141 : 07 Transport  - 1 Purchase of vehicles  - 4 Animal-drawn vehicles  - 1 A | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07211` | 07211 : 07 Transport  - 2 Operation of personal transport equipment  - 1 Spare p | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07221` | 07221 : 07 Transport  - 2 Operation of personal transport equipment  - 2 Fuels a | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07231` | 07231 : 07 Transport  - 2 Operation of personal transport equipment  - 3 Mainten | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07241` | 07241 : 07 Transport  - 2 Operation of personal transport equipment  - 4 Other s | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07311` | 07311 : 07 Transport  - 3 Transport services  - 1 Passenger transport by railway | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07321` | 07321 : 07 Transport  - 3 Transport services  - 2 Passenger transport by road  - | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07331` | 07331 : 07 Transport  - 3 Transport services  - 3 Passenger transport by air  -  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07341` | 07341 : 07 Transport  - 3 Transport services  - 4 Passenger transport by sea and | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07351` | 07351 : 07 Transport  - 3 Transport services  - 5 Combined passenger transport   | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_07361` | 07361 : 07 Transport  - 3 Transport services  - 6 Other purchased transport serv | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_08111` | 0811 : 08 Communication  - 1 Postal services  - 1 Postal services  -   Postal se | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_08211` | 08211 : 08 Communication  - 2 Telephone and telefax equipment  - 1 Telephone and | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_08311` | 08311 : 08 Communication  - 3 Telephone and telefax services  - 1 Telephone and  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09111` | 09111 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09112` | 09112 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09121` | 09121 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09122` | 09122 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09131` | 09131 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09141` | 09141 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09151` | 09151 : 09 Recreation and culture  - 1 Audio-visual, photographic and informatio | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09211` | 09211 : 09 Recreation and culture  - 2 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09221` | 09221 : 09 Recreation and culture  - 2 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09222` | 09222 : 09 Recreation and culture  - 2 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09231` | 09231 : 09 Recreation and culture  - 2 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09311` | 09311 : 09 Recreation and culture  - 3 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09321` | 09321 : 09 Recreation and culture  - 3 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09331` | 09331 : 09 Recreation and culture  - 3 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09341` | 09341 : 09 Recreation and culture  - 3 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09351` | 09351 : 09 Recreation and culture  - 3 Other major durables for recreation and c | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09411` | 09411 : 09 Recreation and culture  - 4 Recreational and cultural services  - 1 R | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09421` | 09421 : 09 Recreation and culture  - 4 Recreational and cultural services  - 2 C | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09422` | 09422 : 09 Recreation and culture  - 4 Recreational and cultural services  - 2 C | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09423` | 09423 : 09 Recreation and culture  - 4 Recreational and cultural services  - 2 C | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09424` | 09424 : 09 Recreation and culture  - 4 Recreational and cultural services  - 2 C | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09511` | 09511 : 09 Recreation and culture  - 5 Newspapers, books and stationery  - 1 Boo | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09521` | 09521 : 09 Recreation and culture  - 5 Newspapers, books and stationery  - 2 New | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09531` | 09531 : 09 Recreation and culture  - 5 Newspapers, books and stationery  - 3 Mis | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09541` | 09541 : 09 Recreation and culture  - 5 Newspapers, books and stationery  - 4 Sta | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_09611` | 096 : 09 Recreation and culture  - 6 Package holidays  -    -  Package holidays | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_10111` | 10111 : 10 Education  - 1 Pre primary and primary education  - 1 Pre primary and | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_10211` | 10211 : 10 Education  - 2 Secondary education  - 1 Secondary education  - 1 Seco | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_10311` | 10311 : 10 Education  - 3 Post-secondary non-tertiary education  - 1 Post-second | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_10411` | 10411 : 10 Education  - 4 Tertiary education  - 1 Tertiary education  - 1 Tertia | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_10511` | 10511 : 10 Education  - 5 Education not definable by level  - 1 Education not de | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_11111` | 11111 : 11 Restaurants and hotels  - 1 Catering services  - 1 Restaurants, cafés | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_11112` | 11112 : 11 Restaurants and hotels  - 1 Catering services  - 1 Restaurants, cafés | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_11121` | 11121 : 11 Restaurants and hotels  - 1 Catering services  - 2 Canteens  - 1 Cant | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_11211` | 11211 : 11 Restaurants and hotels  - 2 Accommodation services - 1 Accommodation  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12111` | 12111 : 12 Miscellaneous goods and services  - 1 Personal care  - 1 Hairdressing | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12121` | 12121 : 12 Miscellaneous goods and services  - 1 Personal care  - 2 Electrical a | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12131` | 12131 : 12 Miscellaneous goods and services  - 1 Personal care  - 3 Other applia | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12311` | 12311 : 12 Miscellaneous goods and services  - 3 Personal effects n.e.c.  - 1 Je | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12321` | 12321 : 12 Miscellaneous goods and services  - 3 Personal effects n.e.c.  - 2 Ot | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12322` | 12322 : 12 Miscellaneous goods and services  - 3 Personal effects n.e.c.  - 2 Ot | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12411` | 12411 : 12 Miscellaneous goods and services  - 4 Social protection  - 1 Social p | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12412` | 12412 : 12 Miscellaneous goods and services  - 4 Social protection  - 1 Social p | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12521` | 12521 : 12 Miscellaneous goods and services  - 5 Insurance  - 2 Insurance connec | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12531` | 12531 : 12 Miscellaneous goods and services  - 5 Insurance  - 3 Insurance connec | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12541` | 12541 : 12 Miscellaneous goods and services  - 5 Insurance  - 4 Insurance connec | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12551` | 12551 : 12 Miscellaneous goods and services  - 5 Insurance  - 5 Other insurance  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12621` | 12621 : 12 Miscellaneous goods and services  - 6 Financial services n.e.c.  - 2  | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_12711` | 12711: 12 Miscellaneous goods and services  - 7 Other services n.e.c.  - 1 Other | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_red1` | vat - reduced rate 1 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_red2` | vat - reduced rate 2 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_red3` | vat - reduced rate 3 | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_std` | vat - standard rate | currency | 2 | 2006 | 2011 | n/a |
| `$tco_t_zero` | vat - 0% rate and exempted | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02111` | excise - ad valorem - 02111 Ethyl alcohol | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02121` | excise - ad valorem - 02121 Wine | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02122` | excise - ad valorem - 02122 Sparkling wine | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02131` | excise - ad valorem - 02131 Beer | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02211` | excise - ad valorem - 02211 Cigarettes | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02212` | excise - ad valorem - 02212 Cigars | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_02213` | excise - ad valorem - 02213 Fine cut | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_04511` | excise - ad valorem - 04511 Electricty | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_04521` | excise - ad valorem - 04521 Natural Gas- Heating | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_04522` | excise - ad valorem - 04522 Liquefied hydrocarbons (butane, propane, etc.) | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_04531` | excise - ad valorem - 04531 Gas Oil- Heating | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_04541` | excise - ad valorem - 04541 Coal and Coke - Heating | currency | 2 | 2006 | 2011 | n/a |
| `$tco_v_07221` | excise - ad valorem - 07221 Petrol-Leaded | currency | 2 | 2006 | 2011 | n/a |

### bhotn_fr (43 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bho_P0_min` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 16 | 2006 | 2025 | (39.15*9+39.15*3)/12#m |
| `$bho_Tf_rate1` | Personal participation rate (Tf)-single person | currency | 2 | 2006 | 2008 | 0.0283 |
| `$bho_Tf_rate2` | Personal participation rate (Tf)-couple, no dependents | currency | 2 | 2006 | 2008 | 0.0315 |
| `$bho_Tf_rate3` | Personal participation rate (Tf)-couple/ lone parent, 1 dependent | currency | 2 | 2006 | 2008 | 0.027 |
| `$bho_Tf_rate4` | Personal participation rate (Tf)-couple/ lone parent, 2 dependents | currency | 2 | 2006 | 2008 | 0.0238 |
| `$bho_Tf_rate5` | Personal participation rate (Tf)-couple/ lone parent, 3 dependents | currency | 2 | 2006 | 2008 | 0.0201 |
| `$bho_Tf_rate6` | Personal participation rate (Tf)-couple/ lone parent, 4 dependents or more | currency | 2 | 2006 | 2008 | 0.0185 |
| `$bho_Tf_rate7` | Personal participation rate (Tf)-couple/ lone parent, 5 dependents or more | currency | 2 | 2006 | 2014 | 0.0179 |
| `$bho_Tf_rate8` | Personal participation rate (Tf)-for each dependent beyond the 5th | currency | 2 | 2006 | 2008 | -0.0006 |
| `$bho_chargeC_amt1` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (59.87*9+60.59*3)/12#m |
| `$bho_chargeC_amt2` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (73.57*9+74.33*3)/12#m |
| `$bho_chargeC_amt3` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (13.60*9+13.74*3)/12#m |
| `$bho_r0_amt1` | R0: Single person | currency/year | 17 | 2006 | 2025 | 5235 |
| `$bho_r0_amt2` | R0: Couple with no dependents- FYA: 2022 Weighted average | currency/year | 17 | 2006 | 2025 | 7501 |
| `$bho_r0_amt3` | R0: couple/ lone parent with 1 dependent- FYA: 2022 Weighted average | currency/year | 17 | 2006 | 2025 | 8947 |
| `$bho_r0_amt4` | R0: couple/ lone parent with 2 dependents-  FYA: 2022 Weighted average | currency/year | 17 | 2006 | 2025 | 9148 |
| `$bho_r0_amt5` | R0: increase for each dependent person after the 2nd -  FYA: 2022 Weighted avera | currency/year | 15 | 2006 | 2025 | 346 |
| `$bho_rentL_lim1` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (329.71*9+333.14*3)/12#m |
| `$bho_rentL_lim10` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (514.64*9+519.99*3)/12#m |
| `$bho_rentL_lim11` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (453.38*9+458.1*3)/12#m |
| `$bho_rentL_lim12` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (418.54*9+422.89*3)/12#m |
| `$bho_rentL_lim13` | FYA: annual increase takes place in July 2022 and October2023
 | currency/month | 17 | 2006 | 2025 | (65.21*9+65.89*3)/12#m |
| `$bho_rentL_lim14` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (57.61*9+58.21*3)/12#m |
| `$bho_rentL_lim15` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (52.47*9+53.01*3)/12#m |
| `$bho_rentL_lim2` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (287.35*9+290.34*3)/12#m |
| `$bho_rentL_lim3` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (269.32*9+272.12*3)/12#m |
| `$bho_rentL_lim4` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (397.64*9+401.78*3)/12#m |
| `$bho_rentL_lim5` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (351.72*9+355.38*3)/12#m |
| `$bho_rentL_lim6` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (326.48*9+329.88*3)/12#m |
| `$bho_rentL_lim7` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (449.43*9+454.1*3)/12#m |
| `$bho_rentL_lim8` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (395.77*9+399.89*3)/12#m |
| `$bho_rentL_lim9` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (366.07*9+369.88*3)/12#m |
| `$bho_rent_amt1` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (287.35*9+290.34*3)/12#m |
| `$bho_rent_amt2` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (351.72*9+355.38*3)/12#m |
| `$bho_rent_amt3` | Baseline rent: couple/ lone parent with 1 dependent | currency/month | 17 | 2006 | 2025 | (395.77*9+399.89*3)/12#m |
| `$bho_rent_amt4` | Baseline rent: couple/ lone parent with 2 dependents | currency/month | 17 | 2006 | 2025 | (453.38*9+458.1*3)/12#m |
| `$bho_rent_amt5` | FYA: annual increase takes place in July 2022 and October2023 | currency/month | 17 | 2006 | 2025 | (57.61*9+58.21*3)/12#m |
| `$bho_rl_minrate1` | Rate: min rate for 0-45 | currency | 1 | 2006 | 2006 | 0 |
| `$bho_rl_minrate2` | Rate: min rate for 45-75 | currency | 1 | 2006 | 2006 | 0.2025 |
| `$bho_rl_minrate3` | Rate: min rate for >75 | currency | 1 | 2006 | 2006 | 0.375 |
| `$bho_rl_rate1` | Rate: rate for 0-45 | currency | 1 | 2006 | 2006 | 0 |
| `$bho_rl_rate2` | Rate: rate for 45-75 | currency | 1 | 2006 | 2006 | 0.45 |
| `$bho_rl_rate3` | Rate: rate for >75 | currency | 1 | 2006 | 2006 | 0.68 |

### bchyc_fr (38 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bchlg_thres1` | Income test: minimum threshold to be considered an earner | currency/year | 18 | 2006 | 2025 | 5983 |
| `$bchyc_amt1` | 185.54 - child born between 1st of April 2014 and 31 March 2018 whose parents ea | currency/month | 8 | 2006 | 2023 | n/a |
| `$bchyc_amt2` | 172.09- child born after 1st of April 2018 whose parents earn income above the s | currency | 9 | 2006 | 2025 | 197.59 |
| `$bchyc_lim1` | Income limit for one earner couples with 1 child - for child born before 1st of  | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim10` | Children born in 2014 to 03.2018: Additional amount per child (income limit) sta | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim11` | Children born in 2014 to 03.2018:Income limit for one earner couple with 1 child | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim12` | Children born in 2014 to 03.2018:Income limit for one earner couple with 2 child | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim13` | Children born in 2014 to 03.2018:Income limit for one earner couple with 3 child | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim14` | Children born in 2014 to 03.2018:Additional amount per child (income limit) star | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim15` | Children born in 2014 to 03.2018: Income limit for two earner couples with 1 chi | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim16` | Children born in 2014 to 03.2018: Income limit for two earner couples with 2 chi | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim17` | Children born in 2014 to 03.2018: Income limit for two earner couples with 3 chi | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim18` | Children born in 2014 to 03.2018:Income limit for two earner couple with 1 child | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim19` | Children born in 2014 to 03.2018:Income limit for two earner couple with 2 child | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim1_2014` | Children born  2014 to 03.2018 (transitional reform): Income limit for one earne | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim2` | Income limit for one earner couples with 2 children - for child born before 1st  | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim20` | Children born in 2014 to 03.2018:Income limit for two earner couple with 3 child | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim21` | Children born after 04.2018 to ..: Income limit for one earner couple with 1 chi | currency | 9 | 2006 | 2025 | 36461 |
| `$bchyc_lim22` | Children born after 04.2018 to ..: Income limit for one earner couple with 2 chi | currency | 9 | 2006 | 2025 | 43753 |
| `$bchyc_lim23` | Children born after 04.2018 to ..: Income limit for one earner couple with 3 chi | currency | 9 | 2006 | 2025 | 52504 |
| `$bchyc_lim24` | Children born after 04.2018 to ..: Additional amount per child (income limit) st | currency | 9 | 2006 | 2025 | 8751 |
| `$bchyc_lim25` | Children born after 04.2018 to ..:  Income limit for one earner couple with 1 ch | currency | 9 | 2006 | 2025 | 30518 |
| `$bchyc_lim26` | Children born after 04.2018 to ..: Income limit for one earner couple with 2 chi | currency | 9 | 2006 | 2025 | 36621 |
| `$bchyc_lim27` | Children born after 04.2018 to ..:  Income limit for one earner couple with 3 ch | currency | 9 | 2006 | 2025 | 43946 |
| `$bchyc_lim28` | Children born after 04.2018 to ..:  Additional amount per child (income limit) s | currency | 9 | 2006 | 2025 | 7324 |
| `$bchyc_lim29` | Children born after 04.2018 to ..: Income limit for two earner couples with 1 ch | currency | 9 | 2006 | 2025 | 48186 |
| `$bchyc_lim3` | Income limit for one earner couples with 3 children  - for child born before 1st | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim30` | Children born after 04.2018 to ..: Income limit for two earner couples with 2 ch | currency | 9 | 2006 | 2025 | 55478 |
| `$bchyc_lim31` | Children born after 04.2018 to ..: Income limit for two earner couples with 3 ch | currency | 9 | 2006 | 2025 | 64229 |
| `$bchyc_lim32` | Children born after 04.2018 to ..:  Income limit for two earner couple with 1 ch | currency | 9 | 2006 | 2025 | 40330 |
| `$bchyc_lim33` | Children born after 04.2018 to ..:  Income limit for two earner couple with 2 ch | currency | 9 | 2006 | 2025 | 46434 |
| `$bchyc_lim34` | Children born after 04.2018 to ..:  Income limit for two earner couple with 3 ch | currency | 9 | 2006 | 2025 | 53758 |
| `$bchyc_lim4` | Additional amount (income limit) starting with the 4th child  - for child born b | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim5` | Income limit for two earner couples with 1 child  - for child born before 1st of | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim6` | Income limit for 2 earner couples with 2 children  - for child born before 1st o | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim7` | Income limit for 2 earner couples with 3 children  - for child born before 1st o | currency/year | 11 | 2006 | 2018 | n/a |
| `$bchyc_lim8` | Children born  2014 to 03.2018: Income limit for one earner couple with 2 childr | currency | 9 | 2006 | 2023 | n/a |
| `$bchyc_lim9` | Children born  2014 to 03.2018: Income limit for one earner couple with 3 childr | currency | 9 | 2006 | 2023 | n/a |

### tinty_fr (33 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$csg_red_thres` | CSG reduction threshold | currency | 1 | 2006 | 2006 | $PSS * 4 |
| `$csg_redrate` | CSG reduction rate | currency | 2 | 2006 | 2012 | 0.0175 |
| `$tintace_rate` | Tax deductions/ allowances for C1 incomes: Rate | currency | 1 | 2006 | 2006 | 0.1 |
| `$tintadb_amt1` | Tax allowance for disabled and old-age (higher amount) | currency/year | 18 | 2006 | 2025 | 2796 |
| `$tintadb_amt2` | Tax allowance for disabled and old-age (lower amount) | currency/year | 17 | 2006 | 2025 | 1398 |
| `$tintadb_lim1` | Income limit to qualify for disabled and old-age allowances (higher amount) | currency/year | 18 | 2006 | 2025 | 17510 |
| `$tintadb_lim2` | Income limit to qualify for disabled and old-age allowances (lower amount) | currency/year | 16 | 2006 | 2025 | 28170 |
| `$tintadp_amt` | Deduction for major children and dependent relatives | currency/year | 18 | 2006 | 2025 | 4039 |
| `$tintadt_dedyiy_amt1` | Deduction for investment income | currency/year | 2 | 2006 | 2012 | n/a |
| `$tintadt_dedyiy_amt2` | Deduction for investment income | currency/year | 2 | 2006 | 2012 | n/a |
| `$tintadt_dedyiy_rate` | Deduction for investment income | currency | 1 | 2006 | 2006 | 0.4 |
| `$tintapv_lowlim` | Minimum deduction for private pension contributions | currency/year | 18 | 2006 | 2025 | 4637 |
| `$tintapv_uplim` | Max deduction for private pension contributions | currency/year | 18 | 2006 | 2025 | 37094 |
| `$tinty_ded_maxamt` | Maximum deduction for earnings | currency/year | 19 | 2006 | 2025 | 14426 |
| `$tinty_ded_minamt` | Minimum deduction for earnings | currency/year | 16 | 2006 | 2025 | 504 |
| `$tinty_dedbun_lowlim` | Minimum deduction for unemployment benefits | currency/year | 12 | 2006 | 2019 | 0 |
| `$tinty_dedpens_maxamt` | Maximum deduction for pension income | currency/year | 18 | 2006 | 2025 | 4399 |
| `$tinty_dedpens_minamt` | Minimum deduction for pension income | currency/year | 16 | 2006 | 2025 | 450 |
| `$tinty_dedub_uplim` | Maximum deduction for unemployment benefit | currency/year | 13 | 2006 | 2019 | 0 |
| `$tinty_limmax` | Income limit for the deduction on property income | currency/year | 1 | 2006 | 2006 | 15000 |
| `$tscxc_thres1` | 1 share higher threshold for exemption | currency/year | 19 | 2006 | 2025 | 12818 |
| `$tscxc_thres2` | Each 0.5 share higher threshold for exemption | currency/year | 19 | 2006 | 2025 | 3422 |
| `$tscxc_thres3` | 1 share higher threshold for reduced rate | currency | 12 | 2006 | 2025 | 16755 |
| `$tscxc_thres4` | Each 0.5 share higher threshold for reduced rate | currency | 12 | 2006 | 2025 | 4474 |
| `$tscxc_thres5` | 1 share higher threshold for median rate | currency | 8 | 2006 | 2025 | 26004 |
| `$tscxc_thres6` | Each 0.5 share higher threshold for median rate | currency | 8 | 2006 | 2025 | 6941 |
| `$tscxcktrd_dedkt_rate` | Deductible CSG on capital income | currency | 3 | 2006 | 2018 | 0.068 |
| `$tscxcnkrd_dedbhl_rate` | Deductible CSG on sickness benefits | currency | 1 | 2006 | 2006 | 0.038 |
| `$tscxcnkrd_dedbun_rate` | Deductible CSG on unemployment benefits | currency | 1 | 2006 | 2006 | 0.038 |
| `$tscxcnkrd_dedpens_rate1` | Deductible CSG on pensions (reduced rate) | currency | 1 | 2006 | 2006 | 0.038 |
| `$tscxcnkrd_dedpens_rate2` | Deductible CSG on pensions (median rate) | currency | 2 | 2006 | 2019 | 0.042 |
| `$tscxcnkrd_dedpens_rate3` | Deductible CSG on pensions (normal rate) | currency | 2 | 2006 | 2018 | 0.059 |
| `$tscxcnkrd_dedyem_rate` | Deductible CSG on earnings | currency | 2 | 2006 | 2018 | 0.068 |

### tscer_fr (29 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tscer_red_coef1` | Reductions in employers’ social security contributions (Fillon reduction) | currency | 13 | 2006 | 2025 | 0.3193 |
| `$tscer_red_coef2` | Reductions in employers’ social security contributions (Fillon reduction) | currency | 12 | 2006 | 2025 | 0.3233 |
| `$tscerap_rate` | Apprenticeship tax rate | currency | 1 | 2006 | 2006 | 0.0068 |
| `$tscerfa_rate` | Employer family insurance contribution rate | currency | 2 | 2006 | 2014 | 0.0525 |
| `$tscerfa_rate2` | Employer family insurance contribution rate - Since 2015, for incomes  below 3.5 | currency | 2 | 2006 | 2015 | 0.0345 |
| `$tscerho_rate1` | Employer housing insurance contribution rate-companies with fewer than 50 employ | currency | 1 | 2006 | 2006 | 0.001 |
| `$tscerho_rate2` | Rate of housing insurance contributions for firms with over 50 employees (20 unt | currency | 1 | 2006 | 2006 | 0.005 |
| `$tscerir_rate1` | PArticipation in reconstruction effort rate | currency | 1 | 2006 | 2006 | 0.0045 |
| `$tscerir_rate2` | Professional training contribution (less than 10 employees) | currency | 2 | 2006 | 2008 | 0.0055 |
| `$tscerir_rate3` | Professional training contribution (10-20 employees) | currency | 3 | 2006 | 2016 | 0.01 |
| `$tscerir_rate4` | Professional training contribution (more than 20 employees) | currency | 3 | 2006 | 2016 | 0.01 |
| `$tscerot_rate` | Contingency insurance contribution rate for white colalr employees | currency | 1 | 2006 | 2006 | 0.015 |
| `$tscerpi_rate1` | Employer old-age insurance contributions-Income group A | currency | 5 | 2006 | 2016 | 0.0855 |
| `$tscerpi_rate10` | Outstanding contribution rate(CET) | currency | 2 | 2006 | 2019 | 0.0021 |
| `$tscerpi_rate2` | Employer old-age insurance contributions-whole income | currency | 5 | 2006 | 2024 | 0.0202 |
| `$tscerpi_rate3` | CSA contribution rate | currency | 2 | 2006 | 2011 | 0.003 |
| `$tscerpi_rate4` | Non white-collar complementary old-age insurance contribution rate-Income Group  | currency | 4 | 2006 | 2019 | 0.0472 |
| `$tscerpi_rate5` | Non white-collar complementary old-age insurance contribution rate-Income Group  | currency | 4 | 2006 | 2019 | 0.1295 |
| `$tscerpi_rate6` | White-collar complementary old-age insurance contribution rate-Income Group A | currency | 4 | 2006 | 2019 | 0.0472 |
| `$tscerpi_rate7` | White-collar complementary old-age insurance contribution rate-Income Group B/C | currency | 4 | 2006 | 2019 | 0.1295 |
| `$tscerpi_rate8` | AGFF contribution rate-all employees-income group 1/A | currency | 2 | 2006 | 2019 | 0.0129 |
| `$tscerpi_rate9` | AGFF contribution rate-all employees-income group 2/B | currency | 2 | 2006 | 2019 | 0.0162 |
| `$tscersi_rate` | Employer sickness insurance contributions rate (from 2019: income > 2.5 SMIC ) | currency | 4 | 2006 | 2018 | 0.13 |
| `$tscersi_rate2` | Employer sickness insurance contributions rate (from 2019: income < 2.5 SMIC ) | currency | 2 | 2006 | 2019 | 0.07 |
| `$tsceruf_rate` | Contribution for labour unions and professional organizations | currency | 2 | 2006 | 2015 | 0.00016 |
| `$tscerui_amt` | Unemployment insurance-lumps sum for white collar workers | currency/year | 6 | 2006 | 2011 | n/a |
| `$tscerui_rate1` | Unemployment insurance contribution rate | currency | 3 | 2006 | 2018 | 0.0405 |
| `$tscerui_rate2` | Unemployment insurance contribution rate-white collar supplement (APEC) | currency | 2 | 2006 | 2011 | 0.00036 |
| `$tscerwgf_rate` | Wage guarantee fund - Income group A and B | currency | 10 | 2006 | 2025 | 0.0025 |

### tscse_fr (29 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tscerfa_artisans_rate1` | Family contribution rate - artisans | currency | 3 | 2006 | 2018 | 0.031 |
| `$tscerfa_artisans_rate2` | Family contribution rate-artisans with low incomes | currency | 3 | 2006 | 2019 | 0 |
| `$tscerfa_rate3` | Family contribution rate-agricultural self-employment -lower rates (only used in | currency | 3 | 2006 | 2016 | n/a |
| `$tscsedi_artisans_rate` | Invalidity and death insurance contribution rate-Artisans | currency | 3 | 2006 | 2015 | 0.013 |
| `$tscsedi_farmers_rate` | Invalidity and death insurance contribution rate-Farmers | currency | 4 | 2006 | 2022 | 0.011 |
| `$tscsedi_industry_rate` | Invalidity and death insurance contribution rate-I&T | currency | 3 | 2006 | 2015 | 0.013 |
| `$tscsedi_minrate` | Invalidity and death insurance contribution rate - minimum rate on PSS | currency | 3 | 2006 | 2016 | 0.115 |
| `$tscseir_artisans_rate` | Professional training contribution rate-Artisans | currency | 4 | 2006 | 2018 | 0.0029 |
| `$tscseir_industry_rate` | Professional training contribution rate-I&T | currency | 2 | 2006 | 2013 | 0.0025 |
| `$tscsepi_farmers_rate3` | Complementary pension insurance contribution rate-farmers | currency | 3 | 2006 | 2018 | 0.04 |
| `$tscsepi_industry_rate8` | Complementary pension insurance contribution rate- I&T
 | currency | 2 | 2006 | 2013 | 0.07 |
| `$tscsepi_rate1` | Pension insurance contribution rates-farmers-Rate 1 | currency | 7 | 2006 | 2018 | 0.1487 |
| `$tscsepi_rate2` | Pension insurance contribution rates-farmers-Rate 2 | currency | 5 | 2006 | 2018 | 0.0224 |
| `$tscsepi_rate4` | Pension insurance contribution rate-I&T | currency | 6 | 2006 | 2017 | 0.1775 |
| `$tscsepi_rate5` | Second rate of pension insurance contributions-I&T | currency | 5 | 2006 | 2017 | 0.006 |
| `$tscsepi_rate6` | Complementary pension insurance contribution rate- Artisans | currency | 3 | 2006 | 2013 | 0.07 |
| `$tscsepi_rate7` | Second rate of complementary pension insurance contribution rates | currency | 3 | 2006 | 2013 | 0.08 |
| `$tscsepi_uplim` | Limit complementary pension insurance, from 2014 | currency | 6 | 2006 | 2020 | 38340 |
| `$tscsesi_rate1` | Sickness insurance rate for agricultural workers up to 2018, revived from 2023 | currency | 4 | 2006 | 2023 | 0 |
| `$tscsesi_rate10` | Supplementary sickness insurance contribution rate for artisans | currency | 2 | 2006 | 2018 | 0.0085 |
| `$tscsesi_rate11` | Sickness insurance contribution rate 2 for farmers from 2023 | currency | 2 | 2006 | 2023 | 0.04 |
| `$tscsesi_rate2` | Sickness insurance contribution upper rate for artisans + for farmers from 2019 | currency | 1 | 2006 | 2006 | 0.065 |
| `$tscsesi_rate3` | Second rate for sickness insurance contributions for artisans & I&T (only until  | currency | 2 | 2006 | 2013 | n/a |
| `$tscsesi_rate4` | Supplementary sickness insurance contribution rate for artisans & I&T | currency | 3 | 2006 | 2018 | 0.0085 |
| `$tscsesi_rate5` | Sickness insurance contribution rate for farmers  - second rate from 2019 | currency | 2 | 2006 | 2019 | 0.015 |
| `$tscsesi_rate6` | Sickness insurance contribution rate for artisans | currency | 4 | 2006 | 2021 | 0.0317 |
| `$tscsesi_rate7` | Sickness insurance contribution rate for artisans | currency | 2 | 2006 | 2018 | 0.0635 |
| `$tscsesi_rate8` | Sickness insurance contribution rate for artisans | currency | 2 | 2006 | 2018 | 0.072 |
| `$tscsesi_rate9` | Sickness insurance contribution rate for artisans | currency | 2 | 2006 | 2018 | 0.022 |

### ConstDef_fr (25 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$PSS` | PSS: Plafond Annuel de la Sécurité Sociale | currency/year | 18 | 2006 | 2025 | 47100 |
| `$RetAge_full` | Minimum age to receive a full state pension |  | 2 | 2006 | 2010 | 67 |
| `$RetAge_min` | Minimum age to receive a state pension |  | 3 | 2006 | 2025 | 62.5 |
| `$UB_QperMin` | Qualifying period: min no of months in work |  | 3 | 2006 | 2020 | 6 |
| `$UB_QperTot` | Qualifying period: over last months |  | 3 | 2006 | 2020 | 24 |
| `$UB_age53plus_QperTot` | Qualifying period for 53 year old or older |  | 2 | 2006 | 2009 | 36 |
| `$UB_dayfixamt` | Fixed daily amount- FYA (12.12+12.47)/2 | currency/day | 17 | 2006 | 2025 | 13.11 |
| `$UB_dayminamt` | Minimum daily amount- Value as of 30th of june | currency/day | 18 | 2006 | 2025 | 31.97 |
| `$UB_rate1` | % of previous salary for calculation of benefit amount, first option | /1 | 1 | 2006 | 2006 | 0.404 |
| `$UB_rate2` | % of previous salary for calculation of benefit amount, second option | /1 | 2 | 2006 | 2015 | 0.57 |
| `$UB_ratemax` | % of previous salary for calculation of maximum benefit amount | /1 | 1 | 2006 | 2006 | 0.75 |
| `$UB_red_thres` | Gross wage from which a reduction for high salaries from 7th month is applied- F | currency | 5 | 2006 | 2025 | 4915.33 |
| `$bunmt_amt` | ASS daily benefit amount: FYA  (17.21+17.9)/2 | currency/day | 17 | 2006 | 2025 | 19.33 |
| `$mc_yem_max` | Maximum wage compensation | currency | 3 | 2006 | 2023 | n/a |
| `$mc_yem_min` | Minimum wage compensation | currency | 3 | 2006 | 2023 | n/a |
| `$mc_yem_rrate` | FYA: replacement rate applied to the salary (weighted average values for each mo | currency | 5 | 2006 | 2023 | n/a |
| `$mc_yem_share` | FYA: share of the wage compensation paid by the state (weighted average of value | currency | 5 | 2006 | 2023 | n/a |
| `$mc_yse_amt` | Average amount of the self-employment compensation scheme (from official statist | currency | 4 | 2006 | 2023 | n/a |
| `$mc_yse_my` | Duration in months of the self-employment compensation scheme | currency | 4 | 2006 | 2023 | n/a |
| `$tinty_yemxp_lim` | Exemption Limit on Overtime Income in SIC and PIT | currency | 3 | 2006 | 2022 | 7500 |
| `$tsc_group1_lim` | Income limits for SIC purposes: 1*monthly PSS | currency/month | 17 | 2006 | 2025 | 3925 |
| `$tsc_group2_lim` | Income limits for SIC purposes: 3*monthly PSS | currency/month | 17 | 2006 | 2025 | 11775 |
| `$tsc_groupA_lim` | Income limits for SIC purposes: 1*monthly PSS | currency/month | 17 | 2006 | 2025 | 3925 |
| `$tsc_groupB_lim` | Income limits for SIC purposes: 4*monthly PSS | currency/month | 17 | 2006 | 2025 | 15700 |
| `$tsc_groupC_lim` | Income limits for SIC purposes: 8* montly PSS | currency/month | 17 | 2006 | 2025 | 31400 |

### tinkt_fr (21 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tin_decote_amt` | Base amount for the tax rebate (decote) | currency | 10 | 2006 | 2025 | 889 |
| `$tin_decote_amt2` | Base amount of decote for couples since 2015 | currency | 10 | 2006 | 2025 | 1470 |
| `$tin_decote_lim1` | Limit for the tax rebate (decote) to apply | currency/year | 17 | 2006 | 2025 | 1964 |
| `$tin_decote_lim2` | Higher threshold for decote for couples since 2015 | currency | 11 | 2006 | 2025 | 3248 |
| `$tin_decote_rate` | Rate for decote | currency | 3 | 2006 | 2020 | 0.4525 |
| `$tin_imaxdep_lim1` | Value of the first 2 half shares for dependents in QF | currency/year | 17 | 2006 | 2025 | 4224 |
| `$tin_imaxdep_lim2` | Value for the third share onwards for dependents in QF | currency/year | 18 | 2006 | 2025 | 1791 |
| `$tin_imaxdis_amt` | Complementary reduction for disabled for whom an imax correction applies | currency/year | 18 | 2006 | 2025 | 1785 |
| `$tin_imaxwd_amt` | Complementary reduction for widow/er with dependent child for whom an imax corre | currency/year | 18 | 2006 | 2025 | 1993 |
| `$tin_rate1` | Rate in band1 | currency | 1 | 2006 | 2006 | 0 |
| `$tin_rate2` | Rate in band 2 | currency | 2 | 2006 | 2015 | n/a |
| `$tin_rate3` | Rate in band 3 | currency | 2 | 2006 | 2020 | 0.11 |
| `$tin_rate4` | Rate in band 4 | currency | 1 | 2006 | 2006 | 0.3 |
| `$tin_rate5` | Rate in band 5 | currency | 2 | 2006 | 2010 | 0.41 |
| `$tin_rate6` | Rate in band 6 | currency | 2 | 2006 | 2012 | 0.45 |
| `$tin_upthres1` | Upper limit for band1 | currency/year | 16 | 2006 | 2025 | 11496 |
| `$tin_upthres2` | Upper limit for band 2 | currency/year | 7 | 2006 | 2015 | n/a |
| `$tin_upthres3` | Upper limit for band 3 | currency/year | 17 | 2006 | 2025 | 29314 |
| `$tin_upthres4` | Upper limit for band 4 | currency/year | 17 | 2006 | 2025 | 83822 |
| `$tin_upthres5` | Upper limit for band 5 | currency | 13 | 2006 | 2025 | 180293 |
| `$tinkt_rate` | Tax rate for capital income under PL (Prelevements liberatoires) | currency | 6 | 2006 | 2018 | 0.128 |

### bhoey_fr (20 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bhoey_amt1` |  | currency | 3 | 2006 | 2019 | 194 |
| `$bhoey_amt10` |  | currency | 2 | 2006 | 2019 | 48 |
| `$bhoey_amt11` |  | currency | 2 | 2006 | 2019 | 63 |
| `$bhoey_amt12` |  | currency | 2 | 2006 | 2019 | 76 |
| `$bhoey_amt13` | Exceptional additional energy bonus | currency | 3 | 2006 | 2023 | n/a |
| `$bhoey_amt14` | Exceptional additional energy bonus | currency | 3 | 2006 | 2023 | n/a |
| `$bhoey_amt2` |  | currency | 3 | 2006 | 2019 | 240 |
| `$bhoey_amt3
` |  | currency | 3 | 2006 | 2019 | 277 |
| `$bhoey_amt4` |  | currency | 3 | 2006 | 2019 | 146 |
| `$bhoey_amt5` |  | currency | 3 | 2006 | 2019 | 176 |
| `$bhoey_amt6` |  | currency | 3 | 2006 | 2019 | 202 |
| `$bhoey_amt7` |  | currency | 3 | 2006 | 2019 | 98 |
| `$bhoey_amt8` |  | currency | 3 | 2006 | 2019 | 113 |
| `$bhoey_amt9` |  | currency | 3 | 2006 | 2019 | 126 |
| `$bhoey_lim1` |  | currency | 3 | 2006 | 2023 | 5700 |
| `$bhoey_lim2` |  | currency | 3 | 2006 | 2023 | 6800 |
| `$bhoey_lim3
` |  | currency | 3 | 2006 | 2023 | 7850 |
| `$bhoey_lim4
` |  | currency | 4 | 2006 | 2023 | 11000 |
| `$bhoey_lim5
` |  | currency | 3 | 2006 | 2023 | n/a |
| `$bhoey_rfr_maxthres` | Maximum RFR threshold at which the access to Energy voucher is granted. | currency | 6 | 2006 | 2023 | 11000 |

### bsa00_fr (20 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bsa00_amt1` | Maximum amount for single person without children- FYA (weighted average) | currency/month | 20 | 2006 | 2025 | 646.52 |
| `$bsa00_amt10` | Extra amount for each child beyond the 2nd, for lone parents with 3+ children, a | currency/month | 20 | 2006 | 2025 | 276.73 |
| `$bsa00_amt2` | Maximum amount for lone parent with 1 dependent child (Age>3)- FYA | currency/month | 20 | 2006 | 2025 | 969.78 |
| `$bsa00_amt3` | Maximum amount for lone parent with 2 dependent children (aged>3)- FYA | currency/month | 20 | 2006 | 2025 | 1163.74 |
| `$bsa00_amt4` | Extra amount for each child beyond the 2nd (Aged>3)- FYA | currency/month | 20 | 2006 | 2025 | 258.61 |
| `$bsa00_amt5` | Maximum amount for couple with no dependent children- FYA | currency/month | 20 | 2006 | 2025 | 969.78 |
| `$bsa00_amt6` | Maximum amount for couple with 1 dependent child - FYA | currency/month | 20 | 2006 | 2025 | 1163.74 |
| `$bsa00_amt7` | Maximum amount for couple with 2 dependent children- FYA | currency/month | 20 | 2006 | 2025 | 1357.7 |
| `$bsa00_amt8` | Maximum amount for lone parent with 1 child<3- FYA | currency/month | 20 | 2006 | 2025 | 1163.74 |
| `$bsa00_amt9` | Maximum amount for lone parent with 2 children, one aged<3 //API before 2009: ac | currency/month | 20 | 2006 | 2025 | 1383.68 |
| `$bsa00_bonus_amt1` | End of year bonus: single person | currency | 2 | 2006 | 2012 | 152.45 |
| `$bsa00_bonus_amt2` | End of year bonus: lone parent with 1 dependent child & couple with no children | currency | 2 | 2006 | 2012 | 228.67 |
| `$bsa00_bonus_amt3` | End of year bonus: lone parent with 2 dependent children & couple with 2 depende | currency | 2 | 2006 | 2012 | 274.41 |
| `$bsa00_bonus_amt4` | End of year bonus: Additional amount for each child after the 2nd | currency | 2 | 2006 | 2012 | 60.98 |
| `$bsa00_bonus_amt5` | End of year bonus: couple with 2 plus children | currency | 2 | 2006 | 2012 | 320.14 |
| `$bsa00_hp_amt1` | Applicable housing package to be deducted: single person - FYA | currency/month | 20 | 2006 | 2025 | 77.58 |
| `$bsa00_hp_amt2` | Applicable housing package to be decuted: lone parent with 1 child- FYA | currency/month | 20 | 2006 | 2025 | 155.16 |
| `$bsa00_hp_amt3` | Applicable housing package to be deducted: lone parent with 2+ children-FYA | currency/month | 20 | 2006 | 2025 | 192.02 |
| `$bsa00_hp_amt4` | Applicable housing package to be deducted: couple with no children- FYA | currency/month | 20 | 2006 | 2025 | 155.16 |
| `$bsa00_hp_amt5` | Applicable housing package to be deducted: couple with 1 or more children- FYA | currency/month | 20 | 2006 | 2025 | 192.02 |

### sickcomp_fr (18 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bhl_Qper12` | qualifying period for bhl: over last 12 months | currency | 1 | 2025 | 2025 | 4 |
| `$bhl_Qper12_se` | qualifying period for bhl - self employed: over last 12 months | currency | 1 | 2025 | 2025 | 12 |
| `$bhl_Qper3` | qualifying period for bhl: over last 3 months | currency | 1 | 2025 | 2025 | 1 |
| `$bhl_day_thres` | max. days covered in total | currency | 1 | 2025 | 2025 | 365 |
| `$bhl_day_thres_ee1` | max. days covered by employer 1 | currency | 1 | 2025 | 2025 | 30 |
| `$bhl_day_thres_ee2` | max. days covered by employer 2 | currency | 1 | 2025 | 2025 | 30 |
| `$bhl_day_thres_pf` | max. days covered in total - professionals | currency | 1 | 2025 | 2025 | 87 |
| `$bhl_day_wait1` | waiting period for social security | currency | 1 | 2025 | 2025 | 3 |
| `$bhl_day_wait2` | waiting period for employer part | currency | 1 | 2025 | 2025 | 7 |
| `$bhl_max_amt1` | maximum ceiling - employees | currency/day | 1 | 2025 | 2025 | 41.47 |
| `$bhl_max_amt2` | maximum ceiling - farmer | currency/day | 1 | 2025 | 2025 | 64.52 |
| `$bhl_max_amt3` | maximum ceiling - professionals | currency/day | 1 | 2025 | 2025 | 193.56 |
| `$bhl_std_rate1` | replacement rate social security for employees | currency | 1 | 2025 | 2025 | 0.5 |
| `$bhl_std_rate2a` | replacement rate employer 1  | currency | 1 | 2025 | 2025 | 0.9 |
| `$bhl_std_rate2b` | replacement rate employer 2 | currency | 1 | 2025 | 2025 | 2/3 |
| `$bhl_std_rate3` | replacement rate farmers, day 1-28 | currency/day | 1 | 2025 | 2025 | 25.79 |
| `$bhl_std_rate4` | replacement rate farmers, day 29+ | currency/day | 1 | 2025 | 2025 | 34.38 |
| `$bhl_std_rate5` | replacement rate professionals | currency | 1 | 2025 | 2025 | 12*3/730 |

### tscee_fr (16 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tscee_yemxp_rate` | Maximum rate sc for overtime (since 2019) | currency | 2 | 2006 | 2019 | 0.1131 |
| `$tsceepi_rate1` | Rate for employee old-age insurance contributions (Income group A+ whole income) | currency | 6 | 2006 | 2017 | 0.073 |
| `$tsceepi_rate10` | AGFF-rate for non white collar employees on second portion of income | currency | 2 | 2006 | 2019 | 0.0108 |
| `$tsceepi_rate11` | AGFF-rate for white collar employees on second portion of income | currency | 2 | 2006 | 2019 | 0.0108 |
| `$tsceepi_rate2` | Rate for employee old-age insurance contributions (whole income) | currency | 5 | 2006 | 2017 | 0.004 |
| `$tsceepi_rate3` | Rate for non white-collar old-age insurance contributions (income group 1) | currency | 4 | 2006 | 2019 | 0.0315 |
| `$tsceepi_rate4` | Rate for non white-collar old-age insurance contributions (income group 2)
 | currency | 4 | 2006 | 2019 | 0.0864 |
| `$tsceepi_rate5` | Rate for white collar old-age complementary insurance (Inc Group A) | currency | 4 | 2006 | 2019 | 0.0315 |
| `$tsceepi_rate6` | Rate for while collar old-age complementary insurance (Inc Group B) | currency | 4 | 2006 | 2019 | 0.0864 |
| `$tsceepi_rate7` | Rate for while collar old-age complementary insurance (Inc Group C) | currency | 4 | 2006 | 2019 | 0.0864 |
| `$tsceepi_rate8` | Rate for outstanding pension contribution (CET) | currency | 2 | 2006 | 2019 | 0.0014 |
| `$tsceepi_rate9` | AGFF-Rate for all employees on first portion of income | currency | 2 | 2006 | 2019 | 0.0086 |
| `$tsceesi_rate` | Rate for employee sickness insurance contributions | currency | 2 | 2006 | 2018 | 0 |
| `$tsceeui_amt` | Unemployment insurance-Extra amount for white collar employees | currency/year | 6 | 2006 | 2011 | n/a |
| `$tsceeui_rate1` | Rate for employee unemployment insurance contribution | currency | 4 | 2006 | 2019 | 0 |
| `$tsceeui_rate2` | Rate for employee unemployment -white collar supplementinsurance contribution | currency | 2 | 2006 | 2012 | 0.00024 |

### twl_fr (16 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$twl_bracket1` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_bracket2` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_bracket3` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_bracket4` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_bracket5` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_bracket6` |  | currency | 1 | 2006 | 2006 | n/a |
| `$twl_credit` |  | currency | 1 | 2006 | 2006 | n/a |
| `$twl_rate1` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_rate2` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_rate3` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_rate4` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_rate5` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_rate6` |  | currency | 1 | 2006 | 2006 | n/a |
| `$twl_smoothing_amount` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_smoothing_rate` |  | currency | 3 | 2006 | 2018 | n/a |
| `$twl_threshold` |  | currency | 3 | 2006 | 2018 | n/a |

### xcc_fr (16 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tintcch_rate` | tax credit equal to 50% of childcares expenses, within an annual cap | currency | 1 | 2024 | 2024 | 50% |
| `$xcc_lowlim1` | Low Lim Hourly rate: 1 child  | currency | 2 | 2024 | 2025 | 0.5 |
| `$xcc_lowlim2` | Low Lim Hourly rate: 2 children | currency | 2 | 2024 | 2025 | 0.41 |
| `$xcc_lowlim3` | Low Lim Hourly rate: 3 children | currency | 2 | 2024 | 2025 | 0.33 |
| `$xcc_lowlim4` | Low Lim Hourly rate: 4-7 children | currency | 2 | 2024 | 2025 | 0.25 |
| `$xcc_lowlim5` | Low Lim Hourly rate: more than 8 children | currency | 2 | 2024 | 2025 | 0.17 |
| `$xcc_rate1` | Family contribution rate per billed hour in child care: 1 child | currency | 1 | 2024 | 2024 | 0.0619% |
| `$xcc_rate2` | Family contribution rate per billed hour in child care: 2 children | currency | 1 | 2024 | 2024 | 0.0516% |
| `$xcc_rate3` | Family contribution rate per billed hour in child care: 3 children | currency | 1 | 2024 | 2024 | 0.0413% |
| `$xcc_rate4` | Family contribution rate per billed hour in child care: 4-7 children | currency | 1 | 2024 | 2024 | 0.0310% |
| `$xcc_rate5` | Family contribution rate per billed hour in child care: more than 8 children | currency | 1 | 2024 | 2024 | 0.0206% |
| `$xcc_uplim1` | Up Lim Hourly rate: 1 child | currency | 2 | 2024 | 2025 | 4.33 |
| `$xcc_uplim2` | Up Lim Hourly rate: 2 children | currency | 2 | 2024 | 2025 | 3.61 |
| `$xcc_uplim3` | Up Lim Hourly rate: 3 children | currency | 2 | 2024 | 2025 | 2.89 |
| `$xcc_uplim4` | Up Lim Hourly rate: 4-7 children | currency | 2 | 2024 | 2025 | 2.17 |
| `$xcc_uplim5` | Up Lim Hourly rate: more than 8 children | currency | 2 | 2024 | 2025 | 1.44 |

### binps_fr (14 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$binps_amt1` | Annual amount for gross income≤ 23700€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_amt2` | Annual amount for 23700<gross income≤ 27300€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_amt3` | Annual amount for 27300<gross income≤ 29160€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_amt4` | Annual amount for 29160<gross income≤ 30840€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_amt5` | Annual amount for30840<gross income≤ 32280€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_amt6` | Annual amount for32280<gross income≤ 33600€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_amt7` | Annual amount for33600<gross income≤ 39000€ per year | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim1` | Maximum income threshold to receive binps_amt1 | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim2` | Maximum income threshold to receive binps_amt2 | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim3` | Maximum income threshold to receive binps_amt3 | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim4` | Maximum income threshold to receive binps_amt4 | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim5` | Maximum income threshold to receive binps_amt5 | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim6` | Maximum income threshold to bonus binps_amt6 | currency | 3 | 2006 | 2024 | n/a |
| `$binps_lim7` | Maximum income threshold to receive binps_amt7 | currency | 3 | 2006 | 2024 | n/a |

### bsawk_fr (14 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bsawk_bonus_rate` | Rate for calculation of maximum amount of individual bonus | currency | 3 | 2006 | 2019 | 0.29101 |
| `$bsawk_hp_amt1` | Applicable housing package to be deducted: single person-  FYA | currency | 11 | 2006 | 2025 | 75.99 |
| `$bsawk_hp_amt2` | Applicable housing package to be decuted: lone parent with 1 child  - FYA | currency | 11 | 2006 | 2025 | 151.97 |
| `$bsawk_hp_amt3` | Applicable housing package to be deducted: lone parent with 2+ children  - FYA | currency | 11 | 2006 | 2025 | 188.06 |
| `$bsawk_hp_amt4` | Applicable housing package to be deducted: couple with no children - FYA | currency | 11 | 2006 | 2025 | 151.97 |
| `$bsawk_hp_amt5` | Applicable housing package to be deducted: couple with 1 or more children- FYA | currency | 11 | 2006 | 2025 | 188.06 |
| `$bsawk_income_rate` | Rate of family income taken into account in step 1 for calculation benefit amoun | currency | 3 | 2006 | 2019 | 0.61 |
| `$bsawk_minamt` | Maximum minimum income (montant forfaitaire)- Single Without children- FYA (Weig | currency | 11 | 2006 | 2025 | 633.21 |
| `$bsawk_minamt1` | Maximum minimum income (montant forfaitaire)- Single with 1 child - FYA (Weighte | currency | 11 | 2006 | 2025 | 949.82 |
| `$bsawk_minamt2` | Maximum minimum income (montant forfaitaire)- Single 2 children- FYA (Weighted A | currency | 11 | 2006 | 2025 | 1139.78 |
| `$bsawk_minamt3` | Extra amount for each child beyond the 2nd - FYA (Weighted Average) | currency | 11 | 2006 | 2025 | 253.28 |
| `$bsawk_minamt4` | Maximum minimum income (montant forfaitaire)- Couple Without children- FYA (Weig | currency | 11 | 2006 | 2025 | 949.82 |
| `$bsawk_minamt5` | Maximum minimum income (montant forfaitaire)- Couple with 1 child- FYA (Weighted | currency | 11 | 2006 | 2025 | 1139.78 |
| `$bsawk_minamt6` | Maximum minimum income (montant forfaitaire)- Couple with 2 children- FYA (Weigh | currency | 11 | 2006 | 2025 | 1329.74 |

### bch00_fr (11 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bch00_age11to16_amt` | Additional amount for children aged 11-16 | currency/month | 6 | 2006 | 2012 | n/a |
| `$bch00_age14plus_amt` | Additional base amount if child is over 14 (full rate)-FYA | currency/month | 18 | 2006 | 2025 | 75.91 |
| `$bch00_child2_amt` | Base amount for families with 2 children (full rate)- FYA | currency/month | 18 | 2006 | 2025 | 151.81 |
| `$bch00_child2_thres1` | Income threshold to receive full rate for families with 2 children | currency | 10 | 2006 | 2025 | 78565 |
| `$bch00_child2_thres2` | Income threshold to receive half rate for families with 2 children | currency | 10 | 2006 | 2025 | 104719 |
| `$bch00_child3_amt` | Base amount for families with 3 children (full rate)- FYA | currency/month | 18 | 2006 | 2025 | 346.29 |
| `$bch00_child3_thres1` | Income threshold to receive full rate for families with 3 children | currency | 10 | 2006 | 2025 | 85111 |
| `$bch00_child3_thres2` | Income threshold to receive half rate for families with 3 children | currency | 10 | 2006 | 2025 | 111265 |
| `$bch00_child3age20_amt` | Additional base amount per each 20 year old child for families with 3 or more ch | currency | 17 | 2006 | 2025 | 95.99 |
| `$bch00_child3plus_amt` | Additional base amount per child for families with more than 3 children (full ra | currency/month | 18 | 2006 | 2025 | 194.49 |
| `$bch00_child3plus_thres` | Increase in income thresholds for each additional child after the third one | currency | 10 | 2006 | 2025 | 6546 |

### tintcot_fr (11 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tintcch_amt` | Maximum tax credit for child care expenses | currency/year | 2 | 2006 | 2023 | 3500 |
| `$tintced_amt1` | Deduction for child in junior high-school education | currency/year | 1 | 2006 | 2006 | 61 |
| `$tintced_amt2` | Deduction for child in upper high-school education | currency/year | 1 | 2006 | 2006 | 153 |
| `$tintced_amt3` | Deduction for child in tertiary education | currency/year | 1 | 2006 | 2006 | 183 |
| `$tintcmi_amt1` |  | currency | 3 | 2006 | 2017 | n/a |
| `$tintcmi_lim1` |  | currency | 3 | 2006 | 2017 | n/a |
| `$tintcmi_lim2` |  | currency | 3 | 2006 | 2017 | n/a |
| `$tintcmi_lim3` |  | currency | 3 | 2006 | 2017 | n/a |
| `$tintcmi_rate1` |  | currency | 3 | 2006 | 2017 | n/a |
| `$tintcmi_rate2` |  | currency | 3 | 2006 | 2017 | n/a |
| `$tintcmi_rate3` |  | currency | 3 | 2006 | 2017 | n/a |

### trewl_fr (10 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$trewl_bracket1` |  | currency | 2 | 2006 | 2018 | 1300000 |
| `$trewl_bracket2` |  | currency | 2 | 2006 | 2018 | 1400000 |
| `$trewl_bracket3` |  | currency | 2 | 2006 | 2018 | 2570000 |
| `$trewl_bracket4` |  | currency | 2 | 2006 | 2018 | 5000000 |
| `$trewl_bracket5` |  | currency | 2 | 2006 | 2018 | 10000000 |
| `$trewl_rate1` |  | currency | 3 | 2006 | 2019 | 0.005 |
| `$trewl_rate2` |  | currency | 2 | 2006 | 2018 | 0.007 |
| `$trewl_rate3` |  | currency | 2 | 2006 | 2018 | 0.01 |
| `$trewl_rate4` |  | currency | 2 | 2006 | 2018 | 0.0125 |
| `$trewl_rate5` |  | currency | 2 | 2006 | 2018 | 0.015 |

### bchlg_fr (9 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bchlg_amt1` | Benefit amount (basic amount since 2014)- FYA (weighted average) | currency/month | 18 | 2006 | 2025 | 197.58 |
| `$bchlg_amt2` | Benefit amount: increased amount (since 2014)- FYA (weighted average) | currency | 13 | 2006 | 2025 | 296.39 |
| `$bchlg_lim1` | Income test: limit for one earner couples | currency/year | 19 | 2006 | 2025 | 43946 |
| `$bchlg_lim2` | Income test: supplement per child | currency/year | 19 | 2006 | 2025 | 7324 |
| `$bchlg_lim3` | Income test: limit for two earner couples or lone parents | currency/year | 19 | 2006 | 2025 | 53758 |
| `$bchlg_lim4` | Income test: higher amount: one earner couples | currency | 12 | 2006 | 2025 | 21976 |
| `$bchlg_lim5` | Income test: higher amount: supplement starting with the 4th child | currency | 12 | 2006 | 2025 | 3663 |
| `$bchlg_lim6` | Income test: higher amount: two earner couples/ lone parents | currency | 12 | 2006 | 2025 | 26883 |
| `$bchlg_thres1` | Income test: minimum threshold to be considered an earner | currency/year | 18 | 2006 | 2025 | 5983 |

### bchcc_fr (8 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bchcc_amt1` | Optional CLCA-amount when receiving PAJE- FYA | currency/month | 19 | 2006 | 2025 | 749.18 |
| `$bchcc_amt2` | Optional CLCA-amount when not receiving PAJE | currency/month | 9 | 2006 | 2015 | n/a |
| `$bchcc_amt3` | CLCA-amount when reducing work by 100% and receiving PAJE- FYA | currency/month | 18 | 2006 | 2025 | 458.34 |
| `$bchcc_amt4` | CLCA-amount when reducing work by 100% and not receiving PAJE | currency/month | 11 | 2006 | 2018 | n/a |
| `$bchcc_amt5` | CLCA-amount when reducing work below 50% and receiving PAJE- FYA | currency/month | 18 | 2006 | 2025 | 296.29 |
| `$bchcc_amt6` | CLCA-amount when reducing work below 50% and not receiving PAJE | currency/month | 11 | 2006 | 2018 | n/a |
| `$bchcc_amt7` | CLCA-amount when reducing work  50%-80%  and receiving PAJE- FYA | currency/month | 18 | 2006 | 2025 | 170.92 |
| `$bchcc_amt8` | CLCA-amount when reducing work  50%-80%  and not receiving PAJE | currency/month | 11 | 2006 | 2018 | n/a |

### tintcee_fr (8 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tintcee_increase1` | Increase for dependent children | currency/year | 3 | 2006 | 2016 | n/a |
| `$tintcee_increase2` | Increase for one earner couples | currency/year | 4 | 2006 | 2016 | n/a |
| `$tintcee_increase3` | Dependent child increase for lone parents | currency/year | 3 | 2006 | 2016 | n/a |
| `$tintcee_minamt` | Minimum amount that the taxpayer needs to earn | currency/year | 4 | 2006 | 2016 | n/a |
| `$tintcee_thres0` | Intermediary threshold | currency/year | 4 | 2006 | 2016 | n/a |
| `$tintcee_thres1` | Maximum threshold for singles & couples with two earned revenues | currency/year | 4 | 2006 | 2016 | n/a |
| `$tintcee_thres2` | Intermediary threshold | currency/year | 4 | 2006 | 2016 | n/a |
| `$tintcee_thres3` | Max threshold for one earner couples | currency/year | 4 | 2006 | 2016 | n/a |

### tscxc_fr (8 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$casa_rate` | Rate for contribution for solidarity and autonomy (CASA) | currency | 2 | 2006 | 2013 | 0.003 |
| `$tscxc_rate1` | CSG normal rate on earnings | currency | 2 | 2006 | 2018 | 0.092 |
| `$tscxc_rate2` | CSG normal rate on pensions | currency | 2 | 2006 | 2018 | 0.083 |
| `$tscxc_rate3` | CSG normal rate on unemployment benefits | currency | 1 | 2006 | 2006 | 0.062 |
| `$tscxc_rate4` | CSG rate on capital income | currency | 3 | 2006 | 2019 | 0.092 |
| `$tscxc_rate5` | CSG rate on sickness benefit | currency | 1 | 2006 | 2006 | 0.062 |
| `$tscxc_rate6` | CSG median rate on pensions (from 2019) | currency | 2 | 2006 | 2019 | 0.066 |
| `$tscxc_rate7` | CSG reduced rate on pensions | currency | 1 | 2006 | 2006 | 0.038 |

### bched_fr (7 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bched_amt1` | Benefit amount (for child aged 6-10)-    2022 FYA= (378.87+394.02)/2 | currency/year | 17 | 2006 | 2025 | 425.61 |
| `$bched_amt2` | Benefit amount for child aged 11-14-    2022 FYA=(399.78+415.77)/2 | currency | 17 | 2006 | 2025 | 449.09 |
| `$bched_amt3` | Benefit amount for child aged 15-18-2022 FYA=(413.63+430.17)/2 | currency | 16 | 2006 | 2025 | 464.65 |
| `$bched_lim1` | Income limit for families with 1 child | currency/year | 18 | 2006 | 2025 | 28444 |
| `$bched_lim2` | Income limit for families with 2 children | currency/year | 18 | 2006 | 2025 | 35008 |
| `$bched_lim3` | Income limit for families with 3 children | currency/year | 18 | 2006 | 2025 | 41572 |
| `$bched_lim4` | Additional amount for income limit starting with the 4th child | currency/year | 18 | 2006 | 2025 | 6564 |

### bchlp_fr (7 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bchlp_fm_amt01` | Family minimum - Pregnant without child (not used) | currency/month | 4 | 2006 | 2009 | n/a |
| `$bchlp_fm_amt02` | Family minimum - One dependent child | currency/month | 4 | 2006 | 2009 | n/a |
| `$bchlp_fm_amt03` | Family minimum - Two dependent children | currency/month | 4 | 2006 | 2009 | n/a |
| `$bchlp_fm_amt04` | Family minimum - Increase for additional children | currency/month | 4 | 2006 | 2009 | n/a |
| `$bchlp_hp_amt01` | Housing Package - Pregnant without child (not used) | currency/month | 4 | 2006 | 2009 | n/a |
| `$bchlp_hp_amt02` | Housing Package - One dependent child | currency/month | 4 | 2006 | 2009 | n/a |
| `$bchlp_hp_amt03` | Housing Package - Two dependent children | currency/month | 4 | 2006 | 2009 | n/a |

### bdi_fr (7 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bdi_amt1` | Benefit amount per month: basic | currency/month | 19 | 2006 | 2025 | 1033.32 |
| `$bdi_amt2` | Benefit amount: supplement for independent living | currency/month | 5 | 2006 | 2018 | 104.77 |
| `$bdi_disr1` | Means test: income disregard for non-disabled partner | currency | 3 | 2006 | 2024 | n/a |
| `$bdi_disr2` | Means test: income disregard per child for non-disabled partner | currency | 3 | 2006 | 2024 | n/a |
| `$bdi_lim1` | Means test: income limit for single adult | currency/year | 20 | 2006 | 2025 | 12400 |
| `$bdi_lim2` | Means test: income limit for couple | currency/year | 19 | 2006 | 2024 | n/a |
| `$bdi_lim3` | Means test: income limit per child | currency/year | 20 | 2006 | 2025 | 6200 |

### tpr_fr (7 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tpr_rate_baties` | Tax rates | currency | 5 | 2006 | 2019 | 0.3062 |
| `$tpr_rate_nonbaties` |  | currency | 2 | 2006 | 2013 | 0 |
| `$tpr_threshold1` | Thresholds for total exemption | currency | 3 | 2006 | 2017 | 10708 |
| `$tpr_threshold2` |  | currency | 2 | 2006 | 2013 | 2839 |
| `$tpr_threshold3` | Thresholds for cap on tax | currency | 3 | 2006 | 2017 | 25180 |
| `$tpr_threshold4` |  | currency | 3 | 2006 | 2017 | 5883 |
| `$tpr_threshold5` |  | currency | 3 | 2006 | 2017 | 4631 |

### bunmt_fr (6 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bunmt_bonus1` |  | currency | 2 | 2006 | 2012 | 152.45 |
| `$bunmt_bonus2` |  | currency | 2 | 2006 | 2023 | 205.81 |
| `$bunmt_bonus3` |  | currency | 2 | 2006 | 2023 | 232.49 |
| `$bunmt_bonus4` |  | currency | 2 | 2006 | 2023 | 248.49 |
| `$bunmt_bonus5` |  | currency | 2 | 2006 | 2023 | 269.84 |
| `$bunmt_bonus6` |  | currency | 2 | 2006 | 2023 | 21.34 |

### tin_fr (5 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tinto_lim1` | First income limit for singles | currency | 2 | 2006 | 2013 | 250000 |
| `$tinto_lim2` | Second income limit for singles and first income limit for couples | currency | 2 | 2006 | 2013 | 500000 |
| `$tinto_lim3` | Second income limit fo couples | currency | 2 | 2006 | 2013 | 1000000 |
| `$tinto_rate1` | Rate 1 for exceptional contributions | currency | 2 | 2006 | 2013 | 0.03 |
| `$tinto_rate2` | Rate 2 for exceptional contributions | currency | 2 | 2006 | 2013 | 0.04 |

### tsckt_fr (4 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tsckt_addrate` | Additional contribution | currency | 2 | 2006 | 2019 | n/a |
| `$tsckt_social_rate` | Social contribution | currency | 5 | 2006 | 2019 | n/a |
| `$tsckt_solidarity_rate` | Solidarity contribution | currency | 4 | 2006 | 2019 | n/a |
| `$tsckt_solidaritylevy_rate` | Solidarity levy | currency | 2 | 2006 | 2019 | 0.075 |

### SetDefault_fr (2 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$MinWage` | Statutory monthly gross minimum wage, no FYA implemented | currency/month | 20 | 2006 | 2025 | 1801.8 |
| `$Minwage_hourly` | FYA- 2021- 2024 | currency/month | 20 | 2006 | 2025 | 11.88 |

### bchba_fr (2 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bchba_amt1` | Before 2014 (1/04/2014 in policy rules) & 2014-2017 (March 2018 in policy rules) | currency/year | 9 | 2006 | 2019 | n/a |
| `$bchba_amt2` | From 2018 (1/04/2018 in policy rules)- FYA (weighted average: (970.19+1008.99)/2 | currency | 9 | 2006 | 2025 | 1089.88 |

### bchor_fr (2 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bchor_amt1` | Amount for children with one parent -FYA | currency/month | 19 | 2006 | 2025 | 200.18 |
| `$bchor_amt2` | Amount for children with no parents -FYA | currency/month | 19 | 2006 | 2025 | 266.83 |

### bmact_fr (2 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bma_max` | On daily basis, maximum amount for maternity/paternity/adoption leave | currency | 1 | 2006 | 2006 | n/a |
| `$bma_min` | On monthly basis, minimum amount of disability pension, sickness/maternity/pater | currency | 1 | 2006 | 2006 | n/a |

### bsaeccm_fr (2 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bsaeccm_TU_amt` |  | currency | 3 | 2006 | 2021 | n/a |
| `$bsaeccm_child_amt` |  | currency | 3 | 2006 | 2021 | n/a |

### bsaoa_fr (2 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$bsaoa_amt1` | Income limit for single person- FYA | currency/month | 20 | 2006 | 2025 | 1034.28 |
| `$bsaoa_amt2` | Income limit for couples - FYA | currency/month | 19 | 2006 | 2025 | 1605.73 |

### tscdf_fr (1 parameters)

| Constant | Label | Unit | # values | First | Last from | Latest value |
|---|---|---|---|---|---|---|
| `$tscdf_fullrate` | Rate | currency | 1 | 2006 | 2006 | 0.005 |

