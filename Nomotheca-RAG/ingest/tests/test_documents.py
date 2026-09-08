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
