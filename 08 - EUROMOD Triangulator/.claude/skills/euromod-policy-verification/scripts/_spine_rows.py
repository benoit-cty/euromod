"""
_spine_rows.py
==============
Build EUROMOD spine-row index for a given country system and look up
parameter/function row numbers for use in Sections 6 and 7 of the
policy verification report.

Edit the SETTINGS block below, then run:
    python _spine_rows.py

Output: printed spine row numbers ready to paste into generate_report.py.

Spine row format
----------------
  Parameter level  (Section 6) : pol_n.func_n.par_n   e.g. "27.1.8"
  Function level   (Section 7) : pol_n.func_n          e.g. "27.1"
  Policy level     (Section 7) : pol_n                 e.g. "27"

All row numbers are 1-based positional ranks derived by sorting siblings
by their <Order> child element (integer) in ascending order.
"""

from lxml import etree

# ============================================================================
# SETTINGS — edit before running
# ============================================================================

CC_XML = r"PATH\TO\XMLParam\Countries\{CC}\{CC}.xml"   # absolute path to XML
TARGET_SYSTEM = "{CC}_2025"                             # system name in the XML
NS = "{http://euromod.com/CountryConfig.xsd}"

# ============================================================================
# HELPERS
# ============================================================================

def _txt(el, tag):
    """Safe text extraction — always use this; never bare lxml truth-testing."""
    child = el.find(f"{NS}{tag}")
    if child is None:
        return ""
    return (child.text or "").strip()


def _iord(el):
    """Return <Order> as int, 0 if missing/unparseable."""
    o = el.find(f"{NS}Order")
    try:
        return int(o.text)
    except Exception:
        return 0


# ============================================================================
# INDEX BUILDERS
# ============================================================================

def build_param_row_index(sys_el):
    """
    Return dict: (pol_name, func_name, par_name, group) -> 'pol_n.func_n.par_n'

    Use for Section 6 (parametric changes) — parameter-level spine rows.
    Look up each DefConst parameter:
        row_idx[('pol_cc', 'DefConst', '$param_name', '')] -> '27.1.8'
    """
    idx = {}
    for pol_n, pol_el in enumerate(
        sorted(sys_el.findall(f"{NS}Policy"), key=_iord), 1
    ):
        pname = _txt(pol_el, "Name")
        for fun_n, fun_el in enumerate(
            sorted(pol_el.findall(f"{NS}Function"), key=_iord), 1
        ):
            fname = _txt(fun_el, "Name")
            param_n = 0
            for par_el in sorted(fun_el.findall(f"{NS}Parameter"), key=_iord):
                parn = _txt(par_el, "Name")
                grp  = _txt(par_el, "Group")
                if not parn:
                    continue
                param_n += 1
                key = (pname, fname, parn, grp)
                if key not in idx:   # first occurrence wins
                    idx[key] = f"{pol_n}.{fun_n}.{param_n}"
    return idx


def get_func_spine(sys_el):
    """
    Return dict: (pol_name, func_name) -> 'pol_n.func_n'  (first occurrence)

    Use for Section 7 (structural changes) — function-level spine rows.
    Look up the function being created or modified:
        fidx[('pol_cc', 'DefConst')] -> '27.1'
        fidx[('pol_cc', 'BenCalc')]  -> '27.3'
    """
    idx = {}
    for pol_n, pol_el in enumerate(
        sorted(sys_el.findall(f"{NS}Policy"), key=_iord), 1
    ):
        pname = _txt(pol_el, "Name")
        for fun_n, fun_el in enumerate(
            sorted(pol_el.findall(f"{NS}Function"), key=_iord), 1
        ):
            fname = _txt(fun_el, "Name")
            key = (pname, fname)
            if key not in idx:
                idx[key] = f"{pol_n}.{fun_n}"
    return idx


def build_pol_row_index(sys_el):
    """
    Return dict: pol_name -> pol_n

    Use when reporting at policy level (e.g. a new policy has no t-1 counterpart
    so only the policy number is meaningful).
    """
    idx = {}
    for pol_n, pol_el in enumerate(
        sorted(sys_el.findall(f"{NS}Policy"), key=_iord), 1
    ):
        pname = _txt(pol_el, "Name")
        if pname not in idx:
            idx[pname] = pol_n
    return idx


# ============================================================================
# MAIN
# ============================================================================

def main():
    print(f"Parsing {CC_XML} ...")
    tree = etree.parse(CC_XML)

    sys_el = None
    for s in tree.iter(f"{NS}System"):
        name_el = s.find(f"{NS}Name")
        if name_el is not None and name_el.text == TARGET_SYSTEM:
            sys_el = s
            break
    if sys_el is None:
        print(f"ERROR: System '{TARGET_SYSTEM}' not found in {CC_XML}")
        return

    print("Building indices ...")
    pidx   = build_param_row_index(sys_el)   # param-level
    fidx   = get_func_spine(sys_el)          # func-level
    polidx = build_pol_row_index(sys_el)     # pol-level

    print(f"  {len(pidx)} parameter-level entries")
    print(f"  {len(fidx)} function-level entries")
    print(f"  {len(polidx)} policy-level entries\n")

    # ------------------------------------------------------------------
    # SECTION 6 LOOKUPS — parameter level
    # ------------------------------------------------------------------
    # Customise the list below for your country and policy areas.
    # Key format: (pol_name, func_name, par_name, group)
    # group is usually "" for DefConst; check the XML if unsure.
    print("=== SECTION 6: parameter-level spine rows ===")
    s6_lookups = [
        # Examples — replace with your country's actual parameters:
        # ("tin_cc", "DefConst", "$tin_upthres1", ""),
        # ("txc_cc", "DefConst", "$txc_basic_rate", ""),
        # ("bch_cc", "BenCalc", "$bch_amt1", ""),
    ]
    for key in s6_lookups:
        row = pidx.get(key, "NOT FOUND")
        pol, func, par, grp = key
        print(f"  {pol} / {func} / {par} (grp={grp!r})  =>  {row}")

    # ------------------------------------------------------------------
    # SECTION 7 LOOKUPS — function level
    # ------------------------------------------------------------------
    print("\n=== SECTION 7: function-level spine rows ===")
    s7_lookups = [
        # Examples — replace with your country's actual policy/function pairs:
        # ("tin_cc", "DefConst"),
        # ("txc_cc", "ArithOp"),
        # ("bch_cc", "Elig"),
    ]
    for key in s7_lookups:
        row = fidx.get(key, "NOT FOUND")
        pol, func = key
        print(f"  {pol} / {func}  =>  {row}")

    print("\nDone.")


if __name__ == "__main__":
    main()
