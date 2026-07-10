import httpx
from bs4 import BeautifulSoup

with httpx.Client(verify=False, follow_redirects=True) as client:
    r = client.get("https://lex.bg/bg/laws/search")
    soup = BeautifulSoup(r.text, 'html.parser')
    forms = soup.find_all('form')
    for i, form in enumerate(forms):
        print(f"--- Form {i} ---")
        print(f"Action: {form.get('action')}")
        for input_tag in form.find_all(["input", "select"]):
            print(f"  {input_tag.get('name')} = {input_tag.get('value')}")
