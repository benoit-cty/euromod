"""Parser and adapter tests for BOE consolidated payloads (inline fixtures).

The fixture is a trimmed excerpt of the real
``legislacion-consolidada/id/BOE-A-2006-20764`` response, keeping one example
of each structure the parser has to survive: nested headings, a scale table,
a hyphenated block id, an out-of-order version chain, and two versions sharing
one ``fecha_vigencia``.
"""

from datetime import date
from uuid import uuid4

import pytest

from nomotheca_ingest.countries.es.adapter import EsAdapter
from nomotheca_ingest.countries.es.parser import parse_boe_xml
from nomotheca_ingest.countries.es.resolver import EsResolver
from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef


ACT_PAYLOAD = b"""<?xml version="1.0" encoding="utf-8"?>
<response>
  <status><code>200</code><text>ok</text></status>
  <data>
    <metadatos>
      <fecha_actualizacion>20260429T074904Z</fecha_actualizacion>
      <identificador>BOE-A-2006-20764</identificador>
      <ambito codigo="1">Estatal</ambito>
      <departamento codigo="7723">Jefatura del Estado</departamento>
      <rango codigo="1300">Ley</rango>
      <fecha_disposicion>20061128</fecha_disposicion>
      <numero_oficial>35/2006</numero_oficial>
      <titulo>Ley 35/2006, de 28 de noviembre, del Impuesto sobre la Renta de las Personas Fisicas.</titulo>
      <fecha_publicacion>20061129</fecha_publicacion>
      <estado_consolidacion codigo="3">Finalizado</estado_consolidacion>
      <url_eli>https://www.boe.es/eli/es/l/2006/11/28/35</url_eli>
      <url_html_consolidada>https://www.boe.es/buscar/act.php?id=BOE-A-2006-20764</url_html_consolidada>
    </metadatos>
    <analisis>
      <referencias>
        <anterior>
          <id_norma>BOE-A-2004-4456</id_norma>
          <relacion codigo="210">DEROGA</relacion>
          <texto>art. 23 y el capitulo VI del titulo VII</texto>
        </anterior>
      </referencias>
    </analisis>
    <texto>
      <bloque id="tv" tipo="encabezado" titulo="T&#205;TULO V">
        <version id_norma="BOE-A-2006-20764" fecha_publicacion="20061129" fecha_vigencia="20070101">
          <p class="titulo">T&#205;TULO V</p>
        </version>
      </bloque>
      <bloque id="ci-2" tipo="encabezado" titulo="CAP&#205;TULO I">
        <version id_norma="BOE-A-2006-20764" fecha_publicacion="20061129" fecha_vigencia="20070101">
          <p class="capitulo">CAP&#205;TULO I</p>
        </version>
      </bloque>
      <bloque id="a63" tipo="precepto" titulo="Art&#237;culo 63">
        <version id_norma="BOE-A-2006-20764" fecha_publicacion="20061129" fecha_vigencia="20070101">
          <p class="articulo">Art&#237;culo 63. Escala general del Impuesto.</p>
          <p class="parrafo">1. La parte de la base liquidable general...</p>
        </version>
        <version id_norma="BOE-A-2020-17339" fecha_publicacion="20201231" fecha_vigencia="20210101">
          <p class="articulo">Art&#237;culo 63. Escala general del Impuesto.</p>
          <table class="tabla">
            <tr>
              <th><p class="cabeza_tabla">Base liquidable<br/>Hasta euros</p></th>
              <th><p class="cabeza_tabla">Tipo aplicable<br/>Porcentaje</p></th>
            </tr>
            <tr>
              <td><p class="cuerpo_tabla_centro">0</p></td>
              <td><p class="cuerpo_tabla_centro">9,50</p></td>
            </tr>
            <tr>
              <td><p class="cuerpo_tabla_centro">300.000,00</p></td>
              <td><p class="cuerpo_tabla_centro">24,50</p></td>
            </tr>
          </table>
        </version>
      </bloque>
      <bloque id="a7" tipo="precepto" titulo="Art&#237;culo 7">
        <version id_norma="BOE-A-2009-20765" fecha_publicacion="20091224" fecha_vigencia="20100113">
          <p class="parrafo">Segunda en el documento, anterior en el tiempo no.</p>
        </version>
        <version id_norma="BOE-A-2009-20375" fecha_publicacion="20091219" fecha_vigencia="20100101">
          <p class="parrafo">Primera por fecha de vigencia.</p>
        </version>
      </bloque>
      <bloque id="a93" tipo="precepto" titulo="Art&#237;culo 93">
        <version id_norma="BOE-A-2022-22128" fecha_publicacion="20221224" fecha_vigencia="20230101">
          <p class="parrafo">Redacci&#243;n descartada.</p>
        </version>
        <version id_norma="BOE-A-2022-22292" fecha_publicacion="20221228" fecha_vigencia="20230101">
          <p class="parrafo">Redacci&#243;n vigente, publicada despu&#233;s.</p>
        </version>
      </bloque>
      <bloque id="dtprimera" tipo="precepto" titulo="Disposici&#243;n transitoria primera">
        <version id_norma="BOE-A-2006-20764" fecha_publicacion="20061129" fecha_vigencia="20070101">
          <p class="parrafo">Primera disposici&#243;n transitoria.</p>
        </version>
      </bloque>
      <bloque id="dtprimera-2" tipo="precepto" titulo="Disposici&#243;n transitoria primera">
        <version id_norma="BOE-A-2014-12327" fecha_publicacion="20141128" fecha_vigencia="20150101">
          <p class="parrafo">Otra disposici&#243;n transitoria, mismo t&#237;tulo.</p>
        </version>
      </bloque>
      <bloque id="da-17" tipo="precepto" titulo="Disposici&#243;n adicional sexag&#233;sima tercera">
        <version id_norma="BOE-A-2026-4667" fecha_publicacion="20260430" fecha_vigencia="20260430">
          <p class="parrafo">Texto de la disposici&#243;n adicional.</p>
        </version>
      </bloque>
    </texto>
  </data>
</response>
"""

