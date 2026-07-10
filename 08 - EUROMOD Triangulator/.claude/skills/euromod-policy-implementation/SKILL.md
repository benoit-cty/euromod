---
name: euromod-policy-implementation
description: "Implement verified EUROMOD policy changes for year t+1 in a country XML model that currently has systems only up to year t. Use when asked to implement, apply, update, or code verified policy changes into the EUROMOD XML model after policy verification is complete, for example cloning a system, applying parametric DefConst changes, or identifying structural XML edits that require manual work."
---

# EUROMOD Policy Implementation

## Overview

This skill picks up where **euromod-policy-verification** leaves off. Its inputs are:
- Verified policy-parameter docx files (with 2026 column correctly filled in)
- `{CC}_issues_{YEAR}.json` — the verification output (required as a gate)
- `{CC}.xml` — the EUROMOD country model to update

Its output is an updated `{CC}.xml` with a new `{CC}_{t+1}` system containing the correct parameter values.

## Workflow

```
Step 1: Verification gate       check issues JSON — block on unresolved factual issues
     |
Step 2: Clone system            CC_t -> CC_{t+1}  using clone_system.py
     |
Step 3: Map changes             run map_changes.py -> changes_{CC}_{t+1}.html + .json
     |
Step 4: Apply parametric changes  write update_{CC}_{t+1}.py from manifest; run it
     |
Step 5: Review structural changes  flag, describe, defer or implement with user
```

---

## Step 1 — Verification Gate

Before any XML work, check the issues JSON:

```python
import json
data = json.load(open(r"{CC}_issues_{YEAR}.json", encoding="utf-8"))
factual = [i for i in data.get("issues", []) + data.get("cross_doc_issues", [])
           if i.get("severity") == "factual"]
if factual:
    raise SystemExit(f"BLOCKED: {len(factual)} unresolved factual issue(s)")
```

**This is automated** — `map_changes.py` runs this check internally and exits early if blocked.

---

## Step 2 — Clone System

Use `scripts/clone_system.py`. Prefer a local JSON config file or pass CLI args. The SETTINGS block is fallback-only.

Preferred repeated-run pattern:

```json
{
     "euromod_path": "C:\\path\\to\\EUROMOD_MODEL",
     "countries": ["SI"],
     "source_suffix": "2025",
     "new_suffix": "2026",
     "overwrite_if_exists": true
}
```

Save as `clone_system.config.json` in the working directory, then run:

```bash
python clone_system.py --config clone_system.config.json
```

One-off CLI usage:

```bash
python clone_system.py \
  --euromod-path "C:\path\to\EUROMOD_MODEL" \
  --countries "SI" \
  --source-suffix 2025 \
  --new-suffix 2026 \
  --overwrite
```

What it handles automatically: GUID regeneration, Extension tables, ConditionalFormat, Year element, DefOutput filenames (two-pass), HHoT dataset refs (`CC_YYYY_hhot` -> `CC_ZZZZ_hhot`), DataConfig DBSystemConfig blocks, EM3 cache clearing, .bak backups.

**After cloning**: all parameter values are copied from CC_t. Steps 3-4 update them.

---

## Step 3 — Map Changes

Run `scripts/map_changes.py` with a local JSON config file or CLI args. The SETTINGS block is fallback-only.

Preferred repeated-run pattern:

```json
{
     "xml_path": "C:\\path\\to\\XMLParam\\Countries\\SI\\SI.xml",
     "docx_dir": "C:\\path\\to\\SI",
     "country": "SI",
     "base_year": 2025,
     "new_year": 2026,
     "verification_json": "C:\\path\\to\\SI_issues_2026.json",
     "docx_files": {
          "Taxes": "taxes_2025_2026.docx",
          "Benefits": "benefits_2025_2026.docx",
          "Contributions": "contributions_2025_2026.docx",
          "Sickness": "SI_sicknessbenefits_2025_2026.docx",
          "Childcare": "SI_childcarecost_2025_2026.docx"
     }
}
```

Save as `map_changes.config.json` in the working directory, then run:

```bash
python map_changes.py --config map_changes.config.json
```

One-off CLI usage:

```bash
python map_changes.py \
     --xml-path "C:\path\to\XMLParam\Countries\SI\SI.xml" \
     --docx-dir "C:\path\to\SI" \
     --country SI \
     --base-year 2025 \
     --new-year 2026 \
     --verification-json "C:\path\to\SI_issues_2026.json"
```

Output: `changes_{CC}_{YEAR}.html` + `changes_{CC}_{YEAR}.json`.

**Change types in the output:**

| Type | Meaning | Action |
|---|---|---|
| `parametric` | Value changed in DefConst | Handled in Step 4 |
| `structural` | Formula/logic/eligibility change | Manual — see Step 5 |
| `label_only` | Year label update only | Usually no XML action needed |
| `no_change` | Empty t+1 column — no change | Confirm and skip |

**How value matching works:** The script builds a numeric value index from all DefConst `$param_name` constants in `CC_t`. For each changed docx row, it extracts numeric values from the year-t text and looks them up in the index. A match means "this docx value appears in this DefConst parameter". No `$param_name` identifiers needed in the docx — matching is by value.

**Known limitation:** The docx 2026 column is often a template with blank value placeholders (e.g. "EUR ___"). When this happens, the script cannot extract new values from the docx; new values must be supplied via a pre-existing `update_{CC}_{YEAR}.py`.

---

## Step 4 — Apply Parametric Changes

Write `update_{CC}_{YEAR}.py` using the `changes_{CC}_{YEAR}.json` manifest plus verified new values from the docx/CR. See [update-script-pattern.md](./references/update-script-pattern.md) for the standard pattern.

Run:
```bash
python update_{CC}_{YEAR}.py
```

Expected output: `N/N applied, 0 warnings`. Any warning means a parameter name was not found or the old value did not match — investigate before proceeding.

**If re-running after a re-clone**: the update script is idempotent; re-run it to restore values.

---

## Step 5 — Structural Changes

Structural changes cannot be fully automated. Each requires understanding the EUROMOD function logic.

**Common structural change types and their XML patterns:**

See [structural-patterns.md](./references/structural-patterns.md) for all five patterns: eligibility condition changes, new BenCalc components, benefit formula changes, SchedCalc tier restructuring, and means test changes.

For each structural change identified in the HTML report:
1. Read the description in the docx (2026 column)
2. Locate the relevant policy in the XML (`euromod-xml` skill)
3. Confirm the change intent with the user before editing
4. Apply using lxml (never text replacement)

---

## Reference Files

- [update-script-pattern.md](./references/update-script-pattern.md) — Standard template for `update_{CC}_{YEAR}.py`: SETTINGS block, the `apply_change()` loop, and idempotency contract
- [structural-patterns.md](./references/structural-patterns.md) — XML patterns for common structural changes (new BenCalc components, Elig condition changes, SchedCalc tier restructuring)
