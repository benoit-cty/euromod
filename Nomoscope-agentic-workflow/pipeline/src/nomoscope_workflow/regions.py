"""Region key of a regional EUROMOD parameter, read off its name (ADR 0003).

Some EUROMOD parameters belong to a sub-national jurisdiction: Spain's
``$bsarg_rg24_basic_amt`` (Aragón's minimum income), ``$bchrg_reg24_lim1``,
``$tin_depallrg30_amt1`` (Madrid's regional IRPF allowance). EUROMOD encodes
the region as the two digits of its NUTS-2 code after an ``rg``/``reg`` token.
That key selects the child jurisdiction whose law may support the parameter:
retrieval runs over ``[country, child]`` and can never reach a sibling
region's act — the false positive the verbatim-extract check cannot catch,
because a quote from the wrong region's decree is still a real quote.

The NUTS-2 -> jurisdiction-code mapping itself lives in the database
(``jurisdictions.metadata->>'nuts2'``, seeded from
``Nomotheca-RAG/ingest/.../countries/es/regions.py``); this module only knows
how to read the key out of a parameter name, and refuses digits that are not
a region of that country so ``…rate10_`` can never be mistaken for one.
"""

from __future__ import annotations

import re

# Per country: how the region token looks in a constant name, and which
# two-digit codes are regions. Countries absent here have no regional layer.
_REGION_TOKEN: dict[str, re.Pattern[str]] = {
    "ES": re.compile(r"r(?:eg|g)(\d{2})(?=_|$)"),
}
_REGION_CODES: dict[str, frozenset[str]] = {
    # NUTS-2 2021, the 17 comunidades + Ceuta (63) and Melilla (64).
    "ES": frozenset(
        {"11", "12", "13", "21", "22", "23", "24", "30", "41", "42", "43",
         "51", "52", "53", "61", "62", "63", "64", "70"}
    ),
}


def region_key(country: str, model_target: str) -> str | None:
    """NUTS-2 code (``ES24``) of a regional parameter, or None for a national one."""
    country = country.upper()
    pattern = _REGION_TOKEN.get(country)
    if pattern is None:
        return None
    name = model_target.rsplit("/", 1)[-1]
    for match in pattern.finditer(name):
        if match.group(1) in _REGION_CODES[country]:
            return f"{country}{match.group(1)}"
    return None
