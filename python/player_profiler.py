"""
Player Profiler — classifies players into archetypes and builds 6-dimension
skill vectors for radar chart visualization.
"""

import json
import os
import numpy as np
import pandas as pd

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")
RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")

# Column mapping — BartTorvik CSV column names to our internal names.
# Adjusted at runtime based on actual column names found.
COLUMN_MAP = {
    "player": ["Player", "player", "Name", "name"],
    "team": ["Team", "team", "School", "school"],
    "pos": ["Pos", "pos", "Position", "position"],
    "height": ["Ht", "ht", "Height", "height", "Hgt"],
    "year_class": ["Yr", "yr", "Year", "year", "Class", "class", "Exp"],
    "gp": ["G", "g", "GP", "gp", "Games"],
    "mpg": ["Min", "min", "MPG", "mpg", "Minutes"],
    "ortg": ["ORtg", "ortg", "ORate", "oRtg", "adjoe"],
    "drtg": ["DRtg", "drtg", "DRate", "dRtg", "adjde"],
    "usage": ["usg", "USG", "Usg", "Usage", "usage", "Poss%"],
    "efg": ["eFG", "efg", "eFG%"],
    "ts": ["TS", "ts", "TS%"],
    "threep_pct": ["3P%", "3p%", "3FG%", "3P_pct"],
    "threep_rate": ["3PAr", "3par", "3PA%", "3FGA%", "3P Rate"],
    "ftr": ["FTR", "ftr", "FT Rate", "FTr"],
    "ast_pct": ["AST%", "ast%", "Ast%", "AST"],
    "tov_pct": ["TOV%", "tov%", "TO%", "Tov%"],
    "orb_pct": ["ORB%", "orb%", "OR%", "OReb%"],
    "drb_pct": ["DRB%", "drb%", "DR%", "DReb%"],
    "blk_pct": ["BLK%", "blk%", "Blk%"],
    "stl_pct": ["STL%", "stl%", "Stl%"],
    "bpm": ["BPM", "bpm", "OBPM", "Adj BPM"],
    "ppg": ["PPG", "ppg", "Pts", "pts", "Points"],
}


def resolve_columns(df: pd.DataFrame) -> dict[str, str | None]:
    """Map our internal column names to actual DataFrame columns."""
    mapping = {}
    available = set(df.columns)

    for internal_name, candidates in COLUMN_MAP.items():
        found = None
        for candidate in candidates:
            if candidate in available:
                found = candidate
                break
        mapping[internal_name] = found

    return mapping


def load_raw_players(year: int = 2025) -> pd.DataFrame:
    """Load raw player JSON into a DataFrame."""
    path = os.path.join(RAW_DIR, f"players_{year}.json")
    with open(path) as f:
        records = json.load(f)
    return pd.DataFrame(records)


