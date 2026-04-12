"use client";

import { useEffect, useState } from "react";
import {
  BenchmarkRun,
  CATEGORY_KEYS,
  CATEGORY_LABELS,
  scoreColor,
} from "@/lib/types";
import { getRuns } from "@/lib/store";
import CategoryRadarChart from "@/components/CategoryRadarChart";

export default function ComparePage() {
  const [runs, setRuns] = useState<BenchmarkRun[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setRuns(getRuns());
    setMounted(true);
  }, []);

  const toggleRun = (runId: string) => {
    setSelectedIds((prev) =>
      prev.includes(runId)
        ? prev.filter((id) => id !== runId)
        : [...prev, runId]
    );
  };

  const selectedRuns = runs.filter((r) => selectedIds.includes(r.run_id));

  if (!mounted) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Compare Runs</h1>

      {/* Run selector */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">
          Select runs to compare (2+)
        </h2>
        {runs.length === 0 ? (
          <p className="text-sm text-gray-400">
            No runs available. Import results first.
          </p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {runs.map((run) => (
              <button
                key={run.run_id}
                onClick={() => toggleRun(run.run_id)}
                className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                  selectedIds.includes(run.run_id)
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                }`}
              >
                {run.model_name}
                <span className="text-xs opacity-75">{run.run_id}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {selectedRuns.length >= 2 && (
        <>
          {/* Radar chart comparison */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-lg font-semibold mb-4">Category Comparison</h2>
            <CategoryRadarChart
              scores={selectedRuns[0].category_scores}
              compareScores={selectedRuns[1].category_scores}
              compareLabel={selectedRuns[1].model_name}
            />
          </div>

          {/* Score comparison table */}
          <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold">Score Comparison</h2>
            </div>
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Metric
                  </th>
                  {selectedRuns.map((run) => (
                    <th
                      key={run.run_id}
                      className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                    >
                      {run.model_name}
                      <br />
                      <span className="text-gray-400 font-normal">
                        {run.run_id}
                      </span>
                    </th>
                  ))}
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Delta
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {/* Overall score */}
                <tr>
                  <td className="px-4 py-3 text-sm font-semibold">
                    Overall Score
                  </td>
                  {selectedRuns.map((run) => (
                    <td
                      key={run.run_id}
                      className={`px-4 py-3 text-sm font-semibold ${scoreColor(
                        run.overall_score
                      )}`}
                    >
                      {run.overall_score.toFixed(1)}
                    </td>
                  ))}
                  <DeltaCell
                    a={selectedRuns[0].overall_score}
                    b={selectedRuns[1].overall_score}
                  />
                </tr>
                {/* Category scores */}
                {CATEGORY_KEYS.map((key) => (
                  <tr key={key}>
                    <td className="px-4 py-3 text-sm font-medium">
                      {CATEGORY_LABELS[key]}
                    </td>
                    {selectedRuns.map((run) => (
                      <td
                        key={run.run_id}
                        className={`px-4 py-3 text-sm ${scoreColor(
                          run.category_scores[key]
                        )}`}
                      >
                        {run.category_scores[key].toFixed(1)}
                      </td>
                    ))}
                    <DeltaCell
                      a={selectedRuns[0].category_scores[key]}
                      b={selectedRuns[1].category_scores[key]}
                    />
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {selectedRuns.length === 1 && (
        <p className="text-sm text-gray-400 text-center py-8">
          Select at least one more run to compare.
        </p>
      )}
    </div>
  );
}

function DeltaCell({ a, b }: { a: number; b: number }) {
  const delta = b - a;
  if (Math.abs(delta) < 0.05) {
    return (
      <td className="px-4 py-3 text-sm text-gray-400">—</td>
    );
  }
  const isPositive = delta > 0;
  return (
    <td
      className={`px-4 py-3 text-sm font-semibold ${
        isPositive ? "text-green-600" : "text-red-600"
      }`}
    >
      {isPositive ? "▲" : "▼"} {Math.abs(delta).toFixed(1)}
    </td>
  );
}
