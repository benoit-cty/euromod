# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "playwright",
#     "beautifulsoup4",
# ]
# ///
import asyncio
import re
import time
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["nav", "footer", "script", "style", "aside", "form", "meta", "link", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n\n", strip=True)

async def fetch_urls():
    base_dir = Path("legislation")
    pending_files = list(base_dir.glob("*/PENDING.md"))
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        for p_file in pending_files:
            country = p_file.parent.name
            print(f"\n--- Processing {country} ---")
            lines = p_file.read_text(encoding="utf-8").splitlines()
            
            raw_dir = p_file.parent / "raw"
            raw_dir.mkdir(exist_ok=True)
            
            new_lines = []
            resolved_count = 0
            
            page = await context.new_page()
            
            for line in lines:
                match = re.search(r'(https?://[^\s\)]+)', line)
                if match:
                    url = match.group(1).strip("'\"")
                    print(f"Attempting: {url}")
                    try:
                        resp = await page.goto(url, timeout=15000, wait_until="domcontentloaded")
                        if resp and resp.status < 400:
                            content = await page.content()
                            text = clean_html(content)
                            if len(text.strip()) > 100:
                                out_file = p_file.parent / f"resolved_{int(time.time())}.md"
                                out_file.write_text(f"Source: {url}\n\n{text}", encoding="utf-8")
                                print(f"Saved: {out_file.name}")
                                resolved_count += 1
                                continue
                            else:
                                print("Content too short.")
                        else:
                            print(f"Failed with status: {resp.status if resp else 'No response'}")
                    except Exception as e:
                        print(f"Playwright failed: {str(e)[:100]}")
                new_lines.append(line)
            
            await page.close()
            
            if resolved_count > 0:
                if len(new_lines) < 5 or not any(re.search(r'(https?://[^\s\)]+)', l) for l in new_lines):
                    print(f"All URLs resolved for {country}. Deleting PENDING.md")
                    p_file.unlink()
                else:
                    p_file.write_text("\n".join(new_lines), encoding="utf-8")
                    print(f"Updated PENDING.md for {country}")
            else:
                print(f"No URLs resolved for {country}")
                
        await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_urls())