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
from nomotheca_ingest.core.text import UniqueCitations, fold_accents, month_alternation

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
    # its figure). A dash may stand between number and title («2 - LE
    # COMPLÉMENT FAMILIAL», the chapter headings of a DSS instruction).
    "numbered": re.compile(r"^\s*(?P<text>(?P<number>\d+(?:\.\d+){0,4})(?:\.?\s+|\s*[-–—]\s+)[^\W\d_].*?)\s*$"),
}

#: A part heading of a numbered document: «II - LE DÉPARTEMENT DE MAYOTTE».
_PART_RE = re.compile(r"^\s*(?P<text>(?P<roman>[IVX]{1,5})\s*[-–—.]\s+[^\W\d_].*?)\s*$")
_ROMAN = {"I": 1, "V": 5, "X": 10}

#: The level of a part heading, above every numbered section (level 1 and up).
PART_LEVEL = 0

#: A heading with less text than this before its first sub-heading is a title
#: only: it gets no text of its own and is carried whole by its sub-sections.
TITLE_ONLY_MAX = 200

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
    line_idx: int  # line index of the heading itself
    content_start: int  # line index of the first body line after the heading
    content_end: int  # line index one past the last body line


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


def _roman(numeral: str) -> int:
    total = 0
    for char, nxt in zip(numeral, numeral[1:] + " ", strict=True):
        value = _ROMAN[char]
        total += -value if nxt != " " and _ROMAN[nxt] > value else value
    return total


def find_parts(lines: list[str]) -> list[Heading]:
    """The parts of a numbered document: «I - …», «II - …», in that order.

    Instruction DSS/2B/2024/181 gives the family-benefit ceilings of the
    mainland under «I - LA MÉTROPOLE, LA GUADELOUPE, …» and those of Mayotte
    under «II - LE DÉPARTEMENT DE MAYOTTE», and numbers the sections of each
    part from 1. With the part headings read as body text, Mayotte's «1.1
    Plafonds … de l'allocation de rentrée scolaire» (35 004 € for one child)
    was a root section like any other and was proposed as the national
    ceiling (28 444 €). A roman numeral is a part only in sequence — I, then
    II, then III — and only when the document has at least two: a lone «I.»
    or a «V.» out of order is an initial or a list item.
    """
    parts: list[Heading] = []
    for idx, line in enumerate(lines):
        match = _PART_RE.match(line)
        if match and _roman(match.group("roman")) == len(parts) + 1:
            parts.append(Heading(PART_LEVEL, match.group("text").strip(), idx, idx + 1, len(lines)))
    return parts if len(parts) >= 2 else []


def with_parts(headings: list[Heading], lines: list[str]) -> list[Heading]:
    """Numbered headings and part headings in document order, bodies re-cut.

    Parts are the document's top level or they are nothing: roman numerals
    that come after numbered sections («I. Première partie du calcul» in the
    worked example annexed to Cnav circular 2024/23, after its sections 1 to
    4) stay body text, or section 5 would be filed under the example.
    """
    parts = find_parts(lines)
    if not parts or any(h.line_idx < parts[0].line_idx for h in headings):
        return headings
    part_lines = {p.line_idx for p in parts}
    merged = sorted([h for h in headings if h.line_idx not in part_lines] + parts, key=lambda h: h.line_idx)
    for i, h in enumerate(merged):
        h.content_end = merged[i + 1].line_idx if i + 1 < len(merged) else len(lines)
    return merged


def _date_or_year_re(lang: str) -> re.Pattern[str]:
    """A day and a month name of the document's language (or English), or a
    year: «31 décembre 2025», «1er avril», «2024 des plafonds»."""
    months = month_alternation([lang, "en"])
    return re.compile(rf"\s*(?:(?:[1-9]|[12]\d|3[01])(?:er)?\s+(?:{months})\b|\d{{4,}}\s)", re.IGNORECASE)


def _date_or_year(line: str, lang: str = "fr") -> bool:
    """A line that starts with a date («31 décembre 2025 (à comparer …)») or a
    four-digit number (a title wrapped onto «2024 des plafonds …»): text, not
    section 31 or section 2024."""
    return _date_or_year_re(lang).match(line) is not None


#: Body text under a numbered heading below which it reads as a table row.
TABLE_ROW_MAX_BODY = 40


