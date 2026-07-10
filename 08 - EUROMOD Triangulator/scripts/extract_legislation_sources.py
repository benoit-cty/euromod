import os
import re
from pathlib import Path
from urllib.parse import urlparse
from collections import defaultdict

def clean_url(url):
    # Remove trailing punctuation often captured by regex
    return re.sub(r'[\.,;:)\'"]+$', '', url)

def classify_url(domain, url):
    domain = domain.lower()
    url = url.lower()
    
    # Legal and core government
    if any(kw in domain for kw in ['lex', 'ris.bka', 'law', 'legis', 'parliament', 'senat', 'assemblee', 'bundestag']):
        return "Legal Repositories & Parliaments"
        
    # Ministries and official Gov portals
    if any(kw in domain for kw in ['gov.', 'gv.', 'fgov', 'government', 'minfin', 'finance', 'revenue', 'social', 'emploi', 'travail']):
        return "Ministries & Government Portals"
        
    # Statistics
    if any(kw in domain for kw in ['stat', 'nsi', 'cso', 'ine']):
        return "Statistical Offices"
        
    # EU / OECD
    if 'europa.eu' in domain or 'oecd' in domain:
        return "European & International Organisations"
        
    return "Other Relevant Sources"

def run_extraction():
    input_dir = Path("country-reports/Y16")
    output_dir = Path("legislation-sources")
    
    md_files = list(input_dir.glob("*.md"))
    print(f"Processing {len(md_files)} files...")
    
    for md_path in md_files:
        country_code = md_path.stem.split('_')[0]
        
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {md_path}: {e}")
            continue
            
        urls_by_category = defaultdict(dict) # category -> {url: context}
        
        for line in lines:
            line_text = line.strip()
            # Regex to find URLs
            found_urls = re.findall(r'http[s]?://[^\s<>)"\]]+', line_text)
            
            for url in found_urls:
                url = clean_url(url)
                
                try:
                    domain = urlparse(url).netloc
                    if not domain:
                        continue
                except:
                    continue
                
                # Skip localhost or clearly invalid
                if domain == 'localhost' or '.' not in domain:
                    continue
                    
                category = classify_url(domain, url)
                
                # Store URL and its context line (truncate context if too long)
                context = line_text if len(line_text) < 150 else line_text[:147] + "..."
                
                # If we already have this URL, maybe append context if it mentions a year and previous didn't
                if url in urls_by_category[category]:
                    if re.search(r'20\d{2}', context) and not re.search(r'20\d{2}', urls_by_category[category][url]):
                        urls_by_category[category][url] = context
                else:
                    urls_by_category[category][url] = context
                    
        # Write output file
        out_file = output_dir / f"{country_code}.md"
        with open(out_file, 'w', encoding='utf-8') as out:
            out.write(f"# Legislation & Policy Sources: {country_code}\n\n")
            out.write("## Overview\n")
            out.write(f"This document tracks the sources used to define tax-benefit rules for {country_code}. ")
            out.write("Sources were initially extracted from the Y16 EUROMOD Country Report.\n\n")
            
            out.write("## Time Coverage & Obsolescence Notes\n")
            out.write("- **Current Basis**: Y16 Report (covers policies predominantly from 2022-2025).\n")
            out.write("- **URL Stability**: Check URLs carefully for hardcoded years (e.g., `.../2023/...`). ")
            out.write("Legal frameworks update frequently; if a URL is dead, look for the base domain's search function or an archived version.\n")
            out.write("- **Version Control**: When checking against models, ensure the legal text corresponds to the exact year of the EUROMOD policy being triangulated.\n\n")
            
            out.write("## Extracted URLs\n")
            
            if not urls_by_category:
                out.write("*No URLs found in the country report.*\n")
            else:
                # Print categories in a logical order
                cat_order = ["Legal Repositories & Parliaments", "Ministries & Government Portals", "Statistical Offices", "European & International Organisations", "Other Relevant Sources"]
                
                for cat in cat_order:
                    if cat in urls_by_category and urls_by_category[cat]:
                        out.write(f"### {cat}\n")
                        # Sort URLs alphabetically
                        for url in sorted(urls_by_category[cat].keys()):
                            context = urls_by_category[cat][url]
                            # Clean up markdown link syntax from context if it's overwhelming
                            context_clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', context)
                            out.write(f"- [{url}]({url})\n")
                            out.write(f"  - *Context:* `{context_clean}`\n")
                        out.write("\n")
                        
    print("Done generating legislation source files.")

if __name__ == "__main__":
    run_extraction()
