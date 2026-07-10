# Variable Naming & Income Lists Reference

## Table of Contents
- [Variable Prefix System](#variable-prefix-system)
- [Social Contribution Subtypes](#social-contribution-subtypes)
- [Special Suffixes and Prefixes](#special-suffixes-and-prefixes)
- [Standard Income Lists](#standard-income-lists)
- [Period Suffixes](#period-suffixes)
- [VARCONFIG.xml Lookup](#varconfigxml-lookup)
- [Tax Unit Conventions](#tax-unit-conventions)
- [Parameter Value Interpretation](#parameter-value-interpretation)

## Variable Prefix System

| Prefix | Category | Key Variables |
|--------|----------|---------------|
| `y` | Income | `yem` (employment), `yse` (self-employment), `yiy` (investment), `yot` (other) |
| `b` | Benefits | `bch` (child), `bsa` (social assistance), `bun` (unemployment), `bho` (housing) |
| `t` | Taxes | `tin` (income tax), `tsc` (social contributions), `tpr` (property tax) |
| `p` | Pensions | `poa` (old-age), `psu` (survivor), `pdi` (disability) |
| `d` | Demographics | `dag` (age), `dgn` (gender), `dms` (marital status), `dec` (education) |
| `x` | Expenditure | `xhc` (housing costs), `xmp` (mortgage), `xcc` (child care) |
| `l` | Labour | `les` (economic status) |
| `a` | Assets | `afc` (financial capital) |
| `k` | In-kind | `kfb` (food benefits) |
| `id` | Identifiers | `idhh` (household), `idperson` (person), `idmother`, `idfather`, `idpartner` |

## Social Contribution Subtypes

| Variable | Meaning |
|----------|---------|
| `tscee` | Employee social insurance contributions |
| `tscse` | Self-employed social insurance contributions |
| `tscer` | Employer social insurance contributions |
| `tsceehl` | Employee health insurance |
| `tsceeui` | Employee unemployment insurance |

## Special Suffixes and Prefixes

| Marker | Meaning | Example |
|--------|---------|---------|
| `_s` | Simulated by model | `bch_s`, `tin_s` |
| `$` | Constant (DefConst) | `$bch_amt1`, `$tin_rate1` |
| `ils_` | Standard income list (all countries) | `ils_dispy`, `ils_origy` |
| `il_` | Country-specific income list | `il_TaxableY` |
| `tu_` | Tax unit | `tu_individual_sl` |
| `stm` | System temporary variable | `stm01_s` |
| `sin` | System intermediate variable | `sin01_s` |
| `sel` | Eligibility variable (Elig default output) | `sel_s` |
| `dwt` | Household sampling weight | — |

## Standard Income Lists

Defined in every country with standardized meanings:

| Income List | Components |
|---|---|
| `ils_earns` | yem + yse |
| `ils_origy` | yem + yse + yiy (original income) |
| `ils_pen` | poa (+ other pensions) |
| `ils_ben` | ils_pen + ils_benmt + ils_bennt |
| `ils_benmt` | Means-tested benefits (e.g., bsa_s) |
| `ils_bennt` | Non-means-tested benefits (e.g., bch_s) |
| `ils_bensim` | Simulated benefits |
| `ils_tax` | ils_taxsim (= tin_s) |
| `ils_taxsim` | Simulated taxes |
| `ils_sicee` | Employee SICs (tscee_s) |
| `ils_sicse` | Self-employed SICs (tscse_s) |
| `ils_sicer` | Employer SICs (tscer_s) |
| `ils_sicdy` | ils_sicee + ils_sicse + ils_sicot |
| **`ils_dispy`** | **Disposable income** = ils_origy + ils_ben - ils_tax - ils_sicdy |

## Period Suffixes

EUROMOD works internally in **monthly** amounts. Suffixes convert:

| Suffix | Period | Conversion |
|--------|--------|------------|
| `#m` | Monthly | No conversion (internal unit) |
| `#y` | Yearly | ÷ 12 |
| `#q` | Quarterly | ÷ 3 |
| `#w` | Weekly | × 4.34 |
| `#d` | Daily | × 30.5 |
| `#l` | Labour day | × 21.73 |
| `#s` | Labour day (6-day) | × 26.07 |

Example: `5000#y` = 5000 EUR/year → ~416.67/month internally.

## VARCONFIG.xml Lookup

VARCONFIG.xml (20 MB) maps acronym prefixes to meanings. To decode a variable:

- `dag` → `d` (demographic) + `ag` (age) = age
- `yem` → `y` (income) + `em` (employment) = employment income
- `bch_s` → `b` (benefit) + `ch` (child) + `_s` (simulated)
- `tscee_s` → `t` (tax) + `sc` (social contribution) + `ee` (employee) + `_s` (simulated)

Search with grep:
```bash
grep -A2 'CDATA\[yem\]' VARCONFIG.xml
```

## Tax Unit Conventions

| Type | Description | Example |
|------|-------------|---------|
| `IND` | Each person is their own unit | `tu_individual_{cc}` |
| `HH` | Entire household | `tu_household_{cc}` |
| `SUBGROUP` | Nuclear family subset | `tu_sben_family_{cc}` |

## Parameter Value Interpretation in Tax Units

| Value type | In conditions | In formulas |
|---|---|---|
| Monetary variables & income lists | Summed over unit | Summed over unit |
| Non-monetary variables | Individual level | Head of unit |
| Individual queries (IsMarried, etc.) | Individual level | Head of unit |

**VOID vs zero:** Simulated variables start at VOID (0.0000000000001), marking them as "not yet calculated." Functions write real values to them.
