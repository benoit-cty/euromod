"""Tests for EUROMOD Country Report Markdown parsing."""

from __future__ import annotations

from datetime import date
from uuid import uuid4

from nomotheca_ingest.core.country_reports import parse_country_report, source_code_for
from nomotheca_ingest.core.ir import SourceTrustClass

SAMPLE = """\
# EUROMOD Country Report — France Y16

Intro paragraph before any section.

## 1. Introduction & scope (CR pages 8-27)

### 1.1 Basic information

France operates a progressive income tax.

### 1.2 Social benefits

## 2. Family benefits

### 2.5.1. Universal child benefit — bch00_s — (Allocation Familiale, AF)

#### Definitions

AF is paid from the second child.

#### Benefit amount

139.84 EUR per month for two children.

### 2.5.1. Universal child benefit — bch00_s — (Allocation Familiale, AF)

Duplicate heading to exercise path dedup.
"""


def _parse():
    return parse_country_report(
        SAMPLE,
        jurisdiction="fr",
        vintage="Y16",
        source_code=source_code_for("fr"),
        valid_from=date(2022, 1, 1),
        snapshot_id=uuid4(),
    )


def test_instrument_identity_and_type() -> None:
    """The CR loads as a country_report instrument with a stable national id."""
    ir = _parse()
    assert ir.instrument_type == "country_report"
    assert ir.national_id == "CR-FR-Y16"
    assert ir.source_code == "FR-EUROMOD-CR"
    assert ir.title["en"].startswith("EUROMOD Country Report")


def test_country_reports_are_context_never_evidence() -> None:
    """The CR corpus describes the model: evidence retrieval excludes it by class."""
    assert _parse().source_trust_class == SourceTrustClass.CONTEXT


def test_hierarchy_follows_markdown_levels() -> None:
    """Units nest by #-depth and containers are flagged."""
    ir = _parse()
    by_path = {u.path: u for u in ir.units}
    assert by_path["sec_1.sec_1_1"].parent_path == "sec_1"
    assert by_path["sec_1"].is_container
    definitions = by_path["sec_2.sec_2_5_1.definitions"]
    assert definitions.parent_path == "sec_2.sec_2_5_1"
    assert definitions.metadata["heading_level"] == 4


def test_content_and_versions() -> None:
    """Only units with own text carry a version; text is verbatim-loadable."""
    ir = _parse()
    by_path = {u.path: u for u in ir.units}
    amount = by_path["sec_2.sec_2_5_1.benefit_amount"]
    assert len(amount.versions) == 1
    assert "139.84 EUR per month" in amount.versions[0].texts[0].content
    assert amount.versions[0].texts[0].lang == "en"
    # '## 2. Family benefits' has no own text, only children
    assert by_path["sec_2"].versions == []
    # preamble captured
    assert "Intro paragraph" in by_path["preamble"].versions[0].texts[0].content


def test_duplicate_headings_get_unique_paths() -> None:
    """Two identical sibling headings must not collide on ltree paths."""
    ir = _parse()
    paths = [u.path for u in ir.units]
    assert len(paths) == len(set(paths))
    assert "sec_2.sec_2_5_1_2" in paths


def test_versions_dedupe_key_is_stable() -> None:
    """Re-ingesting the same vintage must reuse versions, not stack overlaps."""
    ir = _parse()
    ids = {
        v.source_version_id
        for u in ir.units
        for v in u.versions
    }
    assert ids == {"CR-FR-Y16@2022-01-01"}
