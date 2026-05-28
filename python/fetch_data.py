"""
Fetch player-level stats from ESPN's public API for the 2024-25 season.
Computes advanced metrics (ORtg, DRtg, Usage%, etc.) from box score data.
"""

import json
import time
import os
import requests

# ESPN team IDs for our target teams
TEAM_IDS = {
    # ACC
    "Duke": 150, "North Carolina": 153, "Wake Forest": 154, "Clemson": 228, "Virginia": 258,
    # Big Ten
    "Purdue": 2509, "Michigan St": 127, "Illinois": 356, "Wisconsin": 275, "Iowa St": 66,
    # Big 12
    "Houston": 248, "Kansas": 2305, "Arizona": 12, "Baylor": 239, "Texas Tech": 2641,
    # SEC
    "Auburn": 2, "Tennessee": 2633, "Kentucky": 96, "Alabama": 333, "Florida": 57,
    # Big East
    "UConn": 41, "Marquette": 269, "Creighton": 156, "St Johns": 2599,
    # Others
    "Gonzaga": 2250, "St Marys": 2608,
}

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball"
ESPN_WEB_BASE = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/mens-college-basketball"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
}


def fetch_team_roster(team_id: int, team_name: str) -> list[dict]:
    """Fetch roster for a team from ESPN API."""
    url = f"{ESPN_BASE}/teams/{team_id}/roster"
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    athletes = data.get("athletes", [])
    roster = []
    for a in athletes:
        roster.append({
            "espnId": a.get("id"),
            "name": a.get("fullName", a.get("displayName", "Unknown")),
            "position": a.get("position", {}).get("abbreviation", ""),
            "heightInches": a.get("height"),
            "weight": a.get("weight"),
            "year": a.get("experience", {}).get("abbreviation", "") if a.get("experience") else "",
            "jersey": a.get("jersey", ""),
            "team": team_name,
            "teamId": team_id,
        })

    return roster


def fetch_player_stats(espn_id: str) -> dict | None:
    """Fetch season stats for a single player from ESPN."""
    url = f"{ESPN_WEB_BASE}/athletes/{espn_id}/stats"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
    except Exception:
        return None

    stats = {}
    categories = data.get("categories", [])
    for cat in categories:
        names = cat.get("names", [])
        # Find the most recent season stats
        seasons = cat.get("seasons", [])
        if not seasons:
            continue

        # Get the last season (most recent)
        season = seasons[-1]
        season_stats = season.get("stats", [])
        if not season_stats:
            continue

        # Match stat names to values
        for i, name in enumerate(names):
            if i < len(season_stats):
                val = season_stats[i]
                # Handle compound stats like "5.2-10.4"
                if isinstance(val, str) and "-" in val:
                    parts = val.split("-")
                    try:
                        stats[f"{name}_made"] = float(parts[0])
                        stats[f"{name}_att"] = float(parts[1])
                    except (ValueError, IndexError):
                        stats[name] = val
                else:
                    try:
                        stats[name] = float(val)
                    except (ValueError, TypeError):
                        stats[name] = val

    return stats if stats else None


