# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
from pathlib import Path

def verify_legislation():
    bad_files = []
    base_dir = Path("legislation")
    
    # We check all downloaded markdown files
    for cc_dir in base_dir.iterdir():
        if not cc_dir.is_dir():
            continue
        
        md_files = list(cc_dir.glob("*.md"))
        for md_file in md_files:
            if md_file.name == "PENDING.md":
                continue
                
            try:
                content = md_file.read_text(encoding="utf-8")
            except Exception as e:
                bad_files.append((md_file, "Encoding error"))
                continue
            
            # Check 1: Size
            if len(content) < 1500:  # Less than 1.5KB is suspicious for a consolidated law
                bad_files.append((md_file, "Too short (<1500 bytes)"))
                continue
                
            # Check 2: Error messages
            lower_content = content.lower()
            if "404 not found" in lower_content or "403 forbidden" in lower_content or "access denied" in lower_content:
                bad_files.append((md_file, "Contains HTTP error text"))
                continue
                
            # Check 3: Is it just a table of contents or summary?
            # E.g. in ES: "rentas minimas"
            if "table of contents" in lower_content[:2000] and len(content) < 5000:
                bad_files.append((md_file, "Likely just a Table of Contents"))
                continue
                
            if "javascript is required" in lower_content:
                bad_files.append((md_file, "JS Required warning"))
                continue

    with open("task2_report.txt", "w", encoding="utf-8") as f:
        for md, reason in bad_files:
            f.write(f"{md}: {reason}\n")
    print(f"Task 2 complete. Found {len(bad_files)} suspicious files.")

if __name__ == "__main__":
    verify_legislation()