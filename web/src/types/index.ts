export interface PlayerStats {
  ortg: number;
  drtg: number;
  usage: number;
  efg: number;
  ts: number;
  threepPct: number;
  threepRate: number;
  ftr: number;
  astPct: number;
  tovPct: number;
  orbPct: number;
  drbPct: number;
  blkPct: number;
  stlPct: number;
  bpm: number;
  ppg: number;
  rpg: number;
  apg: number;
  spg: number;
  bpg: number;
  mpg: number;
  gp: number;
  fgPct: number;
  ftPct: number;
}

export interface SkillVector {
  scoring: number;
  shooting: number;
  playmaking: number;
  defense: number;
  rebounding: number;
  efficiency: number;
}

export type Archetype =
  | "Floor General"
  | "Scoring Guard"
  | "3-and-D Wing"
  | "Shot Creator"
  | "Stretch Big"
  | "Rim Protector"
  | "Rebounder/Energy"
  | "Two-Way Wing";

export interface Player {
  id: string;
  name: string;
  team: string;
  teamId: string;
  position: string;
  heightInches: number | null;
  heightDisplay: string;
  yearClass: string;
  jersey: string;
  archetype: Archetype;
  skills: SkillVector;
  stats: PlayerStats;
}

export interface TeamData {
  teamId: string;
  teamName: string;
  players: Player[];
}

export interface LineupDimensions {
  offense: number;
  defense: number;
  spacing: number;
  playmaking: number;
  rebounding: number;
  versatility: number;
  balance: number;
}

export interface LineupStrength {
  dimension: string;
  score: number;
}

export interface Lineup {
  rank: number;
  playerIds: string[];
  playerNames: string[];
  composite: number;
  dimensions: LineupDimensions;
  strengths: LineupStrength[];
  weaknesses: LineupStrength[];
}

export interface TeamLineups {
  teamId: string;
  teamName: string;
  totalCombinations: number;
  lineups: Lineup[];
}

export interface TeamSummary {
  teamId: string;
  teamName: string;
  playerCount: number;
  topLineupScore: number;
}

export interface Manifest {
  generatedAt: string;
  season: string;
  teams: TeamSummary[];
}
