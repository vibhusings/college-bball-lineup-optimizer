"""
Fetch player-level advanced stats from BartTorvik for the 2024-25 season.
Outputs raw player data as JSON.
"""

import json
import time
import os
import requests
import pandas as pd
from io import StringIO

# BartTorvik player stats endpoint
BARTTORVIK_PLAYER_URL = "https://barttorvik.com/playerstat.php"

# Teams to fetch — top programs across major conferences
TARGET_TEAMS = [
    # ACC
    "Duke", "North Carolina", "Wake Forest", "Clemson", "Virginia",
    # Big Ten
    "Purdue", "Michigan St.", "Illinois", "Wisconsin", "Iowa St.",
    # Big 12
    "Houston", "Kansas", "Arizona", "Baylor", "Texas Tech",
    # SEC
    "Auburn", "Tennessee", "Kentucky", "Alabama", "Florida",
    # Big East
    "UConn", "Marquette", "Creighton", "St. John's",
    # Others
    "Gonzaga", "St. Mary's",
]

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")


def fetch_all_players(year: int = 2025) -> pd.DataFrame:
    """
    Fetch all D1 player stats from BartTorvik for the given season.
    Returns a DataFrame with per-player advanced stats.
    """
    print(f"Fetching player stats for {year-1}-{str(year)[2:]} season...")

    params = {
        "year": year,
        "csv": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (CollegeBBallLineupOptimizer/1.0; academic research)",
        "Accept": "text/csv,text/plain,*/*",
    }

    resp = requests.get(BARTTORVIK_PLAYER_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()

    # Parse CSV response
    df = pd.read_csv(StringIO(resp.text))
    print(f"  Fetched {len(df)} total player records")

    return df


def normalize_team_name(name: str) -> str:
    """Normalize team names to match BartTorvik conventions."""
    return name.strip()


def filter_to_target_teams(df: pd.DataFrame, teams: list[str]) -> pd.DataFrame:
    """Filter DataFrame to only include players from target teams."""
    # BartTorvik uses a 'Team' column — find it
    team_col = None
    for col in df.columns:
        if col.lower().strip() in ("team", "school"):
            team_col = col
            break

    if team_col is None:
        print(f"  Warning: Could not find team column. Columns: {list(df.columns)}")
        return df

    # Normalize team names for matching
    df_teams = df[team_col].str.strip()
    target_set = {normalize_team_name(t) for t in teams}

    mask = df_teams.isin(target_set)
    filtered = df[mask].copy()
    print(f"  Filtered to {len(filtered)} players from {filtered[team_col].nunique()} target teams")

    # Report which teams were not found
    found_teams = set(filtered[team_col].str.strip().unique())
    missing = target_set - found_teams
    if missing:
        print(f"  Teams not found in data: {missing}")

    return filtered


def save_raw_data(df: pd.DataFrame, year: int = 2025):
    """Save raw player data to JSON."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    output_path = os.path.join(RAW_DATA_DIR, f"players_{year}.json")

    records = df.to_dict(orient="records")
    with open(output_path, "w") as f:
        json.dump(records, f, indent=2, default=str)

    print(f"  Saved {len(records)} records to {output_path}")
    return output_path


def fetch_and_save(year: int = 2025, teams: list[str] | None = None) -> str:
    """Main entry point: fetch player stats and save to disk."""
    if teams is None:
        teams = TARGET_TEAMS

    df = fetch_all_players(year)
    df = filter_to_target_teams(df, teams)
    return save_raw_data(df, year)


if __name__ == "__main__":
    fetch_and_save()
