"""Parser for BOE ``legislacion-consolidada`` XML payloads into legislation IR.

One payload is one complete consolidated act: ``<metadatos>`` (act identity),
``<analisis>`` (subject codes and the amendment graph) and ``<texto>``, whose
``<bloque>`` elements are the act's structural units. Each block carries the
full list of its dated ``<version>`` elements — BOE versions at *provision*
level rather than minting a whole new consolidated document per amendment, so
one fetch yields the entire history and this parser needs no expansion pass.

Four properties of the live data drive the code below (all verified against the
LIRPF and the LGSS, see ``Nomotheca-RAG/Spain_sources_analysis.md`` §3):

1. two versions of one block can share a ``fecha_vigencia`` — collapsed here,
   keeping the later-published text, because a zero-length validity range is
   rejected by ``VersionIR``;
2. version lists are not reliably sorted by date — sorted here before chaining;
3. block ids carry hyphens (``da-17``) and are not ltree-safe — sanitized here;
4. the scales *are* the parameters, so ``<table>`` is rendered row-wise rather
   than flattened, keeping the numbers attached to their columns for the
   verbatim-extract check downstream.
"""

from __future__ import annotations

import re
import unicodedata
import xml.etree.ElementTree as ET
from datetime import date, datetime
from typing import Any

from nomotheca_ingest.core.ir import InstrumentIR, ParsedDoc, Snapshot, SourceRef, TextIR, UnitIR, VersionIR


# Short citation labels for the acts EUROMOD ES cites most, keyed by BOE id.
# Used to build unit citations ("LIRPF Artículo 63"); acts outside the table
# fall back to their official number ("35/2006 Artículo 63").
KNOWN_ACTS: dict[str, str] = {
    "BOE-A-2006-20764": "LIRPF",
    "BOE-A-2007-6820": "RIRPF",
    "BOE-A-2015-11724": "LGSS",
    "BOE-A-2021-21007": "Ley IMV",
    "BOE-A-2025-2576": "RD SMI 2025",
    "BOE-A-2011-18161": "DL 1/2011 Galicia",
}

# ``encabezado`` blocks nest; rank orders the container stack.
_CONTAINER_RANKS: tuple[tuple[str, int, str], ...] = (
    ("subseccion", 4, "subseccion"),
    ("seccion", 3, "seccion"),
    ("capitulo", 2, "capitulo"),
    ("titulo", 1, "titulo"),
    ("libro", 0, "libro"),
)

_UNIT_TYPE_PREFIXES: tuple[tuple[str, str], ...] = (
    ("articulo", "articulo"),
    ("disposicion adicional", "disposicion_adicional"),
    ("disposicion transitoria", "disposicion_transitoria"),
    ("disposicion derogatoria", "disposicion_derogatoria"),
    ("disposicion final", "disposicion_final"),
    ("anexo", "anexo"),
)


