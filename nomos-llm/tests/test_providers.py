from nomos_llm import env, providers


def test_settings_are_built_in_one_place():
    assert "temperature" not in providers.model_settings("azure_openai/gpt-6-luna", 0.2)
    assert providers.model_settings("anthropic/claude-sonnet-5", 0.0, timeout=5)["timeout"] == 5


def test_repo_root_holds_the_workspace():
    assert (env.repo_root() / "pyproject.toml").is_file()
