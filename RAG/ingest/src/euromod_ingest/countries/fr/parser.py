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
    return ParsedDoc(ref=ref, metadata={"raw_type": _raw_type(data)})


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
    valid_from = _parse_date(meta_article.get("DATE_DEBUT")) or date.min
    valid_to = _parse_date(meta_article.get("DATE_FIN"))

    unit = UnitIR(
        unit_type="article",
        path=f"art_{_path_token(article_number)}",
        citation=citation,
        ordinal=_ordinal(article_number),
        national_id=meta_commun.get("ID") or ref.source_id,
        eli=meta_commun.get("ELI_ALIAS"),
        versions=[
            VersionIR(
                valid_from=valid_from,
                valid_to=valid_to,
                source_version_id=ref.source_id,
                eli_version=meta_commun.get("ELI_ALIAS"),
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
        title={"fr": texte.get("#text") or code_cid},
        units=[unit],
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"raw_type": _raw_type(data)})


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
