"""Dated editions of one publication are chained, the latest stays open."""

from __future__ import annotations

from datetime import date

from nomotheca_ingest.core.contributed.series import chain_editions, edition_of

BOFIP = "https://bofip.impots.gouv.fr/bofip/2136-PGP.html/identifiant=BOI-RSA-BASE-30-30-"


def test_a_bofip_url_names_its_series_and_its_edition_date() -> None:
    assert edition_of(BOFIP + "20170724") == ("BOI-RSA-BASE-30-30", date(2017, 7, 24))
    assert edition_of("https://www.legislation.cnav.fr/Pages/texte.aspx?Nom=circulaire_cnav_2025_13") is None
    assert edition_of(BOFIP + "20171345") is None  # not a date


class _Conn:
    """Enough of a connection to see which editions get closed, and where."""

    def __init__(self, instruments: list[tuple[str, int, str]]) -> None:
        self.instruments = instruments
        self.closed: list[tuple[str, date]] = []

    def execute(self, sql: str, params: dict | None = None):
        if params is None:
            return self
        self.closed.append((params["instrument"], params["end"]))
        self.rowcount = 2
        return self

    def fetchall(self):
        return self.instruments


def test_each_edition_ends_where_the_next_one_held_begins() -> None:
    conn = _Conn(
        [
            ("ed2017", 7, BOFIP + "20170724"),
            ("ed2012", 7, BOFIP + "20120912"),
            ("ed2016", 7, BOFIP + "20160613"),
            ("other", 7, "https://bofip.impots.gouv.fr/bofip/2491-PGP.html/identifiant=BOI-IR-LIQ-20-20-10-20250414"),
            ("circular", 7, "https://www.unedic.org/circulaire-2025-03"),
            ("elsewhere", 9, BOFIP + "20200101"),  # another source: not the same series
        ]
    )
    assert chain_editions(conn) == 4
    assert conn.closed == [("ed2012", date(2016, 6, 13)), ("ed2016", date(2017, 7, 24))]
