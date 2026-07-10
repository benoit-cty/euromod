import os
import json
import argparse
import time
import httpx
from lxml import etree

NS = "{http://euromod.com/CountryConfig.xsd}"

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

def get_xml_comments(xml_path):
    """Parse the EUROMOD XML to map parameter names to their comments."""
    tree = etree.parse(xml_path)
    root = tree.getroot()
    param_comments = {}
    
    for param in root.findall(f".//{NS}Parameter"):
        name_elem = param.find(f"{NS}Name")
        comment_elem = param.find(f"{NS}Comment")
        if name_elem is not None and comment_elem is not None and name_elem.text:
            if name_elem.text not in param_comments or not param_comments[name_elem.text]:
                param_comments[name_elem.text] = comment_elem.text
    return param_comments

def formulate_query(country_code, year, param_name, param_value, comment):
    """Use Gemini REST API (or fallback) to formulate a native-language search query."""
    prompt = (
        f"You are a legal researcher finding historical tax and benefit legislation for {country_code} in the year {year}. "
        f"We are missing the ground-truth legal text for a EUROMOD parameter.\n"
        f"Parameter Code: {param_name}\n"
        f"Value in {year}: {param_value}\n"
        f"Context/Comment from EUROMOD: {comment}\n\n"
        f"Generate a single, precise search query in the native language of {country_code} "
        f"that would locate the official government gazette or legal text containing this exact parameter/value. "
        f"Focus on the exact legal terms. Include the year {year} if relevant. Do NOT use site: operators, just the keywords."
        f"\n\nOutput ONLY the search query string."
    )
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            response = httpx.post(url, json=payload, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            print(f"  [LLM Error] {e}")
            
    # Fallback deterministic template
    fallback_comment = (comment or param_name).split("-")[0].strip()
    # E.g. "Minimum wage (Salario Mínimo Interprofesional)"
    return f"{fallback_comment} {year} legislation {country_code}"

def active_web_search(query, country_code):
    """Use Exa or Tavily REST API to search for official government sources."""
    exa_key = os.environ.get("EXA_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    domain_suffix = country_code.lower()
    if domain_suffix == "uk": domain_suffix = "co.uk"
    # Exa handles natural language well, so we format a more natural query
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
            else:
                print(f"  [Exa Error] {res.status_code}: {res.text}")
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

def main(country_code, release_version="J2.0+", year=2025):
    load_env()
    
    inference_path = rf'triangulations/{release_version}/{country_code}_inference.json'
    xml_path = rf'models/EUROMOD_RELEASES_{release_version}/XMLParam/Countries/{country_code}/{country_code}.xml'
    
    if not os.path.exists(inference_path):
        print(f"Error: {inference_path} not found.")
        return
        
    if not os.path.exists(xml_path):
        print(f"Error: {xml_path} not found.")
        return

    print(f"--- Starting Search Augmentation for {country_code} ({year}) ---")
    
    with open(inference_path, 'r', encoding='utf-8') as f:
        inference_data = json.load(f)
        
    discrepancies = inference_data.get("discrepancies", [])
    gaps = [d for d in discrepancies if d.get("cr_value") == "Not Found" and d.get("leg_value") == "Not Found"]
    
    print(f"Found {len(gaps)} parameters missing from both CR and Legislation.")
    
    if not gaps:
        print("No gaps to augment.")
        return

    # Limit to 5 for demonstration so it doesn't time out
    gaps = gaps[:5]
    print(f"Processing first {len(gaps)} gaps for augmentation...")

    print("Parsing XML for parameter comments...")
    comments_map = get_xml_comments(xml_path)
    
    augmented_targets = []
    
    for gap in gaps:
        param_display = gap.get("parameter", "")
        param_name = param_display.split(" ")[0].strip()
        val = gap.get("xml_value")
        
        comment = comments_map.get(param_name, "")
        
        print(f"\nProcessing {param_name} (Value: {val})")
        
        query = formulate_query(country_code, year, param_name, val, comment)
        print(f"  Generated Query: {query}")
        
        results = active_web_search(query, country_code)
        
        if results:
            print(f"  Found {len(results)} potential sources:")
            for r in results:
                print(f"    - {r['title']}: {r['url']}")
        else:
            print("  No search results found.")
            
        augmented_targets.append({
            "parameter": param_name,
            "xml_value": val,
            "comment": comment,
            "query": query,
            "results": results
        })
        
        time.sleep(1)
        
    out_dir = f"legislation/{country_code}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/augmented_targets_{year}.json"
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(augmented_targets, f, indent=2, ensure_ascii=False)
        
    print(f"\nSaved {len(augmented_targets)} augmented search targets to {out_path}.")
    print("Next steps:")
    print("1. Review the URLs in the targets JSON.")
    print("2. Add valid URLs to legislation-sources/[CC].md and run the law-scraper.")
    print("3. Re-run triangulation engine.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", required=True)
    parser.add_argument("--release", default="J2.0+")
    parser.add_argument("--year", default=2025, type=int)
    args = parser.parse_args()
    main(args.country, args.release, args.year)