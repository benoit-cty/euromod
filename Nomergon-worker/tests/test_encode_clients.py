"""The four encode-job clients agree with the worker's JobSpec (code audit 2.1).

The pipeline, the MCP server and the review UI submit `encode` jobs without
importing the worker (the dependency runs worker -> packages, and the UI is
Rust), so each spells the priority itself. This keeps them in step.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from nomergon import jobs

ROOT = Path(__file__).resolve().parents[2]
ENCODE = jobs.default_priority("encode")


def test_the_pipeline_client_uses_the_encode_priority():
    from nomoscope_workflow import encode_client

    assert encode_client.ENCODE_PRIORITY == ENCODE


def test_the_mcp_client_uses_the_encode_priority():
    encoder = pytest.importorskip("nomotheca_mcp.encoder")
    assert encoder.ENCODE_JOB_PRIORITY == ENCODE


def test_the_review_ui_uses_the_encode_priority():
    source = (ROOT / "Nomoscope-agentic-workflow/ui/src-tauri/src/jobs.rs").read_text(encoding="utf-8")
    match = re.search(r"pub const ENCODE_PRIORITY: i16 = (\d+);", source)
    assert match and int(match.group(1)) == ENCODE
