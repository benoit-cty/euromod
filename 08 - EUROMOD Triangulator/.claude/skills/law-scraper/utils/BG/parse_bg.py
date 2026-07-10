import re
import json
from pathlib import Path

text = Path('country-reports/Y16/BG_Y16.md').read_text(encoding='utf-8')
# Find Bulgarian names anywhere
matches = re.findall(r'\b([Зз]акон[а-яА-Я\s\-]+|[Кк]одекс[а-яА-Я\s\-]+)\b', text)
unique_bg_laws = sorted(list(set([re.sub(r'\s+', ' ', m).strip() for m in matches if len(m) > 10])))

# Remove trailing " на " or " за " if cut off
cleaned_laws = set()
for law in unique_bg_laws:
    if law.endswith(' на') or law.endswith(' за'):
        law = law.rsplit(' ', 1)[0]
    cleaned_laws.add(law)

unique_bg_laws = sorted(list(cleaned_laws))

out_file = Path(".copilot/skills/law-scraper/utils/BG/BG_laws_extracted.json")
out_file.parent.mkdir(parents=True, exist_ok=True)
out_file.write_text(json.dumps(unique_bg_laws, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Extracted {len(unique_bg_laws)} Bulgarian laws.")
