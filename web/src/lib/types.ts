export interface CriterionScore {
  name: string;
  score: number;
  max_score: number;
  weight: number;
  rationale: string;
}

export interface GradingDetails {
  grading_method: string;
  total_score: number;
  criterion_scores: CriterionScore[];
  reference_match_type: string | null;
  rationale: string;
}

export interface TaskResult {
  task_id: string;
  category: string;
  score: number;
  raw_output: string;
  grading_details: GradingDetails;
  error: string | null;
  dry_run?: boolean;
}

export interface CategoryScores {
  software_engineering: number;
  planning: number;
  product_mind: number;
  startup_mind: number;
}

export interface BenchmarkRun {
  run_id: string;
  model_name: string;
  timestamp: string;
  overall_score: number;
  category_scores: CategoryScores;
  per_task_results: TaskResult[];
}

export const CATEGORY_LABELS: Record<string, string> = {
  software_engineering: "Software Engineering",
  planning: "Planning",
  product_mind: "Product Mind",
  startup_mind: "Startup Mind",
};

export const CATEGORY_KEYS = [
  "software_engineering",
  "planning",
  "product_mind",
  "startup_mind",
] as const;

export function scoreColor(score: number): string {
  if (score >= 70) return "text-green-600";
  if (score >= 40) return "text-yellow-600";
  return "text-red-600";
}

export function scoreBg(score: number): string {
  if (score >= 70) return "bg-green-50 text-green-700";
  if (score >= 40) return "bg-yellow-50 text-yellow-700";
  return "bg-red-50 text-red-700";
}
