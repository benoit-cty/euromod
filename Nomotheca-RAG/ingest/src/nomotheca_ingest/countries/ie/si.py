"""Irish statutory instruments, as made, from eISB.

Many Irish amounts are not in any Act: the Act says «as may be prescribed»
and a Minister's regulations state the figure (qualified-adult income limits,
the Housing Assistance Payment rent limits, the childcare subsidy rates). eISB
serves an S.I. as one print-style HTML page — no XML, unlike an Act — where
every paragraph is a ``<p>`` in a layout table and a real table is a nested
``<table>``. There is no structure markup, so the text is cut on what the
drafting itself guarantees: after the enacting words («hereby make the
following Regulations»), regulations are numbered 1., 2., 3. … in order, and a
centred «SCHEDULE n» opens a schedule.

Source id ``2007/si/142``. The text is as made: an S.I. amended or revoked
later is not marked so here (eISB publishes no consolidation, and the Law
Reform Commission revises very few S.I.s), which the version's
``amendment_note`` records.
"""

from __future__ import annotations

import re
from datetime import date
from html.parser import HTMLParser

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
from nomotheca_ingest.core.text import UniqueCitations, month_names, pipe_rows

EISB_BASE = "https://www.irishstatutebook.ie"

_SI_ID_RE = re.compile(r"^(\d{4})/si/(\d+)$")
_MONTHS = month_names(["en"])
_VOID = frozenset({"img", "br", "hr", "col", "meta", "link", "input"})

_TITLE_RE = re.compile(r"S\.I\. No\. \d+/\d{4}\s*-\s*(.+)")
_ENACTING_RE = re.compile(r"\bhereby\b[^.]{0,80}\b(?:follow|as follows)", re.IGNORECASE)
_NUMBERED_RE = re.compile(r"^(\d{1,3}[A-Z]?)\.\s*(?=\S)")
_SCHEDULE_RE = re.compile(r"^(?:(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH) )?SCHEDULE(?: (\d+[A-Z]?))?$")
_ORDINALS = {"FIRST": "1", "SECOND": "2", "THIRD": "3", "FOURTH": "4", "FIFTH": "5", "SIXTH": "6"}
_SEAL_RE = re.compile(r"^(?:GIVEN under|Given under|GIVEN this|Dated this|L\.S\.)")
_NOTE_RE = re.compile(r"^EXPLANATORY NOTE", re.IGNORECASE)
_DATE = r"(\d{1,2})(?:st|nd|rd|th)?(?: day of)? (\w+),? (\d{4})"
_OPERATION_RE = re.compile(r"comes? into (?:operation|effect|force) on (?:the )?" + _DATE)
_MADE_RE = re.compile(r"(?:GIVEN under|Given under|GIVEN this|Dated this)[^\n]*\n?[^\n]*?" + _DATE)
_NOTICE_RE = re.compile(r"Iris Oifigiúil[”\"’]? of " + _DATE)


def is_si(source_id: str) -> bool:
    return _SI_ID_RE.match(source_id) is not None


def si_url(source_id: str) -> str:
    """The whole instrument on one page."""
    return f"{EISB_BASE}/eli/{source_id}/made/en/print"


def si_eli(source_id: str) -> str:
    return f"{EISB_BASE}/eli/{source_id}"


class _Blocks(HTMLParser):
    """The page's content as a list of blocks: ("p", text, centred) or ("table", rows, False).

    A stream, not a tree: the layout table never closes its rows, so a tree
    would nest thousands deep.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.blocks: list[tuple[str, object, bool]] = []
        self._in_title = False
        self._content = False
        self._tables = 0  # 1 = the layout table, 2+ = a real table
        self._text: list[str] | None = None
        self._centred = False
        self._rows: list[list[str]] = []
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "title":
            self._in_title = True
        if tag == "div" and "act-content" in values.get("class", ""):
            self._content = True
        if not self._content:
            return
        if tag == "table":
            self._flush()
            self._tables += 1
            if self._tables == 2:
                self._rows = []
        elif self._tables >= 2:
            if tag == "tr":
                self._rows.append([])
            elif tag in ("td", "th"):
                self._cell = []
        elif tag == "p":
            self._flush()
            self._text = []
            self._centred = "text-align:center" in values.get("style", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if not self._content:
            return
        if tag == "table" and self._tables:
            self._tables -= 1
            if self._tables == 1:
                rows = pipe_rows(self._rows)
                if rows:
                    self.blocks.append(("table", rows, False))
            elif self._tables == 0:
                self._flush()
                self._content = False
        elif self._tables >= 2 and tag in ("td", "th") and self._cell is not None:
            if self._rows:
                self._rows[-1].append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "p":
            self._flush()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        elif self._cell is not None:
            self._cell.append(data)
        elif self._text is not None:
            self._text.append(data)

    def _flush(self) -> None:
        if self._text is not None:
            text = " ".join("".join(self._text).split())
            if text:
                self.blocks.append(("p", text, self._centred))
        self._text = None


def _date(match: re.Match | None) -> date | None:
    if match is None:
        return None
    month = _MONTHS.get(match.group(2).lower())
    try:
        return date(int(match.group(3)), month, int(match.group(1))) if month else None
    except ValueError:
        return None


def _kind(title: str) -> str:
    """How the instrument's own provisions are cited."""
    return "reg." if re.search(r"\bRegulations\b", title) else "art."


