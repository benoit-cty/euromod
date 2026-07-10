# The Wayback Machine Fallback

Because we are triangulating historical policies (e.g., 2022-2023), many government URLs found in the Country Reports will be dead (404).

## The Strategy

If an initial request returns `404 Not Found`, the scraper should automatically query the Internet Archive's Wayback Machine API.

## API Endpoint

The CDX (Capture Index) API allows you to find snapshots of a URL.

```
http://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=5
```

If you need a snapshot closest to a specific year (e.g., to match the EUROMOD policy year exactly), use the `from` and `to` parameters (YYYYMMDD format):

```
http://web.archive.org/cdx/search/cdx?url={URL}&from=20230101&to=20231231&output=json&limit=1
```

## Python Implementation

```python
import httpx

def get_archived_url(target_url, target_year):
    """Queries the Wayback Machine for a snapshot from the target year."""
    api_url = "http://web.archive.org/cdx/search/cdx"
    params = {
        "url": target_url,
        "from": f"{target_year}0101",
        "to": f"{target_year}1231",
        "output": "json",
        "limit": 1
    }
    
    resp = httpx.get(api_url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if len(data) > 1: # Index 0 is headers, Index 1 is the first result
            timestamp = data[1][1]
            original = data[1][2]
            return f"https://web.archive.org/web/{timestamp}/{original}"
    return None
```