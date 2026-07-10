import re
import json
from pathlib import Path

text = Path('country-reports/Y16/NL_Y16.md').read_text(encoding='utf-8')
text = re.sub(r'\n+', ' ', text)

# Often in EUROMOD reports, laws are in italics like *Wet op de zorgtoeslag* or explicitly named.
# Let's search for "Wet [A-Z][a-zA-Z\s]+" stopping at punctuation or too many lowercase words.
matches = re.findall(r'\b(?:Wet|Algemene [Ww]et|Besluit|Regeling)\s+(?:[a-zA-Z]+\s*){1,6}', text)

# Also single word laws
single_word = re.findall(r'\b[A-Z][a-z]+wet\b', text)

cleaned = set()
for m in matches + single_word:
    # Trim to end of last capitalized word or specific known words
    m = m.strip()
    words = m.split()
    valid_words = []
    for w in words:
        if w[0].isupper() or w.lower() in ['en', 'de', 'het', 'van', 'naar', 'op', 'tot', 'voor', 'der', 'inzake', 'bij']:
            valid_words.append(w)
        else:
            break
            
    # Clean trailing lowercase connective words
    while valid_words and valid_words[-1].lower() in ['en', 'de', 'het', 'van', 'naar', 'op', 'tot', 'voor', 'der', 'inzake', 'bij']:
        valid_words.pop()
        
    law_name = " ".join(valid_words).replace('*', '')
    if len(law_name) > 6 and 'The ' not in law_name:
        cleaned.add(law_name)

unique_nl_laws = sorted(list(cleaned))

for m in unique_nl_laws:
    print(m)

out_file = Path(".copilot/skills/law-scraper/utils/NL/NL_laws_extracted.json")
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(json.dumps(unique_nl_laws, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Extracted {len(unique_nl_laws)} Dutch laws.")
