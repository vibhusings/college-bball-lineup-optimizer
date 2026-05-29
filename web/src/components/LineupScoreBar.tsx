"use client";

import { LineupDimensions } from "@/types";
import { DIMENSION_LABELS, DIMENSION_DESCRIPTIONS, getScoreBg } from "@/lib/constants";

interface Props {
  dimensions: LineupDimensions;
  composite: number;
}

export default function LineupScoreBar({ dimensions, composite }: Props) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-semibold text-gray-700">Composite Score</span>
        <span className="text-2xl font-bold text-gray-900">{composite}</span>
      </div>
      {Object.entries(dimensions).map(([key, score]) => (
        <div key={key} className="group relative">
          <div className="flex items-center justify-between text-xs mb-0.5">
            <span className="text-gray-600 font-medium">
              {DIMENSION_LABELS[key] || key}
            </span>
            <span className="font-semibold text-gray-800">{score}</span>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${getScoreBg(score)}`}
              style={{ width: `${score}%` }}
            />
          </div>
          <div className="hidden group-hover:block absolute z-10 -top-8 left-0 bg-gray-900 text-white text-xs px-2 py-1 rounded shadow-lg whitespace-nowrap">
            {DIMENSION_DESCRIPTIONS[key]}
          </div>
        </div>
      ))}
    </div>
  );
}
