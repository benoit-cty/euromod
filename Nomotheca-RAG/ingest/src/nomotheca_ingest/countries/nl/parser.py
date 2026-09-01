"""Parser for Dutch BWB payloads into legislation IR.

Two payload shapes, distinguished by the source id (see ``fetcher.py``): an
act's version index (``manifest.xml``) and one dated consolidation (a
``toestand``) whose ``<artikel>`` elements become the per-article units.

The Netherlands republishes the *whole* act on every amendment -- Wet IB 2001
has 733 published toestanden of ~2.5 MB each -- so ingesting them all would
load the same unchanged article thousands of times. Two things keep that in
check: only the toestanden in force at the EUROMOD policy dates are fetched
(``select_toestanden``), and every article carries BWB's own ``versie-id``,
emitted as ``source_version_id`` so the loader skips articles it already has.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import date
from typing import Any

from nomotheca_ingest.core.ir import (
    InstrumentIR,
    ParsedDoc,
    Snapshot,
    SourceRef,
    TextIR,
    UnitIR,
    VersionIR,
    VersionStatus,
)


# BWB's sentinel for "no end date", on both the validity and the view axis.
OPEN_ENDED = "9999-12-31"

# EUROMOD policy dates sampled from each act's version history. One toestand
# per system-year boundary, rather than all 733: because each article records
# its own inwerkingtreding, the validity loaded is still the true legal start
# date and not the sampling date. Extend this list to widen the window.
POLICY_DATES: tuple[date, ...] = (
    date(2022, 1, 1),
    date(2023, 1, 1),
    date(2024, 1, 1),
    date(2025, 1, 1),
    date(2026, 1, 1),
)

# Short citation labels for the acts EUROMOD NL cites most, keyed by BWB id.
# Curated rather than read from the payload because the citeertitel changes over
# time (BWBR0015703 was enacted as the Wet werk en bijstand and is now the
# Participatiewet) while the BWB id never does.
KNOWN_ACTS: dict[str, str] = {
    "BWBR0011353": "Wet IB 2001",
    "BWBR0002471": "Wet LB 1964",
    "BWBR0018472": "AWIR",
    "BWBR0018451": "Wet op de zorgtoeslag",
    "BWBR0008659": "Wet op de huurtoeslag",
    "BWBR0022751": "WKB",
    "BWBR0002368": "AKW",
    "BWBR0015703": "Participatiewet",
    "BWBR0002221": "AOW",
    "BWBR0017017": "Wko",
    "BWBR0004045": "WW",
    "BWBR0017745": "Wfsv",
    "BWBR0007795": "Anw",
    "BWBR0013008": "Wazo",
}

# Structural containers an article can sit under, in nesting order.
CONTAINER_TAGS = ("boek", "deel", "titeldeel", "hoofdstuk", "afdeling", "paragraaf")

# Subtrees that carry publication bookkeeping rather than legal text. Dropping
# them is what keeps ~1300 <publicatie> blocks out of the retrieval chunks.
_SKIP_TAGS = frozenset(
    {"meta-data", "bwb-inputbestand", "bwb-wijzigingen", "redactionele-correcties", "redactie"}
)


def parse_bwb_xml(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse archived BWB XML bytes into a parsed document IR."""
    if "/" in ref.source_id:
        return _parse_toestand(payload, ref, snapshot)
    return _parse_manifest(payload, ref)


# ---------------------------------------------------------------------------
# Version index (manifest.xml)
# ---------------------------------------------------------------------------


def select_toestanden(payload: bytes, targets: tuple[date, ...] = POLICY_DATES) -> list[str]:
    """Return the expression labels to ingest for the given target dates.

    BWB is bitemporal: ``geldigheid`` is when the text was in force,
    ``zicht`` is what the publisher knew when. A later amendment with
    retroactive or deferred effect mints a *new* toestand for the *same*
    validity window, so asking for the version in force on a date returns
    several documents -- all correct, all but one superseded. Their ``_N``
    label suffix is the view generation, not a version number, so taking the
    first or lowest-numbered match silently returns stale text.

    Among the expressions whose validity contains a target date, this takes the
    one with the latest ``zichtdatum_start``: current knowledge. Across all 121
    validity windows of Wet IB 2001 that is always exactly the one expression
    whose ``zichtdatum_eind`` is the ``9999-12-31`` sentinel.

    The toestand still in force (open-ended validity) is always included, so the
    corpus holds the current law even between policy dates.
    """
    root = ET.fromstring(payload)
    expressions = [_expression(node) for node in root.findall("expression")]
    expressions = [item for item in expressions if item["label"] and item["start"]]

    labels: list[str] = []
    wanted = [target.isoformat() for target in targets]
    wanted.extend(item["end"] for item in expressions if item["end"] == OPEN_ENDED)
    for target in wanted:
        candidates = [item for item in expressions if item["start"] <= target <= item["end"]]
        if not candidates:
            continue
        current = max(candidates, key=lambda item: item["zicht_start"])
        if current["label"] not in labels:
            labels.append(current["label"])
    return labels


