"""LLM client wrapper using litellm with retry support."""

from __future__ import annotations

import logging
from typing import Optional

import litellm
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# Suppress litellm's noisy logs
litellm.suppress_debug_info = True

# Known retryable exceptions from litellm
_RETRYABLE_ERRORS = (
    litellm.RateLimitError,
    litellm.Timeout,
    litellm.InternalServerError,
    litellm.ServiceUnavailableError,
    litellm.APIConnectionError,
)

# Attempt to import additional error types
try:
    _RETRYABLE_ERRORS = _RETRYABLE_ERRORS + (litellm.ContentPolicyViolationError,)  # type: ignore[attr-defined]
except AttributeError:
    pass


def _get_logger():
    """Get a logger for retry attempts."""
    import logging
    return logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type(_RETRYABLE_ERRORS),
    before_sleep=before_sleep_log(_get_logger(), logging.WARNING),
    reraise=True,
)
def call_llm(
    model: str,
    prompt: str,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    dry_run: bool = False,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    """Send a prompt to the LLM and return the response text.

    Uses litellm for multi-provider support.
    Retries up to 3 times with exponential backoff on rate limits, timeouts, and server errors.

    Args:
        model: Model identifier (e.g., 'gpt-4o', 'claude-sonnet-4', 'gemini/gemini-2.5-pro')
        prompt: The prompt text
        temperature: Sampling temperature (0 for deterministic)
        max_tokens: Maximum tokens in response
        dry_run: If True, return a mock response without calling the API
        api_base: Optional custom API base URL
        api_key: Optional API key (otherwise uses env vars)

    Returns:
        The LLM response text.
    """
    if dry_run:
        return _mock_response(prompt)

    kwargs: dict = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    # Set API base if provided (e.g., Fireworks AI)
    if api_base:
        kwargs["api_base"] = api_base

    # Set API key if provided
    if api_key:
        kwargs["api_key"] = api_key

    response = litellm.completion(**kwargs)

    # Extract text from response
    content = response.choices[0].message.content  # type: ignore[union-attr]
    return content or ""


def _mock_response(prompt: str) -> str:
    """Generate a mock LLM response for dry-run mode.

    Produces a deterministic response based on the prompt content
    so that grading can still be exercised.
    """
    # Create a plausible mock response that includes some keywords from the prompt
    # This ensures grading logic can run and produce meaningful scores
    lines = [
        "# Mock Response (Dry-Run Mode)",
        "",
        "This is a simulated LLM response for testing purposes.",
        "No actual API calls were made.",
        "",
    ]

    # Extract some key terms from the prompt to make mock grading more realistic
    prompt_lower = prompt.lower()

    # Add category-specific mock content
    if "race condition" in prompt_lower or "async" in prompt_lower:
        lines.extend([
            "## Analysis",
            "The race condition occurs because multiple async tasks"
            " access shared state concurrently.",
            "## Solution",
            "Use asyncio.Lock() to serialize access to the shared resource.",
            "```python",
            "import asyncio",
            "",
            "lock = asyncio.Lock()",
            "",
            "async def safe_operation():",
            "    async with lock:",
            "        # perform git operation",
            "        pass",
            "```",
        ])
    elif "architecture" in prompt_lower or "design" in prompt_lower:
        lines.extend([
            "## Architecture Decision",
            "Based on the requirements, I recommend a layered architecture.",
            "1. **API Layer**: REST endpoints with authentication middleware",
            "2. **Service Layer**: Business logic with tenant isolation",
            "3. **Data Layer**: PostgreSQL with schema-per-tenant for isolation",
            "## Scaling Plan",
            "- Phase 1: Single server, schema-per-tenant",
            "- Phase 2: Read replicas, connection pooling",
            "- Phase 3: Horizontal sharding for 10K+ tenants",
        ])
    elif "user journey" in prompt_lower or "ux" in prompt_lower or "user" in prompt_lower:
        lines.extend([
            "## User Journey Map",
            "### Stage 1: Discovery",
            "- **Action**: User searches for solution",
            "- **Emotion**: Curious but skeptical",
            "- **Pain Point**: Too many options, unclear differentiation",
            "- **Moment of Delight**: Clear value proposition in first 10 seconds",
            "### Stage 2: Onboarding",
            "- **Action**: Signs up, completes profile",
            "- **Emotion**: Hopeful but anxious about complexity",
            "- **Pain Point**: Long setup process",
            "- **Moment of Delight**: Quick wins within first 5 minutes",
        ])
    elif "business" in prompt_lower or "pricing" in prompt_lower or "revenue" in prompt_lower:
        lines.extend([
            "## Business Model Canvas",
            "### Customer Segments",
            "- Primary: AI agent developers (indie to mid-size teams)",
            "- Secondary: Enterprise AI platform companies",
            "### Value Proposition",
            "- Reduce engineering time by 10x for agent memory infrastructure",
            "- MCP integration enables instant agent connectivity",
            "### Revenue Model",
            "- Free tier: 1K API calls/month",
            "- Pro: $49/month, 50K calls",
            "- Enterprise: Custom pricing",
        ])
    else:
        # Generic mock response
        lines.extend([
            "## Response",
            "Based on the requirements provided, here is my analysis and recommendation.",
            "",
            "1. The core issue is balancing complexity with maintainability",
            "2. I recommend following established patterns from the referenced project",
            "3. Implementation should proceed in phases with clear milestones",
            "",
            "This approach provides a solid foundation while allowing iteration.",
        ])

    return "\n".join(lines)


def get_model_info(model: str) -> dict[str, str]:
    """Return basic info about a model identifier for display purposes."""
    info: dict[str, str] = {"model": model}

    if (
        model.startswith("gpt")
        or model.startswith("o1")
        or model.startswith("o3")
        or model.startswith("o4")
    ):
        info["provider"] = "openai"
    elif "claude" in model:
        info["provider"] = "anthropic"
    elif "gemini" in model:
        info["provider"] = "google"
    elif "fireworks" in model or "accounts/fireworks" in model:
        info["provider"] = "fireworks"
    else:
        info["provider"] = "litellm"  # generic routing

    return info
