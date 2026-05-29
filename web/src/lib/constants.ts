export const ARCHETYPE_COLORS: Record<string, string> = {
  "Floor General": "bg-blue-100 text-blue-800",
  "Scoring Guard": "bg-red-100 text-red-800",
  "3-and-D Wing": "bg-green-100 text-green-800",
  "Shot Creator": "bg-purple-100 text-purple-800",
  "Stretch Big": "bg-yellow-100 text-yellow-800",
  "Rim Protector": "bg-orange-100 text-orange-800",
  "Rebounder/Energy": "bg-amber-100 text-amber-800",
  "Two-Way Wing": "bg-teal-100 text-teal-800",
};

export const DIMENSION_LABELS: Record<string, string> = {
  offense: "Offense",
  defense: "Defense",
  spacing: "Spacing",
  playmaking: "Playmaking",
  rebounding: "Rebounding",
  versatility: "Versatility",
  balance: "Balance",
};

export const DIMENSION_DESCRIPTIONS: Record<string, string> = {
  offense: "Usage-weighted offensive rating of the lineup",
  defense: "Average defensive rating with rim protection bonus",
  spacing: "Floor spacing based on 3-point shooting capability",
  playmaking: "Ball handling, assist generation, and turnover control",
  rebounding: "Combined offensive and defensive rebounding coverage",
  versatility: "Position coverage and height distribution",
  balance: "Usage distribution and archetype diversity",
};

export function formatHeight(inches: number | null): string {
  if (inches === null) return "";
  const feet = Math.floor(inches / 12);
  const remaining = inches % 12;
  return `${feet}'${remaining}"`;
}

export function getScoreColor(score: number): string {
  if (score >= 75) return "text-green-600";
  if (score >= 60) return "text-blue-600";
  if (score >= 45) return "text-yellow-600";
  return "text-red-600";
}

export function getScoreBg(score: number): string {
  if (score >= 75) return "bg-green-500";
  if (score >= 60) return "bg-blue-500";
  if (score >= 45) return "bg-yellow-500";
  return "bg-red-500";
}
