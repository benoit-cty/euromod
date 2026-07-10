import httpx
import re
from bs4 import BeautifulSoup

def search_bgbl(term):
    # Search in authentic BGBl (published daily)
    url = f"https://www.ris.bka.gv.at/Ergebnis.wxe?Abfrage=BgblAuth&Titel={term}&SearchInBgblAuth=True"
    r = httpx.get(url, verify=False)
    # The links to the PDFs or HTMLs usually look like: /Dokumente/BgblAuth/BGBLA_2024_II_.../BGBLA_...
    docs = re.findall(r'href="/Dokumente/BgblAuth/([^/]+)/', r.text)
    return list(set(docs))

def get_bgbl_title(doc_id):
    url = f"https://www.ris.bka.gv.at/Dokumente/BgblAuth/{doc_id}/{doc_id}.html"
    r = httpx.get(url, verify=False)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        # the title is often in a specific div or just the text
        return soup.get_text()[:200].replace('\n', ' ').strip()
    return "Error/PDF only"

print("Aufwertungsverordnung 2025:", search_bgbl("Aufwertungsverordnung 2025"))
print("Kalte Progression 2025:", search_bgbl("Kalte-Progression-Anpassungsverordnung 2025"))
print("Familienbeihilfe 2025:", search_bgbl("Familienbeihilfe"))
