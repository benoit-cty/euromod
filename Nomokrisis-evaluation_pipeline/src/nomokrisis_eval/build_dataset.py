"""Draft golden cases with Claude Fable from a source document + Activity 1 parameter files.

The model only extracts the ground-truth value/date/citation from the supplied
document (a EUROMOD country report excerpt, national-team notes, or a pasted
article). The expected *routing* is computed deterministically by comparing the
drafted value against the parameter file's value in force. Every drafted case is
saved with verified=False — a human must confirm it before it counts as ground
truth (freeze the golden set only from verified cases).
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import anthropic
from pydantic import BaseModel, ConfigDict

from nomoscope_workflow.queue_store import load_record
from nomoscope_workflow.schema import Bracket, ParameterRecord, ParameterValue, Routing

from .config import REPO_ROOT
from .labels import draft_labels
from .schema import Expected, GoldenCase
from .scoring import values_equal

FALLBACK_MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """\
You are building a validation ("golden") dataset for a pipeline that updates EUROMOD
fiscal-policy parameters from national legislation. You are given ONE parameter
definition (with its currently recorded value) and a source document that is trusted
ground truth (a EUROMOD country report excerpt or validated notes).

Extract the correct value of the parameter at the given reference date, strictly from
the source document. Rules:
- Normalise rates to fractions (45% -> 0.45). Bracket schedules are ordered lists of
  LOWER thresholds with their rate or amount.
- valid_from is the date the extracted value became applicable, if the document states it.
- citations are pinpoint legal references supporting the value (instrument + article,
  e.g. "CGI, art. 197"), as stated in the document.
- quote is a short verbatim extract from the document supporting the value.
- If the document does not determine the value, return found=false and explain in notes.
  Never guess or use outside knowledge for the value itself.
"""

DRAFT_SCHEMA = {
    "type": "object",
    "properties": {
        "found": {"type": "boolean"},
        "value_scalar": {"type": ["number", "null"]},
        "value_brackets": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "properties": {
                    "threshold": {"type": "number"},
                    "rate": {"type": ["number", "null"]},
                    "amount": {"type": ["number", "null"]},
                },
                "required": ["threshold", "rate", "amount"],
                "additionalProperties": False,
            },
        },
        "valid_from": {"type": ["string", "null"], "description": "ISO date YYYY-MM-DD"},
        "citations": {"type": "array", "items": {"type": "string"}},
        "quote": {"type": ["string", "null"]},
        "confidence": {"type": "number"},
        "notes": {"type": ["string", "null"]},
    },
    "required": [
        "found", "value_scalar", "value_brackets", "valid_from",
        "citations", "quote", "confidence", "notes",
    ],
    "additionalProperties": False,
}


class DraftedTruth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    found: bool
    value_scalar: float | None = None
    value_brackets: list[Bracket] | None = None
    valid_from: date | None = None
    citations: list[str] = []
    quote: str | None = None
    confidence: float = 0.0
    notes: str | None = None


def _current_value(record: ParameterRecord, as_of: date) -> ParameterValue | None:
    for value in record.values:
        if value.valid_from <= as_of and (value.valid_to is None or value.valid_to >= as_of):
            return value
    return None


def _build_user_prompt(record: ParameterRecord, as_of: date, source_text: str) -> str:
    info = record.information
    current = _current_value(record, as_of)
    return (
        f"Reference date (as_of): {as_of.isoformat()}\n\n"
        f"Parameter definition:\n{info.model_dump_json(indent=2, exclude_none=True)}\n\n"
        f"Currently recorded value (may be outdated):\n"
        f"{current.model_dump_json(indent=2, exclude_none=True) if current else 'none'}\n\n"
        f"Source document (trusted ground truth):\n---\n{source_text}\n---"
    )


def draft_truth(
    client: anthropic.Anthropic, model: str, record: ParameterRecord, as_of: date, source_text: str
) -> DraftedTruth:
    """One Fable call -> validated DraftedTruth. Raises on refusal of the whole chain."""
    response = client.beta.messages.create(
        model=model,
        max_tokens=16000,
        # Fable's safety classifiers can false-positive; fall back to Opus in-call.
        betas=["server-side-fallback-2026-06-01"],
        fallbacks=[{"model": FALLBACK_MODEL}],
        output_config={"format": {"type": "json_schema", "schema": DRAFT_SCHEMA}},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(record, as_of, source_text)}],
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(
            f"model declined the request ({response.stop_details.category if response.stop_details else 'unknown'})"
        )
    text = next(b.text for b in response.content if b.type == "text")
    return DraftedTruth.model_validate(json.loads(text))


def to_golden_case(
    record: ParameterRecord,
    parameter_file: Path,
    as_of: date,
    language: str,
    draft: DraftedTruth,
    drafted_by: str,
) -> GoldenCase:
    """Deterministic routing vs the recorded value; the model never decides routing."""
    info = record.information
    current = _current_value(record, as_of)
    value = draft.value_brackets if draft.value_brackets is not None else draft.value_scalar

    if not draft.found or value is None:
        routing = Routing.NOT_FOUND
        value = None
    elif current is None:
        routing = Routing.NEW
    elif values_equal(current.value, value):
        routing = Routing.UNCHANGED
    else:
        routing = Routing.CHANGED

    case_id = f"{info.country.lower()}_{parameter_file.stem}_{as_of.isoformat()}"
    notes = " | ".join(filter(None, [draft.notes, f"quote: {draft.quote}" if draft.quote else None]))
    drafted = draft_labels(
        value=value,
        citations=draft.citations,
        temporal_basis=info.temporal_basis,
        is_bracket_table=bool(draft.value_brackets),
    )
    return GoldenCase(
        id=case_id,
        country=info.country,
        language=language,
        parameter_file=parameter_file.relative_to(REPO_ROOT).as_posix(),
        as_of=as_of,
        difficulty=drafted.difficulty,
        hazards=drafted.hazards,
        source_class="codified_law",
        expected=Expected(
            routing=routing,
            value=value,
            valid_from=draft.valid_from,
            citations=draft.citations,
        ),
        verified=False,
        drafted_by=drafted_by,
        notes=notes or None,
    )


def build_cases(
    model: str,
    source_file: Path,
    parameter_files: list[Path],
    as_of: date,
    language: str,
) -> list[tuple[GoldenCase | None, str]]:
    """Draft one case per parameter file; returns (case, message) pairs."""
    client = anthropic.Anthropic()
    source_text = source_file.read_text(encoding="utf-8")
    out: list[tuple[GoldenCase | None, str]] = []
    for path in parameter_files:
        record = load_record(path)
        try:
            draft = draft_truth(client, model, record, as_of, source_text)
        except Exception as exc:
            out.append((None, f"{path.name}: FAILED ({exc.__class__.__name__}: {exc})"))
            continue
        case = to_golden_case(record, path.resolve(), as_of, language, draft, drafted_by=model)
        out.append((case, f"{path.name}: {case.expected.routing} (confidence {draft.confidence:.2f})"))
    return out
