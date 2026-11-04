"""KALI collective agreements read through the FR DILA parser (ADR 0006)."""

from __future__ import annotations

import io
import json
import tarfile
from uuid import uuid4

import pytest

from nomotheca_ingest.core.ir import Snapshot, SourceRef, SourceTrustClass
from nomotheca_ingest.countries.fr import kali
from nomotheca_ingest.countries.fr.adapter import FR_URL_SOURCE, FrAdapter
from nomotheca_ingest.countries.fr.kali import KaliStore, document_json, kali_url, tree_paths
from nomotheca_ingest.countries.fr.parser import parse_dila_json

# Trimmed from the 13 Jul 2025 global dump: ANI du 17 novembre 2017, art. 37.
ARTICLE_37 = """<?xml version="1.0" encoding="UTF-8"?>
<ARTICLE>
<META>
<META_COMMUN><ID>KALIARTI000036731900</ID><ORIGINE>KALI</ORIGINE><NATURE>Article</NATURE></META_COMMUN>
<META_SPEC><META_ARTICLE>
<NUM>37</NUM><TITRE>Contributions d'équilibre</TITRE><ETAT>VIGUEUR_ETEN</ETAT>
<DATE_DEBUT>2019-01-01</DATE_DEBUT><DATE_FIN>2999-01-01</DATE_FIN>
</META_ARTICLE></META_SPEC>
</META>
<CONTEXTE>
<TEXTE cid="KALITEXT000036731682" date_publi="2999-01-01" date_signature="2017-11-17" nature="Accord national interprofessionnel">
<TITRE_TXT c_titre_court="Régime AGIRC-ARRCO de retraite complémentaire" debut="2019-01-01" fin="2999-01-01" id_txt="KALITEXT000036731682">Accord national interprofessionnel du 17 novembre 2017 relatif au régime AGIRC-ARRCO de retraite complémentaire</TITRE_TXT>
</TEXTE>
</CONTEXTE>
<BLOC_TEXTUEL>
<CONTENU>
<p align="left">Afin de financer plus particulièrement les charges d'anticipation du régime, une contribution d'équilibre général, aux taux de :<br/>
– 2,15 % sur la tranche 1 des revenus définie à l'article 32 ;<br/>
– 2,70 % sur la tranche 2 des revenus définie à l'article 32.</p>
</CONTENU>
</BLOC_TEXTUEL>
</ARTICLE>
""".encode()

TEXT_VERSION = """<?xml version="1.0" encoding="UTF-8"?>
<TEXTE_VERSION>
<META>
<META_COMMUN><ID>KALITEXT000036731682</ID><ORIGINE>KALI</ORIGINE><NATURE>Accord national interprofessionnel</NATURE></META_COMMUN>
<META_SPEC>
<META_TEXTE_CHRONICLE><CID>KALITEXT000036731682</CID><NOR>ASET1850031M</NOR><DATE_PUBLI>2999-01-01</DATE_PUBLI><DATE_TEXTE>2017-11-17</DATE_TEXTE></META_TEXTE_CHRONICLE>
<META_TEXTE_VERSION><TITREFULL>Accord national interprofessionnel du 17 novembre 2017 relatif au régime AGIRC-ARRCO de retraite complémentaire</TITREFULL></META_TEXTE_VERSION>
</META_SPEC>
</META>
</TEXTE_VERSION>
""".encode()

TEXT_STRUCT = """<?xml version="1.0" encoding="UTF-8"?>
<TEXTEKALI>
<META><META_COMMUN><ID>KALITEXT000036731682</ID><NATURE>Accord national interprofessionnel</NATURE></META_COMMUN></META>
<STRUCT>
<LIEN_ART debut="2019-01-01" etat="VIGUEUR_ETEN" fin="2999-01-01" id="KALIARTI000036731694" num="1er" origine="KALI"/>
<LIEN_SECTION_TA cid="KALISCTA000036731704" debut="2019-01-01" etat="VIGUEUR_ETEN" fin="2999-01-01" id="KALISCTA000036731704" niv="1">Chapitre III Cotisations et recouvrement</LIEN_SECTION_TA>
</STRUCT>
</TEXTEKALI>
""".encode()


def _parse(source_id: str, payload: bytes):
    ref = SourceRef(jurisdiction="FR", source_code="FR-KALI", source_id=source_id, source_type="instrument")
    snapshot = Snapshot(
        id=uuid4(),
        source_code="FR-KALI",
        url=kali_url(source_id, "20250713-140000"),
        http_status=200,
        content_type="application/json",
        content_hash="test",
        raw_content=payload,
    )
    return parse_dila_json(payload, ref, snapshot)


def test_tree_paths_follow_the_dump_layout():
    assert tree_paths("KALIARTI000036731900") == ["article/KALI/ARTI/00/00/36/73/19/KALIARTI000036731900.xml"]
    assert tree_paths("KALITEXT000036731682") == [
        "texte/version/KALI/TEXT/00/00/36/73/16/KALITEXT000036731682.xml",
        "texte/struct/KALI/TEXT/00/00/36/73/16/KALITEXT000036731682.xml",
    ]
    with pytest.raises(ValueError):
        tree_paths("KALICONT000046709421")


