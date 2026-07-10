import httpx
from bs4 import BeautifulSoup

url = "https://www.boe.es/buscar/act.php?id=BOE-A-2022-22128"
headers = {"User-Agent": "Mozilla/5.0"}
with httpx.Client(headers=headers, verify=False, timeout=60.0) as client:
    r = client.get(url, follow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find("div", id="textoxslt")
    
    if content:
        # Check for indice
        indice = content.find("div", class_="indice")
        if indice: print("Found class='indice'")
        
        indice_acc = content.find("div", class_="acc-indice")
        if indice_acc: print("Found class='acc-indice'")
        
        # See what elements are at the top
        print(content.prettify()[:1000])
