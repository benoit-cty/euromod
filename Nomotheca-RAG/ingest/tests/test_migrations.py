"""schema.sql records every migration as applied (a fresh DB is at the latest state)."""

from __future__ import annotations

import re
from pathlib import Path

DB = Path(__file__).resolve().parents[2] / "db"


def test_schema_sql_records_every_migration():
    files = sorted(p.stem for p in (DB / "migrations").glob("*.sql"))
    recorded = re.findall(r"\('(\d{4}_[a-z0-9_]+)'\)", (DB / "schema.sql").read_text(encoding="utf-8"))
    assert recorded == files
