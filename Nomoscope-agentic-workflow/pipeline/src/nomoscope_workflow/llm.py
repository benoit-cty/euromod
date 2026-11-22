"""The workflow's two LLM steps (proposal, critique) over nomos_llm.

Provider access — "<provider>/<model>" strings, request settings, context
windows, `run_agent` — is the shared `nomos_llm` package (re-exported here,
so `llm.get_model`, `llm.model_settings`, … keep working); this module adds
the structured-output steps and the prompt trimming they need.
"""

from __future__ import annotations

import logging
from datetime import date

from nomos_llm.providers import *  # noqa: F403  (re-exported)
from nomos_llm.providers import (
    _AZURE_RESPONSES_DEPLOYMENT,  # noqa: F401
    prompt_budget_chars,
    run_agent,
)
from pydantic_ai.exceptions import UserError
from tenacity import retry, retry_if_not_exception_type, stop_after_attempt, wait_random_exponential

from . import prompts
from .schema import CritiqueFindings, ParameterRecord, ProposalDraft, RetrievalHit

log = logging.getLogger(__name__)


def _fitted(model: str, step: str, before: list[RetrievalHit], after: list[RetrievalHit]):
    if len(after) < len(before):
        log.warning(
            "%s: %d of %d retrieved chunks dropped to fit %s's context window",
            step,
            len(before) - len(after),
            len(before),
            model,
        )
    return after


#: Retry transient provider failures only. A configuration error (an unknown
#: provider, a missing key or base URL: `get_model` raises ValueError, and
#: pydantic-ai a UserError) will not fix itself — until 16 Nov 2026 it was
#: retried three times with back-off before failing (code audit 4).
_TRANSIENT = dict(
    wait=wait_random_exponential(min=1, max=30),
    stop=stop_after_attempt(3),
    retry=retry_if_not_exception_type((ValueError, KeyError, TypeError, UserError)),
    reraise=True,
)


@retry(**_TRANSIENT)
def propose_with_llm(
    model: str,
    record: ParameterRecord,
    as_of: date,
    hits: list[RetrievalHit],
    feedback: str | None = None,
) -> ProposalDraft:
    """Proposal step: structured output straight into the ProposalDraft schema."""
    budget = prompt_budget_chars(model)
    if budget is not None:
        fixed = len(prompts.PROPOSAL_SYSTEM) + len(prompts.build_proposal_user(record, as_of, [], feedback))
        hits = _fitted(model, "propose", hits, prompts.fit_hits(hits, budget - fixed))
    return run_agent(
        model,
        prompts.PROPOSAL_SYSTEM,
        prompts.build_proposal_user(record, as_of, hits, feedback),
        output_type=ProposalDraft,
    )


@retry(**_TRANSIENT)
def critique_with_llm(
    model: str,
    record: ParameterRecord,
    as_of: date,
    draft: ProposalDraft,
    hits: list[RetrievalHit],
    mechanical_notes: list[str] | None = None,
) -> CritiqueFindings:
    """LLM critique pass (complements the mechanical checks in pipeline.py)."""
    budget = prompt_budget_chars(model)
    if budget is not None:
        fixed = len(prompts.CRITIQUE_SYSTEM) + len(
            prompts.build_critique_user(record, as_of, draft, [], mechanical_notes)
        )
        cited = {draft.citation_chunk_id, *(op.citation_chunk_id for op in draft.operands or [])}
        hits = _fitted(model, "critique", hits, prompts.fit_hits(hits, budget - fixed, keep=cited - {None}))
    return run_agent(
        model,
        prompts.CRITIQUE_SYSTEM,
        prompts.build_critique_user(record, as_of, draft, hits, mechanical_notes),
        output_type=CritiqueFindings,
    )
