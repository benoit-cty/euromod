"""Pydantic models: Activity 1 parameter records, LLM outputs, and review-queue items."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class LegalStatus(StrEnum):
    ENACTED_IN_FORCE = "enacted_in_force"
    ENACTED_NOT_YET_IN_FORCE = "enacted_not_yet_in_force"
    ADOPTED_PENDING_PUBLICATION = "adopted_pending_publication"
    BILL_PROPOSED = "bill_proposed"
    ANNOUNCED = "announced"
    NATIONAL_TEAM_ESTIMATE = "national_team_estimate"


class TemporalBasis(StrEnum):
    """How legislation dates map to the parameter's validity interval.

    in_force: the value applies from the date the enacting text is in force
      (SMIC, CSG, benefit amounts) — the default.
    income_year: the value belongs to an income year that is NOT the system
      year — see `income_year_for`. The enacting act (loi de finances) is
      published during or after that income year, and valid_from is back-dated
      to the income year start (the OpenFisca convention), so retrieval must
      look for versions consolidated later than the income year itself.
    """

    IN_FORCE = "in_force"
    INCOME_YEAR = "income_year"


#: System-year → income-year offset for `temporal_basis: income_year`.
#: EUROMOD system year 2025 holds the schedule assessed in 2025, which French
#: law levies on 2024 income ("impôt 2025 sur les revenus 2024"), so the offset
#: is -1. Confirmed with the EUROMOD side on 2026-08-11. Note the FR Country
#: Report's Table 2.77 heads that column "Taxation 2025 (income 2025)" — the
#: label is wrong; the values in it are the income-year-2024 barème.
INCOME_YEAR_OFFSET = -1


def income_year_for(system_year: int) -> int:
    """The income year an `income_year` parameter's system year refers to.

    The single place this mapping is decided. Everything downstream derives
    from it: which OpenFisca key a golden case reads, which consolidation date
    retrieval targets, the `valid_from` a proposal must carry, and where the
    critique's budget-act window opens. Changing the offset here moves all four
    together — do not re-derive `as_of.year ± 1` at a call site.
    """
    return system_year + INCOME_YEAR_OFFSET


class SourceType(StrEnum):
    LEGISLATION = "legislation"
    NATIONAL_TEAM = "national_team"
    ADMINISTRATIVE_GUIDANCE = "administrative_guidance"
    OFFICIAL_STATISTICS = "official_statistics"
    PARLIAMENTARY_BILL = "parliamentary_bill"
    GOVERNMENT_ANNOUNCEMENT = "government_announcement"
    OTHER = "other"


class SourceTrustClass(StrEnum):
    """What the instrument behind a chunk may be used for (ADR 0001).

    Mirrors `instruments.source_trust_class` in the legislation DB. Retrieval
    ranks `evidence` and `guidance` equally and never returns `context`; the
    class travels with every hit and every citation so a reviewer can see
    whether a value rests on legislation or on administrative guidance.
    """

    EVIDENCE = "evidence"
    GUIDANCE = "guidance"
    CONTEXT = "context"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"


class Routing(StrEnum):
    UNCHANGED = "unchanged"
    CHANGED = "changed"
    NEW = "new"
    NOT_FOUND = "not_found"
    NATIONAL_TEAM_SOURCE = "national_team_source"
    # The value is a formula over other parameters ($PSS * 4): legislation
    # never states it directly, so the anchor parameter is what gets updated.
    DERIVED = "derived"
    # income_year parameter whose enacting act for the system year is not in
    # the corpus (yet): the best available evidence states the previous year's
    # value. A normal state of the world (finance acts arrive in Y+1), distinct
    # from not_found — there IS a value, it just cannot be confirmed for Y.
    PROVISIONAL = "provisional"


class ItemStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EDITED = "edited"
    ESCALATED = "escalated"


# ---------------------------------------------------------------------------
# Activity 1 parameter record (Param_Schema/parameter_sample.jsonc)
# ---------------------------------------------------------------------------


class Bracket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    threshold: float
    rate: float | None = None
    amount: float | None = None


class Reference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    href: str | None = None
    supporting_extract: str | None = None
    extract_offsets: tuple[int, int] | None = None
    legal_unit_ref: str | None = None
    jrc_database_id: str | None = None
    #: Source-trust class of the instrument this reference points at, so a
    #: stored decision still says what the value rested on.
    source_trust_class: SourceTrustClass | None = None
    reviewer_note: str | None = None


class RetrievalHit(BaseModel):
    """One retrieved chunk; also serves as the retrieval trace entry."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    citation: str | None = None
    context_header: str | None = None
    # "sibling": not retrieved by search — another chunk of an already-retrieved
    # article, pulled in so the whole article is visible (income-year checks).
    # "located": not ranked either — looked up by the article/act the analyst
    # named when it reported a missing source (retrieval.locate_named_units).
    method: Literal[
        "citation", "fts", "vector", "hybrid", "country_report", "sibling", "located"
    ] = "hybrid"
    #: Read from the instrument the chunk belongs to. Defaults to evidence so
    #: hand-built and mock hits behave exactly as before this column existed.
    source_trust_class: SourceTrustClass = SourceTrustClass.EVIDENCE
    score: float | None = None
    validity: str | None = None
    version_status: str | None = None
    lang: str | None = None
    content: str = ""


