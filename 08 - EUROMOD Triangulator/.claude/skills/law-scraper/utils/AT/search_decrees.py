import httpx
import re
from bs4 import BeautifulSoup

def search_ris_title(title):
    url = f"https://www.ris.bka.gv.at/Ergebnis.wxe?Abfrage=Bundesnormen&Titel={title}&SearchInBundesnormen=True"
    r = httpx.get(url, verify=False)
    ids = set(re.findall(r'Gesetzesnummer=(\d{8})', r.text))
    return list(ids)

def search_ris_fulltext(text):
    # Search in full text (Suchworte)
    url = f"https://www.ris.bka.gv.at/Ergebnis.wxe?Abfrage=Bundesnormen&Suchworte={text}&SearchInBundesnormen=True"
    r = httpx.get(url, verify=False)
    ids = set(re.findall(r'Gesetzesnummer=(\d{8})', r.text))
    return list(ids)

print("Aufwertungsverordnung 2025:", search_ris_title("Aufwertungsverordnung 2025"))
print("Progression:", search_ris_title("Progression"))
print("Kalte Progression:", search_ris_title("Kalte Progression"))
print("Anpassungsverordnung 2025:", search_ris_title("Anpassungsverordnung 2025"))
print("Valorisierung 2025:", search_ris_title("Valorisierungsverordnung 2025"))
