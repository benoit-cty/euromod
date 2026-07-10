# Simpleland (SL) Complete Walkthrough

Simpleland is the EUROMOD teaching country with one system (`SL_1996`), using `sl_demo_v4` as input data.

## Policy Spine

| Order | Policy | Type | Functions | Key Output |
|-------|--------|------|-----------|------------|
| 1 | `Uprate_sl` | def | Uprate | All factors = 1 (same year) |
| 2 | `ILsDef_sl` | def | DefIl ×17 | ils_earns, ils_origy, ils_ben, ils_dispy, etc. |
| 3 | `tudef_sl` | def | DefTu ×4 | tu_individual_sl, tu_household_sl, tu_sben_family_sl |
| 4 | `ILDef_sl` | def | DefIl ×2 | il_TaxableY, il_bsa_base |
| 5 | `yem_sl` | def | ArithOp (off) | Minimum wage (inactive) |
| 6 | `neg_sl` | def | Max | yse = max(yse, 0) |
| 7 | `sic_sl` | sic | DefConst + SchedCalc ×3 | tscer_s (10%), tscee_s (5%), tscse_s (13% capped) |
| 8 | `bch_sl` | ben | DefConst + ArithOp | bch_s = 200#m × nChildren |
| 9 | `tin_sl` | tax | DefConst + SchedCalc | tin_s = 20% above 1000#m |
| 10 | `bsa_sl` | ben | DefConst + BenCalc | bsa_s = components by role, 80% withdrawal |
| 11 | `output_std_sl` | def | DefOutput | All vars and ILs to file |
| 12 | `output_std_hh_sl` | def | DefOutput (off) | Household-level output |

## Data Flow Trace

```
yem (from dataset)
  → Uprate_sl: yem × 1 (no change)
  → ILsDef_sl: yem → ils_earns, ils_origy
  → sic_sl: yem → SchedCalc → tscee_s (5%)
  → ILDef_sl: ils_origy + bch_s - ils_sicee - ils_sicse → il_TaxableY
  → tin_sl: il_TaxableY → SchedCalc → tin_s (20% above 1000#m)
  → bsa_sl: il_TaxableY + poa - ils_tax → il_bsa_base → BenCalc → bsa_s
  → ILsDef_sl: ils_origy + ils_ben - ils_tax - ils_sicdy → ils_dispy
  → output_std_sl: written to file
```

## SIC Policy Detail

**Employer SIC** (10% of employment income):
```xml
<Function>
  <Name>SchedCalc</Name>
  <Parameter><Name>base</Name><Value><![CDATA[yem]]></Value></Parameter>
  <Parameter><Name>band_rate</Name><Value><![CDATA[0.1]]></Value><Group>1</Group></Parameter>
  <Parameter><Name>output_var</Name><Value><![CDATA[tscer_s]]></Value></Parameter>
  <Parameter><Name>TAX_UNIT</Name><Value><![CDATA[tu_individual_sl]]></Value></Parameter>
</Function>
```

**Self-employed SIC** (13% with monthly ceiling of 325):
```xml
<Function>
  <Name>SchedCalc</Name>
  <Parameter><Name>base</Name><Value><![CDATA[yse]]></Value></Parameter>
  <Parameter><Name>band_rate</Name><Value><![CDATA[$tscse_rate1]]></Value><Group>1</Group></Parameter>
  <Parameter><Name>uplim</Name><Value><![CDATA[325#m]]></Value></Parameter>
  <Parameter><Name>output_var</Name><Value><![CDATA[tscse_s]]></Value></Parameter>
</Function>
```

## Child Benefit Detail

Flat 200#m per dependent child in the family unit:
```xml
<Function>
  <Name>ArithOp</Name>
  <Parameter><Name>formula</Name>
    <Value><![CDATA[$bch_amt1 * nDepChildrenInTU]]></Value></Parameter>
  <Parameter><Name>output_var</Name><Value><![CDATA[bch_s]]></Value></Parameter>
  <Parameter><Name>TAX_UNIT</Name>
    <Value><![CDATA[tu_sben_family_sl]]></Value></Parameter>
</Function>
```

Family with 3 children → 600/month.

## Income Tax Detail

20% flat rate on taxable income above 1000#m threshold:

```xml
<Function>
  <Name>SchedCalc</Name>
  <Parameter><Name>base</Name><Value><![CDATA[il_TaxableY]]></Value></Parameter>
  <Parameter><Name>band_lowLim</Name>
    <Value><![CDATA[$tin_lowthres1]]></Value><Group>1</Group></Parameter>
  <Parameter><Name>band_rate</Name>
    <Value><![CDATA[$tin_rate1]]></Value><Group>1</Group></Parameter>
  <Parameter><Name>output_var</Name><Value><![CDATA[tin_s]]></Value></Parameter>
  <Parameter><Name>TAX_UNIT</Name>
    <Value><![CDATA[tu_individual_sl]]></Value></Parameter>
</Function>
```

Person with il_TaxableY = 2,000#m → tax = (2,000 - 1,000) × 0.2 = 200#m.

## Social Assistance Detail

Role-based components with 80% income withdrawal:

- Head: 500#m
- Dependent child: 200#m
- Other adult: 350#m

**Example household** (1 head, 1 partner, 2 children):
- Gross = 500 + 350 + 2×200 = 1,250#m
- If il_bsa_base = 500#m → 1,250 - 500×0.8 = 850#m
- If il_bsa_base = 1,562.50#m → fully withdrawn (0)

## Key Income Lists

```
il_TaxableY = ils_origy + bch_s - ils_sicee - ils_sicse
il_bsa_base = il_TaxableY + poa - ils_tax
ils_dispy   = ils_origy + ils_ben - ils_tax - ils_sicdy
```

## Tax Units

| Name | Type | Children condition |
|------|------|--------------------|
| `tu_individual_sl` | IND | — |
| `tu_household_sl` | HH | ≤15 (or ≤18 if in education) |
| `tu_sben_family_sl` | SUBGROUP | Head + partner + own dep. children |
| `tu_hh_oecd_co` | HH | <14 (OECD equivalised) |
