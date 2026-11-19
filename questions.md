# Open questions for the EUROMOD team

Checked against the parameter store on 10 November 2026 (September 2026 enriched exports).
Questions are renumbered per section; the previous number is given in brackets.

## Working hypotheses

These are the assumptions Nómos currently makes. Please tell us which ones are wrong.

- **H1 — A system year holds the rules in force on 30 June of that year.** System `FR_2025` holds the parameter values in force on 30 June 2025 and applies them to 2025 incomes.
- **H2 — French income tax follows H1; only the legal label differs.** `FR_2025` holds the schedule enacted by the 2025 finance act (loi n° 2025-127 of 14 February 2025). French law calls it the schedule "for 2024 income" («impôt 2025 sur les revenus 2024»). EUROMOD applies it to 2025 incomes, with no adjustment since `FR_2019` (see "Evidence in the model" below). So when Nómos looks for the value of system year Y, it searches the finance act that French law labels "income Y−1". This is a search rule, not a claim about which incomes EUROMOD taxes. The evidence is in the table below. It applies to 32 French parameters (schedule, décote, family-quotient caps, 10 % deduction limits).
- **H3 — A few parameters hold the 1 January value.** Eight French parameters (`$tpr_threshold*`, `$UB_dayfixamt`, `$tscerui_rate1`, `$bsawk_income_rate`) show a mid-year legal change only in the following system year.
- **H4 — A mid-year change is held either as a weighted average or as the amount in force.** Some values are formulas such as `(11.65*10 + 11.88*2)/12`. Others are labelled "FYA" but hold the single amount in force after the change. Nómos always proposes the amount in force and accepts either form.
- **H5 — Rates are fractions.** `8.17%` and `0.0817` are the same value, with unit `/1`. A few rates are held in percentage points (`$bho_rl_rate2` = 0.45 for 0.45 %).
- **H6 — The suffix gives the period.** `#m` is monthly and `#y` is yearly, and `747#m` equals `8964#y`.
- **H7 — The law is the reference.** When EUROMOD is one euro or one cent away from the figure the law states, Nómos reports it as a finding. It does not treat it as a rounding tolerance.
- **H8 — Some parameters are not in any act.** National averages (for example `$tpr_rate_baties`) and values supplied by the national team are never proposed from legislation.

Evidence for H2 — first threshold of the income tax schedule (`$tin_upthres1`):

| System year | EUROMOD | Finance act stating it | French legal label | OpenFisca files it under |
|---|---|---|---|---|
| 2022 | 10 225 | LF 2022 | income 2021 | 2021 |
| 2023 | 10 777 | LF 2023 | income 2022 | 2022 |
| 2024 | 11 294 | LF 2024 | income 2023 | 2023 |
| 2025 | 11 496 | LF 2025 (states 11 497) | income 2024 | 2024 |
| 2026 | 11 600 | LF 2026 | income 2025 | 2025 |

EUROMOD and OpenFisca therefore differ by one year on these parameters: OpenFisca files the 2025 finance act schedule under 2024, EUROMOD under 2025.

Evidence in the model (`FR.xml`, release J2.54+, policy `tinty_fr`):

- `FR_2006` to `FR_2018` contain a function "Backrating employment income to better match income year/tax year". It multiplies employment income by about 0.97 (`i_yempv = 0.970157411456056*yem00` in `FR_2018`) before the tax is computed. So the model treated the schedule of system year Y as the schedule for the income of Y−1, and brought earnings back to that level.
- From `FR_2019` to `FR_2026` this function is switched to `n/a`, and the deductions and the schedule read `yem00` directly. 2019 is the year withholding at source started.
- The schedule kept its one-year lag after 2019: `FR_2019` holds 10 064, the schedule of the 2019 finance act, for 2018 income.
- `uprate_fr` brings every income of the dataset to the level of the policy year before any policy runs.

## General questions

- **G1 (was Q1) — Year convention.** Did you get an answer on how the model handles the year, as discussed on Teams? You pointed out that the note in `FR.curation.yaml` says "income tax assessed in year Y is assessed on income of year Y−1", while `FR_2025` computes tax on 2025 income. We think both statements are true: since `FR_2019` the model applies to 2025 income the schedule that French law enacted for 2024 income (see H2 and the evidence from `FR.xml`). We have reworded the note. Can you confirm H2? And was dropping the backrating in 2019 a deliberate choice linked to withholding at source?
- **G2 (was Q2) — Deployment.** Did the IT team answer on how Nómos could be deployed?
- **G3 (was Q5) — Repository.** When should we switch from GitLab to GitHub?
- **G4 (was Q6) — Trying Nómos.** Do you have time to try Nómos yourself, for example by ingesting Belgium? We would rather keep our remaining days to support the EUROMOD team in using it. Status: waiting for the IT team to allow Hannes to use Docker.
- **G5 (was Q13) — All our corrections to the export.** Every change we apply on top of the EUROMOD export is in <https://github.com/benoit-cty/euromod/blob/main/Nomoscope-agentic-workflow/pipeline/curation/>. Could each country team review its file?
- **G6 (was Q4) — Irish bracket groups. Answered.** The Irish export now has 14 bracket groups.

## Questions for the French team

