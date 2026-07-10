"""
map_changes.py
==============
Phase 1 of the EUROMOD policy-implementation workflow.

Given:
  - A set of verified policy-parameter docx files (year t → t+1 changes)
  - The EUROMOD country XML containing the system for year t

Produces:
  - changes_{CC}_{YYYY}.html  — HTML report: each docx changed row mapped to
    its XML DefConst location(s) with parametric / structural classification
  - changes_{CC}_{YYYY}.json  — machine-readable change manifest

Algorithm
---------
1.  Build a DefConst index from the year-t system:
        round(value, 2) → [(policy, param_name, raw_value, unit)]
2.  For each docx, find rows where the "Change in t+1" column is non-empty.
3.  For each changed row, extract numeric values from the year-t text,
    look them up in the DefConst index, and collect XML matches.
4.  Classify the change as parametric / structural / label-only / unclear.
5.  Optionally enrich with known new values from a pre-existing update script.
6.  Render HTML + JSON.

Preferred usage:
    python map_changes.py --config map_changes.config.json

One-off usage:
    python map_changes.py --xml-path path\\to\\CC.xml --docx-dir path\\to\\CC \
        --country SI --base-year 2025 --new-year 2026

CLI flags override values from the JSON config file. JSON config values override
the optional SETTINGS fallback block below.
"""

import argparse
import re
import json
from pathlib import Path
from collections import defaultdict

try:
    from lxml import etree
except ImportError:
    etree = None

try:
    from docx import Document
except ImportError:
    Document = None

# ============================================================================
# SETTINGS — optional fallbacks for repeated local use.
# Prefer --config or CLI flags so the script stays portable across users.
# ============================================================================

DEFAULT_CONFIG_FILE = "map_changes.config.json"

XML_PATH    = None
DOCX_DIR    = None
COUNTRY     = None
BASE_YEAR   = None
NEW_YEAR    = None
BASE_SYSTEM = None
OUTPUT_DIR  = None

# Verification JSON output from the policy-verification skill.
# Set to None to skip the gate check.
VERIFICATION_JSON = None

# Docx files to process: display label -> filename.
# Prefer supplying these in map_changes.config.json under the `docx_files` key.
DOCX_FILES = {}

# ============================================================================
# VERIFICATION GATE
# ============================================================================

def check_verification_gate(json_path):
    """
    Load the verification issues JSON and check for unresolved issues.
    Returns (ok: bool, message: str).
    Blocks on 'factual' severity; warns on 'incomplete'.
    """
    if not json_path:
        return True, "No verification JSON configured — gate skipped."
    path = Path(json_path)
    if not path.exists():
        return True, f"Verification JSON not found at {json_path} — gate skipped."

    data = json.loads(path.read_text(encoding='utf-8'))
    issues = data.get('issues', []) + data.get('cross_doc_issues', [])

    factual    = [i for i in issues if i.get('severity') == 'factual']
    incomplete = [i for i in issues if i.get('severity') == 'incomplete']

    lines = []
    if factual:
        lines.append(f"  BLOCKED: {len(factual)} unresolved factual issue(s):")
        for i in factual[:5]:
            pol  = i.get('policy', i.get('field', '?'))
            fld  = i.get('field', '')
            desc = i.get('source_says') or i.get('description', '')
            lines.append(f"    [{pol}] {fld}: {desc[:120]}")
        if len(factual) > 5:
            lines.append(f"    ... and {len(factual)-5} more")
    if incomplete:
        lines.append(f"  WARNING: {len(incomplete)} incomplete item(s) — review before implementing:")
        for i in incomplete[:3]:
            fld  = i.get('field', '?')
            desc = i.get('description', i.get('source_says', ''))[:100]
            lines.append(f"    {fld}: {desc}")

    if factual:
        return False, '\n'.join(lines)
    msg = ('Verification gate passed.')
    if incomplete:
        msg += f' ({len(incomplete)} incomplete warning(s) noted below)\n' + '\n'.join(lines)
    return True, msg


# ============================================================================
# XML INDEX
# ============================================================================

NS = "{http://euromod.com/CountryConfig.xsd}"

_UNIT_RE  = re.compile(r'^([\d,.]+)\s*#([mywdMYWD])\s*$')
_BARE_RE  = re.compile(r'^[\d,.]+$')
_PCT_RE   = re.compile(r'^([\d,.]+)\s*%\s*$')


