"""Contributed documents: a reviewer hands over a URL or a file, we ingest it.

A country adapter can only ingest what a national portal keys by a national
id. Much of what actually fixes a EUROMOD value is not there at all: a Unedic
circular, a BOFiP doctrine page, a ministerial arrete a reviewer saved as PDF.
This module is the path for those — one library function behind the CLI, the
TUI and the validation UI, so a future cache-miss workflow can contribute a
document with no UI in sight.

The rules that matter (ADR 0001, and the spec's Implementation Decisions):

* **Archive first.** The raw bytes are written to a fetch snapshot with their
  content type, origin and sha256 before anything is parsed.
* **Identity is the document, not the run.** A URL keys the instrument on its
  canonical form (fragment dropped), so the same BOFiP page linked with two
  anchors is one instrument; an uploaded file keys on ``file:<sha256>``.
* **Trust follows the kind, mechanically.** The reviewer names the kind in
  their own country's words; the source-trust class is derived, and "other"
  is never granted evidence-level trust.
* **No invented dates.** A missing validity start is refused, not guessed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit, urlunsplit
from uuid import UUID

import psycopg

from nomotheca_ingest.core import extract
from nomotheca_ingest.core.db import PostgresSnapshotStore, create_fetch_run, finish_fetch_run
from nomotheca_ingest.core.documents import build_document
from nomotheca_ingest.core.ir import (
    InstrumentRelationIR,
    ParsedDoc,
    SourceRef,
    SourceTrustClass,
    Trigger,
)
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats
from nomotheca_ingest.core.routing import RouteOutcome
from nomotheca_ingest.core.snapshots import USER_AGENT

ID_SYSTEM = "contributed"
SOURCE_TYPE = "contributed_document"
SKILL_VERSION = "contrib-0.1"
IMPLEMENTS_RELATION = "implements"


class NormLevel(StrEnum):
    """Where a document sits in the hierarchy of norms.

    The level is the country-neutral fact; the label a reviewer picks from is
    their own country's word for it (see `KINDS_BY_JURISDICTION`).
    """

    STATUTE = "statute"
    GOVERNMENT_REGULATION = "government_regulation"
    MINISTERIAL_ORDER = "ministerial_order"
    ADMINISTRATIVE_GUIDANCE = "administrative_guidance"
    OTHER = "other"


#: Source-trust class per level (ADR 0001). Everything with statute-level
#: authority is evidence; guidance and — deliberately — "other" are guidance,
#: so an unnamed document can never be granted evidence-level trust by
#: accident.
TRUST_CLASS_BY_LEVEL: dict[NormLevel, SourceTrustClass] = {
    NormLevel.STATUTE: SourceTrustClass.EVIDENCE,
    NormLevel.GOVERNMENT_REGULATION: SourceTrustClass.EVIDENCE,
    NormLevel.MINISTERIAL_ORDER: SourceTrustClass.EVIDENCE,
    NormLevel.ADMINISTRATIVE_GUIDANCE: SourceTrustClass.GUIDANCE,
    NormLevel.OTHER: SourceTrustClass.GUIDANCE,
}

#: The kinds a reviewer may state, in their own country's words, in hierarchy
#: order. One table, so the CLI, the UI select and the trust mapping cannot
#: drift apart. A jurisdiction with no entry falls back to `DEFAULT`.
KINDS_BY_JURISDICTION: dict[str, tuple[tuple[str, NormLevel], ...]] = {
    "FR": (
        ("loi", NormLevel.STATUTE),
        ("decret", NormLevel.GOVERNMENT_REGULATION),
        ("arrete", NormLevel.MINISTERIAL_ORDER),
        ("circulaire", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("doctrine", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    ),
    "ES": (
        ("ley", NormLevel.STATUTE),
        ("real_decreto", NormLevel.GOVERNMENT_REGULATION),
        ("orden", NormLevel.MINISTERIAL_ORDER),
        ("circular", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("consulta_vinculante", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    ),
    "NL": (
        ("wet", NormLevel.STATUTE),
        ("algemene_maatregel_van_bestuur", NormLevel.GOVERNMENT_REGULATION),
        ("ministeriele_regeling", NormLevel.MINISTERIAL_ORDER),
        ("beleidsregel", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("besluit", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    ),
    "IE": (
        ("act", NormLevel.STATUTE),
        ("statutory_instrument", NormLevel.GOVERNMENT_REGULATION),
        ("regulation", NormLevel.MINISTERIAL_ORDER),
        ("tax_and_duty_manual", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("guidance", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    ),
    "LT": (
        ("istatymas", NormLevel.STATUTE),
        ("nutarimas", NormLevel.GOVERNMENT_REGULATION),
        ("isakymas", NormLevel.MINISTERIAL_ORDER),
        ("isaiskinimas", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("komentaras", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    ),
    "DEFAULT": (
        ("law", NormLevel.STATUTE),
        ("regulation", NormLevel.GOVERNMENT_REGULATION),
        ("ministerial_order", NormLevel.MINISTERIAL_ORDER),
        ("guidance", NormLevel.ADMINISTRATIVE_GUIDANCE),
        ("other", NormLevel.OTHER),
    ),
}


@dataclass(slots=True)
class DocumentResult:
    """What one contributed-document run did."""

    jurisdiction: str
    source_code: str
    national_id: str
    kind: str
    source_trust_class: SourceTrustClass
    content_hash: str
    origin: str
    #: 'contributed', or 'adapter' when the URL turned out to belong to a
    #: known official source and the legislation ingester ran instead.
    routed_to: str = "contributed"
    #: True when the same document, byte-for-byte, was already in the store:
    #: the run archived the bytes and stopped, so duplicates never pile up.
    already_present: bool = False
    units: int = 0
    versions: int = 0
    texts: int = 0
    chunks: int = 0
    fetch_run_id: UUID | None = None
    snapshot_id: UUID | None = None
    implements: str | None = None


def source_code_for(jurisdiction: str) -> str:
    """Source registry code for a jurisdiction's contributed documents."""
    return f"{jurisdiction.upper()}-CONTRIB"


