"""The ingest vocabularies live in one place each."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

from nomotheca_ingest.core.contributed import (
    DEFAULT_KINDS,
    RefusalError,
    kinds_by_jurisdiction,
    kinds_for,
    stated_fields,
)
from nomotheca_ingest.core.ir import SOURCE_TYPES, NormLevel
from nomotheca_ingest.countries.registry import get_adapter, jurisdictions

SRC = Path(__file__).resolve().parents[1] / "src" / "nomotheca_ingest"
_LITERAL = re.compile(r"""(?:source_type\s*=\s*|"source_type"\s*:\s*)"([a-z_]+)\"""")


def test_every_source_type_in_code_is_documented():
    used = {m.group(1) for path in SRC.rglob("*.py") for m in _LITERAL.finditer(path.read_text(encoding="utf-8"))}
    assert used, "the scan found no source_type literal at all"
    assert used <= set(SOURCE_TYPES), used - set(SOURCE_TYPES)


def test_contributed_kinds_are_declared_by_the_adapters():
    tables = kinds_by_jurisdiction()
    for code in jurisdictions():
        assert tables[code] == get_adapter(code).contributed_kinds
        # every country can still say "I don't know what this is"
        assert dict(tables[code])["other"] is NormLevel.OTHER
    assert tables["DEFAULT"] == DEFAULT_KINDS
    assert kinds_for("FR")["circulaire"] is NormLevel.ADMINISTRATIVE_GUIDANCE
    assert kinds_for("ES-AR") == dict(DEFAULT_KINDS)  # a regional child has no table of its own


def test_an_incomplete_declaration_is_a_refusal_not_any_value_error():
    with pytest.raises(RefusalError, match="title"):
        stated_fields(jurisdiction="FR", lang="fr", title=None, kind="circulaire", valid_from=None)
    with pytest.raises(RefusalError, match="Unknown kind"):
        stated_fields(jurisdiction="FR", lang="fr", title="T", kind="memo", valid_from=date(2025, 1, 1))
