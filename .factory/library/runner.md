# Runner Package

## Setup

The runner requires Python 3.10+ (system Python is 3.9.6, so use the venv).

```bash
# Create venv with Python 3.12 (already done)
/opt/homebrew/bin/python3.12 -m venv /Users/bunyasit/dev/llm-benchmark/runner/.venv

# Install
/Users/bunyasit/dev/llm-benchmark/runner/.venv/bin/pip install -e "/Users/bunyasit/dev/llm-benchmark/runner[dev]"

# Run CLI
/Users/bunyasit/dev/llm-benchmark/runner/.venv/bin/llm-bench --help
```

## Architecture

The runner is structured as:

- `src/benchmark/models.py` - Pydantic models for results, tasks, grading
- `src/benchmark/loader.py` - Load/validate task YAML files from tasks/
- `src/benchmark/llm_client.py` - litellm wrapper with tenacity retries
- `src/benchmark/grader.py` - Auto-grading + rubric + LLM-as-judge
- `src/benchmark/runner.py` - Core execution orchestration + Rich output
- `src/benchmark/results.py` - Atomic JSON storage + category/overall scoring
- `src/benchmark/cli.py` - Click CLI (run, results, task, report commands)

## Key Design Decisions

- **Overall score formula**: SE*0.40 + Planning*0.25 + Product*0.20 + Startup*0.15
- **Category scores**: Average of task scores in that category
- **Dry-run mode**: Category-aware mock responses based on prompt keywords
- **Atomic writes**: Write .tmp then os.replace() for crash safety
- **Error resilience**: Single task failures recorded, not crashing the suite
- **Retry**: 3 retries with exponential backoff via tenacity

## Tasks with reference_answer grading

3 tasks use `reference_answer` instead of `rubric`:
- SE-003, SE-009 (software-engineering)
- START-007 (startup-mind)

These score 0 in dry-run mode because mock responses don't match the reference.
This is correct behavior — real LLM runs should produce matching output.

## Tests

77 tests in `runner/tests/` covering models, loader, grader, results, llm_client, and CLI.
Run with: `/Users/bunyasit/dev/llm-benchmark/runner/.venv/bin/python -m pytest -v`
