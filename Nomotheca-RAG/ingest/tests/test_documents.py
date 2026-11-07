"""Tests for the shared heading-driven document builder."""

from __future__ import annotations

from datetime import date
from uuid import uuid4

from nomotheca_ingest.core.documents import build_document, find_headings

MARKDOWN = """\
Preamble text before any heading.

# Circulaire n. 2025-01

## 1. Champ d'application

Le present texte s'applique aux allocataires.

### 1.1 Exclusions

Les travailleurs frontaliers sont exclus.

## 2. Montant

Le montant journalier est de 31,97 EUR.
"""

HTML_AS_TEXT = """\
<h1>BOFiP - IR - Bareme</h1>
Introduction du commentaire.
<h2>I. Bareme applicable</h2>
Le taux est de 11 %.
<h2>II. Decote</h2>
La decote est de 889 EUR.
"""


def _build(text: str, pattern: str, **kwargs):
    return build_document(
        text=text,
        jurisdiction="fr",
        source_code="FR-CONTRIB",
        instrument_type="circulaire",
        national_id="file:abc123",
        title="Circulaire Unedic",
        valid_from=date(2025, 4, 1),
        snapshot_id=uuid4(),
        citation_prefix="Circulaire Unedic",
        lang="fr",
        pattern=pattern,
        **kwargs,
    )


def test_markdown_headings_build_a_nested_unit_tree() -> None:
    """One unit per heading, nested by level, with the preamble kept."""
    ir = _build(MARKDOWN, "markdown")
    by_path = {u.path: u for u in ir.units}
    root = "circulaire_n_2025_01"

    assert "Preamble text" in by_path["preamble"].versions[0].texts[0].content
    assert by_path[f"{root}.sec_1.sec_1_1"].parent_path == f"{root}.sec_1"
    assert by_path[f"{root}.sec_1"].is_container
    assert "31,97 EUR" in by_path[f"{root}.sec_2"].versions[0].texts[0].content
    # The reviewer's title stands; the h1 is a section like any other heading.
    assert ir.title["fr"] == "Circulaire Unedic"


def test_html_headings_are_the_same_shape_through_a_different_pattern() -> None:
    """h1-h6 in a page reduced to text express the same hierarchy as '#'."""
    ir = _build(HTML_AS_TEXT, "html")
    paths = [u.path for u in ir.units]

    assert [h.level for h in find_headings(HTML_AS_TEXT.splitlines(), "html")] == [1, 2, 2]
    assert "bofip_ir_bareme" in paths
    by_path = {u.path: u for u in ir.units}
    assert by_path["bofip_ir_bareme.i_bareme_applicable"].parent_path == "bofip_ir_bareme"
    assert "11 %" in by_path["bofip_ir_bareme.i_bareme_applicable"].versions[0].texts[0].content


def test_numbered_paragraphs_are_expressible_as_a_pattern() -> None:
    """A circular with decimal numbering and no other markup still splits."""
    text = "1. Objet\nLe present texte fixe le plafond.\n2. Montant\nLe plafond est de 3 925 EUR.\n"
    ir = _build(text, "numbered")

    assert [u.path for u in ir.units] == ["sec_1", "sec_2"]
    assert "3 925 EUR" in ir.units[1].versions[0].texts[0].content


def test_a_numbered_table_row_is_not_a_heading_and_a_numbered_paragraph_is_text() -> None:
    """Cnav circular 2025-13: the couple ceiling's figures and section 2's sentence survive."""
    text = (
        "1. Plafonds de ressources de l'ASI à compter du 1er avril 2025\n"
        "Bénéficiaire Montant annuel Montant mensuel\n"
        "Personne seule 10 978,30 € 914,85 €\n"
        "Couple (bénéficiaire et son conjoint,\n"
        "pacte civil de solidarité)\n"
        "19 212,03 € 1 601 €\n"
        "\n"
        "2. Montant maximal de l'ASI lorsque le conjoint ne bénéficie ni de l'ASI, ni de l'Aspa\n"
        "Le montant de l'allocation servie ne peut excéder le plafond.\n"
    )
    ir = _build(text, "numbered")

    assert [u.path for u in ir.units] == ["sec_1", "sec_2"]
    first, second = (u.versions[0].texts[0].content for u in ir.units)
    assert "19 212,03 € 1 601 €" in first
    assert second.startswith("2. Montant maximal de l'ASI lorsque le conjoint")


