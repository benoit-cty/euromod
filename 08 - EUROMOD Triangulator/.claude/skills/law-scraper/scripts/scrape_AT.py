# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
#     "pypandoc",
# ]
# ///
"""
Scraper: Austria (AT) — Core Tax and Benefit Legislation
Discovery: REST/Query Parameters on ris.bka.gv.at (GeltendeFassung)
Usage:
    uv run scrape_AT.py
"""

import httpx
import logging
import time
import os
import pypandoc
from pathlib import Path
from bs4 import BeautifulSoup

# ── Configuration ──────────────────────────────────────────────
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
REQUEST_DELAY = 2.0  
MAX_RETRIES = 3
RETRY_BACKOFF = [5, 15, 30]

TARGET_DATE = "2025-01-01"
BASE_DIR = Path("legislation/AT")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"

LAWS = {
    "EStG_1988": "10004570", 
    "ASVG": "10008147",      
    "FLAG_1967": "10008220", 
    "AlVG_1977": "10008407", 
    "UStG_1994": "10004873",
    "BSVG": "20003779", 
    "GSVG": "10008422", 
    "FSVG": "10008423", 
    "IESG": "10008465", 
    "TabakStG": "10004877", 
    "BierStG": "10004874", 
    "KBGG": "20001474",      # Kinderbetreuungsgeldgesetz
    "SH-GG": "20010649",     # Sozialhilfe-Grundsatzgesetz
}

# ── Logging ────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def clean_html(html_text):
    """Strips out boilerplate navigation, scripts, and styling to produce clean Markdown."""
    soup = BeautifulSoup(html_text, "html.parser")
    # Decomposing the 'form' tag was deleting all content in RIS.
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "meta", "link"]):
        tag.decompose()
    
    body = soup.body
    if body:
        return str(body)
    return str(soup)

def fetch_with_retry(client: httpx.Client, url: str, params: dict = None, timeout: int = 120):
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.get(url, params=params, timeout=timeout)
            if resp.status_code in [429, 503]:
                log.warning(f"Server returned {resp.status_code}. Sleeping {RETRY_BACKOFF[attempt]}s")
                time.sleep(RETRY_BACKOFF[attempt])
                continue
            resp.raise_for_status()
            return resp
        except (httpx.ConnectError, httpx.ReadTimeout) as e:
            if attempt < MAX_RETRIES - 1:
                log.warning(f"Timeout/Connection error: {e}. Retrying in {RETRY_BACKOFF[attempt]}s...")
                time.sleep(RETRY_BACKOFF[attempt])
                continue
            raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {url}") from e

def scrape():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pending_items = []
    
    with httpx.Client(headers=HEADERS, follow_redirects=True, http2=True) as client:
        for name, gesetzesnummer in LAWS.items():
            log.info(f"Processing {name} (ID: {gesetzesnummer}) for {TARGET_DATE}")
            
            raw_file = RAW_DIR / f"{name}_{TARGET_DATE}.html"
            md_file = BASE_DIR / f"{name}_{TARGET_DATE}.md"
            
            # 1. Download HTML (if not already in raw)
            if not raw_file.exists():
                url = "https://www.ris.bka.gv.at/GeltendeFassung.wxe"
                params = {
                    "Abfrage": "Bundesnormen",
                    "Gesetzesnummer": gesetzesnummer,
                    "FassungVom": TARGET_DATE,
                    "ShowPrintPreview": "True"
                }
                
                try:
                    resp = fetch_with_retry(client, url, params=params)
                    with open(raw_file, "w", encoding="utf-8") as f:
                        f.write(resp.text)
                    log.info(f"Saved raw HTML: {raw_file.name}")
                except Exception as e:
                    log.error(f"Failed to download {name}: {e}")
                    pending_items.append({
                        "name": name,
                        "id": gesetzesnummer,
                        "url": f"https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer={gesetzesnummer}&FassungVom={TARGET_DATE}",
                        "error": str(e)
                    })
                    continue

            # 2. Convert to Markdown (if not already converted)
            if raw_file.exists() and not md_file.exists():
                try:
                    with open(raw_file, "r", encoding="utf-8") as f:
                        raw_html = f.read()
                        
                    cleaned_html = clean_html(raw_html)
                    
                    # Convert to MD
                    # Since pandoc seems to be struggling with some cleaned HTML structures, we will rely on BeautifulSoup to extract text as well if pandoc fails or produces empty.
                    # We will bypass pandoc for now to ensure we get data.
                    soup = BeautifulSoup(cleaned_html, "html.parser")
                    output = soup.get_text(separator="\n\n", strip=True)
                    # No encode/decode trick, just output

                    with open(md_file, "w", encoding="utf-8", errors="ignore") as f:
                        f.write(output)
                    log.info(f"Converted to Markdown: {md_file.name}")
                except Exception as e:
                    log.error(f"Conversion failed for {name}: {e}")

            time.sleep(REQUEST_DELAY)

    # 3. Handle PENDING.md
    if pending_items:
        with open(PENDING_FILE, "w", encoding="utf-8") as pf:
            pf.write(f"# Pending Legislation for AT (Date: {TARGET_DATE})\n\n")
            pf.write("The following legal texts could not be automatically downloaded or processed. ")
            pf.write("These must be resolved before triangulation can proceed.\n\n")
            for item in pending_items:
                pf.write(f"## {item['name']}\n")
                pf.write(f"- **RIS ID**: `{item['id']}`\n")
                pf.write(f"- **Target URL**: [Link]({item['url']})\n")
                pf.write(f"- **Status/Error**: `{item['error']}`\n")
                pf.write("- **Manual Instructions**: Search the title on [RIS](https://www.ris.bka.gv.at), ")
                pf.write("select the version from 01.01.2023, and save as HTML 'Print Preview' into `legislation/AT/raw/`.\n\n")
        log.info(f"Created PENDING.md with {len(pending_items)} items.")
    elif PENDING_FILE.exists():
        PENDING_FILE.unlink()
        log.info("All items resolved. Removed PENDING.md.")

if __name__ == "__main__":
    scrape()