def drop_table_rows(headings: list[Heading], lines: list[str], lang: str = "fr") -> list[Heading]:
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
    A section numbered 0 does not exist, and a heading that repeats an
    earlier one word for word is a table's column header printed again
    (DSS/2B/2025/38: «0 à 3 ans 3 à 6 ans» headed six CMG tables; the six
    "sections" shared one citation, the loader kept the first, and the ASF,
    complément familial and ARS amounts under the third were lost).
    Bare numbers that start over are footnotes, not sections: only a first
    run reaching 2 numbers sections, every later run and a lone «1» are notes
    (Agirc-Arrco circular 2024-18 reads 1 | 1 2 3 | 1 — «1 Plafond de
    sécurité sociale.», the rate table's notes, «1 Ce qui correspond pour
    2025 …» — and its 2025 rate table became a "section 1" opening on a
    footnote, which the vector leg never ranked for the schedule it states).
    Rows stay in the text of the section around them.
    """

    def body(h: Heading) -> int:
        return sum(len(line.strip()) for line in lines[h.content_start : h.content_end])

    def word(h: Heading) -> str:
        rest = _LEADING_NUM_RE.sub("", h.text, count=1).strip()
        return rest.split()[0].lower()[:5] if rest else ""

    def bare(h: Heading) -> bool:  # «1 enfant», not «1. Objet», «2.1 …», «1) …» or «1 - TITRE»
        return re.match(r"\s*\d+\s+(?![-–—]\s)", lines[h.line_idx]) is not None

    rows: set[int] = set()
    runs: list[list[tuple[int, int]]] = []  # (heading index, number) per run of bare numbers
    for i, h in enumerate(headings):
        if bare(h):
            n = int(lines[h.line_idx].split()[0])
            if not runs or n <= runs[-1][-1][1]:
                runs.append([])
            runs[-1].append((i, n))
    for k, run in enumerate(runs):
        if k > 0 or max(n for _, n in run) < 2:
            rows.update(i for i, _ in run)
    seen_texts: set[str] = set()
    for i, h in enumerate(headings):
        repeated = h.text in seen_texts
        seen_texts.add(h.text)
        if re.match(r"\s*0+(?:\.0+)*\.?\s", lines[h.line_idx]) or (repeated and bare(h)):
            rows.add(i)
            continue
        if not bare(h):
            continue
        if _date_or_year(lines[h.line_idx], lang):
            rows.add(i)
            continue
        nxt = headings[i + 1] if i + 1 < len(headings) else None
        if ((nxt is None or nxt.level <= h.level) and body(h) < TABLE_ROW_MAX_BODY) or (
            i - 1 in rows and word(headings[i - 1]) == word(h)
        ):
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
    folded = fold_accents(text).encode("ascii", "ignore").decode()
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


@dataclass(frozen=True, slots=True)
class DocumentSpec:
    """Who a headed text is: its instrument row and its versions' provenance.

    ``version_key`` becomes every version's ``source_version_id``, which is
    what the loader deduplicates on: pass a key that changes exactly when the
    document's content changes and re-ingestion is a no-op or a new version,
    never a pile of near-duplicates. Default: ``<national_id>@<valid_from>``.
    """

    jurisdiction: str
    source_code: str
    instrument_type: str
    national_id: str
    title: str
    valid_from: date
    snapshot_id: UUID
    citation_prefix: str
    lang: str = "en"
    source_trust_class: SourceTrustClass = SourceTrustClass.EVIDENCE
    version_key: str | None = None
    metadata: dict | None = None
    eli: str | None = None

    @property
    def key(self) -> str:
        return self.version_key or f"{self.national_id}@{self.valid_from.isoformat()}"

    def versions(self, content: str, html: str | None = None) -> list[VersionIR]:
        """The one authentic version a unit holding ``content`` gets (none if empty)."""
        if not content.strip():
            return []
        return [
            VersionIR(
                valid_from=self.valid_from,
                source_version_id=self.key,
                fetch_snapshot_id=self.snapshot_id,
                texts=[TextIR(lang=self.lang, authenticity=Authenticity.AUTHENTIC, content=content, content_html=html)],
            )
        ]


def build_document(
    text: str,
    spec: DocumentSpec,
    *,
    pattern: str | re.Pattern[str] = "markdown",
    title_from_heading: bool = False,
    unit_type_by_depth: dict[int, str] | None = None,
    default_unit_type: str = "subsection",
    content_html: str | None = None,
) -> InstrumentIR:
    """Turn one headed text into a loadable InstrumentIR.

    ``title_from_heading`` claims the first level-1 heading as the document
    title (the Country Report shape, where sections start at level 2).
    Otherwise the spec's title stands — a contributed document is titled by
    the reviewer — and sections start at the shallowest heading present.

    Five steps: find the headings, settle the title and section level, the
    preamble unit, one unit per section heading, then prune and finish.
    """
    compiled = heading_pattern(pattern)
    heading_is_body = any(compiled is HEADING_PATTERNS[name] for name in BODY_HEADING_PATTERNS)
    lines = text.splitlines()
    headings = find_headings(lines, compiled)
    if heading_is_body:
        headings = with_parts(drop_table_rows(headings, lines, spec.lang), lines)

    title = spec.title
    if title_from_heading:
        title = next((h.text for h in headings if h.level == 1), title)
        section_level = 2
    else:
        section_level = min((h.level for h in headings), default=1)
    unit_types = unit_type_by_depth or {section_level: "section"}
    preamble_type = unit_types.get(section_level, "section")

    units = _preamble_units(lines, headings, section_level, spec, preamble_type)
    units += _section_units(
        lines,
        headings,
        section_level,
        spec,
        unit_types=unit_types,
        default_unit_type=default_unit_type,
        heading_is_body=heading_is_body,
        used_paths={unit.path for unit in units},
    )
    if not units:
        # No headings and no preamble is only possible for an empty document;
        # a text with no headings at all is one unit holding the whole thing.
        units = [
            UnitIR(
                unit_type=preamble_type,
                path="preamble",
                citation=f"{spec.citation_prefix}, preamble",
                versions=spec.versions(text.strip()),
            )
        ]
    units = _finish_units(units, content_html)

    return InstrumentIR(
        jurisdiction=spec.jurisdiction.upper(),
        source_code=spec.source_code,
        instrument_type=spec.instrument_type,
        source_trust_class=spec.source_trust_class,
        title={spec.lang: title},
        national_id=spec.national_id,
        eli=spec.eli,
        units=units,
        metadata=spec.metadata or {},
    )


def _preamble_units(
    lines: list[str], headings: list[Heading], section_level: int, spec: DocumentSpec, unit_type: str
) -> list[UnitIR]:
    """Whatever precedes the first section heading, as one ``preamble`` unit."""
    first_section = next((h for h in headings if h.level >= section_level), None)
    cutoff = first_section.line_idx if first_section else len(lines)
    heading_lines = {h.line_idx for h in headings}  # not table rows (drop_table_rows)
    preamble = "\n".join(line for i, line in enumerate(lines[:cutoff]) if i not in heading_lines).strip()
    if not preamble:
        return []
    return [
        UnitIR(
            unit_type=unit_type,
            path="preamble",
            citation=f"{spec.citation_prefix}, preamble",
            ordinal=0,
            versions=spec.versions(preamble),
        )
    ]


def _section_units(
    lines: list[str],
    headings: list[Heading],
    section_level: int,
    spec: DocumentSpec,
    *,
    unit_types: dict[int, str],
    default_unit_type: str,
    heading_is_body: bool,
    used_paths: set[str],
) -> list[UnitIR]:
    """One unit per heading at or below the section level, nested by level,
    with de-duplicated ltree paths and unique citations.

    Where the heading is body text (a numbered document), a section opens on
    the headings above it: «2.1 Personne seule : 1 034,28 €» says nothing
    without «2. Montant maximal de l'ASI …», and a section of part II must
    say so. A heading with no text before its first sub-heading is a title
    only — it gets no text of its own, its sub-sections carry it — and a
    section under a part is cited with the part's numeral («§II - 1.1 …»).
    """
    units: list[UnitIR] = []
    citations = UniqueCitations(max_len=200)
    stack: list[tuple[int, str, str, str]] = []  # (level, path, carried text, part numeral)
    child_counts: dict[str | None, int] = {}
    for position, heading in enumerate(headings):
        if heading.level < section_level:
            continue
        while stack and stack[-1][0] >= heading.level:
            stack.pop()
        parent_path = stack[-1][1] if stack else None
        is_part = heading_is_body and heading.level == PART_LEVEL
        part = _PART_RE.match(heading.text).group("roman") if is_part else (stack[-1][3] if stack else "")
        base = f"part_{part.lower()}" if is_part else slugify(heading.text)
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
        carried = ""
        if heading_is_body:
            nxt = headings[position + 1] if position + 1 < len(headings) else None
            title_only = nxt is not None and nxt.level > heading.level and len(content) < TITLE_ONLY_MAX
            carried = content if title_only else heading.text
            above = [entry[2] for entry in stack]
            content = "" if title_only else "\n\n".join([*above, content])
        label = f"{part} - {heading.text}" if part and not is_part else heading.text
        units.append(
            UnitIR(
                unit_type=unit_types.get(heading.level, default_unit_type),
                path=path,
                citation=citations.claim(f"{spec.citation_prefix}, §{label}"),
                ordinal=ordinal,
                parent_path=parent_path,
                versions=spec.versions(content),
                metadata={"heading_level": heading.level},
            )
        )
        stack.append((heading.level, path, carried, part))
    return units


def _finish_units(units: list[UnitIR], content_html: str | None) -> list[UnitIR]:
    """Prune text-less units, mark containers, attach the fetched page once."""
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
    return units
