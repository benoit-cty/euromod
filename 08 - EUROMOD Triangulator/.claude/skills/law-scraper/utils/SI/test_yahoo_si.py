from curl_cffi import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def yahoo_resolve_law(query):
    url = "https://search.yahoo.com/search"
    # broader search
    params = {"p": f"site:pisrs.si/Pis.web/pregledPredpisa {query}"}
    
    r = requests.get(url, params=params, impersonate="chrome120", timeout=15.0)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    for div in soup.find_all('div', class_='compTitle'):
        a = div.find('a')
        if a:
            href = a.get('href', '')
            if 'RU=' in href:
                ru = href.split('RU=')[1].split('/RK=')[0]
                real_url = urllib.parse.unquote(ru)
                if 'pisrs.si/Pis.web/pregledPredpisa' in real_url:
                    print(f"Found: {real_url}")
                    return real_url
    return None

yahoo_resolve_law("Zakon o dolgotrajni oskrbi")
yahoo_resolve_law("Zakon o dohodnini")
yahoo_resolve_law("Personal Income Tax Act")