def _expression(node: ET.Element) -> dict[str, str]:
    """Read one manifest expression's two temporal axes."""
    meta = node.find("metadata")
    read = (lambda tag: (meta.findtext(tag) or "").strip()) if meta is not None else (lambda tag: "")
    return {
        "label": node.get("label") or "",
        "start": read("datum_inwerkingtreding"),
        "end": read("einddatum") or OPEN_ENDED,
        "zicht_start": read("zichtdatum_start"),
        "zicht_end": read("zichtdatum_eind") or OPEN_ENDED,
    }


def _parse_manifest(payload: bytes, ref: SourceRef) -> ParsedDoc:
    """Expose the toestanden an act needs for the EUROMOD policy dates."""
    bwb_id = ref.source_id
    labels = select_toestanden(payload)
    child_refs = [
        {
            "source_id": f"{bwb_id}/{label}",
            "source_type": "toestand",
            "title": f"toestand per {label.rsplit('_', 1)[0]}",
        }
        for label in labels
    ]
    root = ET.fromstring(payload)
    return ParsedDoc(
        ref=ref,
        metadata={
            "child_refs": child_refs,
            "toestanden_available": len(root.findall("expression")),
            "latest_item": root.get("_latestItem"),
        },
    )


# ---------------------------------------------------------------------------
# One dated consolidation (a toestand)
# ---------------------------------------------------------------------------


