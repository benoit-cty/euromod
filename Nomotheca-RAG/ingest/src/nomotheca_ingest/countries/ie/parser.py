"""Parser for Irish payloads into legislation IR.

Two payload shapes, distinguished by the source id (see ``fetcher.py``): the
Oireachtas act index for one year (JSON, discovery only), and one act's
as-enacted eISB XML.

The eISB XML is print-derived: structure lives in ``<part>``/``<chapter>``
containers wrapping ``<sect>`` and ``<schedule>`` leaves, while typography rides
on self-closing elements (``<euro/>``, ``<emdash/>``, the Irish fada set) rather
than Unicode. Expanding those is load-bearing — Nomoscope's anti-hallucination
check matches an LLM's supporting extract character-for-character against the
chunk, so a dropped ``<euro/>`` makes every monetary quote unverifiable.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from datetime import date, datetime
from typing import Any

from nomotheca_ingest.countries.ie.fetcher import (
    ACT_INDEX_PREFIX,
    SOURCE_CODE_EISB,
    act_eli,
    section_eli,
)
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


# Start of the EUROMOD policy window. Consolidation acts are ingested as
# as-enacted baselines and their validity is closed here — see BASELINE_ACTS.
EUROMOD_WINDOW_START = date(2022, 1, 1)

# Principal consolidation acts. Ireland publishes no consolidated version of
# them (the LRC Revised Acts do not cover the TCA at all, and offer no dated
# history for the SWCA), so their as-enacted text is decades out of date for
# every fiscal provision — TCA 1997 s. 15 still states the bands in Irish
# pounds. Loading that open-ended would let `validity @> as_of` answer a 2025
# question with a 1997 answer, so these acts are loaded as structure only:
# version_status 'unknown', validity closed at the window start. The in-force
# statement for the window comes from the annual acts, which carry their own
# effective dates. Upgrade path: parse the eISB Legislation Directory
# (/eli/isbc/{year}_{no}.html) for real per-section amendment dates.
BASELINE_ACTS: dict[str, str] = {
    "1997/act/39": "Taxes Consolidation Act 1997",
    "2005/act/26": "Social Welfare Consolidation Act 2005",
}

# The fiscal act families worth ingesting out of a year's enacted acts. Titles
# are matched whole: 2024 also enacted a "Finance (State Guarantees,
# International Financial Institution Funds and Miscellaneous Provisions) Act"
# and 2025 a "Housing Finance Agency (Amendment) Act", neither of which carries
# a EUROMOD parameter. The "(No. 2)" branch is not cosmetic: the act that
# implements Budget 2024 is the Finance (No. 2) Act 2023, while a plain Finance
# Act 2023 also exists.
FINANCE_ACT_RE = re.compile(r"^Finance(?: \(No\.\s*\d+\))? Act \d{4}$")
SOCIAL_WELFARE_ACT_RE = re.compile(r"^Social Welfare\b.*\bAct \d{4}$")

_STATUTEBOOK_ELI_RE = re.compile(r"eli/(\d{4}/act/\d+)")

# Effective dates, read from the section's own text. Social Welfare Acts state a
# commencement date per section; Finance Acts state a year of assessment.
#
# Commencement is not always a single date: Social Welfare Act 2024 s. 16
# commences "in so far as it relates to jobseeker's benefit … on 26 December
# 2024" and on later dates for other benefits. The anchor phrase and the dates
# are therefore matched separately, and the section starts at the earliest of
# them — which is what the section says — with the full set kept on the version.
_COMMENCEMENT_ANCHOR_RE = re.compile(r"comes? into operation")
_COMMENCEMENT_DATE_RE = re.compile(r"\bon (?:the )?(\d{1,2})(?:st|nd|rd|th)? (\w+),? (\d{4})\b")
_YEAR_OF_ASSESSMENT_RE = re.compile(
    r"(?:[Aa]s respects|applies (?:for|as respects)) the year of assessment (\d{4})"
)
_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
}

# Print typography carried as elements rather than characters.
_ENTITIES = {
    "euro": "€", "pound": "£", "emdash": "—", "endash": "–",
    "odq": "“", "cdq": "”", "osq": "‘", "csq": "’",
    "afada": "á", "Afada": "Á", "efada": "é", "Efada": "É",
    "ifada": "í", "Ifada": "Í", "ofada": "ó", "Ofada": "Ó",
    "ufada": "ú", "Ufada": "Ú",
}
_DROPPED = frozenset({"graphic", "hr1", "marker"})

_CONTAINER_TAGS = {"part": "part", "chapter": "chapter"}
_LEAF_TAGS = {"sect": "section", "schedule": "schedule"}

_PART_LABEL_RE = re.compile(r"\b(?:PART|Part)\s+([0-9IVXLC]+)")
_CHAPTER_LABEL_RE = re.compile(r"\b(?:CHAPTER|Chapter)\s+([0-9IVXLC]+)", re.IGNORECASE)
_SCHEDULE_LABEL_RE = re.compile(r"\bSCHEDULE\s+([0-9IVXLC]+)", re.IGNORECASE)

# Block-level text elements. 'pc' is the TCA's centred-paragraph variant and
# carries schedule headings, so treating it as inline would run "SCHEDULE 1"
# into the schedule's title.
_PARAGRAPH_TAGS = frozenset({"p", "pc"})


def parse_ie(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse an archived Irish payload into a parsed document IR."""
    if ref.source_id.startswith(ACT_INDEX_PREFIX):
        return _parse_act_index(payload, ref)
    return _parse_act_xml(payload, ref, snapshot)


