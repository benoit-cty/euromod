"""Spain's autonomous communities: the region table, its SQL mirrors, and the
parser/resolver behaviour that hangs off it (ADR 0003)."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from uuid import uuid4

import pytest

from nomotheca_ingest.countries.es.adapter import EsAdapter
from nomotheca_ingest.countries.es.parser import KNOWN_ACTS, parse_boe_xml
from nomotheca_ingest.countries.es.regions import (
    AUTONOMOUS_COMMUNITIES,
    by_code,
    by_nuts2,
    jurisdiction_for,
)
from nomotheca_ingest.countries.es.resolver import (
    _ALIASES,
    ELI_PATH_RE,
    EsResolver,
    boe_id_from_eli,
)
from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef

DB_DIR = Path(__file__).resolve().parents[2] / "db"
STATE_ACTS = {
    "BOE-A-2006-20764", "BOE-A-2007-6820", "BOE-A-2015-11724", "BOE-A-2021-21007", "BOE-A-2025-2576",
}


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------


def test_the_table_covers_the_nineteen_communities_with_unique_keys():
    assert len(AUTONOMOUS_COMMUNITIES) == 19
    for field in ("code", "nuts2", "name", "departamento"):
        values = [getattr(ac, field) for ac in AUTONOMOUS_COMMUNITIES]
        assert len(set(values)) == len(values), f"duplicate {field}"
    assert all(re.fullmatch(r"ES-[A-Z]{2}", ac.code) for ac in AUTONOMOUS_COMMUNITIES)
    assert all(re.fullmatch(r"ES\d{2}", ac.nuts2) for ac in AUTONOMOUS_COMMUNITIES)
    # The two digits EUROMOD embeds in parameter names, exactly the NUTS-2 set.
    assert {ac.nuts2[2:] for ac in AUTONOMOUS_COMMUNITIES} == {
        "11", "12", "13", "21", "22", "23", "24", "30", "41", "42", "43",
        "51", "52", "53", "61", "62", "63", "64", "70",
    }
    assert by_nuts2("ES24").code == "ES-AR"
    assert by_code("es-cn").nuts2 == "ES70"


def _sql_rows(path: Path) -> dict[str, dict]:
    pattern = re.compile(
        r"\('(ES-[A-Z]{2})', \(SELECT id FROM jurisdictions WHERE code = 'ES'\), "
        r"'([^']+)', '\{([^}]*)\}', '(\{[^']*\})'\)"
    )
    rows = {}
    for code, name, langs, metadata in pattern.findall(path.read_text(encoding="utf-8")):
        rows[code] = {"name": name, "langs": tuple(langs.split(",")), **json.loads(metadata)}
    return rows


@pytest.mark.parametrize(
    "sql", [DB_DIR / "seed.sql", DB_DIR / "migrations" / "0002_es_autonomous_communities.sql"]
)
def test_the_sql_mirrors_carry_exactly_the_table(sql: Path):
    """seed.sql and the migration are generated from the table; a hand edit on
    either side must fail here rather than desynchronise retrieval scoping."""
    rows = _sql_rows(sql)
    assert set(rows) == {ac.code for ac in AUTONOMOUS_COMMUNITIES}, sql.name
    for ac in AUTONOMOUS_COMMUNITIES:
        row = rows[ac.code]
        assert row["name"] == ac.name, (sql.name, ac.code)
        assert row["langs"] == ac.langs, (sql.name, ac.code)
        assert row["nuts2"] == ac.nuts2, (sql.name, ac.code)
        assert row["eli"] == ac.code.lower(), (sql.name, ac.code)
        assert row["boe_departamento"] == ac.departamento, (sql.name, ac.code)


# ---------------------------------------------------------------------------
# jurisdiction_for
# ---------------------------------------------------------------------------


def test_the_eli_segment_places_an_act_before_the_departamento_text():
    assert jurisdiction_for(
        url_eli="https://www.boe.es/eli/es-ga/dlg/2011/07/28/1",
        departamento="Whatever BOE wrote",
        ambito_codigo="2",
        default="ES",
    ) == "ES-GA"


def test_the_departamento_text_is_the_fallback_and_is_accent_insensitive():
    assert jurisdiction_for(
        url_eli=None, departamento="Comunidad Autonoma de Aragon", ambito_codigo="2", default="ES"
    ) == "ES-AR"


def test_state_acts_keep_the_default_jurisdiction():
    assert jurisdiction_for(
        url_eli="https://www.boe.es/eli/es/l/2006/11/28/35",
        departamento="Jefatura del Estado",
        ambito_codigo="1",
        default="ES",
    ) == "ES"


def test_an_unplaceable_autonomous_act_is_refused_rather_than_filed_under_es():
    with pytest.raises(ValueError, match="unknown region"):
        jurisdiction_for(
            url_eli=None, departamento="Comunidad Autónoma de Atlantis", ambito_codigo="2", default="ES"
        )


# ---------------------------------------------------------------------------
# Parser: a regional payload files under its community
# ---------------------------------------------------------------------------

REGIONAL_PAYLOAD = b"""<?xml version="1.0" encoding="utf-8"?>
<response>
  <status><code>200</code><text>ok</text></status>
  <data>
    <metadatos>
      <identificador>BOE-A-2023-2940</identificador>
      <ambito codigo="2">Auton&#243;mico</ambito>
      <departamento codigo="8140">Comunidad Aut&#243;noma de Canarias</departamento>
      <rango codigo="1300">Ley</rango>
      <fecha_disposicion>20221219</fecha_disposicion>
      <numero_oficial>5/2022</numero_oficial>
      <titulo>Ley 5/2022, de 19 de diciembre, de la renta canaria de ciudadan&#237;a.</titulo>
      <fecha_publicacion>20230203</fecha_publicacion>
      <estado_consolidacion codigo="3">Finalizado</estado_consolidacion>
      <url_eli>https://www.boe.es/eli/es-cn/l/2022/12/19/5</url_eli>
    </metadatos>
    <texto>
      <bloque id="a8" tipo="precepto" titulo="Art&#237;culo 8">
        <version id_norma="BOE-A-2023-2940" fecha_publicacion="20230203" fecha_vigencia="20230204">
          <p class="articulo">Art&#237;culo 8. Cuant&#237;a.</p>
          <p class="parrafo">La cuant&#237;a b&#225;sica se fija en la ley de presupuestos.</p>
        </version>
      </bloque>
    </texto>
  </data>
