"""Parser for Lithuanian TAR Spinta JSON payloads into legislation IR.

Three payload shapes, distinguished by the source id (see ``fetcher.py``):
an act's ``Dokumentas`` row, an act's consolidation index (``Suvestine`` rows
without text), and one dated consolidation whose ``tekstas_lt`` is the full
consolidated act split here into per-article (straipsnis) units — or, for a
resolution or an order, which have no articles, into its numbered points (punktai).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

from nomotheca_ingest.countries.lt.fetcher import CONSOLIDATION_INDEX_SUFFIX, ORIGINAL_TEXT_SUFFIX
from nomotheca_ingest.core.ir import InstrumentIR, ParsedDoc, Snapshot, SourceRef, TextIR, UnitIR, VersionIR


# Consolidations whose validity ended before this date are skipped at expansion
# time: TAR keeps every consolidation since 2014, EUROMOD needs the 2022+ window.
EUROMOD_WINDOW_START = date(2022, 1, 1)

# Official-number and short-citation aliases for the acts EUROMOD LT cites most.
# Keyed by dokumento_id; used for citations when the text header lacks a number.
KNOWN_ACTS: dict[str, tuple[str, str]] = {
    "TAR.C677663D2202": ("IX-1007", "GPMĮ"),
    "TAR.0F9036415DBD": ("I-1336", "VSDĮ"),
    "TAR.068516AF734B": ("IX-110", "LMSDĮ"),
    "TAR.1DEDD43B92AE": ("I-621", "IVĮ"),
    "TAR.3EEE59417F13": ("IX-1675", "PSPĮ"),
    "TAR.FDF42614DE52": ("IX-1904", "NSDĮ"),
}

ARTICLE_RE = re.compile(r"^(\d+(?:-\d+)*)\s+straipsnis\.\s*(.*)$", re.MULTILINE)
CHAPTER_RE = re.compile(r"^([IVXLC]+(?:-[IVXLC]+)*)\s+SKYRIUS\s*$", re.MULTILINE)
# The act's own number sits on the enactment line ("2003 m. liepos 1 d. Nr. IX-1675").
# Anchoring on that line skips both gazette numbers (Žin. 2002, Nr. 73-3085) and
# "Nauja redakcija" notes citing amending acts (Nr. XI-1772, ...), which appear first.
OFFICIAL_NR_RE = re.compile(r"^\d{4}\s+m\..*?\bNr\.\s*([A-Z]+(?:-\d+)+)\b", re.MULTILINE)
# The same enactment line for any act: date, then whatever number it carries ("709", "A1-835").
ENACTMENT_RE = re.compile(r"^(\d{4}\s+m\.\s+\S+\s+\d{1,2}\s+d\.)\s+Nr\.\s*(\S+)", re.MULTILINE)
# A top-level point of a resolution or an order: "1. Patvirtinti …" (not "1.1." nor "1)").
POINT_RE = re.compile(r"^(\d+)\.[ \t\xa0]+(?=\S)", re.MULTILINE)
# Header words naming an act that is not a law; each is a line of its own.
ACT_KINDS = frozenset({"nutarimas", "įsakymas", "sprendimas", "potvarkis"})
NON_LAW_TYPES = frozenset({"nutarimas", "isakymas", "sprendimas", "potvarkis"})


def parse_tar_json(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse archived TAR Spinta JSON bytes into a parsed document IR."""
    rows = json.loads(payload.decode("utf-8")).get("_data", [])
    if ref.source_id.endswith(CONSOLIDATION_INDEX_SUFFIX):
        return _parse_consolidation_index(rows, ref)
    if "/" in ref.source_id:
        # A Suvestinė row, or — ``/orig`` — the Dokumentas row of a never-amended
        # act standing in for its single version (same columns for the text).
        return _parse_consolidation(rows, ref, snapshot)
    return _parse_document(rows, ref)


