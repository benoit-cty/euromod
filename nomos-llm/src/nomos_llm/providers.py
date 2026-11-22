"""Provider-agnostic LLM access, keyed on "<provider>/<model>" strings.

The provider prefix selects the PydanticAI model class and provider, so
swapping models is a config-string change (hard requirement — Activity 5
compares different LLMs). "mock/..." is handled by the callers and never
reaches this factory.

This is the shared base of the workflow (proposal, critique, chat) and the
ingest package's translator. It used to live in nomoscope_workflow.llm, so
the ingest package depended on the whole workflow for it (code audit 2.2).
"""

from __future__ import annotations

import logging
import os
import re

from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

log = logging.getLogger(__name__)

ANTHROPIC_MAX_TOKENS = 8000

#: Azure deployments of OpenAI's own GPT / o-series models. They go through the
#: Responses API: on /chat/completions gpt-6-luna refuses function tools while
#: reasoning is on — and PydanticAI's structured output IS a function tool, so
#: every propose/critique/chat call failed (job 90, 3 Nov 2026). Other Azure
#: deployments (Mistral, DeepSeek, …) are not served by /responses and stay on
#: chat completions.
_AZURE_RESPONSES_DEPLOYMENT = re.compile(r"^(gpt-|o\d)", re.IGNORECASE)


def uses_responses_api(model: str) -> bool:
    """Whether a provider-prefixed model is called through the Responses API."""
    provider, _, name = model.partition("/")
    if provider != "azure_openai":
        return False
    deployment = name or os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    return bool(_AZURE_RESPONSES_DEPLOYMENT.match(deployment))


#: Output cap sent to OpenRouter. Without one, a provider budgets the
#: prompt against window − ITS OWN default output reservation: in the
#: 14 Nov 2026 LT benchmark, OpenRouter fell back from a rate-limited Groq to
#: GMICloud (max output 176 947 tokens), which refused ~88k-token MiniMax M2.7
#: prompts as «context window exceeds limit» while Groq had taken 128k ones —
#: 14 of 234 cases crashed. The cap also stops a runaway answer: one MiniMax
#: call ran to 131 072 output tokens; 99 % stay under 7 740.
ROUTED_MAX_TOKENS = 16_384

#: Context windows (tokens) of the models a full retrieval can outgrow, keyed
#: by the name after the provider prefix; for a router, the smallest window
#: among the providers it may route to. A model not listed is never trimmed
#: (the Azure GPT deployments have room for every prompt the pipeline builds).
CONTEXT_WINDOWS: dict[str, int] = {
    "minimax/minimax-m2.7": 196_608,
    "mistralai/mistral-small-3.2-24b-instruct": 128_000,
    "google/gemma-4-31b-it": 262_144,
    "qwen/qwen3.8-27b": 262_144,  # native; OpenRouter's 1M is YaRN-extended
}

#: Reasoning models whose thinking counts against the output cap: on the
#: 17 Nov 2026 FR sample DeepSeek V4 Flash crashed 5 cases of 40 and
#: GLM-5.3-Flash 11 with "Model token limit (16384) exceeded before any
#: response". Both have 1M-token windows, so a larger reservation costs the
#: prompt nothing.
ROUTED_MAX_OUTPUT: dict[str, int] = {
    "deepseek/deepseek-v4-flash-0731": 65_536,
    "z-ai/glm-5.3-flash": 65_536,
}

#: Characters per prompt token, on the safe side: MiniMax M2.7 measured
#: ~2.4 on Lithuanian law with the JSON parameter block (Phoenix, 14 Nov 2026).
CHARS_PER_TOKEN = 2.0
#: Headroom for the tool schema and message framing the request adds.
PROMPT_MARGIN_TOKENS = 4_096


def max_output_tokens(model: str) -> int | None:
    """The output cap sent with every request to `model`, if any."""
    provider = model.partition("/")[0]
    if provider == "anthropic":
        return ANTHROPIC_MAX_TOKENS
    if provider == "openrouter":
        return ROUTED_MAX_OUTPUT.get(model.partition("/")[2], ROUTED_MAX_TOKENS)
    return None


def prompt_budget_chars(model: str) -> int | None:
    """How many characters of system + user prompt fit `model`'s window, or
    None when the model has no known window to respect."""
    window = CONTEXT_WINDOWS.get(model.partition("/")[2])
    if window is None:
        return None
    room = window - (max_output_tokens(model) or 0) - PROMPT_MARGIN_TOKENS
    return int(room * CHARS_PER_TOKEN)


def model_settings(model: str, temperature: float | None = None, timeout: float | None = None) -> ModelSettings:
    """The request settings every LLM call uses, in one place (the timeout
    included — `run_agent` used to add it afterwards).

    Reasoning models behind the Responses API reject `temperature` outright
    ("Unsupported parameter"), so it is only sent where it is accepted.
    """
    settings: ModelSettings = {}
    if timeout is not None:
        settings["timeout"] = timeout
    if temperature is not None and not uses_responses_api(model):
        settings["temperature"] = temperature
    if (cap := max_output_tokens(model)) is not None:
        settings["max_tokens"] = cap
    return settings


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
                "azure_openai/ needs a deployment name after the slash (or AZURE_OPENAI_DEPLOYMENT as a default)"
            )
        if uses_responses_api(model):
            from pydantic_ai.models.openai import OpenAIResponsesModel

            return OpenAIResponsesModel(deployment, provider=AzureProvider())
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
            provider=OpenAIProvider(base_url=base_url, api_key=os.environ.get("JRC_LLM_API_KEY") or "unset"),
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
    settings = model_settings(model, temperature, timeout)
    agent = Agent(
        get_model(model),
        output_type=output_type,
        instructions=system,
        model_settings=settings,
    )
    return agent.run_sync(user).output
