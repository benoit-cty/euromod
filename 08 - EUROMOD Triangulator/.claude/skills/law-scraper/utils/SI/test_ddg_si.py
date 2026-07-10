from curl_cffi import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def ddg_lite(query):
    url = "https://lite.duckduckgo.com/lite/"
    data = {"q": f"site:pisrs.si {query}"}
    r = requests.post(url, data=data, impersonate="chrome120")
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', class_='result-url'):
        href = a.get('href', '')
        print("Raw link:", href)

ddg_lite("Zakon o dolgotrajni oskrbi")
