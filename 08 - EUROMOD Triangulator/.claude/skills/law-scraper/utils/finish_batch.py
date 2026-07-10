import re
import sys
from pathlib import Path

batch = sys.argv[1:] if len(sys.argv) > 1 else ["BG", "CY", "CZ", "DE", "DK"]

for cc in batch:
    pending_file = Path(f'legislation/{cc}/PENDING.md')
    md_file = Path(f'legislation-sources/{cc}.md')
    
    failed_urls = []
    if pending_file.exists():
        text = pending_file.read_text(encoding='utf-8')
        failed_urls = re.findall(r'- \*\*URL\*\*: (.*?)\n', text)
    
    if not md_file.exists(): continue
    
    md_text = md_file.read_text(encoding='utf-8')
    new_lines = []
    for line in md_text.split('\n'):
        if line.startswith('- [http'):
            url_match = re.search(r'\[(.*?)\]', line)
            if url_match:
                url = url_match.group(1)
                # Ensure no old tags
                line = line.replace(' `[FAILED/PENDING]`', '').replace(' `[✅ DOWNLOADED]`', '')
                if url in failed_urls:
                    line += ' `[FAILED/PENDING]`'
                else:
                    line += ' `[✅ DOWNLOADED]`'
        new_lines.append(line)
        
    md_file.write_text('\n'.join(new_lines), encoding='utf-8')
    print(f"Updated {cc}.md explicit URLs statuses.")