def _to_float(s):
    try:
        return float(s.replace(',', ''))
    except ValueError:
        return None


def _parse_xml_val(v):
    """Return (float, unit_char) or None for non-numeric / n/a values."""
    v = v.strip()
    if v.lower() in ('n/a', '', 'n'):
        return None
    m = _UNIT_RE.match(v)
    if m:
        f = _to_float(m.group(1))
        return (f, m.group(2).lower()) if f is not None else None
    # Exclude bare percentages from the lookup index — they match too broadly
    # (80%, 60%, 50% are rates that appear in many unrelated policy descriptions)
    m = _PCT_RE.match(v)
    if m:
        return None   # skip percentage-valued params from value index
    if _BARE_RE.match(v):
        f = _to_float(v)
        return (f, '') if f is not None else None
    return None


def build_defconst_index(xml_path, system_name):
    """
    Returns:
      index     : {round(val, 2): [(policy, param, raw_value, unit), ...]}
      all_params: [(policy, param, raw_value), ...]
    Only DefConst parameters whose name starts with '$'.
    """
    tree = etree.parse(str(xml_path))
    root = tree.getroot()
    index = defaultdict(list)
    all_params = []

    for sys_el in root.iter(f"{NS}System"):
        if sys_el.findtext(f"{NS}Name") != system_name:
            continue
        for pol_el in sys_el.findall(f"{NS}Policy"):
            pol = pol_el.findtext(f"{NS}Name") or ""
            for fun_el in pol_el.findall(f"{NS}Function"):
                if fun_el.findtext(f"{NS}Name") != "DefConst":
                    continue
                for par_el in fun_el.findall(f"{NS}Parameter"):
                    pname = par_el.findtext(f"{NS}Name") or ""
                    pval  = par_el.findtext(f"{NS}Value") or ""
                    if not pname.startswith("$"):
                        continue
                    all_params.append((pol, pname, pval))
                    parsed = _parse_xml_val(pval)
                    if parsed and parsed[0] is not None and parsed[0] > 0:
                        key = round(parsed[0], 2)
                        index[key].append((pol, pname, pval, parsed[1]))
        break  # found our system

    return dict(index), all_params


# ============================================================================
# NUMBER EXTRACTION
# ============================================================================

# Matches: 1,234.5678  |  9210.26  |  530.19  |  19,736.99  |  1.17259
# (any number with digits, optional comma-thousands, optional decimal)
_NUM_RE = re.compile(r'(?<![.\d])(\d[\d,]*(?:\.\d+)?)(?![.\d])')


def extract_numbers(text):
    """
    Return list of (float_val, match_start, match_end).

    Filtering rules applied to avoid noise:
      - Skip year-like integers in [2000, 2099]
      - Keep val >= 50  (monetary amounts)
      - OR keep val with >= 4 decimal places  (coefficients like 1.17259)
      - Keep val in [0.5, 50) only if it has >= 4 decimal digits (tight coeff)
      - Ignore val < 0.5
    """
    results = []
    for m in _NUM_RE.finditer(text):
        raw = m.group(1).replace(',', '')
        try:
            val = float(raw)
        except ValueError:
            continue
        if 2000 <= val <= 2099:
            continue
        if val < 0.5:
            continue
        dec_places = len(raw.split('.')[-1]) if '.' in raw else 0
        # Avoid small-number false positives (e.g. "6.1" as garbled "614.14")
        if val < 50 and dec_places < 4:
            continue
        results.append((round(val, 2), m.start(), m.end()))
    return results


# ============================================================================
# DOCX PARSING
# ============================================================================

def parse_docx_changes(docx_path, label):
    """
    Parse a 3-column policy table (Field | year-t | Change in year-t+1).
    Returns list of row dicts for ALL substantive rows.
    Rows with an empty 3rd column are included with type 'no_change'.
    """
    doc = Document(str(docx_path))
    rows = []
    for tbl_idx, table in enumerate(doc.tables):
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells]
            if len(cells) < 3:
                continue
            if cells[0] in ('Field', ''):
                continue
            # Skip header-only rows (all cells empty or only first filled)
            if not cells[1] and not cells[2]:
                continue
            rows.append({
                'doc':         label,
                'field':       cells[0],
                'text_t':      cells[1],
                'text_t1':     cells[2],
                'table_idx':   tbl_idx,
                'has_change':  bool(cells[2]),
            })
    return rows


