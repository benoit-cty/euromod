import json
import os
import argparse
from collections import defaultdict

def run_inference(country_code, release_version="J2.0+", year=2025):
    json_path = rf'policies/{release_version}/{country_code}/{country_code}_{year}_rules.json'
    cr_path = rf'country-reports/Y16/{country_code}_Y16.md'
    leg_dir = rf'legislation/{country_code}'
    out_json = rf'triangulations/{release_version}/{country_code}_inference.json'

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    def get_variants(val_str):
        if val_str is None:
            return []
        val_str = str(val_str).split('#')[0].strip()
        try:
            val_float = float(val_str)
        except ValueError:
            return []
            
        if val_float <= 10 and val_float % 1 == 0:
            return []
            
        variants = set()
        val_int = int(val_float)
        
        if val_float == val_int:
            s = str(val_int)
            variants.add(s)
            if len(s) >= 4:
                variants.add(f"{val_int:,}")
                variants.add(f"{val_int:,}".replace(',', '.'))
                variants.add(f"{val_int:,}".replace(',', ' '))
        else:
            variants.add(str(val_float))
            variants.add(str(val_float).replace('.', ','))
            variants.add(f"{val_float:.2f}")
            variants.add(f"{val_float:.2f}".replace('.', ','))
            if val_float > 999:
                variants.add(f"{val_float:,.2f}")
                variants.add(f"{val_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                
        if 0 < val_float < 1:
            pct = val_float * 100
            if pct == int(pct):
                variants.add(str(int(pct)))
                variants.add(f"{int(pct)}%")
            else:
                variants.add(str(pct))
                variants.add(str(pct).replace('.', ','))
                variants.add(f"{pct:.2f}")
                variants.add(f"{pct:.2f}".replace('.', ','))
                
        return list(variants)

    print(f"Loading data sources for {country_code}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        policies = json.load(f)

    with open(cr_path, 'r', encoding='utf-8') as f:
        cr_text = f.read()

    leg_text = ""
    for root, dirs, files in os.walk(leg_dir):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    leg_text += f.read() + "\n"

    print(f"Analyzing whole policy spine for {country_code}...")

    discrepancies = []
    potentials = []
    matches = []

    for p in policies:
        p_name = p.get('name', 'Unnamed_Policy')
        if p_name is None:
            p_name = 'Unnamed_Policy'
            
        p_switch = p.get('switch', 'on')
        if p_switch != 'on':
            p_name += f" (Switch: {p_switch})"
            
        for fn in p['functions']:
            f_switch = fn.get('switch', 'on')
            for k, v in fn.get('params', {}).items():
                if v is None:
                    continue
                k_lower = k.lower()
                if k.lower() == '$policyyear':
                    continue
                if not (k.startswith('$') or 'lim' in k_lower or 'amt' in k_lower or 'rate' in k_lower or 'thres' in k_lower or 'band' in k_lower):
                    continue
                    
                variants = get_variants(v)
                if not variants:
                    continue
                    
                in_cr = any(var in cr_text for var in variants)
                in_leg = any(var in leg_text for var in variants)
                
                clean_val = str(v).split('#')[0].strip()
                
                # Skip instrumental infinity limits used in EUROMOD brackets
                try:
                    if float(clean_val) >= 9999999999:
                        continue
                except ValueError:
                    pass
                
                param_display = k
                if f_switch != 'on':
                    param_display += f" (Func Switch: {f_switch})"
                
                res = {
                    'policy': p_name,
                    'parameter': param_display, 
                    'xml_value': clean_val, 
                    'cr_value': clean_val if in_cr else "Not Found",
                    'leg_value': clean_val if in_leg else "Not Found",
                    'cr_match': "✅" if in_cr and in_leg else ("❌" if in_leg else "❌"), 
                    'xml_match': "✅" if in_leg else "❌", 
                }
                
                if in_leg and in_cr:
                    res['explanation'] = "Parameter perfectly aligned across XML, CR, and National Legislation."
                    matches.append(res)
                elif not in_leg:
                    res['explanation'] = "XML parameter value could not be found in the provided National Legislation."
                    discrepancies.append(res)
                else:
                    res['explanation'] = "Parameter matches Legislation and XML, but was not found in the Country Report."
                    potentials.append(res)

    output_data = {
        "country": country_code,
        "version": release_version,
        "year": year,
        "discrepancies": discrepancies,
        "potentials": potentials,
        "matches": matches
    }

    os.makedirs(os.path.dirname(out_json), exist_ok=True)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    print(f"Inference JSON saved to {out_json}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("country_code")
    parser.add_argument("--release", default="J2.0+")
    parser.add_argument("--year", default=2025, type=int)
    args = parser.parse_args()
    run_inference(args.country_code, args.release, args.year)