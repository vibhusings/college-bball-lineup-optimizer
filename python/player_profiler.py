"""
Player Profiler — classifies players into archetypes and builds 6-dimension
skill vectors for radar chart visualization.

Works with ESPN-sourced player data (from fetch_data.py).
"""

import json
import os
import numpy as np

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")


def load_raw_players(year: int = 2025) -> list[dict]:
    """Load raw player JSON."""
    path = os.path.join(RAW_DIR, f"players_{year}.json")
    with open(path) as f:
        return json.load(f)


def get_stat(player: dict, key: str, default=0.0) -> float:
    """Get an advanced stat from a player dict."""
    val = player.get("advancedStats", {}).get(key, default)
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def classify_archetype(player: dict) -> str:
    """
    Classify a player into one of 8 archetypes based on their stat profile.
    """
    pos = player.get("position", "").upper().strip()
    ast = get_stat(player, "astPct")
    usage = get_stat(player, "usage")
    threep = get_stat(player, "threepPct")
    threep_rate = get_stat(player, "threepRate")
    blk = get_stat(player, "blkPct")
    stl = get_stat(player, "stlPct")
    orb = get_stat(player, "orbPct")
    drb = get_stat(player, "drbPct")
    ortg = get_stat(player, "ortg")
    drtg = get_stat(player, "drtg")

    is_guard = pos in ("PG", "G", "CG", "SG")
    is_wing = pos in ("SF", "F", "GF", "SG/SF")
    is_big = pos in ("PF", "C", "FC", "PF/C", "C/PF")

    # Floor General: high playmaker guard
    if is_guard and ast >= 22:
        return "Floor General"

    # Rim Protector: shot-blocking big
    if is_big and blk >= 5:
        return "Rim Protector"

    # Stretch Big: big who shoots 3s
    if is_big and threep >= 33 and threep_rate >= 18:
        return "Stretch Big"

    # 3-and-D Wing: good shooter + defender
    if (is_wing or is_guard) and threep >= 34 and (stl >= 1.5 or drtg <= 98):
        return "3-and-D Wing"

    # Scoring Guard: high-usage guard
    if is_guard and usage >= 22:
        return "Scoring Guard"

    # Shot Creator: high usage, creates own shot
    if usage >= 25 and ast >= 10:
        return "Shot Creator"

    # Rebounder/Energy: boards machine
    if orb >= 7 or drb >= 16:
        return "Rebounder/Energy"

    # Two-Way Wing: balanced offense and defense
    if (is_wing or is_guard) and ortg >= 103 and drtg <= 103:
        return "Two-Way Wing"

    # Default by position
    if is_guard:
        return "Scoring Guard"
    elif is_wing:
        return "Two-Way Wing"
    else:
        return "Rebounder/Energy"


def compute_percentile_stats(players: list[dict]) -> dict:
    """Compute min/max for normalization across all players."""
    stat_keys = [
        "ortg", "drtg", "usage", "efg", "ts", "threepPct", "threepRate",
        "astPct", "tovPct", "stlPct", "blkPct", "orbPct", "drbPct", "bpm",
    ]

    stats = {}
    for key in stat_keys:
        values = [get_stat(p, key) for p in players]
        values = [v for v in values if v != 0]  # filter zeros
        if values:
            stats[f"{key}_min"] = float(np.percentile(values, 5))
            stats[f"{key}_max"] = float(np.percentile(values, 95))
        else:
            stats[f"{key}_min"] = 0
            stats[f"{key}_max"] = 100

    return stats


def percentile(val: float, min_val: float, max_val: float) -> float:
    """Convert a value to 0-100 scale."""
    if max_val == min_val:
        return 50.0
    return max(0, min(100, ((val - min_val) / (max_val - min_val)) * 100))


