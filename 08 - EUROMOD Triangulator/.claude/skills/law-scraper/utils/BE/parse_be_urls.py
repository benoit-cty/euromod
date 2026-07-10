import re
import json

with open('legislation-sources/BE.md', 'r', encoding='utf-8') as f:
    text = f.read()

urls = re.findall(r'- \[(http.*?)\]', text)
unique_urls = sorted(list(set(urls)))

print(f"Found {len(unique_urls)} explicit URLs in BE.md")
for i, url in enumerate(unique_urls):
    print(f"{i}: {url}")

with open('.copilot/skills/law-scraper/utils/BE/be_urls.json', 'w') as f:
    json.dump(unique_urls, f, indent=2)
