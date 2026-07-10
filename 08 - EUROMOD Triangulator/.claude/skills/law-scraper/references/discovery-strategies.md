# Advanced Discovery Strategies for Government Portals

Government portals are rarely built with scraping in mind. They often rely on heavy legacy enterprise frameworks (JavaServer Faces, old ASP.NET) or modern Single Page Applications (Angular/React) behind intense Web Application Firewalls (Cloudflare, Imperva).

This guide outlines strategies to bypass these issues.

## 1. The "Search Engine Oracle" Strategy (Yahoo + curl_cffi)

When a national gazette (like `lex.bg`) has an internal search engine that is heavily obfuscated (e.g., requires complex JSF ViewStates) or blocks automated traffic, you can bypass the site entirely by querying a global search engine.

**Crucial Finding**: Google and DuckDuckGo aggressively block programmatic queries (HTTP 403 or 202 Accepted with CAPTCHA challenges). **Yahoo Search**, however, allows queries when accessed via `curl_cffi` impersonating Chrome.

### Implementation Pattern

```python
from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

def yahoo_resolve_law(query, domain="lex.bg/laws/ldoc"):
    """Uses Yahoo search to resolve an implicit law title to an official URL."""
    url = "https://search.yahoo.com/search"
    # Use exact match quotes for better accuracy
    params = {"p": f"site:{domain} \"{query}\""}
    
    r = requests.get(url, params=params, impersonate="chrome120", timeout=15.0)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    for div in soup.find_all('div', class_='compTitle'):
        a = div.find('a')
        if a:
            href = a.get('href', '')
            # Yahoo wraps the real URL in a redirect link (RU=...)
            if 'RU=' in href:
                ru = href.split('RU=')[1].split('/RK=')[0]
                real_url = urllib.parse.unquote(ru)
                if domain in real_url:
                    return real_url
    return None
```

## 2. Dealing with Institutional Firewalls & WinError 10054

Certain countries (e.g., Luxembourg's `*.public.lu`, Romania's `statistici.insse.ro`, Slovenia's `stat.si`) implement highly aggressive firewall rules that forcefully sever connections (`[WinError 10054]`) before an HTTP response is even generated.

**Symptoms**:
- `Server disconnected without sending a response`
- `[WinError 10054] An existing connection was forcibly closed by the remote host`
- `multiple Transfer-Encoding headers` (Often a sign of a misconfigured WAF).

**Resolution**:
1. **Network Change**: The target server is likely blocking datacenter IPs or specific user-agents entirely. You must switch to a residential proxy network.
2. **Manual Fallback**: Log these explicitly in `PENDING.md`. The most efficient path forward for a small number of laws is for a human to download them via a standard browser on a residential ISP.

## 3. Detecting SPA "Empty Shells"

Modern tax portals (e.g., Belgium's `minfin.fgov.be` MyMinfin portal) use Single Page Applications protected by SSO. 
If you scrape them using `httpx`, you will get an HTTP 200 OK, but the resulting HTML will be an empty shell (often `< 10KB`) containing just `<app-root></app-root>` or `<div id="root"></div>`.

**Resolution**:
Always implement a size heuristic in your scraper:
```python
if len(resp.text) < 15000 and ("Angular" in resp.text or "app-root" in resp.text):
    log.warning("SPA Empty Shell detected. Requires manual fetch or Playwright.")
```
If Playwright is blocked (as it often is on these sites via `ERR_INVALID_AUTH_CREDENTIALS`), route it to `PENDING.md`.
