import re

# Read PENDING.md to get failed laws
with open('legislation/ES/PENDING.md', 'r', encoding='utf-8') as f:
    pending_lines = f.readlines()

failed_laws = set()
for line in pending_lines:
    if line.startswith('- '):
        # Extract the law name, e.g., "- Decreto 179/2002: BOE Search..."
        law_name = line.split(':')[0].replace('- ', '').strip()
        failed_laws.add(law_name)

# Read the legislation-sources/ES.md
with open('legislation-sources/ES.md', 'r', encoding='utf-8') as f:
    es_md = f.read()

# Replace tags
new_lines = []
for line in es_md.split('\n'):
    if '`[PENDING BOE/GAZETTE FETCH]`' in line:
        # Extract the bolded law name: e.g., "- **Ley 38/1992**:"
        match = re.search(r'\*\*(.*?)\*\*', line)
        if match:
            law_name = match.group(1).strip()
            if law_name in failed_laws:
                line = line.replace('`[PENDING BOE/GAZETTE FETCH]`', '`[FAILED/PENDING]`')
            else:
                line = line.replace('`[PENDING BOE/GAZETTE FETCH]`', '`[✅ DOWNLOADED]`')
    new_lines.append(line)

with open('legislation-sources/ES.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print(f"Updated ES.md. Marked {len(failed_laws)} laws as failed/pending, rest as downloaded.")
