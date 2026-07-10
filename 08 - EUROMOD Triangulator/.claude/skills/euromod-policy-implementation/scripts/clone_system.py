"""
clone_system.py
===============
Create a copy of a EUROMOD system with a new name across one or more countries,
keeping everything else intact (all policies, functions, parameters, extension
records).  All internal GUIDs are replaced with fresh ones.

System names follow the pattern  CC_YYYY[_suffix]  (e.g. ES_2025, ES_2026_TE).
The script automatically sets the <Year> element of each cloned system to the
four-digit year embedded in the new system name, so the year is always
consistent with the name regardless of whether you are copying within a year
or across years.

Systems can be specified three ways (CLI overrides JSON config, JSON config
overrides the SETTINGS block):
  a) Via explicit system names per country using SOURCE_SUFFIX / NEW_SUFFIX
     and a COUNTRIES list (the CC_ prefix is added automatically), OR
    b) Via a JSON config file passed with --config, OR
    c) Directly via --source-suffix / --new-suffix on the command line.

Usage
-----
python clone_system.py --config clone_system.config.json

python clone_system.py [--euromod-path <path>] [--source-suffix <SUFFIX>]
                       [--new-suffix <SUFFIX>] [--countries "AT BE"]
                       [--no-backup] [--overwrite]

Arguments
---------
  --euromod-path    Root folder of the EUROMOD model (contains XMLParam/).
  --source-suffix   Suffix of the system to copy (e.g. 2025 or 2025_TE_OTH).
  --new-suffix      Suffix for the new system    (e.g. 2026 or 2026_TE_OTH).
  --countries       Space-separated country codes (e.g. "AT BE DE").
  --no-backup       Skip creating .bak copies of the XML files.
  --overwrite       Delete and replace an existing target system instead of aborting.

Note: source and new suffix are allowed to have *different* years (e.g. cloning
2025 → 2026).  The <Year> element in the clone is always set to the year found
in NEW_SUFFIX, not the year of the source system.
"""

import argparse
import copy
import io
import json
import re
import shutil
import sys
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

# lxml is ~10-100× faster than stdlib ET for large files.
try:
    from lxml import etree as lET
    _HAVE_LXML = True
except ImportError:
    lET = None  # type: ignore
    _HAVE_LXML = False

# Unified element factories — always use these so stdlib/lxml elements are
# never mixed in the same tree.
_Element    = (lambda tag: lET.Element(tag))                    if _HAVE_LXML else ET.Element
_SubElement = (lambda parent, tag: lET.SubElement(parent, tag)) if _HAVE_LXML else ET.SubElement

NS_URI = "http://euromod.com/CountryConfig.xsd"
NS     = f"{{{NS_URI}}}"
ET.register_namespace("", NS_URI)   # suppress ns0: prefix in stdlib output


# ══════════════════════════════════════════════════════════════════════════════
# SETTINGS  ←  optional fallbacks for repeated local use.
# Prefer --config or CLI flags so the script stays portable across users.
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_CONFIG_FILE = "clone_system.config.json"

# Full path to the root folder of the EUROMOD model (the folder that contains
# XMLParam/).  Use forward slashes or double back-slashes.
EUROMOD_PATH = None

# Countries to process — space-separated two-letter codes.
# Full EU27 list:  AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK
COUNTRIES = ""

# Suffix of the system to copy (without the leading CC_).
# The full source system name is built as  CC_SOURCE_SUFFIX  for each country.
# Examples: "2025"  "2025_TE_OTH"  "2024_REFORM"
SOURCE_SUFFIX = None

# Suffix for the new (cloned) system.
# The full new system name is built as  CC_NEW_SUFFIX  for each country.
# The <Year> element in the clone is automatically set to the four-digit year
# found at the start of NEW_SUFFIX (e.g. NEW_SUFFIX="2026_TE_OTH" → Year=2026).
# Source and new year are allowed to differ (e.g. cloning 2025 → 2026 is fine).
# Examples: "2026"  "2026_TE_OTH"  "2025_REFORM"
NEW_SUFFIX = None

# Set to True to skip making a safety backup of the XML before writing.
SKIP_BACKUP = False

