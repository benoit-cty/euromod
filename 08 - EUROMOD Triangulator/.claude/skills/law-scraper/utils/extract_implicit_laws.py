import re
import json
import sys
from pathlib import Path

def extract_laws(country_code):
    report_path = Path(f"country-reports/Y16/{country_code}_Y16.md")
    if not report_path.exists():
        print(f"Error: {report_path} not found.")
        sys.exit(1)
        
    text = report_path.read_text(encoding='utf-8')
    
    # Dictionary of regex patterns per country/language
    # These are heuristic and meant to capture the law type and the number/year
    PATTERNS = {
        'AT': r'(?i)\b(?:Bundesgesetz|Gesetz|BGBl\.|EStG|ASVG|AlVG|FLAG)\b.*?(?:\d+/\d{4}|\d{4})',
        'BE': r'(?i)\b(?:Loi|Wet|Arrêté royal|Koninklijk besluit|Decreet|Décret)\b\s+.*?de\s+\d{1,2}\s+[a-zA-Z]+\s+\d{4}',
        'BG': r'(?i)\b(?:Закон|Кодекс|Zakon|Kodeks|SG|State Gazette)\b.*?\d+',
        'CY': r'(?i)\b(?:Law|Νόμος)\b.*?\d+/\d{4}',
        'CZ': r'(?i)\b(?:Zákon|Zák\.|Vyhláška)\b.*?\d+/\d{4}',
        'DE': r'(?i)\b(?:Gesetz|SGB|EStG|BGB|BVerfG)\b.*?(?:\d+)',
        'FR': r'(?i)\b(?:Loi|Décret|Ordonnance|Code)\b.*?(?:n°\s*\d+-\d+|\b\d{4}\b)',
        'IT': r'(?i)\b(?:Legge|Decreto Legislativo|D\.Lgs\.|Decreto Legge|D\.L\.|DPR|D\.P\.R\.)\b.*?\d+/\d{4}',
        'PT': r'(?i)\b(?:Lei|Decreto-Lei|Decreto Regulamentar|Portaria)\b.*?\d+/\d{4}'
    }
    
    pattern_str = PATTERNS.get(country_code)
    
    if not pattern_str:
        print(f"Warning: No specific regex defined for {country_code}. Using fallback.")
        pattern_str = r'(?i)\b(?:Law|Act|Decree|Code|Gesetz|Loi|Ley|Legge|Zákon|Lei)\b.*?\d+/\d{4}'
        
    pattern = re.compile(pattern_str)
    matches = pattern.findall(text)
    
    unique_laws = set()
    for match in matches:
        clean_match = re.sub(r'\s+', ' ', match).strip()
        if len(clean_match) > 5:
            unique_laws.add(clean_match)
            
    sorted_laws = sorted(list(unique_laws))
    
    print(f"Found {len(sorted_laws)} potential citations for {country_code}.")
    for l in sorted_laws[:10]:
        print(f" - {l}")
        
    out_dir = Path(f".copilot/skills/law-scraper/utils/{country_code}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{country_code}_laws_extracted.json"
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(sorted_laws, f, indent=2, ensure_ascii=False)
        
    print(f"Saved to {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_implicit_laws.py [CC]")
    else:
        extract_laws(sys.argv[1].upper())
