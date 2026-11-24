"""Staatscourant publications (NL-STCRT): notices, regulations, explanatory notes."""

from __future__ import annotations

from datetime import date
from uuid import uuid4

import pytest
from nomotheca_ingest.core.ir import Snapshot, SourceRef, SourceTrustClass
from nomotheca_ingest.countries.nl.adapter import NlAdapter
from nomotheca_ingest.countries.nl.fetcher import url_for_ref
from nomotheca_ingest.countries.nl.staatscourant import parse_stcrt

NOTICE = """<?xml version="1.0" encoding="utf-8"?>
<officiele-publicatie>
  <kop><titel>STAATSCOURANT</titel></kop>
  <staatscourant>
    <intitule>Mededeling van de Minister van Sociale Zaken en Werkgelegenheid van 25 november 2024, nr. 2024-0000917125, houdende de per 1 januari 2025 gewijzigde bedragen in enkele wetten, besluiten en regelingen</intitule>
    <regeling>
      <aanhef><wie>De Minister van Sociale Zaken en Werkgelegenheid;</wie></aanhef>
      <regeling-tekst>
        <tekst status="goed">
          <al>dat met ingang van 1 januari 2025 in de hierna genoemde regelgeving de bedragen zijn gewijzigd en als volgt komen te luiden:</al>
          <tussenkop kopopmaak="vet">B Algemene nabestaandenwet</tussenkop>
          <al>Het percentage, genoemd in artikel 2 van de Algemene nabestaandenwet bedraagt: 157,5%.</al>
          <tussenkop kopopmaak="vet">C Algemene Ouderdomswet</tussenkop>
          <al>Het bruto-ouderdomspensioen, bedoeld in artikel 9, vijfde lid, van de Algemene Ouderdomswet, bedraagt:</al>
          <lijst>
            <li><li.nr>a.</li.nr><al>in onderdeel a: € 1.580,92; en</al></li>
            <li><li.nr>b.</li.nr><al>in onderdeel b: € 1.081,50.</al></li>
          </lijst>
        </tekst>
      </regeling-tekst>
      <nota-toelichting>
        <kop><titel>TOELICHTING</titel></kop>
        <tekst>
          <al>Deze mededeling volgt op de eerste.<noot><noot.nr>1</noot.nr><noot.al>Stcrt. 2023, 33542.</noot.al></noot> De bedragen zijn gebundeld.</al>
        </tekst>
        <divisie>
          <kop><titel>Artikelsgewijs</titel></kop>
          <divisie>
            <kop><titel>Artikel III</titel></kop>
            <tekst><al>Het maximumdagloon is dan gelijk aan 1/261e van 75.864,87 euro, oftewel 290,67 euro.</al></tekst>
          </divisie>
        </divisie>
      </nota-toelichting>
    </regeling>
  </staatscourant>
</officiele-publicatie>
""".encode()

REGULATION = """<?xml version="1.0" encoding="utf-8"?>
<officiele-publicatie>
  <staatscourant>
    <intitule>Regeling van de Minister van Sociale Zaken en Werkgelegenheid van 19 november 2024, nr. 2024-0000914618, houdende de vaststelling premiepercentages 2025</intitule>
    <regeling>
      <regeling-tekst>
        <artikel status="goed">
          <kop><label>Artikel</label> <nr>III</nr> <titel>Maximum premieloon</titel></kop>
          <al>Het bedrag, bedoeld in artikel 17, eerste lid, bedraagt voor het jaar 2025 € 75.864.</al>
        </artikel>
        <wijzig-artikel>
          <kop>ARTIKEL VIII WIJZIGING REGELING WFSV</kop>
          <wat>In bijlage 1 wordt “€ 7.324.006” vervangen door “€ 7.807.390”.</wat>
        </wijzig-artikel>
        <artikel status="goed">
          <kop><label>Artikel</label> <nr>IX</nr> <titel>Inwerkingtreding</titel></kop>
          <lid><lidnr>1.</lidnr><al>Deze regeling treedt in werking met ingang van 1 januari 2025.</al></lid>
          <lid><lidnr>2.</lidnr><al>Artikel VIII werkt terug tot en met 1 januari 2024.</al></lid>
        </artikel>
      </regeling-tekst>
      <bijlage>
        <kop>BIJLAGE 1, BEHORENDE BIJ ARTIKEL VIII</kop>
        <al>Grootwinkelbedrijf: € 7.807.390.</al>
      </bijlage>
    </regeling>
  </staatscourant>
</officiele-publicatie>
""".encode()

ADVICE = b"""<?xml version="1.0" encoding="utf-8"?>
<officiele-publicatie><staatscourant><intitule>Advies Raad van State</intitule>
<adviesRvS><vrije-tekst><tekst><al>Aan de Koning</al></tekst></vrije-tekst></adviesRvS></staatscourant></officiele-publicatie>
"""


def _parse(payload: bytes, source_id: str):
    ref = SourceRef(jurisdiction="NL", source_code="NL-STCRT", source_id=source_id, source_type="instrument")
    snapshot = Snapshot(
        id=uuid4(), source_code="NL-STCRT", url="https://example.org/x.xml", content_hash="0" * 64, raw_content=payload
    )
    return parse_stcrt(payload, ref, snapshot)


