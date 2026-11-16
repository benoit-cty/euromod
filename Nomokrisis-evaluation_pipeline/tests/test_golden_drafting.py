"""The shared half of the golden drafters: one case-id rule for all of them."""

from __future__ import annotations

from datetime import date

from nomoscope_workflow.schema import (
    Bracket,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    Routing,
    SourceType,
)

from nomokrisis_eval import openfisca_golden as og
from nomokrisis_eval.build_dataset import DraftedTruth, to_golden_case
from nomokrisis_eval.golden_drafting import entry_case_id, golden_case_id

AS_OF = date(2025, 7, 1)
GROUP = "FR:tinkt_fr:tin_schedule"


def test_one_rule_for_scalars_groups_and_explicit_ids():
    target = "euromod://FR/tinkt_fr/def_const/$tin_upthres1"
    assert golden_case_id("FR", AS_OF, target) == "fr_tinkt_tin_upthres1_2025-07-01"
    # A group is slugged from its group id, bare or prefixed.
    assert golden_case_id("FR", AS_OF, f"group:{GROUP}") == golden_case_id("FR", AS_OF, GROUP)
    assert golden_case_id("FR", AS_OF, GROUP) == "fr_fr_tinkt_fr_tin_schedule_2025-07-01"
    # An explicit slug always wins.
    assert golden_case_id("FR", AS_OF, target, "bareme") == "fr_bareme_2025-07-01"
    assert entry_case_id({"model_target": target}, AS_OF, "FR") == golden_case_id("FR", AS_OF, target)
    assert entry_case_id({"group_id": GROUP, "id": "bareme"}, AS_OF, "FR") == "fr_bareme_2025-07-01"
    assert entry_case_id({}, AS_OF, "FR") is None


def _group_record() -> ParameterRecord:
    # paramdb.load_group_record's derived target: not the group id.
    return ParameterRecord(
        information=ParameterInformation(
            country="FR",
            model_target="euromod://FR/tinkt_fr/group/tin_schedule",
            value_type="bracket_schedule",
            unit="/1",
            label={"en": "IR barème"},
        ),
        values=[
            ParameterValue(
                value=[Bracket(threshold=0.0, rate=0.0)],
                valid_from=date(2025, 1, 1),
                source_type=SourceType.LEGISLATION,
            )
        ],
    )


def test_an_openfisca_group_entry_without_id_drafts_the_id_retirement_looks_for(monkeypatch):
    """The OpenFisca drafter slugged a group from its record's derived target
    while retirement slugged it from the group id: a group entry without `id`
    that stopped drafting left its old case behind for ever."""
    entry = {"group_id": GROUP, "openfisca_path": "impot_revenu.bareme", "component": "brackets"}
    monkeypatch.setattr(og, "load_record", lambda conn, e: (_group_record(), f"group:{GROUP}"))
    monkeypatch.setattr(og, "external_parameter", lambda *a, **k: {"id": 1, "commit": "abc1234"})
    monkeypatch.setattr(
        og, "schedule_at", lambda *a: ([Bracket(threshold=0.0, rate=0.0)], date(2025, 1, 1))
    )
    monkeypatch.setattr(og, "references_at", lambda *a: [])
    monkeypatch.setattr(og, "is_annually_indexed", lambda *a: False)

    outcome = og.draft_case(None, entry, AS_OF, "FR", "fr")
    assert outcome.case is not None
    assert outcome.case.id == entry_case_id(entry, AS_OF, "FR")


def test_the_llm_drafter_uses_the_same_rule():
    draft = DraftedTruth(found=True, value_brackets=[Bracket(threshold=0.0, rate=0.0)])
    case = to_golden_case(_group_record(), f"group:{GROUP}", AS_OF, "fr", draft, "anthropic/x")
    assert case.id == entry_case_id({"group_id": GROUP}, AS_OF, "FR")
    assert case.expected.routing == Routing.UNCHANGED
