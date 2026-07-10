import re
import json
from pathlib import Path

text = Path('country-reports/Y16/BG_Y16.md').read_text(encoding='utf-8')
matches = re.findall(r'\*?([Зз]акон.*?[а-яА-Я\s]+|[Кк]одекс.*?[а-яА-Я\s]+)\*?', text)

unique_bg_laws = sorted(list(set([m.replace('*', '').strip() for m in matches if len(m) > 10])))
Path('bg_laws_temp.json').write_text(json.dumps(unique_bg_laws, ensure_ascii=False, indent=2), encoding='utf-8')
