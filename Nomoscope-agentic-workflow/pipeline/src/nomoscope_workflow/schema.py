"""Pydantic models: Activity 1 parameter records, LLM outputs, and review-queue items."""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LegalStatus(StrEnum):
    ENACTED_IN_FORCE = "enacted_in_force"
    ENACTED_NOT_YET_IN_FORCE = "enacted_not_yet_in_force"
    ADOPTED_PENDING_PUBLICATION = "adopted_pending_publication"
    BILL_PROPOSED = "bill_proposed"
    ANNOUNCED = "announced"
    NATIONAL_TEAM_ESTIMATE = "national_team_estimate"


class SourceType(StrEnum):
    LEGISLATION = "legislation"
    NATIONAL_TEAM = "national_team"
    ADMINISTRATIVE_GUIDANCE = "administrative_guidance"
    OFFICIAL_STATISTICS = "official_statistics"
    PARLIAMENTARY_BILL = "parliamentary_bill"
    GOVERNMENT_ANNOUNCEMENT = "government_announcement"
    OTHER = "other"


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
    reviewer_note: str | None = None


class RetrievalHit(BaseModel):
    """One retrieved chunk; also serves as the retrieval trace entry."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    citation: str | None = None
    context_header: str | None = None
    method: Literal["citation", "fts", "vector", "hybrid"] = "hybrid"
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


class ParameterRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    information: ParameterInformation
    values: list[ParameterValue]


# ---------------------------------------------------------------------------
# LLM step outputs
# ---------------------------------------------------------------------------


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
    issues: list[str] = Field(default_factory=list)
    verdict: Literal["pass", "fail"] = "fail"
    critique_model: str | None = None


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
    value_type: str
    unit: str
    label: str | None = None
    status: ItemStatus = ItemStatus.PENDING
    routing: Routing
    current_value: ParameterValue | None = None
    proposed_value: ParameterValue | None = None
    critique: CritiqueReport | None = None
    retrieval_trace: list[RetrievalHit] = Field(default_factory=list)
    proposed_record: ParameterRecord | None = None
    parameter_file: str | None = None
    decision: Decision | None = None
    # routing=derived: the $parameters this value is a formula over.
    derived_from: list[str] | None = None
    # Gap-fill provenance: queries run / instruments auto-ingested before the
    # final retrieval, so the reviewer sees the corpus was extended by this run.
    scout: dict | None = None
