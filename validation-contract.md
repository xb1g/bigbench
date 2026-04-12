# Validation Contract

## Area: Benchmark Task Coverage

### VAL-TASK-001: Software Engineering tasks exist
At least 10 software engineering benchmark tasks are defined, each with clear problem statement, expected output format, and grading rubric.
Tool: file-read
Evidence: task files count, structure validation

### VAL-TASK-002: Planning tasks exist
At least 8 planning benchmark tasks are defined, covering architecture design, requirements analysis, and decomposition.
Tool: file-read
Evidence: task files count, structure validation

### VAL-TASK-003: Product Mind tasks exist
At least 8 product mind benchmark tasks are defined, covering user empathy, feature prioritization, and UX awareness.
Tool: file-read
Evidence: task files count, structure validation

### VAL-TASK-004: Startup Mind tasks exist
At least 8 startup mind benchmark tasks are defined, covering business models, go-to-market, and resource allocation.
Tool: file-read
Evidence: task files count, structure validation

### VAL-TASK-005: Tasks are derived from real projects
Each benchmark task references a specific real project from ~/dev as its context/scenario.
Tool: file-read
Evidence: task YAML files contain project references

### VAL-TASK-006: Multi-language coverage
Benchmark includes tasks spanning multiple programming languages (Python, TypeScript, Go, Rust, etc.).
Tool: file-read
Evidence: task language field distribution

## Area: Benchmark Runner

### VAL-RUNNER-001: Runner installs and runs
`pip install -e .` succeeds and `llm-bench --help` shows available commands without errors.
Tool: terminal
Evidence: terminal output showing help text

### VAL-RUNNER-002: Runner can execute a single task
`llm-bench run --task <id> --model <model>` executes the task and produces a scored result.
Tool: terminal
Evidence: terminal output, result JSON file

### VAL-RUNNER-003: Runner executes full benchmark suite
`llm-bench run --all --model <model>` runs all tasks and produces a complete results file.
Tool: terminal
Evidence: terminal output, full results JSON

### VAL-RUNNER-004: Results include per-category scores
Results file contains scores for each of the 4 categories (software-engineering, planning, product-mind, startup-mind).
Tool: file-read
Evidence: results JSON has category breakdown

### VAL-RUNNER-005: Results include overall score
Results file contains an overall weighted score across all categories.
Tool: file-read
Evidence: results JSON has overall_score field

### VAL-RUNNER-006: Runner supports multiple models
Runner can execute benchmarks against different LLM providers (OpenAI, Anthropic, Google, local).
Tool: terminal
Evidence: successful runs with different model configs

### VAL-RUNNER-007: Auto-grading with reference answers
Tasks with reference answers are automatically graded against expected outputs.
Tool: terminal
Evidence: grading output matches reference scores

### VAL-RUNNER-008: Human-graded tasks support rubric scoring
Tasks without deterministic answers support rubric-based grading with clear scoring criteria.
Tool: file-read
Evidence: rubric fields in task definitions

## Area: Web Results Dashboard

### VAL-WEB-001: Dashboard loads and displays results
Web UI loads and shows a results table with model names, category scores, and overall scores.
Tool: agent-browser
Evidence: screenshot of dashboard with results

### VAL-WEB-002: Category breakdown visualization
Dashboard shows per-category score breakdown (radar chart or bar chart) for each model.
Tool: agent-browser
Evidence: screenshot of category breakdown

### VAL-WEB-003: Per-task results drill-down
Clicking a model/task reveals detailed results including raw LLM output and grading breakdown.
Tool: agent-browser
Evidence: screenshot of task detail view

### VAL-WEB-004: Model comparison view
Dashboard supports side-by-side comparison of two or more model runs.
Tool: agent-browser
Evidence: screenshot of comparison view

### VAL-WEB-005: Results import from JSON
Dashboard can load results from a JSON file (drag-drop or file picker).
Tool: agent-browser
Evidence: screenshot of import flow

## Area: Task Authoring System

### VAL-AUTHOR-001: Task YAML schema validates
All task YAML files pass schema validation (required fields: id, category, title, prompt, grading).
Tool: terminal
Evidence: validation command output

### VAL-AUTHOR-002: New tasks can be added via CLI
`llm-bench task create` command scaffolds a new task template.
Tool: terminal
Evidence: terminal output, created template file

## Cross-Area Flows

### VAL-CROSS-001: Full end-to-end pipeline
Run full benchmark suite → view results in web dashboard → compare models → export report. All steps complete without errors.
Tool: terminal + agent-browser
Evidence: screenshot of complete flow, exported report

### VAL-CROSS-002: Results persist across sessions
Results from a benchmark run can be loaded into the web UI in a separate session.
Tool: terminal + agent-browser
Evidence: screenshot showing loaded results
