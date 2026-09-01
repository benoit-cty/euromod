"""Parser and adapter tests for the Dutch BWB payloads (inline fixtures).

Fixtures are trimmed excerpts of real payloads fetched on 2026-09-01 from
repository.officiele-overheidspublicaties.nl.
"""

from datetime import date
from uuid import uuid4

import pytest

from nomotheca_ingest.countries.nl.adapter import NlAdapter
from nomotheca_ingest.countries.nl.parser import parse_bwb_xml, select_toestanden
from nomotheca_ingest.countries.nl.resolver import NlResolver
from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef, VersionStatus


# Four zicht generations of one validity window plus neighbours, as BWB serves
# them: same geldigheid, different knowledge. Deliberately out of document order.
MANIFEST_PAYLOAD = b"""<?xml version="1.0" encoding="utf-8"?>
<work label="BWBR0011353" _latestItem="2026-01-01_1/xml/BWBR0011353_2026-01-01_1.xml">
  <metadata><datum_inwerkingtreding>2001-01-01</datum_inwerkingtreding></metadata>
  <expression label="2024-01-01_0"><metadata>
    <datum_inwerkingtreding>2024-01-01</datum_inwerkingtreding><einddatum>2024-12-31</einddatum>
    <zichtdatum_start>2024-01-01</zichtdatum_start><zichtdatum_eind>2024-06-30</zichtdatum_eind>
  </metadata></expression>
  <expression label="2025-01-01_0"><metadata>
    <datum_inwerkingtreding>2025-01-01</datum_inwerkingtreding><einddatum>2025-03-14</einddatum>
    <zichtdatum_start>2024-12-24</zichtdatum_start><zichtdatum_eind>2025-03-14</zichtdatum_eind>
  </metadata></expression>
  <expression label="2025-01-01_4"><metadata>
    <datum_inwerkingtreding>2025-01-01</datum_inwerkingtreding><einddatum>2025-03-14</einddatum>
    <zichtdatum_start>2026-02-21</zichtdatum_start><zichtdatum_eind>9999-12-31</zichtdatum_eind>
  </metadata></expression>
  <expression label="2025-01-01_2"><metadata>
    <datum_inwerkingtreding>2025-01-01</datum_inwerkingtreding><einddatum>2025-03-14</einddatum>
    <zichtdatum_start>2025-07-19</zichtdatum_start><zichtdatum_eind>2025-12-31</zichtdatum_eind>
  </metadata></expression>
  <expression label="2024-01-01_5"><metadata>
    <datum_inwerkingtreding>2024-01-01</datum_inwerkingtreding><einddatum>2024-12-31</einddatum>
    <zichtdatum_start>2026-02-21</zichtdatum_start><zichtdatum_eind>9999-12-31</zichtdatum_eind>
  </metadata></expression>
  <expression label="2026-02-21_0"><metadata>
    <datum_inwerkingtreding>2026-02-21</datum_inwerkingtreding><einddatum>9999-12-31</einddatum>
    <zichtdatum_start>2026-02-21</zichtdatum_start><zichtdatum_eind>9999-12-31</zichtdatum_eind>
  </metadata></expression>
</work>
"""

