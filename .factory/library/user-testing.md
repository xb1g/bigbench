# User Testing

## Validation Surfaces

### 1. CLI (Benchmark Runner)
- **Tool**: Terminal commands
- **Testing approach**: Execute CLI commands, verify output format and exit codes
- **Key flows**: 
  - `llm-bench --help` → shows all commands
  - `llm-bench run --task <id> --model <model>` → single task execution
  - `llm-bench run --all --model <model>` → full suite
  - `llm-bench task validate` → task validation
  - `llm-bench report export` → report generation

### 2. Web Dashboard
- **Tool**: agent-browser
- **Testing approach**: Navigate pages, verify UI elements, test interactions
- **Key flows**:
  - Load dashboard → see results table
  - Click run → see radar chart and task details
  - Import JSON → see results appear
  - Compare models → see side-by-side with deltas
- **Port**: 3200

## Validation Concurrency

**CLI**: Sequential testing only (no concurrency concerns)

**Web Dashboard (agent-browser)**: 
- Machine: macOS, ~16GB RAM
- Dev server: ~200MB, each agent-browser session: ~300MB
- Max concurrent validators: **3** (fits within 70% headroom)
- Note: Dashboard is client-side only, lightweight

## Testing Notes

- Use `--dry-run` flag for testing without API costs
- Sample results JSON can be used for web UI testing without running real benchmarks
- Dry-run mode is sufficient for validating the full pipeline structure
