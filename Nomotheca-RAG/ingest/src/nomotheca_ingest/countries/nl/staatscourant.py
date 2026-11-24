"""Staatscourant publications, as published, from the KOOP repository.

BWB consolidates regulations; it does not hold what a Minister only *announces*.
The half-yearly «Mededeling … houdende de per 1 januari 2025 gewijzigde
bedragen in enkele wetten, besluiten en regelingen» (Stcrt. 2024, 39288) is
where the gross AOW pension (art. 9 AOW), the Anw benefits and some forty other
indexed amounts are stated; the acts themselves keep the formula. And a
regulation's explanatory note, never consolidated either, is sometimes the only
official text giving a figure (the maximum daily wage, «1/261e van 75.864,87
euro, oftewel 290,67 euro», in the note to the yearly premium regulation,
Stcrt. 2024, 38722).

Source id ``stcrt-2024-39288``, one XML document per publication on the same
repository host as BWB. Only a regulation or a notice is read (``<regeling>``,
``<circulaire>``); the Staatscourant also prints Council of State opinions,
subsidy ceilings and collective-agreement extensions, which are refused.

One publication gives up to two instruments:

- the text itself: one unit per article, per lettered section of a notice
  («C Algemene Ouderdomswet») or per annex. A regulation, and a Minister's
  «Mededeling» of amounts an act tells him to announce, are ``evidence``; any
  other circular — a policy decree of the tax administration («Besluit
  heffingskortingen», Stcrt. 2024, 38558) — is ``guidance``;
- its «Toelichting», class ``guidance`` (ADR 0001), filed as
  ``stcrt-2024-38722/toelichting``: the Minister explaining the regulation,
  citable but shown as guidance.

The text is as published: a later notice replaces the amounts without marking
this one, which ``amendment_note.as_published`` records. Every unit starts at
the date the publication itself names («met ingang van 1 januari 2025»), else
at its signing date.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import date

from nomotheca_ingest.core.ir import (
    InstrumentIR,
    ParsedDoc,
    Snapshot,
    SourceRef,
    SourceTrustClass,
    TextIR,
    UnitIR,
    VersionIR,
    VersionStatus,
)
from nomotheca_ingest.core.text import UniqueCitations, month_names, path_token
from nomotheca_ingest.countries.nl.parser import MAX_ANNEX_CHARS, _blocks, _inline_text

SOURCE_CODE_STCRT = "NL-STCRT"
REPOSITORY_BASE = "https://repository.officiele-overheidspublicaties.nl/officielepublicaties"
PORTAL_BASE = "https://zoek.officielebekendmakingen.nl"

# A rectification is its own publication, numbered «-n1».
_ID_RE = re.compile(r"^stcrt-(\d{4})-(\d+)(-n\d+)?$")
_MONTHS = month_names(["nl"])
_DATE = r"(\d{1,2})(?:e|ste|de)? (" + "|".join(_MONTHS) + r") (\d{4})"
_SIGNED_RE = re.compile(r"\bvan " + _DATE)
_START_RE = re.compile(r"\b(?:met ingang van|per) " + _DATE)
_COMMENCE_RE = re.compile(r"treedt in werking (?:met ingang van|op) " + _DATE)

# A notice's sections hang on one framing sentence («dat met ingang van
# 1 januari 2025 … de bedragen zijn gewijzigd en als volgt komen te luiden:»),
# the last line before the first section. It is repeated at the head of every
# section, so a quoted amount never stands without its date.
_MAX_FRAME_CHARS = 600
# ltree labels are capped at 255 characters; a section title can exceed that.
_MAX_TOKEN_CHARS = 60
_ARTICLE_TAGS = ("artikel", "wijzig-artikel")

_BODIES = ("regeling", "circulaire")
# Rendered as content by the BWB block renderer once renamed to <al>.
_PARAGRAPH_TAGS = frozenset({"wat", "considerans.al", "context.al"})
_LEAF_TAGS = frozenset({"al", "lijst", "table", "lid", "li", "plaatje", "al-groep"})
_SECTION_TAGS = frozenset({"divisie", "circulaire.divisie"})
_SKIPPED = frozenset(
    {"kop", "aanhef", "circulaire.aanhef", "regeling-sluiting", "circulaire-sluiting", "nota-toelichting", "bijlage"}
)


def is_stcrt(source_id: str) -> bool:
    return _ID_RE.match(source_id) is not None


def stcrt_url(source_id: str) -> str:
    """The publication's XML (the repository redirects to its current version)."""
    match = _ID_RE.match(source_id)
    if match is None:
        raise ValueError(f"not a Staatscourant id: {source_id!r}")
    return f"{REPOSITORY_BASE}/stcrt/{match.group(1)}/{source_id}/xml/{source_id}.xml"


