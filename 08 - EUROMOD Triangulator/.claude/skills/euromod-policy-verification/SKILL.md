---
name: euromod-policy-verification
description: "Cross-check EUROMOD policy parameters across policy docx files, Country Reports (PDF or DOCX), official government or social-insurance websites, and the EUROMOD model XML. Use when asked to check, verify, validate, or compare any combination of these sources against each other, for example docx vs CR, CR vs XML, or CR vs websites."
---

# EUROMOD Policy Verification

## Overview

This skill compares policy parameter values across any combination of sources. There is no fixed "primary" source — the user declares which source(s) are **newly updated and need checking**, and the rest serve as **comparison sources**. The only arbiter of truth is **official legislation and government websites**; all other sources (docx, CR, XML) may contain errors and are treated neutrally — discrepancies are always flagged without assuming any one document is correct.

Typical setups:

| Newly updated source(s) | Typical comparison sources |
|---|---|
| Policy docx files | CR, EUROMOD model XML, official websites |
| Country Report (CR) | EUROMOD model XML, official websites |
| EUROMOD model XML | CR, policy docx files, official websites |
| Policy docx + CR (both updated) | EUROMOD model XML, official websites |

Available sources and their year scope:

| Source | What it covers | Year scope |
|---|---|---|
| **Policy docx files** | Documented policy parameters for t-1 and t | t-1 and t |
| **EUROMOD Country Report (CR — PDF or DOCX)** | Modelled parameters in the EUROMOD baseline | t-1 only |
| **Official websites** | Current and upcoming legislation, rates, and amounts | t-1 and/or t |
| **EUROMOD model XML** | Implemented parameters in the active model system | t-1 only |

The user is asked upfront which source(s) are new/updated and which to compare against.

---

## Working Protocol

The verification follows a **gated workflow**: each phase ends with a user-facing checkpoint before proceeding. Never skip a checkpoint or proceed silently.

```
Phase 0: Setup — detect files, years, and ask user which sources to use  ← WAIT
     ↓
Phase 1: Extract all docx files           ← batch or one doc at a time
     ↓
Phase 2: Search Country Report (PDF/DOCX)  ← t-1 values; one pass for all policies
     ↓                                       (skip if CR not selected)
Phase 3: Fetch official websites          ← t-1 and t values; deduplicate
     ↓                                       (skip if websites not selected)
Phase 4: Check EUROMOD model XML          ← t-1 values; probe the active system
     ↓                                       (skip if model not selected)
Phase 5: Cross-check and compile issues   ← includes cross-doc consistency
     ↓
Phase 6: Generate report                  ← HTML file
```

**Key principle**: Phases 2–4 each run once for all documents — never repeat a CR search, web fetch, or XML probe already done for another policy in the same session.

---

## Step-by-Step Procedure

### Phase 0 — Setup ⛔ WAIT FOR ANSWERS BEFORE ANYTHING

This phase happens **before** any file reading, docx extraction, or PDF access.

**Step 0 — Confirm working directory and country.**

Two things must be unambiguous before you do anything else:

1. **Working directory / file location.** Check whether a folder path is already clear from context (the user pasted a path, a prior session note identifies the folder, or files are visible in the workspace). If not clear — for example, the user says "I want to verify Denmark" with no path — ask:
   > "Where are the policy documents located? Please provide the folder path."
   Wait for the answer before proceeding.

2. **Country.** There must be exactly one country for this session. If the user's request mentions more than one country, or if no country is discernible, ask:
   > "Which country should I verify? Please confirm the single country code (e.g. DK, SI, EL)."
   Wait for the answer. Do **not** guess or infer from partial context — country ambiguity must be resolved by the user, not by the agent.

Only proceed to Step 1 once both the folder path and the country are confirmed.

**Step 1 — Identify available files.**

