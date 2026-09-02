"""Spanish citation resolver and freshness canary definitions."""

from __future__ import annotations

import re
from datetime import date

from nomotheca_ingest.countries.es.fetcher import SOURCE_CODE
from nomotheca_ingest.countries.es.parser import KNOWN_ACTS
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef


# Citation aliases -> BOE identifier. The API has no usable search endpoint
# (every documented ``query=`` form is rejected with HTTP 400), so resolution
# runs off a curated table, as it does for LT.
_ALIASES: dict[str, str] = {
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
}

# A citation may simply carry the BOE id itself.
BOE_ID_RE = re.compile(r"\bBOE-[A-Z]-\d{4}-\d+\b", re.IGNORECASE)


class EsResolver:
    """Resolve ES citations to BOE consolidated-act identifiers.

    ``as_of`` plays no part: one BOE payload carries every dated version of
    every provision, so point-in-time selection happens in SQL against
    ``legal_unit_versions.validity`` rather than at fetch time.
    """

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
        """Return the BOE id a citation names, by id, alias, or official number."""
        direct = BOE_ID_RE.search(citation)
        if direct:
            return direct.group(0).upper()
        upper = citation.upper()
        for alias, boe_id in _ALIASES.items():
            if re.search(rf"(?<![0-9A-Z/]){re.escape(alias)}(?![0-9A-Z/])", upper):
                return boe_id
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
    ]
