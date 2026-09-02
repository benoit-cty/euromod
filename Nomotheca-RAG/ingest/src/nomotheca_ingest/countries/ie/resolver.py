"""Irish citation resolver and freshness canary definitions."""

from __future__ import annotations

import re
from datetime import date

from nomotheca_ingest.countries.ie.fetcher import (
    ACT_INDEX_PREFIX,
    SOURCE_CODE_EISB,
    SOURCE_CODE_OIREACHTAS,
)
from nomotheca_ingest.countries.ie.parser import BASELINE_ACTS
from nomotheca_ingest.core.ir import CanaryFact, CitationRef, SourceRef


# Curated aliases for the principal acts EUROMOD IE cites by name. Everything
# else resolves through the Oireachtas act index for a year.
_ALIASES: dict[str, str] = {
    "TCA": "1997/act/39",
    "TCA 1997": "1997/act/39",
    "TAXES CONSOLIDATION ACT": "1997/act/39",
    "TAXES CONSOLIDATION ACT 1997": "1997/act/39",
    "SWCA": "2005/act/26",
    "SWCA 2005": "2005/act/26",
    "SOCIAL WELFARE CONSOLIDATION ACT": "2005/act/26",
    "SOCIAL WELFARE CONSOLIDATION ACT 2005": "2005/act/26",
}

_ACT_ID_RE = re.compile(r"^\d{4}/act/\d+$")
_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


class IeResolver:
    """Resolve IE citations to fetchable act ids or to a year's act index.

    Ireland has no consolidated code to point at, so a citation resolves to the
    *acts that state the value*: the annual Finance and Social Welfare Acts.
    Ingesting a year's index fans out to each of them; point-in-time selection
    then happens in SQL against the effective dates their own sections state.
    """

    def resolve(self, ref: CitationRef, as_of: date) -> list[SourceRef]:
        """Resolve an Irish citation at a date to fetchable references."""
        citation = ref.citation.strip()
        if _ACT_ID_RE.match(citation):
            return [self._act_ref(ref.jurisdiction, citation, citation)]

        act_id = _ALIASES.get(_normalize(citation))
        if act_id:
            return [self._act_ref(ref.jurisdiction, act_id, BASELINE_ACTS.get(act_id, citation))]

        return [self._index_ref(ref.jurisdiction, year, citation) for year in _years_for(citation, as_of)]

    def _act_ref(self, jurisdiction: str, act_id: str, short_title: str) -> SourceRef:
        """Build a reference to one act's as-enacted text on eISB."""
        return SourceRef(
            jurisdiction=jurisdiction,
            source_code=SOURCE_CODE_EISB,
            source_id=act_id,
            source_type="act",
            metadata={"short_title": short_title},
        )

    def _index_ref(self, jurisdiction: str, year: int, citation: str) -> SourceRef:
        """Build a reference to one act year's Oireachtas index."""
        return SourceRef(
            jurisdiction=jurisdiction,
            source_code=SOURCE_CODE_OIREACHTAS,
            source_id=f"{ACT_INDEX_PREFIX}{year}",
            source_type="act_index",
            metadata={"citation": citation},
        )


def _years_for(citation: str, as_of: date) -> list[int]:
    """Return the act years to search for a citation at a point in time.

    Ireland's budget cycle puts a system year's parameters in the *previous*
    calendar year's act: Finance Act 2024 (signed 2024-11-12) is what states
    "as respects the year of assessment 2025". So a request for a year always
    covers that year and the one before it — the same year-ahead reasoning as
    the FR income_year basis, in the opposite direction.
    """
    match = _YEAR_RE.search(citation)
    year = int(match.group(0)) if match else as_of.year
    return [year - 1, year]


def _normalize(citation: str) -> str:
    """Normalize a citation for alias lookup."""
    return re.sub(r"[\s,]+", " ", citation).strip().rstrip(".").upper()


def canary_facts() -> list[CanaryFact]:
    """Return known Irish legal facts used to detect a stale corpus.

    Each fact is a verbatim substitution made by that year's budget act, in its
    section 2 (USC) — cross-checked against IE_Y16 §2.2 "Main policy changes".
    A corpus answering a system-year question with the previous year's ceiling
    is missing the budget act, which is the only failure mode that matters here.
    """
    return [
        CanaryFact(
            citation="Finance Act 2022, s. 2",
            assert_latest_start_gte=date(2023, 1, 1),
            reason=(
                "Budget 2023 raised the USC 2% ceiling to €22,920 (Finance Act 2022 s. 2(1)(a), "
                "applying for the year of assessment 2023)."
            ),
        ),
        CanaryFact(
            citation="Finance (No. 2) Act 2023, s. 2",
            assert_latest_start_gte=date(2024, 1, 1),
            reason=(
                "Budget 2024 raised the USC 2% ceiling to €25,760 and cut the third rate to 4% "
                "(Finance (No. 2) Act 2023 s. 2). Note the act is 'No. 2': a plain Finance Act 2023 "
                "also exists and is not the budget act."
            ),
        ),
        CanaryFact(
            citation="Finance Act 2024, s. 3",
            assert_latest_start_gte=date(2025, 1, 1),
            reason=(
                "Budget 2025 raised the single standard rate band to €44,000 and the personal, "
                "employee and earned-income credits to €2,000 (Finance Act 2024 s. 3, as respects "
                "the year of assessment 2025); s. 2 raised the USC 2% ceiling to €27,382 and cut "
                "the middle rate to 3.5%. A corpus still answering €42,000 is missing FA 2024."
            ),
        ),
    ]
