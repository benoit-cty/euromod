from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def yahoo_resolve_law(query):
    url = "https://search.yahoo.com/search"
    params = {"p": f"site:wetten.overheid.nl {query}"}
    r = requests.get(url, params=params, impersonate="chrome120", timeout=15.0)
    soup = BeautifulSoup(r.text, 'html.parser')
    for div in soup.find_all('div', class_='compTitle'):
        a = div.find('a')
        if a:
            href = a.get('href', '')
            if 'RU=' in href:
                ru = href.split('RU=')[1].split('/RK=')[0]
                real_url = urllib.parse.unquote(ru)
                if 'BWBR' in real_url:
                    match = re.search(r'(BWBR\d+)', real_url)
                    if match:
                        bwbr = match.group(1)
                        print(f"Found {query}: {bwbr}")
                        return

yahoo_resolve_law("Algemene Ouderdomswet")
yahoo_resolve_law("Algemene Toeslagenwet")
yahoo_resolve_law("Toeslagenwet")
yahoo_resolve_law("Werkloosheidswet")
yahoo_resolve_law("Wet langdurige zorg")
