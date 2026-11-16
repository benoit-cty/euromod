"""The job-type table (``jobs.JOB_SPECS``) against everything else that spells it."""

from __future__ import annotations

import json
import re

from nomergon import cli, db, jobs


def _sql_job_type_lists() -> list[list[str]]:
    """Every literal job-type list in ops_schema.sql: the CHECKs and the upgrade guard."""
    sql = db.SCHEMA_SQL.read_text(encoding="utf-8")
    lists = re.findall(r"job_type IN \(([^)]*)\)", sql) + re.findall(r"unnest\(ARRAY\[([^\]]*)\]\)", sql)
    return [re.findall(r"'([^']+)'", body) for body in lists]


def test_every_sql_job_type_list_is_the_spec_table() -> None:
    lists = _sql_job_type_lists()
    assert len(lists) == 3, "the CREATE TABLE check, the upgrade's check and its guard"
    for found in lists:
        assert found == list(jobs.JOB_TYPES)


def test_derived_lists() -> None:
    assert jobs.JOB_TYPES == tuple(jobs.JOB_SPECS)
    assert set(jobs.PAYLOAD_MODELS) == set(jobs.JOB_TYPES)
    assert jobs.IN_PROCESS_JOB_TYPES == ("encode",)
    assert jobs.SINGLETON_JOB_TYPES == ("embed", "translate", "translate-params")
    assert jobs.default_priority("encode") == jobs.ENCODE_PRIORITY == 100
    assert jobs.default_priority("chat") == jobs.CHAT_PRIORITY == 50
    assert jobs.default_priority("workflow") == 0


def test_job_types_json_is_current() -> None:
    """The UI imports Nomergon-worker/job_types.json; regenerate with `nomergon job-types --write`."""
    assert cli.JOB_TYPES_JSON.read_text(encoding="utf-8") == cli.job_types_json()
    document = json.loads(cli.JOB_TYPES_JSON.read_text(encoding="utf-8"))
    assert [entry["name"] for entry in document["job_types"]] == list(jobs.JOB_TYPES)
