"""Regressions from the 2026-09-08 eval review (eval-20260908T143801Z…luna)."""

from nomoscope_workflow.schema import Lineage, ParameterValue

from nomokrisis_eval.openfisca_golden import _is_pre_indexation_reference
from nomokrisis_eval.scoring import _on_parameter_basis, values_equal


class _Item:
    def __init__(self, raw: str | None):
        self.current_value = (
            ParameterValue(value=8964.0, valid_from="2024-01-01", lineage=Lineage(model_answer=raw))
            if raw is not None
            else None
        )


def test_a_bare_proposal_takes_the_stored_values_period():
    # The pipeline proposes 8964.0 for a parameter EUROMOD holds as `8964#y`;
    # the golden case states the law's `747#m`. Completed with the stored
    # basis, the cross-period comparison the case was written for happens.
    assert _on_parameter_basis(8964.0, _Item("8964#y")) == "8964.0#y"
    assert values_equal(_on_parameter_basis(8964.0, _Item("8964#y")), "747#m")
    assert not values_equal(8964.0, "747#m")


def test_values_without_a_stored_period_or_not_scalars_are_left_alone():
    assert _on_parameter_basis(8964.0, _Item("8964")) == 8964.0
    assert _on_parameter_basis(8964.0, _Item(None)) == 8964.0
    assert _on_parameter_basis("$PSS * 4", _Item("8964#y")) == "$PSS * 4"
    assert _on_parameter_basis([1, 2], _Item("8964#y")) == [1, 2]
    assert _on_parameter_basis(True, _Item("8964#y")) is True


def test_openfisca_pre_indexation_references_do_not_make_a_case_answerable():
    # OpenFisca labels the base article of an annually indexed threshold
    # "(seuils avant revalorisation)"; the year's amount is in the companion
    # reference (a ministerial letter with no Legifrance id).
    assert _is_pre_indexation_reference(
        {"title": "Article L136-8 du Code de la sécurité sociale (seuils avant revalorisation)"}
    )
    assert not _is_pre_indexation_reference({"title": "Article 197 du Code général des impôts"})
    assert not _is_pre_indexation_reference({"title": None})
