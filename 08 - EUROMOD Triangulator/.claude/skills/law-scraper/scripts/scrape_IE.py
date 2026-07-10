# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "beautifulsoup4",
#     "PyMuPDF",
# ]
# ///
"""
Scraper: Ireland (IE)
"""
import httpx
import logging
import time
from pathlib import Path
from bs4 import BeautifulSoup
import fitz

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {"User-Agent": USER_AGENT}
BASE_DIR = Path("legislation/IE")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"

URLS = {
    "Gov_Rent_Limits": "https://www.gov.ie/en/publication/79fdae-maximum-rent-limits/",
    "Citizens_Guardians_NonContrib": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/death_related_benefits/guardians_payments.html",
    "Citizens_Widows_Contrib": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/death_related_benefits/widows_contrib_pension.html",
    "Citizens_Widows_NonContrib": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/death_related_benefits/widows_non_contrib_pen.html",
    "Citizens_Blind_Pension": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/disability_and_illness/blind_persons_pension.html",
    "Citizens_Disability_Allowance": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/disability_and_illness/disability_allowance.html",
    "Citizens_Invalidity_Pension": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/disability_and_illness/invalidity_pension.html",
    "Citizens_Farm_Assist": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/farming_and_fishing/farm_assist.html",
    "Citizens_State_Pension_Contrib": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/older_and_retired_people/state_pension_contributory.html",
    "Citizens_State_Pension_NonContrib": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/older_and_retired_people/state_pension_non_contributory.html",
    "Citizens_One_Parent_Family": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/social_welfare_payments_to_families_and_children/one_parent_family_payment.html",
    "Citizens_Jobseekers_Allowance": "https://www.citizensinformation.ie/en/social_welfare/social_welfare_payments/unemployed_people/jobseekers_allowance.html"
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