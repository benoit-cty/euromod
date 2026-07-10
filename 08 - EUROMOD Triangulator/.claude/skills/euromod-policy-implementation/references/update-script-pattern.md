# Update Script Pattern

Standard template for `update_{CC}_{YEAR}.py` — the script that applies DefConst parameter changes to a cloned system.

## Structure

```python
"""
update_si_2026.py
Apply DefConst parameter changes to SI_2026 in SI.xml.
Run: python update_si_2026.py
"""
from lxml import etree
import sys

XML_PATH    = r"C:\...\XMLParam\Countries\SI\SI.xml"
SYSTEM_NAME = "SI_2026"
NS          = "{http://euromod.com/CountryConfig.xsd}"

# policy_name -> {param_name -> (old_value, new_value, verified, source)}
CHANGES = {
    "ConstDef_si": {
        "$bsa_minamt":      ("494.09#m", "507.43#m", True,  "Benefits docx"),
        "$PolicyYear":      ("2025",     "2026",     True,  "Internal"),
    },
    "tinta01_si": {
        "$tinta01_BasicDed_coef1": ("19736.99#y", "20832.39#y", True, "Taxes docx"),
    },
    "tin_si": {
        "$tin_uplim1": ("9210.26#y", "9721.43#y", True, "Taxes docx"),
    },
    # ... add all parametric changes
}

def main():
    tree = etree.parse(XML_PATH)
    root = tree.getroot()

    target_sys = None
    for sys_el in root.iter(f"{NS}System"):
        if sys_el.findtext(f"{NS}Name") == SYSTEM_NAME:
            target_sys = sys_el
            break
    if target_sys is None:
        sys.exit(f"System {SYSTEM_NAME!r} not found")

    applied = 0
    warnings = 0
    applied_in_policy = {}  # (policy, param) -> True  -- skip duplicates

    for pol_el in target_sys.findall(f"{NS}Policy"):
        pol_name = pol_el.findtext(f"{NS}Name")
        if pol_name not in CHANGES:
            continue
        pol_changes = CHANGES[pol_name]
        for fun_el in pol_el.findall(f"{NS}Function"):
            if fun_el.findtext(f"{NS}Name") != "DefConst":
                continue
            for par_el in fun_el.findall(f"{NS}Parameter"):
                pname = par_el.findtext(f"{NS}Name")
                if pname not in pol_changes:
                    continue
                key = (pol_name, pname)
                if key in applied_in_policy:
                    continue  # skip duplicate param names
                old_v, new_v, verified, source = pol_changes[pname]
                val_el = par_el.find(f"{NS}Value")
                if val_el is None:
                    continue
                if val_el.text != old_v:
                    print(f"  WARN: {pol_name}/{pname}: expected {old_v!r}, found {val_el.text!r}")
                    warnings += 1
                val_el.text = new_v
                applied_in_policy[key] = True
                applied += 1
                print(f"  OK: {pol_name}/{pname}: {old_v} -> {new_v}")

    print(f"\n{applied}/{sum(len(v) for v in CHANGES.values())} applied, {warnings} warnings")
    tree.write(XML_PATH, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    print("Saved.")

if __name__ == "__main__":
    main()
```

## Key Points

- `old_value` is used only for confirmation; mismatch triggers a warning but still applies the change
- Duplicate `$param_name` within the same policy is handled by `applied_in_policy` — only first occurrence updated
- `verified` flag is for documentation; does not affect execution
- Units matter: `494.09#m` (monthly) ≠ `494.09#y` (yearly) ≠ `494.09` (dimensionless)
- Re-running after a re-clone is safe (idempotent if old_value matches the cloned value)

## Building the CHANGES Dict from map_changes.json

```python
import json
manifest = json.load(open("changes_SI_2026.json"))

for row in manifest:
    if row["type"] != "parametric":
        continue
    for m in row["xml_matches"]:
        if m.get("new_value"):
            print(f'    {m["param"]!r}: ({m["raw_value"]!r}, {m["new_value"]!r}, True, "{row["doc"]}"),')
```

This prints the skeleton entries; verify and fill in any missing new values before using.
