"""Parser for French DILA JSON payloads into legislation IR."""

from __future__ import annotations

import json
import re
from datetime import date
from html import unescape
from typing import Any

from euromod_ingest.core.ir import InstrumentIR, ParsedDoc, Snapshot, SourceRef, TextIR, UnitIR, VersionIR


TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def strip_html(value: str) -> str:
    """Convert simple DILA HTML content into normalized plain text."""
    return SPACE_RE.sub(" ", unescape(TAG_RE.sub(" ", value))).strip()


def parse_dila_json(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse archived DILA JSON bytes into a parsed document IR."""
    data = json.loads(payload.decode("utf-8"))
    if ref.source_id.startswith("LEGIARTI") or ref.source_id.startswith("JORFARTI"):
        return _parse_article(data, ref, snapshot)
    if ref.source_id.startswith("JORFTEXT"):
        return _parse_jorf_text(data, ref)
    if ref.source_id.startswith("JORFSCTA"):
        return _parse_jorf_section(data, ref)
    return ParsedDoc(ref=ref, metadata={"raw_type": _raw_type(data), "child_refs": _child_refs(data)})


def _parse_jorf_text(data: dict[str, Any], ref: SourceRef) -> ParsedDoc:
    """Parse a JORF text root and expose its structural children."""
    meta_commun = _dig(data, "META", "META_COMMUN") or {}
    chronicle = _dig(data, "META", "META_SPEC", "META_TEXTE_CHRONICLE") or {}
    version = _dig(data, "META", "META_SPEC", "META_TEXTE_VERSION") or {}
    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type=(meta_commun.get("NATURE") or "loi").lower(),
        national_id=meta_commun.get("ID") or ref.source_id,
        eli=_eli_alias(meta_commun) or meta_commun.get("ID_ELI"),
        title={"fr": version.get("TITREFULL") or version.get("TITRE") or ref.source_id},
        adoption_date=_parse_date(chronicle.get("DATE_TEXTE")),
        publication_date=_parse_date(chronicle.get("DATE_PUBLI")),
        metadata={"nor": chronicle.get("NOR"), "num": chronicle.get("NUM")},
    )
    return ParsedDoc(
        ref=ref,
        instruments=[instrument],
        metadata={"raw_type": _raw_type(data), "child_refs": _child_refs(data)},
    )


def _parse_jorf_section(data: dict[str, Any], ref: SourceRef) -> ParsedDoc:
    """Parse a JORF section enough to continue structural expansion."""
    return ParsedDoc(
        ref=ref,
        metadata={
            "raw_type": "SECTION_TA",
            "title": data.get("TITRE_TA"),
            "child_refs": _child_refs(data),
        },
    )


def _parse_article(data: dict[str, Any], ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse a DILA ARTI payload into one instrument with one article unit."""
    meta_article = _dig(data, "META", "META_SPEC", "META_ARTICLE") or {}
    meta_commun = _dig(data, "META", "META_COMMUN") or {}
    contexte = data.get("CONTEXTE") or {}
    texte = contexte.get("TEXTE") or {}
    bloc = data.get("BLOC_TEXTUEL") or {}

    article_number = str(data.get("NUM") or meta_article.get("NUM") or ref.source_id)
    code_cid = texte.get("@cid") or ref.metadata.get("instrument_id") or "UNKNOWN"
    citation = _citation(code_cid, article_number)
    html = bloc.get("CONTENU") or ""
    content = strip_html(html)
    valid_from = _parse_date(meta_article.get("DATE_DEBUT")) or _parse_date(texte.get("@date_publi")) or date.min
    valid_to = _parse_date(meta_article.get("DATE_FIN"))

    unit = UnitIR(
        unit_type="article",
        path=f"art_{_path_token(article_number)}",
        citation=citation,
        ordinal=_ordinal(article_number),
        national_id=meta_commun.get("ID") or ref.source_id,
        eli=_eli_alias(meta_commun) or meta_commun.get("ID_ELI"),
        versions=[
            VersionIR(
                valid_from=valid_from,
                valid_to=valid_to,
                source_version_id=ref.source_id,
            eli_version=_eli_alias(meta_commun) or meta_commun.get("ID_ELI"),
                citation_label=citation,
                fetch_snapshot_id=snapshot.id,
                texts=[TextIR(lang="fr", content=content, content_html=html)],
                metadata={"etat": meta_article.get("ETAT")},
            )
        ],
    )
    instrument = InstrumentIR(
        jurisdiction="FR",
        source_code=ref.source_code,
        instrument_type="code" if code_cid.startswith("LEGITEXT") else "loi",
        national_id=code_cid,
        title={"fr": _text_title(texte) or code_cid},
        units=[unit],
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"raw_type": _raw_type(data)})


def _child_refs(data: dict[str, Any]) -> list[dict[str, str]]:
    """Extract DILA structural child ids from JORF text or section payloads."""
    struct = data.get("STRUCT") or data.get("STRUCTURE_TA") or {}
    children: list[dict[str, str]] = []
    for key, source_type in (("LIEN_ART", "article"), ("LIEN_SECTION_TA", "section")):
        for item in _as_list(struct.get(key)):
            source_id = item.get("@id")
            if source_id:
                children.append({
                    "source_id": source_id,
                    "source_type": source_type,
                    "title": item.get("#text") or item.get("@num") or source_id,
                })
    return children


def _text_title(texte: dict[str, Any]) -> str | None:
    """Return the best French title from a DILA CONTEXTE.TEXTE object."""
    titles = _as_list(texte.get("TITRE_TXT"))
    for title in titles:
        text = title.get("#text")
        if text:
            return text
    return texte.get("#text")


def _eli_alias(meta_commun: dict[str, Any]) -> str | None:
    """Return a string ELI alias from DILA metadata when present."""
    alias = meta_commun.get("ELI_ALIAS")
    if isinstance(alias, dict):
        return alias.get("ID_ELI_ALIAS")
    if isinstance(alias, str):
        return alias
    return None


def _as_list(value: Any) -> list[dict[str, Any]]:
    """Normalize DILA fields that may be absent, single objects, or lists."""
    if value is None:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _dig(data: dict[str, Any], *keys: str) -> Any:
    """Safely descend through nested dictionary keys."""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _parse_date(value: str | None) -> date | None:
    """Parse a DILA date string, treating the sentinel future date as open-ended."""
    if not value or value == "2999-01-01":
        return None
    return date.fromisoformat(value)


def _citation(code_cid: str, article_number: str) -> str:
    """Build a canonical French citation label for a code article."""
    if code_cid == "LEGITEXT000006069577":
        return f"CGI, art. {article_number}"
    return f"{code_cid}, art. {article_number}"


def _path_token(value: str) -> str:
    """Sanitize an article number into an ltree-compatible path token."""
    token = re.sub(r"[^0-9A-Za-z]+", "_", value).strip("_").lower()
    return token or "unknown"


def _ordinal(value: str) -> int:
    """Extract a numeric sibling order from an article label."""
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else 0


def _raw_type(data: dict[str, Any]) -> str | None:
    """Return the DILA META_COMMUN type when present."""
    meta_commun = _dig(data, "META", "META_COMMUN") or {}
    return meta_commun.get("TYPE")
