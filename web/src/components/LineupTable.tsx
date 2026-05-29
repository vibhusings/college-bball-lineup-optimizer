"use client";

import { useState } from "react";
import { Lineup, Player } from "@/types";
import { getScoreColor, DIMENSION_LABELS, getScoreBg } from "@/lib/constants";
import ArchetypeBadge from "./ArchetypeBadge";

interface Props {
  lineups: Lineup[];
  players: Player[];
}

export default function LineupTable({ lineups, players }: Props) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  const playerMap = new Map(players.map((p) => [p.id, p]));

  return (
    <div className="space-y-2">
      {lineups.map((lineup, idx) => {
        const isExpanded = expandedIdx === idx;
        const lineupPlayers = lineup.playerIds
          .map((id) => playerMap.get(id))
          .filter((p): p is Player => !!p);

        return (
          <div
            key={idx}
            className={`rounded-lg border transition-all ${
              isExpanded ? "border-blue-300 shadow-md" : "border-gray-200 hover:border-gray-300"
            } bg-white`}
          >
            <button
              onClick={() => setExpandedIdx(isExpanded ? null : idx)}
              className="w-full p-3 text-left"
            >
              <div className="flex items-center gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                  <span className="text-sm font-bold text-gray-600">#{lineup.rank}</span>
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex flex-wrap gap-1">
                    {lineup.playerNames.map((name, i) => (
                      <span key={i} className="text-sm text-gray-700">
                        {name}
                        {i < lineup.playerNames.length - 1 && (
                          <span className="text-gray-400 mx-0.5">/</span>
                        )}
                      </span>
                    ))}
                  </div>
                  <div className="flex gap-3 mt-1">
                    {lineup.strengths.slice(0, 2).map((s) => (
                      <span key={s.dimension} className="text-xs text-green-600">
                        {DIMENSION_LABELS[s.dimension]}: {s.score}
                      </span>
                    ))}
                    {lineup.weaknesses.slice(0, 1).map((w) => (
                      <span key={w.dimension} className="text-xs text-red-500">
                        {DIMENSION_LABELS[w.dimension]}: {w.score}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex-shrink-0 text-right">
                  <div className={`text-xl font-bold ${getScoreColor(lineup.composite)}`}>
                    {lineup.composite}
                  </div>
                  <div className="text-xs text-gray-500">Score</div>
                </div>

                <svg
                  className={`w-5 h-5 text-gray-400 transition-transform flex-shrink-0 ${
                    isExpanded ? "rotate-180" : ""
                  }`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </button>

            {isExpanded && (
              <div className="border-t border-gray-100 p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Dimension breakdown */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">Dimension Scores</h4>
                    <div className="space-y-1.5">
                      {Object.entries(lineup.dimensions).map(([key, score]) => (
                        <div key={key} className="flex items-center gap-2">
                          <span className="text-xs text-gray-500 w-20">
                            {DIMENSION_LABELS[key]}
                          </span>
                          <div className="flex-1 bg-gray-100 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${getScoreBg(score)}`}
                              style={{ width: `${score}%` }}
                            />
                          </div>
                          <span className="text-xs font-semibold w-8 text-right">{score}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Player details */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">Players</h4>
                    <div className="space-y-1.5">
                      {lineupPlayers.map((p) => (
                        <div
                          key={p.id}
                          className="flex items-center justify-between text-sm"
                        >
                          <div className="flex items-center gap-2">
                            <span className="font-medium text-gray-900">{p.name}</span>
                            <span className="text-xs text-gray-400">{p.position}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <ArchetypeBadge archetype={p.archetype} />
                            <span className="text-xs text-gray-500">{p.stats.ppg} PPG</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
