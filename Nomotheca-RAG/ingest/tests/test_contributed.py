"""Tests for the contributed-document parse seam: bytes in, loadable IR out."""

from __future__ import annotations

from datetime import date
from uuid import uuid4

import pytest

from nomotheca_ingest.core.contributed import (
    NormLevel,
    canonical_url,
    content_hash,
    ingest_document,
    kinds_for,
    national_id_for,
    norm_level_for,
    parse_document,
    source_code_for,
    suggest,
    trust_class_for,
)
from nomotheca_ingest.core.extract import suggested_valid_from
from nomotheca_ingest.core.ir import Authenticity, SourceTrustClass

from pdf_fixture import make_pdf

MARKDOWN = b"""\
# Circulaire Unedic n. 2025-01

Le present texte precise les regles d'indemnisation.

## 1. Champ d'application

Il s'applique aux allocataires.

## 2. Montant

Le montant journalier est porte a 31,97 EUR.
"""

PLAIN_TEXT = (
    "Le montant journalier de l'allocation est porte a 31,97 EUR "
    "au 1er avril 2025.\n"
).encode("utf-8")

HTML_PAGE = b"""<html><head><title>BOFiP - IR - Bareme d'imposition</title></head><body>
<nav><a href="/">Accueil</a> <a href="/doc">Documentation fiscale</a></nav>
<main>
  <h1>IR - Bareme applicable aux revenus de 2024</h1>
  <p>Le premier taux est de 11 %.</p>
  <h2>I. Decote</h2>
  <p>La decote est de 889 EUR pour une personne seule.</p>
</main>
<footer>Mentions legales - plan du site - accessibilite</footer>
</body></html>"""


def _parse(raw: bytes, content_type: str, *, kind: str = "circulaire", url: str | None = None, **kwargs):
    national_id = national_id_for(raw, url)
    return parse_document(
        raw,
        content_type=content_type,
        jurisdiction="fr",
        lang="fr",
        title="Circulaire Unedic n. 2025-01",
        kind=kind,
        valid_from=date(2025, 4, 1),
        source_code=source_code_for("FR"),
        national_id=national_id,
        origin=url or "file:///tmp/circulaire.md",
        snapshot_id=uuid4(),
        **kwargs,
    )


# --- identity -------------------------------------------------------------


def test_an_uploaded_file_is_keyed_by_its_bytes() -> None:
    """No URL means no stable external identity: the sha256 is the identity."""
    doc = _parse(MARKDOWN, "text/markdown")
    instrument = doc.instruments[0]

    assert instrument.source_code == "FR-CONTRIB"
    assert instrument.national_id == f"file:{content_hash(MARKDOWN)}"
    assert doc.ref.source_id == instrument.national_id


def test_a_url_is_canonicalised_so_two_anchors_are_one_instrument() -> None:
    """A BOFiP page linked with two fragments must not become two instruments."""
    first = "https://BOFiP.impots.gouv.FR/bofip/1234-PGP.html/?identifiant=X#Titre_1"
    second = "https://bofip.impots.gouv.fr/bofip/1234-PGP.html?identifiant=X#Titre_9"

    assert canonical_url(first) == canonical_url(second)
    assert canonical_url(first) == "https://bofip.impots.gouv.fr/bofip/1234-PGP.html?identifiant=X"
    assert national_id_for(HTML_PAGE, first) == national_id_for(HTML_PAGE, second)


# --- kinds, levels and trust ---------------------------------------------


def test_the_kind_is_the_instrument_type_and_the_class_follows_from_it() -> None:
    """The reviewer names a kind; nobody ever states a trust level."""
    doc = _parse(MARKDOWN, "text/markdown", kind="circulaire")
    instrument = doc.instruments[0]

    assert instrument.instrument_type == "circulaire"
    assert instrument.source_trust_class == SourceTrustClass.GUIDANCE
    assert instrument.metadata["norm_level"] == NormLevel.ADMINISTRATIVE_GUIDANCE.value


