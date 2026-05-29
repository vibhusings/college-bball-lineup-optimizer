"use client";

import { useState } from "react";
import { Player, Lineup } from "@/types";
import PlayerCard from "@/components/PlayerCard";
import LineupTable from "@/components/LineupTable";
import LineupBuilder from "@/components/LineupBuilder";

interface Props {
  teamName: string;
  players: Player[];
  lineups: Lineup[];
  totalCombinations: number;
}

type Tab = "roster" | "lineups" | "builder";

export default function TeamDashboard({
  teamName,
  players,
  lineups,
  totalCombinations,
}: Props) {
  const [tab, setTab] = useState<Tab>("lineups");

  const tabs: { key: Tab; label: string; count?: number }[] = [
    { key: "roster", label: "Roster", count: players.length },
    { key: "lineups", label: "Top Lineups", count: lineups.length },
    { key: "builder", label: "Lineup Builder" },
  ];

  return (
    <div>
      {/* Team header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{teamName}</h1>
        <p className="text-sm text-gray-500 mt-1">
          {players.length} rotation players &middot;{" "}
          {totalCombinations.toLocaleString()} possible 5-man combinations
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex gap-6">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`pb-3 text-sm font-medium border-b-2 transition-colors ${
                tab === t.key
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              {t.label}
              {t.count !== undefined && (
                <span className="ml-1.5 text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded-full">
                  {t.count}
                </span>
              )}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab content */}
      {tab === "roster" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {players.map((player) => (
            <PlayerCard key={player.id} player={player} />
          ))}
        </div>
      )}

      {tab === "lineups" && (
        <div>
          <div className="mb-4 text-sm text-gray-600">
            Top {lineups.length} lineup combinations ranked by composite score
            (out of {totalCombinations.toLocaleString()} possible).
          </div>
          <LineupTable lineups={lineups} players={players} />
        </div>
      )}

      {tab === "builder" && (
        <div>
          <div className="mb-4 text-sm text-gray-600">
            Select 5 players to build a custom lineup and see its score in
            real-time.
          </div>
          <LineupBuilder players={players} />
        </div>
      )}
    </div>
  );
}