def test_a_text_with_no_headings_is_one_unit() -> None:
    """An unstructured circular still enters the store, whole."""
    text = "Le montant journalier de l'allocation est porte a 31,97 EUR au 1er avril 2025.\n"
    ir = _build(text, "markdown")

    assert len(ir.units) == 1
    assert ir.units[0].path == "preamble"
    assert ir.units[0].versions[0].texts[0].content.strip() == text.strip()


def test_the_version_key_is_what_re_ingestion_deduplicates_on() -> None:
    """Every unit shares one key, so a re-run reuses versions rather than stacking."""
    ir = _build(MARKDOWN, "markdown", version_key="file:abc123@deadbeef")

    keys = {v.source_version_id for u in ir.units for v in u.versions}
    assert keys == {"file:abc123@deadbeef"}


def test_a_heading_with_nothing_under_it_is_not_a_unit() -> None:
    """Portal widgets mint <h2>-shaped chrome; an empty heading is not a unit.

    Regression: the Unédic circular page wraps a search widget and a share
    widget inside its <main>, and their titles became legal units with no
    text, no chunk and a citation string nobody could ever cite.
    """
    page = (
        "<h1>Circulaire n. 2023-05</h1>\n"
        "Transmission des taux de conversion pour le 3e trimestre 2023.\n"
        "<h2>Moteur de recherche</h2>\n"
        "<h3>Recherches populaires</h3>\n"
        "<h2>Partager cette page</h2>\n"
    )

    ir = _build(page, "html")

    assert [u.path for u in ir.units] == ["circulaire_n_2023_05"]


def test_an_empty_heading_keeps_its_place_when_it_has_text_below_it() -> None:
    """Pruning is about text, not about a section having a body of its own."""
    page = (
        "<h1>Circulaire</h1>\n"
        "<h2>Chapitre I</h2>\n"
        "<h3>Article 1</h3>\n"
        "Le montant est de 31,97 EUR.\n"
    )

    ir = _build(page, "html")
    by_path = {u.path: u for u in ir.units}

    assert set(by_path) == {"circulaire", "circulaire.chapitre_i", "circulaire.chapitre_i.article_1"}
    assert by_path["circulaire.chapitre_i"].is_container


def test_table_rows_starting_with_a_count_stay_in_their_section() -> None:
    """Caf EAJE barème 2025: «1 enfant 0,0619% 0,0516%» … is a table, not ten sections."""
    rows = "".join(f"{n} enfant{'s' if n > 1 else ''} 0,0{n}% 0,0{n}%\n" for n in range(1, 11))
    text = (
        "1) Le barème selon le taux d'effort 2025 est maintenu comme suit :\n"
        "Nombre d'enfants Accueil collectif et Micro-crèche Accueil familial ou parental\n"
        + rows
        + "2) Le plancher : son montant est revalorisé à 801 € pour l'année 2025.\n"
        "3. Le plafond\n"
        "Son montant est maintenu à 7 000 €.\n"
    )
    ir = _build(text, "numbered")

    contents = [u.versions[0].texts[0].content for u in ir.units]
    table = next(c for c in contents if "Accueil collectif" in c)
    assert "1 enfant 0,01% 0,01%" in table and "10 enfants 0,010% 0,010%" in table
    assert any("7 000 €" in c and "Accueil collectif" not in c for c in contents)


