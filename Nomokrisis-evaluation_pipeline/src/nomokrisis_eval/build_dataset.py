"""Draft golden cases with an LLM from a trusted source document + parameter records.

The model only extracts the ground-truth value/date/citation from the supplied
document (a EUROMOD country report excerpt, national-team notes, or a pasted
article). The expected *routing* is computed deterministically by comparing the
drafted value against the parameter's value in force. Every drafted case is
saved with verified=False — a human must confirm it before it counts as ground
truth (freeze the golden set only from verified cases).

The call goes through `nomoscope_workflow.llm.run_agent` (PydanticAI structured
output) like every other LLM call in the system (ADR 0004): the model is a
provider-prefixed string, and the worker is the only process that holds a key.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict

from nomoscope_workflow import paramdb
from nomoscope_workflow.llm import run_agent
from nomoscope_workflow.queue_store import slugify
from nomoscope_workflow.schema import Bracket, ParameterRecord, ParameterValue, Routing

from .labels import draft_labels
from .schema import Expected, GoldenCase
from .scoring import values_equal

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


def check_builder_model(model: str) -> str:
    """A drafting model must be a real one: a `mock/` drafter would write a
    fabricated ground truth into the golden set."""
    provider = model.partition("/")[0]
    if not provider or "/" not in model:
        raise ValueError(
            f"builder model must be provider-prefixed (anthropic/…, azure_openai/…, jrc/…), not {model!r}"
        )
    if provider == "mock":
        raise ValueError(
            f"refusing to draft golden cases with {model!r}: a mock model cannot read the "
            "source document, so its output would be a fabricated ground truth"
        )
    return model


def _current_value(record: ParameterRecord, as_of: date) -> ParameterValue | None:
    for value in record.values:
        if value.valid_from <= as_of and (value.valid_to is None or value.valid_to >= as_of):
            return value
    return None


def case_slug(model_target: str, country: str) -> str:
    """euromod://FR/tinkt_fr/def_const/$tin_upthres1 -> 'tinkt_tin_upthres1'.

    The country prefixes the case id already and `def_const` is the only
    function in the export, so both are noise in a case id.
    """
    parts = paramdb.parse_model_target(model_target)
    policy = (parts["policy"] or "").removesuffix(f"_{country.lower()}")
    name = (parts["name"] or model_target).lstrip("$")
    return slugify(f"{policy}_{name}") if policy else slugify(name)


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


def draft_truth(model: str, record: ParameterRecord, as_of: date, source_text: str) -> DraftedTruth:
    """One structured-output call -> validated DraftedTruth."""
    return run_agent(
        check_builder_model(model),
        SYSTEM_PROMPT,
        _build_user_prompt(record, as_of, source_text),
        output_type=DraftedTruth,
        temperature=0.0,
    )


def to_golden_case(
    record: ParameterRecord,
    parameter_target: str,
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

    country = info.country.lower()
    slug = (
        case_slug(info.model_target, country)
        if not parameter_target.startswith("group:")
        else slugify(parameter_target.removeprefix("group:"))
    )
    notes = " | ".join(filter(None, [draft.notes, f"quote: {draft.quote}" if draft.quote else None]))
    drafted = draft_labels(
        value=value,
        citations=draft.citations,
        temporal_basis=info.temporal_basis,
        is_bracket_table=bool(draft.value_brackets),
    )
    return GoldenCase(
        id=f"{country}_{slug}_{as_of.isoformat()}",
        country=info.country,
        language=language,
        parameter_target=parameter_target,
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
    source_text: str,
    records: list[tuple[ParameterRecord, str]],
    as_of: date,
    language: str,
) -> list[tuple[GoldenCase | None, str]]:
    """Draft one case per (record, parameter_target); returns (case, message) pairs."""
    check_builder_model(model)
    out: list[tuple[GoldenCase | None, str]] = []
    for record, parameter_target in records:
        label = parameter_target
        try:
            draft = draft_truth(model, record, as_of, source_text)
        except Exception as exc:
            out.append((None, f"{label}: FAILED ({exc.__class__.__name__}: {exc})"))
            continue
        case = to_golden_case(record, parameter_target, as_of, language, draft, drafted_by=model)
        out.append((case, f"{label}: {case.expected.routing} (confidence {draft.confidence:.2f})"))
    return out
