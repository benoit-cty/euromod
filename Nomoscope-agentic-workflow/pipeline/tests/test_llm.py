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


def test_openrouter_requests_carry_an_output_cap():
    # Without one, GMICloud (OpenRouter's fallback for MiniMax M2.7) budgeted
    # ~88k-token prompts against its own 176 947-token output reservation and
    # refused them: 14 of the 14 Nov 2026 LT benchmark cases crashed.
    from nomoscope_workflow.llm import ROUTED_MAX_TOKENS, model_settings

    assert model_settings("openrouter/minimax/minimax-m2.7", 0.2) == {
        "temperature": 0.2,
        "max_tokens": ROUTED_MAX_TOKENS,
    }


def test_prompt_budget_only_for_models_with_a_known_window():
    from nomoscope_workflow.llm import ROUTED_MAX_TOKENS, prompt_budget_chars

    budget = prompt_budget_chars("openrouter/minimax/minimax-m2.7")
    assert budget is not None and budget < (196_608 - ROUTED_MAX_TOKENS) * 2.4
    assert prompt_budget_chars("azure_openai/gpt-6-luna") is None


def _hit(chunk_id, method="hybrid", score=None, size=1000):
    from nomoscope_workflow.schema import RetrievalHit

    return RetrievalHit(chunk_id=chunk_id, method=method, score=score, content="x" * size)


def test_fit_hits_returns_a_fitting_prompt_unchanged():
    from nomoscope_workflow.prompts import fit_hits

    hits = [_hit("a", score=0.5), _hit("b", score=0.2)]
    assert fit_hits(hits, 10_000) == hits


def test_fit_hits_drops_lowest_ranked_first_and_keeps_order():
    from nomoscope_workflow.prompts import fit_hits

    hits = [
        _hit("located", method="located", score=0.0),
        _hit("top", score=1.03),
        _hit("tail", score=0.016),
        _hit("mid", score=0.03),
        _hit("later", method="later_in_year", score=0.02),
    ]
    kept = fit_hits(hits, 3 * 1150)
    assert [h.chunk_id for h in kept] == ["located", "top", "later"]


def test_fit_hits_never_drops_a_cited_chunk_and_unranked_go_last():
    from nomoscope_workflow.prompts import fit_hits

    hits = [
        _hit("cited", score=0.01),
        _hit("ranked", score=0.9),
        _hit("loc1", method="located"),
        _hit("loc2", method="located"),
    ]
    kept = fit_hits(hits, 2 * 1150, keep={"cited"})
    assert [h.chunk_id for h in kept] == ["cited", "loc1"]


def test_propose_trims_hits_to_the_model_window(monkeypatch):
    from datetime import date

    from nomoscope_workflow import llm
    from nomoscope_workflow.schema import (
        ParameterInformation,
        ParameterRecord,
    )

    seen = {}

    def fake_run_agent(model, system, user, output_type=str, **_):
        seen["chars"] = len(system) + len(user)
        return None

    monkeypatch.setattr(llm, "run_agent", fake_run_agent)
    monkeypatch.setitem(llm.CONTEXT_WINDOWS, "test/small", 30_000)
    record = ParameterRecord(
        information=ParameterInformation(
            country="LT", model_target="euromod://LT/x/def_const/$x", value_type="scalar", unit="/1"
        ),
        values=[],
    )
    hits = [_hit(f"h{i}", score=1 / (60 + i), size=20_000) for i in range(10)]
    llm.propose_with_llm("openrouter/test/small", record, date(2025, 7, 1), hits)
    assert seen["chars"] <= llm.prompt_budget_chars("openrouter/test/small")
