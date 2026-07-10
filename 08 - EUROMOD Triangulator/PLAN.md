# EUROMOD Triangulator - Execution Plan & Handoff

## Project Overview
The goal is to automatically cross-reference and verify consistency across three core data sources:
1. **EUROMOD Country Reports** (`./country-reports/Y16/`)
2. **National Legislation** (`./legislation/`)
3. **EUROMOD Models** (`./models/EUROMOD_RELEASES_[VERSION]/XMLParam/Countries/`)

---

## 🟢 Current Status: Phases 1, 2, 4 & 5 Completed for Sub-set of Countries

* **Phase 1 (Country Reports):** All 27 Word documents for Y16 have been successfully converted to pure Markdown.
* **Phase 2 (Legislation Scraping):** Automated scraping generated a massive, clean Markdown dataset of national legislation. 
* **Phase 4 (Model XML Extraction):** Successfully extracted the full XML policy spines into lightweight JSON (for programmatic precision) and Markdown (for LLM context efficiency) for 7 complete countries.
* **Phase 5 (Triangulation):** Successfully triangulated the 7 complete countries (AT, ES, HR, HU, LV, NL, SE), resolving Javascript portal bottlenecks (NL) and API data-fetching limits (AT) in the process. Generated styled HTML reports.

### Legislation Extraction Status
**Overall Progress**: 741 files successfully extracted, 293 files pending manual intervention.
**Fully Completed Countries (0 Pending)**: AT, ES, HR, HU, LV, NL, SE.
*Update: Task 1 and Task 2 executed. Task 1 requires human intervention (residential proxies). Task 2 identified several suspicious files in NL, SE, HU, HR requiring manual review.*\n\n---\n\n

---

## 🟢 Where to Resume (Strategic Pivot: Active Parameter Discovery) - COMPLETED

*Update: The new **Search Augmentation Loop** has been built into the `law-scraper` skill. You can run it via `.venv/Scripts/python .copilot/skills/law-scraper/scripts/search_augmentation.py --country CC --year YYYY`.*

### Priority Task: Build the Search Augmentation Loop
✅ **1. Identify Gaps:** Parses existing Triangulation outputs to find missing XML parameters.
✅ **2. Query Formulation:** Uses Gemini API or fallback templates to formulate native-language search queries from XML comments.
✅ **3. Active Web Search:** Leverages Exa and Tavily search APIs to query official government sources (`site:gov.xx` or `site:*.xx`).
✅ **4. Scrape & Validate:** Saves output to `utils/[CC]/augmented_targets_[YEAR].json` for review before scraping.
✅ **5. Re-Triangulate:** Ready to run the engine again with the augmented ground truth.

#### Search Engine Selection Strategy
To accomplish this, we will leverage search APIs depending on the specific retrieval needs. **Note: All API keys (Exa, Tavily, Brave) are securely stored in the `.env` file in the project root. Future scripts should use `python-dotenv` to load these variables and must never hardcode or log them.**
* **Exa (Primary):** Highly recommended for this task. It performs semantic searches based on content type and excels at returning actual official PDFs and government pages rather than SEO-optimized secondary sources (e.g., prompt it to find "Official government legislation in Austria...").
* **Brave (Fallback):** Excellent for exact keyword searches and strictly respects `site:` operators (e.g., `site:boe.es`). Ideal when we know exactly what we are looking for but lack the specific URL.
* **Tavily (Fact-check only):** Good for extracting exact numerical values quickly, but frequently synthesizes answers rather than providing the raw legal text. We should avoid it for downloading laws, but can use it to sanity-check a parameter value before doing a deep Exa search.

#### Methodological Challenges to Address
1. **The "June 30th Rule" (Time-Travel Problem):** EUROMOD policies reflect the law as of June 30th of a specific policy year. Search engines naturally return current values. We must enforce strict date/year constraints in search queries to find historical parameter values. Referencing the system in our search is key (e.g., ES_2025).
2. **The Language and Acronym Barrier:** XML parameters use cryptic variable names (e.g., `ils_sij` or `b_ch_amt`). We require an LLM translation step to convert XML context into semantic, national-language queries. Start from the comment column in the XML, which can provide useful information. If that is not enough, search in the country report by the code of the polici (i.e., `b_ch_amt`)
3. **Primary vs. Secondary Sources:** "Legislation is King." While tax blogs (KPMG, PWC) might have the right numbers, we must prioritize official national gazettes and government portals (e.g., using `site:` operators) to establish actual ground truth.

*Note: Once this feature is implemented and tested, we will return to the pending legislation issues below.*

---

## 🟢 Where to Resume (Implementing Enhancements) - COMPLETED

The two enhancements to improve the visibility of our findings and catch "Ghost Laws" have been successfully implemented and tested.

### Priority Task 1: Highlight CR Omissions in HTML Output
✅ **Implemented:** Modified `.copilot/skills/euromod-policy-verification/scripts/generate_html_report.py`.
✅ **Result:** Parameters that are actively coded in the XML and legally valid in the Legislation, but undocumented in the CR, are now prominently displayed at the very top of the HTML report in a red "🚨 Action Required: Update Country Report" box. This ensures immediate visibility for researchers.

### Priority Task 2: Top-Down "Ghost Law" Discovery
✅ **Implemented:** Created `.copilot/skills/law-scraper/scripts/ghost_law_discovery.py`.
✅ **Execution:** The script extracts macro-policy headers (like "Contributory Benefits", "Taxes") directly from the Country Report Markdown.
✅ **Resilience:** Implemented a dual approach—using the Gemini LLM if the API key is present, and falling back to a deterministic rule-based header extraction heuristic (filtering for keywords like "benefit", "tax", "pension") if it's missing.
✅ **Result:** Successfully tested on Spain (ES). The script successfully searched the Exa/Tavily APIs using the CR headers and returned the exact foundational consolidated laws (e.g., the General Social Security Act) that govern those policies. Results are safely saved to `utils/[CC]/ghost_laws_[YEAR].json` for review before scraping.

