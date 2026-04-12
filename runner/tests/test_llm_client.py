"""Tests for LLM client."""

from benchmark.llm_client import _mock_response, call_llm, get_model_info


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

    def test_unknown_model(self):
        info = get_model_info("some-unknown-model")
        assert info["provider"] == "litellm"


class TestCallLlmDryRun:
    def test_dry_run_returns_mock(self):
        result = call_llm(model="gpt-4o", prompt="Test prompt", dry_run=True)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_dry_run_no_api_key_needed(self):
        # Should work without any API keys set
        result = call_llm(model="claude-sonnet-4", prompt="Test", dry_run=True)
        assert isinstance(result, str)