# Art. 2.10 (the box 1 tariff table) and a repealed neighbour, with the
# publication metadata BWB attaches to every element left in place so the
# parser is exercised against the noise it has to drop.
TOESTAND_PAYLOAD = """<?xml version="1.0" encoding="UTF-8"?>
<toestand bwb-id="BWBR0011353" inwerkingtreding="2025-01-01">
  <wetgeving soort="wet" xml:lang="nl">
    <intitule ondertekening_bron="2000-05-11" publicatie_bron="2000-05-30"
      >Wet van 11 mei 2000 tot vaststelling van de Wet inkomstenbelasting 2001<meta-data><brondata
      ><publicatie soort="Stb"><publicatiejaar>2000</publicatiejaar></publicatie></brondata></meta-data></intitule>
    <citeertitel status="officieel">Wet inkomstenbelasting 2001</citeertitel>
    <wet-besluit>
      <hoofdstuk bwb-ng-variabel-deel="/Hoofdstuk2" label="Hoofdstuk 2">
        <kop><label>Hoofdstuk</label><nr>2</nr><titel>Raamwerk</titel></kop>
        <afdeling bwb-ng-variabel-deel="/Hoofdstuk2/Afdeling2.3" label="Afdeling 2.3">
          <kop><label>Afdeling</label><nr>2.3</nr><titel>Verschuldigde inkomstenbelasting</titel></kop>
          <artikel bwb-ng-variabel-deel="/Hoofdstuk2/Afdeling2.3/Artikel2.10"
                   stam-id="2833703" versie-id="30526332" label="Artikel 2.10"
                   inwerking="2025-01-01" bron="Stcrt.2024-38492" effect="wijziging" status="goed">
            <kop><label>Artikel</label><nr status="officieel">2.10</nr>
              <titel status="officieel">Tarief belastbaar inkomen uit werk en woning</titel></kop>
            <lid>
              <lidnr status="officieel">1</lidnr>
              <al>De belasting op het belastbare inkomen uit werk en woning (<intref
                doc="jci1.3:c:BWBR0011353&amp;afdeling=3.1">afdeling 3.1</intref>) wordt bepaald
                aan de hand van de volgende tabel.</al>
              <table><tgroup cols="4">
                <thead><row><entry><al>meer dan</al></entry><entry><al>maar niet meer dan</al></entry>
                  <entry><al>kolom III</al></entry><entry><al>kolom IV</al></entry></row></thead>
                <tbody>
                  <row><entry><al>&#8211;</al></entry><entry><al>&#8364; 38.441</al></entry>
                    <entry><al>&#8211;</al></entry><entry><al>8,17%</al></entry></row>
                  <row><entry><al>&#8364; 38.441</al></entry><entry><al>&#8364; 76.817</al></entry>
                    <entry><al>&#8364; 3.140</al></entry><entry><al>37,48%</al></entry></row>
                  <row><entry><al>&#8364; 76.817</al></entry><entry><al>&#8211;</al></entry>
                    <entry><al>&#8364; 17.523</al></entry><entry><al>49,50%</al></entry></row>
                </tbody>
              </tgroup></table>
              <meta-data><jcis><jci versie="1.3"/></jcis></meta-data>
            </lid>
            <lid>
              <lidnr status="officieel">3</lidnr>
              <al>De grondslagverminderende posten zijn:</al>
              <lijst>
                <li><li.nr>a.</li.nr><al>de ondernemersaftrek, bedoeld in artikel 3.74;</al></li>
                <li><li.nr>b.</li.nr><al>de MKB-winstvrijstelling.</al></li>
              </lijst>
            </lid>
            <meta-data><brondata><oorspronkelijk><publicatie soort="Stcrt"
              ><publicatienr>38492</publicatienr></publicatie></oorspronkelijk></brondata></meta-data>
          </artikel>
          <artikel bwb-ng-variabel-deel="/Hoofdstuk2/Afdeling2.3/Artikel2.11"
                   stam-id="2833713" versie-id="17000702" label="Artikel 2.11"
                   inwerking="2011-01-01" bron="Stb.2009-611" effect="vervallen" status="vervallen">
            <kop><label>Artikel</label><nr status="officieel">2.11</nr></kop>
            <al>[Vervallen per 01-01-2011]</al>
          </artikel>
        </afdeling>
      </hoofdstuk>
      <hoofdstuk bwb-ng-variabel-deel="/Hoofdstuk10A" label="Hoofdstuk 10A">
        <kop><label>Hoofdstuk</label><nr>10A</nr><titel>Overgangsrecht</titel></kop>
        <artikel bwb-ng-variabel-deel="/Hoofdstuk10A/Artikel10a.30"
                 stam-id="2999999" versie-id="31000000" status="nogniet">
          <kop><label>Artikel</label><nr status="officieel">10a.30</nr>
            <titel>Overgangsbepaling inkomensafhankelijke combinatiekorting</titel></kop>
          <al>Nog niet in werking getreden bepaling.</al>
        </artikel>
      </hoofdstuk>
    </wet-besluit>
  </wetgeving>
</toestand>
""".encode()


def _ref(source_id: str, source_type: str) -> SourceRef:
    return SourceRef(jurisdiction="NL", source_code="NL-BWB", source_id=source_id, source_type=source_type)


