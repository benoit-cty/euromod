"""Tests for French direct-id fetch utilities."""

from nomotheca_ingest.countries.fr.fetcher import dila_json_path


def test_dila_json_path_for_jorf_text() -> None:
    """JORF text identifiers map to the documented Tricoteuses path scheme."""
    assert (
        dila_json_path("JORFTEXT000051168007")
        == "JORF/TEXT/00/00/51/16/80/JORFTEXT000051168007.json"
    )


def test_dila_json_path_for_legi_article() -> None:
    """LEGI article identifiers map to the documented Tricoteuses path scheme."""
    assert (
        dila_json_path("LEGIARTI000051212954")
        == "LEGI/ARTI/00/00/51/21/29/LEGIARTI000051212954.json"
    )


def test_fr_citations_resolve_ids_and_refuse_free_text():
    from datetime import date

    import pytest

    from nomotheca_ingest.core.ir import CitationRef
    from nomotheca_ingest.countries.fr.resolver import FrResolver

    resolver = FrResolver()
    (ref,) = resolver.resolve(CitationRef(jurisdiction="FR", citation="JORFTEXT000051168007"), date(2025, 7, 1))
    assert (ref.source_code, ref.source_id) == ("FR-LEGI", "JORFTEXT000051168007")
    (kali,) = resolver.resolve(
        CitationRef(jurisdiction="FR", citation="https://www.legifrance.gouv.fr/conv_coll/id/KALITEXT000036731682"),
        date(2025, 7, 1),
    )
    assert kali.source_code == "FR-KALI"
    with pytest.raises(ValueError, match="not resolvable"):
        resolver.resolve(CitationRef(jurisdiction="FR", citation="CGI art. 197"), date(2025, 7, 1))