ERROR_PAYLOAD = b"""<?xml version="1.0" encoding="utf-8"?>
<response>
  <status><code>404</code><text>La informacion solicitada no existe</text></status>
  <data/>
</response>
"""


def _ref() -> SourceRef:
    return SourceRef(
        jurisdiction="ES",
        source_code="ES-BOE",
        source_id="BOE-A-2006-20764",
        source_type="instrument",
    )


def _snapshot() -> Snapshot:
    return Snapshot(
        id=uuid4(),
        source_code="ES-BOE",
        url="https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/BOE-A-2006-20764",
        http_status=200,
        content_type="application/xml",
        content_hash="0" * 64,
        raw_content=ACT_PAYLOAD,
    )


def _parse():
    return parse_boe_xml(ACT_PAYLOAD, _ref(), _snapshot())


def _unit(doc, path):
    return next(unit for unit in doc.instruments[0].units if unit.path == path)


def test_instrument_metadata_comes_from_metadatos():
    instrument = _parse().instruments[0]
    assert instrument.jurisdiction == "ES"
    assert instrument.source_code == "ES-BOE"
    assert instrument.national_id == "BOE-A-2006-20764"
    assert instrument.instrument_type == "ley"
    assert instrument.eli == "https://www.boe.es/eli/es/l/2006/11/28/35"
    assert instrument.adoption_date == date(2006, 11, 28)
    assert instrument.publication_date == date(2006, 11, 29)
    assert set(instrument.title) == {"es"}
    assert instrument.metadata["numero_oficial"] == "35/2006"
    assert instrument.metadata["ambito"] == "Estatal"


def test_instrument_identity_is_taken_from_the_ref_not_hardcoded():
    ref = SourceRef(
        jurisdiction="ES",
        source_code="ES-REGIONAL",
        source_id="BOE-A-2006-20764",
        source_type="instrument",
    )
    instrument = parse_boe_xml(ACT_PAYLOAD, ref, _snapshot()).instruments[0]
    assert instrument.source_code == "ES-REGIONAL"


def test_headings_become_containers_nested_by_rank():
    doc = _parse()
    titulo = _unit(doc, "tv")
    capitulo = _unit(doc, "tv.ci_2")
    assert titulo.is_container and capitulo.is_container
    assert titulo.unit_type == "titulo"
    assert capitulo.unit_type == "capitulo"
    assert capitulo.parent_path == "tv"
    # Containers carry the hierarchy but must not emit chunks of their own.
    assert titulo.versions == []
    assert capitulo.versions == []


def test_articles_hang_under_the_open_heading_and_are_not_containers():
    article = _unit(_parse(), "tv.ci_2.a63")
    assert article.is_container is False
    assert article.unit_type == "articulo"
    assert article.parent_path == "tv.ci_2"
    assert article.citation == "LIRPF Artículo 63"
    assert article.national_id == "BOE-A-2006-20764/a63"
    assert article.metadata["bloque_id"] == "a63"


def test_every_path_is_ltree_safe():
    for unit in _parse().instruments[0].units:
        for token in unit.path.split("."):
            assert token.replace("_", "").isalnum(), unit.path
    # The hyphenated BOE id is sanitized, and kept verbatim in metadata.
    disposicion = _unit(_parse(), "tv.ci_2.da_17")
    assert disposicion.metadata["bloque_id"] == "da-17"
    assert disposicion.unit_type == "disposicion_adicional"


