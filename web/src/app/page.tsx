import { Manifest } from "@/types";
import fs from "fs";
import path from "path";
import Link from "next/link";

async function getManifest(): Promise<Manifest> {
  const filePath = path.join(process.cwd(), "public", "data", "manifest.json");
  const raw = fs.readFileSync(filePath, "utf-8");
  return JSON.parse(raw);
}

export default async function Home() {
  const manifest = await getManifest();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Hero */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          College Basketball Lineup Optimizer
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Analyze every possible 5-man lineup combination using advanced stats.
          Surface optimal units, identify hidden-gem combos, and build custom
          lineups with real-time scoring.
        </p>
        <div className="flex items-center justify-center gap-6 mt-5 text-sm text-gray-500">
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-blue-500" />
            {manifest.teams.length} Teams
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-green-500" />
            {manifest.season} Season
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-purple-500" />7 Scoring
            Dimensions
          </div>
        </div>
      </div>

      {/* How it works */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        {[
          {
            title: "Player Profiles",
            desc: "Each player is classified into an archetype with a 6-dimension skill radar based on ORtg, DRtg, usage, shooting, and more.",
            icon: "\u{1F464}",
          },
          {
            title: "Lineup Scoring",
            desc: "Every 5-man combination is scored across offense, defense, spacing, playmaking, rebounding, versatility, and balance.",
            icon: "\u{1F4CA}",
          },
          {
            title: "Interactive Builder",
            desc: "Build custom lineups and see real-time composite scores. Compare units side-by-side to optimize rotations.",
            icon: "⚙️",
          },
        ].map((item) => (
          <div
            key={item.title}
            className="bg-white rounded-lg border border-gray-200 p-5"
          >
            <div className="text-2xl mb-2">{item.icon}</div>
            <h3 className="font-semibold text-gray-900 mb-1">{item.title}</h3>
            <p className="text-sm text-gray-600">{item.desc}</p>
          </div>
        ))}
      </div>

      {/* Team grid */}
      <h2 className="text-xl font-bold text-gray-900 mb-4">Select a Team</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {manifest.teams.map((team) => (
          <Link
            key={team.teamId}
            href={`/team/${team.teamId}`}
            className="group bg-white rounded-lg border border-gray-200 p-4 hover:border-blue-300 hover:shadow-md transition-all"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                  {team.teamName}
                </h3>
                <p className="text-xs text-gray-500 mt-0.5">
                  {team.playerCount} rotation players
                </p>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-blue-600">
                  {team.topLineupScore}
                </div>
                <div className="text-xs text-gray-400">Top lineup</div>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
