import httpx
from bs4 import BeautifulSoup
import re
import urllib.parse
from curl_cffi import requests as cffi_requests

def yahoo_resolve_law(query):
    url = "https://search.yahoo.com/search"
    params = {"p": f"site:wetten.overheid.nl \"{query}\""}
    
    r = cffi_requests.get(url, params=params, impersonate="chrome120", timeout=15.0)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    for div in soup.find_all('div', class_='compTitle'):
        a = div.find('a')
        if a:
            href = a.get('href', '')
            if 'RU=' in href:
                ru = href.split('RU=')[1].split('/RK=')[0]
                real_url = urllib.parse.unquote(ru)
                if 'wetten.overheid.nl' in real_url and 'BWBR' in real_url:
                    print(f"Found: {real_url}")
                    return real_url
    return None

yahoo_resolve_law("Participatiewet")
yahoo_resolve_law("Wet Arbeid en Zorg")
