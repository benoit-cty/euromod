"""Pydantic models: golden cases (Activity 1 schema + expected block) and per-case results.

Value/routing enums and the Bracket type are imported from nomoscope_workflow so the
golden set speaks exactly the same language as the pipeline under test.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from nomoscope_workflow.schema import Bracket, LegalStatus, Routing


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


#: How much work it takes to get from the legal text to the stored value.
#: A property of the parameter, assigned from the ground truth — never derived
#: from a run's outcome, which would make the ladder unfalsifiable.
#:   verbatim  the value appears literally in one provision
#:   combine   it takes two or more provisions read together
#:   derive    it takes arithmetic: a formula, a $-constant, a weighted average
#:             for a mid-year change, a period conversion
#:   table     a full bracket schedule — every bracket must be right
Difficulty = Literal["verbatim", "combine", "derive", "table"]

#: Known failure modes, orthogonal to the ladder: a `verbatim` case can still be
#: an income-year case. Kept as flags rather than ladder rungs because they
#: compose, and because each one names a specific mechanism we can go and fix.
#:   income_year      FR back-dating (system year Y states income year Y-1)
#:   mid_year_change  EUROMOD stores the weighted average of two in-year values
#:   budget_act_window  the value is only final once the budget act passes;
#:                    earlier evidence routes `provisional`
#:   cross_instrument the value is fixed by an act a second act merely points to
#:                    (a code article referring to an arrêté)
#:   unit_conversion  the law states one period, EUROMOD stores another
Hazard = Literal[
    "income_year", "mid_year_change", "budget_act_window", "cross_instrument", "unit_conversion",
    # A sibling region's act is in the corpus and states a near-identical
    # amount for ITS scheme: a proposal citing it passes the verbatim-extract
    # check and is still wrong (ADR 0003). Regional parameters only.
    "sibling_region",
]

#: Whether a case can be scored as model quality at all. Readiness is a property
#: of the GOLDEN SET, not of the model, and the two states below are the reasons
#: a case cannot answer "how good is the model":
#:   no_corpus     the source act is not ingested — no model could answer it
#:   undocumented  no ground-truth citation was ever recorded, so retrieval is
#:                 unscorable and nobody established where the answer lives
#: Only `ready` cases belong in a quality headline.
Readiness = Literal["ready", "no_corpus", "undocumented"]


class GoldenCase(BaseModel):
    """One validation case: run the workflow on parameter_file at as_of, compare to expected."""

    model_config = ConfigDict(extra="forbid")

    id: str
    country: str
    language: str = Field(description="Language of the source legislation, e.g. 'fr'")
    parameter_file: str = Field(description="Activity 1 parameter JSON, path relative to the repo root")
    as_of: date
    difficulty: Difficulty | None = None
    hazards: list[Hazard] = Field(
        default_factory=list,
        description="Known failure modes this case exercises; orthogonal to `difficulty`",
    )
    labels_drafted: bool = Field(
        default=True,
        description="False when a human set difficulty/hazards in the selection file. "
        "`label-cases --apply` refuses to touch those: the drafter sees less than a "
        "reviewer does (it cannot tell a bracket group from a scalar once the case is "
        "materialized), so it must never overwrite a judgement it could not have made.",
    )
    source_class: Literal["codified_law", "gazette", "national_team"] | None = None
    expected: Expected
    corpus_available: bool | None = Field(
        default=None,
        description="True when at least one of the case's ground-truth references resolves to "
        "a legal unit already in the legislation corpus. False marks a case whose source is not "
        "ingested yet: it measures corpus coverage, not model quality, and KPI reports slice it "
        "out. None = never established (no reference to check).",
    )
    verified: bool = Field(default=False, description="True once a human confirmed the ground truth")
    drafted_by: str | None = Field(
        default=None, description="'human', the drafting model name, or 'openfisca@<commit>'"
    )
    # Who reviewed the draft, and what they concluded. reviewed_by distinguishes
    # "rejected by a human" (reviewed_by set, verified false) from "not looked at
    # yet" — both of which keep the case out of a frozen evaluation run.
    reviewed_by: str | None = None
    review_note: str | None = None
    notes: str | None = None

    @field_validator("difficulty", mode="before")
    @classmethod
    def _legacy_plain(cls, value: object) -> object:
        """`plain` was the pre-ladder label, assigned mechanically as "not a
        bracket table". It means the same thing the ladder calls `verbatim`, and
        frozen `cases.json` files from earlier runs still carry it — `rescore`
        must keep loading them."""
        return "verbatim" if value == "plain" else value

    @property
    def readiness(self) -> Readiness:
        """Why this case can or cannot be read as a measure of model quality.

        Checked corpus-first: `no_corpus` is the stronger, positively
        established fact (we looked the act up and it is not there), while
        `undocumented` only says nobody ever recorded where the answer lives.
        """
        if self.corpus_available is False:
            return "no_corpus"
        if not self.expected.citations:
            return "undocumented"
        return "ready"


class EmbeddingCase(BaseModel):
    """One retrieval case: a search query plus the citation(s) of the legal unit(s)
    a correct retriever must surface — evaluates the embedding/search layer alone,
    with no LLM anywhere."""

    model_config = ConfigDict(extra="forbid")

    id: str
    country: str
    language: str = Field(description="Language of the query (the aggregation key, as in GoldenCase)")
    corpus_lang: str | None = Field(
        default=None,
        description="Language of the searched texts; defaults to `language`. "
        "Set both for cross-lingual cases (e.g. an 'en' query over the 'fr' corpus).",
    )
    as_of: date
    query: str
    region: str | None = Field(
        default=None,
        description="NUTS-2 key of a regional parameter (e.g. 'ES24'). Scopes the search to the "
        "country plus that region's child jurisdiction, exactly as the pipeline scopes a run "
        "(ADR 0003); None searches the country's own acts only.",
    )
    expected_citations: list[str] = Field(
        min_length=1,
        description="Relevant legal units, any-of; each must be the exact legal_units.citation "
        'string (e.g. "CGI, art. 197") — compared with punctuation/case-insensitive equality, '
        "not containment, so 'art. 2' never claims 'art. 20'",
    )
    verified: bool = Field(default=False, description="True once a human confirmed the ground truth")
    drafted_by: str | None = Field(default=None, description="'human' or the drafting model name")
    notes: str | None = None


class EmbeddingCaseResult(BaseModel):
    """Rank outcome of one embedding case under each search method.

    ranks maps method ('fts' | 'vector' | 'hybrid') to the 1-based rank of the
    first relevant hit, or None for a miss within top-k. A method absent from
    the dict was not scored (e.g. query encoder unavailable — see error).
    """

    model_config = ConfigDict(extra="forbid")

    case_id: str
    country: str
    language: str
    corpus_lang: str
    k: int
    candidate_chunks: int | None = None
    embedded_chunks: int | None = None
    ranks: dict[str, int | None] = Field(default_factory=dict)
    error: str | None = None


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
    hazards: list[str] = Field(default_factory=list)
    source_class: str | None = None

    routing_expected: str
    routing_actual: str | None = None
    routing_correct: bool | None = None
    value_correct: bool | None = None
    date_correct: bool | None = None
    citation_correct: bool | None = None
    # The three evidence legs, deliberately separate because they are not
    # equally trustworthy:
    #   extract_verbatim  purely mechanical — the cited chunk contains the
    #                     supporting_extract character-for-character. This is
    #                     the anti-hallucination guarantee, and the only one no
    #                     LLM has a say in.
    #   supportedness     extract_verbatim AND the critique model's judgement
    #                     that the extract actually supports the value. LLM-
    #                     assisted, so never compare it across models unless
    #                     the run pinned a fixed critique model.
    #   critique_pass     the critique's overall verdict (dates, units, sanity).
    extract_verbatim: bool | None = None
    supportedness: bool | None = None
    critique_pass: bool | None = None
    hallucination: bool = False
    retrieval_hit: bool | None = None
    # A refusal on a case that has a ground-truth value: the pipeline said
    # not_found rather than proposing something it could not cite. Scored
    # separately because it is the *correct* behaviour when the source is
    # missing from the corpus, yet it costs the value/date/citation legs.
    abstained: bool = False
    # A value was proposed and the pipeline's own critique rejected it (verdict
    # "fail": not verbatim, wrong vintage, unit implausible…). The diff step
    # still routes such an item on its value — `unchanged` when it merely
    # echoes what EUROMOD holds — so scoring the routing and value legs from
    # the routing alone credited proposals the pipeline itself had thrown out:
    # one model gained eight "correct" verdicts that way on a 66-case run, four
    # of them with the barème's stale value and a citation the critique had
    # refused. A rejected proposal is therefore never routing- or value-correct;
    # `routing_actual` still records what the pipeline emitted.
    rejected: bool = False
    # Every citation on the proposal came from administrative guidance rather
    # than legislation (ADR 0001). Not a KPI and not scored: it is the data on
    # which "guidance ranks equal to legislation in retrieval" is to be
    # revisited, grouped by the same per-language, per-model views.
    guidance_only: bool = False
    # Copied from the case so a report can separate model quality from corpus
    # coverage without re-reading the golden set.
    corpus_available: bool | None = None
    # GoldenCase.readiness at scoring time: 'ready', or the reason this case
    # measures the golden set rather than the model. Denormalised for the same
    # reason as corpus_available — reports and SQL should not need the dataset.
    readiness: str | None = None

    confidence: float | None = None
    latency_ms: int | None = None
    error: str | None = None
    item_id: str | None = None
    proposed_value: object | None = None
    expected_value: object | None = None

    # Environmental impact of this case's LLM calls, from EcoLogits over the
    # Phoenix trace (nomoscope_workflow.impact). None for mock runs.
    phoenix_trace_id: str | None = None
    llm_calls: int | None = None
    tokens_prompt: int | None = None
    tokens_completion: int | None = None
    energy_kwh: float | None = None
    gwp_kgco2eq: float | None = None
    # False when EcoLogits has no registry entry for the model: the energy/GWP
    # columns are then left None rather than reported as a measured 0.0.
    impact_estimated: bool | None = None


class RunManifest(BaseModel):
    """Reproducibility manifest, written next to the results and into eval.runs."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    created_at: datetime
    as_of: date
    model: str
    model_provider: str
    model_name: str
    #: The model that ran the critique step. Equal to `model` (the model under
    #: test grading itself) unless EVAL_CRITIQUE_MODEL pinned a fixed judge —
    #: which is what cross-model comparison needs, since supportedness and
    #: critique_pass depend on it.
    critique_model: str | None = None
    #: What the provider layer resolved `model` / `critique_model` to (the
    #: PydanticAI model_name — for azure_openai/ the deployment). Recorded so a
    #: comparison can prove it ran two different models; None for mock/.
    resolved_model: str | None = None
    resolved_critique_model: str | None = None
    prompt_version: str
    agent_version: str
    eval_version: str
    dataset_version: str
    git_commit: str | None = None
    countries: list[str] = Field(default_factory=list)
    notes: str | None = None
