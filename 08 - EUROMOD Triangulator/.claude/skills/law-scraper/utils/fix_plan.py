import re
with open('PLAN.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Using regex to find the block ignoring exactly what is inside those lines
old_block = re.search(r'## .*?Where to Resume \(Immediate Next Steps\).*?PENDING\.md`\.', text, re.DOTALL)
if old_block:
    new_block = """## ⏳ Where to Resume (Immediate Next Steps)
We have proven the implicit text citation strategy with Spain. The generic extractor has been run across all remaining 26 countries, populating `legislation-sources/[CC].md` with pending citations.

**Current Task: Execute Alphabetically**
We are now building out the national scrapers and fetching the implicit laws country by country, alphabetically starting from **AT (Austria)** to **SK (Slovakia)**.

**For the current country (e.g., AT), the workflow is:**
1. **Review Database**: Check `legislation-sources/[CC].md` for pending citations.
2. **Build/Update Scraper**: Update `.copilot/skills/law-scraper/scripts/scrape_[CC].py` to programmatically search the national gazette/repository (e.g., RIS for Austria) for these specific law IDs.
3. **Scrape & Clean**: Download the text (preferably consolidated versions), clean the HTML, and save to `legislation/[CC]/[LawName].md`.
4. **Log Failures**: Ensure anything not found is documented in `legislation/[CC]/PENDING.md`.
5. **Update Status**: Update `legislation-sources/[CC].md` replacing `[PENDING GAZETTE FETCH]` with `[✅ DOWNLOADED]` or `[FAILED/PENDING]`."""
    text = text.replace(old_block.group(0), new_block)
    with open('PLAN.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Plan updated successfully.")
else:
    print("Could not find block in PLAN.md")
