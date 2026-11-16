"""What a reviewer states about a contributed document, and what it means.

The kinds a reviewer may pick, in their own country's words; the level each
sits at in the hierarchy of norms; and the source-trust class derived from
it, never stated (ADR 0001).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from nomotheca_ingest.core.errors import RefusalError
from nomotheca_ingest.core.ir import ContributedKinds, NormLevel, SourceTrustClass


#: Source-trust class per level (ADR 0001). Everything with statute-level
#: authority is evidence, and so is a collective agreement (ADR 0006): where
#: one sets a rate it is the source of truth like a law; guidance and — deliberately — "other" are guidance,
#: so an unnamed document can never be granted evidence-level trust by
#: accident.
TRUST_CLASS_BY_LEVEL: dict[NormLevel, SourceTrustClass] = {
    NormLevel.STATUTE: SourceTrustClass.EVIDENCE,
    NormLevel.GOVERNMENT_REGULATION: SourceTrustClass.EVIDENCE,
    NormLevel.MINISTERIAL_ORDER: SourceTrustClass.EVIDENCE,
    NormLevel.COLLECTIVE_AGREEMENT: SourceTrustClass.EVIDENCE,
    NormLevel.ADMINISTRATIVE_GUIDANCE: SourceTrustClass.GUIDANCE,
    NormLevel.OTHER: SourceTrustClass.GUIDANCE,
}

#: The kinds every country without its own table offers (a regional child
#: jurisdiction such as ES-AR too). A country's own words are declared by its
#: adapter (`contributed_kinds`), so core holds no country's vocabulary.
DEFAULT_KINDS: ContributedKinds = (
    ("law", NormLevel.STATUTE),
    ("regulation", NormLevel.GOVERNMENT_REGULATION),
    ("ministerial_order", NormLevel.MINISTERIAL_ORDER),
    ("collective_agreement", NormLevel.COLLECTIVE_AGREEMENT),
    ("guidance", NormLevel.ADMINISTRATIVE_GUIDANCE),
    ("other", NormLevel.OTHER),
)


def kinds_by_jurisdiction() -> dict[str, ContributedKinds]:
    """Every table a reviewer may pick from: each adapter's, plus ``DEFAULT``.

    One source per country, so the CLI, the UI select and the trust mapping
    cannot drift apart.
    """
    from nomotheca_ingest.countries.registry import contributed_kinds

    return {**contributed_kinds(), "DEFAULT": DEFAULT_KINDS}


@dataclass(frozen=True, slots=True)
class ContributedFields:
    """Everything the reviewer states about a document nobody else can key.

    These six always travel together — from the CLI options or the UI form,
    through the parse, into the instrument — and three of them only mean
    anything with the others present: a kind is a kind *in a jurisdiction*, and
    the source-trust class is the kind read through that country's hierarchy of
    norms. Passing them as one value keeps that reading in one place instead of
    at every call site.

    Built by `stated_fields`, which is where an incomplete declaration is
    refused; constructing one directly asserts the reviewer answered.
    """

    jurisdiction: str
    lang: str
    title: str
    kind: str
    valid_from: date
    #: national_id of the instrument this document implements; None = "none",
    #: a valid answer that must never block an upload.
    implements: str | None = None

    def __post_init__(self) -> None:
        """Normalise the jurisdiction once, so no caller has to remember to."""
        object.__setattr__(self, "jurisdiction", self.jurisdiction.upper())
        # Fails fast, by name, on a kind this country does not use.
        norm_level_for(self.jurisdiction, self.kind)

    @property
    def norm_level(self) -> NormLevel:
        """Where the stated kind sits in this country's hierarchy of norms."""
        return norm_level_for(self.jurisdiction, self.kind)

    @property
    def source_trust_class(self) -> SourceTrustClass:
        """Derived from the kind, never stated — see ADR 0001. Through
        `trust_class_for`, the one function the guidance-publisher test checks."""
        return trust_class_for(self.jurisdiction, self.kind)

    @property
    def source_code(self) -> str:
        """The contributed-document source row this jurisdiction writes to."""
        return source_code_for(self.jurisdiction)


def stated_fields(
    *,
    jurisdiction: str | None,
    lang: str,
    title: str | None,
    kind: str | None,
    valid_from: date | None,
    implements: str | None = None,
) -> ContributedFields:
    """The reviewer's declaration, refusing an incomplete one by name.

    Separate from the value object because the refusals are reviewer-facing
    text, and because the fields arrive optional: a URL that turns out to
    belong to an official portal needs none of them.
    """
    if not jurisdiction:
        msg = "A contributed document needs the jurisdiction it belongs to"
        raise RefusalError(msg)
    if not title:
        msg = "A contributed document needs a title"
        raise RefusalError(msg)
    if not kind:
        allowed = ", ".join(kinds_for(jurisdiction))
        msg = f"A contributed document needs a kind (one of: {allowed})"
        raise RefusalError(msg)
    if valid_from is None:
        msg = (
            "A contributed document needs the date it is in force from "
            "(--valid-from): no version enters the store with an invented legal date"
        )
        raise RefusalError(msg)
    return ContributedFields(
        jurisdiction=jurisdiction,
        lang=lang,
        title=title,
        kind=kind,
        valid_from=valid_from,
        implements=implements,
    )


def source_code_for(jurisdiction: str) -> str:
    """Source registry code for a jurisdiction's contributed documents."""
    return f"{jurisdiction.upper()}-CONTRIB"


def kinds_for(jurisdiction: str) -> dict[str, NormLevel]:
    """The kinds a reviewer may state for a jurisdiction, label -> level."""
    tables = kinds_by_jurisdiction()
    table = tables.get(jurisdiction.upper(), DEFAULT_KINDS)
    return dict(table)


def norm_level_for(jurisdiction: str, kind: str) -> NormLevel:
    """Where a stated kind sits in the hierarchy of norms."""
    kinds = kinds_for(jurisdiction)
    try:
        return kinds[kind]
    except KeyError:
        allowed = ", ".join(kinds)
        msg = f"Unknown kind {kind!r} for {jurisdiction.upper()} (known: {allowed})"
        raise RefusalError(msg) from None


def trust_class_for(jurisdiction: str, kind: str) -> SourceTrustClass:
    """Source-trust class of a stated kind — derived, never stated directly."""
    return TRUST_CLASS_BY_LEVEL[norm_level_for(jurisdiction, kind)]
