import { Manifest, TeamData, TeamLineups } from "@/types";

const BASE_URL = process.env.NODE_ENV === "production" ? "" : "";

export async function getManifest(): Promise<Manifest> {
  const res = await fetch(`${BASE_URL}/data/manifest.json`);
  if (!res.ok) throw new Error("Failed to load manifest");
  return res.json();
}

export async function getTeamPlayers(teamId: string): Promise<TeamData> {
  const res = await fetch(`${BASE_URL}/data/teams/${teamId}/players.json`);
  if (!res.ok) throw new Error(`Failed to load players for ${teamId}`);
  return res.json();
}

export async function getTeamLineups(teamId: string): Promise<TeamLineups> {
  const res = await fetch(`${BASE_URL}/data/teams/${teamId}/lineups.json`);
  if (!res.ok) throw new Error(`Failed to load lineups for ${teamId}`);
  return res.json();
}
