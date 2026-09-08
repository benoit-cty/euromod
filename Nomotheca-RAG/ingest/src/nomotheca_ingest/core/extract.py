"""Bytes plus a content type in, plain text a heading pattern can split out.

Four input shapes reach the contributed-document path: Markdown and plain text
(already text), an HTML page (mostly portal chrome around the doctrine we
want), and a PDF (a scanned-or-not circular). Each is reduced here to a text
whose headings a `documents.HEADING_PATTERNS` entry can find, plus a suggested
title, so the reviewer corrects a title rather than typing one.

No network, no database, no layout-aware PDF tooling — a plain text extractor
is deliberately all a circular needs.
"""

from __future__ import annotations

import io
import re
from dataclasses import dataclass, field
from datetime import date
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

#: Content types this path understands, keyed by file suffix.
CONTENT_TYPE_BY_SUFFIX = {
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".txt": "text/plain",
    ".text": "text/plain",
    ".html": "text/html",
    ".htm": "text/html",
    ".pdf": "application/pdf",
}

#: Page furniture: never part of the document, whatever the page looks like.
CHROME_TAGS = frozenset(
    {"script", "style", "noscript", "nav", "header", "footer", "aside", "form", "svg", "template"}
)

#: Tags that end a line of text when the tree is flattened.
BLOCK_TAGS = frozenset(
    {
        "p", "div", "section", "article", "main", "li", "ul", "ol", "dl", "dt", "dd",
        "table", "thead", "tbody", "tr", "td", "th", "blockquote", "pre", "br", "hr",
        "h1", "h2", "h3", "h4", "h5", "h6", "figure", "figcaption", "address",
    }
)

VOID_TAGS = frozenset({"br", "hr", "img", "input", "meta", "link", "source", "col", "area"})

_HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")

_FR_MONTHS = {
    "janvier": 1, "fevrier": 2, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "aout": 8, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11,
    "decembre": 12, "décembre": 12,
}

_ISO_DATE = re.compile(r"\b(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})\b")
_DMY_DATE = re.compile(r"\b(\d{1,2})[-/.](\d{1,2})[-/.](20\d{2})\b")
_FR_DATE = re.compile(
    r"\b(\d{1,2})(?:er)?\s+(" + "|".join(_FR_MONTHS) + r")\s+(20\d{2})\b", re.IGNORECASE
)
_YEAR = re.compile(r"\b(19[89]\d|20\d{2})\b")


@dataclass(slots=True)
class ExtractedText:
    """One document reduced to something the heading builder can split."""

    text: str
    #: Name of the `documents.HEADING_PATTERNS` entry that fits this text.
    pattern: str
    #: The page as fetched, kept for the unit text's HTML column (HTML only).
    html: str | None = None
    #: Best guess at the document's title: the page title, the PDF metadata
    #: title, the first heading, or None — the caller falls back to the file
    #: name and the reviewer corrects it either way.
    suggested_title: str | None = None


def content_type_for(source: str, declared: str | None = None, raw: bytes | None = None) -> str:
    """Decide a content type from the HTTP header, the file suffix, or the bytes."""
    if declared:
        kind = declared.split(";", 1)[0].strip().lower()
        if kind and kind != "application/octet-stream":
            return kind
    suffix = Path(source.split("?", 1)[0].split("#", 1)[0]).suffix.lower()
    if suffix in CONTENT_TYPE_BY_SUFFIX:
        return CONTENT_TYPE_BY_SUFFIX[suffix]
    if raw is not None:
        if raw[:5] == b"%PDF-":
            return "application/pdf"
        head = raw[:2048].lower()
        if b"<html" in head or b"<!doctype html" in head:
            return "text/html"
    return "text/plain"


def extract(raw: bytes, content_type: str) -> ExtractedText:
    """Reduce archived bytes to text plus the heading pattern that fits it."""
    if content_type == "application/pdf":
        return _from_pdf(raw)
    text = raw.decode("utf-8", errors="replace")
    if content_type in {"text/html", "application/xhtml+xml"}:
        return _from_html(text)
    if content_type == "text/markdown":
        return ExtractedText(text=text, pattern="markdown", suggested_title=_first_md_heading(text))
    return ExtractedText(text=text, pattern=detect_pattern(text))


def detect_pattern(text: str) -> str:
    """Pick the heading syntax a bare text is written in.

    Markdown markers win when present at all — nothing else produces them by
    accident. Decimal numbering needs two matches before it is believed: one
    numbered line is an enumeration, not a structure. Anything else has no
    detectable structure and becomes a single unit, which is the honest
    outcome for an unstructured circular.
    """
    from nomotheca_ingest.core.documents import HEADING_PATTERNS

    lines = text.splitlines()
    if any(HEADING_PATTERNS["markdown"].match(line) for line in lines):
        return "markdown"
    numbered = sum(1 for line in lines if HEADING_PATTERNS["numbered"].match(line))
    return "numbered" if numbered >= 2 else "markdown"


def suggested_valid_from(*candidates: str | None) -> date | None:
    """First date found in a title or a URL, for the validity-date prefill.

    A suggestion only: the reviewer states the date, and a missing one is
    refused rather than invented (see `contributed.ingest_document`).
    """
    for candidate in candidates:
        if not candidate:
            continue
        found = _find_date(candidate)
        if found is not None:
            return found
    return None