def short_citation(source_id: str) -> str:
    """The Dutch citation form: «Stcrt. 2024, 39288»."""
    match = _ID_RE.match(source_id)
    if match is None:
        raise ValueError(f"not a Staatscourant id: {source_id!r}")
    return f"Stcrt. {match.group(1)}, {match.group(2)}{match.group(3) or ''}"


def _date(match: re.Match | None) -> date | None:
    if match is None:
        return None
    try:
        return date(int(match.group(3)), _MONTHS[match.group(2).lower()], int(match.group(1)))
    except (KeyError, ValueError):
        return None


def _normalise(root: ET.Element) -> None:
    """Drop footnotes and turn paragraph-like elements into <al>, in place.

    A footnote sits inside the sentence it annotates («… Verzamelmededeling.
    <noot>1 Stcrt. 2024, 39288</noot>»): left in, it would split the sentence a
    proposal has to quote. Its tail is the rest of the sentence and is kept.
    """
    for parent in list(root.iter()):
        previous: ET.Element | None = None
        for child in list(parent):
            if child.tag != "noot":
                previous = child
                continue
            tail = child.tail or ""
            if previous is None:
                parent.text = (parent.text or "") + tail
            else:
                previous.tail = (previous.tail or "") + tail
            parent.remove(child)
    for node in root.iter():
        if node.tag in _PARAGRAPH_TAGS:
            node.tag = "al"


def _render(node: ET.Element) -> list[str]:
    """One content element as text lines, through the BWB renderer."""
    wrapper = ET.Element("wrapper")
    wrapper.append(node)
    return _blocks(wrapper)


def _sections(node: ET.Element) -> list[tuple[str, list[str]]]:
    """Cut a text into (heading, lines), on division titles and bold subheadings.

    A heading is the path of division titles down to the text, plus the
    subheading it stands under («Artikelsgewijs — Artikel III»). Text before the
    first heading comes back under the empty heading.
    """
    sections: list[tuple[str, list[str]]] = [("", [])]

    def open_section(path: list[str], sub: str) -> None:
        heading = " — ".join([*path, sub] if sub else path)
        sections.append((heading, []))

    def walk(element: ET.Element, path: list[str]) -> None:
        sub = ""
        for child in element:
            tag = child.tag
            if tag in _SKIPPED or tag in _ARTICLE_TAGS:
                continue
            if tag == "tussenkop":
                sub = _inline_text(child)
                open_section(path, sub)
            elif tag in _SECTION_TAGS:
                title = _inline_text(child.find("kop"))
                inner = [*path, title] if title else path
                open_section(inner, "")
                walk(child, inner)
                # What follows a division belongs to its parent again.
                open_section(path, sub)
            elif tag in _LEAF_TAGS:
                sections[-1][1].extend(_render(child))
            else:
                walk(child, path)

    walk(node, [])
    return [(heading, lines) for heading, lines in sections if lines]


