"""BOE daily-gazette ``<documento>`` payloads: an act BOE never consolidated."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import date

from nomotheca_ingest.core.ir import ParsedDoc, Snapshot, SourceRef, TextIR, UnitIR, VersionIR
from nomotheca_ingest.core.text import UniqueCitations
from nomotheca_ingest.countries.es.boe import (
    ContainerStack,
    _citation,
    _element_text,
    _fold,
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


def parse_diario(root: ET.Element, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse a daily-gazette ``<documento>`` (an act BOE never consolidated).

    The yearly cotización orders are published once and never amended, so the
    consolidated API does not have them (see ``fetcher``). The gazette XML is
    the act as published: flat ``<p class=…>`` paragraphs and tables under
    ``<texto>``, with headings told apart by class. Each article, disposición
    and anexo becomes one unit with one version, valid from the act's
    ``fecha_vigencia`` until its ``fecha_derogacion`` if any; chapters and
    sections become containers, like ``encabezado`` blocks; the text before the
    first heading is the preámbulo.
    """
    metadatos = root.find("./metadatos")
    if metadatos is None:
        msg = f"BOE gazette payload for {ref.source_id!r} has no <metadatos> element"
        raise ValueError(msg)
    published = _parse_date(metadatos.findtext("fecha_publicacion"))
    valid_from = _parse_date(metadatos.findtext("fecha_vigencia")) or published
    valid_to = _parse_date(metadatos.findtext("fecha_derogacion"))
    if valid_to is not None and valid_from is not None and valid_to <= valid_from:
        valid_to = None

    units = _parse_diario_units(
        root.find("./texto"),
        boe_id=act_identity(metadatos, ref)[0],
        short_citation=short_citation_for(metadatos, ref),
        url_eli=metadatos.findtext("url_eli"),
        valid_from=valid_from,
        valid_to=valid_to,
        snapshot=snapshot,
    )
    origen = metadatos.find("origen_legislativo")
    instrument = boe_instrument(
        metadatos,
        ref,
        units=units,
        ambito_codigo=origen.get("codigo") if origen is not None else None,
        publication_date=published,
        extra_metadata={"boe_source": "diario"},
    )
    return ParsedDoc(ref=ref, instruments=[instrument], metadata={"blocks": len(units), "boe_source": "diario"})


# Gazette heading classes that open a container, with the rank of the
# matching consolidated ``encabezado`` (see _CONTAINER_RANKS).
_DIARIO_CONTAINERS: dict[str, int] = {"libro_num": 0, "titulo_num": 1, "capitulo_num": 2, "seccion": 3}


def _parse_diario_units(
    texto: ET.Element | None,
    *,
    boe_id: str,
    short_citation: str,
    url_eli: str | None,
    valid_from: date | None,
    valid_to: date | None,
    snapshot: Snapshot,
) -> list[UnitIR]:
    """Split the gazette's flat paragraph stream into units at its headings."""
    if texto is None:
        return []

    # (label, tipo, rank or None, lines) per unit, in document order.
    pieces: list[tuple[str, str, int | None, list[str]]] = [("", "preambulo", None, [])]
    for element in texto:
        css = element.get("class") or ""
        text = _normalize_space(_element_text(element))
        if element.tag == "p" and css in _DIARIO_CONTAINERS and text:
            pieces.append((text, "encabezado", _DIARIO_CONTAINERS[css], []))
        elif element.tag == "p" and css == "articulo" and text:
            pieces.append((_heading_label(text), "precepto", None, [text]))
        elif element.tag == "p" and css == "anexo_num" and text:
            pieces.append((text, "anexo", None, [text]))
        elif element.tag == "table":
            pieces[-1][3].extend(_render_table(element))
        elif text:
            pieces[-1][3].append(text)

    units: list[UnitIR] = []
    containers = ContainerStack()
    citations = UniqueCitations()
    seen_paths: set[str] = set()
    for ordinal, (label, tipo, rank, lines) in enumerate(pieces, start=1):
        if tipo == "anexo" or _fold(label).startswith("disposicion"):
            containers.clear()  # anexos and disposiciones hang under no chapter
        parent_path = containers.parent_for(rank)
        path = base = child_path(parent_path, _path_token(label or tipo))
        n = 1
        while path in seen_paths:
            n += 1
            path = f"{base}_{n}"
        seen_paths.add(path)
        citation = citations.claim(_citation(short_citation, label, tipo))
        content = "\n".join(lines).strip()
        if rank is None and not content:
            continue
        stamp = valid_from.strftime("%Y%m%d") if valid_from else "undated"
        versions = (
            []
            if rank is not None or valid_from is None
            else [
                VersionIR(
                    valid_from=valid_from,
                    valid_to=valid_to,
                    source_version_id=f"{boe_id}/{path}@{stamp}",
                    eli_version=f"{url_eli}/dof" if url_eli else None,
                    citation_label=citation,
                    fetch_snapshot_id=snapshot.id,
                    amendment_note={"id_norma": boe_id, "boe_source": "diario"},
                    texts=[TextIR(lang="es", content=content)],
                )
            ]
        )
        units.append(
            UnitIR(
                unit_type=_unit_type(tipo if tipo != "anexo" else "precepto", label),
                path=path,
                citation=citation,
                ordinal=ordinal,
                parent_path=parent_path,
                national_id=f"{boe_id}/{path}",
                is_container=rank is not None,
                metadata={"tipo": tipo, "boe_source": "diario"},
                versions=versions,
            )
        )
        if rank is not None:
            containers.push(rank, path)
    return units


def _heading_label(heading: str) -> str:
    """Cut a gazette heading to the label consolidated blocks carry.

    «Artículo 3. Bases máximas y mínimas de cotización.» → «Artículo 3», the
    form of a consolidated ``bloque`` title and of the resolver's citations.
    """
    return re.split(r"\.(?:\s|$)", heading, maxsplit=1)[0].strip()