def test_a_stcrt_id_is_fetched_from_the_staatscourant_source():
    adapter = NlAdapter()
    assert adapter.source_code_for("stcrt-2024-39288") == "NL-STCRT"
    assert adapter.source_code_for("BWBR0002221") == "NL-BWB"
    ref = SourceRef(jurisdiction="NL", source_code="NL-STCRT", source_id="stcrt-2024-39288", source_type="instrument")
    assert url_for_ref(ref).endswith("/officielepublicaties/stcrt/2024/stcrt-2024-39288/xml/stcrt-2024-39288.xml")
    assert adapter.url_source.id_pattern.search("https://zoek.officielebekendmakingen.nl/stcrt-2024-39288.html")


def test_a_notice_is_cut_into_its_lettered_sections_each_carrying_the_date():
    doc = _parse(NOTICE, "stcrt-2024-39288")
    notice = doc.instruments[0]
    assert notice.instrument_type == "mededeling"
    assert notice.source_trust_class is SourceTrustClass.EVIDENCE
    assert notice.adoption_date == date(2024, 11, 25)
    assert [unit.citation for unit in notice.units] == [
        "Stcrt. 2024, 39288, B Algemene nabestaandenwet",
        "Stcrt. 2024, 39288, C Algemene Ouderdomswet",
    ]
    aow = notice.units[1].versions[0]
    assert aow.valid_from == date(2025, 1, 1) and aow.valid_to is None
    assert aow.amendment_note == {"as_published": True, "effective_date_basis": "met_ingang_van"}
    text = aow.texts[0]
    assert text.lang == "nl"
    # The framing sentence travels with every section: the amount never stands without its date.
    assert "dat met ingang van 1 januari 2025" in text.content
    assert "a. in onderdeel a: € 1.580,92; en" in text.content
    assert "157,5%" not in text.content


def test_the_explanatory_note_is_a_guidance_instrument_of_its_own():
    doc = _parse(NOTICE, "stcrt-2024-39288")
    note = doc.instruments[1]
    assert note.national_id == "stcrt-2024-39288/toelichting"
    assert note.source_trust_class is SourceTrustClass.GUIDANCE
    assert [unit.citation for unit in note.units] == [
        "Stcrt. 2024, 39288, toelichting",
        "Stcrt. 2024, 39288, toelichting, Artikelsgewijs — Artikel III",
    ]
    # A footnote is dropped where it stands; the sentence around it stays whole.
    assert (
        note.units[0].versions[0].texts[0].content == "Deze mededeling volgt op de eerste. De bedragen zijn gebundeld."
    )
    assert "oftewel 290,67 euro" in note.units[1].versions[0].texts[0].content


def test_a_regulation_is_cut_into_articles_amending_articles_and_annexes():
    doc = _parse(REGULATION, "stcrt-2024-38722")
    assert len(doc.instruments) == 1
    regulation = doc.instruments[0]
    assert regulation.instrument_type == "ministeriele-regeling"
    assert [unit.citation for unit in regulation.units] == [
        "Stcrt. 2024, 38722, artikel III",
        "Stcrt. 2024, 38722, artikel VIII",
        "Stcrt. 2024, 38722, artikel IX",
        "Stcrt. 2024, 38722, bijlage 1",
    ]
    first = regulation.units[0].versions[0]
    assert first.texts[0].content.startswith("Artikel III. Maximum premieloon\nHet bedrag")
    # The commencement article, not the retroactive clause, dates the text.
    assert first.valid_from == date(2025, 1, 1)
    assert first.amendment_note["effective_date_basis"] == "treedt_in_werking"
    assert "vervangen door “€ 7.807.390”" in regulation.units[1].versions[0].texts[0].content
    assert len({unit.national_id for unit in regulation.units}) == 4


def test_what_is_neither_a_regulation_nor_a_notice_is_refused():
    with pytest.raises(ValueError, match="not a regulation or a notice"):
        _parse(ADVICE, "stcrt-2024-1868")


def test_a_circular_that_is_not_a_notice_of_amounts_is_guidance():
    decree = (
        ADVICE.replace(b"Advies Raad van State", b"Inkomstenbelasting en loonbelasting. Besluit heffingskortingen")
        .replace(b"<adviesRvS><vrije-tekst>", b"<circulaire><circulaire-tekst>")
        .replace(b"</vrije-tekst></adviesRvS>", b"</circulaire-tekst></circulaire>")
    )
    instrument = _parse(decree, "stcrt-2024-38558").instruments[0]
    assert instrument.instrument_type == "beleidsregel"
    assert instrument.source_trust_class is SourceTrustClass.GUIDANCE
    notice = decree.replace(b"Inkomstenbelasting en loonbelasting. Besluit", b"Mededeling van de Minister houdende")
    assert _parse(notice, "stcrt-2024-42409").instruments[0].source_trust_class is SourceTrustClass.EVIDENCE