# What to do if a system with the new name already exists in the XML:
#   False  →  abort with an error message (safe default)
#   True   →  delete the existing system and replace it with the fresh clone
OVERWRITE_IF_EXISTS = False

# ══════════════════════════════════════════════════════════════════════════════


# ── helpers ───────────────────────────────────────────────────────────────────

# System suffixes must start with a 4-digit year: YYYY[_anything]
_SUFFIX_RE = re.compile(r'^\d{4}', re.IGNORECASE)


def _validate_suffix(suffix: str, role: str) -> None:
    """Abort if *suffix* does not start with a 4-digit year."""
    if not _SUFFIX_RE.match(suffix):
        sys.exit(
            f"ERROR: {role} '{suffix}' does not start with a 4-digit year. "
            f"Expected format: YYYY[_suffix]  (e.g. 2025  or  2025_TE_FAM)."
        )


def _year_from_suffix(suffix: str) -> str:
    """Extract the 4-digit year from the start of *suffix* (e.g. '2026_TE' → '2026')."""
    return suffix[:4]


def set_system_year(sys_el, year: str) -> bool:
    """Set the <Year> child of *sys_el* to *year*.  Creates the element if absent.
    Returns True if the value was changed (or created), False if already correct."""
    year_el = sys_el.find(f"{NS}Year")
    if year_el is None:
        # <Year> not present — create it after <Name>
        name_el = sys_el.find(f"{NS}Name")
        insert_pos = list(sys_el).index(name_el) + 1 if name_el is not None else 0
        year_el = _Element(f"{NS}Year")
        sys_el.insert(insert_pos, year_el)
    if year_el.text == year:
        return False
    year_el.text = year
    return True


def update_defoutput_filenames(clone, source_name: str, new_name: str) -> int:
    """In *clone*, update output filenames that embed the source system name.

    Two cases are handled:

    1. ``file`` parameters inside ``DefOutput`` functions — value follows
       ``{source_name}_{tail}`` or equals ``{source_name}`` exactly.

    2. ``Param_NewVal`` parameters inside ``ChangeParam`` functions whose
       ``Param_Id`` references the UUID of a ``file`` parameter in a
       ``DefOutput`` function — same rename logic applies to the new value.

    Matching is case-insensitive; the tail's original casing is preserved.
    Returns the total number of values updated.
    """
    n = 0
    src_lower    = source_name.lower()
    prefix_lower = src_lower + "_"

    def _rename(val: str) -> str | None:
        """Return the renamed value, or None if no match."""
        val_low = val.lower()
        if val_low.startswith(prefix_lower):
            return new_name + "_" + val[len(prefix_lower):]
        if val_low == src_lower:
            return new_name
        return None

    # Pass 1 — update 'file' params in DefOutput; collect their UUIDs.
    defout_file_ids: set = set()
    for fn in clone.iter(f"{NS}Function"):
        fn_name_el = fn.find(f"{NS}Name")
        if fn_name_el is None or fn_name_el.text != "DefOutput":
            continue
        for param in fn.iter(f"{NS}Parameter"):
            pe  = param.find(f"{NS}Name")
            ve  = param.find(f"{NS}Value")
            pid = param.find(f"{NS}ID")
            if pe is None or ve is None or pe.text != "file" or not ve.text:
                continue
            if pid is not None and pid.text:
                defout_file_ids.add(pid.text)
            new_val = _rename(ve.text)
            if new_val is not None:
                ve.text = new_val
                n += 1

    # Pass 2 — update Param_NewVal in ChangeParam functions that reference
    # one of the collected DefOutput file parameter UUIDs.
    for fn in clone.iter(f"{NS}Function"):
        fn_name_el = fn.find(f"{NS}Name")
        if fn_name_el is None or fn_name_el.text != "ChangeParam":
            continue
        # Gather Param_Id and Param_NewVal from this function's parameters.
        param_id_val: str | None = None
        newval_el               = None
        for param in fn.iter(f"{NS}Parameter"):
            pe = param.find(f"{NS}Name")
            ve = param.find(f"{NS}Value")
            if pe is None or ve is None:
                continue
            if pe.text == "Param_Id":
                param_id_val = ve.text
            elif pe.text.lower() == "param_newval":   # case-safe: Param_NewVal
                newval_el = ve
        if param_id_val in defout_file_ids and newval_el is not None and newval_el.text:
            new_val = _rename(newval_el.text)
            if new_val is not None:
                newval_el.text = new_val
                n += 1

    return n


