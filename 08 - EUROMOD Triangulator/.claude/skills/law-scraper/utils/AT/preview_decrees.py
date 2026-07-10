import httpx
from bs4 import BeautifulSoup

def get_text_preview(g_id):
    url = f"https://www.ris.bka.gv.at/GeltendeFassung.wxe?Abfrage=Bundesnormen&Gesetzesnummer={g_id}"
    r = httpx.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "meta", "link"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = text.split('\n')
    # Print the first 10 non-empty lines
    non_empty = [l for l in lines if l.strip()][:10]
    print(f"\n--- ID: {g_id} ---")
    print('\n'.join(non_empty))

ids = ['20012951', '20013042', '20012881', '20012102']
for i in ids:
    get_text_preview(i)