def _parse_document(rows: list[dict[str, Any]], ref: SourceRef) -> ParsedDoc:
    """Parse an act's Dokumentas row into an instrument skeleton."""
    if not rows:
        msg = f"TAR returned no Dokumentas row for {ref.source_id!r}"
        raise ValueError(msg)
    row = rows[0]
    dokumento_id = row.get("dokumento_id") or ref.source_id
    instrument_type = _instrument_type(row.get("rusis"))
    national_id, _ = _act_identity(dokumento_id, row.get("atv_dok_nr"), instrument_type)
    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type=instrument_type,
        national_id=national_id,
        eli=row.get("nuoroda"),
        title={"lt": row.get("pavadinimas") or dokumento_id},
        adoption_date=_parse_date(row.get("priimtas")),
        publication_date=_parse_date(row.get("paskelbta_tar")),
        metadata={
            "dokumento_id": dokumento_id,
            "tar_kodas": row.get("tar_kodas"),
            "galioj_busena": row.get("galioj_busena"),
        },
    )
    child_refs = [
        {
            "source_id": f"{dokumento_id}{CONSOLIDATION_INDEX_SUFFIX}",
            "source_type": "consolidation_index",
            "title": "suvestinės redakcijos",
        }
    ]
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"child_refs": child_refs})


def _parse_consolidation_index(rows: list[dict[str, Any]], ref: SourceRef) -> ParsedDoc:
    """Expose an act's dated consolidations overlapping the EUROMOD window."""
    dokumento_id = ref.source_id.removesuffix(CONSOLIDATION_INDEX_SUFFIX)
    child_refs: list[dict[str, str]] = []
    skipped = 0
    if not rows:
        # Never amended, never consolidated: the act's text is on its own
        # Dokumentas row, in force from `isigalioja`.
        child_refs.append(
            {
                "source_id": f"{dokumento_id}{ORIGINAL_TEXT_SUFFIX}",
                "source_type": "consolidation",
                "title": "pradinė redakcija (nekonsoliduotas aktas)",
            }
        )
    for row in rows:
        suvestines_id = row.get("suvestines_id")
        if not suvestines_id:
            continue
        valid_to = _parse_date(row.get("galioja_iki"))
        if valid_to is not None and valid_to < EUROMOD_WINDOW_START:
            skipped += 1
            continue
        child_refs.append(
            {
                "source_id": f"{dokumento_id}/{suvestines_id}",
                "source_type": "consolidation",
                "title": f"suvestinė redakcija nuo {row.get('galioja_nuo')}",
            }
        )
    return ParsedDoc(
        ref=ref,
        metadata={"child_refs": child_refs, "skipped_before_window": skipped},
    )


