#!/usr/bin/env bash
set -e

cd /Users/bunyasit/dev/llm-benchmark

# Ensure directory structure exists
mkdir -p tasks/{software-engineering,planning,product-mind,startup-mind}
mkdir -p results
mkdir -p runner/src/benchmark
mkdir -p web

# Check Python availability
if ! command -v python3 &> /dev/null; then
  echo "ERROR: python3 not found"
  exit 1
fi

# Create .env if not exists
if [ ! -f ".env" ]; then
  cat > .env << 'ENVEOF'
# Primary model: Kimi K2.5 Turbo on Fireworks AI (OpenAI-compatible)
FIREWORKS_API_KEY=fw_4ajrh4wPMyYVJT9oZskV6j
FIREWORKS_API_BASE=https://api.fireworks.ai/inference/v1
DEFAULT_MODEL=openai/accounts/fireworks/routers/kimi-k2p5-turbo

# Additional providers (uncomment if available)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...

# Local LLM support (use model prefix: ollama/*, local/*, fireworks/*)
# Ollama - run 'ollama serve' first
# DEFAULT_MODEL=ollama/llama3
# OLLAMA_API_BASE=http://localhost:11434

# Generic OpenAI-compatible (vLLM, llama.cpp, LM Studio)
# DEFAULT_MODEL=local/llama3
# LOCAL_API_BASE=http://localhost:8080/v1

# Grading model (uses same Fireworks model by default)
# GRADING_MODEL=openai/accounts/fireworks/routers/kimi-k2p5-turbo

# Default temperature (0 for deterministic grading)
DEFAULT_TEMPERATURE=0
ENVEOF
  echo "Created .env template - add your API keys for real benchmark runs"
fi

# Install runner dependencies
if [ -f "runner/pyproject.toml" ]; then
  cd runner && pip install -e ".[dev]" > /dev/null 2>&1 && echo "Runner installed" && cd ..
fi

echo "Benchmark environment ready"
