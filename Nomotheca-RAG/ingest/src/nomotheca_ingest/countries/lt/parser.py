"""Parser for Lithuanian TAR Spinta JSON payloads into legislation IR.

Three payload shapes, distinguished by the source id (see ``fetcher.py``):
an act's ``Dokumentas`` row, an act's consolidation index (``Suvestine`` rows
without text), and one dated consolidation whose ``tekstas_lt`` is the full
consolidated act split here into per-article (straipsnis) units.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta
from typing import Any

from nomotheca_ingest.countries.lt.fetcher import CONSOLIDATION_INDEX_SUFFIX
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
# Seimas act numbers carry a roman-numeral term prefix (IX-1007); requiring the
# letter prefix avoids grabbing the gazette number (Žin. 2002, Nr. 73-3085).
OFFICIAL_NR_RE = re.compile(r"\bNr\.\s*([A-Z]+(?:-\d+)+)\b")


def parse_tar_json(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse archived TAR Spinta JSON bytes into a parsed document IR."""
    rows = json.loads(payload.decode("utf-8")).get("_data", [])
    if ref.source_id.endswith(CONSOLIDATION_INDEX_SUFFIX):
        return _parse_consolidation_index(rows, ref)
    if "/" in ref.source_id:
        return _parse_consolidation(rows, ref, snapshot)
    return _parse_document(rows, ref)


def _parse_document(rows: list[dict[str, Any]], ref: SourceRef) -> ParsedDoc:
    """Parse an act's Dokumentas row into an instrument skeleton."""
    if not rows:
        msg = f"TAR returned no Dokumentas row for {ref.source_id!r}"
        raise ValueError(msg)
    row = rows[0]
    dokumento_id = row.get("dokumento_id") or ref.source_id
    national_id, _ = _act_identity(dokumento_id, row.get("atv_dok_nr"))
    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type=_instrument_type(row.get("rusis")),
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
    valid_from = _parse_date(row.get("galioja_nuo")) or date.min
    valid_to_inclusive = _parse_date(row.get("galioja_iki"))
    # TAR's galioja_iki is the last day in force; the DB validity range is
    # half-open, so the exclusive end is the following day.
    valid_to = valid_to_inclusive + timedelta(days=1) if valid_to_inclusive else None

    national_id, short_citation = _act_identity(dokumento_id, _header_official_nr(text))
    units = [
        _article_unit(
            number=number,
            heading=heading,
            body=body,
            chapter=chapter,
            act_nr=national_id,
            short_citation=short_citation,
            source_version_id=f"{ref.source_id}/str_{_path_token(number)}",
            valid_from=valid_from,
            valid_to=valid_to,
            snapshot=snapshot,
            ordinal=ordinal,
        )
        for ordinal, (number, heading, body, chapter) in enumerate(_split_articles(text), start=1)
    ]
    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type="istatymas",
        national_id=national_id,
        eli=f"https://e-tar.lt/portal/lt/legalAct/{dokumento_id}",
        title={"lt": _header_title(text) or dokumento_id},
        units=units,
        metadata={"dokumento_id": dokumento_id, "suvestines_id": row.get("suvestines_id")},
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"articles": len(units)})


def _article_unit(
    *,
    number: str,
    heading: str,
    body: str,
    chapter: str | None,
    act_nr: str,
    short_citation: str,
    source_version_id: str,
    valid_from: date,
    valid_to: date | None,
    snapshot: Snapshot,
    ordinal: int,
) -> UnitIR:
    """Build the IR for one straipsnis of one dated consolidation."""
    citation = f"{short_citation} {number} straipsnis"
    return UnitIR(
        unit_type="straipsnis",
        path=f"str_{_path_token(number)}",
        citation=citation,
        ordinal=ordinal,
        national_id=f"{act_nr}-{number}",
        metadata={"skyrius": chapter} if chapter else {},
        versions=[
            VersionIR(
                valid_from=valid_from,
                valid_to=valid_to,
                source_version_id=source_version_id,
                citation_label=citation,
                fetch_snapshot_id=snapshot.id,
                texts=[TextIR(lang="lt", content=f"{number} straipsnis. {heading}\n{body}".strip())],
            )
        ],
    )


def _split_articles(text: str) -> list[tuple[str, str, str, str | None]]:
    """Split a consolidated act text into (number, heading, body, chapter) tuples."""
    chapters = [(match.start(), match.group(1)) for match in CHAPTER_RE.finditer(text)]
    matches = list(ARTICLE_RE.finditer(text))
    articles: list[tuple[str, str, str, str | None]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = _normalize_space(text[match.end() : end])
        chapter = None
        for position, label in chapters:
            if position < match.start():
                chapter = label
        articles.append((match.group(1), match.group(2).strip(), body, chapter))
    return articles


def _act_identity(dokumento_id: str, official_nr: str | None) -> tuple[str, str]:
    """Return (official number, short citation label) for an act."""
    known = KNOWN_ACTS.get(dokumento_id)
    if known:
        return (official_nr or known[0], known[1])
    number = official_nr or dokumento_id
    return (number, number)


def _header_official_nr(text: str) -> str | None:
    """Extract the official act number (e.g. IX-1007) from a consolidation header."""
    match = OFFICIAL_NR_RE.search(text[:2000])
    return match.group(1) if match else None


def _header_title(text: str) -> str | None:
    """Extract the act title from the uppercase block heading a consolidation."""
    lines = []
    for line in text.splitlines()[:40]:
        stripped = line.strip()
        if not stripped or stripped.startswith("Suvestinė") or stripped.startswith("Įstatymas paskelbtas"):
            continue
        if stripped != stripped.upper():
            break
        lines.append(stripped)
    return " ".join(lines).strip() or None


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
