from curl_cffi import requests
from bs4 import BeautifulSoup
import re

def search_lex_bg(title):
    print(f"Searching lex.bg for: {title}")
    url = "https://lex.bg/search"
    params = {
        "searchBox": title,
        "search_for_all": "0",
        "search_for_spravochnik": "1",
        "search_for_acts": "1",
        "sprav_filter[]": ["laws", "code"]
    }
    # Important to set impersonate to bypass potential blocks
    r = requests.post(url, data=params, impersonate="chrome120", verify=False)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if '/ldoc/' in href:
            print(f"Found: {a.text.strip()} -> {href}")

search_lex_bg("Закон за закрила на детето")