def test_converted_xml_has_the_tricoteuses_shape():
    data = json.loads(document_json([ARTICLE_37]))
    texte = data["CONTEXTE"]["TEXTE"]
    assert texte["@cid"] == "KALITEXT000036731682"
    assert texte["TITRE_TXT"]["#text"].startswith("Accord national interprofessionnel")
    # CONTENU stays HTML, as the parser expects.
    assert "<br />" in data["BLOC_TEXTUEL"]["CONTENU"]


def test_an_agreement_article_is_evidence_with_its_own_title():
    doc = _parse("KALIARTI000036731900", document_json([ARTICLE_37]))
    (instrument,) = doc.instruments
    assert instrument.national_id == "KALITEXT000036731682"
    assert instrument.instrument_type == "collective_agreement"
    assert instrument.source_trust_class == SourceTrustClass.EVIDENCE
    (unit,) = instrument.units
    assert unit.citation.endswith("AGIRC-ARRCO de retraite complémentaire, art. 37")
    (version,) = unit.versions
    assert version.valid_from.isoformat() == "2019-01-01" and version.valid_to is None
    assert "2,15 % sur la tranche 1" in version.texts[0].content


def test_an_agreement_text_merges_version_and_struct_and_expands():
    doc = _parse("KALITEXT000036731682", document_json([TEXT_VERSION, TEXT_STRUCT]))
    (instrument,) = doc.instruments
    assert instrument.instrument_type == "collective_agreement"
    assert instrument.title["fr"].startswith("Accord national interprofessionnel du 17 novembre 2017")
    assert instrument.adoption_date.isoformat() == "2017-11-17"
    assert [child["source_id"] for child in doc.metadata["child_refs"]] == [
        "KALIARTI000036731694",
        "KALISCTA000036731704",
    ]
    assert [w.ref.source_code for w in FrAdapter().expand(doc)] == ["FR-KALI", "FR-KALI"]


def test_kali_ids_are_their_own_source_and_whole_conventions_are_refused():
    adapter = FrAdapter()
    assert adapter.source_code_for("KALITEXT000036731682") == "FR-KALI"
    assert adapter.source_code_for("LEGIARTI000051521140") == "FR-LEGI"
    assert FR_URL_SOURCE.id_pattern.findall(
        "https://www.legifrance.gouv.fr/conv_coll/id/KALIARTI000036731900"
    ) == ["KALIARTI000036731900"]
    pattern, _hint = FR_URL_SOURCE.refusals[1]
    assert pattern.search("https://www.legifrance.gouv.fr/conv_coll/id/KALICONT000046709421")
    rebuilt = adapter.source_ref_from_url(kali_url("KALIARTI000036731900", "20250713-140000"), "FR-KALI")
    assert rebuilt.source_id == "KALIARTI000036731900" and rebuilt.source_type == "article"


def _dump(members: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for name, payload in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
    return buffer.getvalue()


def test_sync_applies_the_global_dump_then_newer_increments(tmp_path, monkeypatch):
    path = "kali/global/article/" + tree_paths("KALIARTI000036731900")[0].removeprefix("article/")
    dumps = {
        "Freemium_kali_global_20250713-140000.tar.gz": _dump({path: b"<old/>", "kali/global/conteneur/x.xml": b"c"}),
        "KALI_20250710-213429.tar.gz": _dump({"20250710-213429/" + path: b"<older/>"}),
        "KALI_20251102-213929.tar.gz": _dump({"20251102-213929/" + path: ARTICLE_37}),
    }
    store = KaliStore(root=tmp_path)
    monkeypatch.setattr(store.__class__, "_listing", lambda self: " ".join(dumps))

    def fake_apply(self, name):  # the real _apply, minus the HTTP download
        with tarfile.open(fileobj=io.BytesIO(dumps[name]), mode="r:gz") as archive:
            for member in archive:
                relative = kali._kept_relative(member.name)
                if relative and member.isfile():
                    target = self.tree / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.extractfile(member).read())

    monkeypatch.setattr(store.__class__, "_apply", fake_apply)
    report = store.sync()
    # The increment older than the global dump is already in it, and skipped.
    assert report == {"global": "20250713-140000", "increments": ["20251102-213929"]}
    files, applied = store.read("KALIARTI000036731900")
    assert files == [ARTICLE_37] and applied == "20251102-213929"
    assert not (tmp_path / "global" / "conteneur").exists()


def test_a_version_replaced_the_day_it_started_is_skipped():
    same_day = ARTICLE_37.replace(b"<DATE_FIN>2999-01-01</DATE_FIN>", b"<DATE_FIN>2019-01-01</DATE_FIN>")
    doc = _parse("KALIARTI000036731900", document_json([same_day]))
    assert doc.instruments == [] and doc.metadata["skipped"] == "never_in_force"


def test_an_annex_article_is_qualified_by_its_annex():
    in_annex = ARTICLE_37.replace(
        b"</TITRE_TXT>",
        b"</TITRE_TXT><TM><TITRE_TM id=\"KALISCTA1\">Annexes</TITRE_TM><TM>"
        b"<TITRE_TM id=\"KALISCTA2\">Annexe A Sp\xc3\xa9cificit\xc3\xa9s propres</TITRE_TM></TM></TM>",
    )
    (unit,) = _parse("KALIARTI000036731900", document_json([in_annex])).instruments[0].units
    assert unit.path == "annexe_a_art_37"
    assert unit.citation.endswith(", annexe A, art. 37")
    (plain,) = _parse("KALIARTI000036731900", document_json([ARTICLE_37])).instruments[0].units
    assert plain.path == "art_37"