def update_hhot_params(clone, source_name: str, new_name: str) -> int:
    """Rename any parameter <Value> of the form ``{source_name}_hhot`` to
    ``{new_name}_hhot`` throughout the entire clone.  Matching is
    case-insensitive; the stored casing of the suffix is preserved.
    Returns the number of values updated.
    """
    n = 0
    pattern = source_name.lower() + "_hhot"
    for param in clone.iter(f"{NS}Parameter"):
        ve = param.find(f"{NS}Value")
        if ve is None or not ve.text:
            continue
        if ve.text.lower() == pattern:
            # Preserve the '_hhot' suffix as-is from the original value
            suffix = ve.text[len(source_name):]   # e.g. '_hhot'
            ve.text = new_name + suffix
            n += 1
    return n


def _tx(el, tag: str) -> str:
    """Return the text of a direct child element, or '' if absent."""
    c = el.find(f"{NS}{tag}")
    return c.text.strip() if c is not None and c.text else ""


def _new_id() -> str:
    return str(uuid.uuid4())


def _update_backrefs(el, id_map: dict) -> None:
    """Replace known UUID back-references if present in id_map.

    Handles element-tag references (SystemID, PolicyID, FunctionID,
    ReferencePolID) and bare-UUID <Value> fields (e.g. ChangeParam/Param_Id).
    """
    for ref_tag in ("SystemID", "PolicyID", "FunctionID", "ReferencePolID"):
        ref_el = el.find(f"{NS}{ref_tag}")
        if ref_el is not None and ref_el.text and ref_el.text in id_map:
            ref_el.text = id_map[ref_el.text]
    # Some parameters store a UUID directly as <Value> (e.g. ChangeParam Param_Id).
    val_el = el.find(f"{NS}Value")
    if val_el is not None and val_el.text and val_el.text.strip() in id_map:
        val_el.text = id_map[val_el.text.strip()]


def _set_order(sys_el, order_val: int) -> None:
    """Set (or create) the <Order> child of a System element."""
    order_el = sys_el.find(f"{NS}Order")
    if order_el is not None:
        order_el.text = str(order_val)
    else:
        new_el = _SubElement(sys_el, f"{NS}Order")
        new_el.text = str(order_val)


def _find_system(root, name: str):
    """Return the first <System> element whose <Name> matches *name*, or None."""
    # Systems may sit directly under root or inside a <Country> wrapper.
    for sys_el in root.iter(f"{NS}System"):
        if _tx(sys_el, "Name") == name:
            return sys_el
    return None


def _find_system_parent(root, sys_el):
    """Return the parent element of *sys_el* within the tree rooted at *root*."""
    for parent in root.iter():
        if sys_el in list(parent):
            return parent
    return root


def _delete_system(root, sys_el) -> None:
    """Remove *sys_el* from the tree, together with all associated
    Extension_Policy, Extension_Function and ConditionalFormat records."""
    # Collect policy and function IDs belonging to this system
    pol_ids:  set = set()
    func_ids: set = set()
    for pol in sys_el.findall(f"{NS}Policy"):
        pid = _tx(pol, "ID")
        if pid:
            pol_ids.add(pid)
        for func in pol.findall(f"{NS}Function"):
            fid = _tx(func, "ID")
            if fid:
                func_ids.add(fid)

    sys_name = _tx(sys_el, "Name")

    # Remove the system element itself
    parent = _find_system_parent(root, sys_el)
    parent.remove(sys_el)

    # Remove associated root-level records
    for child in list(root):
        tag = child.tag.split("}")[-1]
        if tag == "Extension_Policy" and _tx(child, "PolicyID") in pol_ids:
            root.remove(child)
        elif tag == "Extension_Function" and _tx(child, "FunctionID") in func_ids:
            root.remove(child)
        elif tag == "ConditionalFormat":
            cfs = child.find(f"{NS}ConditionalFormat_Systems")
            if cfs is not None:
                sn = cfs.find(f"{NS}SystemName")
                if sn is not None and sn.text == sys_name:
                    root.remove(child)