def _ingest_through_adapter(
    outcome: RouteOutcome, database_url: str, max_items: int
) -> DocumentResult:
    """Hand a known official source to the existing legislation ingester."""
    from nomotheca_ingest.core.pipeline import run_database_ingest

    pipeline_result = run_database_ingest(
        jurisdiction=outcome.jurisdiction,
        identifier=outcome.national_id,
        database_url=database_url,
        mode="instrument",
        max_items=max_items,
    )
    return DocumentResult(
        jurisdiction=outcome.jurisdiction,
        source_code=outcome.source_name or "",
        national_id=outcome.national_id,
        kind="",
        source_trust_class=SourceTrustClass.EVIDENCE,
        content_hash="",
        origin=outcome.url,
        routed_to="adapter",
        units=sum(item.units for item in pipeline_result.loaded),
        versions=sum(item.versions for item in pipeline_result.loaded),
        texts=sum(item.texts for item in pipeline_result.loaded),
        chunks=sum(item.chunks for item in pipeline_result.loaded),
        fetch_run_id=pipeline_result.run_id,
    )


def route(url: str, database_url: str | None = None) -> RouteOutcome:
    """Classify a URL, resolving Legifrance ELI URLs through the FR resolver."""
    from nomotheca_ingest.core import routing
    from nomotheca_ingest.countries.fr.resolver import resolve_legifrance_url

    return routing.route_url(
        url,
        resolve_legifrance=lambda target: resolve_legifrance_url(
            target, database_url=database_url
        ),
    )


def kinds_for(jurisdiction: str) -> dict[str, NormLevel]:
    """The kinds a reviewer may state for a jurisdiction, label -> level."""
    table = KINDS_BY_JURISDICTION.get(jurisdiction.upper(), KINDS_BY_JURISDICTION["DEFAULT"])
    return dict(table)


def norm_level_for(jurisdiction: str, kind: str) -> NormLevel:
    """Where a stated kind sits in the hierarchy of norms."""
    kinds = kinds_for(jurisdiction)
    try:
        return kinds[kind]
    except KeyError:
        allowed = ", ".join(kinds)
        msg = f"Unknown kind {kind!r} for {jurisdiction.upper()} (known: {allowed})"
        raise ValueError(msg) from None


def trust_class_for(jurisdiction: str, kind: str) -> SourceTrustClass:
    """Source-trust class of a stated kind — derived, never stated directly."""
    return TRUST_CLASS_BY_LEVEL[norm_level_for(jurisdiction, kind)]


def canonical_url(url: str) -> str:
    """One URL per document: lowercased scheme and host, no fragment.

    BOFiP links the same page with different anchors and Legifrance with a
    trailing slash; without this they would become several instruments of the
    same text, each with its own chunks competing in retrieval.
    """
    parts = urlsplit(url.strip())
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def content_hash(raw: bytes) -> str:
    """The sha256 that decides "already present" and keys the version."""
    return sha256(raw).hexdigest()


def national_id_for(raw: bytes, url: str | None = None) -> str:
    """Stable identity of a contributed document.

    A URL identifies the document wherever it was fetched from; an upload has
    only its bytes, so it is keyed by them.
    """
    return canonical_url(url) if url else f"file:{content_hash(raw)}"