def compute_skill_vector(player: dict, norms: dict) -> dict:
    """
    Compute 6-dimension skill vector (0-100 scale) for radar charts.
    """
    ortg = get_stat(player, "ortg")
    drtg = get_stat(player, "drtg")
    usage = get_stat(player, "usage")
    efg = get_stat(player, "efg")
    ts = get_stat(player, "ts")
    threep = get_stat(player, "threepPct")
    threep_rate = get_stat(player, "threepRate")
    ast = get_stat(player, "astPct")
    tov = get_stat(player, "tovPct")
    stl = get_stat(player, "stlPct")
    blk = get_stat(player, "blkPct")
    orb = get_stat(player, "orbPct")
    drb = get_stat(player, "drbPct")
    bpm = get_stat(player, "bpm")

    # Scoring: ORtg (40%) + usage (30%) + eFG (30%)
    scoring = (
        0.4 * percentile(ortg, norms["ortg_min"], norms["ortg_max"])
        + 0.3 * percentile(usage, norms["usage_min"], norms["usage_max"])
        + 0.3 * percentile(efg, norms["efg_min"], norms["efg_max"])
    )

    # Shooting: 3P% (50%) + 3PA rate (30%) + TS% (20%)
    shooting = (
        0.5 * percentile(threep, norms["threepPct_min"], norms["threepPct_max"])
        + 0.3 * percentile(threep_rate, norms["threepRate_min"], norms["threepRate_max"])
        + 0.2 * percentile(ts, norms["ts_min"], norms["ts_max"])
    )

    # Playmaking: AST% (65%) + inverse TOV% (35%)
    playmaking = (
        0.65 * percentile(ast, norms["astPct_min"], norms["astPct_max"])
        + 0.35 * percentile(-tov, -norms["tovPct_max"], -norms["tovPct_min"])
    )

    # Defense: inverse DRtg (40%) + STL% (30%) + BLK% (30%)
    defense = (
        0.4 * percentile(-drtg, -norms["drtg_max"], -norms["drtg_min"])
        + 0.3 * percentile(stl, norms["stlPct_min"], norms["stlPct_max"])
        + 0.3 * percentile(blk, norms["blkPct_min"], norms["blkPct_max"])
    )

    # Rebounding: ORB% (40%) + DRB% (60%)
    rebounding = (
        0.4 * percentile(orb, norms["orbPct_min"], norms["orbPct_max"])
        + 0.6 * percentile(drb, norms["drbPct_min"], norms["drbPct_max"])
    )

    # Efficiency: BPM (50%) + TS% (30%) + inverse TOV% (20%)
    efficiency = (
        0.5 * percentile(bpm, norms["bpm_min"], norms["bpm_max"])
        + 0.3 * percentile(ts, norms["ts_min"], norms["ts_max"])
        + 0.2 * percentile(-tov, -norms["tovPct_max"], -norms["tovPct_min"])
    )

    return {
        "scoring": round(scoring, 1),
        "shooting": round(shooting, 1),
        "playmaking": round(playmaking, 1),
        "defense": round(defense, 1),
        "rebounding": round(rebounding, 1),
        "efficiency": round(efficiency, 1),
    }


def create_team_id(team: str) -> str:
    """Create a URL-safe team ID."""
    clean = team.lower().replace(" ", "_").replace(".", "").replace("'", "")
    return "".join(c for c in clean if c.isalnum() or c == "_")


def create_player_id(name: str, team: str) -> str:
    """Create a URL-safe player ID."""
    clean = f"{name}_{team}".lower().replace(" ", "_").replace(".", "").replace("'", "")
    return "".join(c for c in clean if c.isalnum() or c == "_")


def format_height(inches) -> str:
    """Convert height in inches to display format."""
    if inches is None:
        return ""
    try:
        inches = int(float(inches))
        feet = inches // 12
        remaining = inches % 12
        return f"{feet}'{remaining}\""
    except (ValueError, TypeError):
        return ""


def profile_all_teams(year: int = 2025) -> list[dict]:
    """Profile all teams from raw data. Returns list of team summaries."""
    print("Profiling players...")

    players = load_raw_players(year)
    print(f"  Loaded {len(players)} players")

    # Compute global normalization stats
    norms = compute_percentile_stats(players)

    # Group by team
    teams_map: dict[str, list[dict]] = {}
    for p in players:
        team = p.get("team", "Unknown")
        if team not in teams_map:
            teams_map[team] = []
        teams_map[team].append(p)

    team_summaries = []

    for team_name in sorted(teams_map.keys()):
        team_players = teams_map[team_name]
        team_id = create_team_id(team_name)

        # Sort by minutes, take top 10
        team_players.sort(key=lambda x: get_stat(x, "mpg"), reverse=True)
        team_players = team_players[:10]

        profiled = []
        for p in team_players:
            archetype = classify_archetype(p)
            skills = compute_skill_vector(p, norms)

            profiled.append({
                "id": create_player_id(p["name"], team_name),
                "name": p["name"],
                "team": team_name,
                "teamId": team_id,
                "position": p.get("position", ""),
                "heightInches": p.get("heightInches"),
                "heightDisplay": format_height(p.get("heightInches")),
                "yearClass": p.get("year", ""),
                "jersey": p.get("jersey", ""),
                "archetype": archetype,
                "skills": skills,
                "stats": p.get("advancedStats", {}),
            })

        # Save per-team file
        team_dir = os.path.join(PROCESSED_DIR, "teams", team_id)
        os.makedirs(team_dir, exist_ok=True)
        team_data = {
            "teamId": team_id,
            "teamName": team_name,
            "players": profiled,
        }
        with open(os.path.join(team_dir, "players.json"), "w") as f:
            json.dump(team_data, f, indent=2)

        team_summaries.append({
            "teamId": team_id,
            "teamName": team_name,
            "playerCount": len(profiled),
        })
        print(f"  {team_name}: {len(profiled)} rotation players profiled")

    return team_summaries


if __name__ == "__main__":
    profile_all_teams()
