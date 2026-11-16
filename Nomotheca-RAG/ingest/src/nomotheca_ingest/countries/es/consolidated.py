"""BOE ``legislacion-consolidada`` payloads: one ``<bloque>`` per unit, each
with the full list of its dated ``<version>`` elements."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import date
from typing import Any

from nomotheca_ingest.countries.es.boe import (
    ContainerStack,
    _citation,
    _container_rank,
    _element_text,
    _normalize_space,
    _parse_date,
    _path_token,
    _render_table,
    _unit_type,
    act_identity,
    boe_instrument,
    child_path,
    short_citation_for,
)
from nomotheca_ingest.core.ir import ParsedDoc, Snapshot, SourceRef, TextIR, UnitIR, VersionIR
from nomotheca_ingest.core.text import UniqueCitations


def parse_consolidated(root: ET.Element, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse a consolidated-act payload (``<response>``) into IR."""
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

    units = _parse_units(
        root.find("./data/texto"),
        boe_id=act_identity(metadatos, ref)[0],
        short_citation=short_citation_for(metadatos, ref),
        url_eli=metadatos.findtext("url_eli"),
        snapshot=snapshot,
    )
    ambito = metadatos.find("ambito")
    instrument = boe_instrument(
        metadatos,
        ref,
        units=units,
        ambito_codigo=ambito.get("codigo") if ambito is not None else None,
        publication_date=_parse_date(metadatos.findtext("fecha_publicacion")),
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"blocks": len(units)})


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
    containers = ContainerStack()
    citations = UniqueCitations()
    for ordinal, block in enumerate(texto.findall("bloque"), start=1):
        block_id = block.get("id")
        if not block_id:
            continue
        titulo = (block.get("titulo") or "").strip()
        tipo = block.get("tipo") or "precepto"
        rank = _container_rank(titulo) if tipo == "encabezado" else None
        parent_path = containers.parent_for(rank)
        path = child_path(parent_path, _path_token(block_id))
        citation = citations.claim(_citation(short_citation, titulo, tipo))

        units.append(
            UnitIR(
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
        )
        if rank is not None:
            containers.push(rank, path)
    return units


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
