# College Basketball Lineup Optimizer

A data-driven tool that helps college basketball coaching staffs identify optimal 5-man lineup combinations using publicly available advanced statistics.

## Problem

With 8–12 rotation players on a roster, there are hundreds of possible 5-man lineups. Coaches typically rely on intuition and film to set rotations — this tool quantifies lineup quality across 7 key dimensions to surface the best combinations and hidden-gem units.

## How It Works

1. **Data Pipeline (Python)**: Fetches player-level advanced stats from [BartTorvik](https://barttorvik.com) for the 2024–25 season
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
- **Web App**: Next.js 14, TypeScript, Tailwind CSS, Recharts
- **Deployment**: Vercel

## Data Sources

- [BartTorvik](https://barttorvik.com) — player-level advanced statistics (ORtg, DRtg, usage, shooting splits, etc.)

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
