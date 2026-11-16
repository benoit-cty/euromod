"""Readiness follows schema.income_year_for, not a private ±1 (code audit D3)."""

from __future__ import annotations

from nomoscope_workflow import readiness, schema


def test_system_year_2025_needs_only_the_finance_act_for_2025():
    # LF 2025 carries both the in-force values and the barème the law labels
    # "revenus 2024" — the one EUROMOD system year 2025 holds.
    assert readiness.vintages_for(2025) == [(2025, ("in_force", "income_year"))]


def test_vintages_move_with_the_offset(monkeypatch):
    monkeypatch.setattr(schema, "INCOME_YEAR_OFFSET", 0)
    assert readiness.vintages_for(2025) == [(2025, ("in_force",)), (2026, ("income_year",))]


def test_missing_act_announces_provisional_income_year_params():
    status = readiness.ActStatus(vintage=2025, roles=("in_force", "income_year"))
    line = readiness.describe(status, income_year_params=12)
    assert "in-force params and income-year params" in line
    assert "12 income-year parameter(s) will be provisional" in line