def _kop(node: ET.Element) -> tuple[str, str]:
    """An article's or annex's (number, title) from its <kop>."""
    kop = node.find("kop")
    if kop is None:
        return "", ""
    number, title = (_inline_text(kop.find(tag)) for tag in ("nr", "titel"))
    if not number:
        # Some headings are plain text: «ARTIKEL VIII», «BIJLAGE 1, BEHORENDE BIJ …».
        words = _inline_text(kop).split(None, 2)
        number = words[1] if len(words) > 1 else ""
        title = words[2] if len(words) > 2 else ""
    return number.rstrip(",.:"), title


def _unit(
    *,
    ref_id: str,
    unit_type: str,
    token: str,
    citation: str,
    ordinal: int,
    content: str,
    valid_from: date,
    basis: str,
    snapshot: Snapshot,
) -> UnitIR:
    return UnitIR(
        unit_type=unit_type,
        path=token,
        citation=citation,
        ordinal=ordinal,
        national_id=f"{ref_id}/{token}",
        versions=[
            VersionIR(
                valid_from=valid_from,
                valid_to=None,
                status=VersionStatus.IN_FORCE,
                source_version_id=f"{ref_id}/{token}/published",
                citation_label=citation,
                fetch_snapshot_id=snapshot.id,
                amendment_note={"as_published": True, "effective_date_basis": basis},
                texts=[TextIR(lang="nl", content=content)],
            )
        ],
    )


class _Units:
    """Collects one instrument's units, keeping citations and paths unique."""

    def __init__(self, ref_id: str, short: str, valid_from: date, basis: str, snapshot: Snapshot) -> None:
        self._ref_id = ref_id
        self._short = short
        self._valid_from = valid_from
        self._basis = basis
        self._snapshot = snapshot
        self._citations = UniqueCitations()
        self._tokens: set[str] = set()
        self.units: list[UnitIR] = []

    def add(self, unit_type: str, label: str, token: str, lines: list[str]) -> None:
        content = "\n".join(line for line in lines if line).strip()
        if not content:
            return
        ordinal = len(self.units) + 1
        token = path_token(token, fold=True)[:_MAX_TOKEN_CHARS].strip("_") or f"deel_{ordinal}"
        if token in self._tokens:
            token = f"{token}_{ordinal}"
        self._tokens.add(token)
        self.units.append(
            _unit(
                ref_id=self._ref_id,
                unit_type=unit_type,
                token=token,
                citation=self._citations.claim(f"{self._short}, {label}" if label else self._short),
                ordinal=ordinal,
                content=content,
                valid_from=self._valid_from,
                basis=self._basis,
                snapshot=self._snapshot,
            )
        )


def _body_units(body: ET.Element, units: _Units) -> None:
    """The publication's own provisions: articles, else lettered sections; then annexes."""
    for article in body.iter():
        if article.tag not in _ARTICLE_TAGS:
            continue
        number, title = _kop(article)
        header = f"Artikel {number}".strip() + "." + (f" {title}" if title else "")
        units.add("article", f"artikel {number}".strip(), f"artikel_{number}", [header, *_blocks(article)])

    sections = _sections(body)
    intro = sections.pop(0)[1] if sections and not sections[0][0] else []
    frame = intro[-1:] if sections and intro and len(intro[-1]) <= _MAX_FRAME_CHARS else []
    if intro and (not sections or len(intro) > 1):
        units.add("section", "aanhef" if sections else "tekst", "aanhef" if sections else "tekst", intro)
    for heading, lines in sections:
        units.add("section", heading, heading, [heading, *frame, *lines])

    for annex in body.iter("bijlage"):
        number, title = _kop(annex)
        name = f"bijlage {number}".strip()
        lines = [f"Bijlage {number}".strip() + "." + (f" {title}" if title else ""), *_blocks(annex)]
        # Registers and distribution tables: nothing a parameter is read from.
        if sum(map(len, lines)) <= MAX_ANNEX_CHARS:
            units.add("bijlage", name, f"bijlage_{number}", lines)


