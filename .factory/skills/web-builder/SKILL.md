# Web Builder Skill

You are building a Next.js web dashboard for visualizing LLM benchmark results.

## Procedure

1. Read `/Users/bunyasit/.factory/missions/benchmark-mission/mission.md` for mission context
2. Initialize Next.js project in `/Users/bunyasit/dev/llm-benchmark/web/`
3. Build pages incrementally, testing each before moving to the next

## Tech Stack

- Next.js 15 with App Router
- TypeScript
- Tailwind CSS
- Recharts for charts (radar, bar, line)
- shadcn/ui for UI components

## Pages

1. **Home (/)** - Table of benchmark runs with overall scores
2. **Run Detail (/run/[id])** - Radar chart, per-task scores, model info
3. **Task Detail (/run/[runId]/task/[taskId])** - Raw output, reference answer, grading breakdown
4. **Compare (/compare)** - Side-by-side model comparison

## Key Features

- Drag-drop JSON import for results files
- Responsive design (mobile + desktop)
- Clean, minimal, professional styling
- Dark mode support

## Testing

- Run `pnpm dev` and verify pages load at localhost:3200
- Use agent-browser for manual testing
- Test with sample results JSON files