</response>
"""


def _ref(boe_id: str) -> SourceRef:
    return SourceRef(jurisdiction="ES", source_code="ES-BOE", source_id=boe_id, source_type="instrument")


def _snapshot(payload: bytes, boe_id: str) -> Snapshot:
    return Snapshot(
        id=uuid4(),
        source_code="ES-BOE",
        url=f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}",
        http_status=200,
        content_type="application/xml",
        content_hash="0" * 64,
        raw_content=payload,
    )


def test_a_regional_act_is_filed_under_its_community_with_a_region_qualified_citation():
    doc = parse_boe_xml(REGIONAL_PAYLOAD, _ref("BOE-A-2023-2940"), _snapshot(REGIONAL_PAYLOAD, "BOE-A-2023-2940"))
    instrument = doc.instruments[0]
    assert instrument.jurisdiction == "ES-CN"
    assert instrument.metadata["ambito_codigo"] == "2"
    assert instrument.units[0].citation == "Ley 5/2022 Canarias Artículo 8"


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("citation", "expected"),
    [
        ("Ley 3/2021 Asturias, artículo 14", "BOE-A-2021-13685"),
        ("Ley 3/2021 Aragón", "BOE-A-2021-10673"),
        ("ley 3/2021 aragon", "BOE-A-2021-10673"),
        ("Ley 14/2022 País Vasco art. 55", "BOE-A-2023-1405"),
        ("Ley Foral 15/2016", "BOE-A-2016-11671"),
        ("renta canaria de ciudadanía", "BOE-A-2023-2940"),
        ("https://www.boe.es/eli/es-ga/dlg/2011/07/28/1", "BOE-A-2011-18161"),
    ],
)
def test_region_qualified_aliases_resolve(citation: str, expected: str):
    refs = EsResolver(eli_lookup=_offline_eli).resolve(CitationRef(jurisdiction="ES", citation=citation), date(2025, 7, 1))
    assert [ref.source_id for ref in refs] == [expected]


def test_a_bare_regional_number_is_ambiguous_and_says_which_regions_share_it():
    with pytest.raises(ValueError, match="Ambiguous") as excinfo:
        EsResolver().resolve(CitationRef(jurisdiction="ES", citation="Ley 3/2021 artículo 14"), date(2025, 7, 1))
    assert "LEY 3/2021 ASTURIAS" in str(excinfo.value)
    assert "LEY 3/2021 ARAGON" in str(excinfo.value)


def test_state_aliases_still_resolve_by_bare_number():
    refs = EsResolver().resolve(CitationRef(jurisdiction="ES", citation="35/2006 art. 57"), date(2025, 7, 1))
    assert refs[0].source_id == "BOE-A-2006-20764"


def test_every_alias_target_has_a_short_citation_in_the_parser():
    missing = {boe_id for boe_id in _ALIASES.values() if boe_id not in KNOWN_ACTS}
    assert not missing, f"aliases resolve to acts the parser would cite by bare number: {missing}"


_ELI_PAGES = {
    "https://www.boe.es/eli/es-cn/l/2022/12/19/5/con": b"<html><head><title>BOE-A-2023-2940 Ley 5/2022</title></head></html>",
    "https://www.boe.es/eli/es-ga/dlg/2011/07/28/1/con": b"<html><head><title>BOE-A-2011-18161 DL 1/2011</title></head></html>",
    "https://www.boe.es/eli/es-as/l/2024/12/27/8/con": b"<html><head><title>BOE.es - Error 404</title></head></html>",
    "https://www.boe.es/eli/es-as/l/2024/12/27/8": b"<html><head><title>BOE-A-2025-3124 Ley 8/2024</title></head></html>",
    "https://www.boe.es/eli/es-xx/l/2000/01/01/1/con": b"<html><head><title>BOE.es - Error 404</title></head></html>",
    "https://www.boe.es/eli/es-xx/l/2000/01/01/1": b"<html><head><title>BOE.es - Error 404</title></head></html>",
}


def _offline_eli(url: str) -> bytes | None:
    return _ELI_PAGES.get(url)


def test_eli_paths_are_recognised_with_or_without_the_con_suffix():
    assert ELI_PATH_RE.search("https://www.boe.es/eli/es-cn/l/2022/12/19/5/con").group(1) == "es-cn/l/2022/12/19/5"
    assert ELI_PATH_RE.search("eli/es/l/2006/11/28/35").group(1) == "es/l/2006/11/28/35"
    assert ELI_PATH_RE.search("Ley 35/2006") is None


def test_a_consolidated_eli_resolves_to_its_boe_id():
    assert boe_id_from_eli("es-cn/l/2022/12/19/5", _offline_eli) == ("BOE-A-2023-2940", True)
    refs = EsResolver(eli_lookup=_offline_eli).resolve(
        CitationRef(jurisdiction="ES", citation="https://www.boe.es/eli/es-cn/l/2022/12/19/5/con"), date(2025, 7, 1)
    )
    assert refs[0].source_id == "BOE-A-2023-2940"


def test_a_published_but_unconsolidated_eli_is_refused_with_its_boe_id():
    """Regional budget laws: BOE publishes them (plain ELI resolves) but does
    not consolidate them (/con is a 404 page), and the consolidated API 404s
    on their id. The refusal names the id so the operator knows what exists."""
    assert boe_id_from_eli("es-as/l/2024/12/27/8", _offline_eli) == ("BOE-A-2025-3124", False)
    with pytest.raises(ValueError, match="BOE-A-2025-3124.*not consolidate"):
        EsResolver(eli_lookup=_offline_eli).resolve(
            CitationRef(jurisdiction="ES", citation="https://www.boe.es/eli/es-as/l/2024/12/27/8"), date(2025, 7, 1)
        )


def test_an_unknown_eli_is_an_unknown_act():
    with pytest.raises(ValueError, match="Unknown ES act"):
        EsResolver(eli_lookup=_offline_eli).resolve(
            CitationRef(jurisdiction="ES", citation="https://www.boe.es/eli/es-xx/l/2000/01/01/1"), date(2025, 7, 1)
        )


def test_one_canary_watches_a_regional_act():
    """A stale regional source must be detected the way a stale LIRPF is."""
    resolver = EsResolver()
    regional = [f for f in EsAdapter().canary_facts() if resolver._boe_id(f.citation) not in STATE_ACTS]
    assert regional, "no canary cites an autonomous-community act"
    assert all(f.assert_latest_start_gte and f.reason for f in regional)
