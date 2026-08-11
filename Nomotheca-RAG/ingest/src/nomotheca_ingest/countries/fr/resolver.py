"""French citation resolver interface and freshness canary definitions."""

from __future__ import annotations

from datetime import date

from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef


class FrResolver:
    """Placeholder resolver for French citations until Moulineuse wiring lands."""

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve a French citation at a date to exact source references."""
        raise NotImplementedError("FR citation resolution needs Moulineuse SQL or MCP wiring.")


def canary_facts() -> list[CanaryFact]:
    """Return known French legal facts used to detect stale resolvers."""
    return [
        CanaryFact(
            citation="CGI art. 197",
            assert_latest_start_gte=date(2025, 2, 16),
            reason="LF2025 rewrote the income-tax brackets; older resolvers are stale.",
        )
    ]
