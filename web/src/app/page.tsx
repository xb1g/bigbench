"use client";

import { useEffect, useState } from "react";
import { BenchmarkRun, CATEGORY_LABELS, CATEGORY_KEYS, scoreColor } from "@/lib/types";
import { getRuns, addRun, deleteRun } from "@/lib/store";
import ImportButton from "@/components/ImportButton";

export default function HomePage() {
  const [runs, setRuns] = useState<BenchmarkRun[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setRuns(getRuns());
    setMounted(true);
  }, []);

  const handleImport = (updated: BenchmarkRun[]) => {
    setRuns(updated);
  };

  const handleDelete = (runId: string) => {
    const updated = deleteRun(runId);
    setRuns(updated);
  };

  if (!mounted) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Benchmark Runs</h1>
        <span className="text-sm text-gray-500">{runs.length} run(s)</span>
      </div>

      <ImportButton onImport={handleImport} runs={runs} />

      {runs.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-lg border border-gray-200">
          <div className="text-4xl mb-3">📊</div>
          <p className="text-gray-500">No benchmark results yet.</p>
          <p className="text-sm text-gray-400 mt-1">
            Import JSON results files to get started.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto bg-white rounded-lg border border-gray-200">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Run ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Model
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Date
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Overall
                </th>
                {CATEGORY_KEYS.map((key) => (
                  <th
                    key={key}
                    className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase"
                  >
                    {CATEGORY_LABELS[key]}
                  </th>
                ))}
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {runs
                .sort(
                  (a, b) =>
                    new Date(b.timestamp).getTime() -
                    new Date(a.timestamp).getTime()
                )
                .map((run) => (
                  <tr key={run.run_id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <a
                        href={`/run/${run.run_id}`}
                        className="text-blue-600 hover:underline font-mono text-sm"
                      >
                        {run.run_id}
                      </a>
                    </td>
                    <td className="px-4 py-3 text-sm font-medium">
                      {run.model_name}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(run.timestamp).toLocaleDateString()}
                    </td>
                    <td
                      className={`px-4 py-3 text-sm font-semibold ${scoreColor(
                        run.overall_score
                      )}`}
                    >
                      {run.overall_score.toFixed(1)}
                    </td>
                    {CATEGORY_KEYS.map((key) => (
                      <td
                        key={key}
                        className={`px-4 py-3 text-sm ${scoreColor(
                          run.category_scores[key]
                        )}`}
                      >
                        {run.category_scores[key].toFixed(1)}
                      </td>
                    ))}
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => handleDelete(run.run_id)}
                        className="text-xs text-red-400 hover:text-red-600"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
