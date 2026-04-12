# Architecture

## System Components

### 1. Task Definitions (`tasks/`)
- YAML files organized by category: `tasks/{software-engineering,planning,product-mind,startup-mind}/`
- Each file defines: id, category, title, prompt, grading criteria, difficulty, language, project context
- Schema defined in `tasks/schema.yaml`
- Loaded at runtime by the runner

### 2. Benchmark Runner (`runner/`)
- Python package installed via pip (`llm-bench` CLI command)
- **CLI Layer** (Click): Command routing, argument parsing, Rich terminal output
- **Task Loader**: Reads YAML files, validates against schema, resolves project references
- **LLM Executor**: Uses litellm to route prompts to correct provider (OpenAI/Anthropic/Google)
- **Grading Engine**: 
  - Auto-grading: compares output against reference answers (exact match, structural similarity)
  - Rubric-grading: scores against weighted criteria (0-10 per criterion)
  - LLM-as-judge: fallback for open-ended evaluation
- **Result Writer**: Atomic JSON writes to `results/<run_id>/`

### 3. Results Storage (`results/`)
- File-based: `results/<timestamp>/results.json`
- Schema: `{run_id, model_name, timestamp, overall_score, category_scores{}, per_task_results[]}`
- No database needed - portable JSON files

### 4. Web Dashboard (`web/`)
- Next.js 15 App Router, TypeScript, Tailwind CSS
- Client-side only (no backend API) - reads JSON files directly
- Pages: Home (runs table), Run Detail (radar chart + task table), Task Detail (output + grading), Compare (side-by-side)

## Data Flow

```
Task YAML → Task Loader → LLM Executor → Raw Output → Grading Engine → Scored Result
                                                                      ↓
Results JSON ← Result Writer ←───────────────────────────────────────┘
       ↓
Web Dashboard (reads JSON, visualizes)
```

## Key Design Decisions

- **File-based storage**: No database dependency, results are portable and shareable
- **litellm**: Single interface for all LLM providers, avoids provider-specific code
- **Deterministic grading**: temperature=0 for grading ensures reproducibility
- **Dry-run mode**: Full pipeline test without API costs
- **Atomic writes**: Results written to .tmp then renamed to prevent corruption
