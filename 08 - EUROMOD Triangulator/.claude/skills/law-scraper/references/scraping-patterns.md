# Scraping Patterns for Law Sites

Python script templates and patterns. Use `uv` inline metadata.

## 1. The Script Template

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "curl_cffi",
#     "beautifulsoup4",
#     "PyMuPDF",
# ]
# ///
import json
import logging
import time
from pathlib import Path
import httpx

# Import curl_cffi for fallback
try:
    from curl_cffi import requests as cffi_requests
    HAS_CFFI = True
except ImportError:
    HAS_CFFI = False

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

def scrape():
    # Implementation goes here
    pass

if __name__ == "__main__":
    scrape()
```

## 2. HTTP Client Ladder

**Level 1: httpx** (Default)
Start with standard `httpx`. Ensure `verify=False` to handle broken government SSL certificates and `follow_redirects=True`.

**Level 2: curl_cffi** (Bypass TLS Fingerprinting/Cloudflare)
Use when `httpx` returns 403 Forbidden, 401 Unauthorized, or 503 Service Unavailable (often a Cloudflare interstitial). Also use when `httpx` throws `[SSL: CERTIFICATE_VERIFY_FAILED]` or Connection Reset errors.

```python
def fetch_url(client, url):
    """The HTTP Client Ladder: Tries httpx first, falls back to curl_cffi if blocked."""
    try:
        resp = client.get(url, follow_redirects=True, verify=False, timeout=60.0)
        resp.raise_for_status()
        return resp.content
    except httpx.HTTPStatusError as e:
        # 403 Forbidden, 401 Unauthorized, 503 Service Unavailable (often Cloudflare)
        if e.response.status_code in [403, 401, 503] and HAS_CFFI:
            log.warning(f"Got {e.response.status_code} for {url}. Falling back to curl_cffi impersonation...")
            fallback_resp = cffi_requests.get(url, impersonate="chrome120")
            if fallback_resp.status_code == 200:
                log.info(f"Fallback successful for {url}")
                return fallback_resp.content
        raise e
    except Exception as e:
        # For SSL errors or generic connection resets, try fallback too
        if HAS_CFFI and ("SSL" in str(e) or "Connect" in str(e)):
            log.warning(f"Got connection/SSL error for {url}. Falling back to curl_cffi...")
            try:
                fallback_resp = cffi_requests.get(url, impersonate="chrome120")
                if fallback_resp.status_code == 200:
                    log.info(f"Fallback successful for {url}")
                    return fallback_resp.content
            except Exception as fallback_e:
                raise e # raise original if fallback also fails
        raise e
```

## 3. Error Handling and Government Server Flakiness

Government servers often drop connections (e.g., Luxembourg's `WinError 10054`). 
- Always use exponential backoff.
- If it still fails, it must be logged to `PENDING.md`. Do not allow the script to crash completely if one URL in a batch fails.

```python
from time import sleep

MAX_RETRIES = 3
RETRY_BACKOFF = [2, 5, 15]

def fetch_with_retry(client, url):
    for attempt in range(MAX_RETRIES):
        try:
            resp = client.get(url)
            if resp.status_code == 429:
                sleep(RETRY_BACKOFF[attempt])
                continue
            resp.raise_for_status()
            return resp
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                sleep(RETRY_BACKOFF[attempt])
                continue
            raise
```

## 4. Document Processing
- **HTML Cleanup**: Use `BeautifulSoup` and `.decompose()` on `nav`, `footer`, `script`, `style`, `aside`, `form`, `meta`, and `link` tags before calling `.get_text(separator="\n\n", strip=True)`.
- **PDF Extraction**: Use `PyMuPDF` (`fitz` module). Avoid `pypandoc` for PDFs as it requires system-level installations that might not exist.
```python
import fitz # PyMuPDF
doc = fitz.open(raw_pdf_path)
text = "".join(page.get_text() + "\n\n" for page in doc)
```