def _parse_toestand(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Split one consolidated act into per-article units and versions."""
    root = ET.fromstring(payload)
    bwb_id = root.get("bwb-id") or ref.source_id.split("/", 1)[0]
    label = ref.source_id.split("/", 1)[1] if "/" in ref.source_id else ""
    wetgeving = root.find("wetgeving")
    if wetgeving is None:
        msg = f"BWB toestand {ref.source_id!r} has no <wetgeving> element"
        raise ValueError(msg)

    citeertitel = _inline_text(wetgeving.find("citeertitel")) or bwb_id
    short = KNOWN_ACTS.get(bwb_id, citeertitel)
    units = _article_units(root, bwb_id, short, snapshot)

    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type=wetgeving.get("soort") or "wet",
        national_id=bwb_id,
        # The Netherlands implements no ELI; Juriconnect is its citation scheme.
        eli=None,
        title={"nl": citeertitel},
        adoption_date=_parse_date(_intitule_attr(wetgeving, "ondertekening_bron")),
        publication_date=_parse_date(_intitule_attr(wetgeving, "publicatie_bron")),
        units=units,
        metadata={
            "bwb_id": bwb_id,
            "toestand_label": label,
            "juriconnect": f"jci1.3:c:{bwb_id}",
            "wetten_url": f"https://wetten.overheid.nl/{bwb_id}/{label.rsplit('_', 1)[0]}",
        },
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"articles": len(units)})


def _intitule_attr(wetgeving: ET.Element, name: str) -> str | None:
    """Read a date attribute off the act's <intitule> element."""
    intitule = wetgeving.find("intitule")
    return intitule.get(name) if intitule is not None else None


def _article_units(root: ET.Element, bwb_id: str, short: str, snapshot: Snapshot) -> list[UnitIR]:
    """Build one UnitIR per <artikel>, carrying its own version identity."""
    units: list[UnitIR] = []
    for ordinal, (article, containers) in enumerate(_iter_articles(root), start=1):
        number = _article_number(article)
        if not number:
            continue
        citation = f"{short}, artikel {number}"
        # bwb-ng-variabel-deel is BWB's own structural path ("/Hoofdstuk2/
        # Afdeling2.3/Artikel2.10"), reused as the ltree path so subtree
        # queries follow the act's real structure.
        path = _ltree_path(article.get("bwb-ng-variabel-deel"), number)
        inwerking = _parse_date(article.get("inwerking"))
        if inwerking is None:
            # Articles enacted but not yet commenced (status="nogniet") carry no
            # inwerkingtreding, so there is no validity range to load them under.
            # Wet IB 2001 has two, both Hoofdstuk 10A transitional provisions.
            continue
        units.append(
            UnitIR(
                unit_type="artikel",
                path=path,
                citation=citation,
                ordinal=ordinal,
                national_id=f"{bwb_id}-{number}",
                metadata={key: value for key, value in containers.items() if value},
                versions=[
                    VersionIR(
                        valid_from=inwerking,
                        # BWB gives each article a start date and no end date;
                        # the loader's _chain_versions closes the predecessor
                        # when a later version of the same article arrives.
                        valid_to=None,
                        status=_version_status(article.get("status")),
                        source_version_id=article.get("versie-id"),
                        citation_label=citation,
                        fetch_snapshot_id=snapshot.id,
                        amendment_note=_amendment_note(article),
                        texts=[TextIR(lang="nl", content=_article_text(article, number))],
                    )
                ],
            )
        )
    return units


def _iter_articles(root: ET.Element):
    """Yield every <artikel> with the titles of the containers above it."""
    def walk(node: ET.Element, containers: dict[str, str]):
        for child in node:
            if child.tag in _SKIP_TAGS:
                continue
            if child.tag == "artikel":
                yield child, containers
            elif child.tag in CONTAINER_TAGS:
                nested = {**containers, child.tag: _heading(child)}
                yield from walk(child, nested)
            else:
                yield from walk(child, containers)

    yield from walk(root, {})


def _heading(node: ET.Element) -> str:
    """Return a container's human-readable heading ("Hoofdstuk 1 Algemene bepalingen")."""
    kop = node.find("kop")
    if kop is None:
        return node.get("label") or ""
    parts = [_inline_text(kop.find(tag)) for tag in ("label", "nr", "titel")]
    return " ".join(part for part in parts if part).strip()


def _article_number(article: ET.Element) -> str:
    """Return an article's number ("2.10"), from its <kop> or its label."""
    kop = article.find("kop")
    if kop is not None:
        number = _inline_text(kop.find("nr"))
        if number:
            return number
    label = article.get("label") or ""
    return label.removeprefix("Artikel").strip()


def _article_text(article: ET.Element, number: str) -> str:
    """Render one article as plain text, headings and tables included."""
    kop = article.find("kop")
    title = _inline_text(kop.find("titel")) if kop is not None else ""
    header = f"Artikel {number}." + (f" {title}" if title else "")
    return "\n".join([header, *_blocks(article)]).strip()


def _blocks(node: ET.Element) -> list[str]:
    """Flatten an element's legal content into text blocks."""
    blocks: list[str] = []
    for child in node:
        tag = child.tag
        if tag in _SKIP_TAGS or tag in {"kop", "lidnr", "li.nr"}:
            continue
        if tag == "al":
            text = _inline_text(child)
            if text:
                blocks.append(text)
        elif tag == "table":
            blocks.extend(_table_rows(child))
        elif tag in {"lid", "li"}:
            # Keep the number attached to the first line of its own body, so a
            # quoted extract carries the paragraph number with the sentence.
            marker = _inline_text(child.find("lidnr")) or _inline_text(child.find("li.nr"))
            inner = _blocks(child)
            prefix = f"{marker.rstrip('.')}." if marker else ""
            if inner:
                blocks.append(f"{prefix} {inner[0]}".strip())
                blocks.extend(inner[1:])
            elif prefix:
                blocks.append(prefix)
        else:
            blocks.extend(_blocks(child))
    return blocks


def _table_rows(table: ET.Element) -> list[str]:
    """Render a CALS table as pipe-delimited rows.

    The Dutch fiscal parameters that matter most -- the art. 2.10 tariff
    schedule above all -- are tables, not prose. Rendering each row on one line
    keeps every figure beside its heading, and keeps the anti-hallucination
    check workable: the LLM's supporting_extract has to match this text
    character for character.
    """
    rows: list[str] = []
    for row in table.iter("row"):
        cells = [_inline_text(entry) for entry in row.findall("entry")]
        if any(cells):
            rows.append("| " + " | ".join(cells) + " |")
    return rows


def _inline_text(node: ET.Element | None) -> str:
    """Return an element's text with inline markup flattened, metadata dropped."""
    if node is None:
        return ""
    parts: list[str] = []

    def walk(element: ET.Element) -> None:
        if element.text:
            parts.append(element.text)
        for child in element:
            if child.tag not in _SKIP_TAGS:
                walk(child)
            if child.tail:
                parts.append(child.tail)

    walk(node)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def _amendment_note(article: ET.Element) -> dict[str, Any]:
    """Record which publication produced this version of the article."""
    note = {"bron": article.get("bron"), "effect": article.get("effect")}
    return {key: value for key, value in note.items() if value}


def _version_status(status: str | None) -> VersionStatus:
    """Map a BWB article status onto the schema's version status."""
    if status == "vervallen":
        return VersionStatus.REPEALED
    if status == "nogniet":
        return VersionStatus.NOT_YET_IN_FORCE
    return VersionStatus.IN_FORCE


def _ltree_path(variabel_deel: str | None, number: str) -> str:
    """Build an ltree-safe path from BWB's structural path."""
    segments = [segment for segment in (variabel_deel or "").split("/") if segment]
    if not segments:
        segments = [f"Artikel{number}"]
    return ".".join(_path_token(segment) for segment in segments)


def _path_token(value: str) -> str:
    """Sanitize a label into an ltree-compatible path token."""
    token = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return token or "unknown"


def _parse_date(value: str | None) -> date | None:
    """Parse a BWB ISO date, treating the open-ended sentinel as no date."""
    if not value or value == OPEN_ENDED:
        return None
    return date.fromisoformat(value)
