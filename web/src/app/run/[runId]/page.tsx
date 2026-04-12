"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { BenchmarkRun, scoreColor, scoreBg } from "@/lib/types";
import { getRunById } from "@/lib/store";
import CategoryRadarChart from "@/components/CategoryRadarChart";

export default function RunDetailPage() {
  const params = useParams();
  const runId = params.runId as string;
  const [run, setRun] = useState<BenchmarkRun | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (runId) {
      setRun(getRunById(runId) ?? null);
    }
    setMounted(true);
  }, [runId]);

  if (!mounted) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  if (!run) {
    return (
      <div className="text-center py-16">
        <div className="text-4xl mb-3">🔍</div>
        <p className="text-gray-500">Run not found: {runId}</p>
        <a href="/" className="text-blue-600 hover:underline text-sm mt-2 inline-block">
          Back to runs
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <a href="/" className="text-gray-400 hover:text-gray-600 text-sm">
          ← Runs
        </a>
        <h1 className="text-2xl font-bold">
          {run.model_name}
          <span className="text-gray-400 font-normal ml-2 text-lg">
            {run.run_id}
          </span>
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Radar Chart */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Category Scores</h2>
          <CategoryRadarChart scores={run.category_scores} />
        </div>

        {/* Summary Cards */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">Score Summary</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="border rounded-lg p-4 text-center">
              <div className="text-xs text-gray-500 uppercase mb-1">
                Overall
              </div>
              <div
                className={`text-3xl font-bold ${scoreColor(
                  run.overall_score
                )}`}
              >
                {run.overall_score.toFixed(1)}
              </div>
            </div>
            {(
              Object.entries(run.category_scores) as [string, number][]
            ).map(([key, score]) => (
              <div key={key} className="border rounded-lg p-4 text-center">
                <div className="text-xs text-gray-500 uppercase mb-1">
                  {key.replace(/_/g, " ")}
                </div>
                <div className={`text-2xl font-bold ${scoreColor(score)}`}>
                  {score.toFixed(1)}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 text-sm text-gray-500">
            {run.per_task_results.length} tasks •{" "}
            {new Date(run.timestamp).toLocaleString()}
          </div>
        </div>
      </div>

      {/* Per-task table */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold">Task Results</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Task ID
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Category
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Score
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Method
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {run.per_task_results.map((task) => (
                <tr key={task.task_id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <a
                      href={`/run/${run.run_id}/task/${task.task_id}`}
                      className="text-blue-600 hover:underline font-mono text-sm"
                    >
                      {task.task_id}
                    </a>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">
                    {task.category}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${scoreBg(
                        task.score
                      )}`}
                    >
                      {task.score.toFixed(1)}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-500">
                    {task.grading_details?.grading_method ?? "-"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
