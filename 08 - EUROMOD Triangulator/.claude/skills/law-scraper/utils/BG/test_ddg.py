from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

def ddg_search(query):
    print(f"Searching DDG for: {query}")
    url = "https://html.duckduckgo.com/html/"
    r = requests.post(url, data={"q": query}, impersonate="chrome120")
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', class_='result__url'):
        href = a.get('href')
        if href:
            match = re.search(r'uddg=(https[^&]+)', href)
            if match:
                real_url = urllib.parse.unquote(match.group(1))
                print(f"Found: {real_url}")
                return real_url
    return None

import re
ddg_search('site:lex.bg "Закон за закрила на детето"')
