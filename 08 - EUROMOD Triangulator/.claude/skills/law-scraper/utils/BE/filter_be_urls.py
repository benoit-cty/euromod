import json
import re
from urllib.parse import urlparse

with open('.copilot/skills/law-scraper/utils/BE/be_urls.json', 'r') as f:
    urls = json.load(f)

# Filters out useless urls
blocked_domains = ['euromod-web', 'eurostat', 'oecd', 'dx.doi.org', 'plan.be', 'nbb.be', 'iser.essex.ac.uk', 'economy-finance.ec.europa.eu']

filtered_urls = {}
for url in urls:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    if any(b in domain for b in blocked_domains):
        continue
        
    # Generate a name
    # e.g., www.groeipakket.be/bedragen -> groeipakket_be_bedragen
    # e.g., be.brussels/nl/belastingen-financien/... -> be_brussels_belastingen...
    
    parts = [domain.replace("www.", "").replace(".", "_")]
    path_parts = [p for p in parsed.path.split('/') if p and p not in ['nl', 'fr', 'en', 'latest', 'instructions', 'document', 'pages', 'public', 'fisconet', 'thema-s', 'bedragen-en-loonplafonds-uitkeringen', 'bedragen-en-loonplafonds', 'employer', 'dmfa']]
    
    # Take last 2 meaningful parts of path
    if path_parts:
        parts.extend(path_parts[-2:])
        
    name = "_".join(parts)
    # limit length and clean
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    if len(name) > 60:
        name = name[:60]
        
    filtered_urls[name] = url

print(f"Filtered down to {len(filtered_urls)} legislative URLs.")
for k, v in filtered_urls.items():
    print(f"{k}: {v}")

with open('.copilot/skills/law-scraper/utils/BE/be_filtered_urls.json', 'w') as f:
    json.dump(filtered_urls, f, indent=2)