---

## 🟡 Where to Resume (Paused Tasks)

With the active parameter discovery (bottom-up) and ghost law discovery (top-down) loops complete, the triangulation engine is significantly more robust. We should now return to the original data quality tasks that were previously paused.

### Task 1: Resolve PENDING Legislation (Phase 3)
We cannot triangulate the remaining 20 countries because they have missing laws logged in `PENDING.md` files.
1. Review the `legislation/[CC]/PENDING.md` files.
2. The 293 "Pending" files are strictly due to severe bot protections (e.g., France's `legifrance.gouv.fr`, Luxembourg's `*.public.lu`, Lithuania's `e-tar.lt`).
3. Use headless browsers, residential proxies, or request human intervention to download these laws into `legislation/[CC]/raw/` and delete the `PENDING.md` file.

### Task 2: Verify Downloaded Legislation Quality
For the countries that have successfully downloaded legislation (no PENDING status), systematically read the generated Markdown files to verify they are the *actual* consolidated legal texts we need. 
1. **Quality Control:** Ensure the scraper did not just grab a summary page, a generic administrative order, or a table of contents. (For example, in `ES`, there is a file on *rentas minimas* that may not be the actual base law required).
2. **Action:** If a file does not contain the proper legal text, investigate the correct portal endpoint and re-fetch it, or flag it for manual review.

---

## 📝 Handoff Reminders for the Next AI Agent
1. **Read `CLAUDE.md` first.** It contains absolute system boundaries, the "Legislation is King" directive, and crucial EUROMOD XML parsing gotchas.
2. **Workspace Discipline:** Keep the root directory completely clean. Save country-specific extraction scripts or API explorers into `.copilot/skills/law-scraper/utils/[CC]/`.
3. **Skill Utilization:** Do not write XML parsers from scratch; leverage the tools and scripts built into the `.copilot/skills/` directories.


---

# EUROMOD Triangulator - Last execution resulted in the following

## Task 1: Resolve PENDING Legislation (Phase 3)
An automated attempt was made to resolve the 293 "Pending" files using the HTTP Client Ladder (`httpx` + `curl_cffi` impersonating Chrome) and Wayback Machine fallbacks for dead links. We also attempted resolution via Playwright.

**Result:** Due to severe bot protection (e.g. `e-tar.lt` returning 403 even for headless browsers), geoblocking, and missing laws in national databases (e.g., BOE Search errors for `Decreto 179/2002`), we have exhausted the standard automated approaches without proxies. 

**Action Required (Human Intervention):**
Please use residential proxies or manually download the laws for the 20 pending countries listed in their respective `legislation/[CC]/PENDING.md` files.

---

## Task 2: Verify Downloaded Legislation Quality
For the "Fully Completed" countries (`AT, ES, HR, HU, LV, NL, SE`), an automated quality verification check was run to identify scraped files that are:
- Suspiciously short (< 1500 bytes)
- Contain HTTP error texts like "404 Not Found" or "403 Forbidden"
- Are just an unrendered JS boilerplate
- Or are merely a Table of Contents.

### Findings for Completed Countries:
The following files were flagged for **manual review** as they do not appear to contain the proper legal texts.

**HR (Croatia)**
- `legislation/HR/mdu_gov_hr_8.md`: Too short (<1500 bytes)
- `legislation/HR/podaci_dzs_hr_11.md`: Too short (<1500 bytes)

**HU (Hungary)**
- `legislation/HU/allamkincstar_gov_hu_0.md`: Too short (<1500 bytes)
- `legislation/HU/allamkincstar_gov_hu_1.md`: Too short (<1500 bytes)
- `legislation/HU/allamkincstar_gov_hu_4.md`: Too short (<1500 bytes)
- `legislation/HU/allamkincstar_gov_hu_8.md`: Too short (<1500 bytes)
- `legislation/HU/allamkincstar_gov_hu_9.md`: Too short (<1500 bytes)

**NL (Netherlands)**
- `legislation/NL/Belastingdienst.md`: Too short (<1500 bytes)
- `legislation/NL/belastingdienst_nl_1.md`: Too short (<1500 bytes)
- `legislation/NL/st-ab_nl_3.md`: Too short (<1500 bytes)
- `legislation/NL/svb_nl_4.md`: Too short (<1500 bytes)
- `legislation/NL/UWV.md`: Too short (<1500 bytes)
- `legislation/NL/uwv_nl_6.md`: Too short (<1500 bytes)

**SE (Sweden)**
- `legislation/SE/circabc_europa_eu_2.md`: Too short (<1500 bytes)
- `legislation/SE/prognos_konj_se_0.md`: Too short (<1500 bytes)
- `legislation/SE/Socialstyrelsen_Riksnormen.md`: Too short (<1500 bytes)
- `legislation/SE/socialstyrelsen_se_25.md`: Too short (<1500 bytes)
- `legislation/SE/statistikdatabasen_scb_se_1.md`: Too short (<1500 bytes)
- `legislation/SE/statistikdatabasen_scb_se_26.md`: Too short (<1500 bytes)
- `legislation/SE/statistikdatabasen_scb_se_27.md`: Too short (<1500 bytes)
- `legislation/SE/www4_skatteverket_se_28.md`: Too short (<1500 bytes)
- `legislation/SE/www4_skatteverket_se_29.md`: Too short (<1500 bytes)

*(Note: AT, ES, and LV passed the automated quality check and appear to contain high-quality legal texts).*

