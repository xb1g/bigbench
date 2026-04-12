"use client";

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { CategoryScores, CATEGORY_LABELS, CATEGORY_KEYS } from "@/lib/types";

interface CategoryRadarChartProps {
  scores: CategoryScores;
  compareScores?: CategoryScores;
  compareLabel?: string;
}

export default function CategoryRadarChart({
  scores,
  compareScores,
  compareLabel,
}: CategoryRadarChartProps) {
  const data = CATEGORY_KEYS.map((key) => ({
    category: CATEGORY_LABELS[key],
    score: scores[key],
    ...(compareScores ? { compare: compareScores[key] } : {}),
  }));

  return (
    <ResponsiveContainer width="100%" height={350}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="75%">
        <PolarGrid stroke="#e5e7eb" />
        <PolarAngleAxis
          dataKey="category"
          tick={{ fontSize: 12, fill: "#374151" }}
        />
        <PolarRadiusAxis
          angle={90}
          domain={[0, 100]}
          tick={{ fontSize: 10, fill: "#9ca3af" }}
        />
        <Radar
          name="Score"
          dataKey="score"
          stroke="#3b82f6"
          fill="#3b82f6"
          fillOpacity={0.2}
          strokeWidth={2}
        />
        {compareScores && (
          <Radar
            name={compareLabel || "Compare"}
            dataKey="compare"
            stroke="#f97316"
            fill="#f97316"
            fillOpacity={0.15}
            strokeWidth={2}
          />
        )}
        <Legend />
      </RadarChart>
    </ResponsiveContainer>
  );
}
