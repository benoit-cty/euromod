from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = "https://wetten.overheid.nl/jci1.3:c:BWBR0015703&z=2023-01-01&g=2023-01-01"

r = requests.get(url, impersonate="chrome120")
soup = BeautifulSoup(r.text, 'html.parser')

main = soup.find('main') or soup.find(id=re.compile('content', re.I)) or soup.find(class_=re.compile('content', re.I))
if main:
    print(main.text[:500].strip())
else:
    print("Not found")
    print(r.text[:500])
