# System Cloning Reference

Full procedures for creating variant systems (reform scenarios, sensitivity variants) and the supporting maintenance tasks.

## Table of Contents
- [clone_system.py — Ready-to-run script](#clone_systempy--ready-to-run-script)
- [Extension Policy/Function Tables](#extension-policyffunction-tables)
- [Deep-Copying Systems](#deep-copying-systems)
- [Ordering Cloned Systems](#ordering-cloned-systems)
- [ConditionalFormat Blocks](#conditionalformat-blocks)
- [Positional Duplicate Parameter Keys](#positional-duplicate-parameter-keys)
- [Comparing Systems / Cross-Model Mapping](#comparing-systems--cross-model-mapping)
- [Output Filename Renaming](#output-filename-renaming)
- [Year Alignment](#year-alignment)
- [DataConfig Updating](#dataconfig-updating)
- [EM3 Cache Clearing](#em3-cache-clearing--avoiding-hangs-on-networkonedrive-paths)
- [lxml vs stdlib ElementTree](#lxml-vs-stdlib-elementtree)

---

## clone_system.py — Ready-to-run script

**Location:** `C:\Users\picfide\copilot\Clone systems\clone_system.py`

A production-ready script that handles the full cloning pipeline for one or more countries in a single run. Use this instead of writing ad-hoc cloning code.

### What it handles automatically

| Step | Detail |
|---|---|
| GUID regeneration | All System / Policy / Function / Parameter `<ID>` elements get fresh UUIDs |
| Back-reference fixing | `SystemID`, `PolicyID`, `FunctionID`, `ReferencePolID`, bare-UUID `<Value>` (ChangeParam/Param_Id) |
| Extension tables | `Extension_Policy` / `Extension_Function` root-level records replicated for new IDs |
| ConditionalFormat | Stale record removed; new record added with source system as benchmark |
| `<Year>` element | Set to the year extracted from `NEW_SUFFIX` (cross-year cloning fully supported) |
| DefOutput filenames | Two-pass rename: `DefOutput/file` params + `ChangeParam/Param_NewVal` overrides |
| HHoT dataset refs | Any `<Value>` equal to `{source_name}_hhot` is renamed to `{new_name}_hhot` |
| DataConfig | `DBSystemConfig` blocks cloned into `{CC}_DataConfig.xml` for all datasets |
| EM3 cache | Translation cache files deleted so EUROMOD UI reloads fresh XML |
| Backups | `.bak` copies of both XML files created before writing (unless `--no-backup`) |

### CLI usage

```bash
python clone_system.py \
  --euromod-path "C:\path\to\EUROMOD_MODEL" \
  --countries "SI" \
  --source-suffix 2025 \
  --new-suffix 2026 \
  --overwrite
```

Multiple countries: `--countries "AT BE SI SK"`. Suffix can include a variant tag: `--source-suffix 2025_TE --new-suffix 2026_TE`.

### SETTINGS block (alternative to CLI)

Edit the block near the top of the script for interactive/notebook use:

```python
EUROMOD_PATH        = r"C:\path\to\EUROMOD_MODEL"
COUNTRIES           = "SI"          # space-separated
SOURCE_SUFFIX       = "2025"
NEW_SUFFIX          = "2026"
SKIP_BACKUP         = False
OVERWRITE_IF_EXISTS = True
```

### After cloning: apply parameter changes

The script clones the system with all source-year values intact. Parameter value updates for the new year must be applied separately by editing `<Value>` elements in the cloned system. Pattern:

```python
from lxml import etree
NS = "{http://euromod.com/CountryConfig.xsd}"
tree = etree.parse(xml_path)
root = tree.getroot()

for sys_el in root.iter(f"{NS}System"):
    if sys_el.findtext(f"{NS}Name") == "SI_2026":
        for pol_el in sys_el.findall(f"{NS}Policy"):
            if pol_el.findtext(f"{NS}Name") == "ConstDef_si":
                for fun_el in pol_el.findall(f"{NS}Function"):
                    if fun_el.findtext(f"{NS}Name") == "DefConst":
                        for par_el in fun_el.findall(f"{NS}Parameter"):
                            if par_el.findtext(f"{NS}Name") == "$bsa_minamt":
                                par_el.find(f"{NS}Value").text = "507.43#m"
        break

tree.write(xml_path, encoding="UTF-8", xml_declaration=True)
```

For country-year update scripts, see e.g. `C:\Users\picfide\copilot\SI\update_si_2026.py` (41-parameter SI 2026 update).

---

## Extension Policy/Function Tables

Extension membership (the on/off toggle visible in the EUROMOD UI) is stored in two **flat lookup tables at `CountryConfig` root level**, completely separate from the `System > Policy > Function` hierarchy:

```xml
<Extension_Policy>
  <ExtensionID>557c232a-...</ExtensionID>
  <PolicyID>abc123-...</PolicyID>
  <BaseOff>false</BaseOff>
</Extension_Policy>

<Extension_Function>
  <ExtensionID>557c232a-...</ExtensionID>
  <FunctionID>def456-...</FunctionID>
  <BaseOff>false</BaseOff>
</Extension_Function>
```

Key facts:
- These records are **NOT inside `<System>` elements** — they are direct children of `<CountryConfig>`.
- Extension **names** (e.g. "BTA", "TCA") are in `XMLParam/Config/SWITCHABLEPOLICYCONFIG.xml`. CC.xml only stores `ExtensionID` UUIDs.
- Most functions do NOT have an `Extension_Function` record — only explicitly toggled ones do. That is normal.
- When deep-copying a system, the new policy/function UUIDs are unknown to these root tables — extension switches disappear in the EUROMOD UI for the cloned system.

**Fix — replicate extension records after cloning:**
After assigning fresh UUIDs to a cloned system (returning `pol_id_map` / `func_id_map`), iterate all root-level `Extension_Policy` and `Extension_Function` records. For each record whose ID belongs to the source system, append a new sibling record with the same `ExtensionID` and `BaseOff` but the newly mapped ID:

```python
import copy
NS = "{http://euromod.com/CountryConfig.xsd}"

def replicate_extensions(root, pol_id_map, func_id_map):
    for ep in list(root.iter(f"{NS}Extension_Policy")):
        pid = ep.findtext(f"{NS}PolicyID")
        if pid in pol_id_map:
            clone = copy.deepcopy(ep)
            clone.find(f"{NS}PolicyID").text = pol_id_map[pid]
            ep.addnext(clone)   # lxml; for stdlib ET: parent.insert(idx+1, clone)
    for ef in list(root.iter(f"{NS}Extension_Function")):
        fid = ef.findtext(f"{NS}FunctionID")
        if fid in func_id_map:
            clone = copy.deepcopy(ef)
            clone.find(f"{NS}FunctionID").text = func_id_map[fid]
            ef.addnext(clone)
```

---

## Deep-Copying Systems

When creating a new system as a variant of an existing one (e.g. a reform scenario, a scenario with certain parameters set to zero, a sensitivity variant):

1. **`copy.deepcopy(src_sys)`** — deep-clone the source `<System>` element.
2. **Two-pass ID replacement:**
   - Pass 1: walk every `<Function>` and `<Parameter>` element via `iter()`, generate fresh UUIDs, build `{old_id → new_id}` maps (`pol_id_map` / `func_id_map`), set new IDs in-place.
   - Pass 1 also tracks parameter IDs: for every `<Parameter>` element, store `old_param_id → new_param_id` in the same map. Without this, `ChangeParam` functions whose `<Value>` contains a parameter UUID (the `Param_Id` parameter) keep the source system's UUID and cause "The given key was not present in the dictionary" when the cloned system is later copied in the EUROMOD UI.
   - Pass 2: fix all back-references using the map. Back-reference tags to check: `<SystemID>`, `<PolicyID>`, `<FunctionID>`, **`<ReferencePolID>`** (cross-policy reference used by ChangeParam functions), and bare-UUID `<Value>` elements — in particular `ChangeParam/Param_Id`, whose `<Value>` holds a parameter UUID:
     ```python
     for ref_tag in ("SystemID", "PolicyID", "FunctionID", "ReferencePolID"):
         ref_el = el.find(f"{NS}{ref_tag}")
         if ref_el is not None and ref_el.text and ref_el.text.strip() in id_map:
             ref_el.text = id_map[ref_el.text.strip()]
     # bare-UUID <Value> (e.g. ChangeParam Param_Id)
     val_el = el.find(f"{NS}Value")
     if val_el is not None and val_el.text and val_el.text.strip() in id_map:
         val_el.text = id_map[val_el.text.strip()]
     ```
     Missing `ReferencePolID` or bare-UUID `<Value>` updates leave dangling references to the source system, causing the EUROMOD UI to crash with "The given key was not present in the dictionary" when copying the cloned system.
3. **Set `<Name>`** to the new system name.
4. **Set `<Order>`** (see [Ordering Cloned Systems](#ordering-cloned-systems)) so the system appears correctly in the UI.
5. **Insert position — inside `<Country>`, right after the source system:** in J2.0+ format, all `<System>` elements are children of the `<Country>` sub-element of `<CountryConfig>`, **NOT** direct root children. To insert the clone immediately after the source:
   ```python
   country_el = root.find(f"{NS}Country")
   children   = list(country_el)
   src_idx    = children.index(src_sys)
   country_el.insert(src_idx + 1, new_sys)
   ```
   The `Extension_Policy` / `Extension_Function` flat tables remain **direct root children** of `<CountryConfig>` and are never inside `<Country>`. `ConditionalFormat` blocks are also direct root children that appear before `<Country>` in the file.  
   When the code needs an insertion-anchor relative to root (e.g. for ConditionalFormat), search for the first `Extension_Policy`/`Extension_Function` among root's direct children — but do **not** use that anchor for system insertion, which must go into `<Country>`.
6. **Replicate Extension tables** — call `replicate_extensions()` (see [Extension Policy/Function Tables](#extension-policyffunction-tables)).
7. **Apply parameter overrides** to the cloned system.
8. **Add a ConditionalFormat entry** (see [ConditionalFormat Blocks](#conditionalformat-blocks)).
9. Update `{CC}_DataConfig.xml` (see [DataConfig Updating](#dataconfig-updating)).
10. **Set `<Year>`** on the cloned system (see [Year Alignment](#year-alignment)).
11. Return `(new_sys, pol_id_map, func_id_map)`.

**Remove stale copies before re-inserting:** When re-running a script, remove existing variant systems by name first. Search both direct root children AND inside any `<Country>` element one level deep — scripts that inserted systems in the wrong place leave stranded copies that a root-only cleaner will miss, causing duplicates that crash EUROMOD with "Object reference not set".

---

## Year Alignment

When cloning across years (e.g. 2025 → 2026), the `<Year>` child element of the cloned system must be updated to match the new year. The element may be absent in older country files — create it after `<Name>` if so.

```python
def set_system_year(sys_el, new_year, NS):
    """Set or create <Year> on the system element."""
    year_el = sys_el.find(f"{NS}Year")
    if year_el is None:
        name_el = sys_el.find(f"{NS}Name")
        idx = list(sys_el).index(name_el) + 1
        year_el = ET.Element(f"{NS}Year")
        sys_el.insert(idx, year_el)
    year_el.text = str(new_year)
```

Extract the year from the new suffix with `re.match(r'(\d{4})', new_suffix)`. Cross-year cloning is fully supported — there is no same-year restriction.

---

## Ordering Cloned Systems

EUROMOD sorts systems, policies, functions, and parameters by the `<Order>` child element — **not** by document position. All index builders and traversals must sort explicitly:

```python
def _order(el):
    try: return int(el.findtext(f"{NS}Order") or 0)
    except ValueError: return 0

for pol in sorted(system.findall(f"{NS}Policy"), key=_order):
    for func in sorted(pol.findall(f"{NS}Function"), key=_order):
        for param in sorted(func.findall(f"{NS}Parameter"), key=_order):
            ...
```

Row numbers shown in the EUROMOD UI (e.g. `7.3.12`) reflect `<Order>`-sorted position. Using document order in index builders produces mismatched row labels.

**Ordering cloned systems:** when deriving `n` variant systems from a source system with order `k`, assign them `k+1`, `k+2`, … so they appear immediately after the source in the EUROMOD UI list. If there is a logical hierarchy (e.g. a combined-changes system followed by narrower sub-variants), the combined system should receive `k+1` and the sub-variants `k+2`, `k+3`, …

---

## ConditionalFormat Blocks

Colour-coded comparison in the EUROMOD UI is driven by `<ConditionalFormat>` elements stored at the **top** of each `CC.xml`, before any `<System>` elements. One block per (benchmark / displayed) system pair:

```xml
<ConditionalFormat>
  <ID>uuid</ID>
  <BackColor>FFFFC000</BackColor>
  <ForeColor>no special color</ForeColor>
  <Condition />
  <BaseSystemName>CC_2025</BaseSystemName>
  <ConditionalFormat_Systems>
    <ConditionalFormatID>same-uuid-as-ID</ConditionalFormatID>
    <SystemName>CC_2025_reform</SystemName>
  </ConditionalFormat_Systems>
</ConditionalFormat>
```

`<ID>` and `<ConditionalFormatID>` must share the **same** fresh UUID per record.

**Standard practice when creating cloned systems:** every cloned system should have a ConditionalFormat entry that compares it against the system it was cloned from. Add entries programmatically:
1. Remove stale entries targeting the new system names (for idempotent re-runs).
2. Find insertion point: after the last existing `<ConditionalFormat>`. If none exist, fall back to just before the first `Extension_Policy/Function` block — never insert before `<Country>`.
3. Create one entry per new system, using the clone source as `<BaseSystemName>`.
4. Use `_Element`/`_SubElement` factories (see [lxml vs stdlib ElementTree](#lxml-vs-stdlib-elementtree)) to avoid type-mixing errors.

---

## Positional Duplicate Parameter Keys

Multiple `<Parameter>` elements with the **same structural key** `(pol_name, func_name, param_name, group)` can exist within one system. A naïve `dict` stores only the first occurrence — silently wrong for any index builder.

**Fix:** use a 5-tuple key `(pol, func, param, group, n)` where `n` is a 0-based occurrence counter per 4-tuple key. Apply the same counter logic and the same `<Order>`-based sorting consistently across **all** index builders so that `n` values align when cross-referencing indices.

```python
from collections import defaultdict
counters = defaultdict(int)
for pol in sorted(system.findall(f"{NS}Policy"), key=_order):
    pol_name = pol.findtext(f"{NS}Name")
    for func in sorted(pol.findall(f"{NS}Function"), key=_order):
        func_name = func.findtext(f"{NS}Name")
        for param in sorted(func.findall(f"{NS}Parameter"), key=_order):
            param_name = param.findtext(f"{NS}Name")
            group = param.findtext(f"{NS}Group") or ""
            key4  = (pol_name, func_name, param_name, group)
            n     = counters[key4]
            counters[key4] += 1
            index[(pol_name, func_name, param_name, group, n)] = param.findtext(f"{NS}Value")
```

---

## Comparing Systems / Cross-Model Mapping

### Diffing two systems in the same model

Build a value index for each system using the positional 5-tuple key, then compare:

```python
base_idx = build_param_index(base_sys, cc)    # (pol,func,param,grp,n) -> value
scen_idx = build_param_index(scenario_sys, cc)
changes = [(key, base_idx[key], scen_idx[key])
           for key in base_idx if scen_idx.get(key) != base_idx[key]]
```

Skip parameters whose `<Name>` or `<Value>` matches the UUID regex — these are internal EUROMOD cross-references (`Last_Func`, `Last_Policy`, etc.), not policy parameters. Also skip `DefOutput/file` parameters — these are output filename labels, changed mechanically on every system copy, not policy logic.

### Finding the equivalent parameter in a different model version

When parameters have been **renamed or relocated** between model versions, EUROMOD preserves the UUID across the rename. Use the UUID as a cross-model bridge:

1. Build `old_id_index`:  `(pol, func, param, group, n) → UUID`  from the **old model's system** (same skip-logic and `<Order>` sorting as the diff index, so `n` values align).
2. Build `id_to_key_index`:  `UUID → (pol, func, param, group, n)`  from the **new model's same-year system**. The new model's same-year system shares UUIDs with the old model even for renamed parameters.
3. For each changed parameter: look up its UUID in `old_id_index`, then resolve the key in `id_to_key_index`. This gives the correct structural key (with the new name/location) to use when patching the new model.

**Per-system UUID uniqueness:** EUROMOD assigns fresh UUIDs per system. The UUID bridge only works via the **same-year system** in the new model, not cross-year.

**Fallback — same-year value matching:** When a model block has been bulk-rebuilt with all-new UUIDs and new names (e.g. after a policy restructuring), neither name nor UUID matching works. Fallback: build `value → [(param_name, pol, group)]` from the new model's same-year DefConst and match on value. This works reliably when the 2023 values are preserved; only names changed.

### Replaying changes from one model onto another

The diff-and-replay pattern:
1. Discover changes: `diff(old_base_sys, old_scenario_sys)` → list of `(pol, func, param, grp, n, new_val)` tuples.
2. Translate keys to the new model via UUID bridge (see above).
3. Apply translated changes to the cloned system in the new model.

This is more robust than hard-coded parameter lists because it auto-discovers what the scenario actually changed.

---

## Output Filename Renaming

Every cloned system must write its output to a differently named file. `DefOutput/file` parameters in the cloned system must be updated to reflect the new system name. These parameters are **not** policy logic and should be excluded from all diff/classification work.

**Renaming convention:** if the base system outputs `{CC}_{YEAR}_std`, `{CC}_{YEAR}_web`, etc., the cloned system should output `{CC}_{YEAR}_{variant}_std`, `{CC}_{YEAR}_{variant}_web`, etc. All tail variants (`_std`, `_web`, `_admin`, `_Jobcalc`, `_std_parben`, …) should use the same year as the new system, not the source system's year.

**Two-pass approach — `ChangeParam/Param_NewVal` must also be updated:**

`ChangeParam` functions can override a `file` value at runtime via a `Param_NewVal` parameter (resolved via `Param_Id` → the UUID of the `DefOutput/file` parameter). If only `DefOutput/file` is renamed, the `ChangeParam` override reverts the filename to the old name at runtime — a silent error.

- **Pass 1 — `DefOutput/file` parameters:** walk all `DefOutput` functions in the clone; for each `file` parameter, apply case-insensitive rename and collect the parameter's `<ID>` UUID into `defout_file_ids`.
- **Pass 2 — `ChangeParam/Param_NewVal` parameters:** walk all `ChangeParam` functions; if `Param_Id` holds a UUID from `defout_file_ids`, apply the same rename to `Param_NewVal` (match `Param_NewVal` case-insensitively — `Param_Newval` also appears in real files).

**Note on case:** output filenames in `<Value>` are often lowercase (e.g. `se_2025_yem_std`) even though the system name is uppercase (`SE_2025`). Always compare case-insensitively and preserve the tail casing.

```python
def rename_output_files(cloned_sys, base_name, new_name, NS):
    """Two-pass rename: DefOutput/file then ChangeParam/Param_NewVal."""
    defout_file_ids = set()

    # Pass 1 — DefOutput file parameters
    for pol in cloned_sys.iter(f"{NS}Policy"):
        if "output" not in (pol.findtext(f"{NS}Name") or "").lower():
            continue
        for func in pol.iter(f"{NS}Function"):
            if func.findtext(f"{NS}Name") != "DefOutput":
                continue
            for param in func.iter(f"{NS}Parameter"):
                if param.findtext(f"{NS}Name") == "file":
                    val_el = param.find(f"{NS}Value")
                    if val_el is not None and base_name.lower() in (val_el.text or "").lower():
                        # case-insensitive match, preserve tail
                        val_el.text = val_el.text.lower().replace(
                            base_name.lower(), new_name, 1
                        )
                        pid = param.findtext(f"{NS}ID")
                        if pid:
                            defout_file_ids.add(pid.strip())

    # Pass 2 — ChangeParam Param_NewVal overrides
    for func in cloned_sys.iter(f"{NS}Function"):
        if func.findtext(f"{NS}Name") != "ChangeParam":
            continue
        param_id_val = None
        newval_param = None
        for param in func.iter(f"{NS}Parameter"):
            name = (param.findtext(f"{NS}Name") or "").lower()
            if name == "param_id":
                param_id_val = (param.findtext(f"{NS}Value") or "").strip()
            elif name == "param_newval":
                newval_param = param
        if param_id_val in defout_file_ids and newval_param is not None:
            val_el = newval_param.find(f"{NS}Value")
            if val_el is not None and base_name.lower() in (val_el.text or "").lower():
                val_el.text = val_el.text.lower().replace(
                    base_name.lower(), new_name, 1
                )
```

---

## DataConfig Updating

`{CC}_DataConfig.xml` links datasets to systems. When adding cloned systems, each needs a `DBSystemConfig` block. Use an ET tree approach — not regex/text substitution:

```python
import xml.etree.ElementTree as ET, copy

tree = ET.parse(str(dc_path))
root = tree.getroot()

# Remove stale entries for any previously created variants
for db in root.findall(".//DataBase"):
    for sc in list(db.findall("DBSystemConfig")):
        if sc.findtext("SystemName", "") in new_system_names:
            db.remove(sc)

# Clone the base system's DataConfig block for each new variant
base_sc = root.find(f".//DBSystemConfig[SystemName='{source_system_name}']")
parent  = root.find(".//DataBase")
for new_name, new_sys_id in new_systems.items():
    clone = copy.deepcopy(base_sc)
    clone.find("SystemName").text = new_name
    for sid in clone.iter("SystemID"):
        sid.text = new_sys_id
    idx = list(parent).index(base_sc)
    parent.insert(idx + 1, clone)
```

Preserve the original BOM and CRLF line endings when reserialising.

---

## EM3 Cache Clearing — Avoiding Hangs on Network/OneDrive Paths

Deleting the EM3 translation cache files is necessary after modifying V4 XML (see SKILL.md V4 Multi-System Editing section). The correct pattern is to call `unlink()` directly and swallow `FileNotFoundError` — **do not** call `exists()` first.

On paths served by OneDrive sync or temporarily unavailable network drives, `Path.exists()` can stall indefinitely (minutes). The "check then act" pattern must be eliminated entirely:

```python
# WRONG — exists() can hang on OneDrive/network paths
if p.exists():
    p.unlink()

# CORRECT — unlink directly, ignore if absent
try:
    p.unlink()
except FileNotFoundError:
    pass
```

Apply this to all five cache file paths: `up2Date_{CC}`, `up2Date_{CC}_DataConfig` (under `EM3Translation/XMLParam/Countries/{CC}/`), and `astmp_{CC}.xml` (under `XMLParam/Temp/`).

---

## lxml vs stdlib ElementTree

When using both `lxml.etree` and `xml.etree.ElementTree` in the same script:

- **Never mix element types.** Appending a stdlib element into an lxml tree raises `TypeError`. Use module-level factories to prevent accidental mixing:
  ```python
  try:
      from lxml import etree as lET; _HAVE_LXML = True
  except ImportError:
      lET = None; _HAVE_LXML = False

  _Element    = (lambda tag: lET.Element(tag))                    if _HAVE_LXML else ET.Element
  _SubElement = (lambda parent, tag: lET.SubElement(parent, tag)) if _HAVE_LXML else ET.SubElement
  ```
- **Cross-library serialisation bridge** (cloning a stdlib element into an lxml tree):
  ```python
  raw       = ET.tostring(stdlib_element)    # stdlib → bytes
  lxml_copy = lET.fromstring(raw)            # bytes → lxml element
  ```
  Never call `lET.tostring()` on a stdlib element.
- **Windows path**: `lET.parse()` requires a `str`, not a `pathlib.Path`. Use `lET.parse(str(path))`.
- **Performance:** lxml serialises 28–116 MB CC.xml files in < 2 s. stdlib `tree.write()` on a network path can take > 60 s. Use lxml for all write operations.
- **Element truthiness:** `if element:` raises `DeprecationWarning` in stdlib ET. Use `if element is not None`.
