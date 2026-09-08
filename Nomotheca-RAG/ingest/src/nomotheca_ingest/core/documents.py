"""Heading-driven document building, shared by every text-shaped corpus.

Two paths turn one flat text into loadable legal units: EUROMOD Country
Reports (Markdown converted from the official Word report) and reviewer-
contributed documents (a Markdown file, a plain-text circular, an HTML page
reduced to its main block, a PDF extracted to text). They differ only in
*heading syntax* — ``#`` markers, ``<h2>`` tags, decimal numbering — so the
syntax is a pattern and the rest of the shape lives here once:

  * whatever precedes the first section heading becomes a ``preamble`` unit;
  * every heading at or below the section level becomes a unit holding the
    text up to the next heading of any level;
  * units nest by heading level, with ltree-safe, de-duplicated paths.

Nothing here touches the network or the database.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from nomotheca_ingest.core.ir import (
    Authenticity,
    InstrumentIR,
    SourceTrustClass,
    TextIR,
    UnitIR,
    VersionIR,
)

#: Named heading syntaxes. A pattern must expose a ``text`` group plus one of
#: ``marker`` (repeat count is the level), ``level`` (the level itself) or
#: ``number`` (decimal numbering: depth is the number of components).
HEADING_PATTERNS: dict[str, re.Pattern[str]] = {
    # Markdown: '## 2. Family benefits'
    "markdown": re.compile(r"^(?P<marker>#{1,6})\s+(?P<text>.+?)\s*$"),
    # HTML already reduced to text: heading tags survive as line markers, their
    # inner markup does not (see html_to_text).
    "html": re.compile(
        r"^\s*<h(?P<level>[1-6])[^>]*>\s*(?P<text>.+?)\s*</h(?P=level)>\s*$",
        re.IGNORECASE,
    ),
    # Numbered paragraphs, the usual shape of a circular with no other markup:
    # '2.1.3 Calcul de l\'allocation'
    # The numbering stays inside `text` so the ltree label is the stable
    # 'sec_2_1_3' rather than a slug of the wording.
    "numbered": re.compile(r"^\s*(?P<text>(?P<number>\d+(?:\.\d+){0,4})\.?\s+\S.*?)\s*$"),
}

_LEADING_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s")


@dataclass(slots=True)
class Heading:
    """One heading and the span of body lines that belong to it."""

    level: int
    text: str
    line_idx: int       # line index of the heading itself
    content_start: int  # line index of the first body line after the heading
    content_end: int    # line index one past the last body line


def heading_pattern(pattern: str | re.Pattern[str]) -> re.Pattern[str]:
    """Resolve a named heading syntax, or pass a compiled pattern through."""
    if isinstance(pattern, re.Pattern):
        return pattern
    try:
        return HEADING_PATTERNS[pattern]
    except KeyError:
        allowed = ", ".join(sorted(HEADING_PATTERNS))
        msg = f"Unknown heading pattern: {pattern} (known: {allowed})"
        raise ValueError(msg) from None


def _level(match: re.Match[str]) -> int:
    """Heading depth, however this pattern happens to encode it."""
    groups = match.groupdict()
    if groups.get("marker"):
        return len(groups["marker"])
    if groups.get("level"):
        return int(groups["level"])
    if groups.get("number"):
        return groups["number"].count(".") + 1
    return 1


def find_headings(lines: list[str], pattern: str | re.Pattern[str]) -> list[Heading]:
    """Locate headings outside fenced code blocks, with their body spans."""
    compiled = heading_pattern(pattern)
    found: list[Heading] = []
    in_fence = False
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = compiled.match(line)
        if match:
            if found:
                found[-1].content_end = idx
            found.append(
                Heading(
                    level=_level(match),
                    text=match.group("text").strip(),
                    line_idx=idx,
                    content_start=idx + 1,
                    content_end=len(lines),
                )
            )
    return found


def slugify(text: str) -> str:
    """Fold a heading into an ltree-safe label."""
    numbering = _LEADING_NUM_RE.match(text)
    if numbering:
        return "sec_" + numbering.group(1).replace(".", "_")
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.sub(r"[^a-z0-9]+", "_", folded.lower()).strip("_").split("_")
    slug = "_".join(words[:5])[:40].strip("_")
    return slug or "sec"


def build_document(
    *,
    text: str,
    jurisdiction: str,
    source_code: str,
    instrument_type: str,
    national_id: str,
    title: str,
    valid_from: date,
    snapshot_id: UUID,
    citation_prefix: str,
    lang: str = "en",
    pattern: str | re.Pattern[str] = "markdown",
    source_trust_class: SourceTrustClass = SourceTrustClass.EVIDENCE,
    title_from_heading: bool = False,
    version_key: str | None = None,
    unit_type_by_depth: dict[int, str] | None = None,
    default_unit_type: str = "subsection",
    metadata: dict | None = None,
    content_html: str | None = None,
    eli: str | None = None,
) -> InstrumentIR:
    """Turn one headed text into a loadable InstrumentIR.

    ``title_from_heading`` claims the first level-1 heading as the document
    title (the Country Report shape, where sections start at level 2).
    Otherwise the caller's ``title`` stands — a contributed document is titled
    by the reviewer — and sections start at the shallowest heading present.

    ``version_key`` becomes every version's ``source_version_id``, which is
    what the loader deduplicates on: pass a key that changes exactly when the
    document's content changes and re-ingestion is a no-op or a new version,
    never a pile of near-duplicates.
    """
    jurisdiction = jurisdiction.upper()
    compiled = heading_pattern(pattern)
    lines = text.splitlines()
    headings = find_headings(lines, compiled)

    if title_from_heading:
        title = next((h.text for h in headings if h.level == 1), title)
        section_level = 2
    else:
        section_level = min((h.level for h in headings), default=1)

    key = version_key or f"{national_id}@{valid_from.isoformat()}"
    unit_types = unit_type_by_depth or {section_level: "section"}

    def make_version(content: str, html: str | None = None) -> list[VersionIR]:
        if not content.strip():
            return []
        return [
            VersionIR(
                valid_from=valid_from,
                source_version_id=key,
                fetch_snapshot_id=snapshot_id,
                texts=[
                    TextIR(
                        lang=lang,
                        authenticity=Authenticity.AUTHENTIC,
                        content=content,
                        content_html=html,
                    )
                ],
            )
        ]

    units: list[UnitIR] = []
    used_paths: set[str] = set()
    stack: list[tuple[int, str]] = []          # (level, path) ancestor stack
    child_counts: dict[str | None, int] = {}
    has_children: set[str] = set()

    first_section = next((h for h in headings if h.level >= section_level), None)
    cutoff = first_section.line_idx if first_section else len(lines)
    preamble = "\n".join(line for line in lines[:cutoff] if not compiled.match(line)).strip()
    if preamble:
        units.append(
            UnitIR(
                unit_type=unit_types.get(section_level, "section"),
                path="preamble",
                citation=f"{citation_prefix}, preamble",
                ordinal=0,
                versions=make_version(preamble),
            )
        )
        used_paths.add("preamble")

    for heading in headings:
        if heading.level < section_level:
            continue
        while stack and stack[-1][0] >= heading.level:
            stack.pop()
        parent_path = stack[-1][1] if stack else None
        base = slugify(heading.text)
        path = f"{parent_path}.{base}" if parent_path else base
        bump = 2
        while path in used_paths:
            path = (f"{parent_path}.{base}" if parent_path else base) + f"_{bump}"
            bump += 1
        used_paths.add(path)

        ordinal = child_counts.get(parent_path, 0)
        child_counts[parent_path] = ordinal + 1
        if parent_path:
            has_children.add(parent_path)

        content = "\n".join(lines[heading.content_start : heading.content_end]).strip()
        units.append(
            UnitIR(
                unit_type=unit_types.get(heading.level, default_unit_type),
                path=path,
                citation=f"{citation_prefix}, \u00a7{heading.text}"[:200],
                ordinal=ordinal,
                parent_path=parent_path,
                versions=make_version(content),
                metadata={"heading_level": heading.level},
            )
        )
        stack.append((heading.level, path))

    if not units:
        # No headings and no preamble is only possible for an empty document;
        # a text with no headings at all is one unit holding the whole thing.
        units.append(
            UnitIR(
                unit_type=unit_types.get(section_level, "section"),
                path="preamble",
                citation=f"{citation_prefix}, preamble",
                versions=make_version(text.strip()),
            )
        )

    for unit in units:
        if unit.path in has_children:
            unit.is_container = True

    if content_html is not None:
        # The page as fetched, kept once beside the document's first unit text.
        # The fetch snapshot holds the authoritative bytes; copying the same
        # blob into every unit_texts row would multiply a large page by its
        # section count for no gain.
        for unit in units:
            if unit.versions and unit.versions[0].texts:
                unit.versions[0].texts[0].content_html = content_html
                break

    return InstrumentIR(
        jurisdiction=jurisdiction,
        source_code=source_code,
        instrument_type=instrument_type,
        source_trust_class=source_trust_class,
        title={lang: title},
        national_id=national_id,
        eli=eli,
        units=units,
        metadata=metadata or {},
    )