# ============================================================================
# CHANGE CLASSIFICATION
# ============================================================================

# Keywords that strongly suggest a structural (formula / logic) change.
# IMPORTANT: only trigger if these appear in text that is *new* in t+1
# (i.e. NOT present in text_t). We compare after stripping shared text.
_STRUCTURAL_KW = [
    r'\bformula\b', r'\blinked to\b',
    r'%\s+of\s+(?:the\s+)?(?:minimum|average|net)\s+wage',
    r'\babolish', r'\bintroduc', r'\breplac', r'\bnew component',
    r'\bno longer\b', r'\binstead of\b',
    r'\btier', r'\bnew rule', r'\bnew calculation\b', r'\bnew formula\b',
    r'\bnew supplement\b',
]
_STRUC_RE = re.compile('|'.join(_STRUCTURAL_KW), re.IGNORECASE)


def classify(text_t, text_t1):
    """Return 'parametric' | 'structural' | 'label_only' | 'unclear'."""
    # Only flag structural if the keyword appears in text that is genuinely NEW
    # in t+1 — i.e. not already present in text_t.
    if _STRUC_RE.search(text_t1):
        # Check if it also appears in t (shared boilerplate → not structural)
        t1_unique = text_t1
        if not _STRUC_RE.search(text_t):
            return 'structural'

    # Remove year numbers; if the only difference was a year label, call it label_only
    t_ny  = re.sub(r'\b20\d\d\b', 'YEAR', text_t)
    t1_ny = re.sub(r'\b20\d\d\b', 'YEAR', text_t1)
    nums_t  = {round(v, 1) for v, _, _ in extract_numbers(t_ny)}
    nums_t1 = {round(v, 1) for v, _, _ in extract_numbers(t1_ny)}

    # If both sides have the same set of meaningful numbers after stripping years
    # (or both have none), it's a label-only change
    if nums_t == nums_t1:
        return 'label_only'

    # t1 has fewer numbers (values blanked out) or different numbers → parametric
    if not nums_t1 or nums_t1 != nums_t:
        return 'parametric'

    return 'unclear'


# ============================================================================
# XML MATCHING
# ============================================================================

def match_row(row, xml_index, known_new=None):
    """
    For each number extracted from the year-t text, look it up in the DefConst
    index.  Returns a deduplicated list of match dicts.
    known_new: {(policy, param_name): new_value_str}
    """
    numbers = extract_numbers(row['text_t'])
    found = {}  # (policy, param) -> match dict (deduplicated)
    for val, start, end in numbers:
        for pol, pname, raw_val, unit in xml_index.get(val, []):
            key = (pol, pname)
            if key not in found:
                new_val = (known_new or {}).get(key)
                found[key] = {
                    'policy':     pol,
                    'param':      pname,
                    'raw_value':  raw_val,
                    'unit':       unit,
                    'new_value':  new_val,
                    'matched_on': val,
                }
    return list(found.values())


# ============================================================================
# HTML GENERATION
# ============================================================================

_CSS = """
body{font-family:Arial,sans-serif;margin:24px;max-width:1500px;color:#222}
h1{margin-bottom:4px}
h2{color:#444;border-bottom:2px solid #ccc;padding-bottom:4px;margin-top:36px}
.meta{color:#666;font-size:.9em;margin-bottom:16px}
.summary{display:flex;flex-wrap:wrap;gap:16px;background:#f8f9fa;border:1px solid
 #dee2e6;padding:12px 20px;border-radius:4px;margin:16px 0;align-items:center}
.badge{padding:2px 9px;border-radius:3px;font-size:.82em;color:#fff;font-weight:bold;
 white-space:nowrap}
.bp{background:#28a745}.bs{background:#dc3545}
.bl{background:#6c757d}.bu{background:#fd7e14}.bn{background:#aaa;color:#fff}
table{border-collapse:collapse;width:100%;margin-bottom:28px;font-size:.84em}
th{background:#343a40;color:#fff;padding:8px 10px;text-align:left}
td{padding:7px 10px;border:1px solid #ddd;vertical-align:top}
tr.pr{background:#f0fff4}tr.sr{background:#fff5f5}
tr.lr{background:#f8f9fa}tr.ur{background:#fffbf0}tr.nc{background:#f0f0f0;color:#888}
.mono{font-family:monospace;font-size:.92em;color:#005a9e}
.nv{color:#155724;font-weight:bold}
.unk{color:#856404;font-style:italic;font-size:.9em}
.dim{color:#999;font-style:italic}
.sep{color:#aaa;margin:0 4px}
"""

