---
name: law-scraper
description: Build robust web scrapers for historical government websites, legal repositories, and statistical offices. Use this skill when extracting national legislation, tax codes, or government rules — especially during EUROMOD policy verification when an official source is inaccessible, blocked, or needed as a full legal text rather than a single parameter value. Handles link rot, anti-bot protections, PDF/HTML cleaning, and national gazette search engines across all 27 EU countries.
---

# Law Scraper Skill

Build production-grade scrapers tailored for extracting historical legal texts, tax rules, and government data. This skill adapts general web scraping best practices for the unique challenges of government portals: heavy document usage (PDF/Word), aggressive anti-bot protections, severe link rot for historical policies, and navigating national gazette search engines.

## Core Strategy & Workflow

When processing a new country, follow these standard steps:

### 1. Extract Sources (Explicit & Implicit)
We do not rely solely on explicitly hyperlinked URLs. You must build a comprehensive database of sources:
- **Explicit URLs:** Extract URLs from the source reports, filter out generic domains (e.g., `oecd.org`, `eurostat.eu`), and catalog them.
- **Implicit Citations:** Use Regex/NLP to scan source reports for named laws (e.g., *Gesetz*, *Arrêté royal*, *Zákon*, *Ley*). Deduplicate and catalog them.
- **Update Database:** Write all pending targets to `legislation-sources/[CC].md` (relative to the working directory).

### 2. Run the Scraper
Pre-built scrapers for all 27 EU countries live in `.copilot/skills/law-scraper/scripts/scrape_[CC].py`. Run the relevant one directly or adapt it if the country's portal has changed. Each scraper handles two types of logic:
- **Generic URL Scraper:** Fetches direct URLs.
- **National Gazette Scraper:** Programmatically searches national repositories (like Spain's BOE or Austria's RIS) by Law Title or ID, identifies the correct search result, and targets the **consolidated text** (Geltende Fassung / Texto Consolidado).

To process multiple countries at once, use `utils/run_batch.py`. To extract and filter URLs from source reports in bulk, use `utils/extract_batch_urls.py`.

### 3. Execution & Cleaning
- **HTML:** Use `BeautifulSoup`. Decompose `nav`, `footer`, `script`, `style`, `aside`, `form`, and `meta` tags. Extract the text using `soup.get_text(separator="\n\n", strip=True)`.
- **PDF:** Download the file and use `PyMuPDF` (`fitz`) to extract the text into Markdown.
- **Save:** Write the clean Markdown to `legislation/[CC]/[LawName].md` (relative to the working directory). Update the source index at `legislation-sources/[CC].md`.

### 4. Status Tracking & PENDING.md
**Never fail silently.**
- If a law cannot be found, if a server returns a 403/404, or if a portal uses a Single Page Application (SPA/SSO) that blocks scraping (like Belgium's MinFin), log it in `legislation/[CC]/PENDING.md` with the URL, the Error, and Manual Instructions.
- Update `legislation-sources/[CC].md` by replacing `` `[PENDING GAZETTE FETCH]` `` with `` `[✅ DOWNLOADED]` `` or `` `[FAILED/PENDING]` ``.

### 5. Workspace Cleanup
The root workspace must remain pristine. The `law-scraper` skill must be self-standing for use in other contexts.
- Move any one-off Python scripts, JSON URL lists, or HTML test files generated during this process into `.copilot/skills/law-scraper/utils/[CC]/`.

---


## Known Bottlenecks & Portal Quirks

- **JS-Rendered Portals (e.g., Netherlands `wetten.overheid.nl`)**: 
  - *Symptom:* `httpx` + `BeautifulSoup` successfully returns a 200 OK, but the resulting Markdown is suspiciously small (e.g., ~800 bytes) and only contains generic header/footer navigation boilerplate ("Direct naar content", "Contactgegevens", etc.).
  - *Cause:* The portal uses client-side JavaScript to dynamically load the actual legal text into the DOM.
  - *Alternative Approaches:* 
    1. **Headless Browsers**: Use Playwright/Selenium if the environment allows.
    2. **Alternative Endpoints**: Hunt for `/pdf`, `/print`, or `/xml` endpoints that bypass the JS frontend.
    3. **Official APIs**: For the Netherlands, check *LiDO (Linked Data Overheid)* or *repository.overheid.nl* which serve raw XML/HTML data directly.

## Technical Tooling & Resilience

**The HTTP Client Ladder:**
1. `httpx`: Start here. Enable `verify=False` and `follow_redirects=True`. Use long timeouts (e.g., `timeout=60.0`).
2. `curl_cffi`: Use if `httpx` is blocked with a 403 or Cloudflare error. It impersonates browser TLS fingerprints (e.g., `impersonate="chrome131"`).

**Resilience best practices:**
- Implement rate limiting (`time.sleep(1.5)`) between requests to avoid IP bans.
- Add try/except blocks to continue scraping the rest of the list even if one URL fails.
- Beware of SSL certificate errors (`[SSL: CERTIFICATE_VERIFY_FAILED]`); government portals frequently have misconfigured certificates.

---

## Detailed References

For exact Python script templates, anti-detection measures, and parsing techniques, load the reference files:

- **[scraping-patterns.md](references/scraping-patterns.md)**: Contains the core script templates, the HTTP Client Ladder implementation, and extraction logic.
- **[discovery-strategies.md](references/discovery-strategies.md)**: Advanced techniques for finding hidden APIs on government sites.
- **[wayback-machine.md](references/wayback-machine.md)**: How to integrate Internet Archive fallbacks for dead legal links.

## Bundled Utilities & Scrapers

This skill includes specialized utilities and scrapers:
- **`utils/extract_all_implicit.py`**: Generic regex engine for extracting implicit text citations across all European languages.
- **`scripts/scrape_ES.py`**: Advanced scraper for the Spanish BOE (Boletín Oficial del Estado). Demonstrates how to build an implicit search-to-consolidated-text pipeline.
- **`scripts/scrape_AT.py`**: Scraper for the Austrian RIS database, mapping explicit IDs to consolidated texts.
- **`utils/[CC]/`**: Country-specific helper scripts, test outputs, and filtered JSON targets.
  - *Example (`utils/AT/`)*: Contains highly valuable, production-tested scripts for navigating the Austrian RIS API (Federal Law Gazette / BgblAuth). These scripts show future agents exactly how to search by title (`search_ris.py`), retrieve specific PDF download links by ID (`inspect_bgbl.py`), and automatically download and convert Austrian legal PDFs into Markdown (`fetch_bgbl_pdfs.py`). Use these when fixing missing legislation for Austria.
