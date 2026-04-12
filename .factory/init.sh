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
  cat > .env << 'EOF'
# LLM API Keys (uncomment and add your keys)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...

# Grading model (defaults to gpt-4o)
# GRADING_MODEL=gpt-4o

# Default temperature (0 for deterministic grading)
# DEFAULT_TEMPERATURE=0
EOF
  echo "Created .env template - add your API keys for real benchmark runs"
fi

# Install runner dependencies
if [ -f "runner/pyproject.toml" ]; then
  cd runner && pip install -e ".[dev]" > /dev/null 2>&1 && echo "Runner installed" && cd ..
fi

echo "Benchmark environment ready"
