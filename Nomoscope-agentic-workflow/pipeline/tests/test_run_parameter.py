"""run_parameter on an in-memory record, with and without the queue (ADR 0004)."""

from __future__ import annotations

from datetime import date

import pytest
from nomoscope_workflow.config import WorkflowConfig
from nomoscope_workflow.pipeline import run_parameter
from nomoscope_workflow.schema import (
    ItemStatus,
    ParameterInformation,
    ParameterRecord,
    ParameterValue,
    Routing,
    SourceType,
)
from nomoscope_workflow.tracing import setup_tracing


def _offline_cfg():
    """A config that cannot reach any DB: the run must not need one."""
    return WorkflowConfig(
        database_url="postgresql://nobody@127.0.0.1:1/nothing",
        model="mock/extractor",
        critique_model="mock/extractor",
        tracing_enabled=False,
        scout="off",
    )


def test_run_parameter_takes_a_record_and_can_skip_the_queue(capsys):
    """run_parameter(cfg, tracer, record, as_of, enqueue=False) returns the item without writing.

    A national-team-sourced value is routed before any retrieval, so this
    exercises the whole record -> item path with no DB at all; record_run_safe
    only prints its warning.
    """
    record = ParameterRecord(
        information=ParameterInformation(
            country="FR",
            model_target="euromod://FR/nt_fr/def_const/$nt_test",
            value_type="scalar",
            unit="/1",
        ),
        values=[ParameterValue(value=0.45, valid_from=date(2024, 1, 1), source_type=SourceType.NATIONAL_TEAM)],
    )
    cfg = _offline_cfg()
    item = run_parameter(
        cfg,
        setup_tracing(cfg),
        record,
        date(2025, 7, 1),
        parameter_ref="euromod://FR/nt_fr/def_const/$nt_test",
        enqueue=False,
    )
    assert item.routing == Routing.NATIONAL_TEAM_SOURCE
    assert item.id == "fr_euromod_fr_nt_fr_def_const_nt_test_2025"
    assert item.system_year == 2025
    assert item.parameter_ref == "euromod://FR/nt_fr/def_const/$nt_test"
    assert item.status == ItemStatus.PENDING
    assert "not recorded" in capsys.readouterr().out  # record_run_safe stayed best-effort

    # parameter_ref defaults to the record's model_target
    assert (
        run_parameter(cfg, setup_tracing(cfg), record, date(2025, 7, 1), enqueue=False).parameter_ref
        == record.information.model_target
    )


def test_run_parameter_with_enqueue_fails_when_the_queue_is_unreachable():
    """The queue is rows: no DB, no item — never a silent file fallback."""
    record = ParameterRecord(
        information=ParameterInformation(
            country="FR", model_target="euromod://FR/test", value_type="scalar", unit="/1"
        ),
        values=[ParameterValue(value=0.45, valid_from=date(2024, 1, 1), source_type=SourceType.NATIONAL_TEAM)],
    )
    cfg = _offline_cfg()
    with pytest.raises(Exception):
        run_parameter(cfg, setup_tracing(cfg), record, date(2025, 7, 1))
