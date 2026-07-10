import re
import json

with open('country-reports/Y16/ES_Y16.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Try to capture a broader context: Law Type, Number/Year, and optionally the date and title
# We look for the base pattern and grab up to 100 characters following it to capture the title,
# stopping at certain punctuation if it seems like the end of the citation.
pattern = re.compile(r'\b(Ley Orgánica|Ley|Real Decreto-ley|Real Decreto-Ley|Real Decreto Legislativo|Real Decreto|Decreto-ley|Decreto-Ley|Decreto Legislativo|Decreto)\s+(\d+/\d{4})(.*?)(?:[.;]|\n)', re.IGNORECASE)

matches = pattern.findall(text)

laws_dict = {}

for match in matches:
    law_type = match[0].strip().title()
    number_year = match[1].strip()
    rest = match[2].strip()
    
    # Normalize some titles
    law_type = law_type.replace('Decreto-Ley', 'Decreto-ley')
    
    key = f"{law_type} {number_year}".upper()
    
    # We want to keep the longest 'rest' string we find for a given key, 
    # as it's most likely to contain the full title.
    if key not in laws_dict or len(rest) > len(laws_dict[key].get('title', '')):
        laws_dict[key] = {
            'type': law_type,
            'number': number_year,
            'title': rest
        }

# Convert to list and sort
sorted_laws = sorted(laws_dict.values(), key=lambda x: x['number'].split('/')[1] + x['number'].split('/')[0]) # sort by year roughly

print(f"Found {len(sorted_laws)} unique laws.")

with open('es_laws_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_laws, f, indent=2, ensure_ascii=False)
