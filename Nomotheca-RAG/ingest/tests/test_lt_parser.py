"""Parser and adapter tests for the Lithuanian TAR payloads (inline fixtures)."""

import json
from datetime import date
from uuid import uuid4

import pytest

from nomotheca_ingest.countries.lt.adapter import LtAdapter
from nomotheca_ingest.countries.lt.parser import _header_official_nr, parse_tar_json
from nomotheca_ingest.countries.lt.resolver import LtResolver
from nomotheca_ingest.core.ir import CitationRef, Snapshot, SourceRef


DOCUMENT_PAYLOAD = json.dumps(
    {
        "_data": [
            {
                "dokumento_id": "TAR.C677663D2202",
                "tar_kodas": "1021010ISTA0IX-1007",
                "rusis": "Įstatymas",
                "atv_dok_nr": "IX-1007",
                "pavadinimas": "Lietuvos Respublikos gyventojų pajamų mokesčio įstatymas",
                "priimtas": "2002-07-02",
                "paskelbta_tar": "2002-07-19",
                "galioj_busena": "galioja",
                "nuoroda": "https://e-tar.lt/portal/lt/legalAct/TAR.C677663D2202",
            }
        ]
    }
).encode()

INDEX_PAYLOAD = json.dumps(
    {
        "_data": [
            {
                "dokumento_id": "TAR.C677663D2202",
                "suvestines_id": "oldOldOld1",
                "galioja_nuo": "2020-01-01T00:00:00",
                "galioja_iki": "2020-12-31T00:00:00",
            },
            {
                "dokumento_id": "TAR.C677663D2202",
                "suvestines_id": "ExnKtBqZbP",
                "galioja_nuo": "2024-01-01T00:00:00",
                "galioja_iki": "2024-05-30T00:00:00",
            },
            {
                "dokumento_id": "TAR.C677663D2202",
                "suvestines_id": "hhPqGFmNta",
                "galioja_nuo": "2025-01-02T00:00:00",
                "galioja_iki": None,
            },
        ]
    }
).encode()

CONSOLIDATION_TEXT = """LIETUVOS RESPUBLIKOS

Suvestinė redakcija nuo 2024-01-01 iki 2024-05-30

Įstatymas paskelbtas: Žin. 2002, Nr. 73-3085, i. k. 1021010ISTA0IX-1007

Nauja įstatymo redakcija nuo 2012-01-01:
Nr. XI-1772, 2011-12-01, Žin., 2011, Nr. 155-7353 (2011-12-20)

LIETUVOS RESPUBLIKOS
GYVENTOJŲ PAJAMŲ MOKESČIO
ĮSTATYMAS

2002 m. liepos 2 d. Nr. IX-1007 Vilnius


I SKYRIUS
BENDROSIOS NUOSTATOS

6 straipsnis. Pajamų mokesčio tarifai
1. Pajamų mokesčio tarifas – 20 procentų, jeigu šiame straipsnyje nenustatyta kitaip.


IV SKYRIUS
NEAPMOKESTINAMOSIOS PAJAMOS

20 straipsnis. Neapmokestinamasis pajamų dydis
1. MNPD negali būti didesnis negu 8 964 eurai.
"""

CONSOLIDATION_PAYLOAD = json.dumps(
    {
        "_data": [
            {
                "dokumento_id": "TAR.C677663D2202",
                "suvestines_id": "ExnKtBqZbP",
                "galioja_nuo": "2024-01-01T00:00:00",
                "galioja_iki": "2024-05-30T00:00:00",
                "nuoroda": "https://e-tar.lt/portal/lt/legalAct/TAR.C677663D2202/ExnKtBqZbP",
                "tekstas_lt": CONSOLIDATION_TEXT,
            }
        ]
    }
).encode()


def _ref(source_id: str, source_type: str) -> SourceRef:
    return SourceRef(jurisdiction="LT", source_code="LT-TAR", source_id=source_id, source_type=source_type)


def _snapshot(ref: SourceRef) -> Snapshot:
    return Snapshot(
        id=uuid4(),
        source_code=ref.source_code,
        url="https://get.data.gov.lt/datasets/gov/lrsk/teises_aktai/Suvestine",
        http_status=200,
        content_type="application/json",
        content_hash="0" * 64,
        raw_content=b"{}",
    )


