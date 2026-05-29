import { Player, LineupDimensions } from "@/types";

const WEIGHTS = {
  offense: 0.3,
  defense: 0.25,
  spacing: 0.15,
  playmaking: 0.1,
  rebounding: 0.1,
  versatility: 0.05,
  balance: 0.05,
};

function clamp(val: number, min = 0, max = 100): number {
  return Math.max(min, Math.min(max, val));
}

function mean(arr: number[]): number {
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

function scoreOffense(players: Player[]): number {
  const ortgs = players.map((p) => p.stats.ortg);
  const usages = players.map((p) => p.stats.usage);
  const totalUsage = usages.reduce((a, b) => a + b, 0);
  if (totalUsage === 0) return 50;

  const weightedOrtg =
    ortgs.reduce((sum, o, i) => sum + o * usages[i], 0) / totalUsage;
  let score = ((weightedOrtg - 85) / (125 - 85)) * 100;
  score = clamp(score);

  if (Math.max(...usages) > 32) score *= 0.92;
  return Math.round(score * 10) / 10;
}

function scoreDefense(players: Player[]): number {
  const avgDrtg = mean(players.map((p) => p.stats.drtg));
  let score = ((115 - avgDrtg) / (115 - 85)) * 100;
  score = clamp(score);

  if (players.some((p) => p.stats.blkPct >= 6)) score = Math.min(100, score + 5);
  if (mean(players.map((p) => p.stats.stlPct)) >= 2) score = Math.min(100, score + 3);

  return Math.round(score * 10) / 10;
}

function scoreSpacing(players: Player[]): number {
  const shooters = players.filter(
    (p) => p.stats.threepPct >= 33 && p.stats.threepRate >= 20
  ).length;

  const spacingMap: Record<number, number> = { 0: 10, 1: 30, 2: 55, 3: 78, 4: 93, 5: 100 };
  let score = spacingMap[shooters] ?? 100;

  if (mean(players.map((p) => p.stats.threepPct)) >= 36) score = Math.min(100, score + 5);
  return score;
}

function scorePlaymaking(players: Player[]): number {
  const astPcts = players.map((p) => p.stats.astPct);
  const totalAst = astPcts.reduce((a, b) => a + b, 0);
  const avgTov = mean(players.map((p) => p.stats.tovPct));

  let astScore = ((totalAst - 40) / (120 - 40)) * 100;
  astScore = clamp(astScore);

  const tovPenalty = Math.max(0, (avgTov - 15) * 3);
  let score = astScore - tovPenalty;

  if (astPcts.some((a) => a >= 20)) score = Math.min(100, score + 8);
  else score -= 10;

  return Math.round(clamp(score) * 10) / 10;
}

function scoreRebounding(players: Player[]): number {
  const avgOrb = mean(players.map((p) => p.stats.orbPct));
  const avgDrb = mean(players.map((p) => p.stats.drbPct));

  const orbScore = ((avgOrb - 2) / (12 - 2)) * 100;
  const drbScore = ((avgDrb - 8) / (22 - 8)) * 100;

  let score = 0.4 * orbScore + 0.6 * drbScore;
  score = clamp(score);

  if (players.some((p) => p.stats.drbPct >= 18)) score = Math.min(100, score + 5);
  return Math.round(score * 10) / 10;
}

function scoreVersatility(players: Player[]): number {
  const posMap: Record<string, number> = {
    PG: 1, G: 1.5, CG: 1.5, SG: 2, GF: 2.5, SF: 3, F: 3.5, PF: 4, FC: 4.5, C: 5,
  };

  const posValues = players.map((p) => posMap[p.position.toUpperCase()] ?? 3);
  const uniquePos = new Set(posValues.map(Math.round)).size;
  const posScore = (uniquePos / 5) * 100;

  const heights = players
    .map((p) => p.heightInches)
    .filter((h): h is number => h !== null);
  let htScore = 50;
  if (heights.length >= 3) {
    const range = Math.max(...heights) - Math.min(...heights);
    if (range >= 6 && range <= 12) htScore = 80 + (range - 6) * 3;
    else if (range < 6) htScore = range * 13;
    else htScore = Math.max(50, 100 - (range - 12) * 5);
  }

  return Math.round(clamp(0.6 * posScore + 0.4 * htScore) * 10) / 10;
}

function scoreBalance(players: Player[]): number {
  const usages = players.map((p) => p.stats.usage).sort((a, b) => a - b);
  const n = usages.length;
  const total = usages.reduce((a, b) => a + b, 0);
  const gini =
    total === 0
      ? 0
      : usages.reduce((sum, u, i) => sum + (2 * (i + 1) - n - 1) * u, 0) / (n * total);

  const usageScore = (1 - gini) * 100;

  const archetypes = players.map((p) => p.archetype);
  const uniqueArch = new Set(archetypes).size;
  let archScore = (uniqueArch / 5) * 100;

  const counts = archetypes.reduce(
    (acc, a) => ({ ...acc, [a]: (acc[a] || 0) + 1 }),
    {} as Record<string, number>
  );
  if (Math.max(...Object.values(counts)) >= 3) archScore *= 0.6;

  return Math.round(clamp(0.5 * usageScore + 0.5 * archScore) * 10) / 10;
}

export function scoreLineup(players: Player[]): {
  dimensions: LineupDimensions;
  composite: number;
} {
  const dimensions: LineupDimensions = {
    offense: scoreOffense(players),
    defense: scoreDefense(players),
    spacing: scoreSpacing(players),
    playmaking: scorePlaymaking(players),
    rebounding: scoreRebounding(players),
    versatility: scoreVersatility(players),
    balance: scoreBalance(players),
  };

  const composite = Object.entries(WEIGHTS).reduce(
    (sum, [key, weight]) => sum + dimensions[key as keyof LineupDimensions] * weight,
    0
  );

  return { dimensions, composite: Math.round(composite * 10) / 10 };
}