def _snapshot() -> Snapshot:
    return Snapshot(
        id=uuid4(),
        source_code="NL-BWB",
        url="https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0011353/manifest.xml",
        http_status=200,
        content_type="application/xml",
        content_hash="0" * 64,
        raw_content=b"",
    )


# ---------------------------------------------------------------------------
# Version index and the bitemporal selection rule
# ---------------------------------------------------------------------------


def test_select_toestanden_prefers_current_knowledge_over_first_match():
    # Four toestanden share the 2025-01-01 validity window; only _4 reflects
    # current knowledge. Picking _0 (first, and lowest-numbered) would load
    # what the publisher believed in December 2024.
    labels = select_toestanden(MANIFEST_PAYLOAD, (date(2025, 1, 1),))
    assert labels[0] == "2025-01-01_4"


def test_select_toestanden_always_includes_the_version_in_force_now():
    labels = select_toestanden(MANIFEST_PAYLOAD, (date(2024, 1, 1),))
    assert labels == ["2024-01-01_5", "2026-02-21_0"]


def test_select_toestanden_skips_dates_no_expression_covers():
    assert select_toestanden(MANIFEST_PAYLOAD, (date(1999, 1, 1),)) == ["2026-02-21_0"]


def test_manifest_parses_into_toestand_child_refs():
    doc = parse_bwb_xml(MANIFEST_PAYLOAD, _ref("BWBR0011353", "version_index"), _snapshot())
    assert doc.instruments == []
    assert doc.metadata["toestanden_available"] == 6
    assert doc.metadata["latest_item"].startswith("2026-01-01_1/")
    source_ids = [child["source_id"] for child in doc.metadata["child_refs"]]
    assert "BWBR0011353/2025-01-01_4" in source_ids
    assert all(child["source_type"] == "toestand" for child in doc.metadata["child_refs"])


# ---------------------------------------------------------------------------
# One dated consolidation
# ---------------------------------------------------------------------------


def test_toestand_parses_instrument_metadata():
    doc = parse_bwb_xml(TOESTAND_PAYLOAD, _ref("BWBR0011353/2025-01-01_0", "toestand"), _snapshot())
    instrument = doc.instruments[0]
    assert instrument.jurisdiction == "NL"
    assert instrument.source_code == "NL-BWB"
    assert instrument.national_id == "BWBR0011353"
    assert instrument.instrument_type == "wet"
    assert instrument.title == {"nl": "Wet inkomstenbelasting 2001"}
    assert instrument.adoption_date == date(2000, 5, 11)
    assert instrument.publication_date == date(2000, 5, 30)
    # The Netherlands implements no ELI; Juriconnect is the citation scheme.
    assert instrument.eli is None
    assert instrument.metadata["juriconnect"] == "jci1.3:c:BWBR0011353"
    assert instrument.metadata["toestand_label"] == "2025-01-01_0"


def test_toestand_splits_articles_with_ltree_safe_nested_paths():
    doc = parse_bwb_xml(TOESTAND_PAYLOAD, _ref("BWBR0011353/2025-01-01_0", "toestand"), _snapshot())
    units = doc.instruments[0].units
    # The not-yet-in-force article (status="nogniet", no inwerking) is skipped:
    # there is no validity range to load it under.
    assert [unit.national_id for unit in units] == ["BWBR0011353-2.10", "BWBR0011353-2.11"]

    tariff = units[0]
    assert tariff.unit_type == "artikel"
    assert tariff.path == "hoofdstuk2.afdeling2_3.artikel2_10"
    assert tariff.path.replace(".", "").replace("_", "").isalnum()
    assert tariff.citation == "Wet IB 2001, artikel 2.10"
    assert tariff.metadata == {
        "hoofdstuk": "Hoofdstuk 2 Raamwerk",
        "afdeling": "Afdeling 2.3 Verschuldigde inkomstenbelasting",
    }


def test_article_versions_carry_bwb_version_identity_and_stay_open_ended():
    doc = parse_bwb_xml(TOESTAND_PAYLOAD, _ref("BWBR0011353/2025-01-01_0", "toestand"), _snapshot())
    tariff, repealed = doc.instruments[0].units

    version = tariff.versions[0]
    # inwerking is the article's own start date, not the toestand's.
    assert version.valid_from == date(2025, 1, 1)
    # Open-ended: the loader's _chain_versions closes the predecessor.
    assert version.valid_to is None
    assert version.status is VersionStatus.IN_FORCE
    # versie-id is what makes re-ingesting an unchanged article a no-op.
    assert version.source_version_id == "30526332"
    assert version.amendment_note == {"bron": "Stcrt.2024-38492", "effect": "wijziging"}

    # An article can be older than the toestand that contains it, and repealed.
    assert repealed.versions[0].valid_from == date(2011, 1, 1)
    assert repealed.versions[0].status is VersionStatus.REPEALED


