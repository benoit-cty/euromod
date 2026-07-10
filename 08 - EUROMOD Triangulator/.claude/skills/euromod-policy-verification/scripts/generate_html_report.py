import json
import os
import argparse
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EUROMOD Triangulation Report: {country}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .summary-box {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #3498db; }}
        .stats-text {{ font-style: italic; color: #555; margin-bottom: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 15px; border: 1px solid #ddd; text-align: left; }}
        th {{ background-color: #f1f5f9; font-weight: 600; color: #2c3e50; }}
        tr:nth-child(even) {{ background-color: #fcfcfc; }}
        .status-cell {{ text-align: center; font-size: 18px; }}
        .policy-header {{ background-color: #e2e8f0; font-weight: bold; }}
        .val-col {{ font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; }}
        .explanation {{ font-size: 13px; color: #666; max-width: 300px; }}
        ul {{ margin: 0; padding-left: 20px; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>EUROMOD Triangulation Report: {country}</h1>
    <div class="summary-box">
        <strong>Model Release:</strong> {version}<br>
        <strong>Baseline Year:</strong> {year}<br>
        <strong>Generated on:</strong> {date}<br><br>
        <em>Reporting Logic: <strong>Legislation is King</strong>. National legislation as stored in ./legislation is the ground truth. Both the Country Report (CR) and the EUROMOD Model XML are evaluated against it.</em>
    </div>

    <h2>1. Executive Summary</h2>
    <table>
        <tr>
            <th>Category</th>
            <th>Parameters</th>
            <th>Policies</th>
            <th>Description</th>
        </tr>
        <tr>
            <td><strong>Discrepancies</strong></td>
            <td>{d_params}</td>
            <td>{d_pols}</td>
            <td>XML value contradicts or is not found in Legislation (XML ❌).</td>
        </tr>
        <tr>
            <td><strong>Action Required: Update Country Report</strong></td>
            <td>{p_params}</td>
            <td>{p_pols}</td>
            <td>XML matches Legislation, but CR differs or missed it (CR ❌).</td>
        </tr>
        <tr>
            <td><strong>Matches</strong></td>
            <td>{m_params}</td>
            <td>{m_pols}</td>
            <td>Perfect alignment: XML and CR both match Legislation (✅).</td>
        </tr>
    </table>

    {content}
</body>
</html>
"""

def build_section(title, data_list, is_alert=False):
    if not data_list:
        return f"<h2>{title}</h2>\n<p class='stats-text'>0 parameter findings.</p>\n<p><em>(None found)</em></p>\n"

    # Group by policy
    policies = {}
    for item in data_list:
        pol = item.get("policy", "Unknown")
        if pol not in policies:
            policies[pol] = []
        policies[pol].append(item)

    param_count = len(data_list)
    pol_count = len(policies)
    
    html = ""
    if is_alert:
        html += f"<div style='background-color: #fff3f3; border-left: 5px solid #e74c3c; padding: 15px; margin-bottom: 20px; border-radius: 5px;'>\n"
        html += f"<h2 style='color: #c0392b; margin-top: 0;'>🚨 {title}</h2>\n"
        html += f"<p>The following <strong>{param_count} parameters</strong> across <strong>{pol_count} policies</strong> are actively coded in the model and legally valid according to National Legislation, but are completely undocumented or differ in the Country Report. Please update the Country Report to include these.</p>\n"
    else:
        html += f"<h2>{title}</h2>\n"
        html += f"<p class='stats-text'>{param_count} parameter findings across {pol_count} policies.</p>\n"
    
    html += "<table>\n"
    html += "<tr><th>Parameter</th><th>Legislation Value</th><th>CR Value</th><th>XML Value</th><th title='Country Report Match'>CR ✅/❌</th><th title='XML Model Match'>XML ✅/❌</th><th>Explanation</th></tr>\n"
    
    for pol, items in policies.items():
        html += f"<tr class='policy-header'><td colspan='7'>Policy: <code>{pol}</code></td></tr>\n"
        for item in items:
            html += "<tr>\n"
            html += f"  <td><code>{item.get('parameter', '')}</code></td>\n"
            html += f"  <td class='val-col'>{item.get('leg_value', '-')}</td>\n"
            html += f"  <td class='val-col'>{item.get('cr_value', '-')}</td>\n"
            html += f"  <td class='val-col'>{item.get('xml_value', '-')}</td>\n"
            html += f"  <td class='status-cell'>{item.get('cr_match', '')}</td>\n"
            html += f"  <td class='status-cell'>{item.get('xml_match', '')}</td>\n"
            html += f"  <td class='explanation'>{item.get('explanation', '')}</td>\n"
            html += "</tr>\n"
            
    html += "</table>\n"
    
    if is_alert:
        html += "</div>\n"
        
    return html

def build_ghost_laws_section(ghost_laws_path):
    try:
        with open(ghost_laws_path, 'r', encoding='utf-8') as f:
            ghost_laws = json.load(f)
    except Exception as e:
        return f"<h2>5. Discovered Governing Laws (Top-Down Search)</h2>\n<p>Error loading ghost laws: {e}</p>"

    if not ghost_laws:
        return ""

    html = "<h2>5. Discovered Governing Laws (Top-Down Search)</h2>\n"
    html += "<p class='stats-text'>Governing laws discovered via top-down macro-policy search using Country Report headers.</p>\n"
    html += "<table>\n"
    html += "<tr><th>Macro-Policy Category</th><th>Search Query</th><th>Discovered Official Legal Sources</th></tr>\n"
    
    for item in ghost_laws:
        policy_name = item.get("policy_name", "Unknown Policy")
        query = item.get("query", "")
        results = item.get("results", [])
        
        results_html = ""
        if results:
            results_html += "<ul>\n"
            for r in results:
                title = r.get("title", "Untitled Source")
                url = r.get("url", "#")
                results_html += f"  <li><a href='{url}' target='_blank'>{title}</a></li>\n"
            results_html += "</ul>\n"
        else:
            results_html = "<em>No official sources found.</em>"
            
        html += "<tr>\n"
        html += f"  <td><strong>{policy_name}</strong></td>\n"
        html += f"  <td><code>{query}</code></td>\n"
        html += f"  <td>{results_html}</td>\n"
        html += "</tr>\n"
        
    html += "</table>\n"
    return html

def generate_report(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    discrepancies = data.get("discrepancies", [])
    potentials = data.get("potentials", [])
    matches = data.get("matches", [])

    # Calculate stats
    d_params = len(discrepancies)
    d_pols = len(set(i.get("policy") for i in discrepancies))
    p_params = len(potentials)
    p_pols = len(set(i.get("policy") for i in potentials))
    m_params = len(matches)
    m_pols = len(set(i.get("policy") for i in matches))

    content_html = ""
    # Render potentials FIRST and highlight them
    content_html += build_section("Action Required: Update Country Report", potentials, is_alert=True)
    content_html += build_section("3. Discrepancies", discrepancies)
    content_html += build_section("4. Matches", matches)

    country_code = data.get("country", "Unknown")
    year = data.get("year", "Unknown")
    ghost_laws_path = f"legislation/{country_code}/ghost_laws_{year}.json"
    if os.path.exists(ghost_laws_path):
        content_html += build_ghost_laws_section(ghost_laws_path)

    final_html = HTML_TEMPLATE.format(
        country=data.get("country", "Unknown"),
        version=data.get("version", "Unknown"),
        year=data.get("year", "Unknown"),
        date=datetime.now().strftime("%Y-%m-%d"),
        d_params=d_params, d_pols=d_pols,
        p_params=p_params, p_pols=p_pols,
        m_params=m_params, m_pols=m_pols,
        content=content_html
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML Triangulation Report from JSON inference data.")
    parser.add_argument("json_path", help="Path to the JSON inference file")
    parser.add_argument("output_path", help="Path to save the HTML report")
    args = parser.parse_args()
    
    generate_report(args.json_path, args.output_path)
    print(f"HTML Report generated at: {args.output_path}")