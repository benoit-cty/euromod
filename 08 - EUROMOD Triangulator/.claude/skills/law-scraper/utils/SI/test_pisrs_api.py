import httpx

url = "https://pisrs.si/api/predpis/dokument/ZAKO213"
headers = {"User-Agent": "Mozilla/5.0"}
r = httpx.get(url, headers=headers, verify=False, follow_redirects=True)
print(r.status_code)
print(r.text[:1000])
