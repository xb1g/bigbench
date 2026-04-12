# LLM Benchmark Report

**Date Generated:** 2026-04-12
**Models Compared:** 32
**Runs Analyzed:** 32

> ⚠ **Note:** Some results are from dry-run mode (mock LLM responses)

## Executive Summary

| Rank | Model | Overall Score | SE | Planning | Product Mind | Startup Mind | Rating |
|-----:|-------|-------------:|---:|--------:|-------------:|-------------:|--------|
| 1 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 2 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 3 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 4 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 5 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 6 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 7 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 8 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 9 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 10 | gpt-4o | 59.0 | 53.6 | 65.1 | 63.4 | 57.4 | 🟠 Needs Improvement |
| 11 | openai/accounts/fireworks/routers/kimi-k2p5-turbo | 34.8 | 87.0 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 12 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 13 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 14 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 15 | claude-sonnet-4 | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 16 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 17 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 18 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 19 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 20 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 21 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 22 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 23 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 24 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 25 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 26 | gemini/gemini-2.5-pro | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 27 | gpt-4o | 27.8 | 69.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 28 | gemini/gemini-2.5-pro | 25.0 | 62.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 29 | claude-sonnet-4 | 25.0 | 62.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 30 | gpt-4o | 25.0 | 62.6 | 0.0 | 0.0 | 0.0 | 🔴 Poor |
| 31 | openai/accounts/fireworks/routers/kimi-k2p5-turbo | 18.1 | 0.0 | 72.6 | 0.0 | 0.0 | 🔴 Poor |
| 32 | openai/accounts/fireworks/routers/kimi-k2p5-turbo | 11.9 | 0.0 | 47.8 | 0.0 | 0.0 | 🔴 Poor |

## Per-Category Analysis

### Software Engineering (weight: 40%)

| Metric | Value |
|--------|------|
| Average Score | 60.1 |
| Best Model | openai/accounts/fireworks/routers/kimi-k2p5-turbo (87.0) |
| Worst Model | openai/accounts/fireworks/routers/kimi-k2p5-turbo (0.0) |
| Score Range | 87.0 |

**Score Distribution:**

| Model | Score | Visual |
|-------|------:|--------|
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 87.0 | `█████████████████░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| claude-sonnet-4 | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 69.6 | `█████████████░░░░░░░` |
| gpt-4o | 69.6 | `█████████████░░░░░░░` |
| gemini/gemini-2.5-pro | 62.6 | `████████████░░░░░░░░` |
| claude-sonnet-4 | 62.6 | `████████████░░░░░░░░` |
| gpt-4o | 62.6 | `████████████░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| gpt-4o | 53.6 | `██████████░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |

### Planning (weight: 25%)

| Metric | Value |
|--------|------|
| Average Score | 24.1 |
| Best Model | openai/accounts/fireworks/routers/kimi-k2p5-turbo (72.6) |
| Worst Model | openai/accounts/fireworks/routers/kimi-k2p5-turbo (0.0) |
| Score Range | 72.6 |

**Score Distribution:**

| Model | Score | Visual |
|-------|------:|--------|
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 72.6 | `██████████████░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| gpt-4o | 65.1 | `█████████████░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 47.8 | `█████████░░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| claude-sonnet-4 | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| claude-sonnet-4 | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |

### Product Mind (weight: 20%)

| Metric | Value |
|--------|------|
| Average Score | 19.8 |
| Best Model | gpt-4o (63.4) |
| Worst Model | openai/accounts/fireworks/routers/kimi-k2p5-turbo (0.0) |
| Score Range | 63.4 |

**Score Distribution:**

| Model | Score | Visual |
|-------|------:|--------|
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| gpt-4o | 63.4 | `████████████░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| claude-sonnet-4 | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| claude-sonnet-4 | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |

### Startup Mind (weight: 15%)

| Metric | Value |
|--------|------|
| Average Score | 17.9 |
| Best Model | gpt-4o (57.4) |
| Worst Model | openai/accounts/fireworks/routers/kimi-k2p5-turbo (0.0) |
| Score Range | 57.4 |

**Score Distribution:**

| Model | Score | Visual |
|-------|------:|--------|
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| gpt-4o | 57.4 | `███████████░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| openai/accounts/fireworks/routers/kimi-k2p5-turbo | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| claude-sonnet-4 | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| claude-sonnet-4 | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gemini/gemini-2.5-pro | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |
| gpt-4o | 0.0 | `░░░░░░░░░░░░░░░░░░░░` |

## Per-Model Breakdown

### openai/accounts/fireworks/routers/kimi-k2p5-turbo

