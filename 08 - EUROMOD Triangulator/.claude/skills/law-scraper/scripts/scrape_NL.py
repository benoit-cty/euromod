import httpx
import logging
import time
import json
import re
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
BASE_DIR = Path("legislation/NL")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"
IMPLICIT_FILE = Path(".copilot/skills/law-scraper/utils/NL/NL_laws_extracted.json")
TARGET_DATE = "2023-01-01"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def yahoo_resolve_law(query, use_quotes=True):
    """Uses Yahoo search to resolve an implicit law title to a wetten.overheid.nl URL."""
    url = "https://search.yahoo.com/search"
    if use_quotes:
        params = {"p": f"site:wetten.overheid.nl \"{query}\""}
    else:
        params = {"p": f"site:wetten.overheid.nl {query}"}
    
    try:
        r = cffi_requests.get(url, params=params, impersonate="chrome120", timeout=15.0)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for div in soup.find_all('div', class_='compTitle'):
            a = div.find('a')
            if a:
                href = a.get('href', '')
                if 'RU=' in href:
                    ru = href.split('RU=')[1].split('/RK=')[0]
                    real_url = urllib.parse.unquote(ru)
                    # We are looking for the root document ID
                    if 'wetten.overheid.nl/jci1.3:c:BWBR' in real_url or 'wetten.overheid.nl/BWBR' in real_url:
                        # Normalize to the jci path so we can cleanly append parameters
                        match = re.search(r'(BWBR\d+)', real_url)
                        if match:
                            bwbr = match.group(1)
                            clean_url = f"https://wetten.overheid.nl/jci1.3:c:{bwbr}&z={TARGET_DATE}&g={TARGET_DATE}"
                            return clean_url
        return None
    except Exception as e:
        log.warning(f"Yahoo resolution failed for '{query}': {e}")
        return None

def clean_nl_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    content = soup.find('main')
    if not content:
        content = soup.body if soup.body else soup
        
    for tag in content(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "form", "meta", "link"]):
        tag.decompose()
    
    # Remove some interactive fluff
    for tag in content.select('.help-links, .info-balk, .wetstechnische-informatie'):
        tag.decompose()
        
    text = content.get_text(separator="\n\n", strip=True)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def scrape():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pending = []
    
    if not IMPLICIT_FILE.exists():
        log.error(f"{IMPLICIT_FILE} not found.")
        return
        
    laws = json.loads(IMPLICIT_FILE.read_text(encoding='utf-8'))
    log.info(f"Loaded {len(laws)} implicit Dutch laws to resolve.")
    
    for law_title in laws:
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', law_title)
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')
        
        md_file = BASE_DIR / f"{safe_name}.md"
        raw_file = RAW_DIR / f"{safe_name}.html"
        
        if md_file.exists():
            log.info(f"Skipping {law_title}, already downloaded.")
            continue
            
        log.info(f"Resolving via Yahoo: {law_title}")
        url = yahoo_resolve_law(law_title, use_quotes=True)
        
        if not url:
            log.info(f"Retrying without quotes: {law_title}")
            url = yahoo_resolve_law(law_title, use_quotes=False)
            
        if not url:
            log.warning(f"Could not resolve URL for {law_title}")
            pending.append({"name": law_title, "url": "Yahoo Search", "error": "Not found in Yahoo mapping to wetten.overheid.nl"})
            time.sleep(3)
            continue
            
        log.info(f"Found URL: {url}")
        
        if not raw_file.exists():
            try:
                # Use curl_cffi for wetten.overheid.nl to avoid 429
                resp = cffi_requests.get(url, impersonate="chrome120", timeout=30.0)
                if resp.status_code == 200:
                    raw_file.write_bytes(resp.content)
                    log.info(f"Saved raw HTML for {law_title}")
                else:
                    log.error(f"Failed to download {url}: {resp.status_code}")
                    pending.append({"name": law_title, "url": url, "error": f"HTTP {resp.status_code}"})
                    continue
            except Exception as e:
                log.error(f"Failed to download {url}: {e}")
                pending.append({"name": law_title, "url": url, "error": str(e)})
                time.sleep(2)
                continue
                
        if raw_file.exists():
            try:
                html_content = raw_file.read_text(encoding="utf-8", errors="ignore")
                text = clean_nl_html(html_content)
                if text:
                    md_file.write_text(text, encoding="utf-8", errors="ignore")
                    log.info(f"Converted {law_title} to Markdown")
                else:
                    log.error(f"Empty text extraction for {law_title}")
                    pending.append({"name": law_title, "url": url, "error": "Empty extraction"})
            except Exception as e:
                log.error(f"MD Conversion failed for {law_title}: {e}")
                pending.append({"name": law_title, "url": url, "error": str(e)})
                
        time.sleep(3) # Politeness
            
    if pending:
        mode = "a" if PENDING_FILE.exists() else "w"
        with open(PENDING_FILE, mode, encoding="utf-8") as f:
            if mode == "w": f.write("# Pending Legislation for NL\n\n")
            for p in pending:
                f.write(f"## {p['name']}\n- **URL**: {p['url']}\n- **Error**: `{p['error']}`\n\n")
        log.info(f"Updated PENDING.md with {len(pending)} items.")

if __name__ == "__main__":
    scrape()
