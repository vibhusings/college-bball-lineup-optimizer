import fs from "fs";
import path from "path";
import Link from "next/link";
import { TeamData, TeamLineups } from "@/types";
import TeamDashboard from "./TeamDashboard";

interface PageProps {
  params: Promise<{ teamId: string }>;
}

async function getTeamData(teamId: string): Promise<{
  players: TeamData;
  lineups: TeamLineups;
} | null> {
  const dataDir = path.join(process.cwd(), "public", "data", "teams", teamId);

  try {
    const playersRaw = fs.readFileSync(
      path.join(dataDir, "players.json"),
      "utf-8"
    );
    const lineupsRaw = fs.readFileSync(
      path.join(dataDir, "lineups.json"),
      "utf-8"
    );
    return {
      players: JSON.parse(playersRaw),
      lineups: JSON.parse(lineupsRaw),
    };
  } catch {
    return null;
  }
}

export default async function TeamPage({ params }: PageProps) {
  const { teamId } = await params;
  const data = await getTeamData(teamId);

  if (!data) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-4">Team not found</h1>
        <Link href="/" className="text-blue-600 hover:underline">
          Back to teams
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <Link
        href="/"
        className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
      >
        <svg
          className="w-4 h-4 mr-1"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        All teams
      </Link>

      <TeamDashboard
        teamName={data.players.teamName}
        players={data.players.players}
        lineups={data.lineups.lineups}
        totalCombinations={data.lineups.totalCombinations}
      />
    </div>
  );
}