Using the confirmed country code from Step 0, list all files **in the working directory only**. Identify:
- All `.docx` files for the confirmed country (filename starts with or contains the country code, case-insensitive)
- Any CR file (PDF or DOCX) — e.g. `Y16_CR_EL.pdf` or `Y16_CR_SI.docx`
- Any EUROMOD XML file for the country (e.g. `EL.xml`) — **only if present in the working directory**

⚠️ **Only look inside the working directory.** Do NOT search parent directories, other workspace folders, network shares, or any path outside the confirmed working directory. If a file type (CR, XML) is not found there, treat it as absent — do not go looking for it elsewhere.

⚠️ **Explicitly exclude** any files belonging to other countries, even if in the same folder. List excluded files by name.

Map each included docx to its policy type: Taxes, Benefits, Contributions, Sickness, or Childcare.

**Step 2 — Detect t-1 and t years.**

Infer the year range from the docx filenames (e.g. `EL_taxes_2025_2026.docx` → t-1 = 2025, t = 2026). State this explicitly. Use t-1 throughout Phase 2 (CR) and Phase 4 (model); use both t-1 and t for Phase 3 (websites).

**Step 3 — Scan sources sections.**
Quickly extract only the Sources paragraphs from each **country-filtered** docx (last section). Collect all law names and URLs cited. Also note whether any URLs are already given. Write a short summary listing the files, years, and all sources found.

**Step 3b — Check year coverage for each non-internet source.**

For every non-internet source **actually found in the working directory** (from Step 1), explicitly determine which years it covers. Only include rows for sources that are present — omit the CR row if no CR was found, omit the XML row if no XML was found:

| Source | Year coverage | Notes |
|---|---|---|
| Policy docx files | t-1 **and** t — verify by checking whether the "Change in t" column is populated or explicitly states "no change" | If the entire t column is blank, flag it — could be an empty document or t data truly absent |
| Country Report (CR) *(only if found)* | t-1 **only** — the CR always describes the already-modelled baseline; it never covers t | Exception: if the CR title or a section heading explicitly mentions t (rare), note that and check |
| EUROMOD model XML *(only if found)* | t-1 **only** — only the most recent system (e.g. `DK_2025`) exists at the time of writing; no t system has been implemented yet | |

**Internet sources (web)**: do **not** need a year coverage check here — by default assume they contain information for **both** t-1 and t. Note any exceptions discovered during Phase 3 fetching (e.g. a page only shows current-year rates). State the resulting coverage summary briefly before proceeding; it determines which comparison columns are possible in report Sections 3 and 4.

**Step 4 — Find additional official sources** by web search (tax authority, social insurance institute, legislation portal). Flag any that require JavaScript.

**Step 5 — Present questions to the user and WAIT:**

Use the `vscode_askQuestions` tool to ask **Q1–Q3** in a single call.

- **Q1 — Newly updated sources** (`header: "Q1_new_sources"`): offer only sources actually found in Step 1. Pre-select **"Policy docx files"** if available. No freeform input.

- **Q2 — Comparison sources** (`header: "Q2_compare"`): offer the remaining found sources plus **"Official websites — t-1 and t values"**. Pre-select all available options. Allow a free-text field for extra URLs, circulars, or gazette citations.

- **Q3 — Which policies to check** (`header: "Q3_policies"`): build the list dynamically from available docx/CR/XML evidence. Always include **"All (recommended)"** first and pre-selected. Omit policy areas absent from all available sources and note why. No freeform input.

**Step 6 — Wait for user answers.** Incorporate any additional sources from Q2 free text. Restrict the rest of the session to the policy areas selected in Q3. Then proceed to Phase 1.

**Phase routing based on Q1/Q2 answers:** Extract all Q1 sources first in the order `docx → CR → XML` if multiple are selected. Then process each selected Q2 comparison source in its own phase. Keep the left-to-right report column priority `docx → CR → XML → official websites`.

