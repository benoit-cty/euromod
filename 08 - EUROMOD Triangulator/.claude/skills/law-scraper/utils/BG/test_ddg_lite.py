from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def ddg_lite(query):
    url = "https://lite.duckduckgo.com/lite/"
    data = {"q": f"site:lex.bg/laws/ldoc {query}"}
    r = requests.post(url, data=data, impersonate="chrome120")
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    for a in soup.find_all('a', class_='result-url'):
        href = a.get('href', '')
        print("Href:", href)
        
ddg_lite("Кодекс на труда")
