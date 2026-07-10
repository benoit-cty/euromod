"""Tests for French direct-id fetch utilities."""

from euromod_ingest.countries.fr.fetcher import dila_json_path


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
