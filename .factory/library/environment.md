# Environment

Environment variables, external dependencies, and setup notes.

## Primary LLM Model

**Model:** `accounts/fireworks/routers/kimi-k2p5-turbo` (Kimi K2.5 Turbo)  
**Provider:** Fireworks AI (OpenAI-compatible API)  
**API Base:** `https://api.fireworks.ai/inference/v1`  
**Auth:** FIREWORKS_API_KEY env var  

## Usage via litellm

```python
import litellm
import os

# Method 1: Using openai/ prefix with custom api_base
response = litellm.completion(
    model="openai/accounts/fireworks/routers/kimi-k2p5-turbo",
    messages=[{"role": "user", "content": "Hello"}],
    api_base=os.environ["FIREWORKS_API_BASE"],
    api_key=os.environ["FIREWORKS_API_KEY"],
    temperature=0,
)
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| FIREWORKS_API_KEY | Yes | Fireworks AI API key |
| FIREWORKS_API_BASE | Yes | `https://api.fireworks.ai/inference/v1` |
| DEFAULT_MODEL | No | Default: `openai/accounts/fireworks/routers/kimi-k2p5-turbo` |
| DEFAULT_TEMPERATURE | No | Default: 0 (deterministic) |
| GRADING_MODEL | No | Model for LLM-as-judge grading (defaults to DEFAULT_MODEL) |
| OPENAI_API_KEY | No | Optional: for OpenAI models |
| ANTHROPIC_API_KEY | No | Optional: for Claude models |

## Key Notes

- Fireworks API is fully OpenAI-compatible — same request/response format
- No special SDK needed — works with litellm's `openai/` provider prefix
- API key should be in `.env` file (never committed to git)
