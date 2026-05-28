"""
Lineup Scorer — evaluates every 5-man combination from a team's rotation
players across 7 weighted dimensions.
"""

import json
import os
from itertools import combinations
import numpy as np

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")

# Scoring weights
WEIGHTS = {
    "offense": 0.30,
    "defense": 0.25,
    "spacing": 0.15,
    "playmaking": 0.10,
    "rebounding": 0.10,
    "versatility": 0.05,
    "balance": 0.05,
}


def score_offense(players: list[dict]) -> float:
    """
    Offensive efficiency score (0-100).
    Usage-weighted ORtg with penalty for over-reliance on one scorer.
    """
    ortgs = [p["stats"]["ortg"] for p in players]
    usages = [p["stats"]["usage"] for p in players]

    total_usage = sum(usages)
    if total_usage == 0:
        return 50.0

    # Usage-weighted offensive rating
    weighted_ortg = sum(o * u for o, u in zip(ortgs, usages)) / total_usage

    # Normalize: college ORtg typically ranges 85-125
    score = ((weighted_ortg - 85) / (125 - 85)) * 100
    score = max(0, min(100, score))

    # Penalty if top player has > 32% usage (over-reliance)
    max_usage = max(usages)
    if max_usage > 32:
        score *= 0.92

    return round(score, 1)


def score_defense(players: list[dict]) -> float:
    """
    Defensive efficiency score (0-100).
    Average DRtg (lower = better) with bonus for rim protection.
    """
    drtgs = [p["stats"]["drtg"] for p in players]
    blks = [p["stats"]["blkPct"] for p in players]

    avg_drtg = np.mean(drtgs)

    # Normalize: college DRtg typically ranges 85-115 (lower is better)
    score = ((115 - avg_drtg) / (115 - 85)) * 100
    score = max(0, min(100, score))

    # Bonus for rim protection
    has_rim_protector = any(b >= 6.0 for b in blks)
    if has_rim_protector:
        score = min(100, score + 5)

    # Bonus for perimeter defense
    stls = [p["stats"]["stlPct"] for p in players]
    avg_stl = np.mean(stls)
    if avg_stl >= 2.0:
        score = min(100, score + 3)

    return round(score, 1)


def score_spacing(players: list[dict]) -> float:
    """
    Floor spacing score (0-100).
    Based on number of capable 3-point shooters in the lineup.
    """
    shooters = 0
    for p in players:
        threep = p["stats"]["threepPct"]
        threep_rate = p["stats"]["threepRate"]
        # A "shooter" = 33%+ from 3 with meaningful attempt rate (20%+)
        if threep >= 33 and threep_rate >= 20:
            shooters += 1

    # Scoring curve: 0 shooters is terrible, 4+ is elite
    spacing_map = {0: 10, 1: 30, 2: 55, 3: 78, 4: 93, 5: 100}
    score = spacing_map.get(shooters, 100)

    # Slight bonus for lineup average 3P%
    avg_3p = np.mean([p["stats"]["threepPct"] for p in players])
    if avg_3p >= 36:
        score = min(100, score + 5)

    return round(float(score), 1)


def score_playmaking(players: list[dict]) -> float:
    """
    Playmaking score (0-100).
    Based on assist generation and ball-handling presence.
    """
    ast_pcts = [p["stats"]["astPct"] for p in players]
    tov_pcts = [p["stats"]["tovPct"] for p in players]

    total_ast = sum(ast_pcts)
    avg_tov = np.mean(tov_pcts)

    # Normalize total AST%: typically 40-120 for a 5-man unit
    ast_score = ((total_ast - 40) / (120 - 40)) * 100
    ast_score = max(0, min(100, ast_score))

    # Penalty for high turnover rate
    tov_penalty = max(0, (avg_tov - 15) * 3)

    score = ast_score - tov_penalty

    # Bonus for having a primary ball handler
    has_primary = any(a >= 20 for a in ast_pcts)
    if has_primary:
        score = min(100, score + 8)
    else:
        score -= 10

    return round(max(0, min(100, score)), 1)


def score_rebounding(players: list[dict]) -> float:
    """
    Rebounding score (0-100).
    Combined offensive and defensive rebounding coverage.
    """
    orb_pcts = [p["stats"]["orbPct"] for p in players]
    drb_pcts = [p["stats"]["drbPct"] for p in players]

    avg_orb = np.mean(orb_pcts)
    avg_drb = np.mean(drb_pcts)

    # Normalize ORB%: typically 2-12 range
    orb_score = ((avg_orb - 2) / (12 - 2)) * 100

    # Normalize DRB%: typically 8-22 range
    drb_score = ((avg_drb - 8) / (22 - 8)) * 100

    # Defensive rebounds weighted more (60/40)
    score = 0.4 * orb_score + 0.6 * drb_score
    score = max(0, min(100, score))

    # Bonus for having a dominant rebounder
    has_glass_eater = any(d >= 18 for d in drb_pcts)
    if has_glass_eater:
        score = min(100, score + 5)

    return round(score, 1)


