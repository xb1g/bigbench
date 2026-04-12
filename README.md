# LLM Software Engineering Benchmark

A comprehensive benchmark that evaluates LLM capabilities across four dimensions: software engineering, planning, product thinking, and startup mindset. Each dimension is weighted to reflect its relative importance in real-world AI-assisted development.

## Quick Start

```bash
# Install the runner
cd runner
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Set up API credentials (see Fireworks AI Setup below)
export FIREWORKS_API_KEY=your-key-here
export FIREWORKS_API_BASE=https://api.fireworks.ai/inference/v1
export DEFAULT_MODEL=accounts/fireworks/routers/kimi-k2p5-turbo

# Run a dry-run to verify setup (no API calls)
llm-bench run --all --model accounts/fireworks/routers/kimi-k2p5-turbo --dry-run

# Run the full benchmark suite
llm-bench run --all --model accounts/fireworks/routers/kimi-k2p5-turbo
```

## Project Structure

```
llm-benchmark/
├── tasks/                        # Benchmark task definitions (YAML)
│   ├── schema.yaml               # Task schema specification
│   ├── software-engineering/     # 12 tasks (SE-001 to SE-012)
│   ├── planning/                 # 10 tasks (PLAN-001 to PLAN-010)
│   ├── product-mind/             # 10 tasks (PROD-001 to PROD-010)
│   └── startup-mind/             # 10 tasks (START-001 to START-010)
├── runner/                       # Python benchmark runner
│   ├── pyproject.toml
│   ├── src/benchmark/            # Core package
│   │   ├── cli.py                # CLI interface (Click)
│   │   ├── runner.py             # Task execution orchestration
│   │   ├── llm_client.py         # LLM API client (litellm)
│   │   ├── grader.py             # Scoring and grading logic
│   │   ├── loader.py             # Task YAML loader and validator
│   │   ├── models.py             # Pydantic data models
│   │   ├── results.py            # Results storage and scoring
│   │   └── report.py             # Report generation
│   └── tests/                    # Test suite
├── web/                          # Next.js visualization dashboard
│   ├── package.json
│   └── src/                      # React components and pages
├── results/                      # Stored benchmark run results (JSON)
└── report.md                     # Latest exported report
```

## Task Categories

| Category | Prefix | Tasks | Weight | What It Measures |
|---|---|---|---|---|
| Software Engineering | SE | 12 | 40% | Code understanding, debugging, refactoring, implementation |
| Planning | PLAN | 10 | 25% | System design, requirements analysis, decomposition, trade-off analysis |
| Product Mind | PROD | 10 | 20% | User empathy, feature prioritization, UX awareness, market fit |
| Startup Mind | START | 10 | 15% | Business models, go-to-market, resource allocation, growth thinking |

Tasks are defined as YAML files with structured prompts, grading rubrics, and difficulty levels (easy/medium/hard). Each task references a real project under `~/dev/` for grounded, practical evaluation.

## Running Benchmarks

### Single Task

```bash
llm-bench run --task SE-001 --model accounts/fireworks/routers/kimi-k2p5-turbo
```

### Full Suite

```bash
llm-bench run --all --model accounts/fireworks/routers/kimi-k2p5-turbo
```

### Dry-Run (No API Calls)

```bash
llm-bench run --all --model accounts/fireworks/routers/kimi-k2p5-turbo --dry-run
```

Runs all tasks with mock LLM responses. Useful for verifying setup and exercising grading logic without consuming API credits.

### Subset of Tasks

```bash
llm-bench run --all --model accounts/fireworks/routers/kimi-k2p5-turbo --limit 5
```

### View Results

```bash
llm-bench results list              # List all runs
llm-bench results <run-id>          # Detailed view of a specific run
```

### Task Management

```bash
llm-bench task list                 # List all benchmark tasks
llm-bench task validate             # Validate all task YAML files against schema
llm-bench task create --category software-engineering --id SE-013  # Scaffold a new task
```

### Report Export

```bash
llm-bench report export --format markdown    # Export all runs as report.md
llm-bench report export --format json        # Export all runs as report.json
llm-bench report export --run-id 20260412_132807 --run-id 20260412_133131 --format markdown
```

## Fireworks AI Setup

The benchmark uses Fireworks AI as the primary model provider. Configure the following environment variables:

```bash
export FIREWORKS_API_KEY=your-api-key-here
export FIREWORKS_API_BASE=https://api.fireworks.ai/inference/v1
export DEFAULT_MODEL=accounts/fireworks/routers/kimi-k2p5-turbo
```

The runner uses [litellm](https://github.com/BerriAI/litellm) under the hood, so other providers (OpenAI, Anthropic, Google) also work by passing a different model identifier and ensuring the corresponding API key is set.

Optional grading configuration:

```bash
export GRADING_MODEL=accounts/fireworks/routers/kimi-k2p5-turbo   # Model for LLM-as-judge grading
export DEFAULT_TEMPERATURE=0                                       # 0 for deterministic results
```

## Web Dashboard

A Next.js visualization dashboard is available for exploring results interactively.

```bash
cd web
pnpm install
pnpm dev
```

The dashboard starts on port 3200. It provides:

- Category radar charts comparing runs
- Per-task score breakdowns
- Run comparison views
- Result import from stored JSON files

## Scoring

### Per-Category Score

Each category score is the average of all task scores within that category. Tasks are graded on a 0-100 scale using either:

- **Rubric grading**: Multiple weighted criteria scored by an LLM-as-judge
- **Reference answer grading**: Exact match, structural similarity, or code equivalence against a known answer

### Overall Weighted Score

```
overall = software_engineering * 0.40
        + planning              * 0.25
        + product_mind           * 0.20
        + startup_mind           * 0.15
```

Weights reflect the relative importance of each dimension in software development. Software engineering carries the highest weight because code correctness is non-negotiable; planning is next because poor architecture compounds over time; product and startup thinking are valuable but more context-dependent.

## Adding New Tasks

1. Create a YAML file in the appropriate category directory under `tasks/`:
   - `tasks/software-engineering/SE-013.yaml`
   - `tasks/planning/PLAN-011.yaml`
   - `tasks/product-mind/PROD-011.yaml`
   - `tasks/startup-mind/START-011.yaml`

2. Or use the scaffold command:
   ```bash
   llm-bench task create --category planning --id PLAN-011
   ```

3. Edit the generated template. Required fields:
   - `id`, `category`, `title`, `description`
   - `difficulty` (easy/medium/hard), `estimated_minutes`, `language`
   - `project_ref` (directory under `~/dev/`)
   - `prompt` (200+ words, specific enough for gradable outputs)
   - `input_format`, `output_format`
   - `grading` (rubric with weighted criteria, or reference_answer)

4. Validate the task:
   ```bash
   llm-bench task validate
   ```

## Requirements

- Python 3.10+
- Node.js 18+
- pnpm