def parse_document(
    raw: bytes,
    *,
    content_type: str,
    jurisdiction: str,
    lang: str,
    title: str,
    kind: str,
    valid_from: date,
    source_code: str,
    national_id: str,
    origin: str,
    snapshot_id: UUID,
    implements: str | None = None,
) -> ParsedDoc:
    """Turn archived bytes plus the reviewer's fields into loadable IR.

    Pure: no network, no database. This is the seam the parse tests exercise.
    """
    if valid_from is None:  # pragma: no cover - guarded by ingest_document too
        msg = "A contributed document needs the date it is in force from"
        raise ValueError(msg)

    jurisdiction = jurisdiction.upper()
    trust_class = trust_class_for(jurisdiction, kind)
    extracted = extract.extract(raw, content_type)
    digest = content_hash(raw)

    instrument = build_document(
        text=extracted.text,
        jurisdiction=jurisdiction,
        source_code=source_code,
        instrument_type=kind,
        source_trust_class=trust_class,
        national_id=national_id,
        title=title,
        lang=lang,
        valid_from=valid_from,
        snapshot_id=snapshot_id,
        citation_prefix=title[:120],
        pattern=extracted.pattern,
        # Content, not the date, decides identity of a version: re-adding the
        # same bytes reuses the version, a changed page opens a new one and
        # the loader closes the previous (see LegislationLoader._chain_versions).
        version_key=f"{national_id}@{digest[:16]}",
        content_html=extracted.html,
        metadata={
            "contributed": True,
            "kind": kind,
            "norm_level": norm_level_for(jurisdiction, kind).value,
            "content_hash": digest,
            "content_type": content_type,
            "origin": origin,
        },
    )
    relations = []
    if implements:
        relations.append(
            InstrumentRelationIR(
                relation_type=IMPLEMENTS_RELATION,
                from_ref=national_id,
                to_ref=implements,
                metadata={"stated_by": "reviewer"},
            )
        )
    ref = SourceRef(
        jurisdiction=jurisdiction,
        source_code=source_code,
        source_id=national_id,
        source_type=SOURCE_TYPE,
    )
    return ParsedDoc(ref=ref, instruments=[instrument], relations=relations)


def ensure_source(conn: psycopg.Connection, jurisdiction: str, source_code: str) -> None:
    """Idempotently register the per-country contributed-document source row.

    Created on first use so no seed change is needed before a reviewer's first
    upload.
    """
    row = conn.execute("SELECT id FROM jurisdictions WHERE code = %s", (jurisdiction,)).fetchone()
    if row is None:
        msg = f"Unknown jurisdiction: {jurisdiction} (seed it before contributing a document)"
        raise ValueError(msg)
    conn.execute(
        """
        INSERT INTO sources (jurisdiction_id, code, name, id_system, fetch_skill, terms)
        VALUES (%s, %s, %s, %s, 'core/contributed',
                '{"note": "documents contributed by a reviewer from the validation UI or the CLI"}'::jsonb)
        ON CONFLICT (code) DO NOTHING
        """,
        (row[0], source_code, f"Contributed documents ({jurisdiction})", ID_SYSTEM),
    )


def stored_content_hash(conn: psycopg.Connection, source_code: str, national_id: str) -> str | None:
    """Content hash of this document as already stored, if it is stored at all."""
    row = conn.execute(
        """
        SELECT i.metadata ->> 'content_hash'
        FROM instruments i JOIN sources s ON s.id = i.source_id
        WHERE s.code = %s AND i.national_id = %s
        """,
        (source_code, national_id),
    ).fetchone()
    return row[0] if row else None


