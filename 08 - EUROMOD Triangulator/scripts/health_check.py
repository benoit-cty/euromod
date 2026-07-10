import os
import random
from pathlib import Path

def run_health_checks():
    output_dir = Path("./country-reports/Y16")
    md_files = list(output_dir.glob("*.md"))
    
    print(f"Total MD files found: {len(md_files)}\n")
    
    # Check 1: File sizes (Ensure no file is suspiciously small)
    print("--- Check 1: File Size Anomalies ---")
    small_files = []
    for f in md_files:
        size_kb = f.stat().st_size / 1024
        if size_kb < 50:  # Suspiciously small for a country report
            small_files.append((f.name, size_kb))
    
    if small_files:
        print(f"WARNING: Found {len(small_files)} suspiciously small files (< 50KB):")
        for name, size in small_files:
            print(f"  - {name}: {size:.2f} KB")
    else:
        print("All files are > 50KB. No suspiciously small files found.\n")
        
    # Check 2: Random Content Inspection
    print("--- Check 2: Structural Integrity of 3 Random Files ---")
    sample_files = random.sample(md_files, 3)
    
    required_keywords = ["Introduction", "Simulation", "Data"]
    
    for f in sample_files:
        print(f"\nInspecting: {f.name} ({f.stat().st_size / 1024:.2f} KB)")
        try:
            with open(f, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            # Check length
            print(f"  - Total lines: {len(lines)}")
            
            # Check top 10 non-empty lines for Title/Contents
            top_lines = [line.strip() for line in lines[:50] if line.strip()]
            print(f"  - Start snippet: {top_lines[:2]}")
            
            # Check bottom 10 non-empty lines (looking for References/Appendices)
            bottom_lines = [line.strip() for line in lines[-50:] if line.strip()]
            print(f"  - End snippet: {bottom_lines[-2:]}")
            
            # Check for key sections
            content = "".join(lines)
            found_keywords = [kw for kw in required_keywords if kw.lower() in content.lower()]
            print(f"  - Found key sections: {found_keywords}")
            
        except Exception as e:
            print(f"  - Error reading file: {e}")

if __name__ == "__main__":
    run_health_checks()