def test_document_parses_instrument_skeleton_and_index_child_ref():
    ref = _ref("TAR.C677663D2202", "instrument")
    doc = parse_tar_json(DOCUMENT_PAYLOAD, ref, _snapshot(ref))
    instrument = doc.instruments[0]
    assert instrument.national_id == "IX-1007"
    assert instrument.instrument_type == "istatymas"
    assert instrument.title["lt"].startswith("Lietuvos Respublikos gyventojų")
    assert instrument.eli == "https://e-tar.lt/portal/lt/legalAct/TAR.C677663D2202"
    assert instrument.adoption_date == date(2002, 7, 2)
    assert doc.metadata["child_refs"] == [
        {
            "source_id": "TAR.C677663D2202/asr",
            "source_type": "consolidation_index",
            "title": "suvestinės redakcijos",
        }
    ]


def test_index_skips_consolidations_before_euromod_window():
    ref = _ref("TAR.C677663D2202/asr", "consolidation_index")
    doc = parse_tar_json(INDEX_PAYLOAD, ref, _snapshot(ref))
    source_ids = [child["source_id"] for child in doc.metadata["child_refs"]]
    assert source_ids == ["TAR.C677663D2202/ExnKtBqZbP", "TAR.C677663D2202/hhPqGFmNta"]
    assert doc.metadata["skipped_before_window"] == 1


def test_consolidation_splits_articles_with_validity_and_citations():
    ref = _ref("TAR.C677663D2202/ExnKtBqZbP", "consolidation")
    snapshot = _snapshot(ref)
    doc = parse_tar_json(CONSOLIDATION_PAYLOAD, ref, snapshot)
    instrument = doc.instruments[0]
    assert instrument.national_id == "IX-1007"
    assert instrument.title["lt"] == "LIETUVOS RESPUBLIKOS GYVENTOJŲ PAJAMŲ MOKESČIO ĮSTATYMAS"

    units = {unit.path: unit for unit in instrument.units}
    assert set(units) == {"str_6", "str_20"}
    art20 = units["str_20"]
    assert art20.unit_type == "straipsnis"
    assert art20.citation == "GPMĮ 20 straipsnis"
    assert art20.national_id == "IX-1007-20"
    assert art20.metadata["skyrius"] == "IV"

    version = art20.versions[0]
    assert version.valid_from == date(2024, 1, 1)
    # galioja_iki is the last day in force; the half-open range ends the next day.
    assert version.valid_to == date(2024, 5, 31)
    assert version.source_version_id == "TAR.C677663D2202/ExnKtBqZbP/str_20"
    assert version.fetch_snapshot_id == snapshot.id
    assert version.texts[0].lang == "lt"
    assert version.texts[0].content.startswith("20 straipsnis. Neapmokestinamasis pajamų dydis")
    assert "8 964 eurai" in version.texts[0].content


def test_header_official_nr_skips_gazette_and_amending_act_numbers():
    # The header cites the gazette (Nr. 73-3085) and an amending act (Nr. XI-1772)
    # before the enactment line; only "2002 m. ... Nr. IX-1007" is the act's own number.
    assert _header_official_nr(CONSOLIDATION_TEXT) == "IX-1007"


def test_adapter_expands_child_refs_into_work_items():
    ref = _ref("TAR.C677663D2202", "instrument")
    doc = parse_tar_json(DOCUMENT_PAYLOAD, ref, _snapshot(ref))
    work = LtAdapter().expand(doc)
    assert len(work) == 1
    assert work[0].ref.source_id == "TAR.C677663D2202/asr"
    assert work[0].ref.source_type == "consolidation_index"
    assert work[0].ref.source_code == "LT-TAR"


def test_resolver_maps_known_citations_to_consolidation_index():
    refs = LtResolver().resolve(
        CitationRef(jurisdiction="LT", citation="GPMĮ 20 straipsnis"), date(2025, 6, 30)
    )
    assert refs[0].source_id == "TAR.C677663D2202/asr"
    assert refs[0].source_code == "LT-TAR"

    with pytest.raises(ValueError, match="Unknown LT act"):
        LtResolver().resolve(CitationRef(jurisdiction="LT", citation="Nežinomas įstatymas"), date(2025, 6, 30))


def test_canary_asserts_2025_consolidation():
    facts = LtAdapter().canary_facts()
    assert facts[0].assert_latest_start_gte == date(2025, 1, 2)
