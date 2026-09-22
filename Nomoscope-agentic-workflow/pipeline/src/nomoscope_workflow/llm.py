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
        # OPENAI_API_VERSION from the environment. The name after the slash IS
        # the deployment ("azure_openai/gpt-5.6-sol" -> deployment gpt-5.6-sol);
        # AZURE_OPENAI_DEPLOYMENT only fills in a bare "azure_openai". It must
        # never override an explicit name: when it did, every azure_openai/*
        # model — the model under test *and* the pinned judge — silently ran on
        # the one deployment in .env, and a Sol-vs-Luna eval compared Luna with
        # itself.
        deployment = name or os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
        if not deployment:
            raise ValueError(
                "azure_openai/ needs a deployment name after the slash "
                "(or AZURE_OPENAI_DEPLOYMENT as a default)"
            )
        return OpenAIChatModel(deployment, provider=AzureProvider())
    if provider == "openrouter":
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.openrouter import OpenRouterProvider

        return OpenAIChatModel(name, provider=OpenRouterProvider())
    if provider == "together":
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.together import TogetherProvider

        return OpenAIChatModel(name, provider=TogetherProvider())
    if provider == "jrc":
        from pydantic_ai.models.openai import OpenAIChatModel
        from pydantic_ai.providers.openai import OpenAIProvider

        # JRC's own OpenAI-compatible gateway (ADR 0004). Its own prefix rather
        # than "openai/" + env overrides for the same reason azure_openai/ is:
        # the string must say where the call goes. The base URL and key are
        # only ever set on the worker.
        base_url = os.environ.get("JRC_LLM_BASE_URL", "")
        if not base_url:
            raise ValueError("jrc/ needs JRC_LLM_BASE_URL (and JRC_LLM_API_KEY) in the environment")
        if not name:
            raise ValueError("jrc/ needs the served model name after the slash")
        return OpenAIChatModel(
            name,
            provider=OpenAIProvider(
                base_url=base_url, api_key=os.environ.get("JRC_LLM_API_KEY") or "unset"
            ),
        )
    raise ValueError(
        f"Unknown provider prefix in {model!r}; expected one of "
        "anthropic/, openai/, azure_openai/, openrouter/, together/, jrc/, mock/"
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
    model: str,
    record: ParameterRecord,
    as_of: date,
    draft: ProposalDraft,
    hits: list[RetrievalHit],
    mechanical_notes: list[str] | None = None,
) -> CritiqueFindings:
    """LLM critique pass (complements the mechanical checks in pipeline.py)."""
    return run_agent(
        model,
        prompts.CRITIQUE_SYSTEM,
        prompts.build_critique_user(record, as_of, draft, hits, mechanical_notes),
        output_type=CritiqueFindings,
    )
