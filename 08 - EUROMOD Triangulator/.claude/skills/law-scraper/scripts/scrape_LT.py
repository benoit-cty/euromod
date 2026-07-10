# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
#     "PyMuPDF",
# ]
# ///
"""
Scraper: Lithuania (LT)
"""
import httpx
import logging
import time
from pathlib import Path
from bs4 import BeautifulSoup
import fitz

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {"User-Agent": USER_AGENT}
BASE_DIR = Path("legislation/LT")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"

URLS = {
    "eTAR_09329240aa5611eab9d9cd0c85e0b745": "https://www.e-tar.lt/portal/legalAct.html?documentId=09329240aa5611eab9d9cd0c85e0b745",
    "eTAR_250ebe404a6e11e6b5d09300a16a686c": "https://www.e-tar.lt/portal/legalAct.html?documentId=250ebe404a6e11e6b5d09300a16a686c",
    "eTAR_6ac80c5029a511eb932eb1ed7f923910": "https://www.e-tar.lt/portal/legalAct.html?documentId=6ac80c5029a511eb932eb1ed7f923910",
    "eTAR_732a064025be11eb932eb1ed7f923910": "https://www.e-tar.lt/portal/legalAct.html?documentId=732a064025be11eb932eb1ed7f923910",
    "eTAR_8e886460a8ad11e5be7fbe3f919a1ebe": "https://www.e-tar.lt/portal/legalAct.html?documentId=8e886460a8ad11e5be7fbe3f919a1ebe",
    "eTAR_95e6c310450a11eb8d9fe110e148c770": "https://www.e-tar.lt/portal/legalAct.html?documentId=95e6c310450a11eb8d9fe110e148c770",
    "eTAR_964f55405d9311eca9ac839120d251c4": "https://www.e-tar.lt/portal/legalAct.html?documentId=964f55405d9311eca9ac839120d251c4",
    "eTAR_a235e98049e611eb8d9fe110e148c770": "https://www.e-tar.lt/portal/legalAct.html?documentId=a235e98049e611eb8d9fe110e148c770",
    "eTAR_be79ae40044911e9a5eaf2cd290f1944": "https://www.e-tar.lt/portal/legalAct.html?documentId=be79ae40044911e9a5eaf2cd290f1944",
    "eTAR_c176eaf03ede11eb8d9fe110e148c770": "https://www.e-tar.lt/portal/legalAct.html?documentId=c176eaf03ede11eb8d9fe110e148c770",
    "eTAR_5fc0c06002b311e9a5eaf2cd290f1944": "https://www.e-tar.lt/portal/lt/legalAct/5fc0c06002b311e9a5eaf2cd290f1944",
    "eTAR_TAR_2CE6CFE9E2EE": "https://www.e-tar.lt/portal/lt/legalAct/TAR.2CE6CFE9E2EE",
    "eTAR_TAR_C677663D2202": "https://www.e-tar.lt/portal/lt/legalAct/TAR.C677663D2202/asr",
    "eTAR_f5ee93504a6e11e6b5d09300a16a686c": "https://www.e-tar.lt/portal/lt/legalAct/f5ee93504a6e11e6b5d09300a16a686c",
    "Sodra_Tarifai": "https://www.sodra.lt/lt/situacijos/imoku-tarifai/imoku-tarifai-savarankiskai-dirbantiems?lang=en",
    "Sodra_Amziaus_Lentele": "https://sodra.lt/senatves-pensijos-amziaus-lentele"
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
            ext = "pdf" if url.lower().endswith(".pdf") else "html"
            raw_file = RAW_DIR / f"{name}.{ext}"
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
                    if ext == "pdf":
                        doc = fitz.open(raw_file)
                        text = "".join(page.get_text() + "\n\n" for page in doc)
                        md_file.write_text(text, encoding="utf-8", errors="ignore")
                    else:
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