def _find_date(text: str) -> date | None:
    """Locate the first plausible date in one string."""
    match = _ISO_DATE.search(text)
    if match:
        return _safe_date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    match = _FR_DATE.search(text)
    if match:
        month = _FR_MONTHS[match.group(2).lower()]
        return _safe_date(int(match.group(3)), month, int(match.group(1)))
    match = _DMY_DATE.search(text)
    if match:
        return _safe_date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
    match = _YEAR.search(text)
    if match:
        # A year alone: the reviewer sees 1 January and corrects it if wrong.
        return date(int(match.group(1)), 1, 1)
    return None


def _safe_date(year: int, month: int, day: int) -> date | None:
    """Build a date, or None when the numbers are not one."""
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _first_md_heading(text: str) -> str | None:
    """Text of the first Markdown heading, if the file opens with one."""
    from nomotheca_ingest.core.documents import HEADING_PATTERNS

    for line in text.splitlines():
        match = HEADING_PATTERNS["markdown"].match(line)
        if match:
            return match.group("text").strip()
    return None


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------


def _from_pdf(raw: bytes) -> ExtractedText:
    """Extract a PDF's text, page by page, with no layout reconstruction."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(raw))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:  # a damaged page must not lose the rest of the document
            pages.append("")
    text = "\n".join(pages).strip()
    title = None
    try:
        metadata = reader.metadata
        title = (metadata.title or "").strip() or None if metadata else None
    except Exception:
        title = None
    return ExtractedText(text=text, pattern=detect_pattern(text), suggested_title=title)


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class _Node:
    """One element of a very small DOM: enough to find the main content block."""

    tag: str
    children: list = field(default_factory=list)  # _Node | str


class _DomBuilder(HTMLParser):
    """Build a tree of elements, dropping page furniture as it goes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Node("document")
        self._stack = [self.root]
        self._skip_depth = 0
        self._skip_tag: str | None = None
        self.title: str | None = None
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if self._skip_depth:
            if tag == self._skip_tag:
                self._skip_depth += 1
            return
        if tag in CHROME_TAGS:
            self._skip_tag, self._skip_depth = tag, 1
            return
        if tag == "title":
            self._in_title = True
            return
        if tag in VOID_TAGS:
            self._stack[-1].children.append(_Node(tag))
            return
        node = _Node(tag)
        self._stack[-1].children.append(node)
        self._stack.append(node)

    def handle_startendtag(self, tag: str, attrs) -> None:
        if not self._skip_depth and tag not in CHROME_TAGS:
            self._stack[-1].children.append(_Node(tag))

    def handle_endtag(self, tag: str) -> None:
        if self._skip_depth:
            if tag == self._skip_tag:
                self._skip_depth -= 1
                if not self._skip_depth:
                    self._skip_tag = None
            return
        if tag == "title":
            self._in_title = False
            return
        if tag in VOID_TAGS:
            return
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title = ((self.title or "") + data).strip() or None
            return
        if self._skip_depth or not data.strip():
            return
        self._stack[-1].children.append(data)


def _node_text(node: _Node) -> str:
    """All text under one node, whitespace-collapsed."""
    parts: list[str] = []
    stack = [node]
    while stack:
        current = stack.pop()
        for child in reversed(current.children):
            if isinstance(child, str):
                parts.append(child)
            else:
                stack.append(child)
    return re.sub(r"\s+", " ", " ".join(reversed(parts))).strip()


def main_block(root: _Node) -> _Node:
    """The document's own content: <main>/<article>, else the largest block.

    "Largest block" is resolved by descending from the root into whichever
    child still holds nearly all of the text — the classic readability walk.
    Page furniture has already been dropped by the parser, so what is left is
    the doctrine and not the portal chrome.
    """
    for tag in ("main", "article"):
        found = _find_tag(root, tag)
        if found is not None and _node_text(found):
            return found
    node = _find_tag(root, "body") or root
    while True:
        total = len(_node_text(node))
        if total == 0:
            return node
        elements = [child for child in node.children if isinstance(child, _Node)]
        biggest = max(elements, key=lambda child: len(_node_text(child)), default=None)
        if biggest is None or len(_node_text(biggest)) < 0.9 * total:
            return node
        node = biggest


def _find_tag(node: _Node, tag: str) -> _Node | None:
    """Depth-first search for the first element with a tag."""
    stack = [node]
    while stack:
        current = stack.pop(0)
        if current.tag == tag:
            return current
        stack = [child for child in current.children if isinstance(child, _Node)] + stack
    return None


def _flatten(node: _Node, lines: list[str]) -> None:
    """Render an element tree as lines, headings kept as <hN> markers."""
    if node.tag in _HEADING_TAGS:
        text = _node_text(node)
        if text:
            lines.append(f"<{node.tag}>{text}</{node.tag}>")
        return
    buffer: list[str] = []

    def flush() -> None:
        joined = re.sub(r"\s+", " ", " ".join(buffer)).strip()
        if joined:
            lines.append(joined)
        buffer.clear()

    for child in node.children:
        if isinstance(child, str):
            buffer.append(child)
        elif child.tag in BLOCK_TAGS or child.tag in _HEADING_TAGS:
            flush()
            _flatten(child, lines)
        else:
            buffer.append(_node_text(child))
    flush()


def _from_html(html: str) -> ExtractedText:
    """Reduce a page to its main content block, as text with heading markers."""
    builder = _DomBuilder()
    builder.feed(html)
    builder.close()
    block = main_block(builder.root)
    lines: list[str] = []
    _flatten(block, lines)
    text = "\n".join(lines).strip()
    title = builder.title
    if not title:
        for line in lines:
            if line.startswith("<h"):
                title = unescape(re.sub(r"</?h[1-6][^>]*>", "", line)).strip()
                break
    return ExtractedText(text=text, pattern="html", html=html, suggested_title=title)