def test_a_line_starting_with_a_date_or_a_year_is_not_a_section() -> None:
    """DSS/2B/2024/181: the AF ceiling table stays under its title."""
    text = (
        "1. Plafonds de ressources applicables pour l'attribution des allocations familiales\n"
        "Plafonds applicables du 1er janvier au\n"
        "31 décembre 2025 (à comparer au revenu net catégoriel de l'année 2023)\n"
        "2 enfants ≤ 78 565 ≤ 104 719 > 104 719\n"
        "2024 des plafonds de ressources d'attribution de certaines prestations\n"
        "2. Plafonds du complément familial\n"
        "3 enfants 43 946 53 758\n"
    )
    ir = _build(text, "numbered")

    assert [u.path for u in ir.units] == ["sec_1", "sec_2"]
    first = ir.units[0].versions[0].texts[0].content
    assert "allocations familiales" in first and "78 565" in first and "2024 des plafonds" in first


def test_a_repeated_column_header_is_not_a_section_and_citations_stay_unique() -> None:
    """DSS/2B/2025/38: «0 à 3 ans 3 à 6 ans» headed six CMG tables; sharing one
    citation, they became one unit and the ASF amounts after them were lost."""
    table = "0 à 3 ans 3 à 6 ans 0 à 3 ans 3 à 6 ans\nCMG maximal 178,58 % 847,13 423,57\n" + "suite du tableau\n" * 3
    text = (
        "1 Le coefficient de revalorisation retenu correspond à l'inflation.\n"
        + table
        + table
        + "III.2 Allocation de soutien familial\nTaux partiel 42,20% 200,18\n"
        "5 Complément pour frais\nComplément forfaitaire pour frais 27,19 % 128,98\n"
    )
    ir = _build(text, "numbered")

    citations = [u.citation for u in ir.units]
    assert len(citations) == len(set(citations))
    assert not any("0 à 3 ans" in c for c in citations)
    assert any("200,18" in u.versions[0].texts[0].content for u in ir.units)


def test_two_headings_alike_get_two_citations() -> None:
    ir = _build("1. Objet\nPremier objet du texte.\n2. Champ\nDu texte.\n1. Objet\nSecond objet, en annexe.\n", "numbered")

    citations = [u.citation for u in ir.units]
    assert len(citations) == len(set(citations)) == 3


def test_footnote_numbers_that_start_over_are_not_sections() -> None:
    """Agirc-Arrco circular 2024-18 reads 1 | 1 2 3 | 1: its footnotes cut the
    2025 rate table into a section opening on «1 Plafond de sécurité sociale.»."""
    text = (
        "Paramètres Agirc-Arrco au 1er janvier 2025\n"
        "Par mois 3 925 € 3 925 € 31 400 €\n"
        "1 Plafond de sécurité sociale.\n"
        "Taux sur les tranches 1 et 2 des salaires\n"
        "Tranche 1 (≤ 1 PSS) 6,20 %1 3,72 %2 2,48 %2 7,87 % 4,72 % 3,15 %\n"
        "1 Taux de cotisations : il correspond à 127% du taux de calcul des points\n"
        "2 Sauf obligation née antérieurement au 2 janvier 1993.\n"
        "3 Sauf dispositions particulières applicables dans l'entreprise.\n"
        "1 Ce qui correspond pour 2025 à une limite de 188 400 € par an.\n"
    )
    ir = _build(text, "numbered")

    assert len(ir.units) == 1
    content = ir.units[0].versions[0].texts[0].content
    assert "Paramètres Agirc-Arrco" in content and "3,15 %" in content and "188 400" in content


def test_numbered_sections_keep_their_place_before_a_footnote_run() -> None:
    text = (
        "1 Objet de la circulaire et champ d'application\n"
        "Le présent texte précise les montants applicables.\n"
        "2 Montants revalorisés au 1er avril\n"
        "Le montant forfaitaire mensuel est porté à 646,52 € à compter du 1er avril 2025.\n"
        "1 Décret du 28 mars 2025.\n"
    )
    ir = _build(text, "numbered")

    assert [u.path for u in ir.units] == ["sec_1", "sec_2"]
    assert "Décret du 28 mars" in ir.units[1].versions[0].texts[0].content
