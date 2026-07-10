import os
import json
import argparse
import httpx
import re

def load_env():
    """Load variables from .env manually to avoid python-dotenv dependency."""
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip()

def extract_headers(cr_path):
    """Extract headers from the Markdown Country Report."""
    headers = []
    try:
        with open(cr_path, 'r', encoding='utf-8') as f:
            for line in f:
                if re.match(r"^#{2,4}\s+", line):
                    # Clean up the header string
                    header_text = re.sub(r"^#+\s+", "", line).strip()
                    if header_text:
                        headers.append(header_text)
    except FileNotFoundError:
        print(f"Error: {cr_path} not found.")
    return headers

def extract_macro_policies(country_code, headers, year):
    """Use Gemini to identify top macro-policies and generate search queries."""
    headers_text = "\n".join(headers)
    prompt = (
        f"You are a legal researcher specializing in {country_code} tax and benefit systems for the year {year}.\n"
        f"Below is a list of headers extracted from a EUROMOD Country Report describing the system.\n"
        f"Identify the 5 to 8 most important 'Macro-Policy' categories (e.g., 'Personal Income Tax', "
        f"'Child Benefit', 'Contributory Unemployment Benefit', 'Social Security Contributions').\n"
        f"For each macro-policy, generate a native-language search query that would locate the fundamental, "
        f"consolidated legal text (law/act/decree) governing it in {year}.\n\n"
        f"CR Headers:\n{headers_text}\n\n"
        f"Output ONLY a valid JSON array of objects. Each object must have 'policy_name' (string) and 'query' (string).\n"
        f"Do NOT include markdown formatting or ```json tags. Just the raw JSON array."
    )
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("  [LLM Warning] GEMINI_API_KEY not found. Falling back to rule-based header extraction.")
        fallback_policies = []
        keywords = ["benefit", "tax", "pension", "contribution", "allowance", "income"]
        
        for h in headers:
            # Ignore top level
            if len(h) < 10:
                continue
            h_lower = h.lower()
            if any(kw in h_lower for kw in keywords) and "simulation" not in h_lower:
                fallback_policies.append({
                    "policy_name": h,
                    "query": f"ley {h} {country_code} {year} consolidado" if country_code == "ES" else f"{h} {country_code} legislation {year}"
                })
                if len(fallback_policies) >= 6:
                    break
                    
        return fallback_policies
        
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = httpx.post(url, json=payload, timeout=15.0)
        
        if response.status_code == 200:
            data = response.json()
            text_response = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            # Clean up potential markdown formatting
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            if text_response.startswith("```"):
                text_response = text_response[3:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
            
            return json.loads(text_response.strip())
        else:
            print(f"  [Gemini Error] {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  [LLM Extraction Error] {e}")
        
    print("  [LLM disabled or failed] Falling back to rule-based header extraction.")
    fallback_policies = []
    keywords = ["benefit", "tax", "pension", "contribution", "allowance", "income"]
    
    for h in headers:
        # Ignore top level
        if len(h) < 10:
            continue
        h_lower = h.lower()
        if any(kw in h_lower for kw in keywords) and "simulation" not in h_lower:
            fallback_policies.append({
                "policy_name": h,
                "query": f"ley {h} {country_code} {year} consolidado" if country_code == "ES" else f"{h} {country_code} legislation {year}"
            })
            if len(fallback_policies) >= 6:
                break
                
    return fallback_policies

def active_web_search(query, country_code):
    """Use Exa or Tavily REST API to search for official government sources."""
    exa_key = os.environ.get("EXA_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    domain_suffix = country_code.lower()
    if domain_suffix == "uk": domain_suffix = "co.uk"
    full_query = f"{query} site:*.{domain_suffix} OR site:*.gov OR site:*.eu"

    if exa_key:
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "x-api-key": exa_key
            }
            payload = {
                "query": full_query,
                "useAutoprompt": False,
                "numResults": 3,
            }
            res = httpx.post("https://api.exa.ai/search", json=payload, headers=headers, timeout=15.0)
            if res.status_code == 200:
                results = res.json().get("results", [])
                return [{"title": r.get("title"), "url": r.get("url")} for r in results]
        except Exception as e:
            print(f"  [Exa Search Error] {e}")

    if tavily_key:
        try:
            payload = {
                "api_key": tavily_key,
                "query": full_query,
                "search_depth": "basic",
                "max_results": 3
            }
            res = httpx.post("https://api.tavily.com/search", json=payload, timeout=15.0)
            if res.status_code == 200:
                results = res.json().get("results", [])
                return [{"title": r.get("title"), "url": r.get("url")} for r in results]
        except Exception as e:
            print(f"  [Tavily Search Error] {e}")

    return []

def main(country_code, year=2025):
    load_env()
    cr_path = rf'country-reports/Y16/{country_code}_Y16.md'
    
    print(f"--- Starting Ghost Law Discovery for {country_code} ({year}) ---")
    
    headers = extract_headers(cr_path)
    if not headers:
        print("No headers extracted. Cannot proceed.")
        return
        
    print(f"Extracted {len(headers)} headers from Country Report.")
    print("Asking LLM to identify Macro-Policies and generate queries...")
    
    policies = extract_macro_policies(country_code, headers, year)
    if not policies:
        print("No policies identified.")
        return
        
    print(f"Identified {len(policies)} Macro-Policies. Initiating searches...\n")
    
    discovered_laws = []
    
    for pol in policies:
        name = pol.get("policy_name")
        query = pol.get("query")
        
        print(f"Policy: {name}")
        print(f"Query:  {query}")
        
        results = active_web_search(query, country_code)
        
        if results:
            print(f"  Found {len(results)} potential legal texts:")
            for r in results:
                print(f"    - {r['title']}: {r['url']}")
        else:
            print("  No sources found.")
            
        discovered_laws.append({
            "policy_name": name,
            "query": query,
            "results": results
        })
        print()
        
    out_dir = f"legislation/{country_code}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/ghost_laws_{year}.json"
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(discovered_laws, f, indent=2, ensure_ascii=False)
        
    print(f"Saved {len(discovered_laws)} ghost law searches to {out_path}.")
    print("Please review and inject major missing laws into legislation-sources.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", required=True)
    parser.add_argument("--year", default=2025, type=int)
    args = parser.parse_args()
    main(args.country, args.year)