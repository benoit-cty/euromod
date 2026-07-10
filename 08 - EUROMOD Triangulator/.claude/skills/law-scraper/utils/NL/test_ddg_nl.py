from curl_cffi import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def ddg_lite(query):
    url = "https://lite.duckduckgo.com/lite/"
    data = {"q": f"site:wetten.overheid.nl/BWBR {query}"}
    r = requests.post(url, data=data, impersonate="chrome120")
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', class_='result-url'):
        href = a.get('href', '')
        if 'BWBR' in href:
            match = re.search(r'(BWBR\d+)', href)
            if match:
                print(f"Found {query}: {match.group(1)}")
                return

ddg_lite("Toeslagenwet")
ddg_lite("Werkloosheidswet")
ddg_lite("Wet langdurige zorg")
ddg_lite("Wet uitbreiding loondoorbetalingsverplichting bij ziekte")
