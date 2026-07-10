# Structural Change Patterns

XML patterns for common structural policy changes that cannot be handled by DefConst value updates.

All examples use: `NS = "{http://euromod.com/CountryConfig.xsd}"`

---

## 1. Eligibility Condition Change

**Example:** Income support (bsa_si) — adult-children maintenance obligation abolished in 2026.

Locate the `Elig` function in the relevant policy and modify its `elig_cond` parameter:

```python
from lxml import etree
NS = "{http://euromod.com/CountryConfig.xsd}"
tree = etree.parse(xml_path)
root = tree.getroot()

for sys_el in root.iter(f"{NS}System"):
    if sys_el.findtext(f"{NS}Name") != "SI_2026":
        continue
    for pol_el in sys_el.findall(f"{NS}Policy"):
        if "bsa" not in (pol_el.findtext(f"{NS}Name") or ""):
            continue
        for fun_el in pol_el.findall(f"{NS}Function"):
            if fun_el.findtext(f"{NS}Name") != "Elig":
                continue
            for par_el in fun_el.findall(f"{NS}Parameter"):
                if par_el.findtext(f"{NS}Name") == "elig_cond":
                    old = par_el.find(f"{NS}Value").text
                    # Modify condition here — confirm exact change with user first
                    print(f"Found: {old}")
```

**Checklist before editing:**
- Read the full Elig function (all parameters: `elig_cond`, `who_must_be_elig`, `TAX_UNIT`)
- Understand the logical structure (AND/OR, person vs unit level)
- Confirm the exact condition to remove/add with the user
- Check if multiple Elig functions exist in the same policy (stacked eligibility)

---

## 2. New Benefit Component (BenCalc)

**Example:** Housing supplement — new EUR 0.40/m2 maintenance component added to bho_si.

When a genuinely new calculation line is needed, you must create a new `Function` element.
**Do not attempt without reading the euromod-xml skill first.** The key constraints:

- Every new Function and its Parameters need fresh GUIDs (`str(uuid.uuid4()).upper()`)
- `<Order>` must be set correctly relative to sibling functions
- `<Switch>` defaults to `on`
- Parameters need `<Order>` values within the function

Pattern for a new `BenCalc` line (simplified):

```python
import uuid
from lxml import etree

def new_el(parent, tag, text=None):
    el = etree.SubElement(parent, f"{NS}{tag}")
    if text is not None:
        el.text = text
    return el

# Build the new Function element
fun = etree.Element(f"{NS}Function")
new_el(fun, "ID",     str(uuid.uuid4()).upper())
new_el(fun, "Name",   "BenCalc")
new_el(fun, "Order",  "INSERT_ORDER_HERE")
new_el(fun, "Switch", "on")
# ... add Parameters similarly

# Insert into policy at the right position
pol_el.insert(target_index, fun)
```

Always confirm the new function's logical role and position with the user before inserting.

---

## 3. Benefit Formula Change (fixed amount -> % of MinWage)

**Example:** UE benefit floor/ceiling — changes from fixed EUR to % of MinWage tiers by duration.

This requires either:
- **Option A:** Keeping `BenCalc` but replacing fixed-amount parameters with expressions referencing `$MinWage`
- **Option B:** Adding a new `ArithOp` function that computes the tier-based amount, then referencing its output in `BenCalc`

**Option A is simpler** when EUROMOD supports arithmetic expressions in `<Value>`. Check by looking at existing parameters in the same policy — if you see values like `$MinWage * 0.70`, expressions are in use.

**Option B** is needed when the tier logic requires a `SchedCalc`-style lookup (income duration as input variable, rate as output).

Both options require reading the current `bunct_si` structure in full before proceeding.

---

## 4. Rate Tier Restructuring (SchedCalc)

When bracket limits (`uplim` params) or rates change, these are usually parametric (DefConst update). But when the **number of tiers changes**, new parameters must be added or removed.

**Adding a new tier:**
```python
# Find the last uplim parameter's Order value
# Insert new Parameter elements after it (uplim_N+1, rate_N+1)
# Update Order values of subsequent parameters
```

**Removing a tier:** Set `<Switch>` to `off` on the parameter — never delete parameters from existing systems, as they may be referenced elsewhere.

---

## General Safety Rules

1. **Never edit existing systems** — only the cloned `CC_{t+1}` system
2. **Always make a .bak backup** before any structural edit (clone_system.py does this automatically, but do it again before structural edits)
3. **Use lxml only** — never text/regex replacement on the XML
4. **Confirm before applying** — show the user what will change and wait for approval
5. **Verify with EUROMOD UI** after structural changes — load the model and run the new system to check for errors

---

## 5. Means Test Change

Means-tested benefits use a `Means` function that compares household income (an income list) against a threshold. Changes can affect the threshold value, the income list used, or the treatment of specific income components.

**Threshold change (parametric):** Usually a DefConst update — check `map_changes.py` output first before treating it as structural.

**Income list change (structural):** If the set of income components included in the means test changes, the `DefIl` function for the relevant income list must be modified (add or remove `il_comp` parameters).

**Pattern for threshold lookup:**
```python
for pol_el in sys_el.findall(f"{NS}Policy"):
    if target_policy not in (pol_el.findtext(f"{NS}Name") or ""):
        continue
    for fun_el in pol_el.findall(f"{NS}Function"):
        if fun_el.findtext(f"{NS}Name") != "Means":
            continue
        for par_el in fun_el.findall(f"{NS}Parameter"):
            if par_el.findtext(f"{NS}Name") == "means_limit":
                print(par_el.find(f"{NS}Value").text)
```

**Before editing:** Confirm whether `means_limit` references a `$DefConst` constant or a hardcoded value, and whether the income list (`means_il`) is shared with other policies.
