"""EUROMOD Country Report ingestion — a separate, non-legislative corpus class.

Country Reports describe the EUROMOD model itself, so they must never become
citable evidence for parameter proposals: everything loaded here is tagged
``instrument_type='country_report'`` and the Nomoscope evidence retrieval
excludes that type. The corpus exists so the frame/scout steps and the
validation UI can search it (parameter acronym -> semantic description),
with the same FTS/vector machinery as the legislation corpus.

File-based: the "fetch" is reading a Markdown file already converted from the
official Word/PDF report, archived as a fetch_snapshot like any other source.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from pathlib import Path
from uuid import UUID

import psycopg

from nomotheca_ingest.core.db import create_fetch_run, finish_fetch_run
from nomotheca_ingest.core.ir import (
    Authenticity,
    InstrumentIR,
    ParsedDoc,
    SourceRef,
    TextIR,
    Trigger,
    UnitIR,
    VersionIR,
)
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats

INSTRUMENT_TYPE = "country_report"
ID_SYSTEM = "euromod_cr"
SKILL_VERSION = "cr-md-0.1"

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_LEADING_NUM_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s")
_UNIT_TYPE_BY_DEPTH = {2: "section"}


@dataclass(slots=True)
class _Heading:
    level: int
    text: str
    line_idx: int       # line index of the heading itself
    content_start: int  # line index of first body line after the heading
    content_end: int    # line index one past the last body line


def source_code_for(jurisdiction: str) -> str:
    """Source registry code for a jurisdiction's Country Report corpus."""
    return f"{jurisdiction.upper()}-EUROMOD-CR"


def _slugify(text: str) -> str:
    """Fold a heading into an ltree-safe label."""
    numbering = _LEADING_NUM_RE.match(text)
    if numbering:
        return "sec_" + numbering.group(1).replace(".", "_")
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.sub(r"[^a-z0-9]+", "_", folded.lower()).strip("_").split("_")
    slug = "_".join(words[:5])[:40].strip("_")
    return slug or "sec"


def _headings(lines: list[str]) -> list[_Heading]:
    """Locate markdown headings outside fenced code blocks, with body spans."""
    found: list[_Heading] = []
    in_fence = False
    for idx, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = _HEADING_RE.match(line)
        if match:
            if found:
                found[-1].content_end = idx
            found.append(
                _Heading(
                    level=len(match.group(1)),
                    text=match.group(2),
                    line_idx=idx,
                    content_start=idx + 1,
                    content_end=len(lines),
                )
            )
    return found


def parse_country_report(
    markdown: str,
    jurisdiction: str,
    vintage: str,
    source_code: str,
    valid_from: date,
    snapshot_id: UUID,
    lang: str = "en",
) -> InstrumentIR:
    """Convert one Country Report Markdown file into a loadable InstrumentIR.

    Every heading becomes a legal_unit; the text between a heading and the
    next heading (of any level) is that unit's own content. Hierarchy follows
    markdown levels only — the CRs' decimal numbering is not trusted (the FR
    report reuses '2.' for two different chapters).
    """
    jurisdiction = jurisdiction.upper()
    national_id = f"CR-{jurisdiction}-{vintage}"
    lines = markdown.splitlines()
    headings = _headings(lines)

    title_text = next(
        (h.text for h in headings if h.level == 1),
        f"EUROMOD Country Report {jurisdiction} {vintage}",
    )

    def make_version(content: str) -> list[VersionIR]:
        if not content.strip():
            return []
        return [
            VersionIR(
                valid_from=valid_from,
                source_version_id=f"{national_id}@{valid_from.isoformat()}",
                fetch_snapshot_id=snapshot_id,
                texts=[TextIR(lang=lang, authenticity=Authenticity.AUTHENTIC, content=content)],
            )
        ]

    units: list[UnitIR] = []
    used_paths: set[str] = set()
    # (level, path) ancestor stack; preamble text (before any h2) gets its own unit.
    stack: list[tuple[int, str]] = []
    child_counts: dict[str | None, int] = {}
    has_children: set[str] = set()

    first_section = next((h for h in headings if h.level >= 2), None)
    cutoff = first_section.line_idx if first_section else len(lines)
    preamble = "\n".join(line for line in lines[:cutoff] if not _HEADING_RE.match(line)).strip()
    if preamble:
        units.append(
            UnitIR(
                unit_type="section",
                path="preamble",
                citation=f"CR {jurisdiction} {vintage}, preamble",
                ordinal=0,
                versions=make_version(preamble),
            )
        )
        used_paths.add("preamble")

    for h in headings:
        if h.level < 2:
            continue
        while stack and stack[-1][0] >= h.level:
            stack.pop()
        parent_path = stack[-1][1] if stack else None
        base = _slugify(h.text)
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

        content = "\n".join(lines[h.content_start : h.content_end]).strip()
        units.append(
            UnitIR(
                unit_type=_UNIT_TYPE_BY_DEPTH.get(h.level, "subsection"),
                path=path,
                citation=f"CR {jurisdiction} {vintage}, §{h.text}"[:200],
                ordinal=ordinal,
                parent_path=parent_path,
                versions=make_version(content),
                metadata={"heading_level": h.level},
            )
        )
        stack.append((h.level, path))

    for unit in units:
        if unit.path in has_children:
            unit.is_container = True

    return InstrumentIR(
        jurisdiction=jurisdiction,
        source_code=source_code,
        instrument_type=INSTRUMENT_TYPE,
        title={lang: title_text},
        national_id=national_id,
        units=units,
        metadata={"vintage": vintage, "corpus_class": INSTRUMENT_TYPE},
    )


