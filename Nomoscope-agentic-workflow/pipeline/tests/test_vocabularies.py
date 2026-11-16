"""The unit and source-type vocabularies agree between Python and SQL — statically.

`params.edit_parameter()` validates a UI edit against lists written in SQL;
`paramdb.KNOWN_UNITS` and `schema.SourceType` are the Python side. The only
check used to need a live database (code audit 2.1); this one reads the SQL.
"""

from __future__ import annotations

import re
from pathlib import Path

from nomoscope_workflow import paramdb
from nomoscope_workflow.schema import SourceType

SQL = (Path(__file__).resolve().parents[1] / "db" / "params_schema.sql").read_text(encoding="utf-8")


def _sql_list(field: str) -> set[str]:
    """The values edit_parameter() accepts for `field` (its NOT IN list)."""
    match = re.search(r"p_field = '" + field + r"'.*?NOT IN\s*\(([^)]*)\)", SQL, re.S)
    assert match, field
    return set(re.findall(r"'([^']+)'", match.group(1)))


def test_units_agree():
    assert set(paramdb.KNOWN_UNITS) == _sql_list("unit")


def test_source_types_agree():
    assert {s.value for s in SourceType} == _sql_list("source_type")
