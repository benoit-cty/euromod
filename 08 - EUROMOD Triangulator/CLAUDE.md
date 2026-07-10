# EUROMOD Triangulator - System Instructions & Agent Guide

## Project Overview & Objective
The EUROMOD Triangulator is an automated pipeline designed to cross-reference and verify consistency across three core data sources:
1. **EUROMOD Country Reports (CRs)**: Descriptions of the models.
2. **National Legislation**: The actual legal texts on taxes and benefits (The Ground Truth).
3. **EUROMOD Models (XML)**: The coded tax-benefit rules in the microsimulation model.

**Goal:** Produce clear, structured HTML reports that link these three sources, highlighting consistencies (✅), discrepancies (❌), and potential missing elements.

## Data Sources & Paths
- **Country Reports:** `./country-reports/Y16/` (Markdown format converted from Word/PDF).
- **Legislation:** `./legislation/[CC]/` (Markdown converted from national gazettes).
- **EUROMOD Models:** `./models/EUROMOD_RELEASES_[VERSION]/XMLParam/Countries/[CC]/[CC].xml`
- **Output Triangulations:** `./triangulations/[VERSION]/[CC].html`

## The Triangulation Workflow
The pipeline operates in 5 phases. Future agents should check `PLAN.md` to see the current status.
1. **CR Extraction:** Convert Word/PDF Country Reports into pure Markdown.
2. **Automated Scraping:** Extract laws cited in CRs via automated scripts.
3. **PENDING Resolution:** Manually (or via advanced proxy/headless agents) download laws that blocked standard scrapers. *Never start triangulation for a country if a `PENDING.md` file exists in its legislation folder.*
4. **XML Policy Extraction:** Parse the massive EUROMOD XML files into lightweight `JSON` and `Markdown` files located at `./policies/[VERSION]/[CC]/`. 
5. **Triangulation Engine:** The LLM cross-references the JSON/MD policies against the Country Report and the National Legislation, producing an intermediate JSON inference file, which is then compiled into a final styled HTML report.

## The `.copilot/skills` Ecosystem
Agents MUST rely on the specialized skills located in `.copilot/skills/` to interact with this project:
- **`euromod-policy-verification`**: The core Triangulation Engine. Contains the scripts to extract XML rules (`scripts/extract_rules.py`), run the inference loop (`scripts/run_inference.py`), and generate the final HTML (`scripts/generate_html_report.py`).
- **`law-scraper`**: Used for fetching full legal texts from government portals. Look in `utils/[CC]/` for highly valuable, production-tested scripts for navigating specific national APIs (e.g., Austrian RIS, Dutch wetten.overheid.nl).
- **`euromod-xml`**: **Foundational.** Load this any time you need to deeply understand, navigate, or manually edit a `{CC}.xml` file.

## Core Agent Directives & Gotchas

### 1. Verification & Reporting Rules
- **Legislation is King**: National legislation as stored in `./legislation` is the absolute ground truth. Both the Country Report and the EUROMOD Model XML must be evaluated against it.
- **Two-Step Generation**: Triangulation reports are generated in two steps. First, generate a structured JSON file via inference. Second, run `generate_html_report.py` to convert it into a styled HTML report.
- **Summary Stats & Emojis**: Reports must begin with summary statistics. Tables must use ✅/❌ emojis to indicate match status and include a single-sentence explanation *only when relevant*.
- **Instrumental Values**: Values like `99999999999` used in EUROMOD bracket functions represent infinity (no upper limit). They do not exist in legislation and must be explicitly excluded from discrepancy checks to avoid false positives.

### 2. EUROMOD XML Handling
- **Active & Inactive Policies**: When extracting rules, extract *all* policies and functions regardless of their `<Switch>` status (on, off, n/a), but clearly note their switch status in the extracted Markdown/JSON.
- **Time Context (June 30th Rule):** EUROMOD systems generally reflect the rules in place as of **June 30th** of the given policy year (e.g., `AT_2025` reflects the law as it stood on June 30, 2025). Do not assume January 1st rules apply for the whole year if a mid-year reform occurred.
- **Library Choice:** Always use **`lxml`** for EUROMOD XML parsing (much faster than the standard library). XML files can be up to 116MB; do not load the full tree into memory carelessly.
- **Properties are Children:** All EUROMOD XML properties are child elements, never attributes. Use `.find(f"{NS}Name").text`. Always use the correct namespace `{http://euromod.com/CountryConfig.xsd}`.
- **VARCONFIG Translation:** Do not parse `VARCONFIG.xml` to bridge acronyms to text. The Country Reports naturally act as the translation layer.

### 3. Web Scraping Constraints
- **JS-Rendered Portals (e.g., NL):** If standard `httpx` returns a tiny ~800 byte file with only generic navigation, the portal requires JavaScript. Use `curl_cffi` (impersonating Chrome), official APIs, or headless browsers.
- **SSL & Redirects:** Always use `follow_redirects=True` and `verify=False` for government sites.

### 4. General Coding Rules
- **No hardcoded paths:** Accept paths as arguments, config files, or prompt the user.
- **No silent errors:** Raise or print clearly; never swallow failures.
- **One script, one job.**
