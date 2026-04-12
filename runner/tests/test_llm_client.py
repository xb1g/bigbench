"""Tests for LLM client."""

import os

from benchmark.llm_client import (
    MODEL_PRESETS,
    _mock_response,
    call_llm,
    get_model_info,
    resolve_model_config,
)


class TestMockResponse:
    def test_returns_string(self):
        result = _mock_response("Test prompt")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_contains_dry_run_marker(self):
        result = _mock_response("Test prompt")
        assert "Dry-Run" in result or "mock" in result.lower()

    def test_race_condition_prompt(self):
        result = _mock_response("Fix the race condition in async code")
        assert "asyncio" in result.lower() or "lock" in result.lower()

    def test_architecture_prompt(self):
        result = _mock_response("Design the architecture for a multi-tenant system")
        assert "architecture" in result.lower() or "layer" in result.lower()

    def test_user_journey_prompt(self):
        result = _mock_response("Map the user journey for a mobile app")
        assert "journey" in result.lower() or "stage" in result.lower()

    def test_business_prompt(self):
        result = _mock_response("Create a business model canvas for AI platform")
        assert "business" in result.lower() or "revenue" in result.lower()

    def test_generic_prompt(self):
        result = _mock_response("Explain quantum computing basics")
        assert len(result) > 50


class TestGetModelInfo:
    def test_openai_model(self):
        info = get_model_info("gpt-4o")
        assert info["provider"] == "openai"

    def test_claude_model(self):
        info = get_model_info("claude-sonnet-4")
        assert info["provider"] == "anthropic"

    def test_gemini_model(self):
        info = get_model_info("gemini/gemini-2.5-pro")
        assert info["provider"] == "google"

    def test_fireworks_model(self):
        info = get_model_info("openai/accounts/fireworks/routers/kimi-k2p5-turbo")
        assert info["provider"] == "fireworks"

    def test_ollama_prefix(self):
        info = get_model_info("ollama/llama3")
        assert info["provider"] == "ollama"

    def test_local_prefix(self):
        info = get_model_info("local/mistral")
        assert info["provider"] == "local"

    def test_fireworks_prefix(self):
        info = get_model_info("fireworks/kimi-k2p5-turbo")
        assert info["provider"] == "fireworks"

    def test_unknown_model(self):
        info = get_model_info("some-unknown-model")
        assert info["provider"] == "litellm"