class Lineage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    proposed_by: Literal["pipeline", "human", "national_team", "openfisca"] = "pipeline"
    run_id: str | None = None
    prompt_version: str | None = None
    agent_version: str | None = None
    model: str | None = None
    model_answer: str | None = None
    reviewed_by: str | None = None
    review_status: ReviewStatus = ReviewStatus.PENDING
    reviewed_at: datetime | None = None
    review_note: str | None = None
    confidence: float | None = None
    retrieval_trace: list[RetrievalHit] | None = None


class ParameterValue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # None = "no normalized scalar available" (doc §6: n/a or expression rows
    # in exports >= 0.2.0), never zero.
    value: list[Bracket] | bool | float | str | None
    valid_from: date
    valid_to: date | None = None
    legal_status: LegalStatus | None = None
    source_type: SourceType | None = None
    official_journal_date: date | None = None
    references: list[Reference] = Field(default_factory=list)
    lineage: Lineage | None = None


class ParameterInformation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    country: str
    model_target: str
    spine_order: str | None = None
    value_type: str
    unit: str
    threshold_unit: str | None = None
    label: dict[str, str] | None = None
    short_label: dict[str, str] | None = None
    description: dict[str, str] | None = None
    explanation: dict[str, str] | None = None
    last_confirmed_valid_on: date | None = None
    # Curated, never derivable from the EUROMOD export (see TemporalBasis).
    temporal_basis: TemporalBasis = TemporalBasis.IN_FORCE


class ParameterRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    information: ParameterInformation
    values: list[ParameterValue]


# ---------------------------------------------------------------------------
# LLM step outputs
# ---------------------------------------------------------------------------