- **FR1 (was Q3) — `$Minwage_hourly` has a monthly period.** The export gives `11.88#m` for 2025. But 11.88 is the hourly minimum wage in euro (the monthly one is 1 801.80). Is the `#m` suffix intended? We treat the parameter as `currency/hour`.
- **FR2 (was Q7) — Rate parameters with unit `currency`. Mostly fixed.** The September export corrected 132 of the 146 rates. Eight remain: `$mc_yem_rrate` has no unit, and `$tpr_rate_nonbaties`, `$tintcch_rate` and `$xcc_rate1` to `$xcc_rate5` have unit `/100` while their sibling rates are fractions. Their values are null or 0, so we cannot tell which unit is right. The list is in [FR.curation.yaml](https://github.com/benoit-cty/euromod/blob/main/Nomoscope-agentic-workflow/pipeline/curation/FR.curation.yaml).
- **FR3 (was Q8) — The 2025 schedule is one euro below the law.** `$tin_upthres1`, `3`, `4` and `5` hold 11 496, 29 314, 83 822 and 180 293. CGI art. 197, as amended by the 2025 finance act, states 11 497, 29 315, 83 823 and 180 294. The 2022, 2023, 2024 and 2026 values match the law exactly. The Country Report shows the likely cause (see FR4): in the 2025 column the law's thresholds were written as the start of each band, and the band ends were obtained by subtracting one.
- **FR4 (was Q10) — Country Report, Table 2.77.** Three points on the column "Taxation 2025 (income 2025)":
  - The header is wrong as a statement of French law. The column contains the schedule for 2024 income (taxation 2025, finance act for 2025). The schedule for 2025 income is 11 600, 29 579, 84 577, 181 917. The same shift applies to the three other columns. If the header means "applied by EUROMOD to 2025 incomes" (H2), could it say so, for example "Policy year 2025 (schedule for 2024 income)"?
  - The 2025 column is shifted by one euro. In the other columns the first band ends at the law's threshold ("0 to 11 294", then "11 295 to …"). In the 2025 column the law's threshold starts the next band ("0 to 11 496", then "11 497 to …"). The law states 11 497 as the end of the first band.
  - Its last two rows disagree: "83 823 to 180 293", then "> 180 294".
- **FR5 (was Q9) — Multiples of the social security ceiling stored as numbers.** `$tsc_group2_lim` (11 775) and `$tsc_groupB_lim` (15 700) are 3 and 4 times the monthly ceiling (3 925 in 2025). Elsewhere the export writes such multiples as formulas. Could these be `$PSS`-based formulas too? No act states 11 775 or 15 700, so Nómos cannot find them in the law.
- **FR6 (was Q11) — `$tinty_dedub_uplim` is 0.** It has been 0 since system year 2019. CGI art. 83 still states a ceiling: 14 426 for system year 2025 and 14 555 for 2026, the values `$tinty_ded_maxamt` holds. In `tinty_fr` the constant is still used as the upper limit of the 10 % deduction on unemployment benefits (`comp_uplim#2 = $tinty_dedub_uplim`), and the lower limit `$tinty_dedbun_lowlim` is 0 too. Does an upper limit of 0 set this deduction to zero since `FR_2019`? If so, is that intended?
- **FR7 (was Q12) — `$tscsepi_uplim` is 43 891 for 2025.** This is the first-band ceiling of the complementary pension contribution of self-employed traders and craftsmen. 43 891 is the former specific ceiling, uprated. We understand that, since the 2025 reform of self-employed contributions, the first band ends at the annual social security ceiling (47 100 in 2025). Should the 2025 and 2026 values (43 891 and 44 286) be 47 100 and 48 060?

## Questions for the Irish team

- **IE1 (was Q11) — Rate parameters with unit `currency`.** 48 parameters hold fractions but have unit `currency`: `$tin_high_rate`, `$tin_Std_rate`, `$txcin_rate1` to `4`, the PRSI class rates, the pension relief rates `$tin_pen_rate1` to `6`, the LPT rates. We treat them as `/1`. The list is in [IE.curation.yaml](https://github.com/benoit-cty/euromod/blob/main/Nomoscope-agentic-workflow/pipeline/curation/IE.curation.yaml).
- **IE2 (was Q14) — USC 2 % band ceiling.** `$txcin_upthres2` holds 27 383 for 2025. The law states 27 382.

## Questions for the Spanish team

- **ES1 (was Q15) — The IMV amount is 8 cents below the law.** `$bsa00_amt` holds 7 905.72 per year for 2025, which is 658.81 × 12: the monthly amount rounded to the cent, then annualised. The law states 7 905.80 per year, the value `$poanc_amt` holds.
- **ES2 (was Q16) — Capital income schedule group.** The group `ES:tin_cons_es:tin_capinc_schedule` does not include the 300 000 threshold `$tin_capinc_lim4`, nor the fifth-band rates `$tin_capinc_*rate5`. Should they be part of the group?

## Questions for the Lithuanian team

- **LT1 (was Q12) — Parameters with unit `currency` that are not amounts.** 54 parameters hold fractions and we treat them as `/1`: the income tax and contribution rates, `$tinta_basic_WithdRate*`, `$mc_share*`, `$bsa00_scale_coef*`. 26 more are multipliers above 1, which we treat as `ratio`. A few are durations or volumes (`$bplct_duration_m`, `$xhcht_*_m3`). The list is in [LT.curation.yaml](https://github.com/benoit-cty/euromod/blob/main/Nomoscope-agentic-workflow/pipeline/curation/LT.curation.yaml).