- **Run ID:** 20260412_140608
- **Overall Score:** 18.1 (Poor)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 0.0 | 40% | 0.0 |
| Planning | 72.6 | 25% | 18.1 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **PLAN-002** (planning): 94.0
- **PLAN-010** (planning): 92.5
- **PLAN-005** (planning): 90.0

**Bottom 3 Tasks:**

- **PLAN-003** (planning): 65.0
- **PLAN-001** (planning): 45.0
- **PLAN-007** (planning): 0.0

### openai/accounts/fireworks/routers/kimi-k2p5-turbo

- **Run ID:** 20260412_140059
- **Overall Score:** 11.9 (Poor)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 0.0 | 40% | 0.0 |
| Planning | 47.8 | 25% | 11.9 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **PLAN-005** (planning): 90.0
- **PLAN-001** (planning): 88.5
- **PLAN-002** (planning): 60.5

**Bottom 3 Tasks:**

- **PLAN-002** (planning): 60.5
- **PLAN-003** (planning): 0.0
- **PLAN-004** (planning): 0.0

### openai/accounts/fireworks/routers/kimi-k2p5-turbo

- **Run ID:** 20260412_140050
- **Overall Score:** 34.8 (Poor)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 87.0 | 40% | 34.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 87.0

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 87.0

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_135729
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_135728
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_135721
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_135612
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### claude-sonnet-4

- **Run ID:** 20260412_135611
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_135606
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_134549
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_134548
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_134544
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gpt-4o

- **Run ID:** 20260412_134543
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_133320
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_133311
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_133228
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_133227
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_133222
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gpt-4o

- **Run ID:** 20260412_133221
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_133204
- **Overall Score:** 25.0 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 62.6 | 40% | 25.0 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-005** (software-engineering): 62.6

**Bottom 3 Tasks:**

- **SE-005** (software-engineering): 62.6

### claude-sonnet-4

- **Run ID:** 20260412_133202
- **Overall Score:** 25.0 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 62.6 | 40% | 25.0 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-005** (software-engineering): 62.6

**Bottom 3 Tasks:**

- **SE-005** (software-engineering): 62.6

### gpt-4o

- **Run ID:** 20260412_133200
- **Overall Score:** 25.0 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 62.6 | 40% | 25.0 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-005** (software-engineering): 62.6

**Bottom 3 Tasks:**

- **SE-005** (software-engineering): 62.6

### gpt-4o

- **Run ID:** 20260412_133131
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gpt-4o

- **Run ID:** 20260412_133126
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_133013
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_133007
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_132812
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_132807
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gemini/gemini-2.5-pro

- **Run ID:** 20260412_132756
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

### gpt-4o

- **Run ID:** 20260412_132751
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gpt-4o

- **Run ID:** 20260412_132526
- **Overall Score:** 59.0 (Needs Improvement)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 53.6 | 40% | 21.4 |
| Planning | 65.1 | 25% | 16.3 |
| Product Mind | 63.4 | 20% | 12.7 |
| Startup Mind | 57.4 | 15% | 8.6 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6
- **PLAN-001** (planning): 68.5
- **START-009** (startup-mind): 67.2

**Bottom 3 Tasks:**

- **SE-003** (software-engineering): 0.0
- **SE-009** (software-engineering): 0.0
- **START-007** (startup-mind): 0.0

### gpt-4o

- **Run ID:** 20260412_132513
- **Overall Score:** 27.8 (Poor)
- **Mode:** Dry-run (mock responses)

| Category | Score | Weight | Weighted |
|----------|------:|-------:|---------:|
| Software Engineering | 69.6 | 40% | 27.8 |
| Planning | 0.0 | 25% | 0.0 |
| Product Mind | 0.0 | 20% | 0.0 |
| Startup Mind | 0.0 | 15% | 0.0 |

**Top 3 Tasks:**

- **SE-001** (software-engineering): 69.6

**Bottom 3 Tasks:**

- **SE-001** (software-engineering): 69.6

## Recommendations

1. **Best overall model:** gpt-4o (score: 59.0). Recommended as the primary choice.
2. **Best for Software Engineering:** openai/accounts/fireworks/routers/kimi-k2p5-turbo (87.0). Consider this model for software engineering-focused tasks.
2. **Best for Planning:** openai/accounts/fireworks/routers/kimi-k2p5-turbo (72.6). Consider this model for planning-focused tasks.
3. **Significant gap:** 47.1 points between best and worst. The lower-performing model may not be suitable for this benchmark's requirements.
4. **Systemic weakness:** All models struggle with: Planning, Product Mind, Startup Mind. This may indicate the tasks need prompt refinement or that current LLMs lack capability in these areas.

