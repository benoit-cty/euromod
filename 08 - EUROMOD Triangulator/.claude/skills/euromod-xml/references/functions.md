# Function Types Reference

## Table of Contents
- [Definition Functions](#definition-functions)
- [ArithOp](#arithmop)
- [Elig](#elig)
- [BenCalc](#bencalc)
- [SchedCalc](#schedcalc)
- [DefIl](#defil)
- [DefConst](#defconst)
- [DefTu](#deftu)
- [Uprate](#uprate)
- [DefOutput](#defoutput)
- [Allocate](#allocate)
- [Loop / UnitLoop](#loop--unitloop)
- [Store / Restore](#store--restore)
- [Other Functions](#other-functions)

---

## Definition Functions

| Function | Purpose |
|----------|---------|
| `Uprate` | Adjust monetary dataset values for inflation |
| `DefIl` | Define income lists (aggregates of variables) |
| `DefConst` | Define named constants (`$name`) |
| `DefVar` | Define intermediate variables |
| `DefTu` | Define assessment/tax units |
| `UpdateTu` | Redefine assessment units mid-calculation |
| `SetDefault` | Set default values for missing variables |
| `DefOutput` | Specify output file contents |
| `DefInput` | Read values from external file |

## ArithOp

Simple arithmetic calculator. Evaluates a formula and writes the result.

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `formula` | Yes | Expression to evaluate |
| `output_var` | Yes* | Variable to store result (overwrites) |
| `output_add_var` | Yes* | Variable to add result to (*one of the two required) |
| `TAX_UNIT` | Yes | Assessment unit |
| `lowlim` | No | Lower limit on result |
| `uplim` | No | Upper limit on result |
| `threshold` | No | Below this → result = 0 |
| `who_must_be_elig` | No | `one`/`one_adult`/`all`/`all_adults`/`nobody` |
| `result_var` | No | Second output variable (always overwrites) |

**Formula syntax:** Variables (`yem`), constants (`$bch_amt1`), income lists (`il_TaxableY`), queries (`nDepChildrenInTU`, `IsHeadOfTu`), operators (`+`,`-`,`*`,`/`), amounts with period (`5000#y`), functions (`MIN(a,b)`, `MAX(a,b)`).

**XML example:**
```xml
<Function>
  <Name>ArithOp</Name>
  <Switch>on</Switch>
  <Parameter><Name>formula</Name>
    <Value><![CDATA[$bch_amt1 * nDepChildrenInTU]]></Value>
    <ValueType>formula</ValueType></Parameter>
  <Parameter><Name>output_var</Name>
    <Value><![CDATA[bch_s]]></Value>
    <ValueType>variable</ValueType></Parameter>
  <Parameter><Name>TAX_UNIT</Name>
    <Value><![CDATA[tu_sben_family_sl]]></Value>
    <ValueType>taxunit</ValueType></Parameter>
</Function>
```

## Elig

Evaluates a condition per person, sets eligibility variable (default: `sel_s`) to 0 or 1.

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `elig_cond` | Yes | Condition expression |
| `TAX_UNIT` | Yes | Assessment unit |
| `output_var` | No | Output variable (default: `sel_s`) |

**Unlike other functions**, Elig sets output individually for each person (not just the head).

**Condition syntax:** `dag < 3`, `yem >= 1000#m`, `&` (AND), `|` (OR), `!` (NOT), queries (`IsDepChild`, `IsHeadOfTu`, `IsMarried`, `nDepChildrenInTu > 2`).

**Interaction with subsequent functions** via `who_must_be_elig`:
- `one` — at least one member eligible
- `one_adult` — at least one adult eligible
- `all` — all members eligible
- `all_adults` — all adults eligible
- `nobody` (default) — ignore eligibility

## BenCalc

Benefit calculator with components and withdrawal (tapering).

**Core formula:**
```
result = Σ(comp_i_perTU if comp_i_cond) OR Σ(comp_i_perElig × nElig if comp_i_cond)
tapered = result - max(withdraw_base - withdraw_start, 0) × withdraw_rate
```

**Parameters:**

| Parameter | Group | Description |
|-----------|-------|-------------|
| `comp_cond` | i | Condition for component i |
| `comp_perTU` | i | Amount per unit if condition met |
| `comp_perElig` | i | Amount per eligible person if condition met |
| `base` | — | Base amount (referenced as `$base` in components) |
| `withdraw_base` | — | Income base for withdrawal |
| `withdraw_rate` | — | Taper rate |
| `withdraw_start` | — | Threshold before withdrawal begins |
| `withdraw_end` | — | Income at which benefit = 0 |
| `output_var` | — | Output variable |
| `TAX_UNIT` | — | Assessment unit |

**XML example** (social assistance with role-based components and withdrawal):
```xml
<Function>
  <Name>BenCalc</Name>
  <Switch>on</Switch>
  <!-- Component 1: Head -->
  <Parameter><Name>comp_Cond</Name>
    <Value><![CDATA[IsHeadOfTu]]></Value>
    <ValueType>condition</ValueType><Group>1</Group></Parameter>
  <Parameter><Name>comp_perElig</Name>
    <Value><![CDATA[$bsa_head_amt]]></Value>
    <ValueType>formula</ValueType><Group>1</Group></Parameter>
  <!-- Component 2: Dependent children -->
  <Parameter><Name>comp_Cond</Name>
    <Value><![CDATA[!IsHeadOfTu & IsDepChild]]></Value>
    <ValueType>condition</ValueType><Group>2</Group></Parameter>
  <Parameter><Name>comp_perElig</Name>
    <Value><![CDATA[$bsa_depchild_amt]]></Value>
    <ValueType>formula</ValueType><Group>2</Group></Parameter>
  <!-- Withdrawal -->
  <Parameter><Name>Withdraw_Base</Name>
    <Value><![CDATA[il_bsa_base]]></Value></Parameter>
  <Parameter><Name>Withdraw_Rate</Name>
    <Value><![CDATA[$bsa_withdraw_rate]]></Value></Parameter>
  <Parameter><Name>output_var</Name>
    <Value><![CDATA[bsa_s]]></Value></Parameter>
  <Parameter><Name>TAX_UNIT</Name>
    <Value><![CDATA[tu_household_sl]]></Value></Parameter>
</Function>
```

## SchedCalc

Banded rate schedule calculator (tax brackets). Income is divided into bands, each with its own rate or fixed amount.

**Parameters:**

| Parameter | Group | Description |
|-----------|-------|-------------|
| `base` | — | Income to apply schedule to |
| `band_lowLim` | i | Lower limit of band i |
| `band_upLim` | i | Upper limit of band i |
| `band_rate` | i | Rate for band i |
| `band_amount` | i | Fixed amount for band i (alternative to rate) |
| `quotient` | — | Divisor for joint taxation |
| `simple_prog` | — | If `yes`, highest-reached band rate applies to all income |
| `baseThreshold` | — | Below this → result = 0 |
| `output_var` | — | Output variable |
| `TAX_UNIT` | — | Assessment unit |

**XML example** (flat rate above threshold):
```xml
<Function>
  <Name>SchedCalc</Name>
  <Switch>on</Switch>
  <Parameter><Name>base</Name>
    <Value><![CDATA[il_TaxableY]]></Value></Parameter>
  <Parameter><Name>band_lowLim</Name>
    <Value><![CDATA[$tin_lowthres1]]></Value><Group>1</Group></Parameter>
  <Parameter><Name>band_rate</Name>
    <Value><![CDATA[$tin_rate1]]></Value><Group>1</Group></Parameter>
  <Parameter><Name>output_var</Name>
    <Value><![CDATA[tin_s]]></Value></Parameter>
  <Parameter><Name>TAX_UNIT</Name>
    <Value><![CDATA[tu_individual_sl]]></Value></Parameter>
</Function>
```

**Multi-band example:**
```
Band 1: 0–5,000#y → 0%  |  Band 2: 5,000–50,000 → 25%  |  Band 3: 50,000+ → 50%
Income 60,000 → 0 + 11,250 + 5,000 = 16,250
```

## DefIl

Define an income list as the sum/difference of variables and other income lists.

```xml
<Function>
  <Name>DefIl</Name>
  <Parameter><Name>name</Name><Value><![CDATA[il_TaxableY]]></Value></Parameter>
  <Parameter><Name>ils_origy</Name><Value><![CDATA[+]]></Value></Parameter>
  <Parameter><Name>bch_s</Name><Value><![CDATA[+]]></Value></Parameter>
  <Parameter><Name>ils_sicee</Name><Value><![CDATA[-]]></Value></Parameter>
  <Parameter><Name>ils_sicse</Name><Value><![CDATA[-]]></Value></Parameter>
</Function>
```

Means: `il_TaxableY = ils_origy + bch_s - ils_sicee - ils_sicse`

## DefConst

Define named constants referenced with `$` prefix.

```xml
<Function>
  <Name>DefConst</Name>
  <Parameter><Name>name</Name><Value><![CDATA[$tscer_rate1]]></Value></Parameter>
  <Parameter><Name>$tscer_rate1</Name><Value><![CDATA[0.1]]></Value></Parameter>
</Function>
```

Now `$tscer_rate1` = 0.1 (10%) in subsequent formulas.

## DefTu

Define tax/assessment units.

| Parameter | Description |
|-----------|-------------|
| `name` | Unit name (e.g., `tu_household_sl`) |
| `type` | `IND` (individual), `HH` (whole household), `SUBGROUP` (family subset) |
| `Members` | For SUBGROUP: who to include (e.g., `Partner & OwnDepChild`) |
| `DepChildCond` | Condition defining dependent children |
| `HeadDefInc` | Income concept for determining head |
| `LoneParentCond` | Lone parent identification condition |

## Uprate

Adjust monetary values for inflation between data year and policy year.

| Parameter | Description |
|-----------|-------------|
| `dataset` | Which dataset this applies to |
| `def_factor` | Default factor for all monetary variables |
| `{variable}` | Specific factor for a variable (e.g., `yem` → `1.015`) |
| `factor_name`/`factor_value` | Named factors referenced by variables |
| `Factor_Condition` | Conditional uprating (e.g., by region) |

## DefOutput

Specify output file contents.

| Parameter | Description |
|-----------|-------------|
| `file` | Output filename |
| `var` | Individual variable to include |
| `il`/`ILGroup` | Income lists or wildcards (`ils_*`, `il_*`) |
| `varGroup` | Variable group wildcard (`y*`) |
| `nDecimals` | Decimal precision |
| `TAX_UNIT` | Output aggregation level |

## Allocate

Redistribute amounts between unit members.

| Parameter | Description |
|-----------|-------------|
| `share` | Variable/income list to redistribute |
| `share_between` | Condition for recipients |
| `share_prop` | Proportional distribution variable |
| `output_var` | Output variable |

## Loop / UnitLoop

`Loop` repeats a range of policies N times. `UnitLoop` repeats for each eligible unit.

**Loop parameters:** `nIterations`, `First_Pol`/`Last_Pol`, `BreakCond`, `Loop_Id`.

## Store / Restore

`Store` saves variable values; `Restore` retrieves them. Essential for resetting state between loop iterations.

## Other Functions

| Function | Purpose |
|----------|---------|
| `ChangeParam` | Modify parameter values at runtime |
| `Totals` | Population aggregates (sums, means, medians) |
| `DropUnit` / `KeepUnit` | Filter units by condition |
| `IlArithOp` | Operations on income list components |
| `Scale` | Scale variables by a factor |
| `AddHHMembers` | Add synthetic household members |
| `Break` | Stop execution at that point |
| `CallProgramme` | Call external application |
| `RandSeed` | Set random number seed |
