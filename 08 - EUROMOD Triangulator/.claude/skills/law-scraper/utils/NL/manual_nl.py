import httpx
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
from curl_cffi import requests as cffi_requests

TARGET_DATE = "2023-01-01"
BASE_DIR = Path("legislation/NL")
RAW_DIR = BASE_DIR / "raw"

MANUAL_IDS = {
    "Toeslagenwet": "BWBR0004043",
    "Werkloosheidswet": "BWBR0004045",
    "Wet_Inkomensvoorziening_Oudere": "BWBR0004044", # IOAW
    "Wet_Langdurige_Zorg": "BWBR0035917",
    "Wet_Uitbreiding_Loondoorbetalingsverplichting_Bij_Ziekte": "BWBR0008544"
}

def clean_nl_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    content = soup.find('main')
    if not content:
        content = soup.body if soup.body else soup
    for tag in content(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "form", "meta", "link"]):
        tag.decompose()
    for tag in content.select('.help-links, .info-balk, .wetstechnische-informatie'):
        tag.decompose()
    text = content.get_text(separator="\n\n", strip=True)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

for name, bwbr in MANUAL_IDS.items():
    print(f"Downloading {name}...")
    url = f"https://wetten.overheid.nl/jci1.3:c:{bwbr}&z={TARGET_DATE}&g={TARGET_DATE}"
    resp = cffi_requests.get(url, impersonate="chrome120")
    if resp.status_code == 200:
        raw_file = RAW_DIR / f"{name}.html"
        md_file = BASE_DIR / f"{name}.md"
        raw_file.write_bytes(resp.content)
        text = clean_nl_html(resp.text)
        md_file.write_text(text, encoding="utf-8")
        print(f"Saved {name}")
    else:
        print(f"Failed {name}")