def test_the_hierarchy_of_norms_maps_to_exactly_two_trust_classes() -> None:
    """Statute-level authority is evidence; guidance and 'other' are guidance."""
    assert trust_class_for("FR", "loi") == SourceTrustClass.EVIDENCE
    assert trust_class_for("FR", "decret") == SourceTrustClass.EVIDENCE
    assert trust_class_for("FR", "arrete") == SourceTrustClass.EVIDENCE
    assert trust_class_for("FR", "circulaire") == SourceTrustClass.GUIDANCE
    assert trust_class_for("FR", "doctrine") == SourceTrustClass.GUIDANCE
    # "other" must never grant evidence-level trust by accident.
    assert norm_level_for("FR", "other") == NormLevel.OTHER
    assert trust_class_for("FR", "other") == SourceTrustClass.GUIDANCE


def test_every_jurisdiction_offers_its_own_words_for_the_same_levels() -> None:
    """The kind list is one table, so the UI select and the mapping cannot drift."""
    assert list(kinds_for("FR")) == ["loi", "decret", "arrete", "circulaire", "doctrine", "other"]
    assert set(kinds_for("ES").values()) == set(NormLevel)
    # An unknown jurisdiction still gets a usable, country-neutral list.
    assert "guidance" in kinds_for("BE")


def test_an_unknown_kind_is_refused_by_name() -> None:
    with pytest.raises(ValueError, match="Unknown kind"):
        trust_class_for("FR", "ordonnance_royale")


# --- structure, validity, language ---------------------------------------


def test_markdown_units_carry_validity_language_and_authenticity() -> None:
    doc = _parse(MARKDOWN, "text/markdown")
    by_path = {u.path: u for u in doc.instruments[0].units}
    montant = by_path["circulaire_unedic_n_2025_01.sec_2"]
    version = montant.versions[0]
    text = version.texts[0]

    assert "31,97 EUR" in text.content
    assert text.lang == "fr"
    assert text.authenticity == Authenticity.AUTHENTIC
    assert version.valid_from == date(2025, 4, 1)


def test_an_unstructured_text_becomes_one_unit() -> None:
    """A circular with no headings still enters the store, whole."""
    doc = _parse(PLAIN_TEXT, "text/plain")
    units = doc.instruments[0].units

    assert len(units) == 1
    assert "31,97 EUR" in units[0].versions[0].texts[0].content


def test_html_keeps_the_main_block_and_drops_the_chrome() -> None:
    """Chunks must contain the doctrine, not the portal navigation and footer."""
    doc = _parse(HTML_PAGE, "text/html", kind="doctrine", url="https://bofip.impots.gouv.fr/x.html")
    instrument = doc.instruments[0]
    body = " ".join(
        text.content for unit in instrument.units for version in unit.versions for text in version.texts
    )

    assert "11 %" in body
    assert "889 EUR" in body
    assert "Accueil" not in body
    assert "Mentions legales" not in body
    # The page as fetched is kept once, beside the first unit text.
    html_columns = [
        text.content_html
        for unit in instrument.units
        for version in unit.versions
        for text in version.texts
    ]
    assert html_columns.count(HTML_PAGE.decode()) == 1


def test_html_headings_become_one_unit_per_section() -> None:
    doc = _parse(HTML_PAGE, "text/html", kind="doctrine", url="https://bofip.impots.gouv.fr/x.html")
    paths = [u.path for u in doc.instruments[0].units]

    assert any(path.endswith("i_decote") for path in paths)


def test_a_pdf_with_headings_yields_several_units() -> None:
    pdf = make_pdf(
        ["1. Objet", "Le present texte fixe le montant.", "2. Montant", "Le montant est de 31,97 EUR."],
        title="Circulaire Unedic 2025-01",
    )
    doc = _parse(pdf, "application/pdf")

    assert [u.path for u in doc.instruments[0].units] == ["sec_1", "sec_2"]


