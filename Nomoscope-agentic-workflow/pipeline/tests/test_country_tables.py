"""The country tables across Python and the two apps agree (code audit 2.1).

The pilot countries are spelled in the workflow (law language, scout
sources), the ingest registry, and the apps' labels, hand-off prompt and chat.
No single table can own them all (the apps are JS, the ingest package does
not depend on the workflow), so this test keeps them in step.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from nomoscope_workflow.corpus import LANG_BY_COUNTRY
from nomoscope_workflow.scout_sources import COUNTRY_SOURCES

APPS = Path(__file__).resolve().parents[2]
PILOT = set(LANG_BY_COUNTRY)


def _js(path: str) -> str:
    return (APPS / path).read_text(encoding="utf-8")


def _object_keys(source: str, name: str) -> set[str]:
    body = re.search(r"const " + name + r" = \{(.*?)\n\};?", source, re.S).group(1)
    return set(re.findall(r"^\s*([A-Z]{2}):", body, re.M))


def test_the_apps_name_the_same_countries():
    assert _object_keys(_js("shared/lib/labels.js"), "COUNTRIES") == PILOT
    handoff = _js("ui/src/lib/handoff.js")
    assert _object_keys(handoff, "COUNTRY_SOURCES") == PILOT
    chat = re.search(r"export const COUNTRIES = \[([^\]]*)\]", _js("rag-ui/src/lib/chat.js")).group(1)
    assert set(re.findall(r"'([A-Z]{2})'", chat)) == PILOT


def test_the_hand_off_prompt_uses_each_country_s_law_language():
    law_lang = re.search(r"const LAW_LANG = \{([^}]*)\}", _js("ui/src/lib/handoff.js")).group(1)
    assert dict(re.findall(r"([A-Z]{2}): '([a-z]{2})'", law_lang)) == LANG_BY_COUNTRY


def test_scout_and_adapters_cover_only_pilot_countries():
    assert set(COUNTRY_SOURCES) <= PILOT
    registry = pytest.importorskip("nomotheca_ingest.countries.registry")
    assert set(registry.jurisdictions()) <= PILOT