**Column anchor rule for report Sections 3–4** (when multiple Q1 sources exist): the leftmost data column uses the fixed priority order **docx → CR → XML**. All Q1 sources appear as adjacent columns before any Q2 comparison columns. Official websites always appear last.

**Neutral error direction**: discrepancies are always reported relative to **official sources** (legislation, government websites). When two Q1 sources disagree with each other, the issue is flagged neutrally — both values are shown and the official source arbitrates. Never assume a Q1 source is correct simply because it is newer.

**Scope restriction**: process only the policy areas selected in Q3. Within each phase, skip any policy area not selected. If a phase (e.g. CR) does not contain a section for a selected policy area, note it briefly and move on — do not treat it as an error.

### Phase 1 — Extract docx files ← skip if docx not in Q1 or Q2

**⚠️ Only extract docx files for the detected country (from Phase 0 Step 1). Never read docx files for other countries, even if they are in the same folder.**

Extract all selected, country-filtered docx files in one batch. Use [extract_docx.py](./scripts/extract_docx.py).

**⚠️ Dense paragraph warning**: Some docx files store multiple parameter values as a single long narrative paragraph (e.g. "General allowance: €X + ... Pension deduction: up to €Y. Student allowance: €Z. ...") rather than in table cells. Standard table-cell extraction will miss all of these. **Always read document paragraphs as well as tables.** After extraction, verify that every parameter expected from the policy area has a value — if a parameter appears in the t-1 column but has no t value and no explicit "unchanged" marker, do not assume it is TBD: search the paragraphs of the t column for the value.

**⚠️ Empty t column ≠ TBD**: An empty 2026 column in the docx means the parameter is **confirmed unchanged** — it is not a missing value. Only use TBD when there is a positive signal of change (e.g. "updated", "indexed") but no new value is given.

**⚠️ Nested tables warning**: Policy docx files sometimes contain nested tables inside cells (e.g. bracket tables for childcare discounts or PIT schedules). `cell.text` alone will miss them. Inspect nested tables explicitly; if a cell ends with a colon (e.g. "according to the income bracket:") but contains no numbers, suspect a nested table.

For each docx, build a structured summary table with columns `Field | t-1 Text | Change in t`.

Note: the "Change in t" column is often entirely empty — verify this is intentional, not an omission.

**Checkpoint**: Show the summary table(s). Flag any document where the entire t column is empty. Proceed to the next applicable phase.

### Phase 2 — Country Report (PDF or DOCX) (t-1) ← skip if CR not selected

**Scope**: the CR covers only **year t-1** parameter values. Do not use it to validate t (upcoming) values.

**Where to look**: Policy parameter values in the CR are **always in Section 2** (e.g. "2. Description of the tax-benefit system"). Do not search other sections (data chapters, SILC methodology, etc.) for policy parameters — they will not be there. Start your keyword scan on Section 2 pages only. If you do not know which pages Section 2 spans, first scan for the heading "2." or "Section 2" to locate its start and end pages, then restrict all further extraction to that range.

**Step 1 — Detect CR format.** Check whether the CR is a `.pdf` or `.docx` file.

- **If PDF**: use `pdfplumber` or [search_pdf.py](./scripts/search_pdf.py). Do a keyword scan first, then read the full relevant pages.
- **If DOCX**: use `python-docx` and search both paragraphs and tables.

**Warning**: CR PDFs often have non-policy sections (data chapters, SILC methodology). Restrict reading to the policy chapter, usually Section 2 in the first ~60 pages.

Good keywords by policy type (for both formats):

| Policy | Keywords to search |
|---|---|
| Taxes | tax schedule, income tax, bracket, rate |
| Benefits | allowance, grant, scholarship, social assistance |
| Contributions | contribution rate, employer, employee, self-employed |
| Sickness | nadomestilo, sickness benefit, replacement rate, sick leave |
| Childcare | childcare, kindergarten, vrtec, fee, income bracket |

