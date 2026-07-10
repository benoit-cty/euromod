# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
#     "pypandoc",
# ]
# ///
"""
Scraper: Belgium (BE) — Tax and Benefit Legislation
Discovery: Mixed sources (Fisconet, Social Security, Regional Portals)
"""

import httpx
import logging
import time
import os
import json
import pypandoc
from pathlib import Path
from bs4 import BeautifulSoup

# ⚙️ Configuration ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}
REQUEST_DELAY = 2.0
MAX_RETRIES = 1
RETRY_BACKOFF = [2]

BASE_DIR = Path("legislation/BE")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"
JSON_FILE = Path(".copilot/skills/law-scraper/utils/BE/be_filtered_urls.json")

# 📝 Logging ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def clean_html(html_text):
    """Strips out boilerplate navigation, scripts, and styling to produce clean Markdown."""
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "form", "meta", "link"]):
        tag.decompose()
    # Belgium specific hidden classes and menus
    for hidden in soup.select(".hidden, .sr-only, .visually-hidden, .menu, .navbar, #header, #footer"):
        hidden.decompose()
        
    content = soup.select_one("main, .main-content, #main-content, article, .content")
    if content:
        return str(content)
    elif soup.body:
        return str(soup.body)
    return str(soup)

def fetch_with_retry(client, url, timeout=60):
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.get(url, timeout=timeout)
            if resp.status_code in [429, 503]:
                log.warning(f"Server returned {resp.status_code}. Sleeping {RETRY_BACKOFF[attempt]}s")
                time.sleep(RETRY_BACKOFF[attempt])
                continue
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                log.warning(f"Error {e}. Retrying in {RETRY_BACKOFF[attempt]}s...")
                time.sleep(RETRY_BACKOFF[attempt])
                continue
            raise e

def scrape():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pending_items = []
    
    if not JSON_FILE.exists():
        log.error(f"{JSON_FILE} not found. Run the extraction script first.")
        return
        
    with open(JSON_FILE, "r") as f:
        urls = json.load(f)
    
    with httpx.Client(headers=HEADERS, follow_redirects=True, http2=True) as client:
        for name, url in urls.items():
            log.info(f"Processing {name}")
            raw_file = RAW_DIR / f"{name}.html"
            md_file = BASE_DIR / f"{name}.md"
            
            if not raw_file.exists():
                try:
                    resp = fetch_with_retry(client, url)
                    
                    # Detect SPA empty shell (Heuristic: very small file size and lack of core tags)
                    if "minfin" in url and (len(resp.text) < 10000 or "MyMinfin" in resp.text and "Angular" in resp.text):
                        log.warning(f"{name} appears to be a dynamic SPA shell with no content. Flagging as Pending.")
                        pending_items.append({"name": name, "url": url, "error": "SPA Empty Shell / Needs Manual Save"})
                        continue

                    with open(raw_file, "w", encoding="utf-8") as f:
                        f.write(resp.text)
                    log.info(f"Saved raw HTML: {raw_file.name}")
                    
                except Exception as e:
                    log.error(f"Failed {name}: {e}")
                    pending_items.append({"name": name, "url": url, "error": str(e)})
                    continue

            if raw_file.exists() and not md_file.exists():
                try:
                    with open(raw_file, "r", encoding="utf-8") as f:
                        raw_html = f.read()
                        
                    cleaned_html = clean_html(raw_html)
                    
                    soup = BeautifulSoup(cleaned_html, "html.parser")
                    output = soup.get_text(separator="\n\n", strip=True)
                    
                    with open(md_file, "w", encoding="utf-8", errors="ignore") as f:
                        f.write(output)
                    log.info(f"Converted: {md_file.name}")
                except Exception as e:
                    log.error(f"MD Conversion failed {name}: {e}")

            time.sleep(REQUEST_DELAY)

    if pending_items:
        with open(PENDING_FILE, "w", encoding="utf-8") as pf:
            pf.write("# Pending Legislation for BE\n\n")
            for item in pending_items:
                pf.write(f"## {item['name']}\n- **URL**: {item['url']}\n- **Error**: `{item['error']}`\n")
                if "minfin" in item['url']:
                    pf.write("- **Manual Instructions**: The Belgian MinFin portal uses a modern SPA architecture protected by SSO. Please open the URL in a browser, let it load, and use 'Save As... Webpage Complete' or copy the text manually into `legislation/BE/raw/`.\n")
        log.info(f"Updated PENDING.md")

if __name__ == "__main__":
    scrape()
