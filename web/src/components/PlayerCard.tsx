"use client";

import { useState } from "react";
import { Player } from "@/types";
import { formatHeight, getScoreColor } from "@/lib/constants";
import ArchetypeBadge from "./ArchetypeBadge";
import PlayerRadar from "./PlayerRadar";

interface Props {
  player: Player;
  selected?: boolean;
  onToggle?: (player: Player) => void;
  compact?: boolean;
}

export default function PlayerCard({ player, selected, onToggle, compact }: Props) {
  const [expanded, setExpanded] = useState(false);
  const { stats, skills } = player;

  return (
    <div
      className={`rounded-lg border transition-all ${
        selected
          ? "border-blue-500 bg-blue-50 shadow-md"
          : "border-gray-200 bg-white hover:border-gray-300 hover:shadow-sm"
      } ${onToggle ? "cursor-pointer" : ""}`}
      onClick={() => onToggle?.(player)}
    >
      <div className="p-3">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              {onToggle && (
                <div
                  className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 ${
                    selected ? "bg-blue-500 border-blue-500" : "border-gray-300"
                  }`}
                >
                  {selected && (
                    <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </div>
              )}
              <h3 className="font-semibold text-gray-900 truncate">{player.name}</h3>
            </div>
            <div className="flex items-center gap-2 mt-1 text-sm text-gray-500">
              <span>{player.position}</span>
              {player.heightInches && <span>{formatHeight(player.heightInches)}</span>}
              {player.yearClass && <span>{player.yearClass}</span>}
            </div>
            <div className="mt-1.5">
              <ArchetypeBadge archetype={player.archetype} />
            </div>
          </div>
          <div className="text-right flex-shrink-0 ml-2">
            <div className="text-lg font-bold text-gray-900">{stats.ppg}</div>
            <div className="text-xs text-gray-500">PPG</div>
          </div>
        </div>

        {!compact && (
          <div className="grid grid-cols-4 gap-2 mt-3 text-center text-xs">
            <div>
              <div className="font-semibold text-gray-900">{stats.rpg}</div>
              <div className="text-gray-500">RPG</div>
            </div>
            <div>
              <div className="font-semibold text-gray-900">{stats.apg}</div>
              <div className="text-gray-500">APG</div>
            </div>
            <div>
              <div className={`font-semibold ${getScoreColor(stats.efg)}`}>{stats.efg}%</div>
              <div className="text-gray-500">eFG%</div>
            </div>
            <div>
              <div className="font-semibold text-gray-900">{stats.mpg}</div>
              <div className="text-gray-500">MPG</div>
            </div>
          </div>
        )}

        {!compact && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setExpanded(!expanded);
            }}
            className="w-full mt-2 text-xs text-blue-600 hover:text-blue-800"
          >
            {expanded ? "Hide details" : "Show details"}
          </button>
        )}
      </div>

      {expanded && !compact && (
        <div className="border-t border-gray-100 p-3">
          <PlayerRadar skills={skills} size={200} />
          <div className="grid grid-cols-3 gap-2 mt-2 text-xs">
            <div className="text-center">
              <span className="text-gray-500">ORtg: </span>
              <span className="font-semibold">{stats.ortg}</span>
            </div>
            <div className="text-center">
              <span className="text-gray-500">DRtg: </span>
              <span className="font-semibold">{stats.drtg}</span>
            </div>
            <div className="text-center">
              <span className="text-gray-500">USG%: </span>
              <span className="font-semibold">{stats.usage}</span>
            </div>
            <div className="text-center">
              <span className="text-gray-500">3P%: </span>
              <span className="font-semibold">{stats.threepPct}</span>
            </div>
            <div className="text-center">
              <span className="text-gray-500">AST%: </span>
              <span className="font-semibold">{stats.astPct}</span>
            </div>
            <div className="text-center">
              <span className="text-gray-500">BPM: </span>
              <span className="font-semibold">{stats.bpm}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
