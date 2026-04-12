# Task Author Skill

You are creating benchmark task definitions as YAML files for evaluating LLMs across 4 categories.

## Procedure

1. Read `/Users/bunyasit/.factory/missions/benchmark-mission/mission.md` for mission context
2. Read the existing task files in `tasks/` to understand the format and style
3. Create new task YAML files following the schema below
4. Validate all tasks pass schema validation

## Task YAML Schema

```yaml
id: SE-001
category: software-engineering  # software-engineering | planning | product-mind | startup-mind
title: "Fix Race Condition in WebSocket Handler"
description: "Identify and fix a race condition in a WebSocket message handler that causes duplicate messages under concurrent connections."
difficulty: hard  # easy | medium | hard
estimated_minutes: 30
language: python
project_ref: symphony
prompt: |
  Given the following WebSocket handler code from the Symphony project...
  [detailed prompt with code/context]
  
input_format: |
  Code snippet and test cases that reproduce the bug
  
output_format: |
  - Fixed code
  - Explanation of the race condition
  - Test case that proves the fix
  
grading:
  type: rubric  # reference_answer | rubric
  criteria:
    - name: Bug Identification
      weight: 0.25
      description: "Correctly identifies the race condition cause"
    - name: Fix Correctness
      weight: 0.40
      description: "Fix resolves the race condition without introducing new bugs"
    - name: Test Coverage
      weight: 0.20
      description: "Provides test case that proves the fix"
    - name: Explanation Quality
      weight: 0.15
      description: "Clear explanation of the root cause"
```

## Project References

Use these real projects from ~/dev as context:
- passionseed, careerac, pseed, 911stock, NeuralMix, freeflow
- FiJob, adwise, agent-x, pi-phone, onecha-line-bot, life-os
- coffee, hive, buildiff, knowme, rocketmap, portex-custom
- karmabook, csii-curriculum, goportex, symphony, skilliglot

## Task Distribution Requirements

Per category, ensure difficulty distribution:
- Easy: 30% (basic understanding, simple modifications)
- Medium: 50% (moderate complexity, multi-step reasoning)  
- Hard: 20% (architectural decisions, complex debugging)

## Language Coverage

- Python: 35% of tasks
- TypeScript/JavaScript: 30%
- Go: 10%
- Rust: 10%
- SQL/Shell/Other: 15%

## Important

- Each task must be self-contained and solvable without external context beyond what's provided
- Prompts must be specific enough to produce gradable outputs
- Reference answers must be complete and correct
- Rubric criteria must be measurable and unambiguous
