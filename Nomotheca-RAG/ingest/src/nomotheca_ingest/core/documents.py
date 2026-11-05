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
    # 'sec_2_1_3' rather than a slug of the wording. A letter must follow the
    # number: a table row is not a heading («19 212,03 € 1 601 €», the couple
    # ceiling of Cnav circular 2025-13, became section 19 and was pruned with
    # its figure).
    "numbered": re.compile(
        r"^\s*(?P<text>(?P<number>\d+(?:\.\d+){0,4})\.?\s+[^\W\d_].*?)\s*$"
    ),
}

#: Patterns whose headings are body text, kept as their unit's first line. A
#: numbered paragraph is a sentence of the document («2. Montant maximal de
#: l'ASI lorsque le conjoint … ne bénéficie ni de l'ASI, ni de l'Aspa à compter
#: du 1er avril 2025»), not a title: left out, it can be neither retrieved nor
#: quoted. Markdown and HTML headings stay titles, kept in the citation only.
BODY_HEADING_PATTERNS = frozenset({"numbered"})

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


_MONTHS = (
    "janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|decembre"
    "|january|february|march|april|may|june|july|august|september|october|november|december"
)
_DATE_OR_YEAR = re.compile(rf"\s*(?:(?:[1-9]|[12]\d|3[01])(?:er)?\s+(?:{_MONTHS})\b|\d{{4,}}\s)", re.IGNORECASE)


def _date_or_year(line: str) -> bool:
    """A line that starts with a date («31 décembre 2025 (à comparer …)») or a
    four-digit number (a title wrapped onto «2024 des plafonds …»): text, not
    section 31 or section 2024."""
    return _DATE_OR_YEAR.match(line) is not None


#: Body text under a numbered heading below which it reads as a table row.
TABLE_ROW_MAX_BODY = 40


def drop_table_rows(headings: list[Heading], lines: list[str]) -> list[Heading]:
    """Numbered "headings" that are table rows, folded back into the body.

    A PDF table flattens to lines that start with a count and a word: «1
    enfant 0,0619% 0,0516%», «2 enfants» … (the Caf EAJE barème 2025, the
    PAJE annex of instruction DSS/2B/2025/38). Read as headings, each row
    became a 25-character section of its own, cut off from the column
    headers that say which rate is the crèche one — three crèche rates were
    not_found with the barème in the corpus. A heading with almost no body
    followed by one at the same depth is a row; so is the heading that
    continues a run of rows with the same first word («10 enfants»). Only a
    bare count is a row: «1. Objet» over one short sentence is a section.
    A bare date or year is never a heading (DSS/2B/2024/181: «31 décembre
    2025 (à comparer …)» headed the family-allowance ceiling table, cut off
    from its «Plafonds de ressources … allocations familiales» title).
    Rows stay in the text of the section around them.
    """
    def body(h: Heading) -> int:
        return sum(len(line.strip()) for line in lines[h.content_start : h.content_end])

    def word(h: Heading) -> str:
        rest = _LEADING_NUM_RE.sub("", h.text, count=1).strip()
        return rest.split()[0].lower()[:5] if rest else ""

    def bare(h: Heading) -> bool:  # «1 enfant», not «1. Objet», «2.1 …» or «1) …»
        return re.match(r"\s*\d+\s", lines[h.line_idx]) is not None

    rows: set[int] = set()
    for i, h in enumerate(headings):
        if not bare(h):
            continue
        if _date_or_year(lines[h.line_idx]):
            rows.add(i)
            continue
        nxt = headings[i + 1] if i + 1 < len(headings) else None
        if (nxt is None or nxt.level <= h.level) and body(h) < TABLE_ROW_MAX_BODY:
            rows.add(i)
        elif i - 1 in rows and word(headings[i - 1]) == word(h):
            rows.add(i)
    if not rows:
        return headings
    kept = [h for i, h in enumerate(headings) if i not in rows]
    for i, h in enumerate(kept):  # a kept heading's body runs to the next kept one
        h.content_end = kept[i + 1].line_idx if i + 1 < len(kept) else len(lines)
    return kept


def slugify(text: str) -> str:
    """Fold a heading into an ltree-safe label."""
    numbering = _LEADING_NUM_RE.match(text)
    if numbering:
        return "sec_" + numbering.group(1).replace(".", "_")
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.sub(r"[^a-z0-9]+", "_", folded.lower()).strip("_").split("_")
    slug = "_".join(words[:5])[:40].strip("_")
    return slug or "sec"


def _prune_textless(units: list[UnitIR]) -> list[UnitIR]:
    """Drop units that carry no text anywhere below them.

    A heading with no body and no text-bearing children is not a legal unit:
    it produces no chunk and can never be cited, but it does put a row in the
    store with a citation string. HTML portals mint these by the handful — a
    page's <main> often wraps a search widget and a share widget whose <h2>
    titles look exactly like section headings. Iterative, so a widget's whole
    subtree goes together.
    """
    kept = list(units)
    while True:
        parents = {unit.parent_path for unit in kept if unit.parent_path}
        survivors = [unit for unit in kept if unit.versions or unit.path in parents]
        if len(survivors) == len(kept):
            return kept
        kept = survivors


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
    heading_is_body = any(compiled is HEADING_PATTERNS[name] for name in BODY_HEADING_PATTERNS)
    lines = text.splitlines()
    headings = find_headings(lines, compiled)
    if heading_is_body:
        headings = drop_table_rows(headings, lines)

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

    first_section = next((h for h in headings if h.level >= section_level), None)
    cutoff = first_section.line_idx if first_section else len(lines)
    heading_lines = {h.line_idx for h in headings}  # not table rows (drop_table_rows)
    preamble = "\n".join(line for i, line in enumerate(lines[:cutoff]) if i not in heading_lines).strip()
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

        start = heading.line_idx if heading_is_body else heading.content_start
        content = "\n".join(lines[start : heading.content_end]).strip()
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

    units = _prune_textless(units)
    surviving_parents = {unit.parent_path for unit in units if unit.parent_path}
    for unit in units:
        if unit.path in surviving_parents:
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