# ── core clone logic ──────────────────────────────────────────────────────────

def clone_system(src_sys, new_name: str):
    """Deep-copy *src_sys*, rename it, and replace ALL internal GUIDs.

    Returns (clone_element, id_map) where id_map maps each old policy/function
    UUID to its new UUID — needed to replicate Extension records.
    """
    # Serialize + re-parse is far faster than copy.deepcopy for large trees.
    if _HAVE_LXML:
        clone = lET.fromstring(lET.tostring(src_sys))
    else:
        clone = ET.fromstring(ET.tostring(src_sys))

    id_map: dict = {}       # old_uuid → new_uuid  (policies + functions)
    full_ref_map: dict = {} # includes system ID for back-reference updates

    # System ID
    sys_id_el = clone.find(f"{NS}ID")
    old_sys_id = sys_id_el.text if sys_id_el is not None else None
    new_sys_id = _new_id()
    if sys_id_el is not None:
        sys_id_el.text = new_sys_id
    clone.find(f"{NS}Name").text = new_name

    if old_sys_id:
        full_ref_map[old_sys_id] = new_sys_id

    # Pass 1 — assign fresh IDs to policies, functions, parameters
    for pol in clone.findall(f"{NS}Policy"):
        old_pol_id = _tx(pol, "ID")
        new_pol_id = _new_id()
        if old_pol_id:
            id_map[old_pol_id]       = new_pol_id
            full_ref_map[old_pol_id] = new_pol_id
        pol_id_el = pol.find(f"{NS}ID")
        if pol_id_el is not None:
            pol_id_el.text = new_pol_id

        for func in pol.findall(f"{NS}Function"):
            old_func_id = _tx(func, "ID")
            new_func_id = _new_id()
            if old_func_id:
                id_map[old_func_id]       = new_func_id
                full_ref_map[old_func_id] = new_func_id
            func_id_el = func.find(f"{NS}ID")
            if func_id_el is not None:
                func_id_el.text = new_func_id

            for param in func.findall(f"{NS}Parameter"):
                param_id_el = param.find(f"{NS}ID")
                if param_id_el is not None:
                    old_param_id = param_id_el.text
                    new_param_id = _new_id()
                    if old_param_id:
                        full_ref_map[old_param_id] = new_param_id
                    param_id_el.text = new_param_id

    # Pass 2 — fix all back-references (SystemID / PolicyID / FunctionID)
    for pol in clone.findall(f"{NS}Policy"):
        _update_backrefs(pol, full_ref_map)
        for func in pol.findall(f"{NS}Function"):
            _update_backrefs(func, full_ref_map)
            for param in func.findall(f"{NS}Parameter"):
                _update_backrefs(param, full_ref_map)

    return clone, id_map


def replicate_extensions(root, id_map: dict):
    """For every Extension_Policy / Extension_Function whose PolicyID /
    FunctionID maps to a new ID in id_map, append a matching record at root."""
    new_eps, new_efs = [], []
    for child in list(root):
        tag = child.tag.split("}")[-1]
        if tag == "Extension_Policy":
            old_pid = _tx(child, "PolicyID")
            if old_pid in id_map:
                ep = copy.deepcopy(child)
                ep.find(f"{NS}PolicyID").text = id_map[old_pid]
                new_eps.append(ep)
        elif tag == "Extension_Function":
            old_fid = _tx(child, "FunctionID")
            if old_fid in id_map:
                ef = copy.deepcopy(child)
                ef.find(f"{NS}FunctionID").text = id_map[old_fid]
                new_efs.append(ef)
    for ep in new_eps:
        root.append(ep)
    for ef in new_efs:
        root.append(ef)
    return len(new_eps), len(new_efs)


# ── conditional formatting ───────────────────────────────────────────────────

