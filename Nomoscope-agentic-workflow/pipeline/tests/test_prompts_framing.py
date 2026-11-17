"""What the model is shown: the frame query and the prompt's notes."""

from __future__ import annotations

from types import SimpleNamespace

from nomoscope_workflow.framing import _clean_query_text
from nomoscope_workflow.prompts import _average_note


def test_a_law_language_query_keeps_the_names_in_quotes_and_parentheses():
    text = (
        "Le montant de la « prime de fin d’année » (également appelée prime exceptionnelle de Noël) "
        "versé aux bénéficiaires du RSA (Revenu de Solidarité Active), commentaire « Calculate end of year bonus » "
        "(Table 2.52)"
    )
    query = _clean_query_text(text, "fr")
    assert "prime de fin d’année" in query and "prime exceptionnelle de Noël" in query
    assert "Revenu de Solidarité Active" in query
    assert "Calculate" not in query and "2.52" not in query
    assert "Revenu" not in _clean_query_text(text)  # an English record drops spans as before


def test_an_average_labelled_amount_is_proposed_as_the_amount_in_force():
    fya = SimpleNamespace(label={"en": "Base amount - FYA"}, short_label=None, description={})
    plain = SimpleNamespace(label={"en": "Base amount"}, short_label=None, description={})
    held = SimpleNamespace(lineage=SimpleNamespace(model_answer="938.64"))
    formula = SimpleNamespace(lineage=SimpleNamespace(model_answer="(498.39*9+514.64*3)/12#m"))
    assert "IN FORCE" in _average_note(fya, held)
    assert "IN FORCE" in _average_note(plain, formula)
    assert _average_note(plain, held) == ""