def safe_get(row, col_name: str | None, default=0.0):
    """Safely get a value from a row, returning default if column is None or value is NaN."""
    if col_name is None:
        return default
    val = row.get(col_name, default)
    if pd.isna(val):
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def classify_archetype(player: dict, col_map: dict) -> str:
    """
    Classify a player into an archetype based on their stat profile.

    Archetypes:
    - Floor General: high AST%, guard
    - Scoring Guard: high usage, guard
    - 3-and-D Wing: good 3P% + defensive stats, wing
    - Shot Creator: high usage, moderate AST%
    - Stretch Big: big + shoots 3s
    - Rim Protector: high BLK%, big
    - Rebounder/Energy: high rebound rates
    - Two-Way Wing: balanced offense + defense
    """
    pos = str(player.get(col_map["pos"], "")).strip().upper()
    ast = safe_get(player, col_map["ast_pct"])
    usage = safe_get(player, col_map["usage"])
    threep = safe_get(player, col_map["threep_pct"])
    threep_rate = safe_get(player, col_map["threep_rate"])
    blk = safe_get(player, col_map["blk_pct"])
    stl = safe_get(player, col_map["stl_pct"])
    orb = safe_get(player, col_map["orb_pct"])
    drb = safe_get(player, col_map["drb_pct"])
    ortg = safe_get(player, col_map["ortg"])
    drtg = safe_get(player, col_map["drtg"])

    is_guard = pos in ("PG", "G", "CG", "1", "2", "GUARD", "COMBO GUARD")
    is_wing = pos in ("SG", "SF", "F", "GF", "WING", "3", "SG/SF")
    is_big = pos in ("PF", "C", "FC", "4", "5", "CENTER", "FORWARD")

    # Floor General: high playmaker guard
    if is_guard and ast >= 22:
        return "Floor General"

    # Rim Protector: shot-blocking big
    if is_big and blk >= 6:
        return "Rim Protector"

    # Stretch Big: big who shoots 3s
    if is_big and threep >= 33 and threep_rate >= 20:
        return "Stretch Big"

    # 3-and-D Wing: good shooter + defender
    if (is_wing or is_guard) and threep >= 34 and (stl >= 1.8 or drtg <= 98):
        return "3-and-D Wing"

    # Scoring Guard: high-usage guard
    if is_guard and usage >= 24:
        return "Scoring Guard"

    # Shot Creator: high usage, creates own shot
    if usage >= 26 and ast >= 12:
        return "Shot Creator"

    # Rebounder/Energy: boards machine
    if (orb >= 8 or drb >= 18):
        return "Rebounder/Energy"

    # Two-Way Wing: balanced offense and defense
    if (is_wing or is_guard) and ortg >= 105 and drtg <= 102:
        return "Two-Way Wing"

    # Default classification by position
    if is_guard:
        return "Scoring Guard"
    elif is_wing:
        return "Two-Way Wing"
    else:
        return "Rebounder/Energy"


def compute_skill_vector(player: dict, col_map: dict, stats: dict) -> dict[str, float]:
    """
    Compute a 6-dimension skill vector (0-100 scale) for radar charts.

    Dimensions:
    1. Scoring: f(ORtg, usage, eFG%)
    2. Shooting: f(3P%, 3PA_rate, FT%)
    3. Playmaking: f(AST%, inverse TOV%)
    4. Defense: f(inverse DRtg, STL%, BLK%)
    5. Rebounding: f(ORB%, DRB%)
    6. Efficiency: f(BPM, TS%, inverse TOV%)
    """

    def percentile(val, min_val, max_val):
        """Convert a value to 0-100 scale based on observed min/max."""
        if max_val == min_val:
            return 50.0
        return max(0, min(100, ((val - min_val) / (max_val - min_val)) * 100))

    ortg = safe_get(player, col_map["ortg"])
    drtg = safe_get(player, col_map["drtg"])
    usage = safe_get(player, col_map["usage"])
    efg = safe_get(player, col_map["efg"])
    ts = safe_get(player, col_map["ts"])
    threep = safe_get(player, col_map["threep_pct"])
    threep_rate = safe_get(player, col_map["threep_rate"])
    ast = safe_get(player, col_map["ast_pct"])
    tov = safe_get(player, col_map["tov_pct"])
    stl = safe_get(player, col_map["stl_pct"])
    blk = safe_get(player, col_map["blk_pct"])
    orb = safe_get(player, col_map["orb_pct"])
    drb = safe_get(player, col_map["drb_pct"])
    bpm = safe_get(player, col_map["bpm"])

    # Scoring: ORtg (40%) + usage (30%) + eFG (30%)
    scoring = (
        0.4 * percentile(ortg, stats["ortg_min"], stats["ortg_max"])
        + 0.3 * percentile(usage, stats["usage_min"], stats["usage_max"])
        + 0.3 * percentile(efg, stats["efg_min"], stats["efg_max"])
    )

    # Shooting: 3P% (50%) + 3PA rate (30%) + TS% (20%)
    shooting = (
        0.5 * percentile(threep, stats["threep_min"], stats["threep_max"])
        + 0.3 * percentile(threep_rate, stats["threep_rate_min"], stats["threep_rate_max"])
        + 0.2 * percentile(ts, stats["ts_min"], stats["ts_max"])
    )

    # Playmaking: AST% (65%) + inverse TOV% (35%)
    playmaking = (
        0.65 * percentile(ast, stats["ast_min"], stats["ast_max"])
        + 0.35 * percentile(-tov, -stats["tov_max"], -stats["tov_min"])
    )

    # Defense: inverse DRtg (40%) + STL% (30%) + BLK% (30%)
    defense = (
        0.4 * percentile(-drtg, -stats["drtg_max"], -stats["drtg_min"])
        + 0.3 * percentile(stl, stats["stl_min"], stats["stl_max"])
        + 0.3 * percentile(blk, stats["blk_min"], stats["blk_max"])
    )

    # Rebounding: ORB% (40%) + DRB% (60%)
    rebounding = (
        0.4 * percentile(orb, stats["orb_min"], stats["orb_max"])
        + 0.6 * percentile(drb, stats["drb_min"], stats["drb_max"])
    )

    # Efficiency: BPM (50%) + TS% (30%) + inverse TOV% (20%)
    efficiency = (
        0.5 * percentile(bpm, stats["bpm_min"], stats["bpm_max"])
        + 0.3 * percentile(ts, stats["ts_min"], stats["ts_max"])
        + 0.2 * percentile(-tov, -stats["tov_max"], -stats["tov_min"])
    )

    return {
        "scoring": round(scoring, 1),
        "shooting": round(shooting, 1),
        "playmaking": round(playmaking, 1),
        "defense": round(defense, 1),
        "rebounding": round(rebounding, 1),
        "efficiency": round(efficiency, 1),
    }


