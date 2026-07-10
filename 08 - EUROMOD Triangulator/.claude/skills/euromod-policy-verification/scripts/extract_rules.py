import json
import sys
import os
from lxml import etree

NS = "{http://euromod.com/CountryConfig.xsd}"

def format_policy(policy_data):
    lines = []
    switch_val = policy_data.get('switch', 'on')
    switch_str = "" if switch_val == 'on' else f" *(Switch: {switch_val})*"
    lines.append(f"## Policy: {policy_data['name']}{switch_str}")
    
    for idx, func in enumerate(policy_data['functions']):
        f_switch_val = func.get('switch', 'on')
        f_switch_str = "" if f_switch_val == 'on' else f" *(Switch: {f_switch_val})*"
        lines.append(f"### {idx+1}. Function: {func['name']}{f_switch_str}")
        
        params = func.get('params', {})
        
        if func['name'] == 'DefConst':
            lines.append("  **Constants Defined:**")
            for k, v in params.items():
                lines.append(f"  - `{k}`: {v}")
                
        elif func['name'] == 'ArithOp':
            lines.append(f"  **Formula:** `{params.get('Formula', params.get('formula', ''))}`")
            lines.append(f"  **Output Variable:** `{params.get('Output_Var', params.get('output_var', ''))}`")
            if 'TAX_UNIT' in params:
                lines.append(f"  **Tax Unit:** `{params['TAX_UNIT']}`")
            if 'Run_Cond' in params:
                lines.append(f"  **Run Condition:** `{params['Run_Cond']}`")
                
        elif func['name'] == 'SchedCalc':
            lines.append("  **Schedule Calculation:**")
            lines.append(f"  - **Income Variable:** `{params.get('Income_Var', params.get('income_var', ''))}`")
            lines.append(f"  - **Tax Unit:** `{params.get('TAX_UNIT', '')}`")
            lines.append(f"  - **Output Variable:** `{params.get('Output_Var', params.get('output_var', ''))}`")
            
            bands = {}
            for k, v in params.items():
                if k.startswith('Band'):
                    band_id = k.split('_')[0]
                    prop = k.split('_')[1] if '_' in k else 'Value'
                    if band_id not in bands:
                        bands[band_id] = {}
                    bands[band_id][prop] = v
            
            for band_id, props in sorted(bands.items()):
                lines.append(f"    - {band_id}: Rate=`{props.get('Rate', props.get('rate', ''))}`, Limit=`{props.get('Limit', props.get('limit', ''))}`")

        elif func['name'] == 'Elig':
            lines.append("  **Eligibility Check:**")
            lines.append(f"  - **Condition:** `{params.get('elig_cond', params.get('Elig_Cond', ''))}`")
            lines.append(f"  - **Tax Unit:** `{params.get('TAX_UNIT', '')}`")
            if 'Run_Cond' in params:
                lines.append(f"  **Run Condition:** `{params['Run_Cond']}`")
        
        else:
            for k, v in params.items():
                lines.append(f"  - **{k}**: `{v}`")
                
        lines.append("")
        
    return "\n".join(lines)

def get_version_name(model_folder):
    if model_folder.startswith("EUROMOD_RELEASES_"):
        return model_folder.replace("EUROMOD_RELEASES_", "")
    return model_folder

def extract_rules(country_code, model_folder, year=None):
    release_version = get_version_name(model_folder)
    xml_path = fr"models\{model_folder}\XMLParam\Countries\{country_code}\{country_code}.xml"
    if not os.path.exists(xml_path):
        print(f"Error: {xml_path} not found.")
        sys.exit(1)

    print(f"Parsing {xml_path}...")
    tree = etree.parse(xml_path)
    root = tree.getroot()

    systems = root.findall(f".//{{http://euromod.com/CountryConfig.xsd}}System")
    if not systems:
        print("No systems found.")
        sys.exit(1)

    # Use the most recent system if no year provided
    target_system = systems[-1]
    if year:
        for s in systems:
            if s.find(f"{{http://euromod.com/CountryConfig.xsd}}Year").text == str(year):
                target_system = s
                break

    sys_name = target_system.find(f"{{http://euromod.com/CountryConfig.xsd}}Name").text
    
    policies = target_system.findall(f"{{http://euromod.com/CountryConfig.xsd}}Policy")
    
    extracted_policies = []
    for p in policies:
        p_switch = p.find(f"{{http://euromod.com/CountryConfig.xsd}}Switch").text
        p_name = p.find(f"{{http://euromod.com/CountryConfig.xsd}}Name").text
        
        functions = []
        for f in p.findall(f"{{http://euromod.com/CountryConfig.xsd}}Function"):
            f_switch = f.find(f"{{http://euromod.com/CountryConfig.xsd}}Switch").text
            f_name = f.find(f"{{http://euromod.com/CountryConfig.xsd}}Name").text
            params = {}
            for param in f.findall(f"{{http://euromod.com/CountryConfig.xsd}}Parameter"):
                param_name = param.find(f"{{http://euromod.com/CountryConfig.xsd}}Name").text
                param_val = param.find(f"{{http://euromod.com/CountryConfig.xsd}}Value")
                if param_val is not None:
                    params[param_name] = param_val.text
                
            functions.append({
                "name": f_name,
                "switch": f_switch,
                "params": params
            })
            
        extracted_policies.append({
            "name": p_name,
            "switch": p_switch,
            "functions": functions
        })

    out_dir = f"./policies/{release_version}/{country_code}"
    os.makedirs(out_dir, exist_ok=True)
    
    # Dump JSON intermediate
    json_path = os.path.join(out_dir, f"{sys_name}_rules.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(extracted_policies, f, indent=2)
        
    # Dump Markdown
    md_lines = [f"# EUROMOD Tax-Benefit Rules for {sys_name}\n"]
    for policy in extracted_policies:
        md_lines.append(format_policy(policy))
        md_lines.append("\n---\n")

    md_output = "\n".join(md_lines)
    md_path = os.path.join(out_dir, f"{sys_name}_rules.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_output)

    print(f"Extraction complete for {sys_name}.")
    print(f"JSON intermediate: {json_path}")
    print(f"Markdown output  : {md_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract EUROMOD XML policies to structured Markdown.")
    parser.add_argument("country_code", help="2-letter country code (e.g. AT, ES)")
    parser.add_argument("--model-folder", default="EUROMOD_RELEASES_J2.0+", help="Folder name inside ./models/ (default: EUROMOD_RELEASES_J2.0+)")
    args = parser.parse_args()
    
    model_folder = args.model_folder
    if not model_folder:
        model_dirs = [d for d in os.listdir("models") if os.path.isdir(os.path.join("models", d))]
        if len(model_dirs) == 1:
            model_folder = model_dirs[0]
        else:
            print("Error: Multiple or no folders in ./models/. Please specify --model-folder")
            sys.exit(1)
            
    extract_rules(args.country_code, model_folder)
