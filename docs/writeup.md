# College Basketball Lineup Optimizer — Project Write-Up

**Live demo:** https://college-bball-lineup-optimizer.vercel.app/
**Source code:** https://github.com/vibhusings/college-bball-lineup-optimizer

## Problem Statement

College basketball coaching staffs face a combinatorial challenge in rotation planning. With 8-12 rotation players on a typical roster, there are **56-792 possible 5-man lineup combinations** -- far too many to evaluate through film study and intuition alone. Coaches need a data-driven tool to:

- **Identify optimal lineups** they may not have considered
- **Quantify the tradeoffs** of each combination (e.g., gaining spacing at the cost of rim protection)
- **Test "what-if" scenarios** before committing practice time to new units
- **Prepare situation-specific lineups** (need shooting? defense? rebounding?)

This tool solves the problem by scoring every possible 5-man combination across 7 key dimensions, surfacing the top-ranked lineups, and letting staff build and compare custom units interactively.

## Data Sources

**Primary Source: Publicly Available Box Score Statistics (2024-25 Season)**

Player-level per-game statistics were sourced from public box score data for 14 top Division I programs:

- Alabama, Auburn, Duke, Florida, Gonzaga, Houston, Kansas, Kentucky, Marquette, Michigan State, Purdue, St. John's, Tennessee, UConn

**Basic stats collected per player:**
- Points, rebounds, assists, steals, blocks per game
- Field goal %, 3-point %, free throw %
- Field goal attempts, 3-point attempts, free throw attempts
- Minutes and games played

**Advanced metrics computed from basic stats using standard basketball analytics formulas:**

| Metric | Formula Basis |
|--------|--------------|
| ORtg (Offensive Rating) | Points produced per 100 possessions, adjusted by team context |
| DRtg (Defensive Rating) | Points allowed per 100 possessions, adjusted by individual defense |
| Usage% | (FGA + 0.44*FTA + TOV) * TeamMIN / (MIN * TeamPoss * 5) |
| TS% (True Shooting) | PTS / (2 * (FGA + 0.44 * FTA)) |
| eFG% (Effective FG) | (FGM + 0.5 * 3PM) / FGA |
| AST% | Assists / Teammate FGM while on court |
| BPM (Box Plus-Minus) | Composite of scoring, rebounding, assists, turnovers, steals, blocks |

These formulas follow established basketball analytics methodology used by KenPom, BartTorvik, and Basketball Reference.

## Solution Architecture

### Data Pipeline (Python)

```
seed_data.py  -->  player_profiler.py  -->  lineup_scorer.py
  (box scores)      (archetypes + skill      (7-dimension
                      vectors)                 lineup scoring)
```

1. **Seed Data Generator**: Provides baseline box score data for 114 players across 14 teams
2. **Player Profiler**: Classifies each player into one of 8 archetypes (Floor General, Rim Protector, 3-and-D Wing, etc.) and computes a 6-dimension skill vector for radar chart visualization
3. **Lineup Scorer**: Evaluates all C(n,5) combinations per team across 7 weighted dimensions

### Scoring Model

Each 5-man lineup is scored on a 0-100 composite scale:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Offensive Efficiency | 30% | Usage-weighted ORtg with over-reliance penalty |
| Defensive Efficiency | 25% | Average DRtg with rim protection and perimeter bonuses |
| Floor Spacing | 15% | Number of capable 3-point shooters (33%+ on 20%+ rate) |
| Playmaking | 10% | Total AST% with ball-handler requirement and TOV penalty |
| Rebounding | 10% | Combined ORB%/DRB% with dominant rebounder bonus |
| Versatility | 5% | Position coverage (1-5) and height distribution |
| Balance | 5% | Usage Gini coefficient and archetype diversity |

### Web Application (Next.js)

- **Landing Page**: Team selector with top-lineup-score preview
- **Roster View**: Player cards with archetype badges, expandable skill radar charts, and key stats
- **Top Lineups Tab**: Ranked table of top 50 lineup combinations with expandable dimension breakdowns
- **Lineup Builder**: Interactive 5-player selector with real-time composite scoring and lineup profile radar

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Data Pipeline | Python 3, pandas, NumPy |
| Web Framework | Next.js 16 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Deployment | Vercel |

## Why This Is Useful to a GM / Coaching Staff

1. **Time savings**: Instantly evaluate hundreds of lineup combinations that would take hours of film review
2. **Discovery**: Surface non-obvious lineup combinations that score well -- units the staff may never have tried together
3. **Quantified tradeoffs**: See exactly what you gain and lose with each lineup swap (e.g., "swapping Player A for B gains +12 spacing but costs -8 defense")
4. **Situation prep**: Filter for lineups that excel in specific dimensions -- need a closing lineup with elite spacing? A defensive unit for late-game stops?
5. **Recruiting/portal context**: When evaluating transfers or recruits, plug them into the builder to see how they'd affect lineup quality
6. **Communication**: Provides objective language for staff discussions about rotation decisions

## Running the Project

### Data Pipeline
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

Open http://localhost:3000

## Future Enhancements

- **Live data integration**: Connect to BartTorvik or ESPN APIs for automatic data updates
- **Play-by-play lineup data**: Incorporate actual on-court +/- for lineup combinations with play-by-play data
- **Opponent-specific analysis**: Score lineups relative to a specific opponent's tendencies
- **Fatigue modeling**: Factor in minutes load and rest patterns
- **Expanded roster**: Support for all D1 teams (350+)
- **Historical tracking**: Compare lineup effectiveness across seasons