_ROW_CLASS = {
    'parametric': 'pr', 'structural': 'sr',
    'label_only': 'lr', 'unclear': 'ur', 'no_change': 'nc',
}
_BADGE_CLASS = {
    'parametric': 'bp', 'structural': 'bs',
    'label_only': 'bl', 'unclear': 'bu', 'no_change': 'bn',
}


def _e(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def generate_html(all_rows, output_path, country, base_year, new_year):
    counts = defaultdict(int)
    for r in all_rows:
        counts[r['type']] += 1

    docs = {}
    for r in all_rows:
        docs.setdefault(r['doc'], []).append(r)

    changed_rows = [r for r in all_rows if r['type'] != 'no_change']
    n_matched    = sum(1 for r in changed_rows if r.get('xml_matches'))
    n_with_newval = sum(
        1 for r in changed_rows
        for m in r.get('xml_matches', []) if m.get('new_value')
    )

    html = [f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{country} {new_year} — Policy Changes XML Map</title>
<style>{_CSS}</style></head><body>
<h1>{country} {new_year} — Policy Changes: XML Location Report</h1>
<p class="meta">
  Source system: <code>{country}_{base_year}</code> DefConst index&nbsp;&nbsp;·&nbsp;&nbsp;
  {len(changed_rows)} changed rows across {len(docs)} documents&nbsp;&nbsp;·&nbsp;&nbsp;
  {n_matched} rows matched to XML&nbsp;&nbsp;·&nbsp;&nbsp;
  {n_with_newval} XML params with known new values
</p>
<div class="summary">
  <span><span class="badge bp">parametric</span>&nbsp;{counts['parametric']}</span>
  <span><span class="badge bs">structural</span>&nbsp;{counts['structural']}</span>
  <span><span class="badge bl">label only</span>&nbsp;{counts['label_only']}</span>
  <span><span class="badge bu">unclear</span>&nbsp;{counts['unclear']}</span>
  <span><span class="badge bn">no change</span>&nbsp;{counts['no_change']}</span>
  <strong style="margin-left:8px">Total rows: {len(all_rows)}</strong>
</div>
"""]

    for doc_label, rows in docs.items():
        html.append(f'<h2>{_e(doc_label)}</h2>\n')
        html.append(
            f'<table><thead><tr>'
            f'<th style="width:120px">Field</th>'
            f'<th style="width:28%">{base_year} (current)</th>'
            f'<th style="width:28%">{new_year} change</th>'
            f'<th>XML DefConst match(es)</th>'
            f'<th style="width:100px">Type</th>'
            f'</tr></thead><tbody>\n'
        )
        for r in rows:
            t = r['type']
            rc    = _ROW_CLASS.get(t, 'ur')
            bcls  = _BADGE_CLASS.get(t, 'bu')
            badge = f'<span class="badge {bcls}">{_e(t)}</span>'

            matches = r.get('xml_matches', [])
            if t == 'no_change':
                xml_cell = '<span class="dim">—</span>'
            elif matches:
                parts = []
                for m in matches:
                    if m.get('new_value'):
                        arrow = (f'<span class="sep">→</span>'
                                 f'<span class="nv">{_e(m["new_value"])}</span>')
                    else:
                        arrow = '<span class="sep">→</span><span class="unk">?</span>'
                    parts.append(
                        f'<span class="mono">{_e(m["policy"])}'
                        f'&nbsp;/&nbsp;{_e(m["param"])}'
                        f'&nbsp;=&nbsp;{_e(m["raw_value"])}</span>{arrow}'
                    )
                xml_cell = '<br>'.join(parts)
            else:
                xml_cell = '<span class="dim">no match</span>'

            html.append(
                f'<tr class="{rc}">'
                f'<td><strong>{_e(r["field"])}</strong></td>'
                f'<td style="white-space:pre-wrap">{_e(r["text_t"][:400])}</td>'
                f'<td style="white-space:pre-wrap">{_e(r["text_t1"][:400])}</td>'
                f'<td>{xml_cell}</td>'
                f'<td>{badge}</td>'
                f'</tr>\n'
            )
        html.append('</tbody></table>\n')

    html.append('</body></html>')
    out = Path(output_path)
    out.write_text(''.join(html), encoding='utf-8')
    print(f"  HTML → {out}")


# ============================================================================
# MAIN
# ============================================================================

def load_known_changes(docx_dir, country, new_year):
    """
    Try to import CHANGES from update_{cc}_{year}.py in docx_dir.
    Returns {(policy, param_name): new_value_str} or {}.
    """
    import importlib.util
    script = Path(docx_dir) / f"update_{country.lower()}_{new_year}.py"
    if not script.exists():
        return {}
    try:
        spec = importlib.util.spec_from_file_location("_update_script", script)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        known = {}
        for policy, params in getattr(mod, 'CHANGES', {}).items():
            for pname, change_tuple in params.items():
                # change_tuple is (old_val, new_val, verified, source)
                new_val = change_tuple[1] if len(change_tuple) > 1 else None
                if new_val:
                    known[(policy, pname)] = new_val
        print(f"  Loaded {len(known)} known new values from {script.name}")
        return known
    except Exception as exc:
        print(f"  WARNING: could not load known changes: {exc}")
        return {}


def build_parser():
    parser = argparse.ArgumentParser(
        description="Map verified docx changes to XML DefConst parameters.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--config",
        default=None,
        help=(
            "Path to a JSON config file. If omitted, map_changes.config.json in "
            "the current working directory is used when present."
        ),
    )
    parser.add_argument("--xml-path", default=None, help="Path to the country XML file.")
    parser.add_argument("--docx-dir", default=None, help="Directory containing the policy docx files.")
    parser.add_argument("--country", default=None, help="Two-letter country code, e.g. SI.")
    parser.add_argument("--base-year", type=int, default=None, help="Base year t, e.g. 2025.")
    parser.add_argument("--new-year", type=int, default=None, help="New year t+1, e.g. 2026.")
    parser.add_argument(
        "--base-system",
        default=None,
        help="System name to index in the XML. Defaults to COUNTRY_BASEYEAR if omitted.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for the HTML/JSON report. Defaults to DOCX_DIR if omitted.",
    )
    parser.add_argument(
        "--verification-json",
        default=None,
        help="Path to the verification issues JSON. Omit to skip the gate if no config/settings value is set.",
    )
    return parser


def load_json_config(config_path):
    if not config_path:
        return {}

    path = Path(config_path)
    if not path.exists():
        raise SystemExit(f"ERROR: config file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: could not parse config JSON {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: config file must contain a top-level JSON object: {path}")
    return data


def resolve_settings(args):
    config_path = args.config
    if config_path is None and Path(DEFAULT_CONFIG_FILE).exists():
        config_path = DEFAULT_CONFIG_FILE

    config = load_json_config(config_path)

    xml_path = args.xml_path or config.get('xml_path') or XML_PATH
    docx_dir = args.docx_dir or config.get('docx_dir') or DOCX_DIR
    country = args.country or config.get('country') or COUNTRY
    base_year = args.base_year or config.get('base_year') or BASE_YEAR
    new_year = args.new_year or config.get('new_year') or NEW_YEAR
    base_system = args.base_system or config.get('base_system') or BASE_SYSTEM
    verification_json = args.verification_json
    if verification_json is None:
        verification_json = config.get('verification_json', VERIFICATION_JSON)
    output_dir = args.output_dir or config.get('output_dir') or OUTPUT_DIR
    docx_files = config.get('docx_files') or DOCX_FILES

    if country is not None:
        country = str(country).strip().upper()
    if base_system is None and country and base_year:
        base_system = f"{country}_{base_year}"
    if output_dir is None and docx_dir:
        output_dir = docx_dir

    missing = []
    for label, value in (
        ('xml_path', xml_path),
        ('docx_dir', docx_dir),
        ('country', country),
        ('base_year', base_year),
        ('new_year', new_year),
        ('base_system', base_system),
        ('output_dir', output_dir),
    ):
        if value in (None, ""):
            missing.append(label)
    if missing:
        joined = ', '.join(missing)
        raise SystemExit(
            "ERROR: missing required settings: "
            f"{joined}. Provide them via CLI flags, {DEFAULT_CONFIG_FILE}, or the SETTINGS block."
        )

    if not isinstance(docx_files, dict) or not docx_files:
        raise SystemExit(
            "ERROR: no docx_files configured. Provide a non-empty 'docx_files' object via "
            f"{DEFAULT_CONFIG_FILE} or the SETTINGS block."
        )

    return {
        'xml_path': Path(xml_path),
        'docx_dir': Path(docx_dir),
        'country': country,
        'base_year': int(base_year),
        'new_year': int(new_year),
        'base_system': base_system,
        'output_dir': Path(output_dir),
        'verification_json': verification_json,
        'docx_files': {str(label): str(fname) for label, fname in docx_files.items()},
    }


def require_dependencies():
    missing = []
    if etree is None:
        missing.append('lxml')
    if Document is None:
        missing.append('python-docx')
    if missing:
        joined = ', '.join(missing)
        raise SystemExit(
            "ERROR: missing required Python packages: "
            f"{joined}. Install them in the active environment before running map_changes.py."
        )


def main():
    args = build_parser().parse_args()
    settings = resolve_settings(args)
    require_dependencies()

    xml_path = settings['xml_path']
    docx_dir = settings['docx_dir']
    out_dir  = settings['output_dir']
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1 — build XML index
    print(f"Building DefConst index from {settings['base_system']} ...")
    xml_index, all_params = build_defconst_index(xml_path, settings['base_system'])
    n_entries = sum(len(v) for v in xml_index.values())
    print(f"  {n_entries} indexed entries ({len(all_params)} total DefConst params, "
          f"{len(xml_index)} distinct numeric keys)")

    # 2 — verification gate
    print("Checking verification gate ...")
    gate_ok, gate_msg = check_verification_gate(settings['verification_json'])
    print(f"  {gate_msg}")
    if not gate_ok:
        print("\nImplementation blocked — resolve verification issues first.")
        return

    # 3 — load known new values (from update script if available)
    known_new = load_known_changes(docx_dir, settings['country'], settings['new_year'])

    # 4 — parse docx files
    all_rows = []
    print("Parsing docx files ...")
    for label, fname in settings['docx_files'].items():
        path = docx_dir / fname
        if not path.exists():
            print(f"  WARNING: {fname} not found, skipping")
            continue
        rows = parse_docx_changes(path, label)
        n_changed  = sum(1 for r in rows if r['has_change'])
        n_nochange = len(rows) - n_changed
        print(f"  {label}: {n_changed} change(s), {n_nochange} no-change row(s)")
        for row in rows:
            if not row['has_change']:
                row['type']        = 'no_change'
                row['xml_matches'] = []
            else:
                row['type']        = classify(row['text_t'], row['text_t1'])
                row['xml_matches'] = match_row(row, xml_index, known_new)
        all_rows.extend(rows)

    changed_rows = [r for r in all_rows if r['type'] != 'no_change']
    print(f"\nTotal: {len(all_rows)} rows ({len(changed_rows)} with changes)")

    # 5 — type summary
    counts = defaultdict(int)
    for r in all_rows:
        counts[r['type']] += 1
    for t, n in counts.items():
        print(f"  {t}: {n}")

    matched = [r for r in changed_rows if r.get('xml_matches')]
    print(f"  Rows with XML match: {len(matched)} / {len(changed_rows)}")

    # 5 — write outputs
    stem = f"changes_{settings['country']}_{settings['new_year']}"

    html_path = out_dir / f"{stem}.html"
    print(f"\nWriting HTML report ...")
    generate_html(all_rows, html_path, settings['country'], settings['base_year'], settings['new_year'])

    json_path = out_dir / f"{stem}.json"
    manifest = [
        {
            'doc':         r['doc'],
            'field':       r['field'],
            'text_t':      r['text_t'],
            'text_t1':     r['text_t1'],
            'type':        r['type'],
            'xml_matches': r.get('xml_matches', []),
        }
        for r in all_rows
    ]
    json_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    print(f"  JSON → {json_path}")
    print("\nDone.")


if __name__ == '__main__':
    main()