class TestResolveModelConfig:
    """Tests for the resolve_model_config function that handles model prefix routing."""

    def test_ollama_preset(self):
        config = resolve_model_config("ollama/llama3")
        assert config["litellm_model"] == "ollama/llama3"
        assert config["api_base"] == "http://localhost:11434"
        assert config["api_key"] == "not-needed"

    def test_ollama_custom_model(self):
        """Non-preset ollama model still gets Ollama routing."""
        config = resolve_model_config("ollama/phi3")
        assert config["litellm_model"] == "ollama/phi3"
        assert config["api_base"] == "http://localhost:11434"
        assert config["api_key"] == "not-needed"

    def test_ollama_custom_api_base(self):
        """CLI --api-base overrides the Ollama default."""
        config = resolve_model_config("ollama/llama3", api_base="http://192.168.1.100:11434")
        assert config["api_base"] == "http://192.168.1.100:11434"

    def test_local_preset(self):
        config = resolve_model_config("local/llama3")
        assert config["litellm_model"] == "openai/llama3"
        assert config["api_base"] == "http://localhost:8080/v1"
        assert config["api_key"] == "not-needed"

    def test_local_custom_model(self):
        config = resolve_model_config("local/my-model")
        assert config["litellm_model"] == "openai/my-model"
        assert config["api_base"] == "http://localhost:8080/v1"

    def test_local_custom_api_base(self):
        config = resolve_model_config("local/llama3", api_base="http://localhost:1234/v1")
        assert config["api_base"] == "http://localhost:1234/v1"
        assert config["litellm_model"] == "openai/llama3"

    def test_fireworks_preset(self, monkeypatch):
        monkeypatch.setenv("FIREWORKS_API_KEY", "fw_test_key")
        config = resolve_model_config("fireworks/kimi-k2p5-turbo")
        assert config["litellm_model"] == "openai/accounts/fireworks/routers/kimi-k2p5-turbo"
        assert config["api_base"] == "https://api.fireworks.ai/inference/v1"
        assert config["api_key"] == "fw_test_key"

    def test_fireworks_custom_model(self, monkeypatch):
        monkeypatch.setenv("FIREWORKS_API_KEY", "fw_test_key")
        config = resolve_model_config("fireworks/my-custom-model")
        assert config["litellm_model"] == "openai/accounts/fireworks/my-custom-model"
        assert config["api_base"] == "https://api.fireworks.ai/inference/v1"

    def test_fireworks_api_key_override(self, monkeypatch):
        monkeypatch.setenv("FIREWORKS_API_KEY", "fw_env_key")
        config = resolve_model_config("fireworks/kimi-k2p5-turbo", api_key="fw_cli_key")
        assert config["api_key"] == "fw_cli_key"

    def test_standard_model_no_prefix(self, monkeypatch):
        """Standard litellm model passes through unchanged."""
        config = resolve_model_config("gpt-4o")
        assert config["litellm_model"] == "gpt-4o"

    def test_standard_model_uses_env_fallback(self, monkeypatch):
        """Standard models use FIREWORKS_API_BASE/KEY as fallback."""
        monkeypatch.setenv("FIREWORKS_API_BASE", "https://api.fireworks.ai/inference/v1")
        monkeypatch.setenv("FIREWORKS_API_KEY", "fw_key")
        config = resolve_model_config("gpt-4o")
        assert config["api_base"] == "https://api.fireworks.ai/inference/v1"
        assert config["api_key"] == "fw_key"

    def test_cli_flags_override_env(self, monkeypatch):
        monkeypatch.setenv("FIREWORKS_API_BASE", "https://env-base")
        monkeypatch.setenv("FIREWORKS_API_KEY", "env-key")
        config = resolve_model_config("gpt-4o", api_base="https://cli-base", api_key="cli-key")
        assert config["api_base"] == "https://cli-base"
        assert config["api_key"] == "cli-key"


class TestModelPresets:
    """Tests for the MODEL_PRESETS dictionary."""

    def test_all_presets_have_required_fields(self):
        for preset_id, preset in MODEL_PRESETS.items():
            assert "provider" in preset, f"{preset_id} missing 'provider'"
            assert "litellm_model" in preset, f"{preset_id} missing 'litellm_model'"
            assert "default_api_base" in preset, f"{preset_id} missing 'default_api_base'"
            assert "instructions" in preset, f"{preset_id} missing 'instructions'"

    def test_expected_presets_exist(self):
        expected = [
            "ollama/llama3",
            "ollama/codellama",
            "ollama/mistral",
            "local/llama3",
            "local/mistral",
            "fireworks/kimi-k2p5-turbo",
        ]
        for preset in expected:
            assert preset in MODEL_PRESETS, f"Missing preset: {preset}"


class TestCallLlmDryRun:
    def test_dry_run_returns_mock(self):
        result = call_llm(model="gpt-4o", prompt="Test prompt", dry_run=True)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dry_run_no_api_key_needed(self):
        # Should work without any API keys set
        result = call_llm(model="claude-sonnet-4", prompt="Test", dry_run=True)
        assert isinstance(result, str)

    def test_dry_run_with_ollama_model(self):
        result = call_llm(model="ollama/llama3", prompt="Test", dry_run=True)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dry_run_with_local_model(self):
        result = call_llm(model="local/llama3", prompt="Test", dry_run=True)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dry_run_with_fireworks_model(self):
        result = call_llm(model="fireworks/kimi-k2p5-turbo", prompt="Test", dry_run=True)
        assert isinstance(result, str)
        assert len(result) > 0
