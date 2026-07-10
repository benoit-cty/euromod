import json

with open('es_laws_extracted.json', 'r', encoding='utf-8') as f:
    laws = json.load(f)

# Read the existing ES.md
with open('legislation-sources/ES.md', 'r', encoding='utf-8') as f:
    es_md = f.read()

# Group laws by type
grouped = {}
for law in laws:
    l_type = law['type']
    if l_type not in grouped:
        grouped[l_type] = []
    grouped[l_type].append(law)

# Prepare markdown to append
md_append = "\n\n## Extracted Law Citations (Text-based)\n"
md_append += "The following laws were cited by name in the text but lacked direct URLs. They need to be retrieved via the BOE or regional gazettes.\n\n"

# Define order of importance
order = ['Ley', 'Ley Orgánica', 'Real Decreto-ley', 'Real Decreto Legislativo', 'Real Decreto', 'Decreto-ley', 'Decreto Legislativo', 'Decreto']

for ot in order:
    if ot in grouped:
        md_append += f"### {ot}\n"
        # Sort by year then number
        def sort_key(l):
            parts = l['number'].split('/')
            if len(parts) == 2:
                num, year = parts
                return (year, num.zfill(4))
            return l['number']
            
        grouped[ot].sort(key=sort_key)
        for l in grouped[ot]:
            title = l['title'].strip()
            # Clean up leading commas
            if title.startswith(','):
                title = title[1:].strip()
            citation = f"{l['type']} {l['number']}"
            if title:
                citation += f", {title}"
            
            # Format markdown row
            # We add a placeholder for BOE link
            md_append += f"- **{l['type']} {l['number']}**"
            if title:
                md_append += f": {title}"
            md_append += " `[PENDING BOE/GAZETTE FETCH]`\n"
        md_append += "\n"

# Write back
with open('legislation-sources/ES.md', 'w', encoding='utf-8') as f:
    f.write(es_md.strip() + md_append)
