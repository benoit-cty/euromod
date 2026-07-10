import os
import json
import re
import sys
from pathlib import Path

# Helper script to consolidate the explicit URLs for the batch of countries
batch = sys.argv[1:] if len(sys.argv) > 1 else ["BG", "CY", "CZ", "DE", "DK"]
blocked_domains = ['euromod-web', 'eurostat', 'oecd', 'dx.doi.org']

for cc in batch:
    source_md = Path(f"legislation-sources/{cc}.md")
    out_dir = Path(f".copilot/skills/law-scraper/utils/{cc}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / f"{cc}_filtered_urls.json"
    
    if not source_md.exists():
        print(f"{cc} source MD missing.")
        continue
        
    text = source_md.read_text(encoding='utf-8')
    urls = re.findall(r'- \[(http.*?)\]', text)
    unique_urls = sorted(list(set(urls)))
    
    filtered = {}
    for url in unique_urls:
        if any(b in url for b in blocked_domains): continue
        
        # Simple name generation
        domain = url.split('/')[2].replace("www.", "").replace(".", "_")
        name = f"{domain}_{len(filtered)}"
        filtered[name] = url
        
    out_json.write_text(json.dumps(filtered, indent=2))
    print(f"{cc}: Extracted {len(filtered)} explicit URLs.")
