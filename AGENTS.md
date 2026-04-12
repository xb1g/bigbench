# Mission: LLM Software Engineering Benchmark

## Mission Boundaries (NEVER VIOLATE)

**Port Range:** 3200-3299. Never start services outside this range.

**Directory:**
- Working directory: /Users/bunyasit/dev/llm-benchmark
- Read ~/dev project code for reference ONLY (do not modify projects in ~/dev)
- Never modify any project outside ~/dev/llm-benchmark/

**External Services:**
- USE OpenAI API if key is available (OPENAI_API_KEY env var)
- USE Anthropic API if key is available (ANTHROPIC_API_KEY env var)
- DO NOT create new cloud resources or paid services

**Off-Limits:**
- ~/dev subdirectories except for reading as reference
- Any ~/.config or system-level configuration
- Port 3000 (common dev server)

## Architecture

Python-based benchmark tool with:
1. **Task definitions** (YAML files in `tasks/` directory)
2. **Runner CLI** (Python package with click/argparse)
3. **Grading system** (auto-grading with reference answers + rubric-based)
4. **Web results dashboard** (Next.js app for visualization)

## Conventions

- Python 3.10+ for runner (no heavy dependencies)
- YAML for task definitions
- JSON for results
- TypeScript/Next.js for web UI
- All code in /Users/bunyasit/dev/llm-benchmark/

## Testing & Validation Guidance

- Benchmark runner must be testable via CLI commands
- Web UI testable via agent-browser
- Results are deterministic given same model + temperature=0
