"""Provider-agnostic LLM access, keyed on "<provider>/<model>" strings.

Pattern lifted from update_openfisca_ai's get_llm_instance: the provider prefix
selects the LangChain chat class, so swapping models is a config-string change
(hard requirement — Activity 5 compares different LLMs). "mock/..." is handled
upstream in mock.py and never reaches this factory.
"""

from __future__ import annotations

import os
from datetime import date

from tenacity import retry, stop_after_attempt, wait_random_exponential

from . import prompts
from .schema import CritiqueFindings, ParameterRecord, ProposalDraft, RetrievalHit


def get_chat_model(model: str, temperature: float = 0.2):
    """Instantiate a LangChain chat model from a provider-prefixed name."""
    provider, _, name = model.partition("/")
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model_name=name, max_tokens=8000, temperature=temperature)
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=name, temperature=temperature)
    if provider == "azure_openai":
        from langchain_openai import AzureChatOpenAI

        return AzureChatOpenAI(
            api_version=os.environ.get("OPENAI_API_VERSION"),
            azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", name),
        )
    if provider == "openrouter":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=name,
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=temperature,
            streaming=False,
        )
    if provider == "together":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=name,
            api_key=os.environ.get("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1",
            temperature=temperature,
            streaming=False,
        )
    raise ValueError(
        f"Unknown provider prefix in {model!r}; expected one of "
        "anthropic/, openai/, azure_openai/, openrouter/, together/, mock/"
    )


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3), reraise=True)
def propose_with_llm(
    model: str, record: ParameterRecord, as_of: date, hits: list[RetrievalHit]
) -> ProposalDraft:
    """Proposal step: structured output straight into the ProposalDraft schema."""
    llm = get_chat_model(model).with_structured_output(ProposalDraft)
    return llm.invoke(
        [
            ("system", prompts.PROPOSAL_SYSTEM),
            ("human", prompts.build_proposal_user(record, as_of, hits)),
        ]
    )


@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3), reraise=True)
def critique_with_llm(
    model: str, record: ParameterRecord, as_of: date, draft: ProposalDraft, hits: list[RetrievalHit]
) -> CritiqueFindings:
    """LLM critique pass (complements the mechanical checks in pipeline.py)."""
    llm = get_chat_model(model).with_structured_output(CritiqueFindings)
    return llm.invoke(
        [
            ("system", prompts.CRITIQUE_SYSTEM),
            ("human", prompts.build_critique_user(record, as_of, draft, hits)),
        ]
    )