def parse_boe_xml(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse an archived BOE consolidated-act payload into IR."""
    root = ET.fromstring(payload)
    code = root.findtext("./status/code")
    if code is not None and code != "200":
        msg = f"BOE returned status {code} for {ref.source_id!r}: {root.findtext('./status/text')}"
        raise ValueError(msg)

    # Anchored to ./data/ rather than searched with .//: <analisis> nests one
    # <texto> per amendment reference (131 of them in the LIRPF payload), and a
    # descendant search picks up the first reference blurb instead of the act.
    metadatos = root.find("./data/metadatos")
    if metadatos is None:
        msg = f"BOE payload for {ref.source_id!r} has no <metadatos> element"
        raise ValueError(msg)

    boe_id = metadatos.findtext("identificador") or ref.source_id
    numero_oficial = metadatos.findtext("numero_oficial") or boe_id
    short_citation = KNOWN_ACTS.get(boe_id, numero_oficial)
    url_eli = metadatos.findtext("url_eli")

    units = _parse_units(
        root.find("./data/texto"),
        boe_id=boe_id,
        short_citation=short_citation,
        url_eli=url_eli,
        snapshot=snapshot,
    )

    instrument = InstrumentIR(
        jurisdiction=ref.jurisdiction,
        source_code=ref.source_code,
        instrument_type=_instrument_type(metadatos.findtext("rango")),
        national_id=boe_id,
        eli=url_eli,
        title={"es": metadatos.findtext("titulo") or boe_id},
        adoption_date=_parse_date(metadatos.findtext("fecha_disposicion")),
        publication_date=_parse_date(metadatos.findtext("fecha_publicacion")),
        units=units,
        metadata=_instrument_metadata(metadatos, numero_oficial),
        )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"blocks": len(units)})


def _instrument_metadata(metadatos: ET.Element, numero_oficial: str) -> dict[str, Any]:
    """Collect act-level provenance worth keeping beside the instrument."""
    metadata: dict[str, Any] = {"numero_oficial": numero_oficial}
    for field in (
        "ambito",
        "departamento",
        "rango",
        "diario",
        "fecha_actualizacion",
        "fecha_vigencia",
        "estado_consolidacion",
        "estatus_derogacion",
        "vigencia_agotada",
        "url_html_consolidada",
    ):
        value = metadatos.findtext(field)
        if value:
            metadata[field] = value
    ambito = metadatos.find("ambito")
    if ambito is not None and ambito.get("codigo"):
        metadata["ambito_codigo"] = ambito.get("codigo")
    return metadata


def _parse_units(
    texto: ET.Element | None,
    *,
    boe_id: str,
    short_citation: str,
    url_eli: str | None,
    snapshot: Snapshot,
) -> list[UnitIR]:
    """Turn ``<bloque>`` elements into units, nesting them under their headings.

    ``encabezado`` blocks (TÍTULO/CAPÍTULO/Sección) become container units with
    no versions: they carry the hierarchy for breadcrumbs without emitting a
    near-empty "TÍTULO I" chunk into retrieval.
    """
    if texto is None:
        return []

    units: list[UnitIR] = []
    stack: list[tuple[int, str]] = []  # (rank, path) of open containers
    seen_citations: dict[str, int] = {}
    for ordinal, block in enumerate(texto.findall("bloque"), start=1):
        block_id = block.get("id")
        if not block_id:
            continue
        titulo = (block.get("titulo") or "").strip()
        tipo = block.get("tipo") or "precepto"
        token = _path_token(block_id)

        rank = _container_rank(titulo) if tipo == "encabezado" else None
        if rank is not None:
            while stack and stack[-1][0] >= rank:
                stack.pop()

        parent_path = stack[-1][1] if stack else None
        path = f"{parent_path}.{token}" if parent_path else token
        citation = _unique_citation(short_citation, titulo, tipo, seen_citations)

        unit = UnitIR(
            unit_type=_unit_type(tipo, titulo),
            path=path,
            citation=citation,
            ordinal=ordinal,
            parent_path=parent_path,
            national_id=f"{boe_id}/{block_id}",
            is_container=rank is not None,
            metadata={"bloque_id": block_id, "tipo": tipo},
            versions=(
                []
                if rank is not None
                else _parse_versions(
                    block,
                    boe_id=boe_id,
                    block_id=block_id,
                    citation=citation,
                    url_eli=url_eli,
                    snapshot=snapshot,
                )
            ),
        )
        units.append(unit)
        if rank is not None:
            stack.append((rank, path))
    return units


def _unique_citation(short_citation: str, titulo: str, tipo: str, seen: dict[str, int]) -> str:
    """Return a citation unique within the act, suffixing repeats with an index.

    Block titles repeat: an act amended over time accumulates several
    "Disposición transitoria primera" blocks (BOE distinguishes them only by id
    — ``dtprimera`` vs ``dtprimera-2``), and headings like "CAPÍTULO I" recur in
    every título. The loader reconciles units by ``national_id`` *or*
    ``citation``, so two units sharing a citation silently collapse into one and
    the second provision's versions are grafted onto the first.
    """
    base = _citation(short_citation, titulo, tipo)
    seen[base] = seen.get(base, 0) + 1
    return base if seen[base] == 1 else f"{base} ({seen[base]})"


def _parse_versions(
    block: ET.Element,
    *,
    boe_id: str,
    block_id: str,
    citation: str,
    url_eli: str | None,
    snapshot: Snapshot,
) -> list[VersionIR]:
    """Build the dated version chain of one block.

    Same-date versions are collapsed (last in document order wins — the
    later-published text) and the chain is sorted before each version is
    bounded by the start of the next; the final version stays open-ended.
    """
    dated: dict[date, ET.Element] = {}
    for element in block.findall("version"):
        valid_from = _parse_date(element.get("fecha_vigencia"))
        if valid_from is not None:
            dated[valid_from] = element

    starts = sorted(dated)
    versions: list[VersionIR] = []
    for index, valid_from in enumerate(starts):
        element = dated[valid_from]
        valid_to = starts[index + 1] if index + 1 < len(starts) else None
        content = _render_version(element)
        if not content:
            continue
        stamp = valid_from.strftime("%Y%m%d")
        versions.append(
            VersionIR(
                valid_from=valid_from,
                valid_to=valid_to,
                source_version_id=f"{boe_id}/{block_id}@{stamp}",
                eli_version=f"{url_eli}/con/{stamp}" if url_eli else None,
                citation_label=citation,
                fetch_snapshot_id=snapshot.id,
                amendment_note=_amendment_note(element),
                texts=[TextIR(lang="es", content=content)],
            )
        )
    return versions


def _amendment_note(element: ET.Element) -> dict[str, Any]:
    """Record which norm produced this version, from the version attributes."""
    note: dict[str, Any] = {}
    if element.get("id_norma"):
        note["id_norma"] = element.get("id_norma")
    published = element.get("fecha_publicacion") or element.get("fpub")
    if published:
        note["fecha_publicacion"] = published
    return note


def _render_version(element: ET.Element) -> str:
    """Render one version's mixed content as plain text.

    Tables are emitted row-wise: the tax scales are the parameters, and a flat
    ``itertext()`` would strand every figure from its column.
    """
    return "\n".join(_render_children(element)).strip()


def _render_children(element: ET.Element) -> list[str]:
    """Render an element's children into text lines."""
    lines: list[str] = []
    for child in element:
        if child.tag == "table":
            lines.extend(_render_table(child))
        elif any(grandchild.tag in {"p", "table", "blockquote"} for grandchild in child):
            lines.extend(_render_children(child))
        else:
            text = _normalize_space(_element_text(child))
            if text:
                lines.append(text)
    return lines


def _render_table(table: ET.Element) -> list[str]:
    """Render a table as pipe-separated rows, keeping figures with columns."""
    rows: list[str] = []
    for row in table.iter("tr"):
        cells = [_normalize_space(_element_text(cell)) for cell in row]
        if any(cells):
            rows.append(" | ".join(cells))
    return rows


def _element_text(element: ET.Element) -> str:
    """Collect an element's text, treating ``<br/>`` as a word separator.

    Header cells routinely read ``Base liquidable<br/>Hasta euros``; a plain
    ``itertext()`` would run those into "Base liquidableHasta euros".
    """
    parts: list[str] = [element.text or ""]
    for child in element:
        parts.append(" " if child.tag == "br" else _element_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def _citation(short_citation: str, titulo: str, tipo: str) -> str:
    """Build the human citation recorded on a unit and its versions."""
    label = titulo or {"preambulo": "preámbulo", "firma": "firma", "nota_inicial": "nota inicial"}.get(tipo, tipo)
    return f"{short_citation} {label}"


def _container_rank(titulo: str) -> int | None:
    """Return the nesting rank of a heading block, or None if unrecognised."""
    folded = _fold(titulo)
    for prefix, rank, _ in _CONTAINER_RANKS:
        if folded.startswith(prefix):
            return rank
    return None


def _unit_type(tipo: str, titulo: str) -> str:
    """Normalize a block into an ASCII unit_type value."""
    folded = _fold(titulo)
    if tipo == "encabezado":
        for prefix, _, name in _CONTAINER_RANKS:
            if folded.startswith(prefix):
                return name
        return "encabezado"
    for prefix, name in _UNIT_TYPE_PREFIXES:
        if folded.startswith(prefix):
            return name
    return _path_token(tipo)


def _instrument_type(rango: str | None) -> str:
    """Normalize a BOE ``rango`` (Ley, Real Decreto…) into an ASCII slug."""
    return _path_token(rango) if rango else "norma"


def _parse_date(value: str | None) -> date | None:
    """Parse a BOE ``YYYYMMDD`` date string."""
    if not value or not value.isdigit() or len(value) != 8:
        return None
    try:
        return datetime.strptime(value, "%Y%m%d").date()
    except ValueError:
        return None


def _fold(value: str) -> str:
    """Lowercase and strip accents so heading matches are accent-insensitive."""
    decomposed = unicodedata.normalize("NFKD", value.strip().lower())
    return "".join(char for char in decomposed if not unicodedata.combining(char))


def _path_token(value: str) -> str:
    """Sanitize a label into an ltree-compatible path token."""
    token = re.sub(r"[^0-9A-Za-z]+", "_", _fold(value)).strip("_").lower()
    return token or "unknown"


def _normalize_space(value: str) -> str:
    """Collapse the payload's XML indentation into single spaces."""
    return " ".join(value.split())