def compute_global_stats(df: pd.DataFrame, col_map: dict) -> dict:
    """Compute min/max for each stat across all players (for percentile normalization)."""
    stats = {}
    stat_cols = [
        ("ortg", "ortg"), ("drtg", "drtg"), ("usage", "usage"),
        ("efg", "efg"), ("ts", "ts"), ("threep", "threep_pct"),
        ("threep_rate", "threep_rate"), ("ast", "ast_pct"),
        ("tov", "tov_pct"), ("stl", "stl_pct"), ("blk", "blk_pct"),
        ("orb", "orb_pct"), ("drb", "drb_pct"), ("bpm", "bpm"),
    ]

    for key, col_key in stat_cols:
        col_name = col_map.get(col_key)
        if col_name and col_name in df.columns:
            vals = pd.to_numeric(df[col_name], errors="coerce").dropna()
            stats[f"{key}_min"] = float(vals.quantile(0.05)) if len(vals) > 0 else 0
            stats[f"{key}_max"] = float(vals.quantile(0.95)) if len(vals) > 0 else 100
        else:
            stats[f"{key}_min"] = 0
            stats[f"{key}_max"] = 100

    return stats


def create_player_id(name: str, team: str) -> str:
    """Create a URL-safe player ID."""
    clean = f"{name}_{team}".lower().replace(" ", "_").replace(".", "").replace("'", "")
    return "".join(c for c in clean if c.isalnum() or c == "_")


def create_team_id(team: str) -> str:
    """Create a URL-safe team ID."""
    clean = team.lower().replace(" ", "_").replace(".", "").replace("'", "")
    return "".join(c for c in clean if c.isalnum() or c == "_")


def parse_height_inches(ht_str) -> int | None:
    """Parse height string like '6-7' or '6\\'7' into inches."""
    if pd.isna(ht_str):
        return None
    ht_str = str(ht_str).strip()
    for sep in ["-", "'", "'"]:
        if sep in ht_str:
            parts = ht_str.split(sep)
            try:
                feet = int(parts[0].strip())
                inches = int(parts[1].strip().replace('"', ''))
                return feet * 12 + inches
            except (ValueError, IndexError):
                continue
    try:
        val = float(ht_str)
        if val > 60:  # already in inches
            return int(val)
        return int(val * 12)  # feet as decimal
    except ValueError:
        return None


