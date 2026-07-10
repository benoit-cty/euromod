# Report Template: generate_report.py

This file specifies the complete structure, helper functions, CSS, and section-by-section content rules for the HTML verification report produced by `generate_report.py`.

An example output is available at [references/EM_DK_policy_verification_2025_2026.html](./EM_DK_policy_verification_2025_2026.html).

---

## Required Helper Functions

Copy exactly into every `generate_report.py`:

```python
SEV_COLOR = {"WARNING": "#fd7e14", "INFO": "#0d6efd"}
SEV_BG    = {"WARNING": "#fff3cd", "INFO": "#f0f4ff"}

def badge(sev):
    c = SEV_COLOR.get(sev, "#555")
    return f'<span style="background:{c};color:white;padding:2px 8px;border-radius:4px;font-size:0.82em;font-weight:bold">{sev}</span>'

def domain_badge(domain):
    color_map = {"Benefits": "#198754", "Taxes": "#0dcaf0",
                 "Contributions": "#6f42c1", "Childcare": "#198754", "XML": "#dc3545"}
    c = color_map.get(domain, "#888")
    return f'<span style="background:{c};color:white;padding:2px 7px;border-radius:4px;font-size:0.80em;">{domain}</span>'

def row_color(sev):
    return SEV_BG.get(sev, "#f9f9f9")

def ok(v):   return f'<span class="ok">{v}</span>'
def warn(v): return f'<span class="warn">{v}</span>'
def dash():  return "\u2014"
def bold(v): return f'<strong>{v}</strong>'
def tbd(v):  return f'<em style="color:#888">{v}</em>'
```

> **⛔ MANDATORY — Parameter constant names in tables:** EUROMOD parameter names (e.g. `$txc_basic_rate`, `$tin_upthres1`) must **never** be combined with a numeric value in the same cell. They must go in a **dedicated column** (e.g. a "Constant" or "Parameter" column separate from the value column). **Spine Row** columns (`pol_n.func_n.par_n` / `pol_n.func_n`) are only present in Sections 6 and 7 — never add them elsewhere.

---

## Page-Level Structure (top to bottom)

1. `<h1>🇨🇨 CountryName (CC) — Policy Verification Report YYYY</h1>`
2. `<p>Generated: {today} | System: CC_t-1 (base) → target: CC_t</p>`
3. `<div class="summary-box">` — n_param parametric changes, n_warning warnings, n_info info, n_structural structural changes
4. `<h2 id="toc">Contents</h2>` + `<ul class="toc">` with 7 anchor links (one per section)
5. Sections 1–7 as below
6. Footer: `<hr>` + `<p style="color:#888;font-size:0.85em">Report generated...</p>`

---

## CSS

Must match the canonical DK template exactly:

```css
body { font-family: 'Segoe UI', Arial, sans-serif; margin: 20px 40px; color: #212529; font-size: 14px; }
h1 { color: #003087; border-bottom: 3px solid #003087; padding-bottom: 6px; }
h2 { color: #003087; margin-top: 30px; border-left: 4px solid #003087; padding-left: 10px; }
h3 { color: #333; margin-top: 20px; }
table { border-collapse: collapse; width: 100%; margin-top: 10px; }
th { background: #003087; color: white; padding: 8px 10px; text-align: left; font-size: 0.9em; }
td { border: 1px solid #dee2e6; padding: 7px 10px; vertical-align: top; }
tr:nth-child(even) { background: #f8f9fa; }
.summary-box { background: #e9f0fb; border-left: 5px solid #003087; padding: 12px 16px; margin: 16px 0; border-radius: 4px; }
code { background: #e9ecef; padding: 1px 4px; border-radius: 3px; font-size: 0.88em; }
.source-ok { color: #198754; font-weight: bold; }
.source-fail { color: #dc3545; }
.toc a { color: #003087; }
.ok { color: #198754; font-weight: bold; }
.warn { color: #e65c00; font-weight: 600; }
```

**Note**: `h1` uses a bottom border (not a filled background). `body` uses `margin: 20px 40px` (not `max-width` / `margin: auto`).

---

## Section Specifications

The 7 sections are always present; omit a section's table rows if data is absent but keep the heading.

