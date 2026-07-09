"""Typed intermediate representation shared by country adapters and loaders."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import AnyUrl, BaseModel, ConfigDict, Field, model_validator


class Trigger(StrEnum):
    """Allowed reasons for starting an ingestion fetch run."""

    CACHE_MISS = "cache_miss"
    REFRESH = "refresh"
    BULK_SEED = "bulk_seed"
    EVAL_FREEZE = "eval_freeze"
    MANUAL = "manual"


class Authenticity(StrEnum):
    """Describes whether a text is legally authentic or derived."""

    AUTHENTIC = "authentic"
    OFFICIAL_TRANSLATION = "official_translation"
    MACHINE_TRANSLATION = "machine_translation"


class VersionStatus(StrEnum):
    """Database-compatible status values for a legal unit version."""

    IN_FORCE = "in_force"
    REPEALED = "repealed"
    NOT_YET_IN_FORCE = "not_yet_in_force"
    SUSPENDED = "suspended"
    UNKNOWN = "unknown"


class CitationRef(BaseModel):
    """A user or parameter citation before it has been resolved to source ids."""

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str = Field(min_length=2, max_length=8)
    citation: str = Field(min_length=1)
    instrument_id: str | None = None
    article_number: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceRef(BaseModel):
    """A fetchable source object id, independent of where it will be fetched from."""

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str = Field(min_length=2, max_length=8)
    source_code: str
    source_id: str
    source_type: str
    url: AnyUrl | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Snapshot(BaseModel):
    """Archived HTTP response bytes with their provenance identifier."""

    model_config = ConfigDict(extra="forbid")

    id: UUID
    source_code: str
    url: AnyUrl
    http_status: int | None = None
    content_type: str | None = None
    content_hash: str
    raw_content: bytes


class TextIR(BaseModel):
    """Language-specific rendering of a legal unit version."""

    model_config = ConfigDict(extra="forbid")

    lang: str = Field(min_length=2, max_length=12)
    authenticity: Authenticity = Authenticity.AUTHENTIC
    content: str
    content_html: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class VersionIR(BaseModel):
    """Point-in-time legal state for one structural legal unit."""

    model_config = ConfigDict(extra="forbid")

    valid_from: date
    valid_to: date | None = None
    status: VersionStatus = VersionStatus.IN_FORCE
    source_version_id: str | None = None
    eli_version: str | None = None
    citation_label: str | None = None
    fetch_snapshot_id: UUID
    amendment_note: dict[str, Any] = Field(default_factory=dict)
    texts: list[TextIR] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validity_is_not_empty(self) -> VersionIR:
        """Reject empty or reversed validity intervals before database loading."""
        if self.valid_to is not None and self.valid_to <= self.valid_from:
            msg = "valid_to must be after valid_from"
            raise ValueError(msg)
        return self


class UnitIR(BaseModel):
    """Timeless structural unit such as an article, section, or chapter."""

    model_config = ConfigDict(extra="forbid")

    unit_type: str
    path: str
    citation: str
    ordinal: int = 0
    parent_path: str | None = None
    eli: str | None = None
    national_id: str | None = None
    is_container: bool = False
    versions: list[VersionIR] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class InstrumentIR(BaseModel):
    """Citable legal instrument containing one or more legal units."""

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str
    source_code: str
    instrument_type: str
    title: dict[str, str]
    national_id: str | None = None
    eli: str | None = None
    adoption_date: date | None = None
    publication_date: date | None = None
    units: list[UnitIR] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class InstrumentRelationIR(BaseModel):
    """Amendment or citation edge discovered while parsing an instrument."""

    model_config = ConfigDict(extra="forbid")

    relation_type: str
    from_ref: str
    to_ref: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ParsedDoc(BaseModel):
    """Country-neutral parser output for one archived source document."""

    model_config = ConfigDict(extra="forbid")

    ref: SourceRef
    instruments: list[InstrumentIR] = Field(default_factory=list)
    relations: list[InstrumentRelationIR] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkItem(BaseModel):
    """Follow-up source reference discovered during parse expansion."""

    model_config = ConfigDict(extra="forbid")

    ref: SourceRef
    reason: str


class CanaryFact(BaseModel):
    """Known legal fact used to detect stale resolvers or corpora."""

    model_config = ConfigDict(extra="forbid")

    citation: str
    assert_latest_start_gte: date
    reason: str
