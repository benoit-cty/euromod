"""Pydantic models: golden cases (Activity 1 schema + expected block) and per-case results.

Value/routing enums and the Bracket type are imported from euromod_workflow so the
golden set speaks exactly the same language as the pipeline under test.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from euromod_workflow.schema import Bracket, LegalStatus, Routing


class Expected(BaseModel):
    """Ground truth for one (parameter, as_of) case. None fields are not scored."""

    model_config = ConfigDict(extra="forbid")

    routing: Routing
    value: list[Bracket] | bool | float | str | None = None
    valid_from: date | None = None
    legal_status: LegalStatus | None = None
    citations: list[str] = Field(
        default_factory=list,
        description='Acceptable pinpoint citations, e.g. ["CGI, art. 197"]; any-of match',
    )


class GoldenCase(BaseModel):
    """One validation case: run the workflow on parameter_file at as_of, compare to expected."""

    model_config = ConfigDict(extra="forbid")

    id: str
    country: str
    language: str = Field(description="Language of the source legislation, e.g. 'fr'")
    parameter_file: str = Field(description="Activity 1 parameter JSON, path relative to the repo root")
    as_of: date
    difficulty: Literal["plain", "combine", "table"] | None = None
    source_class: Literal["codified_law", "gazette", "national_team"] | None = None
    expected: Expected
    verified: bool = Field(default=False, description="True once a human confirmed the ground truth")
    drafted_by: str | None = Field(default=None, description="'human' or the drafting model name")
    notes: str | None = None


class CaseResult(BaseModel):
    """Scored outcome of one golden case against one workflow run.

    Boolean KPIs are None when the case does not exercise that KPI
    (e.g. no expected value on a not_found routing case).
    """

    model_config = ConfigDict(extra="forbid")

    case_id: str
    country: str
    language: str
    model_target: str | None = None
    difficulty: str | None = None
    source_class: str | None = None

    routing_expected: str
    routing_actual: str | None = None
    routing_correct: bool | None = None
    value_correct: bool | None = None
    date_correct: bool | None = None
    citation_correct: bool | None = None
    supportedness: bool | None = None
    hallucination: bool = False
    retrieval_hit: bool | None = None

    confidence: float | None = None
    latency_ms: int | None = None
    error: str | None = None
    item_id: str | None = None
    proposed_value: object | None = None
    expected_value: object | None = None


class RunManifest(BaseModel):
    """Reproducibility manifest, written next to the results and into eval.runs."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    created_at: datetime
    as_of: date
    model: str
    model_provider: str
    model_name: str
    prompt_version: str
    agent_version: str
    eval_version: str
    dataset_version: str
    git_commit: str | None = None
    countries: list[str] = Field(default_factory=list)
    notes: str | None = None
