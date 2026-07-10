import json
import re

with open('legislation/BE/PENDING.md', 'r', encoding='utf-8') as f:
    pending_lines = f.readlines()

failed_urls = []
for line in pending_lines:
    if line.startswith('- **URL**: '):
        failed_urls.append(line.replace('- **URL**: ', '').strip())

with open('legislation-sources/BE.md', 'r', encoding='utf-8') as f:
    be_md = f.read()

new_lines = []
for line in be_md.split('\n'):
    if line.startswith('- [http'):
        url_match = re.search(r'\[(.*?)\]', line)
        if url_match:
            url = url_match.group(1)
            # Find if this URL is in the failed_urls
            if url in failed_urls:
                line += ' `[FAILED/PENDING]`'
            else:
                line += ' `[✅ DOWNLOADED]`'
    new_lines.append(line)

with open('legislation-sources/BE.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Updated BE.md statuses.")
