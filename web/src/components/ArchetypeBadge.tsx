import { ARCHETYPE_COLORS } from "@/lib/constants";

interface Props {
  archetype: string;
}

export default function ArchetypeBadge({ archetype }: Props) {
  const color = ARCHETYPE_COLORS[archetype] || "bg-gray-100 text-gray-800";
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${color}`}>
      {archetype}
    </span>
  );
}
