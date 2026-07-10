from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def bing_search(query):
    print(f"Searching Bing for: {query}")
    url = "https://www.bing.com/search"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, params=params, headers=headers, impersonate="chrome120")
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href')
        if href and 'lex.bg/laws/ldoc/' in href:
            print(f"Found: {href}")
            return href
    return None

bing_search('site:lex.bg "Закон за закрила на детето"')
bing_search('site:lex.bg "Кодекс на труда"')
