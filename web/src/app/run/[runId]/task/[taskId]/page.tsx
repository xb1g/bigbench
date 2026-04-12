"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { BenchmarkRun, TaskResult, scoreColor } from "@/lib/types";
import { getRunById } from "@/lib/store";

function SyntaxHighlight({ content }: { content: string }) {
  // Basic markdown / code detection
  const lines = content.split("\n");
  return (
    <pre className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto text-sm leading-relaxed font-mono whitespace-pre-wrap break-words">
      {lines.map((line, i) => {
        // Highlight markdown headings
        if (line.startsWith("# ")) {
          return (
            <div key={i} className="text-blue-300 font-bold">
              {line}
            </div>
          );
        }
        if (line.startsWith("## ")) {
          return (
            <div key={i} className="text-blue-400 font-semibold">
              {line}
            </div>
          );
        }
        if (line.startsWith("### ")) {
          return (
            <div key={i} className="text-blue-400">
              {line}
            </div>
          );
        }
        // Highlight code fences
        if (line.startsWith("```")) {
          return (
            <div key={i} className="text-green-400">
              {line}
            </div>
          );
        }
        // Highlight bullet points
        if (line.startsWith("- ") || line.startsWith("* ")) {
          return (
            <div key={i} className="text-yellow-200">
              {line}
            </div>
          );
        }
        // Highlight numbered lists
        if (/^\d+\.\s/.test(line)) {
          return (
            <div key={i} className="text-cyan-200">
              {line}
            </div>
          );
        }
        // Bold text
        const boldified = line.replace(
          /\*\*(.+?)\*\*/g,
          '<strong class="text-white font-bold">$1</strong>'
        );
        if (boldified !== line) {
          return (
            <div
              key={i}
              dangerouslySetInnerHTML={{ __html: boldified }}
            />
          );
        }
        return <div key={i}>{line}</div>;
      })}
    </pre>
  );
}

export default function TaskDetailPage() {
  const params = useParams();
  const runId = params.runId as string;
  const taskId = params.taskId as string;
  const [run, setRun] = useState<BenchmarkRun | null>(null);
  const [task, setTask] = useState<TaskResult | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (runId && taskId) {
      const r = getRunById(runId);
      if (r) {
        setRun(r);
        const t = r.per_task_results.find((t) => t.task_id === taskId);
        setTask(t ?? null);
      }
    }
    setMounted(true);
  }, [runId, taskId]);

  if (!mounted) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  if (!run || !task) {
    return (
      <div className="text-center py-16">
        <div className="text-4xl mb-3">🔍</div>
        <p className="text-gray-500">
          Task not found: {runId}/{taskId}
        </p>
        <a href="/" className="text-blue-600 hover:underline text-sm mt-2 inline-block">
          Back to runs
        </a>
      </div>
    );
  }

  const gd = task.grading_details;

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <a
          href={`/run/${runId}`}
          className="text-gray-400 hover:text-gray-600 text-sm"
        >
          ← {run.model_name} ({runId})
        </a>
      </div>

      {/* Task header */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-xl font-bold font-mono">{task.task_id}</h1>
          <span
            className={`text-2xl font-bold ${scoreColor(task.score)}`}
          >
            {task.score.toFixed(1)}
          </span>
        </div>
        <div className="flex gap-3 text-sm text-gray-500">
          <span className="bg-gray-100 px-2 py-0.5 rounded">
            {task.category}
          </span>
          {task.dry_run && (
            <span className="bg-orange-100 text-orange-700 px-2 py-0.5 rounded">
              Dry Run
            </span>
          )}
        </div>
      </div>

      {/* Grading breakdown */}
      {gd && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h2 className="text-lg font-semibold mb-4">
            Grading Breakdown
            <span className="text-sm font-normal text-gray-400 ml-2">
              {gd.grading_method}
            </span>
          </h2>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Criterion
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Score
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Weight
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                    Rationale
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {gd.criterion_scores.map((c, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="px-4 py-2 text-sm font-medium">
                      {c.name}
                    </td>
                    <td
                      className={`px-4 py-2 text-sm font-semibold ${scoreColor(
                        (c.score / c.max_score) * 100
                      )}`}
                    >
                      {c.score.toFixed(1)} / {c.max_score.toFixed(1)}
                    </td>
                    <td className="px-4 py-2 text-sm text-gray-500">
                      {(c.weight * 100).toFixed(0)}%
                    </td>
                    <td className="px-4 py-2 text-sm text-gray-600 max-w-md">
                      {c.rationale}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {gd.rationale && (
            <div className="mt-4 p-3 bg-gray-50 rounded text-sm text-gray-600">
              <span className="font-medium text-gray-700">Overall rationale: </span>
              {gd.rationale}
            </div>
          )}
        </div>
      )}

      {/* Raw output */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h2 className="text-lg font-semibold mb-4">Raw LLM Output</h2>
        <SyntaxHighlight content={task.raw_output} />
      </div>
    </div>
  );
}