def _parse_consolidation(rows: list[dict[str, Any]], ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Split one consolidated act text into per-article units and versions."""
    if not rows:
        msg = f"TAR returned no Suvestine row for {ref.source_id!r}"
        raise ValueError(msg)
    row = rows[0]
    dokumento_id = row.get("dokumento_id") or ref.source_id.split("/", 1)[0]
    text = row.get("tekstas_lt") or ""
    # Suvestinė rows date themselves with galioja_nuo/galioja_iki; a Dokumentas
    # row standing in for a never-consolidated act with isigalioja/negalioja.
    valid_from = _parse_date(row.get("galioja_nuo") or row.get("isigalioja")) or date.min
    valid_to_inclusive = _parse_date(row.get("galioja_iki") or row.get("negalioja"))
    # TAR's galioja_iki is the last day in force; the DB validity range is
    # half-open, so the exclusive end is the following day.
    valid_to = valid_to_inclusive + timedelta(days=1) if valid_to_inclusive else None

    # A Dokumentas row (``/orig``) says what the act is; a Suvestinė row does not,
    # and its header does ("nutarimas", "įsakymas" on a line of their own).
    instrument_type = _instrument_type(row.get("rusis") or _header_kind(text))
    national_id, short_citation = _act_identity(dokumento_id, _header_official_nr(text), instrument_type)
    if instrument_type in NON_LAW_TYPES:
        short_citation = _header_enactment(text) or short_citation
    units = [
        _section_unit(
            section,
            act_nr=national_id,
            short_citation=short_citation,
            source_version_id=f"{ref.source_id}/{section.path}",
            valid_from=valid_from,
            valid_to=valid_to,
            snapshot=snapshot,
            ordinal=ordinal,
        )
        for ordinal, section in enumerate(_split_sections(text), start=1)
    ]
    if instrument_type in NON_LAW_TYPES:
        # Its header opens with the issuer («LIETUVOS RESPUBLIKOS VYRIAUSYBĖ»), not a title.
        title = row.get("pavadinimas") or _header_subject(text) or dokumento_id
    else:
        title = _header_title(text) or row.get("pavadinimas") or dokumento_id
    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type=instrument_type,
        national_id=national_id,
        eli=f"https://e-tar.lt/portal/lt/legalAct/{dokumento_id}",
        title={"lt": title},
        units=units,
        metadata={"dokumento_id": dokumento_id, "suvestines_id": row.get("suvestines_id")},
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"articles": len(units)})


@dataclass(frozen=True)
class _Section:
    """One citable piece of an act: a straipsnis, a punktas, a preamble, or the whole text."""

    unit_type: str
    path: str
    label: str  # appended to the act's short citation; "" for the whole text
    content: str
    number: str | None = None
    chapter: str | None = None


def _section_unit(
    section: _Section,
    *,
    act_nr: str,
    short_citation: str,
    source_version_id: str,
    valid_from: date,
    valid_to: date | None,
    snapshot: Snapshot,
    ordinal: int,
) -> UnitIR:
    """Build the IR for one section of one dated consolidation."""
    citation = f"{short_citation} {section.label}".strip()
    return UnitIR(
        unit_type=section.unit_type,
        path=section.path,
        citation=citation,
        ordinal=ordinal,
        national_id=f"{act_nr}-{section.number}" if section.number else f"{act_nr}-{section.path}",
        metadata={"skyrius": section.chapter} if section.chapter else {},
        versions=[
            VersionIR(
                valid_from=valid_from,
                valid_to=valid_to,
                source_version_id=source_version_id,
                citation_label=citation,
                fetch_snapshot_id=snapshot.id,
                texts=[TextIR(lang="lt", content=section.content)],
            )
        ],
    )


def _split_sections(text: str) -> list[_Section]:
    """Split an act text into its straipsniai — or, for a resolution or an order,
    which have none, into its numbered punktai, else into one whole-text unit.

    A Government resolution states the year's amount in a point («1. Patvirtinti
    2025 metais taikomą … minimaliąją mėnesinę algą – 1038 eurus.»); split on
    articles alone it had no unit, and the instrument loaded as an empty shell.
    """
    articles = _split_articles(text)
    if articles:
        return articles
    points = _split_points(text)
    if points:
        return points
    content = _normalize_space(text)
    return [_Section("tekstas", "tekstas", "", content)] if content else []


def _split_articles(text: str) -> list[_Section]:
    """Split a consolidated act text into its straipsniai."""
    chapters = [(match.start(), match.group(1)) for match in CHAPTER_RE.finditer(text)]
    matches = list(ARTICLE_RE.finditer(text))
    articles: list[_Section] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = _normalize_space(text[match.end() : end])
        chapter = None
        for position, label in chapters:
            if position < match.start():
                chapter = label
        number, heading = match.group(1), match.group(2).strip()
        articles.append(
            _Section(
                unit_type="straipsnis",
                path=f"str_{_path_token(number)}",
                label=f"{number} straipsnis",
                content=f"{number} straipsnis. {heading}\n{body}".strip(),
                number=number,
                chapter=chapter,
            )
        )
    return articles


def _split_points(text: str) -> list[_Section]:
    """Split a resolution's or an order's text into its top-level numbered points.

    Only the first run 1, 2, 3, … counts: a number out of sequence (an annex
    numbering its own points from 1, a "2.1." sub-point) stays in the body of the
    point before it, so every punktas citation is unique. The text before point 1
    (issuer, title, date and number, the legal basis «Vadovaudamasi … nutaria:»)
    is its own preamble unit.
    """
    starts: list[re.Match[str]] = []
    for match in POINT_RE.finditer(text):
        if int(match.group(1)) == len(starts) + 1:
            starts.append(match)
    if not starts:
        return []
    sections: list[_Section] = []
    preamble = _normalize_space(text[: starts[0].start()])
    if preamble:
        sections.append(_Section("preambule", "preambule", "preambulė", preamble))
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        number = match.group(1)
        sections.append(
            _Section(
                unit_type="punktas",
                path=f"pkt_{number}",
                label=f"{number} punktas",
                content=_normalize_space(text[match.start() : end]),
                number=number,
            )
        )
    return sections


def _act_identity(dokumento_id: str, official_nr: str | None, instrument_type: str = "istatymas") -> tuple[str, str]:
    """Return (official number, short citation label) for an act.

    For known acts the curated number always wins: the document row and each
    consolidation must resolve to the same national_id or the loader inserts
    duplicate instruments (and trips the unique eli constraint). Only a law's
    number (IX-1007) is unique across the register: a resolution's «Nr. 709» or
    a ministry's «Nr. V-524» is not, so any other act keeps its dokumento_id.
    """
    known = KNOWN_ACTS.get(dokumento_id)
    if known:
        return known
    number = (None if instrument_type in NON_LAW_TYPES else official_nr) or dokumento_id
    return (number, number)


def _header_official_nr(text: str) -> str | None:
    """Extract the official act number (e.g. IX-1007) from a consolidation header."""
    match = OFFICIAL_NR_RE.search(text[:2000])
    return match.group(1) if match else None


def _header_kind(text: str) -> str | None:
    """Read the act kind from the header line that names it ("nutarimas", "ĮSAKYMAS")."""
    for line in text.splitlines()[:40]:
        word = line.replace("\xa0", " ").strip().lower()
        if word in ACT_KINDS:
            return word
    return None


def _header_enactment(text: str) -> str | None:
    """Cite a resolution or an order as Lithuanian lawyers do: «2024 m. rugpjūčio 28 d. nutarimas Nr. 709»."""
    match = ENACTMENT_RE.search(text[:2000])
    kind = _header_kind(text)
    if not match or not kind:
        return None
    return f"{match.group(1)} {kind} Nr. {match.group(2)}"


def _header_subject(text: str) -> str | None:
    """The «DĖL …» title of a resolution or an order, which may run over several
    lines and be in mixed case («DĖL socialinės paramos … rodiklių / DYDŽIŲ PATVIRTINIMO»)."""
    lines = [line.replace("\xa0", " ").strip() for line in text.splitlines()[:40]]
    for index, line in enumerate(lines):
        if line.upper().startswith("DĖL "):
            title = [line]
            for following in lines[index + 1 :]:
                if not following or ENACTMENT_RE.match(following):
                    break
                title.append(following)
            return " ".join(title)
    return None


def _header_title(text: str) -> str | None:
    """Extract the act title: an uppercase block starting "LIETUVOS RESPUBLIKOS".

    Editorial notes precede it (gazette reference, "Nauja redakcija" amendments),
    and some acts open with a stray lone "LIETUVOS RESPUBLIKOS" line before those
    notes — so collect every candidate block and prefer the one that actually
    ends with the act-type word ("… ĮSTATYMAS").
    """
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines()[:80]:
        stripped = line.replace("\xa0", " ").strip()
        uppercase = bool(stripped) and stripped == stripped.upper()
        if current is None:
            if uppercase and stripped.startswith("LIETUVOS RESPUBLIKOS"):
                current = [stripped]
        elif uppercase:
            current.append(stripped)
        else:
            blocks.append(current)
            current = None
    if current:
        blocks.append(current)
    for block in blocks:
        if block[-1].endswith("ĮSTATYMAS"):
            return " ".join(block)
    return " ".join(max(blocks, key=len)) if blocks else None


def _instrument_type(rusis: str | None) -> str:
    """Normalize a TAR document type into an ASCII instrument_type value."""
    mapping = {"įstatymas": "istatymas", "nutarimas": "nutarimas", "įsakymas": "isakymas"}
    if not rusis:
        return "istatymas"
    return mapping.get(rusis.lower(), _path_token(rusis))


def _parse_date(value: str | None) -> date | None:
    """Parse a Spinta date or datetime string into a date."""
    if not value:
        return None
    return datetime.fromisoformat(value).date()


def _path_token(value: str) -> str:
    """Sanitize a label into an ltree-compatible path token."""
    token = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return token or "unknown"


def _normalize_space(value: str) -> str:
    """Collapse the register's triple blank lines while keeping paragraphs."""
    return re.sub(r"\n{3,}", "\n\n", value).strip()