def test_a_pdf_with_no_structure_yields_one_unit() -> None:
    pdf = make_pdf(["Le montant journalier est porte a 31,97 EUR au 1er avril 2025."])
    doc = _parse(pdf, "application/pdf")
    units = doc.instruments[0].units

    assert len(units) == 1
    assert "31,97 EUR" in units[0].versions[0].texts[0].content


# --- version keys ---------------------------------------------------------


def test_the_same_bytes_produce_the_same_version_key() -> None:
    """Re-adding an unchanged document reuses its version instead of stacking one."""
    first = _parse(MARKDOWN, "text/markdown")
    second = _parse(MARKDOWN, "text/markdown")

    assert _version_keys(first) == _version_keys(second)


def test_changed_bytes_produce_a_new_version_key() -> None:
    """A page updated in place becomes a new version; the loader closes the old one."""
    changed = MARKDOWN.replace(b"31,97", b"32,13")
    url = "https://unedic.example/circulaire"

    assert _version_keys(_parse(MARKDOWN, "text/markdown", url=url)) != _version_keys(
        _parse(changed, "text/markdown", url=url)
    )


def _version_keys(doc) -> set[str]:
    return {
        version.source_version_id
        for instrument in doc.instruments
        for unit in instrument.units
        for version in unit.versions
    }


# --- refusals -------------------------------------------------------------


def test_a_missing_validity_date_is_refused_before_anything_is_written() -> None:
    """No version enters the store with an invented legal date."""
    with pytest.raises(ValueError, match="in force from"):
        ingest_document(
            # An unusable URL: reaching the database at all would be the bug.
            database_url="postgresql://nobody@127.0.0.1:1/none",
            jurisdiction="FR",
            lang="fr",
            title="Circulaire Unedic",
            kind="circulaire",
            valid_from=None,
            file_path="/nonexistent.md",
        )


def test_contributing_needs_exactly_one_of_a_url_and_a_file(tmp_path) -> None:
    with pytest.raises(ValueError, match="exactly one"):
        suggest(url=None, file_path=None)


# --- suggestions ----------------------------------------------------------


def test_a_page_title_is_suggested_for_an_html_document(tmp_path) -> None:
    page = tmp_path / "bareme.html"
    page.write_bytes(HTML_PAGE)

    assert suggest(file_path=str(page))["title"] == "BOFiP - IR - Bareme d'imposition"


def test_pdf_metadata_supplies_the_suggested_title(tmp_path) -> None:
    pdf = tmp_path / "circulaire.pdf"
    pdf.write_bytes(make_pdf(["1. Objet", "Texte."], title="Circulaire Unedic 2025-01"))

    suggestion = suggest(file_path=str(pdf))
    assert suggestion["title"] == "Circulaire Unedic 2025-01"
    assert suggestion["valid_from"] == "2025-01-01"


def test_the_file_name_is_the_last_resort_title(tmp_path) -> None:
    note = tmp_path / "note-unedic.txt"
    note.write_bytes(PLAIN_TEXT)

    assert suggest(file_path=str(note))["title"] == "note-unedic.txt"


def test_a_date_in_a_title_or_a_url_prefills_the_validity_date() -> None:
    assert suggested_valid_from("Circulaire du 1er avril 2025", None) == date(2025, 4, 1)
    assert suggested_valid_from(None, "https://x/eli/arrete/2020/12/28/CCPD2036946A/jo/texte") == date(
        2020, 12, 28
    )
    assert suggested_valid_from("no date at all here", None) is None


# --- the statute a document implements ------------------------------------


def test_a_stated_link_becomes_one_implements_relation() -> None:
    """Provenance: the reviewer says which statute this document implements."""
    doc = _parse(MARKDOWN, "text/markdown", implements="JORFTEXT000051168007")

    assert len(doc.relations) == 1
    relation = doc.relations[0]
    assert relation.relation_type == "implements"
    assert relation.from_ref == doc.instruments[0].national_id
    assert relation.to_ref == "JORFTEXT000051168007"


def test_no_link_writes_no_relation() -> None:
    """'None' is a valid answer: a missing statute never blocks the upload."""
    assert _parse(MARKDOWN, "text/markdown").relations == []
