---
name: euromod-xml
description: Read, navigate, and modify EUROMOD tax-benefit microsimulation model XML files. Use when working with EUROMOD country policy XML files ({CC}.xml), DataConfig files ({CC}_DataConfig.xml), VARCONFIG.xml, or any XML file under an XMLParam/ directory. Also use when the user asks about the EUROMOD policy spine of any EU country.
---

# EUROMOD XML

EUROMOD is the EU's tax-benefit microsimulation model. Policy rules are stored as XML files under `XMLParam/Countries/{CC}/{CC}.xml`. This skill provides the domain-specific knowledge needed to read, interpret, and modify these files. You can learn about EUROMOD here: https://euromod-web.jrc.ec.europa.eu/.

For in-depth documentation on any function or feature, the built-in help file is available at `C:\Program Files\EUROMOD\Help\EUROMODHelp.chm`. It can be extracted with 7-Zip to `C:\Temp\euromod_help\` and the resulting `.htm` files read directly (e.g. `EM_FC_BenCalc.htm`, `EM_FC_SchedCalc.htm`, etc.).

## File Navigation

| Looking for... | Path |
|---|---|
| Country policy rules | `XMLParam/Countries/{CC}/{CC}.xml` |
| Dataset-system linkage | `XMLParam/Countries/{CC}/{CC}_DataConfig.xml` |
| Variable acronym lookup | `XMLParam/Config/VARCONFIG.xml` (20 MB — grep, don't load fully) |
| Add-on modules | `XMLParam/AddOns/{AddOn}/{AddOn}.xml` |

Country XML files are 28–116 MB. Use grep to find specific policies, functions, or constants rather than reading entire files.

## Core Hierarchy

```
CountryConfig (namespace: http://euromod.com/CountryConfig.xsd)
└── Country (Name, ShortName, ID)
    └── System (one per policy year, e.g., SL_1996)
        └── Policy (one per tax/benefit, e.g., tin_sl)
            └── Function (e.g., SchedCalc, BenCalc, Elig)
                └── Parameter (e.g., band_rate, output_var)
```

Every entity has a GUID `<ID>`, an `<Order>` (execution sequence), and a `<Switch>` (`on`/`off`/`n/a`).

### Programmatic Parsing (Python)

All EUROMOD XML uses the namespace `http://euromod.com/CountryConfig.xsd`. When parsing with lxml or ElementTree, **every tag lookup must include the namespace prefix**:

```python
from lxml import etree
NS = "{http://euromod.com/CountryConfig.xsd}"
tree = etree.parse("MT.xml")
for system in tree.iter(f"{NS}System"):
    name = system.find(f"{NS}Name").text
```

Without the `{NS}` prefix, `find()` / `iter()` silently return nothing.

> **CRITICAL — Properties are child elements, never XML attributes.**
> Every `<Policy>`, `<Function>`, and `<Parameter>` stores its name, order, switch, and all other properties as **child elements**, e.g.:
> ```xml
> <Policy>
>   <Name>tin_dk</Name>
>   <Order>32</Order>
>   <Switch>on</Switch>
> </Policy>
> ```
> Never use `.get("Name")` or `.attrib["Order"]` — they will always return `None`/`KeyError`. Always use `.find(f"{NS}Name").text`.

> **CRITICAL — Policies are children of their System element, not global.**
> The tree is `Country → System → Policy → Function → Parameter`. To get policies for a specific system, always call `sys_el.findall(f"{NS}Policy")` on the system element. Never use `tree.findall(f".//{NS}Policy")` — that returns policies from **all** systems mixed together.

## Policy Spine Execution

Policies execute sequentially by `Order`. Typical order:

1. `Uprate_{cc}` — adjust data to policy year
2. `ILsDef_{cc}` — standard income list definitions
3. `tudef_{cc}` — tax unit definitions
4. `ILDef_{cc}` — country-specific income lists
5. SIC policies (`sic_{cc}`) — social insurance contributions
6. Benefit policies (`ben` type) — child benefit, unemployment, etc.
7. Tax policies (`tax` type) — income tax
8. Means-tested benefits — social assistance (depends on taxes)
9. `output_std_{cc}` — output definition

## Private Components

Every `System`, `Policy`, `Function`, `Parameter`, and `DataBase` element may carry a `<Private>` child. The semantics:

| XML | Meaning |
|---|---|
| element absent | **not** private |
| `<Private />` (empty) | **not** private |
| `<Private>no</Private>` | **not** private |
| `<Private>yes</Private>` | **private** |

Only the explicit text `yes` marks an element as private. Empty tags and absent elements are both treated as not-private.

```python
def is_private(el, ns):
    """Return True only if <Private>yes</Private>."""
    priv = el.find(f"{ns}Private")
    return priv is not None and (priv.text or "").strip().lower() == "yes"
```

> **Connector limitation:** The Python `euromod` connector exposes `.private` only on `Dataset` objects. Detecting private `Policy`, `Function`, and `Parameter` entries requires lxml parsing of `{CC}.xml` directly.

### Row Numbers (Positional Rank)

The EUROMOD UI displays row numbers as `pol_n.func_n.par_n` — **1-based positional ranks** after sorting all siblings by their `<Order>` integer, not the raw Order values. A policy with `<Order>25</Order>` may display as row `6` if it is 6th when sorted.

Three precision levels:
- **Policy level** (`pol_n`, e.g., `6`) — identifies the policy
- **Function level** (`pol_n.func_n`, e.g., `6.2`) — identifies the function within a policy
- **Parameter level** (`pol_n.func_n.par_n`, e.g., `6.2.1`) — highest precision; identifies an individual parameter

Always use the **deepest applicable level**: parameter level for individual parameters, function level for structural changes, policy level only when no deeper anchor exists (e.g., when a policy is entirely new).

To build a complete row-number lookup from a system element `sys_el`, use [scripts/build_param_row_index.py](scripts/build_param_row_index.py). Always build from the **most-recent-year** system (highest `<Year>` integer).

## Key Naming Conventions

| Pattern | Example | Meaning |
|---|---|---|
| `{var}_s` | `bch_s` | Simulated by model |
| `${name}` | `$tin_rate1` | Constant (DefConst) |
| `ils_{name}` | `ils_dispy` | Standard income list (all countries) |
| `il_{name}` | `il_TaxableY` | Country-specific income list |
| `tu_{name}_{cc}` | `tu_household_mt` | Tax unit |

Variable prefixes: `y`=income, `b`=benefit, `t`=tax, `p`=pension, `d`=demographic, `x`=expenditure, `l`=labour, `id`=identifiers.

Period suffixes: `#m`=monthly (internal), `#y`=yearly, `#q`=quarterly, `#w`=weekly.

## Function Types (Quick Reference)

**Definition:** `Uprate`, `DefIl`, `DefConst`, `DefVar`, `DefTu`, `SetDefault`, `DefOutput`

**Calculation:** `ArithOp` (arithmetic), `Elig` (eligibility → sel_s), `BenCalc` (benefit with components/withdrawal), `SchedCalc` (banded rate schedule), `Allocate`, `Min`, `Max`

**Advanced:** `Loop`, `UnitLoop`, `Store`, `Restore`, `ChangeParam`, `Totals`

For detailed function parameters and XML examples, see [references/functions.md](references/functions.md).

## Essential Formulas & Patterns

**Disposable income:** `ils_dispy = ils_origy + ils_ben - ils_tax - ils_sicdy`

**Result assignment:** Results go to the **head** of the tax unit. Other members get 0 (for `output_var`) or keep their value (for `output_add_var`). Exception: `Elig` sets values per-person.

**`output_var` vs `output_add_var`:**  `output_var` overwrites all values (even for non eligible observations), `output_add_var` accumulates, modifying only eligible observations.

**Groups:** Related parameters share a `<Group>` number (e.g., band 1, band 2 in SchedCalc; component 1, component 2 in BenCalc).

## Extensions

For extension types, `BaseOff` semantics, `Extension_Policy`/`Extension_Function`/`Extension_Parameter` structure, and the `country_uses_extension()` helper, see [references/extensions.md](references/extensions.md).

## XML Search Patterns

```bash
# Find all policies in a country file
grep '<Name>.*_{cc}</Name>' {CC}.xml

# Find a specific function type
grep '<Name>SchedCalc</Name>' {CC}.xml

# Find a constant definition
grep '\$tin_rate' {CC}.xml

# Find income list definitions
grep '<Name>DefIl</Name>' {CC}.xml
```

## XML Editing Patterns

**Order numbering:** New functions should use the next sequential Order after the existing maximum in the policy (e.g., if max is 77, start at 78). Do NOT use large jumps (e.g., 500, 2000) — the engine rejects out-of-range Orders. To insert between existing functions, renumber first by multiplying all existing Orders by 100 (e.g., 1→100, 2→200) to create uniform gaps.

**Execution-order-aware insertion (critical):** When a reform function writes to the **same output variable** as an existing function (e.g., a new SchedCalc that overwrites `tin_s`), it must be placed **immediately after** the function it replaces — not appended at the end of the policy. Functions within a policy execute in Order sequence, and downstream functions depend on intermediate results. Appending at the end means the reform overwrites a value *after* all downstream logic has already consumed the original, so final aggregates like `ils_dispy` remain unchanged despite the reform producing different intermediate values.

Example: Suppose Simpleland's `tin_sl` is extended with a family tax credit:
- Order 0: DefConst → `$tin_rate1`, `$tin_lowthres1`, `$tin_credit`
- Order 1: SchedCalc → `tin_s` (base tax: 20% above 1000#m on `il_TaxableY`)
- Order 2: Elig → families with children
- Order 3: ArithOp → `tin_s = tin_s - $tin_credit` (reduce tax for families)

A reform SchedCalc (e.g., lowering the rate to 15%) must go right after Order 1 — NOT appended at Order 4. At Order 4, the new SchedCalc overwrites `tin_s` *after* the family credit at Order 3 already reduced it, so families lose their credit. The result: `tin_s` changes but `ils_dispy` does not reflect the intended reform correctly — a silent bug with 0 errors and 0 warnings. Use the ×100 renumbering technique to create insertion gaps when needed.

**Mutually exclusive branches:** When adding conditional paths (e.g., different tax schedules by number of children), use an `Elig` → `SchedCalc` pair per branch. The Elig evaluates the condition; the SchedCalc uses `who_must_be_elig=one`. For overwriting output variables, all branches can use `output_var` because only the last eligible branch's result persists. Do NOT use `Run_Cond` for per-unit conditions — it only accepts global variables.

**New element IDs:** Generate fresh GUIDs for every new `<ID>`. Each system must have its own unique IDs — never reuse an ID across systems. Ensure `FunctionID` points to the parent function's ID, and `PolicyID` points to the parent policy's ID.

**n/a stubs for non-target systems:** When inserting new functions into one system (e.g., a reform scenario), mirror the same structure in all other systems with `<Switch>n/a</Switch>` and all `<Value><![CDATA[n/a]]></Value>`. Parameter count, Names, and Orders must match exactly. See the "V4 Multi-System Editing" section.

## V4 Multi-System Editing (Critical)

In V4 format, each `<System>` is self-contained: the same logical function (e.g., "income tax SchedCalc") has a **different `<ID>` in each system** but the same `<Order>` and `<Name>`. When inserting new functions:

1. **Insert into ALL systems, not just the target.** The EUROMOD engine uses a V4→V3 translator that creates cross-reference tables (`SYS_FUN`, `SYS_PAR`) mapping each system to each function. If a function exists in only one system, the translator silently drops it, causing "Failed to assign parameter" warnings at runtime.

2. **For non-target systems, use `n/a` stubs:** set `<Switch>n/a</Switch>` and all `<Value><![CDATA[n/a]]></Value>`. The function structure (Name, Order, parameter Names, parameter count) must mirror the active version exactly.

3. **Use contiguous Order numbers.** New functions must use the next sequential Order after the existing maximum within the policy. Gaps or out-of-range Orders (e.g., jumping from 77 to 500) cause "Failed to assign parameter" warnings for every parameter in those functions.

4. **Clear the EM3Translation cache** after modifying V4 XML: delete `EM3Translation/XMLParam/Countries/{CC}/up2Date_{CC}` and `up2Date_{CC}_DataConfig`. Also delete `XMLParam/Temp/astmp_{CC}.xml`. These force the engine to regenerate the V3 translation from the updated V4 source.

### Editing Checklist

```
□ Map the policy's execution flow — identify which functions write to which output variables
□ Determine correct insertion point (immediately after the function the reform replaces/extends)
□ If inserting between existing functions, renumber all Orders ×100 to create gaps
□ Assign new Orders at the correct position (NOT just max+1 if that's the wrong execution point)
□ Generate unique IDs per system (different GUIDs for each system's copy)
□ Insert active functions into target system (Switch=on, real values)
□ Insert n/a stubs into all other systems (Switch=n/a, all values=n/a)
□ Delete EM3Translation cache files (up2Date_{CC}, astmp_{CC}.xml)
□ Run EUROMOD and verify 0 errors + 0 warnings
□ Compare baseline vs reform — verify that downstream aggregates (ils_dispy) reflect the change
```

## System Cloning

Cloning a system (e.g. `SE_2025` → `SE_2026`) requires consistent updates across four areas of `{CC}.xml` plus `{CC}_DataConfig.xml`.

### 1. GUID Regeneration

Every `<ID>` element at System, Policy, Function, and Parameter level must be replaced with a fresh UUID. Back-references scattered throughout must also be updated using an `old→new` map:

| Element | Back-reference fields to update |
|---|---|
| Policy | `<SystemID>`, `<ReferencePolID>` |
| Function | `<PolicyID>` |
| Parameter | `<FunctionID>`, and `<Value>` when it holds a UUID (e.g. `ChangeParam/Param_Id`) |

### 2. Root-level flat records

`<Extension_Policy>` / `<Extension_Function>` and `<ConditionalFormat>` are root-level elements (not inside any `<System>`). All three must be handled during cloning:

- **Extension_Policy / Extension_Function**: iterate all root-level records; for each whose `PolicyID`/`FunctionID` is in the old→new map, append a copy with the new ID.
- **ConditionalFormat**: pairs a system with a benchmark for the UI's compare view. Add a record with `<SystemName>` = new system, `<BaseSystemName>` = source system. Remove any stale record with the same `<SystemName>` first (idempotent).

```xml
<ConditionalFormat>
  <SystemName>SE_2026</SystemName>
  <BaseSystemName>SE_2025</BaseSystemName>
</ConditionalFormat>
```

### 3. DataConfig (`{CC}_DataConfig.xml`)

For every `<DataBase>` that contains a `<DBSystemConfig>` block for the source system, insert a copy with `<SystemName>` and all `<SystemID>` elements updated to the new system's UUID. Read from the `.bak` if present to ensure a clean baseline.

### 4. DefOutput filename renaming (two-pass)

Output filenames embed the system name, often lowercase (e.g. `se_2025_yem_std`). Two passes are needed:

1. **Pass 1 — DefOutput `file` parameters:** Walk all `DefOutput` functions in the clone. For each `file` parameter, do a case-insensitive prefix match and replace `{source_name}_{tail}` → `{new_name}_{tail}`. Collect each such parameter's `<ID>` UUID into a set.
2. **Pass 2 — ChangeParam `Param_NewVal`:** Walk all `ChangeParam` functions. If `Param_Id` holds a UUID from the set above, apply the same rename to `Param_NewVal` (match `Param_NewVal` case-insensitively).

### 5. EM3 cache clearing (safe pattern)

Do NOT call `p.exists()` before `p.unlink()` — on OneDrive-synced or network paths, `exists()` can stall indefinitely. Instead:

```python
for p in cache_paths:
    try:
        p.unlink()
    except FileNotFoundError:
        pass
```

### Performance note

With `lxml` installed (`pip install lxml`), a 40 MB country XML (e.g. SE) takes ~5–6 s total per country. Without `lxml`, stdlib `ElementTree` is ~10× slower.

---

## Run_Cond vs Elig (Common Pitfall)

`Run_Cond` is a **function-level** parameter that gates whether a function executes at all. It can **only use global variables** (e.g., `IsUsedDatabase#99`). Using per-unit variables like `nDepChildrenInTu` in `Run_Cond` triggers: *"condition must use global variables only"*.

To conditionally execute a SchedCalc based on household-level variables (e.g., number of children), use an **Elig → SchedCalc pair**:

```
Order N:   Elig      elig_cond = "nDepChildrenInTu=1"    TAX_UNIT = tu_...
Order N+1: SchedCalc  who_must_be_elig = "one"            TAX_UNIT = tu_...
```

The Elig sets `sel_s` per person; the subsequent SchedCalc with `who_must_be_elig=one` only fires for units where at least one member is eligible. This replaces `Run_Cond` for any condition involving tax-unit or person-level variables.

## System Cloning

**Use the ready-made script** `C:\Users\picfide\copilot\Clone systems\clone_system.py` for all cloning tasks — it handles the full pipeline (GUID regeneration, extensions, DataConfig, EM3 cache, DefOutput filenames, HHoT dataset refs, ConditionalFormat, Year). See [references/system-cloning.md](references/system-cloning.md) for its full documentation and the underlying procedures covering:

- Extension_Policy / Extension_Function table replication
- Deep-copying systems: two-pass GUID replacement, back-reference fixing (`ReferencePolID`, bare-UUID `<Value>`)
- Assigning `<Order>` values to cloned systems (k+1, k+2 relative to source)
- ConditionalFormat blocks (UI colour-coded comparison)
- Positional duplicate parameter keys (5-tuple indexing)
- Comparing/diffing two systems; cross-model UUID bridging; replaying changes
- Output filename renaming (two-pass: `DefOutput/file` + `ChangeParam/Param_NewVal`)
- Year alignment (`<Year>` element on cloned system; cross-year cloning supported)
- DataConfig (`{CC}_DataConfig.xml`) updating
- EM3 cache clearing (use `unlink()` directly — `exists()` hangs on OneDrive/network paths)
- lxml vs stdlib ElementTree mixing rules

## Known Hard Limit — Adding DefIl Functions to `ILDef_{cc}`

Attempting to add new `DefIl` functions to `ILDef_{cc}` via XML editing causes EUROMOD to crash with "Index out of range". Confirmed after nine independent attempts across structural variants, namespace/UUID/Extension record/cache explanations, and multiple countries. Root cause: EUROMOD validates a count or registry not stored in CC.xml (likely `Extensions.xml` or a compiled schema).

**Workaround:** add the DefIl manually via the EUROMOD UI, then diff the resulting CC.xml (and all files written by the UI) against the pre-edit state to discover exactly what the UI writes.

## Detailed References

- **XML schema, attributes, inheritance, V4 format, ordering rules:** See [references/xml-schema.md](references/xml-schema.md)
- **All function types with parameters:** See [references/functions.md](references/functions.md)
- **Variable naming, prefixes, income lists:** See [references/variables.md](references/variables.md)
- **Config files (VARCONFIG, HICP, exchange rates, DataConfig):** See [references/config-files.md](references/config-files.md)
- **Simpleland complete walkthrough:** See [references/simpleland-examples.md](references/simpleland-examples.md)
- **System cloning, deep-copy, extensions, diffing, lxml:** See [references/system-cloning.md](references/system-cloning.md)
- **Extension types, BaseOff semantics, country_uses_extension helper:** See [references/extensions.md](references/extensions.md)
- **Row-number index builder:** See [scripts/build_param_row_index.py](scripts/build_param_row_index.py)
