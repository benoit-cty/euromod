from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://pisrs.si/predpis/ZAKO213")
    time.sleep(5)
    print(f"Title: {page.title()}")
    
    # Wait for the specific content element
    try:
        page.wait_for_selector(".besedilo-predpisa", timeout=10000)
        content = page.query_selector(".besedilo-predpisa").inner_text()
        print(f"Length of text: {len(content)}")
        print(content[:500])
    except Exception as e:
        print(f"Error: {e}")
        
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
