import re
import json
from pathlib import Path

text = Path('country-reports/Y16/SI_Y16.md').read_text(encoding='utf-8')

# Let's find exactly the names of the acts mentioned in English and Slovenian in SI report
# Look for "Zakon o [something]" 
slovenian_laws = re.findall(r'\b[Zz]akon o [a-zA-Z\s\-\u010D\u0161\u017E\u010C\u0160\u017D]+\b', text)
slovenian_laws = set(slovenian_laws)

# Often EUROMOD translates them to English in the report, like "Exercise of Rights to Public Funds Act"
# Let's catch all "Act" and "Law" strings
english_acts = re.findall(r'\b[A-Z][a-zA-Z\s\-]*\sAct\b', text)
english_laws = re.findall(r'\b[A-Z][a-zA-Z\s\-]*\sLaw\b', text)

all_implicit = slovenian_laws.union(english_acts).union(english_laws)

cleaned = set()
for law in all_implicit:
    law = re.sub(r'\s+', ' ', law).strip()
    if len(law) > 8 and "Abstract" not in law and "EUROMOD" not in law:
        # Strip some leading words if they are just generic
        if law.startswith('The '): law = law[4:]
        cleaned.add(law)
        
unique_si_laws = sorted(list(cleaned))
for m in unique_si_laws[:20]:
    print(m)

out_file = Path(".copilot/skills/law-scraper/utils/SI/SI_laws_extracted.json")
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(json.dumps(unique_si_laws, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Extracted {len(unique_si_laws)} laws.")