| # | Section `id` | Section title | Content |
|---|---|---|---|
| 1 | `sources` | Source Inventory | Table: **Source \| Type \| Role \| Status \| Coverage**. One row per source (docx files, Country Report, EUROMOD XML, web sources). Role: "New/Updated" (Q1 sources) or "Comparison" (Q2 sources). Status: ✅ Extracted / ⚠️ Partial / ❌ Inaccessible |
| 2 | `phase1` | Changes Documented in Policy Docx (t-1 → t) | **Conditional — include only if docx files were selected (Q1 or Q2); omit entirely if not.** `<h3>` subsections per policy area, each with: **Policy \| Parameter \| t-1 Value \| t Value**. Rule 1: always show the explicit t value — never write "unchanged". Rule 2: bold t Value cell when t ≠ t-1, no colour changes. Rule 3: no `warn()`, `ok()`, `badge()`, or CSS colour anywhere in this section. |
| 3 | `phase2` | Year t-1 (YYYY) — Cross-Check of Available Sources | Columns: **Parameter \| Policy/Constant \| [one column per selected source: Docx → CR → XML → Web] \| Status**. Include a column for every selected source; write "—" if no value found. Omit a column only if that source was not selected at all. All data columns must be plain text — no colour, no tick marks. Reserve orange/warn styling for the Status column only. |
| 4 | `phase4` | Year t (YYYY) — Cross-Check of Available Sources | 5 columns: **Parameter \| Policy/Constant \| Docx t \| Web source \| Status**. No CR column (CR never covers t). Write "—" for unchecked parameters (never "site: TBD"). |
| 5 | `issues` | Issues & Warnings | 6 columns: **ID \| Severity \| Domain \| Policy/Title \| Detail \| Recommendation**. Use `badge(sev)` for Severity and `domain_badge(domain)` for Domain. Row background from `row_color(sev)`. Severity: `WARNING` (fix needed) or `INFO` (advisory). |
| 6 | `params` | Parametric Changes to be Implemented in [CC]_t | **7 columns**: **Spine Row \| Parameter \| Policy \| t-1 Value \| t Value \| Nature \| Source**. Spine Row at parameter level (`pol_n.func_n.par_n`). Nature: *Parametric* or *Structural*. Before each policy-area group, insert a divider row: `<td colspan="7" style="background:#003087;color:white;font-weight:bold;padding:6px 10px">GroupName</td>`. Bold t Value for known changes; plain text for unchanged; italic grey for TBD. Source column cites separately for t-1 and t (e.g. "2025: docx ✓, CR ✓; 2026: docx ✓"). Write `NEW` for parameters with no t-1 counterpart. **Case A** (t system does not exist): show ALL parametric changes; precede with `<p class="warn">⚠️ The <code>[CC]_t</code> system does not yet exist…</p>`. **Case B** (t system exists): show ONLY discrepant parameters; precede with `<p>ℹ️ The <code>[CC]_t</code> system already exists…</p>`. |
| 7 | `structural` | Structural Changes to be Implemented in [CC]_t | **3 columns**: **Spine Row \| Policy \| Description of Structural Change**. Spine Row at function level (`pol_n.func_n`); write `NEW` for new policies. One row per structural change. Never use `<ul>` here — always `<table>`. **Case A**: list every new structure to create. **Case B**: list only structural issues found during verification. |

---

## Status Values (Sections 3 and 4)

- `✅ MATCH` / `✅ CONFIRMED` — all checked sources agree
- `⚠️ DISCREPANCY — see [ID]` — sources disagree; issue logged in Section 5
- `ℹ️ Docx only` — no comparison source available for this parameter
- `⚠️ Docx AND XML wrong` — both docx and XML diverge from the authoritative source

---

## Key Rules

**Section 3**: docx column always comes first, then CR, then XML, then web. Write "—" for any source not consulted — never leave a cell empty.

**Section 4**: CR is never included (it covers only t-1). Only sources with actual t-year data go in the table.

**Sections 6 and 7 are always present** — never omit them. Check during Phase 4 whether `[CC]_t` exists in the XML; record as Case A or Case B and apply accordingly.
