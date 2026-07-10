from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

def yahoo_search(query):
    url = "https://search.yahoo.com/search"
    params = {"p": f"site:lex.bg/laws/ldoc \"{query}\""}
    r = requests.get(url, params=params, impersonate="chrome120")
    soup = BeautifulSoup(r.text, 'html.parser')
    for div in soup.find_all('div', class_='compTitle'):
        a = div.find('a')
        if a:
            href = a.get('href', '')
            print("Link:", href)
            # Yahoo uses a redirect link like r.search.yahoo.com... RU=https://lex.bg...
            if 'RU=' in href:
                ru = href.split('RU=')[1].split('/')[0]
                real_url = urllib.parse.unquote(ru)
                print("Decoded:", real_url)

yahoo_search("Кодекс на труда")