def _ensure_source(conn: psycopg.Connection, jurisdiction: str, source_code: str) -> None:
    """Idempotently register the per-country EUROMOD-CR source row."""
    row = conn.execute(
        "SELECT id FROM jurisdictions WHERE code = %s", (jurisdiction,)
    ).fetchone()
    if row is None:
        msg = f"Unknown jurisdiction: {jurisdiction} (seed it before ingesting its CR)"
        raise ValueError(msg)
    conn.execute(
        """
        INSERT INTO sources (jurisdiction_id, code, name, id_system, fetch_skill, terms)
        VALUES (%s, %s, %s, %s, 'core/country_reports',
                '{"note": "non-legislative corpus: excluded from evidence retrieval"}'::jsonb)
        ON CONFLICT (code) DO NOTHING
        """,
        (row[0], source_code, f"EUROMOD Country Report ({jurisdiction})", ID_SYSTEM),
    )


def _write_file_snapshot(
    conn: psycopg.Connection, run_id: UUID, source_code: str, path: Path, content: bytes
) -> UUID:
    """Archive the Markdown file bytes as the version's provenance snapshot."""
    row = conn.execute(
        """
        INSERT INTO fetch_snapshots (run_id, source_id, url, content_type, content_hash, raw_content)
        VALUES (%s, (SELECT id FROM sources WHERE code = %s), %s, 'text/markdown', %s, %s)
        RETURNING id
        """,
        (run_id, source_code, path.resolve().as_uri(), sha256(content).hexdigest(), content),
    ).fetchone()
    return row[0]


def ingest_country_report(
    path: str | Path,
    jurisdiction: str,
    database_url: str,
    *,
    vintage: str = "Y16",
    valid_from: date = date(2022, 1, 1),
    lang: str = "en",
) -> LoadStats:
    """Load one Country Report Markdown file into the legislation DB.

    Idempotent: re-running updates texts and regenerates chunks in place
    (versions are deduplicated on source_version_id).
    """
    file_path = Path(path)
    raw = file_path.read_bytes()
    jurisdiction = jurisdiction.upper()
    source_code = source_code_for(jurisdiction)

    with psycopg.connect(database_url) as conn:
        _ensure_source(conn, jurisdiction, source_code)
        run_id = create_fetch_run(conn, source_code, SKILL_VERSION, Trigger.BULK_SEED)
        try:
            snapshot_id = _write_file_snapshot(conn, run_id, source_code, file_path, raw)
            instrument = parse_country_report(
                raw.decode("utf-8"), jurisdiction, vintage, source_code, valid_from, snapshot_id, lang
            )
            ref = SourceRef(
                jurisdiction=jurisdiction,
                source_code=source_code,
                source_id=instrument.national_id or file_path.name,
                source_type=INSTRUMENT_TYPE,
            )
            stats = LegislationLoader(conn).load(ParsedDoc(ref=ref, instruments=[instrument]))
            finish_fetch_run(
                conn,
                run_id,
                "succeeded",
                {
                    "trigger": Trigger.BULK_SEED.value,
                    "file": file_path.name,
                    "instruments": stats.instruments,
                    "units": stats.units,
                    "versions": stats.versions,
                    "texts": stats.texts,
                    "chunks": stats.chunks,
                },
            )
        except Exception as exc:
            finish_fetch_run(conn, run_id, "failed", {"trigger": Trigger.BULK_SEED.value, "error": str(exc)})
            raise
    return stats