# ---------------------------------------------------------------------------
# Oireachtas act index (discovery)
# ---------------------------------------------------------------------------


def _parse_act_index(payload: bytes, ref: SourceRef) -> ParsedDoc:
    """Expose one year's fiscal acts as follow-up work, loading nothing."""
    results = json.loads(payload.decode("utf-8")).get("results", [])
    child_refs: list[dict[str, str]] = []
    skipped = 0
    for result in results:
        act = (result.get("bill") or {}).get("act") or {}
        title = (act.get("shortTitleEn") or "").strip()
        act_id = _act_id_from_uri(act.get("statutebookURI"))
        if not act_id:
            continue
        if not _is_fiscal_act(title):
            skipped += 1
            continue
        child_refs.append(
            {
                "source_id": act_id,
                "source_type": "act",
                "source_code": SOURCE_CODE_EISB,
                "title": title,
                "short_title": title,
                "short_title_ga": (act.get("shortTitleGa") or "").strip(),
                "date_signed": act.get("dateSigned") or "",
            }
        )
    return ParsedDoc(ref=ref, metadata={"child_refs": child_refs, "skipped_non_fiscal": skipped})


def _is_fiscal_act(short_title: str) -> bool:
    """Return whether a short title belongs to a fiscal act family."""
    return bool(FINANCE_ACT_RE.match(short_title) or SOCIAL_WELFARE_ACT_RE.match(short_title))


def _act_id_from_uri(uri: str | None) -> str | None:
    """Extract the ``{year}/act/{no}`` ingest id from an eISB ELI."""
    match = _STATUTEBOOK_ELI_RE.search(uri or "")
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# eISB act XML
# ---------------------------------------------------------------------------