def compute_advanced_stats(player: dict, team_stats: dict) -> dict:
    """
    Compute advanced basketball metrics from basic box score stats.

    Key formulas:
    - Usage% = 100 * ((FGA + 0.44*FTA + TOV) * TeamMinutes) / (Minutes * (TeamFGA + 0.44*TeamFTA + TeamTOV) * 5)
    - TS% = PTS / (2 * (FGA + 0.44 * FTA))
    - eFG% = (FGM + 0.5 * 3PM) / FGA
    - ORtg/DRtg = estimated from individual + team stats
    """
    stats = player.get("rawStats", {})
    if not stats:
        return {}

    gp = stats.get("gamesPlayed", 1)
    if gp == 0:
        gp = 1

    mpg = stats.get("avgMinutes", 0)
    ppg = stats.get("avgPoints", 0)
    apg = stats.get("avgAssists", 0)
    rpg = stats.get("avgRebounds", 0)
    orpg = stats.get("avgOffensiveRebounds", 0)
    drpg = stats.get("avgDefensiveRebounds", 0)
    spg = stats.get("avgSteals", 0)
    bpg = stats.get("avgBlocks", 0)
    topg = stats.get("avgTurnovers", 0)
    fpg = stats.get("avgFouls", 0)

    fg_pct = stats.get("fieldGoalPct", 0) / 100 if stats.get("fieldGoalPct", 0) > 1 else stats.get("fieldGoalPct", 0)
    three_pct = stats.get("threePointFieldGoalPct", 0) / 100 if stats.get("threePointFieldGoalPct", 0) > 1 else stats.get("threePointFieldGoalPct", 0)
    ft_pct = stats.get("freeThrowPct", 0) / 100 if stats.get("freeThrowPct", 0) > 1 else stats.get("freeThrowPct", 0)

    # Estimate per-game attempts from percentages and makes
    fgm_pg = stats.get("avgFieldGoalsMade-avgFieldGoalsAttempted_made", ppg * 0.4)
    fga_pg = stats.get("avgFieldGoalsMade-avgFieldGoalsAttempted_att", fgm_pg / max(fg_pct, 0.01))
    tpm_pg = stats.get("avgThreePointFieldGoalsMade-avgThreePointFieldGoalsAttempted_made", 0)
    tpa_pg = stats.get("avgThreePointFieldGoalsMade-avgThreePointFieldGoalsAttempted_att", 0)
    ftm_pg = stats.get("avgFreeThrowsMade-avgFreeThrowsAttempted_made", 0)
    fta_pg = stats.get("avgFreeThrowsMade-avgFreeThrowsAttempted_att", 0)

    # True Shooting %
    ts_denom = 2 * (fga_pg + 0.44 * fta_pg)
    ts_pct = (ppg / ts_denom * 100) if ts_denom > 0 else 0

    # Effective FG%
    efg = ((fgm_pg + 0.5 * tpm_pg) / fga_pg * 100) if fga_pg > 0 else 0

    # 3-Point attempt rate
    three_rate = (tpa_pg / fga_pg * 100) if fga_pg > 0 else 0

    # Free throw rate
    ftr = (fta_pg / fga_pg * 100) if fga_pg > 0 else 0

    # Team-level estimates (per-game)
    team_fga = team_stats.get("fga_pg", 60)
    team_fta = team_stats.get("fta_pg", 18)
    team_tov = team_stats.get("tov_pg", 12)
    team_ppg = team_stats.get("ppg", 75)
    team_opp_ppg = team_stats.get("opp_ppg", 70)
    team_pace = team_stats.get("pace", 68)

    # Usage Rate (simplified)
    possessions_used = fga_pg + 0.44 * fta_pg + topg
    team_possessions = team_fga + 0.44 * team_fta + team_tov
    if mpg > 0 and team_possessions > 0:
        usage = 100 * (possessions_used * 40) / (mpg * team_possessions)
    else:
        usage = 0
    usage = min(usage, 45)  # cap at reasonable max

    # Assist Rate (simplified estimate)
    if mpg > 0:
        # AST% = 100 * AST / (((MIN / (TeamMIN / 5)) * TeamFGM) - FGM)
        team_fgm = team_stats.get("fgm_pg", 25)
        teammate_fgm = max(team_fgm - fgm_pg, 1)
        min_ratio = mpg / 40  # proportion of game played
        ast_pct = 100 * apg / (min_ratio * teammate_fgm) if (min_ratio * teammate_fgm) > 0 else 0
        ast_pct = min(ast_pct, 50)
    else:
        ast_pct = 0

    # Turnover Rate
    if possessions_used > 0:
        tov_pct = 100 * topg / possessions_used
    else:
        tov_pct = 0

    # Rebound Rates (simplified)
    team_orb = team_stats.get("orb_pg", 10)
    team_drb = team_stats.get("drb_pg", 25)
    opp_drb = team_stats.get("opp_drb_pg", 25)
    opp_orb = team_stats.get("opp_orb_pg", 10)

    if mpg > 0:
        min_ratio = mpg / 40
        orb_pct = 100 * orpg / (min_ratio * (team_orb + opp_drb)) if (min_ratio * (team_orb + opp_drb)) > 0 else 0
        drb_pct = 100 * drpg / (min_ratio * (team_drb + opp_orb)) if (min_ratio * (team_drb + opp_orb)) > 0 else 0
    else:
        orb_pct = 0
        drb_pct = 0

    # Block and Steal rates (simplified)
    opp_fga = team_stats.get("opp_fga_pg", 58)
    if mpg > 0:
        min_ratio = mpg / 40
        blk_pct = 100 * bpg / (min_ratio * opp_fga * 0.5) if (min_ratio * opp_fga) > 0 else 0  # ~half are 2pt attempts
        stl_pct = 100 * spg / (min_ratio * team_possessions) if (min_ratio * team_possessions) > 0 else 0
    else:
        blk_pct = 0
        stl_pct = 0

    # Offensive Rating (points produced per 100 possessions, simplified)
    # Use team ORtg as base, adjust by player efficiency relative to team
    team_ortg = (team_ppg / team_pace) * 100 if team_pace > 0 else 100
    player_efficiency = ppg / max(possessions_used, 0.1)
    team_efficiency = team_ppg / max(team_possessions, 0.1)
    ortg = team_ortg * (0.4 + 0.6 * (player_efficiency / max(team_efficiency, 0.01)))
    ortg = max(80, min(130, ortg))  # clamp to reasonable range

    # Defensive Rating (simplified — estimate from team DRtg + individual defensive stats)
    team_drtg = (team_opp_ppg / team_pace) * 100 if team_pace > 0 else 100
    def_contribution = (stl_pct * 0.5 + blk_pct * 0.3 + drb_pct * 0.2) / 10
    drtg = team_drtg - def_contribution
    drtg = max(85, min(115, drtg))

    # Box Plus-Minus (simplified)
    bpm = (ppg - team_ppg / 5) * 0.3 + (rpg - 4) * 0.2 + apg * 0.3 - topg * 0.4 + spg * 0.5 + bpg * 0.5
    bpm = max(-8, min(12, bpm))

    return {
        "ortg": round(ortg, 1),
        "drtg": round(drtg, 1),
        "usage": round(usage, 1),
        "efg": round(efg, 1),
        "ts": round(ts_pct, 1),
        "threepPct": round(three_pct * 100, 1),
        "threepRate": round(three_rate, 1),
        "ftr": round(ftr, 1),
        "astPct": round(ast_pct, 1),
        "tovPct": round(tov_pct, 1),
        "orbPct": round(orb_pct, 1),
        "drbPct": round(drb_pct, 1),
        "blkPct": round(blk_pct, 1),
        "stlPct": round(stl_pct, 1),
        "bpm": round(bpm, 1),
        "ppg": round(ppg, 1),
        "rpg": round(rpg, 1),
        "apg": round(apg, 1),
        "spg": round(spg, 1),
        "bpg": round(bpg, 1),
        "mpg": round(mpg, 1),
        "gp": int(gp),
        "fgPct": round(fg_pct * 100, 1),
        "ftPct": round(ft_pct * 100, 1),
    }


