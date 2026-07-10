import httpx
from bs4 import BeautifulSoup

def test():
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    data = {"q": "site:lex.bg Закон за закрила на детето", "b": ""}
    with httpx.Client(follow_redirects=True) as client:
        r = client.post(url, headers=headers, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Look for any link
        links = soup.select('.result__a')
        for a in links[:3]:
            print(f"{a.text} -> {a.get('href')}")
test()