class Operand(BaseModel):
    """One figure a derivation uses, with the verbatim extract that states it.

    Checked exactly like a supporting_extract: the quote must be found
    character-for-character in the cited chunk, and it must state `value`.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Symbol used in `derivation`, e.g. a, b, hours")
    value: float = Field(description="The figure as the extract states it (108 % -> 1.08 is fine)")
    citation_chunk_id: str = Field(description="chunk_id of the extract stating this figure")
    supporting_extract: str = Field(description="VERBATIM contiguous quote from that chunk containing the figure")


class ProposalDraft(BaseModel):
    """Structured output of the proposal step (LLM or mock extractor)."""

    model_config = ConfigDict(extra="forbid")

    found: bool = Field(description="False when no value could be determined from the extracts")
    value_scalar: float | None = Field(default=None, description="Scalar value, unit-normalised (e.g. 20% -> 0.20)")
    value_brackets: list[Bracket] | None = Field(
        default=None, description="Ordered bands, each with its LOWER threshold and rate or amount"
    )
    valid_from: date | None = None
    valid_to: date | None = None
    legal_status: LegalStatus | None = None
    official_journal_date: date | None = None
    citation_chunk_id: str | None = Field(default=None, description="chunk_id of the extract supporting the value")
    supporting_extract: str | None = Field(
        default=None, description="VERBATIM contiguous quote from the cited chunk containing the value"
    )
    original_language_quote: str | None = None
    english_translation: str | None = None
    confidence: float = 0.0
    reasoning: str | None = None
    #: When no extract states the value (or the extracts only point at another
    #: text), the documents that would be needed — named in the law's own words
    #: and terms, e.g. "l'arrêté fixant le plafond annuel de la sécurité sociale
    #: pour 2025" or "article L. 241-3 du code de la sécurité sociale". This is
    #: what drives the gap-fill scout: the model routinely knows exactly which
    #: act it lacks and says so in prose, and this makes that machine-readable.
    #: It names DOCUMENTS to fetch, never values — nothing here is ever evidence.
    missing_sources: list[str] = Field(default_factory=list)
    #: Arithmetic over quoted operands, for a value no extract states but the
    #: extracts state everything it is computed from (a ratio of two statutory
    #: amounts, a base plus a statutory increment, hourly rate x statutory
    #: hours). `value_scalar` must equal this expression over `operands`; each
    #: operand is verified verbatim against its chunk like a supporting_extract
    #: and the only bare figures allowed are calendar constants
    #: (pipeline.DERIVATION_CONSTANTS). A stated value always wins over a
    #: derived one; the prompt says so and the critique reads both.
    derivation: str | None = Field(
        default=None,
        description="Arithmetic over operand names (+ - * / only), e.g. 'a / b', when the extracts state the operands but not the value",
    )
    operands: list[Operand] = Field(default_factory=list)


class CritiqueFindings(BaseModel):
    """Structured output of the LLM critique pass."""

    model_config = ConfigDict(extra="forbid")

    citation_supports_value: bool = True
    dates_consistent: bool = True
    values_sane: bool = True
    issues: list[str] = Field(default_factory=list)


class CritiqueReport(BaseModel):
    """Mechanical checks + LLM critique, merged."""

    model_config = ConfigDict(extra="forbid")

    schema_valid: bool = False
    citation_verified: bool = False
    extract_offsets: tuple[int, int] | None = None
    dates_consistent: bool = False
    values_sane: bool = False
    # income_year only: the cited version predates the budget-act window, so
    # the proposal likely re-states the previous year's value (see Routing).
    provisional: bool = False
    issues: list[str] = Field(default_factory=list)
    verdict: Literal["pass", "fail"] = "fail"
    critique_model: str | None = None
    #: Offsets of each operand extract (same order as draft.operands) when the
    #: proposal carried a derivation; None per operand whose quote failed.
    operand_offsets: list[tuple[int, int] | None] | None = None


# ---------------------------------------------------------------------------
# Review queue
# ---------------------------------------------------------------------------


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action: ItemStatus
    reviewer: str | None = None
    note: str | None = None
    decided_at: datetime | None = None


class ReviewItem(BaseModel):
    """One (country, parameter, as_of) run result, as shown to the human reviewer."""

    model_config = ConfigDict(extra="forbid")

    id: str
    run_id: str
    # OTel trace id (32 hex chars) of the run's root span in Phoenix — the link
    # to the full agent process. None when tracing was disabled.
    phoenix_trace_id: str | None = None
    created_at: datetime
    country: str
    model_target: str
    as_of: date
    # The EUROMOD system year this run verifies (= as_of.year). One run, one
    # system year — mirroring EUROMOD's one-software-version-per-year model.
    system_year: int | None = None
    value_type: str
    unit: str
    label: str | None = None
    status: ItemStatus = ItemStatus.PENDING
    routing: Routing
    current_value: ParameterValue | None = None
    proposed_value: ParameterValue | None = None
    critique: CritiqueReport | None = None
    #: True when the proposal has citations and every one of them is guidance
    #: (ADR 0001). Informational: Accept stays available — for a circular-
    #: governed scheme the circular IS the operative text.
    guidance_only: bool = False
    retrieval_trace: list[RetrievalHit] = Field(default_factory=list)
    proposed_record: ParameterRecord | None = None
    #: What the run was asked for: a `euromod://…` target or `group:<group_id>`.
    #: Items stored before the queue moved into the DB carried the materialized
    #: file's path under `parameter_file`; that key still loads.
    parameter_ref: str | None = Field(
        default=None, validation_alias=AliasChoices("parameter_ref", "parameter_file")
    )
    decision: Decision | None = None
    # routing=derived: the $parameters this value is a formula over.
    derived_from: list[str] | None = None
    # Gap-fill provenance: queries run / instruments auto-ingested before the
    # final retrieval, so the reviewer sees the corpus was extended by this run.
    scout: dict | None = None
    #: «a / b with a = 347.83 (AKW, artikel 12), b = 286.45 (AKW, artikel 12)»
    #: when the value was derived from quoted operands rather than stated.
    derivation: str | None = None
