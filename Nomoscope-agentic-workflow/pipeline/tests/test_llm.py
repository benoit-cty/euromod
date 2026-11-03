"""get_model: the provider-prefixed string alone decides which model runs."""

from __future__ import annotations

import pytest

from nomoscope_workflow.llm import get_model


@pytest.fixture
def azure_env(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://example.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "test")
    monkeypatch.setenv("OPENAI_API_VERSION", "2024-10-21")


def test_azure_name_is_the_deployment_even_when_env_default_is_set(azure_env, monkeypatch):
    # Regression: AZURE_OPENAI_DEPLOYMENT used to override the explicit name, so
    # azure_openai/gpt-5.6-sol and azure_openai/gpt-5.6-luna both ran on the
    # deployment in .env and a two-model eval compared one model with itself.
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.6-luna")
    assert get_model("azure_openai/gpt-5.6-sol").model_name == "gpt-5.6-sol"
    assert get_model("azure_openai/gpt-5.6-luna").model_name == "gpt-5.6-luna"


def test_azure_env_default_fills_a_bare_provider(azure_env, monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.6-luna")
    assert get_model("azure_openai").model_name == "gpt-5.6-luna"
    assert get_model("azure_openai/").model_name == "gpt-5.6-luna"


def test_azure_without_any_deployment_is_an_error(azure_env, monkeypatch):
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    with pytest.raises(ValueError, match="deployment"):
        get_model("azure_openai/")


def test_jrc_prefix_is_an_openai_compatible_gateway(monkeypatch):
    """jrc/<served name>: the name after the slash is the served model, the gateway comes from env."""
    monkeypatch.setenv("JRC_LLM_BASE_URL", "https://llm.jrc.example/v1")
    monkeypatch.setenv("JRC_LLM_API_KEY", "test")
    model = get_model("jrc/x")
    assert model.model_name == "x"
    assert model.base_url.rstrip("/") == "https://llm.jrc.example/v1"


def test_jrc_without_a_gateway_is_an_error(monkeypatch):
    monkeypatch.delenv("JRC_LLM_BASE_URL", raising=False)
    with pytest.raises(ValueError, match="JRC_LLM_BASE_URL"):
        get_model("jrc/x")


def test_unknown_prefix_lists_jrc():
    with pytest.raises(ValueError, match="jrc/"):
        get_model("nope/x")


def test_azure_gpt_deployments_use_the_responses_api_without_temperature(azure_env):
    # gpt-6-luna refuses function tools on /chat/completions while reasoning is
    # on, and refuses `temperature` on /responses (3 Nov 2026).
    from nomoscope_workflow.llm import model_settings

    assert type(get_model("azure_openai/gpt-6-luna")).__name__ == "OpenAIResponsesModel"
    assert "temperature" not in model_settings("azure_openai/gpt-6-luna", 0.2)


def test_other_azure_deployments_stay_on_chat_completions(azure_env):
    from nomoscope_workflow.llm import model_settings

    assert type(get_model("azure_openai/mistral-large-3")).__name__ == "OpenAIChatModel"
    assert model_settings("azure_openai/mistral-large-3", 0.2) == {"temperature": 0.2}
    assert model_settings("anthropic/claude-sonnet-5", 0.0)["max_tokens"] > 0