def set_conditional_format(root, base_name: str, new_name: str) -> None:
    """Add a <ConditionalFormat> record so the new system compares against
    the baseline system (CC_YYYY) in the EUROMOD UI.  The benchmark is always
    the bare CC_YYYY base system, not whichever system was used as clone source.
    Any stale record for *new_name* is removed first (idempotent on re-run)."""
    # Remove stale entry if present
    for cf in list(root.findall(f"{NS}ConditionalFormat")):
        cfs = cf.find(f"{NS}ConditionalFormat_Systems")
        if cfs is not None:
            sn = cfs.find(f"{NS}SystemName")
            if sn is not None and sn.text == new_name:
                root.remove(cf)

    # Find insertion point: just after the last existing ConditionalFormat,
    # or before the first Extension block if none exist yet.
    insert_pos = None
    for i, child in enumerate(root):
        if child.tag == f"{NS}ConditionalFormat":
            insert_pos = i + 1
    if insert_pos is None:
        all_children = list(root)
        insert_pos = next(
            (i for i, c in enumerate(all_children)
             if c.tag.split("}")[-1] in ("Extension_Policy", "Extension_Function",
                                          "Extension_Parameter")),
            len(all_children),
        )

    new_id = str(uuid.uuid4())
    cf = _Element(f"{NS}ConditionalFormat")
    _SubElement(cf, f"{NS}ID").text             = new_id
    _SubElement(cf, f"{NS}BackColor").text      = "FFFFC000"
    _SubElement(cf, f"{NS}ForeColor").text      = "no special color"
    _SubElement(cf, f"{NS}Condition")            # empty / self-closing
    _SubElement(cf, f"{NS}BaseSystemName").text = base_name
    cfs_el = _SubElement(cf, f"{NS}ConditionalFormat_Systems")
    _SubElement(cfs_el, f"{NS}ConditionalFormatID").text = new_id
    _SubElement(cfs_el, f"{NS}SystemName").text          = new_name
    root.insert(insert_pos, cf)


# ── DataConfig update ─────────────────────────────────────────────────────────

def update_dataconfig(dc_xml: Path, source_name: str, new_name: str,
                      new_sys_uuid: str) -> int:
    """In *dc_xml* (CC_DataConfig.xml): for every DataBase that contains a
    DBSystemConfig block for *source_name*, deep-copy that block, replace
    SystemName with *new_name* and all SystemID elements with *new_sys_uuid*,
    and insert it right after the source block.  Removes any stale block for
    *new_name* first so the function is idempotent.  Returns blocks inserted."""
    # Parse from the .bak if available (guarantees a clean pre-run baseline).
    bak_xml   = dc_xml.with_suffix(".xml.bak")
    parse_src = bak_xml if bak_xml.exists() else dc_xml
    dc_raw    = parse_src.read_bytes()
    dc_tree   = ET.parse(parse_src)
    dc_root   = dc_tree.getroot()

    # Auto-detect DataConfig namespace
    dc_ns = ""
    for el in dc_root.iter():
        if "}" in el.tag:
            dc_ns = "{" + el.tag.split("}")[0].lstrip("{") + "}"
            break

    # Step 1 — remove stale blocks for new_name
    for db in dc_root.iter(f"{dc_ns}DataBase"):
        stale = [
            cfg for cfg in db.findall(f"{dc_ns}DBSystemConfig")
            if (cfg.findtext(f"{dc_ns}SystemName") or "").strip() == new_name
        ]
        for cfg in stale:
            db.remove(cfg)

    # Step 2 — clone the source block inside each DataBase
    n_inserted = 0
    for db in dc_root.iter(f"{dc_ns}DataBase"):
        for cfg in list(db.findall(f"{dc_ns}DBSystemConfig")):
            if (cfg.findtext(f"{dc_ns}SystemName") or "").strip() == source_name:
                new_cfg = copy.deepcopy(cfg)
                new_cfg.find(f"{dc_ns}SystemName").text = new_name
                for sid_el in new_cfg.iter(f"{dc_ns}SystemID"):
                    sid_el.text = new_sys_uuid
                new_cfg.tail = cfg.tail
                children = list(db)
                db.insert(children.index(cfg) + 1, new_cfg)
                n_inserted += 1

    if n_inserted == 0:
        return 0

    # Step 3 — serialise, preserving original BOM + CRLF line endings
    if dc_ns:
        ET.register_namespace("", dc_ns[1:-1])
    dc_raw_text = dc_raw.decode("utf-8-sig")
    root_open   = dc_raw_text[: dc_raw_text.index(">") + 1]
    root_tag    = dc_root.tag.split("}")[1] if "}" in dc_root.tag else dc_root.tag
    dc_str      = ET.tostring(dc_root, encoding="unicode", xml_declaration=False)
    dc_inner    = dc_str[dc_str.index(">") + 1 : dc_str.rfind("</")]
    dc_final    = root_open + dc_inner + f"</{root_tag}>"
    dc_crlf     = dc_final.replace("\r\n", "\n").replace("\n", "\r\n")
    bom         = b"\xef\xbb\xbf" if dc_raw[:3] == b"\xef\xbb\xbf" else b""
    dc_xml.write_bytes(bom + dc_crlf.encode("utf-8"))
    return n_inserted


