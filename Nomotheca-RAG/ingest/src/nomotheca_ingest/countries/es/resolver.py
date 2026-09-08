"""Spanish citation resolver and freshness canary definitions."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Callable
from datetime import date

from nomotheca_ingest.countries.es.fetcher import SOURCE_CODE
from nomotheca_ingest.countries.es.parser import KNOWN_ACTS
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef


# Citation aliases -> BOE identifier. The API has no usable search endpoint
# (every documented ``query=`` form is rejected — HTTP 400 for state acts,
# HTTP 500 "Code: 109" for regional ones), so resolution runs off a curated
# table, as it does for LT. Keys are matched accent-insensitively on the
# upper-cased citation, so "Aragón" and "Aragon" both hit.
#
# Regional entries are QUALIFIED BY REGION on purpose: Asturias and Aragón both
# have a "Ley 3/2021", Canarias and Cantabria both a "Ley 2/2007"-shaped
# number, and half the communities call their scheme "renta garantizada". A
# bare regional number therefore never resolves — see ``_regional_numbers``.
_ALIASES: dict[str, str] = {
    # --- state acts -------------------------------------------------------
    "LIRPF": "BOE-A-2006-20764",
    "IRPF": "BOE-A-2006-20764",
    "LEY 35/2006": "BOE-A-2006-20764",
    "35/2006": "BOE-A-2006-20764",
    "RIRPF": "BOE-A-2007-6820",
    "RD 439/2007": "BOE-A-2007-6820",
    "439/2007": "BOE-A-2007-6820",
    "LGSS": "BOE-A-2015-11724",
    "RDL 8/2015": "BOE-A-2015-11724",
    "8/2015": "BOE-A-2015-11724",
    "IMV": "BOE-A-2021-21007",
    "LEY 19/2021": "BOE-A-2021-21007",
    "19/2021": "BOE-A-2021-21007",
    "SMI": "BOE-A-2025-2576",
    "RD 87/2025": "BOE-A-2025-2576",
    "87/2025": "BOE-A-2025-2576",
    # --- autonomous communities (consolidated by BOE, verified 2026-09-08) --
    # Galicia
    "DL 1/2011 GALICIA": "BOE-A-2011-18161",
    "DECRETO LEGISLATIVO 1/2011 GALICIA": "BOE-A-2011-18161",
    "TRIBUTOS CEDIDOS GALICIA": "BOE-A-2011-18161",
    "LEY 3/2011 GALICIA": "BOE-A-2011-13120",
    "APOYO A LA FAMILIA GALICIA": "BOE-A-2011-13120",
    # Canarias
    "LEY 5/2022 CANARIAS": "BOE-A-2023-2940",
    "RENTA CANARIA DE CIUDADANIA": "BOE-A-2023-2940",
    "LEY 1/2007 CANARIAS": "BOE-A-2007-4066",
    "PRESTACION CANARIA DE INSERCION": "BOE-A-2007-4066",
    "DL 3/2021 CANARIAS": "BOE-A-2021-9007",
    # Principado de Asturias
    "LEY 3/2021 ASTURIAS": "BOE-A-2021-13685",
    "GARANTIA DE DERECHOS Y PRESTACIONES VITALES": "BOE-A-2021-13685",
    # País Vasco
    "LEY 14/2022 PAIS VASCO": "BOE-A-2023-1405",
    "LEY 14/2022 EUSKADI": "BOE-A-2023-1405",
    "SISTEMA VASCO DE GARANTIA DE INGRESOS": "BOE-A-2023-1405",
    "LEY 18/2008 PAIS VASCO": "BOE-A-2011-15732",
    "LEY 18/2008 EUSKADI": "BOE-A-2011-15732",
    # Navarra
    "LEY FORAL 15/2016": "BOE-A-2016-11671",
    "LEY FORAL 15/2016 NAVARRA": "BOE-A-2016-11671",
    "RENTA GARANTIZADA NAVARRA": "BOE-A-2016-11671",
    # Aragón
    "LEY 3/2021 ARAGON": "BOE-A-2021-10673",
    "PRESTACION ARAGONESA COMPLEMENTARIA": "BOE-A-2021-10673",
    # Comunidad de Madrid
    "LEY 15/2001 MADRID": "BOE-A-2002-4378",
    "RENTA MINIMA DE INSERCION MADRID": "BOE-A-2002-4378",
    # Cataluña
    "LEY 14/2017 CATALUNA": "BOE-A-2017-9799",
    "LLEI 14/2017": "BOE-A-2017-9799",
    "RENDA GARANTIDA DE CIUTADANIA": "BOE-A-2017-9799",
    # Illes Balears
    "LEY 4/2023 ILLES BALEARS": "BOE-A-2023-13761",
    "LEY 4/2023 BALEARES": "BOE-A-2023-13761",
    "DL 10/2020 ILLES BALEARS": "BOE-A-2020-8013",
    "DL 10/2020 BALEARES": "BOE-A-2020-8013",
    "LEY 5/2016 ILLES BALEARS": "BOE-A-2016-4178",
    "LEY 5/2016 BALEARES": "BOE-A-2016-4178",
    "RENTA SOCIAL GARANTIZADA": "BOE-A-2016-4178",
    # Cantabria
    "LEY 2/2007 CANTABRIA": "BOE-A-2007-8186",
    "LEY DE CANTABRIA 2/2007": "BOE-A-2007-8186",
    # Extremadura, La Rioja, Murcia — framework laws, consolidated, not yet
    # ingested (no bsarg/bchrg parameter names these regions).
    "LEY 5/2019 EXTREMADURA": "BOE-A-2019-3491",
    "RENTA EXTREMENA GARANTIZADA": "BOE-A-2019-3491",
    "LEY 4/2017 LA RIOJA": "BOE-A-2017-5627",
    "LEY 3/2007 MURCIA": "BOE-A-2008-12493",
    "RENTA BASICA DE INSERCION MURCIA": "BOE-A-2008-12493",
}

# A citation may simply carry the BOE id itself.
BOE_ID_RE = re.compile(r"\bBOE-[A-Z]-\d{4}-\d+\b", re.IGNORECASE)

# …or a BOE ELI path, state (``es``) or regional (``es-cn``):
# ``https://www.boe.es/eli/es-cn/l/2022/12/19/5/con``. BOE's ELI pages are the
# one working programmatic lookup left — the open-data search is dead — and
# the ``/con`` form resolves only when BOE consolidates the act.
ELI_PATH_RE = re.compile(
    r"eli/(es(?:-[a-z]{2})?/[a-z]+/\d{4}/\d{2}/\d{2}/\d+)(?:/con)?\b", re.IGNORECASE
)
_ELI_TITLE_RE = re.compile(rb"<title>\s*(BOE-A-\d{4}-\d+)")
_OFFICIAL_NUMBER_RE = re.compile(r"\b(\d{1,3}/\d{4})\b")

EliLookup = Callable[[str], bytes | None]


def _fold(value: str) -> str:
    """Upper-case and strip accents: 'Aragón' and 'ARAGON' are one key."""
    decomposed = unicodedata.normalize("NFKD", value.upper())
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def _regional_numbers() -> dict[str, list[str]]:
    """Official numbers that appear only in region-qualified aliases."""
    numbers: dict[str, list[str]] = {}
    for alias in _ALIASES:
        match = _OFFICIAL_NUMBER_RE.search(alias)
        if match and alias != match.group(1) and match.group(1) not in _ALIASES:
            numbers.setdefault(match.group(1), []).append(alias)
    return numbers


_REGIONAL_NUMBERS = _regional_numbers()


def _http_get(url: str) -> bytes | None:
    import httpx

    try:
        response = httpx.get(url, timeout=20.0, follow_redirects=True)
    except Exception:
        return None
    return response.content if response.status_code == 200 else None


def boe_id_from_eli(path: str, lookup: EliLookup = _http_get) -> tuple[str | None, bool]:
    """Resolve a BOE ELI path to its BOE id by reading the ELI page's title.

    Returns ``(boe_id, consolidated)``. BOE answers an unknown ELI with an
    HTTP 200 "Error 404" page, so presence of the id in ``<title>`` is the
    signal, not the status. The ``/con`` form is tried first; when only the
    plain form resolves the act is *published but not consolidated* — the
    consolidated API will 404 on that id, and the caller says so instead of
    letting the fetcher fail with a bare status.
    """
    for suffix, consolidated in (("/con", True), ("", False)):
        body = lookup(f"https://www.boe.es/eli/{path}{suffix}")
        match = _ELI_TITLE_RE.search(body or b"")
        if match:
            return match.group(1).decode(), consolidated
    return None, False


class EsResolver:
    """Resolve ES citations to BOE consolidated-act identifiers.

    ``as_of`` plays no part: one BOE payload carries every dated version of
    every provision, so point-in-time selection happens in SQL against
    ``legal_unit_versions.validity`` rather than at fetch time.
    """

    def __init__(self, eli_lookup: EliLookup = _http_get) -> None:
        """Create the resolver; ``eli_lookup`` fetches ELI pages (injectable for tests)."""
        self._eli_lookup = eli_lookup

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Spanish citation to a fetchable BOE reference."""
        boe_id = self._boe_id(ref.citation)
        if boe_id is None:
            msg = f"Unknown ES act in citation {ref.citation!r}; known aliases: {sorted(_ALIASES)}"
            raise ValueError(msg)
        return [
            SourceRef(
                jurisdiction=ref.jurisdiction,
                source_code=SOURCE_CODE,
                source_id=boe_id,
                source_type="instrument",
                metadata={"as_of": as_of.isoformat(), "citation": ref.citation},
            )
        ]

    def _boe_id(self, citation: str) -> str | None:
        """Return the BOE id a citation names, by id, ELI, alias, or official number."""
        direct = BOE_ID_RE.search(citation)
        if direct:
            return direct.group(0).upper()
        eli = ELI_PATH_RE.search(citation)
        if eli:
            boe_id, consolidated = boe_id_from_eli(eli.group(1).lower(), self._eli_lookup)
            if boe_id and not consolidated:
                msg = (
                    f"{eli.group(1)} is published as {boe_id} but BOE does not consolidate it "
                    "(no /con form), so the legislacion-consolidada API cannot serve it. "
                    "Regional budget laws are the usual case; see .scratch/es-autonomous-"
                    "communities/issues/06-*.md"
                )
                raise ValueError(msg)
            return boe_id
        folded = _fold(citation)
        for alias, boe_id in _ALIASES.items():
            if re.search(rf"(?<![0-9A-Z/]){re.escape(alias)}(?![0-9A-Z/])", folded):
                return boe_id
        for number, aliases in _REGIONAL_NUMBERS.items():
            if re.search(rf"(?<![0-9/]){re.escape(number)}(?![0-9/])", folded):
                msg = (
                    f"Ambiguous ES citation {citation!r}: official number {number} belongs to "
                    f"more than one community's law or to a regional act that must be named with "
                    f"its region. Qualify it — one of {sorted(aliases)}"
                )
                raise ValueError(msg)
        return None


