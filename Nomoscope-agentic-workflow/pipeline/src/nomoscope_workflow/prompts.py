"""Versioned prompts. Prompts are artefacts: bump PROMPT_VERSION on any wording change."""

from __future__ import annotations

import json
from datetime import date

from .schema import ParameterRecord, ProposalDraft, RetrievalHit

PROMPT_VERSION = "0.1.0"

PROPOSAL_SYSTEM = """\
You are a legal analyst updating tax-benefit policy parameters for the EUROMOD microsimulation model.
You are given ONE parameter (its meaning, unit and current value) and a set of retrieved legal text
extracts, each identified by a chunk_id. Determine the value of this parameter in force on the
reference date, using ONLY the provided extracts.

Rules:
- supporting_extract MUST be a verbatim, contiguous quote copied from the chosen extract and must
  contain the value. It is checked character-for-character against the source; paraphrase = rejection.
- citation_chunk_id MUST be the chunk_id of the extract you quoted.
- Normalise units: percentages become decimal fractions when the parameter unit is "/1"
  (11 % -> 0.11); durations in months become decimal years only if the unit says so.
- Bracket schedules: ordered ascending, each band carries its LOWER threshold plus rate (or amount);
  the first band starts at threshold 0; the last band runs to infinity.
- valid_from is the date the value takes effect (from the version validity or the text itself).
- If the extracts do not determine the value, return found=false with a short reasoning. Never guess.
- original_language_quote is the supporting extract in the source language; english_translation is
  your faithful translation of it.
- confidence in [0,1]: 0.9+ only when the extract states the value explicitly and unambiguously.
"""

CRITIQUE_SYSTEM = """\
You are a sceptical reviewer of a proposed policy-parameter update. You get the parameter
definition, the proposal, and the legal extracts it was based on. Check ONLY:
1. citation_supports_value — does the quoted extract actually state the proposed value
   (after unit normalisation, e.g. 11 % -> 0.11 for unit "/1")?
2. dates_consistent — is valid_from compatible with the cited version's validity window
   and the reference date?
3. values_sane — units plausible (rates in [0,1] for unit "/1"), bracket thresholds strictly
   ascending, no obvious magnitude errors versus the current value.
List every problem in issues (empty list if none). Be strict: silent errors here reach a human
reviewer as trusted data.
"""


def _hits_block(hits: list[RetrievalHit]) -> str:
    """Render retrieved chunks for the prompt."""
    parts = []
    for hit in hits:
        parts.append(
            f"[chunk_id: {hit.chunk_id}]\n"
            f"citation: {hit.citation} | validity: {hit.validity} | status: {hit.version_status} "
            f"| lang: {hit.lang}\n"
            f"{hit.content}"
        )
    return "\n\n---\n\n".join(parts)


def _parameter_block(record: ParameterRecord, as_of: date) -> str:
    """Render the parameter definition and its current value for the prompt."""
    info = record.information
    current = record.values[-1] if record.values else None
    return (
        f"Parameter: {info.model_target} (country {info.country})\n"
        f"Labels: {json.dumps(info.label or info.short_label or {}, ensure_ascii=False)}\n"
        f"Description: {json.dumps(info.description or {}, ensure_ascii=False)}\n"
        f"value_type: {info.value_type} | unit: {info.unit}"
        + (f" | threshold_unit: {info.threshold_unit}" if info.threshold_unit else "")
        + f"\nReference date (as_of): {as_of.isoformat()}\n"
        f"Current value: {json.dumps(current.model_dump(mode='json', include={'value', 'valid_from', 'valid_to'}), ensure_ascii=False) if current else 'none'}"
    )


def build_proposal_user(record: ParameterRecord, as_of: date, hits: list[RetrievalHit]) -> str:
    """User message for the proposal step."""
    return (
        _parameter_block(record, as_of)
        + "\n\nRetrieved legal extracts:\n\n"
        + _hits_block(hits)
    )


def build_critique_user(
    record: ParameterRecord, as_of: date, draft: ProposalDraft, hits: list[RetrievalHit]
) -> str:
    """User message for the critique step."""
    return (
        _parameter_block(record, as_of)
        + "\n\nProposal to review:\n"
        + json.dumps(draft.model_dump(mode="json"), ensure_ascii=False, indent=2)
        + "\n\nLegal extracts the proposal was based on:\n\n"
        + _hits_block(hits)
    )
