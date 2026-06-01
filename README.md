# College Basketball Lineup Optimizer

A data-driven tool that helps college basketball coaching staffs identify optimal 5-man lineup combinations using publicly available advanced statistics.

**🔗 Live demo: [college-bball-lineup-optimizer.vercel.app](https://college-bball-lineup-optimizer.vercel.app/)**

## Problem

With 8–12 rotation players on a roster, there are hundreds of possible 5-man lineups. Coaches typically rely on intuition and film to set rotations — this tool quantifies lineup quality across 7 key dimensions to surface the best combinations and hidden-gem units.

## How It Works

1. **Data Pipeline (Python)**: Builds a dataset of player-level box score stats for 14 top Division I programs (2024–25 season) and computes advanced metrics (ORtg, DRtg, Usage%, TS%, etc.) from them using standard basketball analytics formulas
2. **Player Profiling**: Classifies each player into an archetype (Floor General, Rim Protector, 3-and-D Wing, etc.) and builds a 6-dimension skill vector
3. **Lineup Scoring**: Evaluates every possible 5-man combination across 7 weighted dimensions:
   - Offensive Efficiency (30%)
   - Defensive Efficiency (25%)
   - Floor Spacing (15%)
   - Playmaking (10%)
   - Rebounding (10%)
   - Versatility (5%)
   - Balance (5%)
4. **Interactive Dashboard (Next.js)**: Explore top lineups, build custom combinations, and compare units side-by-side

## Tech Stack

- **Data Pipeline**: Python, pandas, NumPy, requests
- **Web App**: Next.js 16, TypeScript, Tailwind CSS, Recharts
- **Deployment**: Vercel

## Data Sources

Player-level box score statistics for the 2024–25 season (points, rebounds, assists, shooting splits, minutes, etc.) for 14 top Division I programs, sourced from publicly available box score data. Advanced metrics (ORtg, DRtg, Usage%, True Shooting%, eFG%, AST%, BPM) are computed from these box scores using standard formulas — the same methodology used by public analytics sites like [KenPom](https://kenpom.com), [BartTorvik](https://barttorvik.com), and [Basketball Reference](https://www.sports-reference.com/cbb/).

> **Note on data:** The pipeline ships with a curated dataset (`python/seed_data.py`) of known 2024–25 stats so the project runs reproducibly out of the box. A live-fetch path (`python/fetch_data.py`) is included for future integration with ESPN/BartTorvik once their endpoints are accessible.

## Getting Started

### Python Pipeline

```bash
cd python
pip install -r requirements.txt
python pipeline.py
```

### Web App

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## License

MIT