# ── EM3 cache clearing ────────────────────────────────────────────────────────

def clear_em3_cache(euromod_path: str, cc: str) -> None:
    """Delete EM3Translation / Temp cache files so the EUROMOD UI reloads
    fresh XML on next open.  Files that don't exist are silently skipped.
    Any I/O error (missing directory, locked file, etc.) is caught and reported
    as a warning so the script never stalls here."""
    base = Path(euromod_path)
    ccl  = cc.lower()
    targets = [
        base / "EM3Translation" / "XMLParam" / "Countries" / cc / f"up2Date_{ccl}",
        base / "EM3Translation" / "XMLParam" / "Countries" / cc / f"up2Date_{ccl}_DataConfig",
        base / "EM3Translation" / "XMLParam" / "Countries" / cc / f"{ccl}.xml",
        base / "XMLParam" / "Temp" / f"astmp_{cc}.xml",
        base / "XMLParam" / "Temp" / f"astmp_{cc}_DataConfig.xml",
    ]
    for p in targets:
        try:
            p.unlink()
            print(f"  Deleted cache: {p.name}", flush=True)
        except FileNotFoundError:
            pass   # file or parent dir absent — nothing to do
        except Exception as e:
            print(f"  WARN: cache delete failed: {p.name}: {e}", flush=True)


# ── entry point ───────────────────────────────────────────────────────────────

def load_json_config(config_path):
    if not config_path:
        return {}

    path = Path(config_path)
    if not path.exists():
        raise SystemExit(f"ERROR: config file not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: could not parse config JSON {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: config file must contain a top-level JSON object: {path}")
    return data

