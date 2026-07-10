from curl_cffi import requests
from bs4 import BeautifulSoup

def search_wetten(title):
    print(f"Searching wetten.overheid.nl for: {title}")
    url = "https://wetten.overheid.nl/zoeken"
    params = {"ZoekOp_Titel": title}
    try:
        r = requests.get(url, params=params, impersonate="chrome120")
        print(f"Status: {r.status_code}")
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Results list?
        results = soup.select('a')
        found = False
        for a in results:
            href = a.get('href', '')
            if 'BWBR' in href and 'zoeken' not in href: # BWBR is typical ID prefix in wetten.overheid.nl
                print(f"Found: {a.text.strip()} -> {href}")
                found = True
                
        if not found:
            print("No links with BWBR found")
            
    except Exception as e:
        print(f"Error: {e}")

search_wetten("Participatiewet")