**When processing jointly**: run a single keyword scan for all policy types at once, then read all relevant pages/paragraphs in one pass — do not repeat the CR search per document.

**Checkpoint**: Report which pages cover which policies, and which policies were NOT found in the CR (common: sickness and childcare). Note the CR version. Then proceed.

### Phase 3 — Official Websites (t-1 and t) ← skip if websites not selected

**Scope**: websites can validate **both t-1 and t** values. They are the only source for upcoming (t) changes not yet in the CR. When a website covers a t-1 value also in the CR, prefer the CR verdict but note agreement.

Use `fetch_webpage` for official sources. Strategy:

**Step 1 — Independently discover specific URLs per policy.** Do NOT rely solely on URLs collected in Phase 0 or cited in the CR — those may be general homepages, outdated, or wrong subdomains. For each policy area, find the most specific current official page available: tax authority PIT page, benefits subpage, insurance rates/amounts page, or ministry fees/prices page.

**Step 2 — Fetch the discovered specific URL** and extract the relevant values. If a specific URL is not known, start with the homepage to locate the right subpage link, then fetch the subpage.

**Step 3 — Note all JS-blocked/inaccessible sources** and follow the fallback ladder below.

**When processing jointly**: deduplicate sources across policies — if a URL serves multiple policies (e.g. the health insurance site covers both contributions and sickness), fetch it once and extract what is needed for each.

**When a source is inaccessible (JS-rendered, 404, or blocked)**, work through the [fallback ladder](./references/web-fallback.md) in order before giving up. Use only official documents or sites that host official documents verbatim.

**Checkpoint**: Present a source-status table with columns `Source | Policies covered | Status`. For any inaccessible source whose fallbacks failed, state what information it was expected to provide and ask the user for that information if needed.

### Phase 4 — EUROMOD Model XML (t-1) ← skip if model not selected

**Scope**: the model XML covers only **year t-1** — specifically, the most recent system for the country (e.g. `EL_2025`). No t system exists at the time the docx is written. Use this phase to verify that the implemented model parameters match the docx and the CR.

**Step 1 — Locate the XML file.**

Look for the model in the working directory or a known subfolder (e.g. `EUROMOD_MASTER_VERSION_*/XMLParam/Countries/[CC]/[CC].xml`). If not present, ask the user for the path. Do not guess the path.

**Step 2 — Identify the active system.**

> ⛔ **BLOCKING REQUIREMENT: Load the `euromod-xml` skill before writing any probe script, reading the XML, or making assumptions about XML structure.** It contains the canonical XML navigation rules and function patterns.

Grep for `<Name>[CC]_20` in the XML to list available systems and use the most recent t-1 system (e.g. `EL_2025`). Then write a targeted probe script (`_probe_[cc]_xml.py`) that extracts `DefConst`, `Elig`, and `SchedCalc` parameters for the selected policy areas and save output to `_probe_[cc]_out.txt`.

Start XML policy search with these families, then refine inside the `euromod-xml` skill: taxes `tin*` / `txc*`; contributions `tsc*`; benefits `b*`; sickness `sickcomp*` / `sick*`; childcare `xcc_*`. Adjust with the country suffix (`_el`, `_si`, etc.).

**Step 4 — Compare model values to docx.**

For each docx parameter:
- Search the probe output for the corresponding XML parameter name
- Compare value ± unit (note `#m` = monthly, `#y` = yearly, `#d` = daily, `#c` = capital value)
- Flag discrepancies and classify per the taxonomy in Phase 5

**Key patterns to check:**
- `DefConst` stores named constants (e.g. `$bunct_rate = 0.55`)
- `SchedCalc` stores bracket tables (uplim values + rates)
- `Elig` stores eligibility conditions (e.g. `dag >= 22` for age)
- Cross-reference `ConstDef_[cc]` policy for shared uprate constants (e.g. `$siclim`)

**Step 5 — Handle model–docx discrepancies.**

