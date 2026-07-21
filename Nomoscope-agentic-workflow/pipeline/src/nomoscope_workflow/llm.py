"""Provider-agnostic LLM access, keyed on "<provider>/<model>" strings.

The provider prefix selects the PydanticAI model class and provider, so
swapping models is a config-string change (hard requirement — Activity 5
compares different LLMs). "mock/..." is handled upstream in mock.py and never
reaches this factory.
"""

from __future__ import annotations

import os
from datetime import date

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from tenacity import retry, stop_after_attempt, wait_random_exponential

from . import prompts
from .schema import CritiqueFindings, ParameterRecord, ProposalDraft, RetrievalHit

ANTHROPIC_MAX_TOKENS = 8000


def get_model(model: str):
    """Instantiate a PydanticAI model from a provider-prefixed name."""
    provider, _, name = model.partition("/")
    if provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel

        return AnthropicModel(name)
    if provider == "openai":
        from pydantic_ai.models.openai import OpenAIChatModel

        return OpenAIChatModel(name)
    if provider == "azure_openai":
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.azure import AzureProvider

        # AzureProvider reads AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY and
        # OPENAI_API_VERSION from the environment.
        return OpenAIChatModel(
            os.environ.get("AZURE_OPENAI_DEPLOYMENT", name), provider=AzureProvider()
        )
    if provider == "openrouter":
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.openrouter import OpenRouterProvider

        return OpenAIChatModel(name, provider=OpenRouterProvider())
    if provider == "together":
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.together import TogetherProvider

        return OpenAIChatModel(name, provider=TogetherProvider())
    raise ValueError(
        f"Unknown provider prefix in {model!r}; expected one of "
        "anthropic/, openai/, azure_openai/, openrouter/, together/, mock/"
    )


def run_agent(
    model: str,
    system: str,
    user: str,
    output_type: type = str,
    temperature: float = 0.2,
    timeout: float | None = None,
):
    """One agent run: system + user prompt in, plain text or a schema instance out."""
    settings: ModelSettings = {"temperature": temperature}
    if model.partition("/")[0] == "anthropic":
        settings["max_tokens"] = ANTHROPIC_MAX_TOKENS
    if timeout is not None:
        settings["timeout"] = timeout
    agent = Agent(
        get_model(model),
        output_type=output_type,
        instructions=system,
        model_settings=settings,
    )
    return agent.run_sync(user).output


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3), reraise=True)
def propose_with_llm(
    model: str,
    record: ParameterRecord,
    as_of: date,
    hits: list[RetrievalHit],
    feedback: str | None = None,
) -> ProposalDraft:
    """Proposal step: structured output straight into the ProposalDraft schema."""
    return run_agent(
        model,
        prompts.PROPOSAL_SYSTEM,
        prompts.build_proposal_user(record, as_of, hits, feedback),
        output_type=ProposalDraft,
    )


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3), reraise=True)
def critique_with_llm(
    model: str, record: ParameterRecord, as_of: date, draft: ProposalDraft, hits: list[RetrievalHit]
) -> CritiqueFindings:
    """LLM critique pass (complements the mechanical checks in pipeline.py)."""
    return run_agent(
        model,
        prompts.CRITIQUE_SYSTEM,
        prompts.build_critique_user(record, as_of, draft, hits),
        output_type=CritiqueFindings,
    )
