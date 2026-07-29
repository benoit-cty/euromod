"""Versioned prompts. Prompts are artefacts: bump PROMPT_VERSION on any wording change."""

from __future__ import annotations

import json
from datetime import date

from .schema import ParameterRecord, ProposalDraft, RetrievalHit

PROMPT_VERSION = "0.3.0"

PROPOSAL_SYSTEM = """\
You are a legal analyst updating tax-benefit policy parameters for the EUROMOD microsimulation model.
You are given ONE parameter (its meaning, unit and current value) and a set of retrieved legal text
extracts, each identified by a chunk_id. Determine the value of this parameter in force on the
reference date, using ONLY the provided extracts.

The current value is a stale snapshot from an earlier year, given only so you can recognise the
concept and spot magnitude errors. Legislation NEVER mentions EUROMOD parameter names and rarely
still contains the old value — the extract linking to the parameter name or stating the current
value is NOT required and its absence is NOT a reason to return found=false. Match on the concept
described (what the parameter means, per its labels and description); if an extract states a value
for that concept in force on the reference date, propose it, even when it differs from the current
value — an updated amount is the expected, most valuable outcome.

Rules:
- supporting_extract MUST be a verbatim, contiguous quote copied from the chosen extract and must
  contain the value. It is checked character-for-character against the source; paraphrase = rejection.
- citation_chunk_id MUST be the chunk_id of the extract you quoted.
- Normalise units: percentages become decimal fractions when the parameter unit is "/1"
  (11 % -> 0.11); durations in months become decimal years only if the unit says so.
- Bracket schedules: ordered ascending, each band carries its LOWER threshold plus rate (or amount);
  the first band starts at threshold 0; the last band runs to infinity.
- valid_from is the date the value takes effect (from the version validity or the text itself).
  EXCEPTION — when the parameter block declares "Temporal basis: INCOME YEAR", valid_from MUST be
  1 January of the reference year (the income year), NOT the act's publication or in-force date:
  such acts are published after the income year yet apply retroactively to its income.
- Several extracts may state this value for different periods (annual implementing acts are
  common): choose the one whose period covers the reference date. Never prefer an extract
  merely because it matches the current value — detecting a change IS the job.
- Return found=false ONLY when no extract states a value for the described concept in force on the
  reference date. Never guess a value that is not present in the extracts.
- original_language_quote is the supporting extract in the source language; english_translation is
  your faithful translation of it.
- confidence in [0,1]: 0.9+ only when the extract states the value explicitly and unambiguously.
"""

CRITIQUE_SYSTEM = """\
You are a sceptical reviewer of a proposed policy-parameter update. You get the parameter
definition, the proposal, and the legal extracts it was based on. Perform EXACTLY three checks,
each producing one boolean (true = the check passes):
1. citation_supports_value — the quoted extract states the proposed value
   (after unit normalisation, e.g. 11 % -> 0.11 for unit "/1").
2. dates_consistent — valid_from is compatible with the cited version's validity window
   and the reference date. When the parameter block declares "Temporal basis: INCOME YEAR",
   valid_from must instead be 1 January of the reference (income) year, and a version entering
   into force AFTER the income year is correct, not an inconsistency — but a version consolidated
   before December of the income year likely states the PREVIOUS year's value: fail the check.
3. values_sane — units plausible (rates in [0,1] for unit "/1"), bracket thresholds strictly
   ascending, no absurd magnitude versus the current value.

Output procedure — follow it literally:
- Decide each check, then set its boolean: pass = true, fail = false.
- For each boolean you set to false, add ONE issues entry naming the check and the concrete error.
- Never mention a passing check in issues. If all three pass, issues MUST be the empty list [].
- An output where a boolean is false but its issues entry concludes the check actually passes is
  INVALID — re-decide and make them agree.
- Do not fail for anything outside these three checks. In particular: the current value is a stale
  snapshot from an earlier year, so a different proposed value is the expected outcome of a
  legislative update, not an error; legislation never names EUROMOD parameters, so never require
  an explicit link between the extract and the parameter name or the current value — the extract
  matching the concept in the parameter description suffices. Doubts outside the three checks may
  be recorded as an issues entry prefixed "note:" WITHOUT setting any boolean to false.
Be strict on real errors: silent errors here reach a human reviewer as trusted data.
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
    temporal_note = ""
    if info.temporal_basis == "income_year":
        year = as_of.year
        temporal_note = (
            f"\nTemporal basis: INCOME YEAR (system year = income year).\n"
            f"This parameter governs income earned in {year}. The enacting budget/finance act is "
            f"normally published late {year} or in {year + 1} yet applies retroactively to {year} "
            f"income. valid_from must be {year}-01-01. Prefer the version enacted for income year "
            f"{year}; a version in force since early {year} or before almost certainly states the "
            f"schedule for {year - 1} income — if only that is available, the act for {year} income "
            f"is not yet in the corpus."
        )
    return (
        f"Parameter: {info.model_target} (country {info.country})\n"
        f"Labels: {json.dumps(info.label or info.short_label or {}, ensure_ascii=False)}\n"
        f"Description: {json.dumps(info.description or {}, ensure_ascii=False)}\n"
        f"value_type: {info.value_type} | unit: {info.unit}"
        + (f" | threshold_unit: {info.threshold_unit}" if info.threshold_unit else "")
        + f"\nReference date (as_of): {as_of.isoformat()}"
        + temporal_note
        + f"\nCurrent value: {json.dumps(current.model_dump(mode='json', include={'value', 'valid_from', 'valid_to'}), ensure_ascii=False) if current else 'none'}"
    )


def build_proposal_user(
    record: ParameterRecord,
    as_of: date,
    hits: list[RetrievalHit],
    feedback: str | None = None,
) -> str:
    """User message for the proposal step; feedback carries a failed critique on retries."""
    message = (
        _parameter_block(record, as_of)
        + "\n\nRetrieved legal extracts:\n\n"
        + _hits_block(hits)
    )
    if feedback:
        message += (
            "\n\nYour previous proposal was rejected by review. "
            "Produce a corrected proposal that addresses every issue below:\n" + feedback
        )
    return message


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
