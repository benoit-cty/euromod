"""Parser for BOE ``legislacion-consolidada`` XML payloads into legislation IR.

The consolidated payload is parsed in `consolidated`, the daily gazette's in
`diario`; what they share is in `boe`.

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

import xml.etree.ElementTree as ET

from nomotheca_ingest.countries.es.boe import KNOWN_ACTS
from nomotheca_ingest.countries.es.consolidated import parse_consolidated
from nomotheca_ingest.countries.es.diario import parse_diario
from nomotheca_ingest.core.ir import ParsedDoc, Snapshot, SourceRef

__all__ = ["KNOWN_ACTS", "parse_boe_xml"]


def parse_boe_xml(payload: bytes, ref: SourceRef, snapshot: Snapshot) -> ParsedDoc:
    """Parse an archived BOE payload into IR: a consolidated act, or (root
    ``<documento>``) one from the daily gazette."""
    root = ET.fromstring(payload)
    if root.tag == "documento":
        return parse_diario(root, ref, snapshot)
    return parse_consolidated(root, ref, snapshot)
