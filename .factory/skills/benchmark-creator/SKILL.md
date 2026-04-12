# Benchmark Creator Skill

You are building a Python CLI benchmark tool for evaluating LLMs.

## Procedure

1. Read `/Users/bunyasit/.factory/missions/benchmark-mission/mission.md` for mission context
2. Read `/Users/bunyasit/.factory/missions/benchmark-mission/AGENTS.md` for constraints
3. Read the assigned feature from `features.json` in the mission directory
4. Implement the feature as described
5. Test your implementation before committing
6. Commit changes with a descriptive message

## Key Patterns

- Use Click for CLI commands
- Use litellm for multi-provider LLM calls
- Use Pydantic for data validation
- Use Rich for terminal output formatting
- Use tenacity for retry logic
- Results stored as JSON in `results/<run_id>/` directory
- Tasks loaded from YAML files in `tasks/` directory

## Testing

- Run `pytest` in the runner directory
- For LLM calls, use `--dry-run` flag to avoid API costs during development
- Verify CLI commands work: `llm-bench --help`, `llm-bench run --help`

## Important

- The benchmark runner must work without API keys in dry-run mode
- All results must be deterministic given the same model and temperature=0
- Error handling is critical - never crash the entire run on a single task failure