def main():
    parser = argparse.ArgumentParser(
        description="Clone a EUROMOD system with a new name across one or more countries.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--config", default=None,
                        help=("Path to a JSON config file. If omitted, "
                              "clone_system.config.json in the current working directory "
                              "is used when present."))
    parser.add_argument("--euromod-path", default=None,
                        help="Root folder of the EUROMOD model (contains XMLParam/).")
    parser.add_argument("--source-suffix", default=None,
                        help="System suffix to copy (e.g. 2025_TE_OTH).")
    parser.add_argument("--new-suffix", default=None,
                        help="Suffix for the new system (e.g. 2025_TE_PENS).")
    parser.add_argument("--countries", default=None,
                        help="Space-separated country codes to process (e.g. \"AT BE DE\").")
    parser.add_argument("--no-backup", action="store_true",
                        help="Skip creating .bak copies of the XML files.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Delete and replace an existing system with the same new name "
                             "instead of aborting.")
    args = parser.parse_args()

    config_path = args.config
    if config_path is None and Path(DEFAULT_CONFIG_FILE).exists():
        config_path = DEFAULT_CONFIG_FILE
    config = load_json_config(config_path)

    # CLI arguments override JSON config, which overrides the SETTINGS block.
    euromod_path = args.euromod_path or config.get("euromod_path") or EUROMOD_PATH
    source_suffix = args.source_suffix or config.get("source_suffix") or SOURCE_SUFFIX
    new_suffix = args.new_suffix or config.get("new_suffix") or NEW_SUFFIX
    countries_raw = args.countries if args.countries is not None else config.get("countries", COUNTRIES)
    if isinstance(countries_raw, list):
        countries_str = " ".join(str(c) for c in countries_raw)
    else:
        countries_str = countries_raw or ""
    no_backup = args.no_backup or bool(config.get("skip_backup", SKIP_BACKUP))
    overwrite = args.overwrite or bool(config.get("overwrite_if_exists", OVERWRITE_IF_EXISTS))

    missing = []
    for label, value in (
        ("euromod_path", euromod_path),
        ("source_suffix", source_suffix),
        ("new_suffix", new_suffix),
        ("countries", countries_str),
    ):
        if value in (None, ""):
            missing.append(label)
    if missing:
        joined = ", ".join(missing)
        sys.exit(
            "ERROR: missing required settings: "
            f"{joined}. Provide them via CLI flags, {DEFAULT_CONFIG_FILE}, or the SETTINGS block."
        )

    # Validate suffixes (both must start with YYYY — years are allowed to differ)
    _validate_suffix(source_suffix, "SOURCE_SUFFIX")
    _validate_suffix(new_suffix,    "NEW_SUFFIX")
    new_year = _year_from_suffix(new_suffix)

    countries = [c.strip().upper() for c in countries_str.split() if c.strip()]
    if not countries:
        sys.exit("ERROR: no countries specified.")

    print(f"Countries : {' '.join(countries)}")
    print(f"Source    : CC_{source_suffix}")
    print(f"New       : CC_{new_suffix}  (Year → {new_year})")
    print()

    # Result buckets for the end-of-run report
    res_xml_missing  = []   # XML file not found
    res_src_missing  = []   # source system not found in XML
    res_skipped      = []   # target already exists and overwrite=False
    res_created      = []   # target system newly created
    res_replaced     = []   # target system deleted and recreated

    for cc in countries:
        source      = f"{cc}_{source_suffix}"
        new_name    = f"{cc}_{new_suffix}"
        base_system = source   # source system is the benchmark for ConditionalFormat

        print(f"── {cc} ──────────────────────────────────────", flush=True)

        xml_path = (
            Path(euromod_path)
            / "XMLParam" / "Countries" / cc / f"{cc}.xml"
        )
        if not xml_path.exists():
            print(f"  ERROR: XML file not found: {xml_path} — skipped.", flush=True)
            res_xml_missing.append(cc)
            continue

        # Parse
        print(f"  Parsing {xml_path.name} ...", flush=True)
        if _HAVE_LXML:
            tree = lET.parse(str(xml_path))
        else:
            tree = ET.parse(xml_path)
        root = tree.getroot()

        # Locate source system
        src_sys = _find_system(root, source)
        if src_sys is None:
            print(f"  ERROR: system '{source}' not found — skipped.", flush=True)
            res_src_missing.append(cc)
            continue

        # Check whether the target already exists
        existing    = _find_system(root, new_name)
        was_replace = False
        if existing is not None:
            if not overwrite:
                print(f"  SKIP: '{new_name}' already exists. "
                      f"Set OVERWRITE_IF_EXISTS = True (or --overwrite) to replace it.",
                      flush=True)
                res_skipped.append(cc)
                continue
            print(f"  Overwrite: removing existing '{new_name}' ...", flush=True)
            _delete_system(root, existing)
            was_replace = True

        # Backup
        if not no_backup:
            bak = xml_path.with_suffix(".xml.bak")
            shutil.copy2(str(xml_path), bak)
            print(f"  Backup  -> {bak.name}", flush=True)

        # Clone
        print(f"  Cloning '{source}' -> '{new_name}' ...", flush=True)
        clone, id_map = clone_system(src_sys, new_name)
        clone.tail = src_sys.tail   # preserve whitespace between <System> elements

        # Determine Order for the clone (source order + 1)
        src_order_el = src_sys.find(f"{NS}Order")
        src_order = int(src_order_el.text) if src_order_el is not None and src_order_el.text else 0
        _set_order(clone, src_order + 1)

        # Insert the clone right after the source system
        parent = _find_system_parent(root, src_sys)
        parent_list = list(parent)
        src_idx = next((i for i, c in enumerate(parent_list) if c is src_sys), len(parent_list))
        parent.insert(src_idx + 1, clone)
        print(f"  Inserted '{new_name}' at position {src_idx + 1}.", flush=True)

        # Replicate Extension_Policy / Extension_Function records
        n_ep, n_ef = replicate_extensions(root, id_map)
        print(f"  Extension records replicated: {n_ep} policy, {n_ef} function.", flush=True)

        # Retrieve the new system's UUID (needed for DataConfig)
        new_sys_uuid = clone.find(f"{NS}ID").text

        # Set <Year> in the clone to match the year in new_suffix
        changed = set_system_year(clone, new_year)
        if changed:
            print(f"  Year set to {new_year}.", flush=True)
        else:
            print(f"  Year already {new_year} — no change.", flush=True)

        # Update DefOutput file names: replace source system name prefix with new name
        n_files = update_defoutput_filenames(clone, source, new_name)
        print(f"  DefOutput file names updated: {n_files}.", flush=True)

        # Rename CC_YYYY_hhot parameter values to CC_ZZZZ_hhot when year changes
        n_hhot = update_hhot_params(clone, source, new_name)
        if n_hhot:
            print(f"  HHoT dataset references updated: {n_hhot}.", flush=True)

        # Add ConditionalFormat so the clone compares against the baseline in the UI
        set_conditional_format(root, base_system, new_name)
        print(f"  Conditional format set (benchmark: '{base_system}').", flush=True)

        # Serialise and write the country XML
        print("  Serialising ...", end="", flush=True)
        if _HAVE_LXML:
            xml_bytes = lET.tostring(root, encoding="utf-8", xml_declaration=True)
        else:
            buf = io.BytesIO()
            tree.write(buf, encoding="utf-8", xml_declaration=True)
            xml_bytes = buf.getvalue()
        print(f" {len(xml_bytes) // 1024} KB", flush=True)

        xml_path.write_bytes(xml_bytes)
        print(f"  Written -> {xml_path.name}  ({xml_path.stat().st_size // 1024} KB on disk)",
              flush=True)

        # Update DataConfig
        dc_xml_path = xml_path.with_name(f"{cc}_DataConfig.xml")
        if dc_xml_path.exists():
            if not no_backup:
                shutil.copy2(str(dc_xml_path), dc_xml_path.with_suffix(".xml.bak"))
                print(f"  Backup  -> {dc_xml_path.with_suffix('.xml.bak').name}", flush=True)
            n_dc = update_dataconfig(dc_xml_path, source, new_name, new_sys_uuid)
            print(f"  DataConfig updated: {n_dc} DBSystemConfig block(s) added.", flush=True)
        else:
            print(f"  WARN: DataConfig not found at {dc_xml_path.name} — skipped.", flush=True)

        # Clear EM3 translation cache so EUROMOD UI picks up the changes
        print("  Clearing EM3 cache ...", end="", flush=True)
        clear_em3_cache(euromod_path, cc)
        print(" done.", flush=True)

        if was_replace:
            res_replaced.append(cc)
        else:
            res_created.append(cc)
        print(f"  {cc}: done.", flush=True)

    # ── End-of-run report ────────────────────────────────────────────────────
    def _fmt(lst):
        return " ".join(lst) if lst else "(none)"

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Created  ({len(res_created):>2})  : {_fmt(res_created)}")
    print(f"  Replaced ({len(res_replaced):>2})  : {_fmt(res_replaced)}")
    print(f"  Skipped  ({len(res_skipped):>2})  : {_fmt(res_skipped)}"
          + ("  [target already exists; set OVERWRITE_IF_EXISTS=True to replace]"
             if res_skipped else ""))
    print(f"  No source({len(res_src_missing):>2})  : {_fmt(res_src_missing)}"
          + (f"  ['{source_suffix}' not found in these countries]"
             if res_src_missing else ""))
    print(f"  No XML   ({len(res_xml_missing):>2})  : {_fmt(res_xml_missing)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
