"""Deterministic mock proposer/critic — the zero-API-key provider ("mock/...").

Lets the whole loop (retrieval -> proposal -> critique -> diff -> UI) run
against the seed corpus with no LLM credentials: rates/thresholds are pulled
from the retrieved text with regexes tuned to the seed articles. Demo only;
any real evaluation uses a real provider via llm.py.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Callable

from .retrieval import validity_start
from .schema import (
    Bracket,
    CritiqueFindings,
    LegalStatus,
    ParameterRecord,
    ProposalDraft,
    RetrievalHit,
    TemporalBasis,
    income_year_for,
)

# "11 % pour la fraction supérieure à 11 497 €" / "11% for the fraction above EUR 11,497"
_FR_BAND = re.compile(r"(\d+(?:,\d+)?)\s*%\s*pour la fraction supérieure à\s*([\d\s  ]+)€")
_EN_BAND = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*for the fraction above\s*EUR\s*([\d,]+)")
_ANY_RATE = re.compile(r"(\d+(?:[.,]\d+)?)\s*%")

_STATUS_MAP = {
    "in_force": LegalStatus.ENACTED_IN_FORCE,
    "not_yet_in_force": LegalStatus.ENACTED_NOT_YET_IN_FORCE,
}


def _num(text: str) -> float:
    """Parse a number with French/English thousand separators."""
    return float(text.replace(" ", "").replace(" ", "").replace(" ", "").replace(",", "."))


def _num_en(text: str) -> float:
    return float(text.replace(",", ""))


def _pick_hit(hits: list[RetrievalHit]) -> RetrievalHit | None:
    """Only trust citation-path hits (in-force first) — the regex extractor has no
    semantic judgement, so hybrid-only hits would let it read values off the wrong
    article. A real LLM provider sees every hit and reasons about relevance."""
    candidates = [h for h in hits if h.method == "citation"]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda h: (h.version_status != "in_force", -(h.score or 0.0)),
    )[0]


def _band_matches(content: str) -> tuple[list[tuple[float, float]], tuple[int, int] | None]:
    """Extract (threshold, rate) bands and the verbatim span covering them."""
    for pattern, parse in ((_FR_BAND, _num), (_EN_BAND, _num_en)):
        matches = list(pattern.finditer(content))
        if matches:
            bands = [(parse(m.group(2)), _num(m.group(1)) / 100.0) for m in matches]
            return bands, (matches[0].start(), matches[-1].end())
    return [], None


def propose_with_mock(
    record: ParameterRecord,
    as_of: date,
    hits: list[RetrievalHit],
    translation_lookup: Callable[[str], str | None] | None = None,
) -> ProposalDraft:
    """Rule-based stand-in for the proposal LLM call."""
    hit = _pick_hit(hits)
    if hit is None:
        return ProposalDraft(found=False, reasoning="No legal text retrieved.")

    info = record.information
    bands, span = _band_matches(hit.content)
    # income_year parameters are back-dated to the income year start: the
    # version's in-force date is the consolidation date of the finance act,
    # not when the value applies. The income year is not the system year —
    # `income_year_for` owns that mapping.
    valid_from = (
        date(income_year_for(as_of.year), 1, 1)
        if info.temporal_basis == TemporalBasis.INCOME_YEAR
        else validity_start(hit.validity)
    )
    draft = ProposalDraft(
        found=False,
        valid_from=valid_from,
        legal_status=_STATUS_MAP.get(hit.version_status or ""),
        citation_chunk_id=hit.chunk_id,
        reasoning=f"mock extractor over chunk {hit.chunk_id} ({hit.citation})",
    )

    if info.value_type in ("bracket", "bracket_schedule") and bands:
        draft.found = True
        draft.value_brackets = [Bracket(threshold=0, rate=0.0)] + [
            Bracket(threshold=t, rate=r) for t, r in bands
        ]
        draft.confidence = 0.9
    elif info.value_type == "scalar" and info.unit == "/1":
        # Demo heuristic: a scalar rate parameter takes the top schedule rate;
        # bands only, so incidental percentages elsewhere in the article don't win.
        if bands:
            top_threshold, top_rate = max(bands, key=lambda band: band[1])
            draft.found = True
            draft.value_scalar = top_rate
            draft.confidence = 0.75
            for pattern in (_FR_BAND, _EN_BAND):
                match = next(
                    (m for m in pattern.finditer(hit.content) if _num(m.group(1)) / 100.0 == top_rate),
                    None,
                )
                if match:
                    span = (match.start(), match.end())
                    break

    if draft.found and span:
        draft.supporting_extract = hit.content[span[0] : span[1]]
        draft.original_language_quote = draft.supporting_extract
        if hit.lang != "en" and translation_lookup:
            draft.english_translation = translation_lookup(hit.chunk_id)
    if not draft.found:
        draft.reasoning = (
            f"mock extractor found no {info.value_type} value in chunk {hit.chunk_id}"
        )
    return draft


def critique_with_mock(draft: ProposalDraft) -> CritiqueFindings:
    """Mock critique defers entirely to the mechanical checks in pipeline.py."""
    return CritiqueFindings(
        citation_supports_value=draft.found,
        dates_consistent=True,
        values_sane=True,
        issues=[],
    )