def fetch_team_stats(team_id: int) -> dict:
    """Fetch team-level stats to use as context for advanced stat computation."""
    url = f"{ESPN_BASE}/teams/{team_id}/statistics"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return _default_team_stats()

    results = data.get("results", {}).get("stats", {})
    categories = results.get("categories", [])

    team_stats = {}
    for cat in categories:
        for stat in cat.get("stats", []):
            team_stats[stat["name"]] = stat.get("value", 0)

    gp = team_stats.get("gamesPlayed", 34)

    return {
        "ppg": team_stats.get("avgPoints", 75),
        "opp_ppg": team_stats.get("avgPointsAgainst", team_stats.get("avgPoints", 75) - 5),
        "fga_pg": team_stats.get("avgFieldGoalsAttempted", 58),
        "fgm_pg": team_stats.get("avgFieldGoalsMade", 25),
        "fta_pg": team_stats.get("avgFreeThrowsAttempted", 18),
        "tov_pg": team_stats.get("avgTurnovers", 12),
        "orb_pg": team_stats.get("avgOffensiveRebounds", 10),
        "drb_pg": team_stats.get("avgDefensiveRebounds", 25),
        "opp_drb_pg": 25,  # estimate
        "opp_orb_pg": 10,  # estimate
        "opp_fga_pg": 58,  # estimate
        "pace": 68,  # average D1 pace
        "gp": gp,
    }


def _default_team_stats() -> dict:
    return {
        "ppg": 75, "opp_ppg": 70, "fga_pg": 58, "fgm_pg": 25,
        "fta_pg": 18, "tov_pg": 12, "orb_pg": 10, "drb_pg": 25,
        "opp_drb_pg": 25, "opp_orb_pg": 10, "opp_fga_pg": 58,
        "pace": 68, "gp": 34,
    }


def fetch_and_save(year: int = 2025) -> str:
    """Fetch all team rosters and player stats, save to disk."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    all_players = []
    print(f"Fetching data for {len(TEAM_IDS)} teams...")

    for team_name, team_id in TEAM_IDS.items():
        print(f"  {team_name} (ESPN ID: {team_id})...")

        # Fetch roster
        try:
            roster = fetch_team_roster(team_id, team_name)
        except Exception as e:
            print(f"    Error fetching roster: {e}")
            continue

        # Fetch team-level stats
        team_stats = fetch_team_stats(team_id)
        time.sleep(0.3)  # be nice to ESPN

        # Fetch per-player stats
        for player in roster:
            espn_id = player.get("espnId")
            if not espn_id:
                continue

            raw_stats = fetch_player_stats(espn_id)
            if raw_stats:
                player["rawStats"] = raw_stats
                player["advancedStats"] = compute_advanced_stats(player, team_stats)
            else:
                player["rawStats"] = {}
                player["advancedStats"] = {}

            time.sleep(0.15)  # rate limiting

        # Filter to players with meaningful minutes
        rotation = [p for p in roster if p.get("advancedStats", {}).get("mpg", 0) >= 5]
        rotation.sort(key=lambda x: x.get("advancedStats", {}).get("mpg", 0), reverse=True)

        all_players.extend(rotation)
        print(f"    {len(rotation)} rotation players (of {len(roster)} total)")

    # Save raw data
    output_path = os.path.join(RAW_DATA_DIR, f"players_{year}.json")
    with open(output_path, "w") as f:
        json.dump(all_players, f, indent=2, default=str)

    print(f"\nSaved {len(all_players)} players to {output_path}")
    return output_path


if __name__ == "__main__":
    fetch_and_save()
