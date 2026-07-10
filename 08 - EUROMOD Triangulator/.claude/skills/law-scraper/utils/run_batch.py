import httpx
import logging
import time
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import sys

# Try to import curl_cffi for the fallback ladder
try:
    from curl_cffi import requests as cffi_requests
    HAS_CFFI = True
except ImportError:
    HAS_CFFI = False

# Generic Batch URL Scraper
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {"User-Agent": USER_AGENT}
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "form", "meta", "link"]):
        tag.decompose()
    return soup.get_text(separator="\n\n", strip=True)

def fetch_url(client, url):
    """The HTTP Client Ladder: Tries httpx first, falls back to curl_cffi if blocked."""
    try:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.content
    except httpx.HTTPStatusError as e:
        # 403 Forbidden, 401 Unauthorized, 503 Service Unavailable (often Cloudflare)
        if e.response.status_code in [403, 401, 503] and HAS_CFFI:
            log.warning(f"Got {e.response.status_code} for {url}. Falling back to curl_cffi impersonation...")
            fallback_resp = cffi_requests.get(url, impersonate="chrome120")
            if fallback_resp.status_code == 200:
                log.info(f"Fallback successful for {url}")
                return fallback_resp.content
        raise e
    except Exception as e:
        # For SSL errors or generic connection resets, try fallback too
        if HAS_CFFI and ("SSL" in str(e) or "Connect" in str(e)):
            log.warning(f"Got connection/SSL error for {url}. Falling back to curl_cffi...")
            try:
                fallback_resp = cffi_requests.get(url, impersonate="chrome120")
                if fallback_resp.status_code == 200:
                    log.info(f"Fallback successful for {url}")
                    return fallback_resp.content
            except Exception as fallback_e:
                raise e # raise original if fallback also fails
        raise e

def run_scraper(cc):
    base_dir = Path(f"legislation/{cc}")
    raw_dir = base_dir / "raw"
    pending_file = base_dir / "PENDING.md"
    json_file = Path(f".copilot/skills/law-scraper/utils/{cc}/{cc}_filtered_urls.json")
    
    raw_dir.mkdir(parents=True, exist_ok=True)
    pending = []
    
    # Check if there are implicit laws that need manual fetching
    implicit_file = Path(f".copilot/skills/law-scraper/utils/{cc}/{cc}_laws_extracted.json")
    if implicit_file.exists():
        implicit_laws = json.loads(implicit_file.read_text(encoding='utf-8'))
        for law in implicit_laws:
            pending.append({"name": law, "url": "Implicit Citation", "error": "Needs manual lookup or specialized scraper in national gazette"})
    
    if not json_file.exists():
        log.warning(f"No URLs to scrape for {cc}")
    else:
        urls = json.loads(json_file.read_text(encoding='utf-8'))
        with httpx.Client(headers=HEADERS, follow_redirects=True, verify=False, timeout=30) as client:
            for name, url in urls.items():
                raw_file = raw_dir / f"{name}.html"
                md_file = base_dir / f"{name}.md"
                
                # Check for PDF
                if url.lower().endswith('.pdf'):
                    raw_file = raw_dir / f"{name}.pdf"
                    
                if not raw_file.exists():
                    try:
                        content = fetch_url(client, url)
                        raw_file.write_bytes(content)
                        log.info(f"[{cc}] Saved {name}")
                    except Exception as e:
                        log.error(f"[{cc}] Failed {name}: {e}")
                        pending.append({"name": name, "url": url, "error": str(e)})
                        continue
                
                if raw_file.exists() and not md_file.exists():
                    try:
                        if raw_file.suffix == '.pdf':
                            import fitz
                            doc = fitz.open(raw_file)
                            text = "".join(page.get_text() + "\n\n" for page in doc)
                            md_file.write_text(text, encoding="utf-8", errors="ignore")
                        else:
                            html_content = raw_file.read_text(encoding="utf-8", errors="ignore")
                            text = clean_html(html_content)
                            md_file.write_text(text, encoding="utf-8", errors="ignore")
                        log.info(f"[{cc}] Converted {name}")
                    except Exception as e:
                        log.error(f"[{cc}] Conversion failed {name}: {e}")
                        pending.append({"name": name, "url": url, "error": str(e)})
                        
                time.sleep(1)

    if pending:
        # Write/Append to PENDING.md
        mode = "a" if pending_file.exists() else "w"
        with open(pending_file, mode, encoding="utf-8") as f:
            if mode == "w": f.write(f"# Pending Legislation for {cc}\n\n")
            for p in pending:
                f.write(f"## {p['name']}\n- **URL**: {p['url']}\n- **Error**: `{p['error']}`\n\n")
        log.info(f"[{cc}] Logged {len(pending)} pending items.")
    elif pending_file.exists():
        pending_file.unlink()

if __name__ == "__main__":
    batch = sys.argv[1:] if len(sys.argv) > 1 else ["BG", "CY", "CZ", "DE", "DK"]
    for country in batch:
        log.info(f"--- Starting {country} ---")
        run_scraper(country)
