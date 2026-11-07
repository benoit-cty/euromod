# FR golden set — selection and build guide

France's golden set: 59 cases for system year 2025 (as-of 2025-06-01). Two selection rows in
`eval.golden_selections` produce them:

| kind | entries | cases | where the expected value comes from |
|---|---|---|---|
| `openfisca` | 52 (1 excluded, 1 skipped) | 50 | OpenFisca-France, read at the as-of date (income-year parameters at the income-year start) |
| `curated` | 9 | 9 | stated in the entry, in EUROMOD's own spelling |

This document is the rationale. The rows are the source; edit them with `selection-export` /
`selection-import`, never the case rows.

```bash
uv run nomokrisis-eval selection-export FR --kind openfisca --out /tmp/fr_of.json
uv run nomokrisis-eval selection-export FR --kind curated   --out /tmp/fr_cu.json
#   ... edit, then:
uv run nomokrisis-eval selection-import /tmp/fr_of.json
uv run nomokrisis-eval selection-import /tmp/fr_cu.json
uv run nomokrisis-eval build-openfisca-dataset --year 2025 --country FR --limit 100
uv run nomokrisis-eval build-curated-dataset   --year 2025 --country FR
```

`--limit 100`: the default of 50 cuts the openfisca selection, which now has 51 entries that draft.

## Every case is an explicit entry

The openfisca row's header carries `fill_from_links: false`. The builder used to top the set up
from `params.parameter_links` by link score. On 7 Nov 2026, seven of those top-ups were no longer
produced by the links (the three `bch00` AF ceilings, `tintadp_amt`, `tscxc_thres3/4/6`). They
survived only because they had been reviewed, so a rebuild would have left them stale without
saying so. All 20 top-ups are now explicit entries, with the same case ids.

An entry with `exclude: true` is neither drafted nor topped up. `tscsepi_uplim` is excluded
from the openfisca kind because OpenFisca's `montant_du_plafond_rci` is the RCI ceiling the 2025
reform abolished. Its case is in the curated row instead.

## What the FR 2025 benchmark changed (review of 7 Nov 2026)

The blind EUROMOD 2024 → 2025 benchmark (agent 0.9.1, 345 parameters) showed which texts answer
which parameters. Here is what it changed in this set.

**Answerable now, expected value unchanged, citations and `corpus_available` added.** These
cases were `no_corpus` or `undocumented` in the September runs:
- AF ceilings `bch00_child2_thres1/2`, `child3plus_thres`: instruction DSS/2B/2024/181 (guidance).
- `bunmt_amt`: décret n° 2025-302 (ASS).
- `UB_dayminamt`: convention d'assurance chômage du 15 novembre 2024, annexe II art. 14. It is
  a collective agreement and so evidence (ADR 0006). It used to be "HARD / not_found".
- `tintadp_amt`, `tinty_ded_*`, `tinty_dedpens_*`: décret n° 2025-547 art. 2 (CGI
  incorporation), plus CGI art. 83 / 158.
- `tscxc_thres3–6`: the CSG instruction of 4 Dec 2024 (guidance). L136-8 holds only the
  pre-indexation figures.
- `tscersi_rate`: CSS D242-3.
- `MinWage`: Cnav circular 2025/08 is also accepted.
- `tin_imaxdep_lim1/2` and `tin_imaxwd_amt`: BOFiP BOI-IR-LIQ-20-20-20 is also accepted.

**Wrong expectations, corrected.**
- `tinty_dedub_uplim` expected `changed` to 14 426. EUROMOD has held 0 as `national_team` since
  2019, so the pipeline routes `national_team_source` and never proposes. It is now a
  national-team trap case.
- `tscsepi_uplim` expected 43 891, `unchanged`, from OpenFisca. Since 1 January 2025, CSS D635-7
  (décret n° 2024-688) bands the RCI at the annual PSS: 47 100. The case is now curated,
  `changed` to 47 100. It is a EUROMOD finding: the 2025 self-employed reform is not modelled,
  and the 8,1 / 9,1 % rates where EUROMOD keeps 7 / 8 % are part of the same finding.
- `Minwage_hourly`: the unit defect the note described is fixed in the store (`currency/hour`).
  Only the note changed.

**Kept, with a better note.** `tscsepi_rate5`: CSS D633-3 applies 0,72 % from 1 January 2025.
EUROMOD holds 0,60 % for 2025 and moves only in 2026, so `changed` is right, and EUROMOD is a
year behind.

**New curated cases: kinds of evidence the openfisca kind cannot state.**

| case | what it tests |
|---|---|
| `tscee_tsceeui_rate2` | a collective agreement as evidence: ANI APEC du 12 juillet 2011 art. 14 (a transcription; the signed PDF is a scan) |
| `tscer_tscerpi_rate4` | AGIRC-ARRCO arithmetic: 6,20 % × 127 % × 60 % = 4,72 % (ANI 2017 art. 35/36). The circular states the same figure verbatim |
| `bsa00_bsa00_amt3` | **the first ready FR derive case**: RSA 646,52 × 1,8 = 1 163,74 (décret n° 2025-293 + CASF R262-1) |
| `bsawk_bsawk_minamt4` | prime d'activité 633,21 × 1,5 = 949,82. EUROMOD labels it "FYA" but holds the April amount |
| `bch00_bch00_child2_amt` | a one-cent EUROMOD finding: the law says 151,80, EUROMOD holds 151,81. The expected value is the law's |
| `bsa00_bsa00_bonus_amt1` | an act later in the year: the prime de Noël décret enters into force on 14 Dec 2025 |
| `constdef_ub_dayfixamt` | the `start_of_year` basis: 13,11 on 1 January 2025, not the 13,18 of 1 July |

## Verification

The rebuild reset every case whose ground truth moved (citations included) to `verified:
false`. 40 of the 59 cases need a human check before `nomokrisis-eval run` counts them, since
runs are `--verified-only` by default. Use the UI's Golden set tab or `nomokrisis-eval verify
<id>`.

## Still out of reach (not in the set)

- **AGS rate (`tscerwgf_rate`):** no source dated 2025 is in the corpus. The 17 Dec 2025
  release states only the 2026 rate.
- **Employee unemployment and health rates of 0 %:** no text states a zero.
- **Farmers' schedules:** the 2025 corpus holds only the 2026 amendment.
