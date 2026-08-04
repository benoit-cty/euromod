"""Lithuanian citation resolver and freshness canary definitions."""

from __future__ import annotations

from datetime import date

from nomotheca_ingest.countries.lt.fetcher import CONSOLIDATION_INDEX_SUFFIX
from nomotheca_ingest.countries.lt.parser import KNOWN_ACTS
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef


# Reverse alias lookup: official number and short label -> dokumento_id.
_ALIASES: dict[str, str] = {}
for _dokumento_id, (_nr, _short) in KNOWN_ACTS.items():
    _ALIASES[_nr.upper()] = _dokumento_id
    _ALIASES[_short.upper()] = _dokumento_id


class LtResolver:
    """Resolve LT citations against the known-act alias table.

    Returns the act's consolidation index; ingesting it loads every dated
    consolidation overlapping the EUROMOD window, including the one in force
    at ``as_of`` — point-in-time selection then happens in SQL.
    """

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Lithuanian citation at a date to fetchable TAR references."""
        tokens = ref.citation.upper().replace(",", " ").split()
        for token in tokens:
            dokumento_id = _ALIASES.get(token)
            if dokumento_id:
                return [
                    SourceRef(
                        jurisdiction=ref.jurisdiction,
                        source_code="LT-TAR",
                        source_id=f"{dokumento_id}{CONSOLIDATION_INDEX_SUFFIX}",
                        source_type="consolidation_index",
                        metadata={"as_of": as_of.isoformat(), "citation": ref.citation},
                    )
                ]
        msg = f"Unknown LT act in citation {ref.citation!r}; known aliases: {sorted(_ALIASES)}"
        raise ValueError(msg)


def canary_facts() -> list[CanaryFact]:
    """Return known Lithuanian legal facts used to detect stale sources."""
    return [
        CanaryFact(
            citation="GPMĮ 20 straipsnis",
            assert_latest_start_gte=date(2025, 1, 2),
            reason=(
                "The GPMĮ's latest consolidation starts 2025-01-02 (2025 NPD step: "
                "747 EUR below MMA 1038 EUR); an older latest version means a stale source."
            ),
        )
    ]
