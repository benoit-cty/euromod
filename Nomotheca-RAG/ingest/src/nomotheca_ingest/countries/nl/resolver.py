"""Dutch citation resolver and freshness canary definitions."""

from __future__ import annotations

from datetime import date

from nomotheca_ingest.countries.nl.fetcher import sru_search_url
from nomotheca_ingest.countries.nl.parser import KNOWN_ACTS
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef


# Reverse alias lookup: BWB id and short citation label -> BWB id.
_ALIASES: dict[str, str] = {}
for _bwb_id, _short in KNOWN_ACTS.items():
    _ALIASES[_bwb_id.upper()] = _bwb_id
    _ALIASES[_short.upper()] = _bwb_id

# Longer forms EUROMOD citations use for the same acts.
_ALIASES.update(
    {
        "WET INKOMSTENBELASTING 2001": "BWBR0011353",
        "WET OP DE LOONBELASTING 1964": "BWBR0002471",
        "ALGEMENE WET INKOMENSAFHANKELIJKE REGELINGEN": "BWBR0018472",
        "WET OP HET KINDGEBONDEN BUDGET": "BWBR0022751",
        "ALGEMENE KINDERBIJSLAGWET": "BWBR0002368",
        "ALGEMENE OUDERDOMSWET": "BWBR0002221",
        "WET KINDEROPVANG": "BWBR0017017",
        "WERKLOOSHEIDSWET": "BWBR0004045",
        "WET FINANCIERING SOCIALE VERZEKERINGEN": "BWBR0017745",
        "ALGEMENE NABESTAANDENWET": "BWBR0007795",
        "WET ARBEID EN ZORG": "BWBR0013008",
    }
)

_MAX_ALIAS_WORDS = max(len(alias.split()) for alias in _ALIASES)


class NlResolver:
    """Resolve NL citations against the known-act alias table.

    Returns the act's version index (``manifest.xml``); ingesting it loads the
    toestanden in force at the EUROMOD policy dates, including the one covering
    ``as_of`` -- point-in-time selection then happens in SQL.
    """

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a Dutch citation at a date to a fetchable BWB reference."""
        bwb_id = _match_alias(ref.citation)
        if bwb_id is None:
            # SRU is the discovery layer; point whoever hit this at the query
            # that answers it rather than at a bare list of known aliases.
            lookup = sru_search_url(f'overheidbwb.titel="{ref.citation}"')
            msg = (
                f"Unknown NL act in citation {ref.citation!r}. Resolve its BWB id with "
                f"{lookup} (match dcterms:title exactly -- overheidbwb.titel ranks "
                f"amending acts first), then add it to KNOWN_ACTS. "
                f"Known aliases: {sorted(_ALIASES)}"
            )
            raise ValueError(msg)
        return [
            SourceRef(
                jurisdiction=ref.jurisdiction,
                source_code="NL-BWB",
                source_id=bwb_id,
                source_type="version_index",
                metadata={"as_of": as_of.isoformat(), "citation": ref.citation},
            )
        ]


def _match_alias(citation: str) -> str | None:
    """Find the longest known act alias occurring in a citation."""
    words = citation.upper().replace(",", " ").split()
    for size in range(min(_MAX_ALIAS_WORDS, len(words)), 0, -1):
        for start in range(len(words) - size + 1):
            bwb_id = _ALIASES.get(" ".join(words[start : start + size]))
            if bwb_id:
                return bwb_id
    return None


def canary_facts() -> list[CanaryFact]:
    """Return known Dutch legal facts used to detect stale sources."""
    return [
        CanaryFact(
            citation="Wet IB 2001, artikel 2.10",
            assert_latest_start_gte=date(2025, 1, 1),
            reason=(
                "Art. 2.10's 2025 version splits box 1 into three bands "
                "(thresholds EUR 38.441 and EUR 76.817, rates 8,17% / 37,48% / 49,50%); "
                "an older latest version means a stale source. Note the statute's 8,17% "
                "is the tax component only -- CR Y16 2.2.3 quotes 35,82% including "
                "premies volksverzekeringen."
            ),
        ),
        CanaryFact(
            citation="AOW",
            assert_latest_start_gte=date(2025, 1, 1),
            reason=(
                "The state pension age reached 67 in 2024 (CR Y16 2.2.2); the AOW must "
                "carry a 2025 or later consolidation for the 2025 system year."
            ),
        ),
    ]
