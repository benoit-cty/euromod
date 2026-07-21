"""Tests for French DILA JSON parsing and structural expansion."""

from __future__ import annotations

from uuid import uuid4

from nomotheca_ingest.countries.fr.adapter import FrAdapter
from nomotheca_ingest.countries.fr.parser import parse_dila_json
from nomotheca_ingest.core.ir import Snapshot, SourceRef


def test_jorf_text_parses_instrument_and_child_refs() -> None:
    """A JORF text root exposes the bill instrument and structural worklist."""
    ref = SourceRef(jurisdiction="FR", source_code="FR-LEGI", source_id="JORFTEXT000051168007", source_type="instrument")
    doc = parse_dila_json(
        """
        {
          "META": {
            "META_COMMUN": {
              "ID": "JORFTEXT000051168007",
              "ID_ELI": "https://www.legifrance.gouv.fr/eli/loi/2025/2/14/ECOX2423405L/jo/texte",
              "NATURE": "LOI"
            },
            "META_SPEC": {
              "META_TEXTE_CHRONICLE": {
                "NUM": "2025-127",
                "NOR": "ECOX2423405L",
                "DATE_PUBLI": "2025-02-15",
                "DATE_TEXTE": "2025-02-14"
              },
              "META_TEXTE_VERSION": {
                "TITREFULL": "LOI n° 2025-127 du 14 février 2025 de finances pour 2025 (1)"
              }
            }
          },
          "STRUCT": {
            "LIEN_ART": {"@id": "JORFARTI000051168008", "@num": "liminaire"},
            "LIEN_SECTION_TA": {"#text": "PREMIERE PARTIE", "@id": "JORFSCTA000051168011"}
          }
        }
        """.encode(),
        ref,
        _snapshot(ref),
    )

    assert doc.instruments[0].national_id == "JORFTEXT000051168007"
    assert doc.instruments[0].title["fr"].startswith("LOI n° 2025-127")
    assert [child["source_id"] for child in doc.metadata["child_refs"]] == [
        "JORFARTI000051168008",
        "JORFSCTA000051168011",
    ]


def test_fr_adapter_expands_jorf_child_refs() -> None:
    """The French adapter turns parsed child refs into source work items."""
    ref = SourceRef(jurisdiction="FR", source_code="FR-LEGI", source_id="JORFTEXT000051168007", source_type="instrument")
    doc = parse_dila_json(
      '{"META": {"META_COMMUN": {"ID": "JORFTEXT000051168007"}}, "STRUCT": {"LIEN_SECTION_TA": {"@id": "JORFSCTA000051168011"}}}'.encode(),
        ref,
        _snapshot(ref),
    )

    work = FrAdapter().expand(doc)

    assert len(work) == 1
    assert work[0].ref.source_id == "JORFSCTA000051168011"
    assert work[0].ref.source_type == "section"


def _snapshot(ref: SourceRef) -> Snapshot:
    """Build a minimal snapshot for parser tests."""
    return Snapshot(
        id=uuid4(),
        source_code=ref.source_code,
        url="https://example.test/source.json",
        http_status=200,
        content_type="application/json",
        content_hash="0" * 64,
        raw_content=b"{}",
    )