When sources disagree, the **official source (legislation, government websites) is the arbiter**. Never assume a source is correct simply because it is the newest or because it is the Q1 source. Determine the direction as follows:
- If **web/legislation = source A ≠ source B**: source B has an error — flag it
- If **web/legislation = source A = source B**: ✅ fully consistent
- If **web/legislation disagrees with all sources**: flag all as incorrect
- If **source A ≠ source B** but **no web/legislation available**: flag neutrally — both values shown, arbitration not possible from available sources
- If **web = source A ≠ source B** and source B is the XML: model has an error (flag for XML fix)
- If **web = source A ≠ source B** and source B is the docx: docx has an error

**Checkpoint**: Report per-parameter model vs docx comparison in a table. Flag any discrepancy. Then proceed to Phase 5.

### Phase 5 — Cross-check and Compile Issues

**Per-document checks**: read [references/checklist.md](./references/checklist.md) now and use it to compare each docx against all selected sources (CR, websites, model) for every criterion.

**For each finding, record which source(s) support it:**

| Finding | CR (t-1) | Website (t-1) | Website (t) | Model (t-1) |
|---|---|---|---|---|
| Rate X = Y | ✅ | ✅ | — | ✅ |
| Threshold Z wrong | ✅ CR: 7,373 | — | — | ✅ model: 7,572 (advisory) |

**Cross-document consistency checks**:
- Wage anchors (minimum wage, average wage) should be identical across all documents that reference them
- The same benefit/rate should not appear with different values in two different docx files
- If year X is the base year in one document, it should be the base year in all

Report issues using the taxonomy in the **Issue Taxonomy** section of [references/checklist.md](./references/checklist.md).

### Phase 6 — Generate Report

Before writing `generate_report.py`, compute spine rows either with `build_param_row_index` from the `euromod-xml` skill or with [scripts/_spine_rows.py](./scripts/_spine_rows.py). In Section 6 use parameter-level rows `pol_n.func_n.par_n`; in Section 7 use function-level rows `pol_n.func_n`; use `NEW` if no t-1 counterpart exists and investigate any `?` lookup before finalising.

Then follow [references/report-template.md](./references/report-template.md) exactly for HTML structure, CSS, section specifications, tables-only rules, save-location logic, and the final `Report saved to: ...` line. Always write `generate_report.py` as a file in the working directory and run that file directly; do not use `python -c`.

---

For policy-specific pitfalls, use [references/checklist.md](./references/checklist.md). For country-specific source URLs and legal databases, use [references/sources-by-country.md](./references/sources-by-country.md).

---

## Scripts and References

- [Extract docx paragraphs](./scripts/extract_docx.py)
- [Search PDF for keywords](./scripts/search_pdf.py)
- For DOCX CR: search paragraphs and tables with `python-docx` (no separate script needed)
- [Generate HTML report — reference example](./scripts/generate_report.py) *(structural reference only — write a fresh copy to the working directory for each run)*
- [Fallback ladder for inaccessible sources](./references/web-fallback.md)
- [Report template — HTML structure, CSS, section specs](./references/report-template.md)
- [Verification checklist by policy type](./references/checklist.md)
- [Source patterns by country](./references/sources-by-country.md)
- [Example report output](./references/EM_DK_policy_verification_2025_2026.html)

**⛔ CRITICAL — How to run the report generator:** Always write `generate_report.py` into the working directory as a file and run that file directly. Never use `python -c "..."` for the report generator; Windows command-length limits make that unreliable for large report payloads.

---

## Handoff to Implementation

Once verification is complete and the issues JSON has been saved, hand off to the **euromod-policy-implementation** skill.

Implementation can proceed only when all `"factual"` issues are resolved. `"incomplete"` issues are warnings. Save the verification output as `{CC}_issues_{YEAR}.json` in the working directory, then switch to the implementation skill, which uses this JSON as the gate for `map_changes.py`.
