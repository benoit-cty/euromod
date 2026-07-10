# XML Schema & Structure Reference

## Table of Contents
- [XML Schema \& Structure Reference](#xml-schema--structure-reference)
  - [Table of Contents](#table-of-contents)
  - [Namespace](#namespace)
  - [Key Attributes](#key-attributes)
  - [Annotated Minimal XML](#annotated-minimal-xml)
  - [Switch Mechanism](#switch-mechanism)
  - [Policy Inheritance (ReferencePolID)](#policy-inheritance-referencepolid)
  - [run\_cond Parameter](#run_cond-parameter)
  - [Multi-System Files](#multi-system-files)
  - [Footnote Parameters](#footnote-parameters)
  - [External Statistics](#external-statistics)
  - [V4 Format: Self-Contained Systems](#v4-format-self-contained-systems)
    - [V4→V3 Translation](#v4v3-translation)
    - [Cache Files](#cache-files)
    - [Order Numbering Rules](#order-numbering-rules)
    - [Execution-Order-Aware Insertion](#execution-order-aware-insertion)

## Namespace

```xml
<CountryConfig xmlns="http://euromod.com/CountryConfig.xsd">
```

DataConfig uses `http://euromod.com/DataConfig.xsd`, VarConfig uses `http://euromod.com/VarConfig.xsd`.

## Key Attributes

| Attribute | Purpose |
|---|---|
| `ID` | GUID (32-hex) — unique cross-reference identifier |
| `Name` | Human-readable name |
| `Order` | Execution sequence (lower = earlier) |
| `Switch` | `on` / `off` / `n/a` |
| `Type` | Policy category: `def`, `sic`, `ben`, `tax` |
| `ValueType` | How to interpret the value: `string`, `formula`, `condition`, `variable`, `taxunit`, `categorical` |
| `Group` | Groups related parameters (e.g., bands in SchedCalc, components in BenCalc) |
| `ReferencePolID` | Links to another policy for inheritance |
| `Comment` | Descriptive text (often in CDATA) |
| `SystemID` | Links a policy to its parent system |
| `FunctionID` | Links a parameter to its parent function |
| `PolicyID` | Links a function to its parent policy |

## Annotated Minimal XML

```xml
<CountryConfig xmlns="http://euromod.com/CountryConfig.xsd">
  <Country>
    <ID>7D856D7D-500A-423D-BA8A-205B0AD159CB</ID>
    <Name>Simpleland</Name>
    <ShortName>sl</ShortName>

    <System>
      <ID>F7E5CACE-CECC-4BB6-9841-A936D0975481</ID>
      <Name>SL_1996</Name>
      <Year>1996</Year>
      <CurrencyOutput>euro</CurrencyOutput>
      <CurrencyParam>euro</CurrencyParam>
      <HeadDefInc>ils_origy</HeadDefInc>
      <Order>1</Order>

      <Policy>
        <ID>04C1DA51-4F68-42A5-8C0A-7CD6103F486B</ID>
        <Name>Uprate_sl</Name>
        <Type>def</Type>
        <Order>1</Order>
        <Switch>on</Switch>

        <Function>
          <ID>053D4698-8878-4D80-95BF-4F40C763BC4C</ID>
          <Name>Uprate</Name>
          <Order>1</Order>
          <Switch>on</Switch>

          <Parameter>
            <ID>A7AEEA78-E3BB-4D21-8AC4-31F07A782BF1</ID>
            <Name>dataset</Name>
            <Value><![CDATA[sl_demo_v4]]></Value>
            <Order>1</Order>
            <ValueType>string</ValueType>
            <Group />
          </Parameter>
        </Function>
      </Policy>
    </System>
  </Country>
</CountryConfig>
```

## Switch Mechanism

Operates at two levels:

- **Policy switch**: Enables/disables an entire policy for a system
- **Function switch**: Enables/disables individual functions within a policy

Values: `on` (executed), `off` (skipped), `n/a` (not applicable to this system — treated as off).

## Policy Inheritance (ReferencePolID)

When `<ReferencePolID>` is set, the policy inherits its structure from the referenced policy. Only changed parameters need new values. This enables year-to-year policy evolution across systems.

## run_cond Parameter

A global condition for whether a function runs at all (unlike `Elig` which is per-household). If `run_cond` evaluates to false, the function is entirely skipped.

**Critical restriction:** `Run_Cond` only accepts **global variables** — variables that have the same value for all persons/households. Examples: `IsUsedDatabase#99`, dataset flags. Using per-unit variables like `nDepChildrenInTu`, `IsMarried`, `dag`, etc. produces the warning: *"condition must use global variables only"*.

To conditionally execute a function based on household or person-level variables, use an `Elig` function immediately before the target function, then set `who_must_be_elig` on the target function. See the Elig→SchedCalc pattern in SKILL.md.

## Multi-System Files

Real country files contain one `<System>` per policy year. Parameter values differ between systems to capture policy changes over time. In the EUROMOD GUI, systems appear as columns; in XML, they are parallel `<System>` elements.

## Footnote Parameters

Operands in formulas can be further specified using footnote notation:

```
formula: yem#1 * 0.1 + yse#2 * 0.15
#_uplim (Group 1): 20000#y       ← upper limit for yem
#_uplim (Group 2): 30000#y       ← upper limit for yse
#_level (Group 1): tu_family_sl  ← evaluate yem at family level
```

## External Statistics

`<ExternalStatistic>` elements at the end of country XML files store validation data (inequality measures, poverty rates, aggregate totals). These are reference values only — they don't affect simulation.

## V4 Format: Self-Contained Systems

In V4 format (the current standard under `XMLParam/Countries/`), each `<System>` block is **self-contained**: every Policy, Function, and Parameter has its own unique `<ID>`, `<Switch>`, and `<Value>` within each system. The same logical function (e.g., "income tax schedule") appears once per system with different IDs but matching `<Order>` and `<Name>`.

This differs from the V3 format (under `EM3Translation/XMLParam/Countries/`) where functions and parameters are defined once, and separate `SYS_FUN` / `SYS_PAR` cross-reference tables map `SystemID → FunctionID → Switch` and `SystemID → ParameterID → Value`.

### V4→V3 Translation

The EUROMOD engine (including the Stata connector) reads the V3 format. A built-in translator converts V4→V3 automatically, caching the result. The translator:

1. Creates one `<FUN>` definition per unique function (matched across systems by `<Order>` within the same policy)
2. Creates `<SYS_FUN>` entries mapping each SystemID to each FunctionID (providing the Switch value)
3. Creates `<SYS_PAR>` entries mapping each SystemID to each ParameterID (providing the Value)

**If a function exists in only one system**, the translator cannot create the cross-reference entries and silently drops it. The engine then reports "Failed to assign parameter" for every parameter in those functions.

### Cache Files

After modifying V4 XML, delete these cache files to force regeneration:

| File | Location |
|------|----------|
| `up2Date_{CC}` | `EM3Translation/XMLParam/Countries/{CC}/` |
| `up2Date_{CC}_DataConfig` | `EM3Translation/XMLParam/Countries/{CC}/` |
| `astmp_{CC}.xml` | `XMLParam/Temp/` |

### Order Numbering Rules

Within a policy, `<Order>` values determine execution sequence. When inserting new functions:

- Orders must be **contiguous** with the existing range. If the policy's existing functions use Orders 0–77, new functions should start at 78.
- Large gaps (e.g., jumping to 500) or collisions with existing Orders cause "Failed to assign parameter" warnings.
- The Order is a policy-local sequence number — it's independent of other policies.
- In the EUROMOD log, orders appear as `PolicyOrder·FunctionOrder·ParameterOrder` (e.g., `35·78·0` = Policy 35, Function 78, Parameter 0).

### Execution-Order-Aware Insertion

**This is the most common source of silent reform bugs.** When a reform function writes to the same `output_var` as an existing function (e.g., a new SchedCalc that overwrites `tin_s`), it must be inserted **immediately after** the original — not appended at the end of the policy.

Functions within a policy execute strictly by Order. Downstream functions consume intermediate results. If a reform function is appended at the end, it overwrites a variable *after* all downstream logic has already used the original value. The result: intermediate variables change but final aggregates like `ils_dispy` remain completely unchanged — a silent bug with no errors or warnings.

**Example — extending Simpleland's `tin_sl` with a family tax credit:**

```
Order 0: DefConst  → $tin_rate1, $tin_lowthres1, $tin_credit
Order 1: SchedCalc → tin_s  (base tax: 20% above 1000#m on il_TaxableY)
Order 2: Elig      → families with children
Order 3: ArithOp   → tin_s = tin_s - $tin_credit  (reduce tax for families)
```

A reform SchedCalc (e.g., lower rate to 15%) must go right after Order 1 — NOT appended at Order 4. At Order 4, the new SchedCalc overwrites `tin_s` after the family credit at Order 3 already reduced it, so families lose their credit and `ils_dispy` does not reflect the reform correctly.

In real country files (e.g., `tin_mt` with 78 functions), the dependency chain is longer — multiple SchedCalc variants feed into a BenCalc optimization, followed by rebates and credits — but the principle is identical: always insert immediately after the function being replaced.

**Renumbering technique for mid-policy insertion:**

1. Multiply ALL existing Orders by 100 (0→0, 1→100, 2→200, 3→300)
2. Insert new functions in the created gaps (e.g., 110 for right after Order 1→100)
3. Apply to ALL systems to maintain cross-system Order consistency

This preserves relative execution order while creating room for precise insertion.
