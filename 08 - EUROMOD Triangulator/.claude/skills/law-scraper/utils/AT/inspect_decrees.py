import httpx
import re
from bs4 import BeautifulSoup

def get_title(g_id):
    url = f"https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer={g_id}"
    r = httpx.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    title_el = soup.find('h1', class_='Titel')
    if title_el:
        return title_el.text.strip()
    return "Unknown Title"

# The IDs we found for Valorisierung
val_ids = ['20012951', '20013042', '20012881']
print("--- Valorisierung IDs ---")
for v_id in val_ids:
    print(f"{v_id}: {get_title(v_id)}")

def search_ris_full(term):
    url = f"https://www.ris.bka.gv.at/Ergebnis.wxe?Abfrage=Bundesnormen&Suchworte={term}&SearchInBundesnormen=True"
    r = httpx.get(url, verify=False)
    ids = set(re.findall(r'Gesetzesnummer=(\d{8})', r.text))
    return list(ids)

print("\n--- Broad Searches ---")
# Limit to first few
aw_ids = search_ris_full("Aufwertungsverordnung")
print("Aufwertungsverordnung (first 5):")
for i in aw_ids[:5]:
    print(f"  {i}: {get_title(i)}")

kp_ids = search_ris_full("Kalte-Progression")
print("Kalte-Progression (first 5):")
for i in kp_ids[:5]:
    print(f"  {i}: {get_title(i)}")

