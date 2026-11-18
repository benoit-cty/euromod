"""Parser for the Law Reform Commission's Revised Acts (consolidated text).

eISB serves acts as enacted only, so a value last changed years ago is found
in an old amending act (the Pensions (Amendment) Act 2002, the Finance Act
2015) and nowhere as the law in force. The Law Reform Commission publishes
administrative consolidations of about 580 acts at revisedacts.lawreform.ie,
one HTML page per act: the Social Welfare Consolidation Act 2005, the Finance
(Local Property Tax) Act 2012, the Childcare Support Act 2018. The Taxes
Consolidation Act 1997 is not among them.

One page is one point in time («Updated to 1 October 2026»); the site keeps no
dated history. What it does give is, per section, the F-notes: every textual
amendment with its date («Substituted (1.01.2026) by Social Welfare Act 2025
(…), s. 5»). A section's text has read as shown since its latest F-note date,
so that date is the version's start: a rate table rewritten on 1 January 2026
is not offered as the 2025 amount, and a threshold untouched since 2007 is in
force for every year of the window.

The text is rendered without the editorial apparatus — F-note markers, the
square brackets around amended words, page markers, the annotations block —
because a supporting extract is matched character-for-character.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
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
from nomotheca_ingest.core.text import UniqueCitations, month_names, path_token, pipe_rows

LRC_BASE = "https://revisedacts.lawreform.ie"
SOURCE_CODE_LRC = "IE-LRC"
REVISED_SUFFIX = "/revised"

_VOID = frozenset({"img", "br", "hr", "col", "meta", "link", "input"})
#: Editorial apparatus, never part of the law's text.
_APPARATUS = frozenset({"annotations", "commentary-reference", "markup", "page", "sect-tab", "number"})
_BLOCK_TAGS = frozenset({"p", "div", "li", "tr", "h1", "h2", "h3", "h4"})
_CONTAINERS = {"part": "part", "chapter": "chapter"}

_UPDATED_RE = re.compile(r"Updated to (\d{1,2}) (\w+) (\d{4})")
# «(1.01.2026)», and a staggered commencement «(31.12.2025 to 7.01.2026)»: the
# text reads as shown only once the last of them has passed.
_NOTE_DATE_RE = re.compile(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b")
_NOT_COMMENCED_RE = re.compile(r"not commenced", re.IGNORECASE)
_LABEL_RE = re.compile(r"^(?:PART|CHAPTER|SCHEDULE)\s+([0-9A-Z]+)\b", re.IGNORECASE)
_MONTHS = month_names(["en"])


def revised_url(source_id: str) -> str:
    """The whole-act page for a ``{year}/act/{no}/revised`` id."""
    return f"{LRC_BASE}/eli/{source_id.removesuffix(REVISED_SUFFIX)}/revised/en/html"


def is_revised(source_id: str) -> bool:
    return source_id.endswith(REVISED_SUFFIX)


@dataclass(slots=True)
class _Node:
    tag: str
    classes: frozenset[str] = frozenset()
    attrs: dict[str, str] = field(default_factory=dict)
    children: list = field(default_factory=list)  # _Node | str

    def find_all(self, cls: str):
        for child in self.children:
            if isinstance(child, _Node):
                if cls in child.classes:
                    yield child
                yield from child.find_all(cls)


class _Dom(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Node("document")
        self._stack = [self.root]

    def handle_starttag(self, tag: str, attrs) -> None:
        values = {key: value or "" for key, value in attrs}
        node = _Node(tag, frozenset(values.get("class", "").split()), values)
        self._stack[-1].children.append(node)
        if tag not in _VOID:
            self._stack.append(node)

    def handle_startendtag(self, tag: str, attrs) -> None:
        self._stack[-1].children.append(_Node(tag))

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self._stack[-1].children.append(data)


def _text(node: _Node, *, skip_sections: bool = False) -> str:
    """The law's text under a node: no apparatus, one line per paragraph or table row."""
    parts: list[str] = []
    _render(node, parts, skip_sections)
    text = "".join(parts)
    text = re.sub(r"[ \t\r\f\v ]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    return re.sub(r"\n{2,}", "\n", text).strip()


def _render(node: _Node, parts: list[str], skip_sections: bool) -> None:
    for child in node.children:
        if isinstance(child, str):
            parts.append(re.sub(r"\s+", " ", child))
            continue
        if child.classes & _APPARATUS or child.tag in ("script", "style", "img"):
            continue
        if skip_sections and child.tag == "section":
            continue
        if child.tag == "table":
            rows = pipe_rows(
                [" ".join(_text(cell).split()) for cell in _cells(row)] for row in _rows(child)
            )
            parts.append("\n" + "\n".join(rows) + "\n")
            continue
        block = child.tag in _BLOCK_TAGS
        if block:
            parts.append("\n")
        _render(child, parts, skip_sections)
        if block:
            parts.append("\n")


def _rows(table: _Node):
    for child in table.children:
        if isinstance(child, _Node):
            if child.tag == "tr":
                yield child
            elif child.tag in ("tbody", "thead", "tfoot"):
                yield from _rows(child)


def _cells(row: _Node):
    return [c for c in row.children if isinstance(c, _Node) and c.tag in ("td", "th")]


def _title_node(node: _Node) -> _Node | None:
    for child in node.children:
        if isinstance(child, _Node) and "title" in child.classes:
            return child
    return None


def _note_dates(nodes, revised_on: date) -> tuple[list[date], int]:
    """Amendment dates in a unit's F-notes, and how many notes are not yet commenced."""
    dates: list[date] = []
    pending = 0
    for node in nodes:
        for note in node.find_all("f-note"):
            text = _text(note)
            if _NOT_COMMENCED_RE.search(text):
                pending += 1
                continue
            for day, month, year in _NOTE_DATE_RE.findall(text):
                try:
                    stated = date(int(year), int(month), int(day))
                except ValueError:
                    continue
                if stated <= revised_on:
                    dates.append(stated)
    return dates, pending


def parse_revised(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Split one Revised Act page into container, section and schedule units."""
    html_text = payload.decode("utf-8", errors="replace")
    act_id = ref.source_id.removesuffix(REVISED_SUFFIX)
    match = re.search(r"<title>\s*(.*?)\s*\|", html_text, flags=re.S)
    act_title = " ".join((ref.metadata.get("short_title") or (match.group(1) if match else act_id)).split())
    updated = _UPDATED_RE.search(html_text)
    if updated is None or updated.group(2).lower() not in _MONTHS:
        msg = f"Revised Act page for {act_id!r} states no 'Updated to' date"
        raise ValueError(msg)
    revised_on = date(int(updated.group(3)), _MONTHS[updated.group(2).lower()], int(updated.group(1)))

    dom = _Dom()
    dom.feed(html_text)
    builder = _Builder(act_id, f"{act_title} (Revised)", revised_on, snapshot)
    builder.walk(dom.root, None, [], "")
    if not builder.leaf_count:
        msg = f"Revised Act page for {act_id!r} has no section"
        raise ValueError(msg)

    year = int(act_id.split("/")[0])
    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=SOURCE_CODE_LRC,
        instrument_type="act",
        national_id=ref.source_id,
        eli=revised_url(ref.source_id),
        title={"en": builder.title},
        adoption_date=date(year, 12, 31),
        publication_date=revised_on,
        units=builder.units,
        metadata={
            "act_id": act_id,
            "consolidation": "Law Reform Commission Revised Act (administrative consolidation)",
            "revised_to": revised_on.isoformat(),
        },
    )
    return ParsedDoc(
        ref=ref,
        instruments=[instrument],
        metadata={"sections": builder.leaf_count, "revised_to": revised_on.isoformat()},
    )


class _Builder:
    def __init__(self, act_id: str, title: str, revised_on: date, snapshot: Snapshot) -> None:
        self.act_id = act_id
        self.title = title
        self.revised_on = revised_on
        self.snapshot = snapshot
        self.default_start = date(int(act_id.split("/")[0]), 12, 31)
        self.units: list[UnitIR] = []
        self.leaf_count = 0
        self._ordinal = 0
        self._paths: set[str] = set()
        self._citations = UniqueCitations()

    def walk(self, node: _Node, parent_path: str | None, titles: list[_Node], prefix: str) -> None:
        """Emit units below a node. ``titles`` are the enclosing containers' title
        blocks (their F-notes date the whole container), ``prefix`` the schedule a
        part belongs to («Sch. 4, »)."""
        for child in node.children:
            if not isinstance(child, _Node):
                continue
            if child.tag != "section":
                self.walk(child, parent_path, titles, prefix)
            elif "sect" in child.classes:
                self._section(child, parent_path, titles)
            elif "schedule" in child.classes:
                self._schedule(child, parent_path)
            elif child.classes & set(_CONTAINERS):
                kind = next(_CONTAINERS[c] for c in child.classes if c in _CONTAINERS)
                if prefix and not any(True for _ in child.find_all("sect")):
                    self._leaf(child, parent_path, titles, kind, prefix)
                else:
                    path = self._container(child, parent_path, kind, prefix)
                    self.walk(child, path, [*titles, *_maybe(_title_node(child))], prefix)
            else:
                self.walk(child, parent_path, titles, prefix)

    def _container(self, node: _Node, parent_path: str | None, kind: str, prefix: str) -> str:
        heading = _heading(node)
        label = _label(node, heading)
        path = self._claim(parent_path, f"{kind}_{path_token(label)}")
        self._ordinal += 1
        self.units.append(
            UnitIR(
                unit_type=kind,
                path=path,
                citation=self._citations.claim(f"{self.title}, {prefix}{kind.capitalize()} {label}"),
                ordinal=self._ordinal,
                parent_path=parent_path,
                is_container=True,
                metadata={"heading": heading},
            )
        )
        return path

    def _section(self, node: _Node, parent_path: str | None, titles: list[_Node]) -> None:
        number = (node.attrs.get("data-number") or node.attrs.get("id", "").removeprefix("SEC")).strip()
        heading = _heading(node)
        body = _text(node, skip_sections=True)
        title = _title_node(node)
        if title is not None:
            body = body.removeprefix(_text(title)).strip()
        self._emit(
            node, parent_path, titles, unit_type="section", token=f"sect_{path_token(number)}",
            citation=f"{self.title}, s. {number}", heading=heading,
            content=f"Section {number}. {heading}\n{body}".strip(),
            eli=f"{LRC_BASE}/eli/{self.act_id}/section/{number}/revised/en/html",
            national_id=f"{self.act_id}/revised/section/{number}",
        )

    def _schedule(self, node: _Node, parent_path: str | None) -> None:
        heading = _heading(node)
        label = _label(node, heading)
        parts = [c for c in node.find_all("part")]
        if not parts:
            self._leaf(node, parent_path, [], "schedule", "", label=label)
            return
        path = self._claim(parent_path, f"sched_{path_token(label)}")
        self._ordinal += 1
        self.units.append(
            UnitIR(
                unit_type="schedule", path=path, ordinal=self._ordinal, parent_path=parent_path,
                citation=self._citations.claim(f"{self.title}, Sch. {label}"),
                is_container=True, metadata={"heading": heading},
            )
        )
        self.walk(node, path, [*_maybe(_title_node(node))], f"Sch. {label}, ")

    def _leaf(self, node, parent_path, titles, kind, prefix, label: str | None = None) -> None:
        """A schedule, or a schedule's part, as one unit of text."""
        heading = _heading(node)
        label = label or _label(node, heading)
        name = "Sch." if kind == "schedule" else kind.capitalize()
        body = _text(node)
        self._emit(
            node, parent_path, titles, unit_type="schedule", token=f"{kind[:5]}_{path_token(label)}",
            citation=f"{self.title}, {prefix}{name} {label}", heading=heading, content=body,
            eli=None, national_id=f"{self.act_id}/revised/{path_token(prefix + name + ' ' + label)}",
        )

    def _emit(self, node, parent_path, titles, *, unit_type, token, citation, heading, content, eli, national_id):
        dates, pending = _note_dates([node, *titles], self.revised_on)
        # An amendment «not commenced as of date of revision» (47 notes in the
        # 2005 Act, some dating from 2008) does not date the section: section 13,
        # the PRSI rates, carries one. The count is kept on the version.
        valid_from = max(dates, default=self.default_start)
        basis = "latest_amendment" if dates else "act_year"
        citation = self._citations.claim(citation)
        self.leaf_count += 1
        self._ordinal += 1
        self.units.append(
            UnitIR(
                unit_type=unit_type,
                path=self._claim(parent_path, token),
                citation=citation,
                ordinal=self._ordinal,
                parent_path=parent_path,
                eli=eli,
                national_id=national_id,
                metadata={"heading": heading},
                versions=[
                    VersionIR(
                        valid_from=valid_from,
                        valid_to=None,
                        status=VersionStatus.IN_FORCE,
                        # Keyed by its start, not by the revision: a later revision of an
                        # unchanged section is the same version, an amended one a new
                        # version that closes this one (loader._chain_versions).
                        source_version_id=f"{national_id}@{valid_from.isoformat()}",
                        eli_version=eli,
                        citation_label=citation,
                        fetch_snapshot_id=self.snapshot.id,
                        amendment_note={
                            "effective_date_basis": basis,
                            "revised_to": self.revised_on.isoformat(),
                            "amendments": len(dates),
                            "uncommenced_amendments": pending,
                        },
                        texts=[TextIR(lang="en", content=content)],
                    )
                ],
            )
        )

    def _claim(self, parent_path: str | None, token: str) -> str:
        path = f"{parent_path}.{token}" if parent_path else token
        if path in self._paths:
            path = f"{path}_{self._ordinal + 1}"
        self._paths.add(path)
        return path


def _maybe(node: _Node | None) -> list[_Node]:
    return [] if node is None else [node]


def _heading(node: _Node) -> str:
    title = _title_node(node)
    return " — ".join(line for line in _text(title).splitlines() if line) if title is not None else ""


def _label(node: _Node, heading: str) -> str:
    """«4» for SCHEDULE 4, «1» for a schedule's PART 1, from the heading or the id."""
    match = _LABEL_RE.match(heading)
    if match:
        return match.group(1)
    tail = re.split(r"[-_]", node.attrs.get("id", ""))[-1]
    return re.sub(r"^(?:PART|CHAPTER|CHAP|SCHED)", "", tail, flags=re.IGNORECASE) or "1"
