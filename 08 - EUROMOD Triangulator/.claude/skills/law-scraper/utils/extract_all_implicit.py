import re
import sys
from pathlib import Path

def extract_laws_to_md(country_code):
    report_path = Path(f"country-reports/Y16/{country_code}_Y16.md")
    source_md_path = Path(f"legislation-sources/{country_code}.md")
    
    if not report_path.exists():
        print(f"Error: {report_path} not found.")
        return
        
    text = report_path.read_text(encoding='utf-8')
    
    # Generic regex trying to capture capitalized words ending in Law, Act, Code, Decree, Gesetz, Закон, etc.
    # or starting with Loi, Ley, Decreto, Wet, Закон
    patterns = [
        r'(?i)\b([A-Z][\w\-]+\s+(?:Act|Law|Code|Decree|Gesetz|Zákon|Кодекс))\b',
        r'(?i)\b(?:Loi|Wet|Arrêté royal|Decreto|Ley|Lei|Закон)\s+(?:du\s+|de\s+|of\s+|on\s+|за\s+|)[0-9A-Z][^\.,\n]{5,50}'
    ]
    
    citations = set()
    for p in patterns:
        for match in re.finditer(p, text):
            # Capture the match and a bit of context if needed, but match.group(0) is usually enough
            val = match.group(0).strip()
            # Clean up trailing spaces or parentheses
            val = re.sub(r'[\(\)]', '', val)
            if len(val) > 8 and val.count(' ') < 10:
                citations.add(val)
                
    if not citations:
        print(f"No implicit citations found for {country_code}")
        return
        
    sorted_citations = sorted(list(citations))
    
    # Append to MD
    if source_md_path.exists():
        md_text = source_md_path.read_text(encoding='utf-8')
        if "## Extracted Law Citations (Text-based)" in md_text:
            print(f"{country_code} already has extracted citations block.")
            return
            
        append_text = "\n\n## Extracted Law Citations (Text-based)\n"
        append_text += "The following laws were cited by name in the text but lacked direct URLs. They need to be retrieved via national gazettes.\n\n"
        
        for cit in sorted_citations:
            append_text += f"- **{cit}**: `[PENDING GAZETTE FETCH]`\n"
            
        source_md_path.write_text(md_text + append_text, encoding='utf-8')
        print(f"Updated {source_md_path} with {len(sorted_citations)} citations.")
    else:
        print(f"Warning: {source_md_path} does not exist.")

if __name__ == "__main__":
    for cc in ["AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT", "NL", "PL", "PT", "RO", "SE", "SI", "SK"]:
        extract_laws_to_md(cc)
