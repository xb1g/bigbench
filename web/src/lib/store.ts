"use client";

import { BenchmarkRun } from "./types";

const STORAGE_KEY = "llm-benchmark-runs";

export function getRuns(): BenchmarkRun[] {
  if (typeof window === "undefined") return [];
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw) as BenchmarkRun[];
  } catch {
    return [];
  }
}

export function saveRuns(runs: BenchmarkRun[]): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(runs));
}

export function addRun(run: BenchmarkRun): BenchmarkRun[] {
  const runs = getRuns();
  const existing = runs.findIndex((r) => r.run_id === run.run_id);
  if (existing >= 0) {
    runs[existing] = run;
  } else {
    runs.push(run);
  }
  saveRuns(runs);
  return runs;
}

export function getRunById(runId: string): BenchmarkRun | undefined {
  return getRuns().find((r) => r.run_id === runId);
}

export function deleteRun(runId: string): BenchmarkRun[] {
  const runs = getRuns().filter((r) => r.run_id !== runId);
  saveRuns(runs);
  return runs;
}

export function importJsonFile(file: File): Promise<BenchmarkRun> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target?.result as string) as BenchmarkRun;
        if (!data.run_id || !data.model_name || !data.per_task_results) {
          reject(new Error("Invalid benchmark results format"));
          return;
        }
        resolve(data);
      } catch (err) {
        reject(new Error("Failed to parse JSON file"));
      }
    };
    reader.onerror = () => reject(new Error("Failed to read file"));
    reader.readAsText(file);
  });
}