def score_versatility(players: list[dict]) -> float:
    """
    Versatility score (0-100).
    Position coverage and height distribution.
    """
    positions = [p["position"].upper().strip() for p in players]
    heights = [p["heightInches"] for p in players if p["heightInches"] is not None]

    # Position coverage: map to 1-5 scale
    pos_map = {
        "PG": 1, "G": 1.5, "CG": 1.5, "COMBO GUARD": 1.5,
        "SG": 2, "GF": 2.5,
        "SF": 3, "F": 3.5, "WING": 3,
        "PF": 4, "FC": 4.5,
        "C": 5,
    }

    pos_values = []
    for p in positions:
        for key, val in pos_map.items():
            if key in p:
                pos_values.append(val)
                break
        else:
            pos_values.append(3)  # default to wing

    # Unique position coverage (more spread = more versatile)
    pos_spread = len(set(round(v) for v in pos_values))  # unique position slots
    pos_score = (pos_spread / 5) * 100

    # Height distribution: want reasonable spread (not all same height)
    if len(heights) >= 3:
        ht_range = max(heights) - min(heights)
        # Ideal range is 6-10 inches
        if 6 <= ht_range <= 12:
            ht_score = 80 + (ht_range - 6) * 3
        elif ht_range < 6:
            ht_score = ht_range * 13
        else:
            ht_score = max(50, 100 - (ht_range - 12) * 5)
    else:
        ht_score = 50

    score = 0.6 * pos_score + 0.4 * ht_score
    return round(max(0, min(100, score)), 1)


def score_balance(players: list[dict]) -> float:
    """
    Balance score (0-100).
    Usage distribution (not too concentrated) and archetype diversity.
    """
    usages = [p["stats"]["usage"] for p in players]
    archetypes = [p["archetype"] for p in players]

    # Gini coefficient of usage rates (0 = perfectly equal, 1 = all to one player)
    usages_sorted = sorted(usages)
    n = len(usages_sorted)
    total = sum(usages_sorted)
    if total == 0:
        gini = 0
    else:
        numerator = sum((2 * (i + 1) - n - 1) * u for i, u in enumerate(usages_sorted))
        gini = numerator / (n * total)

    # Lower Gini = more balanced = higher score
    usage_score = (1 - gini) * 100

    # Archetype diversity: unique archetypes
    unique_archetypes = len(set(archetypes))
    archetype_score = (unique_archetypes / 5) * 100  # max 5 unique in a 5-man unit

    # Penalize duplicate archetypes heavily if 3+ of same type
    from collections import Counter
    arch_counts = Counter(archetypes)
    max_same = max(arch_counts.values())
    if max_same >= 3:
        archetype_score *= 0.6

    score = 0.5 * usage_score + 0.5 * archetype_score
    return round(max(0, min(100, score)), 1)


def score_lineup(players: list[dict]) -> dict:
    """
    Score a 5-man lineup across all dimensions.
    Returns dimension scores and composite score.
    """
    dimensions = {
        "offense": score_offense(players),
        "defense": score_defense(players),
        "spacing": score_spacing(players),
        "playmaking": score_playmaking(players),
        "rebounding": score_rebounding(players),
        "versatility": score_versatility(players),
        "balance": score_balance(players),
    }

    composite = sum(dimensions[k] * WEIGHTS[k] for k in WEIGHTS)

    return {
        "dimensions": dimensions,
        "composite": round(composite, 1),
    }


def identify_strengths_weaknesses(dimensions: dict) -> dict:
    """Identify top strengths and biggest weaknesses of a lineup."""
    sorted_dims = sorted(dimensions.items(), key=lambda x: x[1], reverse=True)

    strengths = [{"dimension": d, "score": s} for d, s in sorted_dims[:2] if s >= 60]
    weaknesses = [{"dimension": d, "score": s} for d, s in sorted_dims[-2:] if s < 50]

    return {"strengths": strengths, "weaknesses": weaknesses}


def score_team_lineups(team_data: dict) -> list[dict]:
    """
    Score all possible 5-man combinations from a team's rotation.
    Returns sorted list of top 50 lineups.
    """
    players = team_data["players"]

    if len(players) < 5:
        print(f"  Warning: {team_data['teamName']} has only {len(players)} players, skipping")
        return []

    all_lineups = []

    for combo in combinations(range(len(players)), 5):
        five = [players[i] for i in combo]
        result = score_lineup(five)

        analysis = identify_strengths_weaknesses(result["dimensions"])

        lineup_entry = {
            "playerIds": [five[i]["id"] for i in range(5)],
            "playerNames": [five[i]["name"] for i in range(5)],
            "composite": result["composite"],
            "dimensions": result["dimensions"],
            "strengths": analysis["strengths"],
            "weaknesses": analysis["weaknesses"],
        }
        all_lineups.append(lineup_entry)

    # Sort by composite score, take top 50
    all_lineups.sort(key=lambda x: x["composite"], reverse=True)
    top_lineups = all_lineups[:50]

    # Add rank
    for i, lineup in enumerate(top_lineups):
        lineup["rank"] = i + 1

    return top_lineups


def score_all_teams() -> list[dict]:
    """Score lineups for all profiled teams."""
    teams_dir = os.path.join(PROCESSED_DIR, "teams")
    if not os.path.exists(teams_dir):
        print("No profiled teams found. Run player_profiler.py first.")
        return []

    results = []

    for team_id in sorted(os.listdir(teams_dir)):
        team_dir = os.path.join(teams_dir, team_id)
        players_path = os.path.join(team_dir, "players.json")

        if not os.path.exists(players_path):
            continue

        with open(players_path) as f:
            team_data = json.load(f)

        print(f"  Scoring {team_data['teamName']} lineups...")
        lineups = score_team_lineups(team_data)

        # Save lineups
        with open(os.path.join(team_dir, "lineups.json"), "w") as f:
            json.dump({
                "teamId": team_data["teamId"],
                "teamName": team_data["teamName"],
                "totalCombinations": len(list(combinations(range(len(team_data["players"])), 5))),
                "lineups": lineups,
            }, f, indent=2)

        results.append({
            "teamId": team_data["teamId"],
            "teamName": team_data["teamName"],
            "topLineupScore": lineups[0]["composite"] if lineups else 0,
            "totalLineups": len(lineups),
        })
        print(f"    Top lineup: {lineups[0]['composite']} — {', '.join(lineups[0]['playerNames'][:3])}...")

    return results


if __name__ == "__main__":
    score_all_teams()