def parse_si(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Cut one statutory instrument into its numbered provisions and schedules."""
    match = _SI_ID_RE.match(ref.source_id)
    if match is None:
        raise ValueError(f"not a statutory instrument id: {ref.source_id!r}")
    year, number = int(match.group(1)), match.group(2)
    try:
        html = payload.decode("utf-8")
    except UnicodeDecodeError:
        html = payload.decode("cp1252", errors="replace")
    page = _Blocks()
    page.feed(html)
    page.close()
    blocks = page.blocks
    if not blocks:
        raise ValueError(f"eISB page for {ref.source_id!r} has no content (no div.act-content)")

    title_match = _TITLE_RE.search(" ".join(page.title.split()))
    title = title_match.group(1).strip() if title_match else f"S.I. No. {number} of {year}"
    name = f"{title} (S.I. No. {number} of {year})"

    flat = "\n".join(text if kind == "p" else "\n".join(text) for kind, text, _ in blocks)
    made = _date(_MADE_RE.search(flat)) or _date(_NOTICE_RE.search(flat)) or date(year, 1, 1)
    stated = [d for d in map(_date, _OPERATION_RE.finditer(flat)) if d is not None]
    valid_from = min(stated) if stated else made

    # The provisions start after the enacting words; without them (a rare
    # scheme or notice) the whole text is one unit.
    start = next(
        (i + 1 for i, (kind, text, _) in enumerate(blocks) if kind == "p" and _ENACTING_RE.search(text)),
        0,
    )
    units: list[tuple[str, str, list[str]]] = []  # (unit_type, label, lines)
    expected = 1
    in_schedule = False
    pending: list[str] = []  # centred headings waiting for the provision they introduce
    for kind, text, centred in blocks[start:]:
        if kind == "table":
            (units[-1][2] if units else pending).extend(text)
            continue
        if _NOTE_RE.match(text):
            break  # the explanatory note is not part of the instrument
        schedule = _SCHEDULE_RE.match(text) if centred else None
        if schedule:
            in_schedule = True
            label = schedule.group(2) or _ORDINALS.get(schedule.group(1) or "", "")
            units.append(("schedule", label, [text]))
            pending = []
            continue
        if _SEAL_RE.match(text):
            in_schedule = False
            expected = -1  # signature block: nothing more until a schedule
            continue
        if in_schedule:
            units[-1][2].append(text)
            continue
        if expected < 0:
            continue
        numbered = _NUMBERED_RE.match(text)
        label = numbered.group(1) if numbered else ""
        # The next number, or a lettered insert after the last one (7A after 7):
        # a numbered item inside a provision starts over and opens nothing.
        if label == str(expected) or (label[-1:].isalpha() and label[:-1] == str(expected - 1)):
            if label == str(expected):
                expected += 1
            # A side heading sits on its own line before the number it titles;
            # without a centred style it was read as the previous provision's end.
            if units and not pending and units[-1][0] == "regulation" and len(units[-1][2]) > 1:
                last = units[-1][2][-1]
                if len(last) < 100 and last[-1:] not in ".;:,—" and " | " not in last:
                    pending = [units[-1][2].pop()]
            units.append(("regulation", label, [*pending, text]))
            pending = []
        elif centred and (not units or len(text) < 120):
            pending.append(text)
        elif units:
            units[-1][2].append(text)
        else:
            pending.append(text)
    if not units:
        units = [("regulation", "1", [text if kind == "p" else "\n".join(text) for kind, text, _ in blocks[start:]])]

    citations = UniqueCitations()
    paths: set[str] = set()
    abbreviation = _kind(title)
    ir_units: list[UnitIR] = []
    for ordinal, (unit_type, label, lines) in enumerate(units, start=1):
        content = "\n".join(lines).strip()
        if not content:
            continue
        if unit_type == "schedule":
            citation = citations.claim(f"{name}, Sch. {label}".rstrip() if label else f"{name}, Sch.")
            token = f"sched_{label or ordinal}"
        else:
            citation = citations.claim(f"{name}, {abbreviation} {label}")
            token = f"reg_{label}"
        path = token.lower()
        if path in paths:
            path = f"{path}_{ordinal}"
        paths.add(path)
        ir_units.append(
            UnitIR(
                unit_type="schedule" if unit_type == "schedule" else "article",
                path=path,
                citation=citation,
                ordinal=ordinal,
                national_id=f"{ref.source_id}/{token}",
                versions=[
                    VersionIR(
                        valid_from=valid_from,
                        valid_to=None,
                        status=VersionStatus.IN_FORCE,
                        source_version_id=f"{ref.source_id}/{token}/made",
                        eli_version=f"{si_eli(ref.source_id)}/made/en/html",
                        citation_label=citation,
                        fetch_snapshot_id=snapshot.id,
                        amendment_note={
                            "as_made": True,
                            "effective_date_basis": "comes_into_operation" if stated else "made",
                        },
                        texts=[TextIR(lang="en", content=content)],
                    )
                ],
            )
        )

    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type="statutory_instrument",
        national_id=ref.source_id,
        eli=si_eli(ref.source_id),
        title={"en": name},
        adoption_date=made,
        publication_date=made,
        units=ir_units,
        metadata={"si_number": number, "si_year": str(year), "as_made": True},
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"provisions": len(ir_units), "as_made": True})
