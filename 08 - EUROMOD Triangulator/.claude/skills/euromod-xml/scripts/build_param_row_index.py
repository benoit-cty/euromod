"""
build_param_row_index.py
========================
Build a row-number lookup dict from a EUROMOD system XML element.

The EUROMOD UI displays row numbers as pol_n.func_n.par_n — 1-based positional
ranks after sorting all siblings by their <Order> integer.

Usage
-----
    from lxml import etree
    from build_param_row_index import build_param_row_index

    NS = "{http://euromod.com/CountryConfig.xsd}"
    tree = etree.parse("SI.xml")

    # Get the most-recent-year system element
    systems = sorted(
        tree.iter(f"{NS}System"),
        key=lambda s: int(s.findtext(f"{NS}Year") or 0)
    )
    sys_el = systems[-1]

    idx = build_param_row_index(sys_el, NS)
    # idx[(pol_name, func_name, par_name, group)] -> 'pol_n.func_n.par_n'
"""

from lxml import etree


def _iord(el, ns):
    o = el.find(f"{ns}Order")
    try:    return int(o.text)
    except: return 0


def build_param_row_index(sys_el, NS):
    """Return dict: (pol_name, func_name, par_name, group) → 'pol_n.func_n.par_n'"""
    idx = {}
    for pol_n, pol_el in enumerate(sorted(sys_el.findall(f"{NS}Policy"), key=lambda e: _iord(e, NS)), 1):
        pname = (pol_el.find(f"{NS}Name") or type('',(),{'text':''})()).text or ""
        for fun_n, fun_el in enumerate(sorted(pol_el.findall(f"{NS}Function"), key=lambda e: _iord(e, NS)), 1):
            fname = (fun_el.find(f"{NS}Name") or type('',(),{'text':''})()).text or ""
            param_n = 0
            for par_el in sorted(fun_el.findall(f"{NS}Parameter"), key=lambda e: _iord(e, NS)):
                parn = (par_el.find(f"{NS}Name") or type('',(),{'text':''})()).text or ""
                grp  = (par_el.find(f"{NS}Group") or type('',(),{'text':''})()).text or ""
                if not parn:
                    continue
                param_n += 1
                key = (pname, fname, parn, grp)
                if key not in idx:   # first occurrence wins
                    idx[key] = f"{pol_n}.{fun_n}.{param_n}"
    return idx
