"use client";

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { SkillVector } from "@/types";

interface Props {
  skills: SkillVector;
  compareSkills?: SkillVector;
  size?: number;
}

const LABELS: Record<keyof SkillVector, string> = {
  scoring: "Scoring",
  shooting: "Shooting",
  playmaking: "Playmaking",
  defense: "Defense",
  rebounding: "Rebounding",
  efficiency: "Efficiency",
};

export default function PlayerRadar({ skills, compareSkills, size = 250 }: Props) {
  const data = Object.entries(LABELS).map(([key, label]) => ({
    subject: label,
    value: skills[key as keyof SkillVector],
    ...(compareSkills ? { compare: compareSkills[key as keyof SkillVector] } : {}),
  }));

  return (
    <ResponsiveContainer width="100%" height={size}>
      <RadarChart data={data} cx="50%" cy="50%" outerRadius="70%">
        <PolarGrid stroke="#e5e7eb" />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: "#6b7280", fontSize: 11 }}
        />
        <PolarRadiusAxis
          angle={30}
          domain={[0, 100]}
          tick={{ fontSize: 9 }}
          tickCount={4}
        />
        <Radar
          name="Player"
          dataKey="value"
          stroke="#3b82f6"
          fill="#3b82f6"
          fillOpacity={0.25}
          strokeWidth={2}
        />
        {compareSkills && (
          <Radar
            name="Compare"
            dataKey="compare"
            stroke="#ef4444"
            fill="#ef4444"
            fillOpacity={0.15}
            strokeWidth={2}
          />
        )}
        {compareSkills && <Legend />}
      </RadarChart>
    </ResponsiveContainer>
  );
}