def parse_stcrt(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Cut one Staatscourant publication into its provisions and its explanatory note."""
    match = _ID_RE.match(ref.source_id)
    if match is None:
        raise ValueError(f"not a Staatscourant id: {ref.source_id!r}")
    root = ET.fromstring(payload)
    publication = root.find("staatscourant")
    body = None if publication is None else next((node for node in publication if node.tag in _BODIES), None)
    if publication is None or body is None:
        found = sorted({child.tag for child in publication}) if publication is not None else []
        raise ValueError(
            f"{ref.source_id} is not a regulation or a notice (found {found}); only <regeling> and <circulaire> are read"
        )
    _normalise(root)

    title = _inline_text(publication.find("intitule")) or _inline_text(publication.find("kop"))
    short = short_citation(ref.source_id)
    year = int(match.group(1))

    own = ET.tostring(body, encoding="unicode", method="text")
    note = body.find("nota-toelichting")
    if note is not None:
        own = own.replace(ET.tostring(note, encoding="unicode", method="text"), "")
    own = re.sub(r"\s+", " ", own)
    signed = _date(_SIGNED_RE.search(title)) or date(year, 1, 1)
    commenced = [d for d in map(_date, _COMMENCE_RE.finditer(own)) if d is not None]
    announced = _date(_START_RE.search(title)) or _date(_START_RE.search(own))
    if commenced:
        valid_from, basis = min(commenced), "treedt_in_werking"
    elif announced:
        valid_from, basis = announced, "met_ingang_van"
    else:
        valid_from, basis = signed, "signed"

    units = _Units(ref.source_id, short, valid_from, basis, snapshot)
    _body_units(body, units)
    if not units.units:
        raise ValueError(f"{ref.source_id} has no text under its <{body.tag}>")

    metadata = {
        "stcrt_id": ref.source_id,
        "citation": short,
        "as_published": True,
        "portal_url": f"{PORTAL_BASE}/{ref.source_id}.html",
    }
    has_articles = any(node.tag in _ARTICLE_TAGS for node in body.iter())
    if body.tag == "regeling" and has_articles:
        instrument_type, trust = "ministeriele-regeling", SourceTrustClass.EVIDENCE
    elif body.tag == "regeling" or title.lower().startswith("mededeling"):
        instrument_type, trust = "mededeling", SourceTrustClass.EVIDENCE
    else:
        # A circular that is not the announcement of statutory amounts states
        # how an administration applies the law (ADR 0001).
        instrument_type, trust = "beleidsregel", SourceTrustClass.GUIDANCE
    instruments = [
        InstrumentIR(
            jurisdiction=ref.jurisdiction,
            source_code=ref.source_code,
            instrument_type=instrument_type,
            source_trust_class=trust,
            national_id=ref.source_id,
            title={"nl": f"{title} ({short})" if title else short},
            adoption_date=signed,
            publication_date=signed,
            units=units.units,
            metadata=metadata,
        )
    ]

    if note is not None:
        note_id = f"{ref.source_id}/toelichting"
        note_units = _Units(note_id, f"{short}, toelichting", valid_from, basis, snapshot)
        for heading, lines in _sections(note):
            note_units.add("section", heading, heading or "algemeen", [heading, *lines] if heading else lines)
        if note_units.units:
            instruments.append(
                InstrumentIR(
                    jurisdiction=ref.jurisdiction,
                    source_code=ref.source_code,
                    instrument_type="toelichting",
                    source_trust_class=SourceTrustClass.GUIDANCE,
                    national_id=note_id,
                    title={"nl": f"Toelichting bij: {title} ({short})" if title else f"Toelichting, {short}"},
                    adoption_date=signed,
                    publication_date=signed,
                    units=note_units.units,
                    metadata={**metadata, "explains": ref.source_id},
                )
            )

    return ParsedDoc(
        ref=ref,
        instruments=instruments,
        metadata={"provisions": len(units.units), "as_published": True, "explanatory_note": len(instruments) > 1},
    )
