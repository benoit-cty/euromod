# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
# ]
# ///
"""
Scraper: Czech Republic (CZ)
"""
import httpx
import logging
import time
from pathlib import Path
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {"User-Agent": USER_AGENT}
BASE_DIR = Path("legislation/CZ")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"

URLS = {
    "MPSV_Material_Need": "https://www.mpsv.cz/web/en/assistance-in-material-need",
    "MPSV_Disability": "https://www.mpsv.cz/web/en/disability",
    "MPSV_Family": "https://www.mpsv.cz/web/en/family",
    "MPSV_Pensions": "https://www.mpsv.cz/web/en/pensions",
    "MPSV_Sickness_Insurance": "https://www.mpsv.cz/web/en/sickness-insurance",
    "MPSV_State_Social_Support": "https://www.mpsv.cz/web/en/state-social-support"
}

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def clean_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "form", "meta", "link"]):
        tag.decompose()
    return str(soup.body) if soup.body else str(soup)

def scrape():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pending = []
    
    with httpx.Client(headers=HEADERS, follow_redirects=True, verify=False) as client:
        for name, url in URLS.items():
            raw_file = RAW_DIR / f"{name}.html"
            md_file = BASE_DIR / f"{name}.md"
            
            if not raw_file.exists():
                try:
                    resp = client.get(url, timeout=30)
                    resp.raise_for_status()
                    raw_file.write_bytes(resp.content)
                    log.info(f"Saved {name}")
                except Exception as e:
                    log.error(f"Failed {name}: {e}")
                    pending.append({"name": name, "url": url, "error": str(e)})
                    continue
            
            if raw_file.exists() and not md_file.exists():
                try:
                    html_content = raw_file.read_text(encoding="utf-8", errors="ignore")
                    cleaned = clean_html(html_content)
                    text = BeautifulSoup(cleaned, "html.parser").get_text(separator="\n\n", strip=True)
                    md_file.write_text(text, encoding="utf-8", errors="ignore")
                    log.info(f"Converted {name}")
                except Exception as e:
                    log.error(f"MD Conversion failed {name}: {e}")
                    
            time.sleep(2)
            
    if pending:
        with open(PENDING_FILE, "w", encoding="utf-8") as f:
            f.write("# Pending\n\n")
            for p in pending:
                f.write(f"- {p['name']}: {p['url']} ({p['error']})\n")

if __name__ == "__main__":
    scrape()