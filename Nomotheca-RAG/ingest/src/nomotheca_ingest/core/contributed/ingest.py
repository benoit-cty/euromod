"""Archive, parse and load a contributed document; re-parse stored ones."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from uuid import UUID

import psycopg

from nomotheca_ingest.core import extract
from nomotheca_ingest.core.contributed.fetch import SourceDocument, read_input
from nomotheca_ingest.core.contributed.kinds import ContributedFields, stated_fields
from nomotheca_ingest.core.contributed.series import chain_editions
from nomotheca_ingest.core.db import connect, ensure_source, fetch_run
from nomotheca_ingest.core.documents import DocumentSpec, build_document
from nomotheca_ingest.core.errors import RefusalError
from nomotheca_ingest.core.ir import (
    IngestMode,
    InstrumentRelationIR,
    ParsedDoc,
    SourceRef,
    SourceTrustClass,
    Trigger,
)
from nomotheca_ingest.core.loader import LegislationLoader, LoadStats
from nomotheca_ingest.core.reparse import ReparseStats, reload
from nomotheca_ingest.core.routing import RouteKind, RouteOutcome

ID_SYSTEM = "contributed"
SOURCE_TYPE = "contributed_document"
SKILL_VERSION = "contrib-0.1"
IMPLEMENTS_RELATION = "implements"


@dataclass(slots=True)
class DocumentResult:
    """What one contributed-document run did."""

    jurisdiction: str
    source_code: str
    national_id: str
    origin: str
    # None on the adapter path: an official act ingested by its own adapter has
    # no reviewer-stated kind, and its bytes were archived by that adapter.
    kind: str | None = None
    source_trust_class: SourceTrustClass | None = None
    content_hash: str | None = None
    #: 'contributed', or 'adapter' when the URL turned out to belong to a
    #: known official source and the legislation ingester ran instead.
    routed_to: RouteKind = "contributed"
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


def _ingest_through_adapter(outcome: RouteOutcome, database_url: str, max_items: int) -> DocumentResult:
    """Hand a known official source to the existing legislation ingester."""
    from nomotheca_ingest.core.pipeline import run_database_ingest

    pipeline_result = run_database_ingest(
        jurisdiction=outcome.jurisdiction,
        identifier=outcome.national_id,
        database_url=database_url,
        mode=IngestMode.INSTRUMENT,
        max_items=max_items,
    )
    loaded = LoadStats.total(pipeline_result.loaded)
    return DocumentResult(
        jurisdiction=outcome.jurisdiction,
        source_code=outcome.source_name or "",
        national_id=outcome.national_id,
        origin=outcome.url,
        routed_to="adapter",
        units=loaded.units,
        versions=loaded.versions,
        texts=loaded.texts,
        chunks=loaded.chunks,
        fetch_run_id=pipeline_result.run_id,
    )


def route(url: str, database_url: str | None = None) -> RouteOutcome:
    """Classify a URL against the official portals the adapters declare."""
    from nomotheca_ingest.core import routing

    return routing.route_url(url, database_url=database_url)


def parse_document(document: SourceDocument, fields: ContributedFields) -> ParsedDoc:
    """Turn one archived document plus the reviewer's declaration into loadable IR.

    Pure: no network, no database. This is the seam the parse tests exercise.
    """
    if document.snapshot_id is None:
        msg = "Archive the bytes before parsing them (archive-first)"
        raise ValueError(msg)

    extracted = extract.extract(document.raw, document.content_type)
    digest = document.content_hash

    spec = DocumentSpec(
        jurisdiction=fields.jurisdiction,
        source_code=fields.source_code,
        instrument_type=fields.kind,
        source_trust_class=fields.source_trust_class,
        national_id=document.national_id,
        title=fields.title,
        lang=fields.lang,
        valid_from=fields.valid_from,
        snapshot_id=document.snapshot_id,
        citation_prefix=fields.title[:120],
        # Content, not the date, decides identity of a version: re-adding the
        # same bytes reuses the version, a changed page opens a new one and
        # the loader closes the previous (see LegislationLoader._chain_versions).
        version_key=f"{document.national_id}@{digest[:16]}",
        metadata={
            "contributed": True,
            "kind": fields.kind,
            "norm_level": fields.norm_level.value,
            "content_hash": digest,
            "content_type": document.content_type,
            "origin": document.origin,
        },
    )
    instrument = build_document(extracted.text, spec, pattern=extracted.pattern, content_html=extracted.html)
    return ParsedDoc(
        ref=source_ref(document, fields),
        instruments=[instrument],
        relations=_relations_for(document.national_id, fields.implements),
    )


def source_ref(document: SourceDocument, fields: ContributedFields) -> SourceRef:
    """How this document is addressed in the snapshot store and the loader."""
    return SourceRef(
        jurisdiction=fields.jurisdiction,
        source_code=fields.source_code,
        source_id=document.national_id,
        source_type=SOURCE_TYPE,
    )


def _relations_for(national_id: str, implements: str | None) -> list[InstrumentRelationIR]:
    """The provenance edge a reviewer's "implements" answer stands for.

    "None" is a valid answer — a missing statute must never block an upload —
    and then there is no edge.
    """
    if not implements:
        return []
    return [
        InstrumentRelationIR(
            relation_type=IMPLEMENTS_RELATION,
            from_ref=national_id,
            to_ref=implements,
            metadata={"stated_by": "reviewer"},
        )
    ]


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
    trigger: Trigger = Trigger.MANUAL,
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
            raise RefusalError(outcome.hint)
        if outcome.kind == "adapter":
            report(
                {
                    "phase": "adapter",
                    "detail": f"{outcome.source_name}: {outcome.national_id} (resolved by {outcome.resolved_by})",
                }
            )
            return _ingest_through_adapter(outcome, database_url, max_items)

    # The fields arrive optional because an adapter URL needs none of them;
    # past the routing they must be a complete declaration.
    fields = stated_fields(
        jurisdiction=jurisdiction,
        lang=lang,
        title=title,
        kind=kind,
        valid_from=valid_from,
        implements=implements,
    )

    report({"phase": "fetch", "detail": url or file_path or ""})
    document = read_input(url, file_path)
    report({"phase": "archive", "detail": f"{len(document.raw)} bytes, {document.content_type}"})

    def register_source(conn: psycopg.Connection) -> None:
        ensure_source(
            conn,
            fields.jurisdiction,
            fields.source_code,
            name=f"Contributed documents ({fields.jurisdiction})",
            id_system=ID_SYSTEM,
            fetch_skill="core/contributed",
            note="documents contributed by a reviewer from the validation UI or the CLI",
        )

    with fetch_run(database_url, fields.source_code, SKILL_VERSION, trigger, setup=register_source) as run:
        result = DocumentResult(
            jurisdiction=fields.jurisdiction,
            source_code=fields.source_code,
            national_id=document.national_id,
            kind=fields.kind,
            source_trust_class=fields.source_trust_class,
            content_hash=document.content_hash,
            origin=document.origin,
            fetch_run_id=run.id,
            implements=fields.implements,
        )
        ref = source_ref(document, fields)
        document = document.archived_as(
            run.store.write_snapshot(
                ref=ref,
                url=document.origin,
                status_code=200,
                content_type=document.content_type,
                content_hash=document.content_hash,
                content=document.raw,
            )
        )
        result.snapshot_id = document.snapshot_id

        with connect(database_url) as conn:
            stored = stored_content_hash(conn, fields.source_code, document.national_id)
            if stored == document.content_hash:
                report({"phase": "already_present", "detail": document.national_id})
                result.already_present = True
                # The bytes are unchanged, so nothing is re-parsed — but the
                # reviewer may have come back to state (or correct) which
                # statute this document implements, and that is the only way
                # to record it once a document is in the store.
                if fields.implements:
                    LegislationLoader(conn).load(
                        ParsedDoc(
                            ref=ref,
                            instruments=[],
                            relations=_relations_for(document.national_id, fields.implements),
                        )
                    )
                run.stats = {
                    "national_id": document.national_id,
                    "already_present": True,
                    "implements": fields.implements,
                }
                return result

            report({"phase": "parse", "detail": document.content_type})
            doc = parse_document(document, fields)
            report({"phase": "load", "detail": document.national_id})
            stats: LoadStats = LegislationLoader(conn).load(doc)
            chain_editions(conn)
        report({"phase": "done", "detail": f"{stats.chunks} chunks"})
        result.units = stats.units
        result.versions = stats.versions
        result.texts = stats.texts
        result.chunks = stats.chunks
        run.stats = {
            "national_id": document.national_id,
            "kind": fields.kind,
            "source_trust_class": fields.source_trust_class.value,
            "units": stats.units,
            "versions": stats.versions,
            "texts": stats.texts,
            "chunks": stats.chunks,
        }
    return result


def reparse_documents(
    database_url: str,
    *,
    jurisdiction: str | None = None,
    title_like: str | None = None,
    progress: Callable[[dict], None] | None = None,
) -> list[tuple[str, int, int]]:
    """Re-parse stored contributed documents from their archived bytes.

    A parser fix used to mean deleting the instrument and ingesting it again,
    refetching a page that may now want a browser (the Bulletin officiel) or
    be gone. The snapshot holds the bytes and the instrument holds the
    reviewer's declaration, so both are read back, the units are replaced and
    the instrument row (its id, class and kind) stays. Changed texts lose
    their vectors: run `embeddings build` after. Returns (title, units
    before, units after) per document.
    """
    report = progress or (lambda event: None)
    done: list[tuple[str, int, int]] = []
    with connect(database_url) as conn:
        rows = conn.execute(
            """
            SELECT i.id, j.code, i.national_id, i.title, i.metadata,
                   (SELECT min(lower(v.validity)) FROM legal_units u
                      JOIN legal_unit_versions v ON v.legal_unit_id = u.id
                     WHERE u.instrument_id = i.id),
                   (SELECT t.national_id FROM instrument_relations r
                      JOIN instruments t ON t.id = r.to_instrument_id
                     WHERE r.from_instrument_id = i.id AND r.relation_type = %(implements)s LIMIT 1),
                   (SELECT count(*) FROM legal_units u WHERE u.instrument_id = i.id)
            FROM instruments i JOIN jurisdictions j ON j.id = i.jurisdiction_id
            WHERE i.metadata ->> 'contributed' = 'true'
              AND (%(jurisdiction)s::text IS NULL OR j.code = %(jurisdiction)s)
              AND (%(title_like)s::text IS NULL OR i.title::text ILIKE %(title_like)s)
            ORDER BY i.created_at
            """,
            {"implements": IMPLEMENTS_RELATION, "jurisdiction": jurisdiction, "title_like": title_like},
        ).fetchall()
        for iid, code, national_id, titles, meta, valid_from, implements, before in rows:
            lang, title = next(iter(titles.items()))
            snap = conn.execute(
                "SELECT id, raw_content, content_type FROM fetch_snapshots "
                "WHERE content_hash = %s AND raw_content IS NOT NULL ORDER BY retrieved_at DESC LIMIT 1",
                (meta.get("content_hash"),),
            ).fetchone()
            if snap is None or valid_from is None:
                report({"phase": "skipped", "detail": f"{title}: no snapshot or no version"})
                continue
            fields = ContributedFields(
                jurisdiction=code,
                lang=lang,
                title=title,
                kind=meta["kind"],
                valid_from=valid_from,
                implements=implements,
            )
            document = SourceDocument(
                raw=bytes(snap[1]),
                content_type=meta.get("content_type") or snap[2],
                origin=meta.get("origin") or national_id,
                national_id=national_id,
                snapshot_id=snap[0],
            )
            doc = parse_document(document, fields)
            reload(conn, LegislationLoader(conn), doc, ReparseStats(), replace_units_of=iid)
            after = sum(1 for unit in doc.instruments[0].units)
            report({"phase": "reparsed", "detail": f"{title}: {before} -> {after} units"})
            done.append((title, before, after))
        closed = chain_editions(conn)  # a reload reopens the editions it replaced
        if closed:
            report({"phase": "chained", "detail": f"{closed} versions closed by a later edition"})
    return done