def read_input(url: str | None, file_path: str | None) -> tuple[bytes, str, str]:
    """Read a contributed document's bytes, however the reviewer named it.

    Returns (raw bytes, content type, origin URI). Fetching happens here, in
    Python — never in the UI, which passes a URL or a path and nothing else.
    """
    if bool(url) == bool(file_path):
        msg = "Contribute exactly one of a URL or a file path"
        raise ValueError(msg)
    if url:
        import httpx

        with httpx.Client(
            timeout=60.0,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            response = client.get(url)
        response.raise_for_status()
        raw = response.content
        return raw, extract.content_type_for(url, response.headers.get("content-type"), raw), str(response.url)
    path = Path(file_path)
    raw = path.read_bytes()
    return raw, extract.content_type_for(path.name, None, raw), path.resolve().as_uri()


def suggest(url: str | None = None, file_path: str | None = None) -> dict[str, str | None]:
    """Title and validity-date suggestions for an input, loading nothing.

    Cheap enough for the UI to call while the reviewer is still typing: it
    reads the document, never the database.
    """
    raw, content_type, origin = read_input(url, file_path)
    extracted = extract.extract(raw, content_type)
    fallback = Path(urlsplit(origin).path).name or None
    title = extracted.suggested_title or fallback
    valid_from = extract.suggested_valid_from(title, url or origin)
    return {
        "title": title,
        "valid_from": valid_from.isoformat() if valid_from else None,
        "content_type": content_type,
    }


def ingest_document(
    *,
    database_url: str,
    jurisdiction: str | None = None,
    lang: str = "en",
    title: str | None = None,
    kind: str | None = None,
    valid_from: date | None = None,
    url: str | None = None,
    file_path: str | None = None,
    implements: str | None = None,
    max_items: int = 500,
    progress: Callable[[dict], None] | None = None,
) -> DocumentResult:
    """Fetch or read one contributed document and load it into the store.

    A URL is routed here rather than wherever the caller decided: a known
    official source is handed to its country adapter, a whole-code or
    unresolvable URL is refused with its hint. For everything else the order
    is archive, parse, load — the raw bytes reach `fetch_snapshots` before a
    parser has seen them, exactly as an adapter-ingested act does.
    """
    report = progress or (lambda event: None)
    if url:
        report({"phase": "route", "detail": url})
        outcome = route(url, database_url)
        if outcome.kind == "refused":
            raise ValueError(outcome.hint)
        if outcome.kind == "adapter":
            report(
                {
                    "phase": "adapter",
                    "detail": f"{outcome.source_name}: {outcome.national_id} "
                    f"(resolved by {outcome.resolved_by})",
                }
            )
            return _ingest_through_adapter(outcome, database_url, max_items)

    if not jurisdiction:
        msg = "A contributed document needs the jurisdiction it belongs to"
        raise ValueError(msg)
    if not title:
        msg = "A contributed document needs a title"
        raise ValueError(msg)
    if not kind:
        allowed = ", ".join(kinds_for(jurisdiction))
        msg = f"A contributed document needs a kind (one of: {allowed})"
        raise ValueError(msg)
    if valid_from is None:
        msg = (
            "A contributed document needs the date it is in force from "
            "(--valid-from): no version enters the store with an invented legal date"
        )
        raise ValueError(msg)
    jurisdiction = jurisdiction.upper()
    trust_class = trust_class_for(jurisdiction, kind)  # fails fast on an unknown kind
    source_code = source_code_for(jurisdiction)

    report({"phase": "fetch", "detail": url or file_path or ""})
    raw, content_type, origin = read_input(url, file_path)
    national_id = national_id_for(raw, url)
    digest = content_hash(raw)
    report({"phase": "archive", "detail": f"{len(raw)} bytes, {content_type}"})

    with psycopg.connect(database_url) as conn:
        ensure_source(conn, jurisdiction, source_code)
        run_id = create_fetch_run(conn, source_code, SKILL_VERSION, Trigger.MANUAL)
        result = DocumentResult(
            jurisdiction=jurisdiction,
            source_code=source_code,
            national_id=national_id,
            kind=kind,
            source_trust_class=trust_class,
            content_hash=digest,
            origin=origin,
            fetch_run_id=run_id,
            implements=implements,
        )
        try:
            ref = SourceRef(
                jurisdiction=jurisdiction,
                source_code=source_code,
                source_id=national_id,
                source_type=SOURCE_TYPE,
            )
            store = PostgresSnapshotStore(conn, run_id)
            result.snapshot_id = store.write_snapshot(
                ref=ref,
                url=origin,
                status_code=200,
                content_type=content_type,
                content_hash=digest,
                content=raw,
            )
            if stored_content_hash(conn, source_code, national_id) == digest:
                report({"phase": "already_present", "detail": national_id})
                result.already_present = True
                finish_fetch_run(
                    conn,
                    run_id,
                    "succeeded",
                    {
                        "trigger": Trigger.MANUAL.value,
                        "national_id": national_id,
                        "already_present": True,
                    },
                )
                return result

            report({"phase": "parse", "detail": content_type})
            doc = parse_document(
                raw,
                content_type=content_type,
                jurisdiction=jurisdiction,
                lang=lang,
                title=title,
                kind=kind,
                valid_from=valid_from,
                source_code=source_code,
                national_id=national_id,
                origin=origin,
                snapshot_id=result.snapshot_id,
                implements=implements,
            )
            report({"phase": "load", "detail": national_id})
            stats: LoadStats = LegislationLoader(conn).load(doc)
            report({"phase": "done", "detail": f"{stats.chunks} chunks"})
            result.units = stats.units
            result.versions = stats.versions
            result.texts = stats.texts
            result.chunks = stats.chunks
            finish_fetch_run(
                conn,
                run_id,
                "succeeded",
                {
                    "trigger": Trigger.MANUAL.value,
                    "national_id": national_id,
                    "kind": kind,
                    "source_trust_class": trust_class.value,
                    "units": stats.units,
                    "versions": stats.versions,
                    "texts": stats.texts,
                    "chunks": stats.chunks,
                },
            )
        except Exception as exc:
            finish_fetch_run(
                conn, run_id, "failed", {"trigger": Trigger.MANUAL.value, "error": str(exc)}
            )
            raise
    return result
