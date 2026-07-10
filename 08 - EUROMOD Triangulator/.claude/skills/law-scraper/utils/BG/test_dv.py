import httpx
from bs4 import BeautifulSoup

with httpx.Client(verify=False, follow_redirects=True) as client:
    r = client.get("https://dv.parliament.bg/DVWeb/broeveList.faces")
    print(f"Status: {r.status_code}")
    soup = BeautifulSoup(r.text, 'html.parser')
    forms = soup.find_all('form')
    for i, form in enumerate(forms):
        print(f"--- Form {i} --- Action: {form.get('action')}")
        for tag in form.find_all(['input', 'select']):
            print(f"  {tag.get('name')} = {tag.get('value')}")
