"""
Main pipeline orchestrator — fetches data, profiles players, scores lineups.

Usage:
    python pipeline.py           # Full pipeline
    python pipeline.py --skip-fetch  # Skip fetching (use cached raw data)
"""

import json
import os
import sys
import time

from fetch_data import fetch_and_save, TARGET_TEAMS
from player_profiler import profile_all_teams
from lineup_scorer import score_all_teams

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "data", "processed")


def build_manifest(team_results: list[dict], lineup_results: list[dict]):
    """Build a manifest file listing all available teams."""
    # Merge team info with lineup info
    lineup_map = {r["teamId"]: r for r in lineup_results}

    manifest = {
        "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "season": "2024-25",
        "teams": [],
    }

    for team in team_results:
        lineup_info = lineup_map.get(team["teamId"], {})
        manifest["teams"].append({
            "teamId": team["teamId"],
            "teamName": team["teamName"],
            "playerCount": team["playerCount"],
            "topLineupScore": lineup_info.get("topLineupScore", 0),
        })

    # Sort by team name
    manifest["teams"].sort(key=lambda t: t["teamName"])

    manifest_path = os.path.join(PROCESSED_DIR, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest saved to {manifest_path}")
    print(f"Total teams: {len(manifest['teams'])}")


def run_pipeline(skip_fetch: bool = False):
    """Run the full data pipeline."""
    start = time.time()
    print("=" * 60)
    print("College Basketball Lineup Optimizer — Data Pipeline")
    print("=" * 60)

    # Step 1: Fetch raw data
    if not skip_fetch:
        print("\n[1/3] Fetching player data from BartTorvik...")
        try:
            fetch_and_save()
        except Exception as e:
            print(f"  Error fetching data: {e}")
            print("  Falling back to cached data if available...")
    else:
        print("\n[1/3] Skipping fetch (using cached data)...")

    # Step 2: Profile players
    print("\n[2/3] Profiling players and classifying archetypes...")
    team_results = profile_all_teams()

    # Step 3: Score lineups
    print("\n[3/3] Scoring lineup combinations...")
    lineup_results = score_all_teams()

    # Build manifest
    build_manifest(team_results, lineup_results)

    elapsed = time.time() - start
    print(f"\nPipeline complete in {elapsed:.1f}s")


if __name__ == "__main__":
    skip = "--skip-fetch" in sys.argv
    run_pipeline(skip_fetch=skip)
