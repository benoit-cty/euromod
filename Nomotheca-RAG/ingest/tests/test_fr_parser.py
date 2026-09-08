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


def test_code_article_keeps_its_nota_application_note() -> None:
    """The NOTA is where a consolidated article says which income year it applies to."""
    ref = SourceRef(jurisdiction="FR", source_code="FR-LEGI", source_id="LEGIARTI000051200465", source_type="article")
    doc = parse_dila_json(
        """
        {
          "META": {
            "META_COMMUN": {"ID": "LEGIARTI000051200465", "NATURE": "Article"},
            "META_SPEC": {"META_ARTICLE": {"NUM": "224", "ETAT": "VIGUEUR", "DATE_DEBUT": "2025-02-16", "DATE_FIN": "2999-01-01"}}
          },
          "CONTEXTE": {"TEXTE": {"@cid": "LEGITEXT000006069577", "TITRE_TXT": [{"#text": "Code général des impôts"}]}},
          "NOTA": {"CONTENU": "<p>Conformément au A du IV de l'article 10 de la loi n° 2025-127 du 14 février 2025, les I et II de l'article précité sont applicables à l'imposition des revenus de l'année 2025.</p>"},
          "BLOC_TEXTUEL": {"CONTENU": "<p>I.-Il est institué une contribution à la charge des contribuables.</p>"}
        }
        """.encode(),
        ref,
        _snapshot(ref),
    )

    text = doc.instruments[0].units[0].versions[0].texts[0]
    assert text.content.startswith("I.-Il est institué une contribution")
    assert "\n\nNOTA : Conformément au A du IV de l'article 10" in text.content
    assert text.content.endswith("revenus de l'année 2025.")
    assert "<strong>NOTA :</strong>" in text.content_html


def test_article_without_nota_is_unchanged() -> None:
    ref = SourceRef(jurisdiction="FR", source_code="FR-LEGI", source_id="LEGIARTI000051212954", source_type="article")
    doc = parse_dila_json(
        '{"META": {"META_COMMUN": {"ID": "LEGIARTI000051212954"}, "META_SPEC": {"META_ARTICLE": {"NUM": "197", "DATE_DEBUT": "2025-02-16"}}},'
        ' "CONTEXTE": {"TEXTE": {"@cid": "LEGITEXT000006069577"}}, "BLOC_TEXTUEL": {"CONTENU": "<p>I. – Barème.</p>"}}'.encode(),
        ref,
        _snapshot(ref),
    )
    assert doc.instruments[0].units[0].versions[0].texts[0].content == "I. – Barème."


def test_fr_adapter_rebuilds_source_ref_from_snapshot_url() -> None:
    """`reparse` replays the archive: the DILA id in the URL is all it needs."""
    adapter = FrAdapter()
    ref = adapter.source_ref_from_url(
        "https://git.tricoteuses.fr/dila/donnees_juridiques/raw/branch/main/LEGI/ARTI/00/00/51/20/04/LEGIARTI000051200465.json",
        "FR-LEGI",
    )
    assert (ref.source_id, ref.source_type, ref.source_code) == ("LEGIARTI000051200465", "article", "FR-LEGI")
    assert adapter.source_ref_from_url("https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000051168007", "FR-LEGI").source_type == "instrument"
    assert adapter.source_ref_from_url("https://example.org/report.pdf", "FR-LEGI") is None


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
