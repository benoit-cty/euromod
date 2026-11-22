"""What the two BOE parsers share: act labels, the instrument row, the
container stack and the small text/date helpers.

`consolidated` reads the ``legislacion-consolidada`` API (a ``<bloque>`` per
unit, with its dated versions); `diario` reads the daily gazette's
``<documento>`` (an act BOE never consolidated, as published).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import date, datetime
from typing import Any

from nomotheca_ingest.core.ir import InstrumentIR, SourceRef, UnitIR
from nomotheca_ingest.core.text import fold_accents, path_token, pipe_rows
from nomotheca_ingest.countries.es.regions import jurisdiction_for

# Short citation labels for the acts EUROMOD ES cites most, keyed by BOE id.
# Used to build unit citations ("LIRPF Artículo 63"); acts outside the table
# fall back to their official number ("35/2006 Artículo 63").
KNOWN_ACTS: dict[str, str] = {
    "BOE-A-2006-20764": "LIRPF",
    "BOE-A-2007-6820": "RIRPF",
    "BOE-A-2015-11724": "LGSS",
    "BOE-A-2021-21007": "Ley IMV",
    "BOE-A-2025-2576": "RD SMI 2025",
    # Autonomous-community acts, qualified by region: several communities
    # share an official number (Asturias and Aragón both have a Ley 3/2021),
    # and the citation is what the pipeline's golden cases and the resolver
    # aliases key on, so the region is part of the name.
    "BOE-A-2011-18161": "DL 1/2011 Galicia",
    "BOE-A-2011-13120": "Ley 3/2011 Galicia",
    "BOE-A-2023-2940": "Ley 5/2022 Canarias",
    "BOE-A-2007-4066": "Ley 1/2007 Canarias",
    "BOE-A-2021-9007": "DL 3/2021 Canarias",
    "BOE-A-2021-13685": "Ley 3/2021 Asturias",
    "BOE-A-2023-1405": "Ley 14/2022 País Vasco",
    "BOE-A-2011-15732": "Ley 18/2008 País Vasco",
    "BOE-A-2016-11671": "Ley Foral 15/2016 Navarra",
    "BOE-A-2021-10673": "Ley 3/2021 Aragón",
    "BOE-A-2002-4378": "Ley 15/2001 Madrid",
    "BOE-A-2017-9799": "Ley 14/2017 Cataluña",
    "BOE-A-2023-13761": "Ley 4/2023 Illes Balears",
    "BOE-A-2020-8013": "DL 10/2020 Illes Balears",
    "BOE-A-2016-4178": "Ley 5/2016 Illes Balears",
    "BOE-A-2007-8186": "Ley 2/2007 Cantabria",
    "BOE-A-2019-3491": "Ley 5/2019 Extremadura",
    "BOE-A-2017-5627": "Ley 4/2017 La Rioja",
    "BOE-A-2008-12493": "Ley 3/2007 Murcia",
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


class ContainerStack:
    """The open ``encabezado`` containers (TÍTULO, CAPÍTULO, Sección…), by rank.

    A heading closes every open container of its rank or deeper, then hangs
    under what is left; units that are not containers hang under the top.
    """

    def __init__(self) -> None:
        self._open: list[tuple[int, str]] = []  # (rank, path)

    def parent_for(self, rank: int | None) -> str | None:
        """The path a unit of this rank (None: not a container) hangs under."""
        if rank is not None:
            while self._open and self._open[-1][0] >= rank:
                self._open.pop()
        return self._open[-1][1] if self._open else None

    def push(self, rank: int, path: str) -> None:
        self._open.append((rank, path))

    def clear(self) -> None:
        self._open.clear()


def child_path(parent_path: str | None, token: str) -> str:
    return f"{parent_path}.{token}" if parent_path else token


def boe_instrument(
    metadatos: ET.Element,
    ref: SourceRef,
    *,
    units: list[UnitIR],
    ambito_codigo: str | None,
    publication_date: date | None,
    extra_metadata: dict[str, Any] | None = None,
) -> InstrumentIR:
    """The instrument row, from a payload's ``<metadatos>``.

    An autonomous-community act files under its community (ES-GA, ES-CN, …),
    a child jurisdiction of the adapter's ES: see regions.py and ADR 0003.
    State acts keep the ref's jurisdiction.
    """
    boe_id, numero_oficial = act_identity(metadatos, ref)
    url_eli = metadatos.findtext("url_eli")
    return InstrumentIR(
        jurisdiction=jurisdiction_for(
            url_eli=url_eli,
            departamento=metadatos.findtext("departamento"),
            ambito_codigo=ambito_codigo,
            default=ref.jurisdiction,
        ),
        source_code=ref.source_code,
        instrument_type=_instrument_type(metadatos.findtext("rango")),
        national_id=boe_id,
        eli=url_eli,
        title={"es": metadatos.findtext("titulo") or boe_id},
        adoption_date=_parse_date(metadatos.findtext("fecha_disposicion")),
        publication_date=publication_date,
        units=units,
        metadata={**_instrument_metadata(metadatos, numero_oficial), **(extra_metadata or {})},
    )


def act_identity(metadatos: ET.Element, ref: SourceRef) -> tuple[str, str]:
    """(BOE id, official number) of the act a payload carries."""
    boe_id = metadatos.findtext("identificador") or ref.source_id
    return boe_id, metadatos.findtext("numero_oficial") or boe_id


def short_citation_for(metadatos: ET.Element, ref: SourceRef) -> str:
    """«LIRPF», or the official number for an act outside `KNOWN_ACTS`."""
    boe_id, numero_oficial = act_identity(metadatos, ref)
    return KNOWN_ACTS.get(boe_id, numero_oficial)


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


def _render_table(table: ET.Element) -> list[str]:
    """Render a table as pipe-separated rows, keeping figures with columns."""
    return pipe_rows([_normalize_space(_element_text(cell)) for cell in row] for row in table.iter("tr"))


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
    return fold_accents(value.strip().lower())


def _path_token(value: str) -> str:
    """Sanitize a label into an ltree-compatible path token, accents folded."""
    return path_token(value, fold=True)


def _normalize_space(value: str) -> str:
    """Collapse the payload's XML indentation into single spaces."""
    return " ".join(value.split())
