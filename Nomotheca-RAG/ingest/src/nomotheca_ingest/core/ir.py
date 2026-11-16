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


class IngestMode(StrEnum):
    """What the identifier handed to an ingest run is."""

    #: A national id the adapter fetches directly (JORFTEXT…, BOE-A-…).
    INSTRUMENT = "instrument"
    #: A human citation the adapter's resolver turns into ids, at a date.
    CITATION = "citation"


class RunStatus(StrEnum):
    """``fetch_runs.status`` (the schema's CHECK constraint lists the same four)."""

    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    PARTIAL = "partial"


class NormLevel(StrEnum):
    """Where a document sits in the hierarchy of norms.

    The level is the country-neutral fact; the label a reviewer picks from is
    their own country's word for it (each adapter's `contributed_kinds`).
    """

    STATUTE = "statute"
    GOVERNMENT_REGULATION = "government_regulation"
    MINISTERIAL_ORDER = "ministerial_order"
    #: An agreement between the social partners (ANI, convention, CAO, convenio)
    #: — the operative text for contributions such as AGIRC-ARRCO, APEC or a
    #: CAO pension scheme, whose rates no statute states.
    COLLECTIVE_AGREEMENT = "collective_agreement"
    ADMINISTRATIVE_GUIDANCE = "administrative_guidance"
    OTHER = "other"


#: The kinds a reviewer may state for one country's contributed documents, in
#: that country's words, in hierarchy order: (label, level) pairs.
ContributedKinds = tuple[tuple[str, NormLevel], ...]


class Authenticity(StrEnum):
    """Describes whether a text is legally authentic or derived."""

    AUTHENTIC = "authentic"
    OFFICIAL_TRANSLATION = "official_translation"
    MACHINE_TRANSLATION = "machine_translation"


class SourceTrustClass(StrEnum):
    """What an instrument's text may be used for (ADR 0001).

    evidence: national legislation and the administrative acts that carry
      statute-level authority — the default for adapter-ingested instruments.
    guidance: circulars and administrative doctrine. Citable, and ranked equal
      to evidence in retrieval, but a proposal supported only by guidance is
      labelled as such for the reviewer.
    context: retrievable for query framing, never citable evidence (EUROMOD
      Country Reports describe the model, so citing one is circular).
    """

    EVIDENCE = "evidence"
    GUIDANCE = "guidance"
    CONTEXT = "context"


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
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceRef(BaseModel):
    """A fetchable source object id, independent of where it will be fetched from."""

    model_config = ConfigDict(extra="forbid")

    jurisdiction: str = Field(min_length=2, max_length=8)
    source_code: str
    source_id: str
    #: What kind of object ``source_id`` names — one of `SOURCE_TYPES`.
    #: Recorded for provenance and logs; no parser dispatches on it.
    source_type: str
    metadata: dict[str, Any] = Field(default_factory=dict)


#: Every ``SourceRef.source_type`` in use, and what it names. Free text in the
#: model (a new adapter may need a new word) but listed here, in one place;
#: `tests/test_ir_vocabulary.py` fails on a value used in code and missing here.
SOURCE_TYPES: dict[str, str] = {
    "instrument": "a whole act by its national id (FR JORFTEXT/KALITEXT, ES BOE-A-…, a resolved citation)",
    "article": "one article version (FR LEGIARTI/JORFARTI/KALIARTI)",
    "section": "a section of a consolidated text, expanded into its articles (FR LEGISCTA)",
    "act": "an Irish act in the eISB (IE)",
    "act_index": "the eISB's list of a year's acts (IE)",
    "toestand": "one consolidated state of a BWB regulation (NL)",
    "version_index": "the BWB list of a regulation's states (NL)",
    "consolidation_index": "the TAR list of an act's consolidated versions (LT)",
    "consolidation": "one consolidated version of a TAR act (LT)",
    "contributed_document": "a document a reviewer contributed (core.contributed)",
}


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
    source_trust_class: SourceTrustClass = SourceTrustClass.EVIDENCE
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
