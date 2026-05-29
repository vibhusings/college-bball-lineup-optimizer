"use client";

import { useState, useMemo } from "react";
import { Player } from "@/types";
import { scoreLineup } from "@/lib/scoring";
import PlayerCard from "./PlayerCard";
import LineupScoreBar from "./LineupScoreBar";
import PlayerRadar from "./PlayerRadar";
import { SkillVector } from "@/types";

interface Props {
  players: Player[];
}

function averageSkills(players: Player[]): SkillVector {
  if (players.length === 0) {
    return { scoring: 0, shooting: 0, playmaking: 0, defense: 0, rebounding: 0, efficiency: 0 };
  }
  const keys: (keyof SkillVector)[] = [
    "scoring", "shooting", "playmaking", "defense", "rebounding", "efficiency",
  ];
  const result: Record<string, number> = {};
  for (const key of keys) {
    result[key] = players.reduce((sum, p) => sum + p.skills[key], 0) / players.length;
  }
  return result as unknown as SkillVector;
}

export default function LineupBuilder({ players }: Props) {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  const selectedPlayers = useMemo(
    () => players.filter((p) => selectedIds.has(p.id)),
    [players, selectedIds]
  );

  const lineupScore = useMemo(() => {
    if (selectedPlayers.length !== 5) return null;
    return scoreLineup(selectedPlayers);
  }, [selectedPlayers]);

  const avgSkills = useMemo(() => averageSkills(selectedPlayers), [selectedPlayers]);

  const togglePlayer = (player: Player) => {
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(player.id)) {
        next.delete(player.id);
      } else if (next.size < 5) {
        next.add(player.id);
      }
      return next;
    });
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Player selection */}
      <div className="lg:col-span-2">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-gray-700">
            Select 5 players ({selectedIds.size}/5)
          </h3>
          {selectedIds.size > 0 && (
            <button
              onClick={() => setSelectedIds(new Set())}
              className="text-xs text-red-600 hover:text-red-800"
            >
              Clear all
            </button>
          )}
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {players.map((player) => (
            <PlayerCard
              key={player.id}
              player={player}
              selected={selectedIds.has(player.id)}
              onToggle={togglePlayer}
              compact
            />
          ))}
        </div>
      </div>

      {/* Score panel */}
      <div className="lg:col-span-1">
        <div className="sticky top-4 space-y-4">
          <div className="bg-white rounded-lg border border-gray-200 p-4">
            <h3 className="font-semibold text-gray-900 mb-3">Lineup Score</h3>

            {selectedPlayers.length === 0 && (
              <p className="text-sm text-gray-500">Select players to see lineup score</p>
            )}

            {selectedPlayers.length > 0 && selectedPlayers.length < 5 && (
              <div>
                <p className="text-sm text-gray-500 mb-3">
                  Select {5 - selectedPlayers.length} more player
                  {5 - selectedPlayers.length > 1 ? "s" : ""}
                </p>
                <div className="space-y-1">
                  {selectedPlayers.map((p) => (
                    <div
                      key={p.id}
                      className="flex items-center justify-between text-sm bg-blue-50 rounded px-2 py-1"
                    >
                      <span className="font-medium">{p.name}</span>
                      <span className="text-xs text-gray-500">{p.position}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {lineupScore && (
              <LineupScoreBar
                dimensions={lineupScore.dimensions}
                composite={lineupScore.composite}
              />
            )}
          </div>

          {selectedPlayers.length >= 3 && (
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900 mb-2 text-sm">Lineup Profile</h3>
              <PlayerRadar skills={avgSkills} size={220} />
            </div>
          )}

          {lineupScore && (
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900 mb-2 text-sm">Selected Players</h3>
              <div className="space-y-1.5">
                {selectedPlayers.map((p) => (
                  <div
                    key={p.id}
                    className="flex items-center justify-between text-sm"
                  >
                    <div>
                      <span className="font-medium text-gray-900">{p.name}</span>
                      <span className="text-xs text-gray-400 ml-1">{p.position}</span>
                    </div>
                    <div className="text-xs text-gray-500">
                      {p.stats.ppg}/{p.stats.rpg}/{p.stats.apg}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
