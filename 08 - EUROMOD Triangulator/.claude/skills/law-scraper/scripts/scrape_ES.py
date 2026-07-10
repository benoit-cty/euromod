import httpx
import logging
import time
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
HEADERS = {"User-Agent": USER_AGENT}
BASE_DIR = Path("legislation/ES")
RAW_DIR = BASE_DIR / "raw"
PENDING_FILE = BASE_DIR / "PENDING.md"
JSON_FILE = Path(".copilot/skills/law-scraper/utils/ES/es_laws_extracted.json")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

def get_boe_id(client, law_type, number):
    url = "https://www.boe.es/buscar/legislacion.php"
    query = f"{law_type} {number}"
    params = {
        "accion": "Buscar",
        "campo[2]": "DOC",
        "dato[2]": query,
        "checkbox_solo_tit": "S",
        "operador[2]": "and",
        "sort_field[0]": "PESO",
        "sort_order[0]": "desc"
    }
    
    try:
        r = client.get(url, params=params, follow_redirects=True, timeout=30.0)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        results = soup.find_all("li", class_="resultado-busqueda")
        
        for res in results:
            link = res.find("a")
            if link:
                title = link.text.strip()
                # Instead of a strict regex which failed, let's just do a substring search on the URL
                # Actually, the result title inside the <p> might be better
                ps = res.find_all("p")
                if len(ps) >= 2:
                    doc_title = ps[1].text.strip()
                    # Check if doc_title starts with or contains our law type and number
                    # e.g., "Ley 31/2022" or "Ley Orgánica 1/2004"
                    if re.search(rf"^{law_type}\s+{number}\b", doc_title, re.IGNORECASE):
                        boe_id = link['href'].split('id=')[-1]
                        # Check if consolidated is available
                        conso_link = res.find("li", class_="puntoConso")
                        has_conso = conso_link is not None
                        return boe_id, has_conso
        return None, False
    except Exception as e:
        log.error(f"Search failed for {query}: {e}")
        return None, False

def clean_boe_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    content = soup.find("div", id="textoxslt")
    if not content:
        content = soup.find("div", id="documento")
        
    if not content:
        return "" # Failed to parse
        
    # Remove index drop-downs
    for m in content.find_all("div", class_="marcadores"):
        m.decompose()
        
    # Remove navigation, styles, scripts
    for tag in content(["nav", "script", "style", "aside", "svg", "form", "meta", "link"]):
        tag.decompose()
        
    text = content.get_text(separator="\n\n", strip=True)
    # Remove repeated empty lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text

def scrape():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    pending = []
    
    if not JSON_FILE.exists():
        log.error(f"{JSON_FILE} not found. Run the extraction script first.")
        return
        
    laws = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    
    with httpx.Client(headers=HEADERS, follow_redirects=True, verify=False, timeout=60.0) as client:
        for law in laws:
            l_type = law['type']
            l_number = law['number']
            
            # Clean up number slashes for filename
            safe_name = f"{l_type}_{l_number}".replace("/", "_").replace(" ", "_")
            md_file = BASE_DIR / f"{safe_name}.md"
            raw_file = RAW_DIR / f"{safe_name}.html"
            
            if md_file.exists():
                log.info(f"Skipping {safe_name}, already exists.")
                continue
                
            log.info(f"Processing {l_type} {l_number}...")
            boe_id, has_conso = get_boe_id(client, l_type, l_number)
            
            if not boe_id:
                log.warning(f"Could not find BOE ID for {l_type} {l_number}")
                pending.append({"name": f"{l_type} {l_number}", "url": "BOE Search", "error": "Not found in BOE Search"})
                time.sleep(1)
                continue
                
            log.info(f"Found BOE ID: {boe_id} (Consolidated: {has_conso})")
            
            if has_conso:
                doc_url = f"https://www.boe.es/buscar/act.php?id={boe_id}"
            else:
                doc_url = f"https://www.boe.es/buscar/doc.php?id={boe_id}"
                
            if not raw_file.exists():
                try:
                    resp = client.get(doc_url)
                    resp.raise_for_status()
                    raw_file.write_text(resp.text, encoding="utf-8", errors="ignore")
                    log.info(f"Saved raw HTML for {safe_name}")
                except Exception as e:
                    log.error(f"Failed to download {doc_url}: {e}")
                    pending.append({"name": f"{l_type} {l_number}", "url": doc_url, "error": str(e)})
                    time.sleep(2)
                    continue
                    
            if raw_file.exists():
                try:
                    html_content = raw_file.read_text(encoding="utf-8", errors="ignore")
                    text = clean_boe_html(html_content)
                    if text:
                        md_file.write_text(text, encoding="utf-8")
                        log.info(f"Converted {safe_name} to Markdown")
                    else:
                        log.error(f"Empty text extraction for {safe_name}")
                        pending.append({"name": f"{l_type} {l_number}", "url": doc_url, "error": "Empty extraction"})
                except Exception as e:
                    log.error(f"MD Conversion failed for {safe_name}: {e}")
                    pending.append({"name": f"{l_type} {l_number}", "url": doc_url, "error": str(e)})
                    
            time.sleep(2) # Politeness
            
    if pending:
        # Append to PENDING.md
        mode = "a" if PENDING_FILE.exists() else "w"
        with open(PENDING_FILE, mode, encoding="utf-8") as f:
            if mode == "w": f.write("# Pending\n\n")
            for p in pending:
                f.write(f"- {p['name']}: {p['url']} ({p['error']})\n")

if __name__ == "__main__":
    scrape()