def canary_facts() -> list[CanaryFact]:
    """Return known Spanish legal facts used to detect stale sources."""
    return [
        CanaryFact(
            citation="LIRPF Artículo 66",
            assert_latest_start_gte=date(2024, 12, 22),
            reason=(
                "Ley 7/2024 raised the top savings rate to 30% above 300 000 EUR "
                "for 2025 (CR Y16 §2.2, 2024-2025); art. 66's latest version starts "
                "2024-12-22. An older latest version means a stale source."
            ),
        ),
        CanaryFact(
            citation="LIRPF Artículo 63",
            assert_latest_start_gte=date(2021, 1, 1),
            reason=(
                "The 47% top general bracket (LPGE 2021) is the newest change to the "
                "state general scale and is still in force for 2022-2025."
            ),
        ),
        CanaryFact(
            citation="LGSS Artículo 19",
            assert_latest_start_gte=date(2024, 1, 1),
            reason="Contribution-base rules were last amended with effect 2024-01-01.",
        ),
        CanaryFact(
            # Regional canary. The unit title carries BOE's non-breaking space
            # ("Artículo\u00a013"), as every BOE-derived citation does.
            citation="Ley 14/2022 País Vasco Artículo\u00a013",
            assert_latest_start_gte=date(2025, 12, 30),
            reason=(
                "The Basque Sistema Vasco de Garantía de Ingresos (Ley 14/2022, "
                "BOE-A-2023-1405) was amended by BOE-A-2026-1256 with effect "
                "2025-12-30 (arts. 13 and 25) and BOE-A-2026-1257 with effect "
                "2026-01-01 (art. 64). An older latest version of art. 13 means the "
                "regional source is stale — the same signal the LIRPF canaries give "
                "for state law."
            ),
        ),
    ]