def _parse_act_xml(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Split one as-enacted act into container, section, and schedule units."""
    root = ET.fromstring(payload.decode("utf-8"))
    meta = root.find("metadata")
    if meta is None:
        msg = f"eISB XML for {ref.source_id!r} has no <metadata> element"
        raise ValueError(msg)

    act_id = ref.source_id
    enacted = _parse_compact_date(_child_text(meta, "dateofenactment"))
    short_title = _short_title(ref, _child_text(meta, "title"), act_id)
    baseline = act_id in BASELINE_ACTS

    builder = _UnitBuilder(
        act_id=act_id,
        short_title=short_title,
        enacted=enacted,
        baseline=baseline,
        snapshot=snapshot,
    )
    # Sections sit in <body>; schedules — which carry the benefit rate tables —
    # sit in <backmatter>. Both are substantive text, only <frontmatter> (long
    # title and table of contents) is not.
    for section in ("body", "backmatter"):
        element = root.find(section)
        if element is not None:
            builder.walk(element, parent_path=None)

    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type="act",
        national_id=act_id,
        eli=act_eli(act_id),
        title={"en": short_title},
        adoption_date=enacted,
        publication_date=enacted,
        units=builder.units,
        metadata={
            "act_id": act_id,
            "act_number": _child_text(meta, "number"),
            "act_year": _child_text(meta, "year"),
            "as_enacted_baseline": baseline,
            **({"short_title_ga": ref.metadata["short_title_ga"]} if ref.metadata.get("short_title_ga") else {}),
        },
    )
    return ParsedDoc(
        ref=ref,
        instruments=[instrument],
        metadata={"sections": builder.leaf_count, "as_enacted_baseline": baseline},
    )


class _UnitBuilder:
    """Walk an act body into flat IR units carrying their container path."""

    def __init__(
        self,
        *,
        act_id: str,
        short_title: str,
        enacted: date,
        baseline: bool,
        snapshot: Snapshot,
    ) -> None:
        """Create a builder bound to one act's identity and snapshot."""
        self.act_id = act_id
        self.short_title = short_title
        self.enacted = enacted
        self.baseline = baseline
        self.snapshot = snapshot
        self.units: list[UnitIR] = []
        self.leaf_count = 0
        self._ordinal = 0
        self._paths: set[str] = set()

    def walk(self, element: ET.Element, parent_path: str | None) -> None:
        """Emit units for one element's children, recursing into containers."""
        for child in element:
            if child.tag in _CONTAINER_TAGS:
                path = self._container(child, parent_path)
                self.walk(child, path)
            elif child.tag in _LEAF_TAGS:
                self._leaf(child, parent_path)

    def _container(self, element: ET.Element, parent_path: str | None) -> str:
        """Emit a Part or Chapter container unit and return its path."""
        unit_type = _CONTAINER_TAGS[element.tag]
        heading = _element_text(element.find("title")).strip()
        label = _container_label(element, unit_type, heading)
        path = self._claim_path(parent_path, f"{unit_type}_{_path_token(label)}")
        self._ordinal += 1
        self.units.append(
            UnitIR(
                unit_type=unit_type,
                path=path,
                citation=f"{self.short_title}, {unit_type.capitalize()} {label}",
                ordinal=self._ordinal,
                parent_path=parent_path,
                is_container=True,
                metadata={"heading": _first_line(heading)},
            )
        )
        return path

    def _leaf(self, element: ET.Element, parent_path: str | None) -> None:
        """Emit a section or schedule unit with its single as-enacted version."""
        unit_type = _LEAF_TAGS[element.tag]
        number = _leaf_number(element, unit_type, fallback=str(self.leaf_count + 1))
        heading = _heading(element)
        body = _normalize_space(_element_text(element, skip={"title", "number"}))

        label = "s." if unit_type == "section" else "Sch."
        citation = f"{self.short_title}, {label} {number}"
        content = f"{unit_type.capitalize()} {number}. {heading}\n{body}".strip()

        self.leaf_count += 1
        self._ordinal += 1
        path = self._claim_path(parent_path, f"{'sect' if unit_type == 'section' else 'sched'}_{_path_token(number)}")
        self.units.append(
            UnitIR(
                unit_type=unit_type,
                path=path,
                citation=citation,
                ordinal=self._ordinal,
                parent_path=parent_path,
                eli=section_eli(self.act_id, number) if unit_type == "section" else None,
                national_id=f"{self.act_id}/{unit_type}/{number}",
                metadata={"heading": heading},
                versions=[self._version(number, citation, content, body)],
            )
        )

    def _version(self, number: str, citation: str, content: str, body: str) -> VersionIR:
        """Build the single version an as-enacted provision has."""
        effective, basis, stated = _effective_date(body, self.enacted)
        if self.baseline:
            # Structure only: we do not assert this text is in force in the window.
            valid_from, valid_to = self.enacted, EUROMOD_WINDOW_START
            status = VersionStatus.UNKNOWN
            basis = "as_enacted_baseline"
        else:
            valid_from, valid_to = effective, None
            status = VersionStatus.IN_FORCE
        note: dict[str, object] = {"effective_date_basis": basis}
        if len(stated) > 1:
            note["commencement_dates"] = stated
        return VersionIR(
            valid_from=valid_from,
            valid_to=valid_to,
            status=status,
            source_version_id=f"{self.act_id}/{number}/enacted",
            eli_version=section_eli(self.act_id, number),
            citation_label=citation,
            fetch_snapshot_id=self.snapshot.id,
            amendment_note=note,
            texts=[TextIR(lang="en", content=content)],
        )

    def _claim_path(self, parent_path: str | None, token: str) -> str:
        """Return a unique ltree path below a parent, disambiguating collisions."""
        path = f"{parent_path}.{token}" if parent_path else token
        if path in self._paths:
            path = f"{path}_{self._ordinal + 1}"
        self._paths.add(path)
        return path


def _effective_date(body: str, enacted: date) -> tuple[date, str, list[str]]:
    """Return the date a provision takes effect, how it was read, and all dates."""
    commencement = _commencement_dates(body)
    if commencement:
        basis = "comes_into_operation_staggered" if len(commencement) > 1 else "comes_into_operation"
        return min(commencement), basis, [day.isoformat() for day in commencement]
    match = _YEAR_OF_ASSESSMENT_RE.search(body)
    if match:
        return date(int(match.group(1)), 1, 1), "year_of_assessment", []
    return enacted, "enactment", []


def _commencement_dates(body: str) -> list[date]:
    """Return every commencement date stated after a section's operation clause."""
    anchor = _COMMENCEMENT_ANCHOR_RE.search(body)
    if anchor is None:
        return []
    dates = []
    for match in _COMMENCEMENT_DATE_RE.finditer(body, anchor.end()):
        month = _MONTHS.get(match.group(2).lower())
        if month:
            dates.append(date(int(match.group(3)), month, int(match.group(1))))
    return dates


def _short_title(ref: SourceRef, xml_title: str, act_id: str) -> str:
    """Return the act's short title, preferring the resolver's clean form.

    The XML carries a shouted print title ("FINANCE ACT 2024"); the Oireachtas
    API carries the proper short title, which the resolver forwards on the ref.
    """
    for candidate in (ref.metadata.get("short_title"), BASELINE_ACTS.get(act_id)):
        if candidate:
            return str(candidate)
    return xml_title.title() if xml_title.isupper() else (xml_title or act_id)


def _container_label(element: ET.Element, unit_type: str, heading: str) -> str:
    """Return a Part/Chapter label from the element id or its heading text."""
    element_id = element.get("id")
    if element_id:
        digits = re.sub(r"[^0-9A-Za-z]", "", element_id)
        stripped = re.sub(r"^(PART|CHAP|CHAPTER|SCHED)", "", digits, flags=re.IGNORECASE)
        if stripped:
            return stripped
    pattern = _PART_LABEL_RE if unit_type == "part" else _CHAPTER_LABEL_RE
    match = pattern.search(heading)
    return match.group(1) if match else _first_line(heading) or "1"


def _leaf_number(element: ET.Element, unit_type: str, fallback: str) -> str:
    """Return a section or schedule number, from <number>, the id, or the title.

    Sections always carry <number>. Schedules never do, and only some acts give
    them an id ("SCHED1"): Finance Act 2024's <schedule> elements are bare, so
    the number has to come off the "SCHEDULE 1" heading.
    """
    number = _child_text(element, "number").strip().rstrip(".")
    if number:
        return number
    element_id = element.get("id") or ""
    match = re.search(r"(?:SEC|SCHED)\.?([0-9A-Za-z]+)", element_id, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    if unit_type == "schedule":
        match = _SCHEDULE_LABEL_RE.search(_element_text(element.find("title")))
        if match:
            return match.group(1)
    return fallback


# ---------------------------------------------------------------------------
# Text rendering
# ---------------------------------------------------------------------------


def _element_text(element: ET.Element | None, skip: set[str] | None = None) -> str:
    """Render an element's content as plain text, expanding print entities."""
    if element is None:
        return ""
    if element.tag in _ENTITIES:
        return _ENTITIES[element.tag]
    if element.tag == "unicode":
        return _unicode_char(element.get("ch"))
    if element.tag in _DROPPED:
        return ""
    if element.tag == "table":
        return _render_table(element)
    parts = [element.text or ""]
    for child in element:
        if skip and child.tag in skip:
            parts.append(child.tail or "")
            continue
        parts.append(_element_text(child))
        parts.append(child.tail or "")
    body = "".join(parts)
    if element.tag in _PARAGRAPH_TAGS:
        return f"{body.strip()}\n"
    return body


def _render_table(element: ET.Element) -> str:
    """Flatten a rate table into pipe-delimited rows.

    Benefit and band tables are the highest-value text in the Irish corpus
    (Social Welfare Act 2024's Schedule 1 alone is ~900 cells), and a proposal
    must be able to quote a row verbatim — so the rendering has to be stable.
    """
    rows = []
    for row in element.iter("tr"):
        cells = [" ".join(_element_text(cell).split()) for cell in row.findall("td")]
        if any(cells):
            rows.append(" | ".join(cells))
    return "\n" + "\n".join(rows) + "\n" if rows else ""


def _unicode_char(code_point: str | None) -> str:
    """Return the character for a <unicode ch="00D7"/> element."""
    try:
        return chr(int(code_point or "", 16))
    except ValueError:
        return ""


def _child_text(element: ET.Element, tag: str) -> str:
    """Return the plain text of a direct child element, or an empty string."""
    child = element.find(tag)
    return "" if child is None else _element_text(child).strip()


def _first_line(value: str) -> str:
    """Return the first non-empty line of a rendered block."""
    for line in value.splitlines():
        if line.strip():
            return line.strip()
    return ""


_REDUNDANT_HEADING_RE = re.compile(r"^(?:SCHEDULE|PART|CHAPTER)\s+[0-9IVXLC]+$", re.IGNORECASE)


def _heading(element: ET.Element) -> str:
    """Return a one-line heading for a leaf unit.

    Titles run to several paragraphs: a schedule repeats its own number before
    the descriptive title, and TCA sections carry a derivation note
    ("[ITA67 s3; FA74 s86 …]") worth keeping as provenance. Drop the repeated
    number, keep the rest on one line.
    """
    lines = [line.strip() for line in _element_text(element.find("title")).splitlines() if line.strip()]
    if lines and _REDUNDANT_HEADING_RE.match(lines[0]):
        lines = lines[1:]
    return " — ".join(lines)


def _parse_compact_date(value: str) -> date:
    """Parse eISB's <dateofenactment>YYYYMMDD</dateofenactment>."""
    try:
        return datetime.strptime(value, "%Y%m%d").date()
    except ValueError as exc:
        msg = f"Unparseable eISB enactment date: {value!r}"
        raise ValueError(msg) from exc


def _path_token(value: str) -> str:
    """Sanitize a label into an ltree-compatible path token."""
    token = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return token or "unknown"


def _normalize_space(value: str) -> str:
    """Collapse the print layout's whitespace to one line per paragraph.

    Every paragraph is already its own <p>, so the blank lines the renderer
    leaves behind (element tail newlines) carry no structure — only tokens.
    """
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" ?\n ?", "\n", value)
    return re.sub(r"\n{2,}", "\n", value).strip()


def act_index_child_metadata(child: dict[str, Any]) -> dict[str, Any]:
    """Return the ref metadata a discovered act carries into its own fetch."""
    return {
        key: child[key]
        for key in ("short_title", "short_title_ga", "date_signed")
        if child.get(key)
    }
