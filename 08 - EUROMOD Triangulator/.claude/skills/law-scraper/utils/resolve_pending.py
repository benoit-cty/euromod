# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "curl_cffi",
#     "beautifulsoup4",
#     "PyMuPDF",
# ]
# ///
import os
import re
import time
import json
from pathlib import Path
import httpx
from curl_cffi import requests as cffi_requests
from bs4 import BeautifulSoup
import fitz

import urllib3
urllib3.disable_warnings()

HAS_CFFI = True

def get_archived_url(target_url):
    print(f"Trying Wayback Machine for: {target_url}")
    api_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": target_url,
        "output": "json",
        "limit": 1
    }
    try:
        resp = httpx.get(api_url, params=params, timeout=15.0)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 1:
                timestamp = data[1][1]
                original = data[1][2]
                return f"https://web.archive.org/web/{timestamp}/{original}"
    except Exception as e:
        print(f"Wayback Machine failed: {e}")
    return None

def fetch_url(url):
    client = httpx.Client(verify=False, timeout=30.0)
    # httpx
    try:
        resp = client.get(url, follow_redirects=True)
        resp.raise_for_status()
        return resp.content, resp.headers.get("Content-Type", "")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            archived = get_archived_url(url)
            if archived:
                print(f"Found archived: {archived}")
                return fetch_url(archived)
        if e.response.status_code in [403, 401, 503, 502, 500]:
            print(f"Got {e.response.status_code}, falling back to curl_cffi")
            try:
                fallback = cffi_requests.get(url, impersonate="chrome120", timeout=30.0, verify=False)
                if fallback.status_code == 200:
                    return fallback.content, fallback.headers.get("Content-Type", "")
            except Exception as fe:
                print(f"curl_cffi failed: {fe}")
        raise e
    except Exception as e:
        print(f"Got connection/SSL error: {e}, falling back to curl_cffi")
        try:
            fallback = cffi_requests.get(url, impersonate="chrome120", timeout=30.0, verify=False)
            if fallback.status_code == 200:
                return fallback.content, fallback.headers.get("Content-Type", "")
        except Exception as fe:
            print(f"curl_cffi failed: {fe}")
        raise e

def clean_html(html_bytes):
    soup = BeautifulSoup(html_bytes, "html.parser")
    for tag in soup(["nav", "footer", "script", "style", "aside", "form", "meta", "link", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n\n", strip=True)

def extract_pdf(pdf_bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        print(f"PDF extraction failed: {e}")
        return ""

def process_pending():
    base_dir = Path("legislation")
    pending_files = list(base_dir.glob("*/PENDING.md"))
    
    for p_file in pending_files:
        country = p_file.parent.name
        print(f"\n--- Processing {country} ---")
        lines = p_file.read_text(encoding="utf-8").splitlines()
        
        new_lines = []
        raw_dir = p_file.parent / "raw"
        raw_dir.mkdir(exist_ok=True)
        
        resolved_count = 0
        
        for line in lines:
            match = re.search(r'(https?://[^\s\)]+)', line)
            if match:
                url = match.group(1).strip("'\"")
                print(f"Attempting: {url}")
                try:
                    content, ctype = fetch_url(url)
                    text = ""
                    ext = "md"
                    
                    if b"%PDF-" in content[:1024]:
                        print("Detected PDF")
                        text = extract_pdf(content)
                        raw_pdf_path = raw_dir / f"{country}_{int(time.time())}.pdf"
                        raw_pdf_path.write_bytes(content)
                    else:
                        text = clean_html(content)
                        
                    if text.strip():
                        # Save to markdown
                        out_file = p_file.parent / f"resolved_{int(time.time())}.md"
                        out_file.write_text(f"Source: {url}\n\n{text}", encoding="utf-8")
                        print(f"Saved: {out_file.name}")
                        resolved_count += 1
                        continue # Skip appending this line to new PENDING.md
                except Exception as e:
                    print(f"Failed to fetch {url}: {e}")
            new_lines.append(line)
            
        if resolved_count > 0:
            if len(new_lines) < 5 or not any(re.search(r'(https?://[^\s\)]+)', l) for l in new_lines):
                # Probably empty or only headers left
                print(f"All URLs resolved for {country}. Deleting PENDING.md")
                p_file.unlink()
            else:
                p_file.write_text("\n".join(new_lines), encoding="utf-8")
                print(f"Updated PENDING.md for {country}")
        else:
            print(f"No URLs resolved for {country}")

if __name__ == "__main__":
    process_pending()