def profile_team(team_df: pd.DataFrame, team_name: str, col_map: dict, global_stats: dict) -> dict:
    """
    Build player profiles for a single team.
    Returns team dict with players array.
    """
    team_id = create_team_id(team_name)
    players = []

    # Sort by minutes played, take top 10 rotation players
    min_col = col_map.get("mpg")
    if min_col and min_col in team_df.columns:
        team_df = team_df.copy()
        team_df[min_col] = pd.to_numeric(team_df[min_col], errors="coerce").fillna(0)
        team_df = team_df.sort_values(min_col, ascending=False).head(10)

    for _, row in team_df.iterrows():
        player_dict = row.to_dict()
        name = str(player_dict.get(col_map["player"], "Unknown"))
        pos = str(player_dict.get(col_map["pos"], "")).strip()
        ht_raw = player_dict.get(col_map["height"]) if col_map["height"] else None
        yr = str(player_dict.get(col_map["year_class"], "")) if col_map["year_class"] else ""

        archetype = classify_archetype(player_dict, col_map)
        skills = compute_skill_vector(player_dict, col_map, global_stats)

        player_profile = {
            "id": create_player_id(name, team_name),
            "name": name,
            "team": team_name,
            "teamId": team_id,
            "position": pos,
            "heightInches": parse_height_inches(ht_raw),
            "yearClass": yr,
            "archetype": archetype,
            "skills": skills,
            "stats": {
                "ortg": safe_get(player_dict, col_map["ortg"]),
                "drtg": safe_get(player_dict, col_map["drtg"]),
                "usage": safe_get(player_dict, col_map["usage"]),
                "efg": safe_get(player_dict, col_map["efg"]),
                "ts": safe_get(player_dict, col_map["ts"]),
                "threepPct": safe_get(player_dict, col_map["threep_pct"]),
                "threepRate": safe_get(player_dict, col_map["threep_rate"]),
                "astPct": safe_get(player_dict, col_map["ast_pct"]),
                "tovPct": safe_get(player_dict, col_map["tov_pct"]),
                "orbPct": safe_get(player_dict, col_map["orb_pct"]),
                "drbPct": safe_get(player_dict, col_map["drb_pct"]),
                "blkPct": safe_get(player_dict, col_map["blk_pct"]),
                "stlPct": safe_get(player_dict, col_map["stl_pct"]),
                "bpm": safe_get(player_dict, col_map["bpm"]),
                "ppg": safe_get(player_dict, col_map["ppg"]),
                "mpg": safe_get(player_dict, col_map["mpg"]),
                "gp": safe_get(player_dict, col_map["gp"]),
            },
        }
        players.append(player_profile)

    return {
        "teamId": team_id,
        "teamName": team_name,
        "players": players,
    }


def profile_all_teams(year: int = 2025) -> list[dict]:
    """Profile all teams from raw data. Returns list of team dicts."""
    print("Profiling players...")

    df = load_raw_players(year)
    col_map = resolve_columns(df)

    # Log column resolution
    resolved = {k: v for k, v in col_map.items() if v is not None}
    missing = {k for k, v in col_map.items() if v is None}
    print(f"  Resolved {len(resolved)}/{len(col_map)} columns")
    if missing:
        print(f"  Missing columns: {missing}")

    global_stats = compute_global_stats(df, col_map)

    team_col = col_map["team"]
    if team_col is None:
        raise ValueError("Cannot find team column in data")

    teams = []
    for team_name in sorted(df[team_col].unique()):
        team_df = df[df[team_col] == team_name]
        team_data = profile_team(team_df, team_name, col_map, global_stats)

        # Save per-team file
        team_dir = os.path.join(PROCESSED_DIR, "teams", team_data["teamId"])
        os.makedirs(team_dir, exist_ok=True)
        with open(os.path.join(team_dir, "players.json"), "w") as f:
            json.dump(team_data, f, indent=2)

        teams.append({
            "teamId": team_data["teamId"],
            "teamName": team_data["teamName"],
            "playerCount": len(team_data["players"]),
        })
        print(f"  {team_name}: {len(team_data['players'])} players profiled")

    return teams


if __name__ == "__main__":
    profile_all_teams()