def test_versions_are_chained_into_contiguous_validity_ranges():
    versions = _unit(_parse(), "tv.ci_2.a63").versions
    assert [v.valid_from for v in versions] == [date(2007, 1, 1), date(2021, 1, 1)]
    assert versions[0].valid_to == date(2021, 1, 1)
    assert versions[-1].valid_to is None
    assert versions[-1].source_version_id == "BOE-A-2006-20764/a63@20210101"
    assert versions[-1].eli_version == "https://www.boe.es/eli/es/l/2006/11/28/35/con/20210101"
    assert versions[-1].amendment_note["id_norma"] == "BOE-A-2020-17339"
    assert versions[-1].citation_label == "LIRPF Artículo 63"


def test_version_snapshot_id_is_recorded_on_every_version():
    snapshot = _snapshot()
    doc = parse_boe_xml(ACT_PAYLOAD, _ref(), snapshot)
    versions = [v for unit in doc.instruments[0].units for v in unit.versions]
    assert versions
    assert all(version.fetch_snapshot_id == snapshot.id for version in versions)


def test_out_of_order_version_chains_are_sorted_before_chaining():
    versions = _unit(_parse(), "tv.ci_2.a7").versions
    assert [v.valid_from for v in versions] == [date(2010, 1, 1), date(2010, 1, 13)]
    assert versions[0].valid_to == date(2010, 1, 13)
    assert "Primera por fecha" in versions[0].texts[0].content


def test_versions_sharing_a_date_collapse_to_the_later_published_text():
    versions = _unit(_parse(), "tv.ci_2.a93").versions
    assert len(versions) == 1
    assert versions[0].valid_from == date(2023, 1, 1)
    assert "vigente" in versions[0].texts[0].content
    assert versions[0].amendment_note["id_norma"] == "BOE-A-2022-22292"


def test_scale_tables_are_rendered_row_wise():
    content = _unit(_parse(), "tv.ci_2.a63").versions[-1].texts[0].content
    assert "Base liquidable Hasta euros | Tipo aplicable Porcentaje" in content
    assert "0 | 9,50" in content
    assert "300.000,00 | 24,50" in content
    # Text is authentic Spanish, not a translation.
    assert _unit(_parse(), "tv.ci_2.a63").versions[-1].texts[0].lang == "es"


def test_repeated_block_titles_get_distinct_citations():
    # BOE distinguishes these only by block id; the loader reconciles units by
    # national_id OR citation, so a shared citation would silently merge two
    # different transitional provisions into one unit.
    doc = _parse()
    first = _unit(doc, "tv.ci_2.dtprimera")
    second = _unit(doc, "tv.ci_2.dtprimera_2")
    assert first.citation == "LIRPF Disposición transitoria primera"
    assert second.citation == "LIRPF Disposición transitoria primera (2)"
    citations = [unit.citation for unit in doc.instruments[0].units]
    assert len(citations) == len(set(citations)), "citations must be unique within an act"
    # The disambiguated citation is what the version carries too.
    assert second.versions[0].citation_label == "LIRPF Disposición transitoria primera (2)"


def test_error_envelope_raises_instead_of_parsing_empty_data():
    with pytest.raises(ValueError, match="status 404"):
        parse_boe_xml(ERROR_PAYLOAD, _ref(), _snapshot())


def test_adapter_constructs_with_zero_args_and_declares_its_source():
    adapter = EsAdapter()
    assert adapter.jurisdiction == "ES"
    assert adapter.default_source_code == "ES-BOE"


def test_adapter_expands_to_nothing_because_one_fetch_is_the_whole_act():
    assert EsAdapter().expand(_parse()) == []


@pytest.mark.parametrize(
    ("citation", "expected"),
    [
        ("LIRPF art. 63", "BOE-A-2006-20764"),
        ("Ley 35/2006", "BOE-A-2006-20764"),
        ("LGSS art. 19", "BOE-A-2015-11724"),
        ("BOE-A-2011-18161", "BOE-A-2011-18161"),
    ],
)
def test_resolver_maps_citations_to_boe_ids(citation, expected):
    refs = EsResolver().resolve(CitationRef(jurisdiction="ES", citation=citation), date(2025, 7, 1))
    assert [ref.source_id for ref in refs] == [expected]
    assert refs[0].source_code == "ES-BOE"
    assert refs[0].source_type == "instrument"


def test_resolver_rejects_unknown_citations():
    with pytest.raises(ValueError, match="Unknown ES act"):
        EsResolver().resolve(CitationRef(jurisdiction="ES", citation="Ley del Cine"), date(2025, 7, 1))


def test_canary_facts_are_declared_and_dated():
    facts = EsAdapter().canary_facts()
    assert facts
    assert all(fact.reason for fact in facts)
    savings = next(fact for fact in facts if "66" in fact.citation)
    assert savings.assert_latest_start_gte == date(2024, 12, 22)