def test_article_text_renders_the_tariff_table_with_figures_intact():
    doc = parse_bwb_xml(TOESTAND_PAYLOAD, _ref("BWBR0011353/2025-01-01_0", "toestand"), _snapshot())
    content = doc.instruments[0].units[0].versions[0].texts[0].content

    assert content.startswith("Artikel 2.10. Tarief belastbaar inkomen uit werk en woning")
    # The 2025 three-band schedule, one row per line: the anti-hallucination
    # check needs each figure beside its heading, character for character.
    assert "| € 38.441 | € 76.817 | € 3.140 | 37,48% |" in content
    assert "| € 76.817 | – | € 17.523 | 49,50% |" in content
    assert "| – | € 38.441 | – | 8,17% |" in content
    # Lid numbers stay attached to their own text; inline refs are flattened.
    assert "1. De belasting op het belastbare inkomen uit werk en woning (afdeling 3.1)" in content
    assert "a. de ondernemersaftrek, bedoeld in artikel 3.74;" in content
    # Publication bookkeeping never reaches the retrieval chunks.
    assert "38492" not in content
    assert "jci1.3" not in content


def test_article_text_language_is_dutch():
    doc = parse_bwb_xml(TOESTAND_PAYLOAD, _ref("BWBR0011353/2025-01-01_0", "toestand"), _snapshot())
    assert doc.instruments[0].units[0].versions[0].texts[0].lang == "nl"


# ---------------------------------------------------------------------------
# Adapter, resolver, canary
# ---------------------------------------------------------------------------


def test_adapter_constructs_with_zero_args_and_declares_its_source():
    adapter = NlAdapter()
    assert adapter.jurisdiction == "NL"
    # The Nomoscope scout invokes the CLI without --source-code.
    assert adapter.default_source_code == "NL-BWB"


def test_adapter_expands_child_refs_into_work_items():
    adapter = NlAdapter()
    doc = parse_bwb_xml(MANIFEST_PAYLOAD, _ref("BWBR0011353", "version_index"), _snapshot())
    work = adapter.expand(doc)
    assert [item.ref.source_id for item in work] == [
        child["source_id"] for child in doc.metadata["child_refs"]
    ]
    assert all(item.ref.source_code == "NL-BWB" for item in work)
    assert adapter.expand(parse_bwb_xml(TOESTAND_PAYLOAD, _ref("BWBR0011353/2025-01-01_0", "toestand"), _snapshot())) == []


@pytest.mark.parametrize(
    ("citation", "expected"),
    [
        ("Wet IB 2001, artikel 2.10", "BWBR0011353"),
        ("Wet inkomstenbelasting 2001 art. 2.10", "BWBR0011353"),
        ("BWBR0002221", "BWBR0002221"),
        ("Algemene wet inkomensafhankelijke regelingen, artikel 7", "BWBR0018472"),
    ],
)
def test_resolver_maps_known_citations_to_the_version_index(citation, expected):
    refs = NlResolver().resolve(CitationRef(jurisdiction="NL", citation=citation), date(2025, 6, 30))
    assert len(refs) == 1
    assert refs[0].source_id == expected
    assert refs[0].source_type == "version_index"
    assert refs[0].source_code == "NL-BWB"


def test_resolver_points_unknown_citations_at_the_sru_lookup():
    with pytest.raises(ValueError, match="zoekservice.overheid.nl"):
        NlResolver().resolve(
            CitationRef(jurisdiction="NL", citation="Wet op de dierenbescherming"), date(2025, 6, 30)
        )


def test_canary_asserts_the_2025_three_band_schedule():
    facts = NlAdapter().canary_facts()
    tariff = next(fact for fact in facts if "2.10" in fact.citation)
    assert tariff.assert_latest_start_gte == date(2025, 1, 1)
    assert "38.441" in tariff.reason
