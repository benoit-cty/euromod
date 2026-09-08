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
