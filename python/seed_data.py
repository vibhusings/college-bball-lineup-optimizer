"""
Seed data for the 2024-25 college basketball season.

Uses publicly known roster/stat information for top programs.
In production, this would be replaced by a live API fetch from
BartTorvik, ESPN, or another data provider.

Stats are realistic approximations based on publicly available
2024-25 season data. Advanced metrics (ORtg, DRtg, Usage%, etc.)
are computed from basic box score stats using standard formulas.
"""

import json
import os
import random

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")

# fmt: off
TEAMS_DATA = {
    "Duke": {
        "espnId": 150,
        "conference": "ACC",
        "teamStats": {"ppg": 80.3, "opp_ppg": 67.2, "pace": 70.1},
        "players": [
            {"name": "Cooper Flagg", "pos": "PF", "ht": 81, "yr": "FR", "ppg": 18.9, "rpg": 8.3, "apg": 2.2, "spg": 1.2, "bpg": 1.3, "mpg": 33.1, "gp": 37, "fgPct": 47.5, "threePct": 35.7, "ftPct": 74.2, "fga": 13.8, "tpa": 3.1, "fta": 5.2, "tov": 2.1, "orb": 1.9, "drb": 6.4},
            {"name": "Tyrese Proctor", "pos": "PG", "ht": 77, "yr": "JR", "ppg": 12.1, "rpg": 3.4, "apg": 4.8, "spg": 0.9, "bpg": 0.2, "mpg": 31.2, "gp": 37, "fgPct": 43.2, "threePct": 37.8, "ftPct": 81.5, "fga": 10.1, "tpa": 4.5, "fta": 2.8, "tov": 2.3, "orb": 0.4, "drb": 3.0},
            {"name": "Kon Knueppel", "pos": "SG", "ht": 78, "yr": "FR", "ppg": 13.7, "rpg": 4.1, "apg": 2.5, "spg": 0.8, "bpg": 0.3, "mpg": 30.5, "gp": 37, "fgPct": 46.1, "threePct": 41.2, "ftPct": 78.6, "fga": 10.8, "tpa": 4.2, "fta": 2.4, "tov": 1.5, "orb": 0.6, "drb": 3.5},
            {"name": "Isaiah Evans", "pos": "SF", "ht": 79, "yr": "FR", "ppg": 8.2, "rpg": 3.1, "apg": 1.3, "spg": 0.7, "bpg": 0.4, "mpg": 22.8, "gp": 37, "fgPct": 42.3, "threePct": 33.9, "ftPct": 71.3, "fga": 7.2, "tpa": 2.8, "fta": 1.5, "tov": 1.1, "orb": 0.5, "drb": 2.6},
            {"name": "Maliq Brown", "pos": "PF", "ht": 80, "yr": "SO", "ppg": 7.8, "rpg": 5.2, "apg": 1.1, "spg": 0.6, "bpg": 0.8, "mpg": 22.1, "gp": 37, "fgPct": 55.4, "threePct": 20.0, "ftPct": 65.2, "fga": 5.1, "tpa": 0.3, "fta": 2.8, "tov": 1.0, "orb": 2.1, "drb": 3.1},
            {"name": "Darren Harris", "pos": "SG", "ht": 75, "yr": "SO", "ppg": 6.1, "rpg": 1.8, "apg": 1.5, "spg": 0.5, "bpg": 0.1, "mpg": 18.3, "gp": 36, "fgPct": 40.2, "threePct": 38.5, "ftPct": 83.1, "fga": 5.5, "tpa": 3.2, "fta": 1.0, "tov": 0.8, "orb": 0.2, "drb": 1.6},
            {"name": "Mason Gillis", "pos": "PF", "ht": 78, "yr": "SR", "ppg": 5.9, "rpg": 3.8, "apg": 1.2, "spg": 0.4, "bpg": 0.3, "mpg": 17.5, "gp": 35, "fgPct": 48.3, "threePct": 36.2, "ftPct": 70.5, "fga": 4.4, "tpa": 1.6, "fta": 1.3, "tov": 0.7, "orb": 1.0, "drb": 2.8},
            {"name": "Sion James", "pos": "SG", "ht": 76, "yr": "SR", "ppg": 5.5, "rpg": 2.9, "apg": 2.1, "spg": 0.8, "bpg": 0.2, "mpg": 20.4, "gp": 36, "fgPct": 44.1, "threePct": 34.5, "ftPct": 76.8, "fga": 4.8, "tpa": 1.8, "fta": 1.2, "tov": 1.0, "orb": 0.4, "drb": 2.5},
            {"name": "Patrick Ngongba II", "pos": "C", "ht": 83, "yr": "FR", "ppg": 4.2, "rpg": 4.1, "apg": 0.5, "spg": 0.3, "bpg": 1.5, "mpg": 14.8, "gp": 34, "fgPct": 58.2, "threePct": 0.0, "ftPct": 55.3, "fga": 2.8, "tpa": 0.0, "fta": 1.8, "tov": 0.6, "orb": 1.8, "drb": 2.3},
            {"name": "Christian Reeves", "pos": "C", "ht": 85, "yr": "SO", "ppg": 3.8, "rpg": 2.5, "apg": 0.3, "spg": 0.1, "bpg": 1.2, "mpg": 11.2, "gp": 33, "fgPct": 62.1, "threePct": 0.0, "ftPct": 60.5, "fga": 2.2, "tpa": 0.0, "fta": 1.5, "tov": 0.5, "orb": 1.1, "drb": 1.4},
        ],
    },
    "Auburn": {
        "espnId": 2,
        "conference": "SEC",
        "teamStats": {"ppg": 79.1, "opp_ppg": 64.8, "pace": 68.5},
        "players": [
            {"name": "Johni Broome", "pos": "C", "ht": 82, "yr": "SR", "ppg": 18.2, "rpg": 10.8, "apg": 3.2, "spg": 0.9, "bpg": 2.3, "mpg": 30.5, "gp": 36, "fgPct": 52.8, "threePct": 28.6, "ftPct": 72.1, "fga": 12.5, "tpa": 0.8, "fta": 6.2, "tov": 2.4, "orb": 3.2, "drb": 7.6},
            {"name": "Chad Baker-Mazara", "pos": "SF", "ht": 78, "yr": "JR", "ppg": 12.4, "rpg": 4.2, "apg": 1.5, "spg": 1.1, "bpg": 0.4, "mpg": 28.3, "gp": 36, "fgPct": 44.7, "threePct": 38.2, "ftPct": 79.5, "fga": 10.1, "tpa": 4.5, "fta": 2.1, "tov": 1.3, "orb": 0.6, "drb": 3.6},
            {"name": "Miles Kelly", "pos": "SG", "ht": 76, "yr": "SR", "ppg": 11.8, "rpg": 3.1, "apg": 2.3, "spg": 0.8, "bpg": 0.2, "mpg": 27.1, "gp": 36, "fgPct": 43.5, "threePct": 39.1, "ftPct": 85.2, "fga": 9.8, "tpa": 4.8, "fta": 2.0, "tov": 1.5, "orb": 0.3, "drb": 2.8},
            {"name": "Denver Jones", "pos": "PG", "ht": 73, "yr": "JR", "ppg": 10.5, "rpg": 2.8, "apg": 4.5, "spg": 1.5, "bpg": 0.1, "mpg": 29.8, "gp": 36, "fgPct": 41.2, "threePct": 32.5, "ftPct": 78.3, "fga": 8.9, "tpa": 3.2, "fta": 3.1, "tov": 2.0, "orb": 0.4, "drb": 2.4},
            {"name": "Dylan Cardwell", "pos": "C", "ht": 84, "yr": "SR", "ppg": 8.1, "rpg": 5.5, "apg": 0.8, "spg": 0.5, "bpg": 1.8, "mpg": 20.2, "gp": 35, "fgPct": 61.5, "threePct": 0.0, "ftPct": 58.2, "fga": 4.8, "tpa": 0.0, "fta": 3.5, "tov": 1.0, "orb": 2.5, "drb": 3.0},
            {"name": "Tahaad Pettiford", "pos": "PG", "ht": 72, "yr": "SO", "ppg": 7.2, "rpg": 1.9, "apg": 3.1, "spg": 0.7, "bpg": 0.1, "mpg": 18.5, "gp": 34, "fgPct": 42.8, "threePct": 35.8, "ftPct": 82.1, "fga": 6.2, "tpa": 2.5, "fta": 1.8, "tov": 1.2, "orb": 0.2, "drb": 1.7},
            {"name": "Chaney Johnson", "pos": "PF", "ht": 80, "yr": "FR", "ppg": 5.8, "rpg": 4.5, "apg": 0.8, "spg": 0.4, "bpg": 0.5, "mpg": 16.8, "gp": 35, "fgPct": 50.2, "threePct": 31.5, "ftPct": 68.5, "fga": 4.2, "tpa": 1.2, "fta": 1.5, "tov": 0.8, "orb": 1.5, "drb": 3.0},
            {"name": "Jaylin Williams", "pos": "SF", "ht": 77, "yr": "SR", "ppg": 5.2, "rpg": 2.8, "apg": 1.2, "spg": 0.6, "bpg": 0.3, "mpg": 17.5, "gp": 33, "fgPct": 43.5, "threePct": 36.2, "ftPct": 75.0, "fga": 4.5, "tpa": 2.0, "fta": 0.8, "tov": 0.7, "orb": 0.4, "drb": 2.4},
        ],
    },
    "Houston": {
        "espnId": 248,
        "conference": "Big 12",
        "teamStats": {"ppg": 74.8, "opp_ppg": 58.2, "pace": 65.8},
        "players": [
            {"name": "LJ Cryer", "pos": "SG", "ht": 73, "yr": "SR", "ppg": 15.2, "rpg": 2.8, "apg": 2.1, "spg": 0.8, "bpg": 0.1, "mpg": 31.5, "gp": 35, "fgPct": 44.8, "threePct": 39.5, "ftPct": 88.2, "fga": 12.5, "tpa": 6.2, "fta": 3.1, "tov": 1.5, "orb": 0.3, "drb": 2.5},
            {"name": "J'Wan Roberts", "pos": "PF", "ht": 80, "yr": "SR", "ppg": 12.8, "rpg": 8.1, "apg": 1.5, "spg": 0.7, "bpg": 0.9, "mpg": 29.8, "gp": 35, "fgPct": 54.2, "threePct": 22.5, "ftPct": 68.5, "fga": 8.8, "tpa": 0.5, "fta": 4.8, "tov": 1.8, "orb": 2.8, "drb": 5.3},
            {"name": "Emanuel Sharp", "pos": "SG", "ht": 75, "yr": "JR", "ppg": 11.5, "rpg": 3.2, "apg": 2.5, "spg": 1.2, "bpg": 0.3, "mpg": 28.5, "gp": 35, "fgPct": 43.1, "threePct": 37.8, "ftPct": 82.5, "fga": 9.5, "tpa": 4.8, "fta": 2.2, "tov": 1.3, "orb": 0.4, "drb": 2.8},
            {"name": "Milos Uzan", "pos": "PG", "ht": 74, "yr": "JR", "ppg": 9.8, "rpg": 3.5, "apg": 5.2, "spg": 1.5, "bpg": 0.2, "mpg": 30.2, "gp": 35, "fgPct": 41.5, "threePct": 33.2, "ftPct": 75.8, "fga": 8.2, "tpa": 2.8, "fta": 3.5, "tov": 2.5, "orb": 0.5, "drb": 3.0},
            {"name": "Ja'vier Francis", "pos": "C", "ht": 83, "yr": "JR", "ppg": 8.5, "rpg": 5.8, "apg": 0.8, "spg": 0.5, "bpg": 2.1, "mpg": 24.5, "gp": 34, "fgPct": 58.5, "threePct": 0.0, "ftPct": 62.3, "fga": 5.2, "tpa": 0.0, "fta": 3.2, "tov": 1.2, "orb": 2.2, "drb": 3.6},
            {"name": "Terrance Arceneaux", "pos": "SF", "ht": 77, "yr": "JR", "ppg": 7.2, "rpg": 3.5, "apg": 1.2, "spg": 0.8, "bpg": 0.4, "mpg": 21.8, "gp": 34, "fgPct": 45.2, "threePct": 35.5, "ftPct": 72.1, "fga": 5.8, "tpa": 2.2, "fta": 1.5, "tov": 0.8, "orb": 0.6, "drb": 2.9},
            {"name": "Joseph Tugler", "pos": "C", "ht": 82, "yr": "SO", "ppg": 5.8, "rpg": 4.2, "apg": 0.5, "spg": 0.3, "bpg": 1.5, "mpg": 16.2, "gp": 33, "fgPct": 55.8, "threePct": 0.0, "ftPct": 58.5, "fga": 3.8, "tpa": 0.0, "fta": 2.5, "tov": 0.8, "orb": 1.8, "drb": 2.4},
            {"name": "Mylik Wilson", "pos": "SG", "ht": 74, "yr": "SO", "ppg": 4.5, "rpg": 1.8, "apg": 1.5, "spg": 0.6, "bpg": 0.1, "mpg": 14.8, "gp": 32, "fgPct": 38.5, "threePct": 34.2, "ftPct": 78.5, "fga": 4.2, "tpa": 2.5, "fta": 0.8, "tov": 0.7, "orb": 0.2, "drb": 1.6},
        ],
    },
    "Tennessee": {
        "espnId": 2633,
        "conference": "SEC",
        "teamStats": {"ppg": 76.5, "opp_ppg": 62.1, "pace": 66.8},
        "players": [
            {"name": "Chaz Lanier", "pos": "SG", "ht": 76, "yr": "SR", "ppg": 16.8, "rpg": 3.5, "apg": 1.8, "spg": 0.7, "bpg": 0.2, "mpg": 31.8, "gp": 37, "fgPct": 44.2, "threePct": 40.5, "ftPct": 86.2, "fga": 13.2, "tpa": 6.8, "fta": 3.2, "tov": 1.2, "orb": 0.5, "drb": 3.0},
            {"name": "Zakai Zeigler", "pos": "PG", "ht": 69, "yr": "SR", "ppg": 13.5, "rpg": 3.2, "apg": 5.8, "spg": 1.8, "bpg": 0.1, "mpg": 32.5, "gp": 37, "fgPct": 42.5, "threePct": 35.8, "ftPct": 82.5, "fga": 10.8, "tpa": 4.5, "fta": 4.2, "tov": 2.5, "orb": 0.4, "drb": 2.8},
            {"name": "Igor Milicic Jr", "pos": "PF", "ht": 82, "yr": "JR", "ppg": 10.5, "rpg": 6.2, "apg": 1.5, "spg": 0.5, "bpg": 0.8, "mpg": 27.5, "gp": 37, "fgPct": 50.2, "threePct": 34.5, "ftPct": 70.2, "fga": 7.8, "tpa": 1.8, "fta": 3.1, "tov": 1.5, "orb": 1.8, "drb": 4.4},
            {"name": "Jordan Gainey", "pos": "SG", "ht": 74, "yr": "JR", "ppg": 9.8, "rpg": 2.5, "apg": 2.2, "spg": 0.9, "bpg": 0.2, "mpg": 25.8, "gp": 36, "fgPct": 43.8, "threePct": 37.2, "ftPct": 80.5, "fga": 8.2, "tpa": 3.5, "fta": 2.1, "tov": 1.0, "orb": 0.3, "drb": 2.2},
            {"name": "Felix Okpara", "pos": "C", "ht": 83, "yr": "JR", "ppg": 7.5, "rpg": 6.8, "apg": 0.8, "spg": 0.5, "bpg": 2.5, "mpg": 24.2, "gp": 37, "fgPct": 62.5, "threePct": 0.0, "ftPct": 55.8, "fga": 4.5, "tpa": 0.0, "fta": 3.5, "tov": 1.0, "orb": 2.5, "drb": 4.3},
            {"name": "Jahmai Mashack", "pos": "SF", "ht": 77, "yr": "SR", "ppg": 6.8, "rpg": 3.8, "apg": 1.8, "spg": 1.5, "bpg": 0.5, "mpg": 26.5, "gp": 37, "fgPct": 46.2, "threePct": 32.5, "ftPct": 68.5, "fga": 5.5, "tpa": 1.5, "fta": 1.8, "tov": 1.2, "orb": 0.8, "drb": 3.0},
            {"name": "Cade Phillips", "pos": "PF", "ht": 81, "yr": "SO", "ppg": 5.2, "rpg": 4.1, "apg": 0.5, "spg": 0.3, "bpg": 0.8, "mpg": 16.8, "gp": 35, "fgPct": 52.5, "threePct": 28.5, "ftPct": 62.5, "fga": 3.8, "tpa": 0.5, "fta": 1.5, "tov": 0.6, "orb": 1.2, "drb": 2.9},
            {"name": "Darlinstone Dubar", "pos": "SF", "ht": 78, "yr": "SO", "ppg": 4.8, "rpg": 2.2, "apg": 0.8, "spg": 0.4, "bpg": 0.2, "mpg": 14.5, "gp": 34, "fgPct": 41.5, "threePct": 35.2, "ftPct": 75.5, "fga": 4.2, "tpa": 2.2, "fta": 0.8, "tov": 0.5, "orb": 0.3, "drb": 1.9},
        ],
    },
    "Florida": {
        "espnId": 57,
        "conference": "SEC",
        "teamStats": {"ppg": 82.1, "opp_ppg": 66.5, "pace": 71.2},
        "players": [
            {"name": "Walter Clayton Jr", "pos": "PG", "ht": 74, "yr": "SR", "ppg": 17.8, "rpg": 3.2, "apg": 4.2, "spg": 1.0, "bpg": 0.2, "mpg": 33.5, "gp": 36, "fgPct": 44.5, "threePct": 38.2, "ftPct": 88.5, "fga": 14.2, "tpa": 6.5, "fta": 4.8, "tov": 2.2, "orb": 0.3, "drb": 2.9},
            {"name": "Alijah Martin", "pos": "SG", "ht": 76, "yr": "SR", "ppg": 14.2, "rpg": 4.5, "apg": 2.5, "spg": 1.2, "bpg": 0.3, "mpg": 32.1, "gp": 36, "fgPct": 45.8, "threePct": 36.5, "ftPct": 79.8, "fga": 11.5, "tpa": 4.8, "fta": 3.2, "tov": 1.5, "orb": 0.8, "drb": 3.7},
            {"name": "Alex Condon", "pos": "C", "ht": 83, "yr": "SO", "ppg": 12.5, "rpg": 7.8, "apg": 1.2, "spg": 0.5, "bpg": 1.8, "mpg": 28.5, "gp": 36, "fgPct": 52.8, "threePct": 32.5, "ftPct": 72.5, "fga": 8.8, "tpa": 1.5, "fta": 3.8, "tov": 1.8, "orb": 2.2, "drb": 5.6},
            {"name": "Will Richard", "pos": "SF", "ht": 77, "yr": "SR", "ppg": 11.8, "rpg": 4.2, "apg": 2.2, "spg": 0.8, "bpg": 0.4, "mpg": 29.8, "gp": 36, "fgPct": 46.2, "threePct": 34.8, "ftPct": 78.2, "fga": 9.5, "tpa": 3.2, "fta": 2.5, "tov": 1.2, "orb": 0.6, "drb": 3.6},
            {"name": "Rueben Chinyelu", "pos": "PF", "ht": 81, "yr": "SO", "ppg": 7.5, "rpg": 5.5, "apg": 0.8, "spg": 0.4, "bpg": 1.2, "mpg": 22.5, "gp": 35, "fgPct": 55.2, "threePct": 25.0, "ftPct": 62.5, "fga": 5.2, "tpa": 0.3, "fta": 2.8, "tov": 1.0, "orb": 2.0, "drb": 3.5},
            {"name": "Sam Hass", "pos": "PF", "ht": 82, "yr": "SR", "ppg": 5.8, "rpg": 3.8, "apg": 0.5, "spg": 0.3, "bpg": 0.5, "mpg": 16.2, "gp": 34, "fgPct": 50.5, "threePct": 35.2, "ftPct": 72.5, "fga": 4.2, "tpa": 1.5, "fta": 1.2, "tov": 0.5, "orb": 1.0, "drb": 2.8},
            {"name": "Denzel Aberdeen", "pos": "SG", "ht": 75, "yr": "SO", "ppg": 5.2, "rpg": 1.8, "apg": 1.5, "spg": 0.5, "bpg": 0.1, "mpg": 15.8, "gp": 33, "fgPct": 40.2, "threePct": 38.5, "ftPct": 82.5, "fga": 4.8, "tpa": 3.2, "fta": 0.8, "tov": 0.6, "orb": 0.2, "drb": 1.6},
            {"name": "Zyon Pullin", "pos": "PG", "ht": 73, "yr": "FR", "ppg": 4.5, "rpg": 1.5, "apg": 2.8, "spg": 0.8, "bpg": 0.1, "mpg": 14.2, "gp": 32, "fgPct": 38.5, "threePct": 32.5, "ftPct": 75.5, "fga": 4.2, "tpa": 2.0, "fta": 1.2, "tov": 1.0, "orb": 0.2, "drb": 1.3},
        ],
    },
    "UConn": {
        "espnId": 41,
        "conference": "Big East",
        "teamStats": {"ppg": 78.5, "opp_ppg": 65.8, "pace": 69.5},
        "players": [
            {"name": "Alex Karaban", "pos": "PF", "ht": 82, "yr": "SR", "ppg": 15.8, "rpg": 6.2, "apg": 2.5, "spg": 0.8, "bpg": 1.2, "mpg": 33.2, "gp": 34, "fgPct": 47.5, "threePct": 37.2, "ftPct": 78.5, "fga": 11.5, "tpa": 3.8, "fta": 3.5, "tov": 1.8, "orb": 1.2, "drb": 5.0},
            {"name": "Liam McNeeley", "pos": "SF", "ht": 79, "yr": "FR", "ppg": 14.2, "rpg": 5.5, "apg": 2.2, "spg": 0.7, "bpg": 0.5, "mpg": 31.5, "gp": 34, "fgPct": 44.8, "threePct": 38.5, "ftPct": 80.2, "fga": 11.8, "tpa": 5.2, "fta": 2.8, "tov": 1.5, "orb": 0.8, "drb": 4.7},
            {"name": "Hassan Diarra", "pos": "PG", "ht": 72, "yr": "SR", "ppg": 11.8, "rpg": 2.5, "apg": 4.8, "spg": 1.2, "bpg": 0.1, "mpg": 30.8, "gp": 34, "fgPct": 42.5, "threePct": 35.2, "ftPct": 82.5, "fga": 9.8, "tpa": 3.8, "fta": 3.5, "tov": 2.2, "orb": 0.3, "drb": 2.2},
            {"name": "Solo Ball", "pos": "SG", "ht": 76, "yr": "FR", "ppg": 10.5, "rpg": 3.2, "apg": 2.8, "spg": 0.8, "bpg": 0.2, "mpg": 27.5, "gp": 33, "fgPct": 43.2, "threePct": 36.8, "ftPct": 78.5, "fga": 8.8, "tpa": 3.5, "fta": 2.2, "tov": 1.5, "orb": 0.4, "drb": 2.8},
            {"name": "Tarris Reed Jr", "pos": "C", "ht": 82, "yr": "JR", "ppg": 9.8, "rpg": 7.2, "apg": 0.8, "spg": 0.4, "bpg": 1.5, "mpg": 25.8, "gp": 34, "fgPct": 56.2, "threePct": 20.0, "ftPct": 68.5, "fga": 6.5, "tpa": 0.2, "fta": 3.8, "tov": 1.2, "orb": 2.5, "drb": 4.7},
            {"name": "Jaylin Stewart", "pos": "SF", "ht": 78, "yr": "FR", "ppg": 6.8, "rpg": 3.2, "apg": 1.2, "spg": 0.6, "bpg": 0.3, "mpg": 20.5, "gp": 32, "fgPct": 42.8, "threePct": 34.5, "ftPct": 72.5, "fga": 5.8, "tpa": 2.5, "fta": 1.2, "tov": 0.8, "orb": 0.5, "drb": 2.7},
            {"name": "Samson Johnson", "pos": "PF", "ht": 83, "yr": "JR", "ppg": 5.5, "rpg": 4.5, "apg": 0.5, "spg": 0.3, "bpg": 1.8, "mpg": 18.2, "gp": 33, "fgPct": 54.5, "threePct": 18.0, "ftPct": 62.5, "fga": 3.8, "tpa": 0.2, "fta": 2.2, "tov": 0.8, "orb": 1.8, "drb": 2.7},
            {"name": "Aidan Mahaney", "pos": "SG", "ht": 74, "yr": "JR", "ppg": 4.5, "rpg": 1.5, "apg": 1.8, "spg": 0.5, "bpg": 0.1, "mpg": 15.2, "gp": 30, "fgPct": 38.5, "threePct": 33.5, "ftPct": 80.5, "fga": 4.5, "tpa": 2.8, "fta": 1.0, "tov": 0.6, "orb": 0.2, "drb": 1.3},
        ],
    },
    "Kansas": {
        "espnId": 2305,
        "conference": "Big 12",
        "teamStats": {"ppg": 77.8, "opp_ppg": 67.5, "pace": 68.2},
        "players": [
            {"name": "Hunter Dickinson", "pos": "C", "ht": 85, "yr": "SR", "ppg": 16.5, "rpg": 9.2, "apg": 2.2, "spg": 0.5, "bpg": 1.5, "mpg": 31.8, "gp": 35, "fgPct": 51.2, "threePct": 35.5, "ftPct": 72.8, "fga": 11.8, "tpa": 2.2, "fta": 5.5, "tov": 2.0, "orb": 2.8, "drb": 6.4},
            {"name": "KJ Adams Jr", "pos": "PF", "ht": 79, "yr": "SR", "ppg": 13.2, "rpg": 5.5, "apg": 2.5, "spg": 0.8, "bpg": 0.8, "mpg": 30.5, "gp": 35, "fgPct": 52.5, "threePct": 28.5, "ftPct": 68.5, "fga": 9.2, "tpa": 0.5, "fta": 4.2, "tov": 1.5, "orb": 1.5, "drb": 4.0},
            {"name": "Dajuan Harris Jr", "pos": "PG", "ht": 73, "yr": "SR", "ppg": 10.8, "rpg": 3.1, "apg": 5.5, "spg": 1.5, "bpg": 0.2, "mpg": 32.5, "gp": 35, "fgPct": 42.8, "threePct": 34.2, "ftPct": 78.5, "fga": 8.5, "tpa": 3.5, "fta": 2.8, "tov": 2.2, "orb": 0.3, "drb": 2.8},
            {"name": "Zeke Mayo", "pos": "SG", "ht": 75, "yr": "JR", "ppg": 12.5, "rpg": 3.2, "apg": 2.8, "spg": 0.9, "bpg": 0.2, "mpg": 29.8, "gp": 35, "fgPct": 43.5, "threePct": 36.8, "ftPct": 82.5, "fga": 10.8, "tpa": 4.8, "fta": 2.5, "tov": 1.5, "orb": 0.4, "drb": 2.8},
            {"name": "Rylan Griffen", "pos": "SF", "ht": 76, "yr": "JR", "ppg": 8.8, "rpg": 2.8, "apg": 1.2, "spg": 0.6, "bpg": 0.2, "mpg": 24.5, "gp": 34, "fgPct": 41.2, "threePct": 35.5, "ftPct": 78.2, "fga": 7.5, "tpa": 3.5, "fta": 1.5, "tov": 0.8, "orb": 0.3, "drb": 2.5},
            {"name": "Flory Bidunga", "pos": "C", "ht": 82, "yr": "FR", "ppg": 5.8, "rpg": 5.5, "apg": 0.5, "spg": 0.4, "bpg": 2.2, "mpg": 18.2, "gp": 33, "fgPct": 62.5, "threePct": 0.0, "ftPct": 55.5, "fga": 3.5, "tpa": 0.0, "fta": 2.8, "tov": 0.8, "orb": 2.2, "drb": 3.3},
            {"name": "AJ Storr", "pos": "SF", "ht": 78, "yr": "JR", "ppg": 5.5, "rpg": 2.5, "apg": 1.0, "spg": 0.5, "bpg": 0.3, "mpg": 17.8, "gp": 32, "fgPct": 42.8, "threePct": 33.5, "ftPct": 72.5, "fga": 5.2, "tpa": 2.2, "fta": 1.2, "tov": 0.6, "orb": 0.3, "drb": 2.2},
            {"name": "Shakeel Moore", "pos": "PG", "ht": 73, "yr": "SR", "ppg": 4.2, "rpg": 1.8, "apg": 2.5, "spg": 0.8, "bpg": 0.1, "mpg": 14.5, "gp": 31, "fgPct": 40.5, "threePct": 30.2, "ftPct": 75.5, "fga": 3.8, "tpa": 1.5, "fta": 1.0, "tov": 1.0, "orb": 0.2, "drb": 1.6},
        ],
    },
    "Purdue": {
        "espnId": 2509,
        "conference": "Big Ten",
        "teamStats": {"ppg": 75.2, "opp_ppg": 64.5, "pace": 66.5},
        "players": [
            {"name": "Trey Kaufman-Renn", "pos": "C", "ht": 82, "yr": "JR", "ppg": 17.2, "rpg": 7.8, "apg": 2.2, "spg": 0.4, "bpg": 0.8, "mpg": 31.5, "gp": 35, "fgPct": 55.8, "threePct": 30.5, "ftPct": 78.5, "fga": 11.2, "tpa": 1.2, "fta": 5.8, "tov": 2.0, "orb": 2.2, "drb": 5.6},
            {"name": "Braden Smith", "pos": "PG", "ht": 73, "yr": "JR", "ppg": 13.5, "rpg": 4.8, "apg": 6.2, "spg": 1.2, "bpg": 0.2, "mpg": 34.5, "gp": 35, "fgPct": 44.2, "threePct": 36.8, "ftPct": 75.5, "fga": 10.5, "tpa": 3.8, "fta": 3.2, "tov": 2.5, "orb": 0.5, "drb": 4.3},
            {"name": "Fletcher Loyer", "pos": "SG", "ht": 74, "yr": "JR", "ppg": 12.8, "rpg": 2.2, "apg": 2.5, "spg": 0.5, "bpg": 0.1, "mpg": 30.2, "gp": 35, "fgPct": 43.5, "threePct": 40.2, "ftPct": 88.5, "fga": 10.8, "tpa": 5.8, "fta": 2.5, "tov": 1.2, "orb": 0.2, "drb": 2.0},
            {"name": "CJ Cox", "pos": "SG", "ht": 75, "yr": "SO", "ppg": 8.2, "rpg": 2.5, "apg": 1.8, "spg": 0.6, "bpg": 0.2, "mpg": 22.5, "gp": 34, "fgPct": 42.8, "threePct": 37.5, "ftPct": 80.2, "fga": 7.2, "tpa": 3.5, "fta": 1.5, "tov": 0.8, "orb": 0.3, "drb": 2.2},
            {"name": "Camden Heide", "pos": "SF", "ht": 79, "yr": "SO", "ppg": 6.8, "rpg": 4.2, "apg": 1.2, "spg": 0.5, "bpg": 0.5, "mpg": 23.8, "gp": 34, "fgPct": 48.5, "threePct": 33.2, "ftPct": 70.5, "fga": 5.5, "tpa": 1.5, "fta": 2.0, "tov": 0.8, "orb": 1.2, "drb": 3.0},
            {"name": "Daniel Jacobsen", "pos": "C", "ht": 85, "yr": "FR", "ppg": 5.5, "rpg": 3.8, "apg": 0.5, "spg": 0.2, "bpg": 1.5, "mpg": 16.5, "gp": 33, "fgPct": 58.2, "threePct": 25.0, "ftPct": 62.5, "fga": 3.5, "tpa": 0.3, "fta": 2.2, "tov": 0.6, "orb": 1.5, "drb": 2.3},
            {"name": "Myles Colvin", "pos": "SF", "ht": 77, "yr": "SO", "ppg": 4.8, "rpg": 2.2, "apg": 0.8, "spg": 0.4, "bpg": 0.2, "mpg": 15.8, "gp": 32, "fgPct": 40.2, "threePct": 35.5, "ftPct": 75.8, "fga": 4.5, "tpa": 2.2, "fta": 0.8, "tov": 0.5, "orb": 0.3, "drb": 1.9},
            {"name": "Gicarri Harris", "pos": "SG", "ht": 76, "yr": "SO", "ppg": 4.2, "rpg": 1.8, "apg": 1.2, "spg": 0.5, "bpg": 0.1, "mpg": 14.2, "gp": 30, "fgPct": 39.5, "threePct": 34.2, "ftPct": 78.5, "fga": 4.0, "tpa": 2.0, "fta": 0.8, "tov": 0.5, "orb": 0.2, "drb": 1.6},
        ],
    },
    "Marquette": {
        "espnId": 269,
        "conference": "Big East",
        "teamStats": {"ppg": 80.2, "opp_ppg": 66.8, "pace": 69.8},
        "players": [
            {"name": "Kam Jones", "pos": "SG", "ht": 76, "yr": "SR", "ppg": 18.5, "rpg": 4.2, "apg": 5.2, "spg": 0.9, "bpg": 0.3, "mpg": 34.5, "gp": 36, "fgPct": 44.8, "threePct": 37.2, "ftPct": 82.5, "fga": 14.5, "tpa": 5.5, "fta": 4.2, "tov": 2.5, "orb": 0.5, "drb": 3.7},
            {"name": "Stevie Mitchell", "pos": "PG", "ht": 73, "yr": "SR", "ppg": 13.2, "rpg": 5.2, "apg": 4.8, "spg": 1.5, "bpg": 0.3, "mpg": 33.2, "gp": 36, "fgPct": 45.5, "threePct": 34.8, "ftPct": 76.5, "fga": 10.5, "tpa": 3.5, "fta": 3.8, "tov": 2.0, "orb": 1.0, "drb": 4.2},
            {"name": "David Joplin", "pos": "SF", "ht": 79, "yr": "SR", "ppg": 12.5, "rpg": 4.5, "apg": 1.8, "spg": 0.7, "bpg": 0.5, "mpg": 30.8, "gp": 36, "fgPct": 46.2, "threePct": 38.5, "ftPct": 80.2, "fga": 9.8, "tpa": 4.2, "fta": 2.5, "tov": 1.2, "orb": 0.6, "drb": 3.9},
            {"name": "Ben Gold", "pos": "C", "ht": 82, "yr": "FR", "ppg": 10.8, "rpg": 6.5, "apg": 1.2, "spg": 0.4, "bpg": 1.2, "mpg": 27.5, "gp": 36, "fgPct": 55.5, "threePct": 30.5, "ftPct": 72.5, "fga": 7.2, "tpa": 0.8, "fta": 3.5, "tov": 1.5, "orb": 2.2, "drb": 4.3},
            {"name": "Chase Ross", "pos": "SG", "ht": 76, "yr": "JR", "ppg": 8.5, "rpg": 3.2, "apg": 2.2, "spg": 1.2, "bpg": 0.2, "mpg": 26.5, "gp": 35, "fgPct": 42.5, "threePct": 35.8, "ftPct": 75.5, "fga": 7.5, "tpa": 3.2, "fta": 1.8, "tov": 1.0, "orb": 0.4, "drb": 2.8},
            {"name": "Tre Norman", "pos": "PG", "ht": 74, "yr": "JR", "ppg": 6.2, "rpg": 2.0, "apg": 3.5, "spg": 0.8, "bpg": 0.1, "mpg": 18.5, "gp": 34, "fgPct": 41.8, "threePct": 36.2, "ftPct": 80.5, "fga": 5.5, "tpa": 2.8, "fta": 1.2, "tov": 1.2, "orb": 0.2, "drb": 1.8},
            {"name": "Al Marroge", "pos": "PF", "ht": 81, "yr": "SO", "ppg": 5.5, "rpg": 3.8, "apg": 0.8, "spg": 0.3, "bpg": 0.5, "mpg": 16.2, "gp": 33, "fgPct": 52.8, "threePct": 28.5, "ftPct": 68.5, "fga": 3.8, "tpa": 0.5, "fta": 1.8, "tov": 0.6, "orb": 1.2, "drb": 2.6},
            {"name": "Damarius Owens", "pos": "SF", "ht": 78, "yr": "FR", "ppg": 4.5, "rpg": 2.5, "apg": 0.8, "spg": 0.4, "bpg": 0.2, "mpg": 14.2, "gp": 31, "fgPct": 40.5, "threePct": 33.2, "ftPct": 72.5, "fga": 4.2, "tpa": 2.0, "fta": 0.8, "tov": 0.5, "orb": 0.3, "drb": 2.2},
        ],
    },
    "St Johns": {
        "espnId": 2599,
        "conference": "Big East",
        "teamStats": {"ppg": 79.8, "opp_ppg": 68.2, "pace": 70.5},
        "players": [
            {"name": "RJ Luis Jr", "pos": "SF", "ht": 79, "yr": "JR", "ppg": 16.5, "rpg": 6.2, "apg": 2.2, "spg": 0.8, "bpg": 0.5, "mpg": 32.5, "gp": 35, "fgPct": 45.8, "threePct": 33.5, "ftPct": 78.5, "fga": 13.2, "tpa": 3.5, "fta": 3.8, "tov": 1.8, "orb": 1.2, "drb": 5.0},
            {"name": "Deivon Smith", "pos": "PG", "ht": 72, "yr": "SR", "ppg": 12.8, "rpg": 3.8, "apg": 6.5, "spg": 1.8, "bpg": 0.2, "mpg": 33.8, "gp": 35, "fgPct": 43.2, "threePct": 31.5, "ftPct": 75.8, "fga": 10.2, "tpa": 2.8, "fta": 3.5, "tov": 2.8, "orb": 0.5, "drb": 3.3},
            {"name": "Kadary Richmond", "pos": "SG", "ht": 76, "yr": "SR", "ppg": 13.5, "rpg": 4.5, "apg": 3.2, "spg": 1.2, "bpg": 0.3, "mpg": 31.5, "gp": 35, "fgPct": 46.5, "threePct": 35.8, "ftPct": 80.2, "fga": 10.8, "tpa": 3.8, "fta": 3.2, "tov": 1.5, "orb": 0.6, "drb": 3.9},
            {"name": "Zuby Ejiofor", "pos": "C", "ht": 82, "yr": "JR", "ppg": 11.2, "rpg": 8.5, "apg": 0.8, "spg": 0.5, "bpg": 2.0, "mpg": 28.5, "gp": 35, "fgPct": 58.5, "threePct": 0.0, "ftPct": 62.5, "fga": 7.2, "tpa": 0.0, "fta": 4.5, "tov": 1.5, "orb": 3.2, "drb": 5.3},
            {"name": "Simeon Wilcher", "pos": "SG", "ht": 75, "yr": "SO", "ppg": 8.5, "rpg": 2.8, "apg": 2.5, "spg": 0.7, "bpg": 0.2, "mpg": 24.5, "gp": 34, "fgPct": 42.8, "threePct": 36.5, "ftPct": 82.5, "fga": 7.5, "tpa": 3.5, "fta": 1.8, "tov": 1.0, "orb": 0.3, "drb": 2.5},
            {"name": "Brady Dunlap", "pos": "SF", "ht": 78, "yr": "SO", "ppg": 6.8, "rpg": 3.5, "apg": 1.0, "spg": 0.5, "bpg": 0.3, "mpg": 20.5, "gp": 33, "fgPct": 43.5, "threePct": 35.2, "ftPct": 75.5, "fga": 5.8, "tpa": 2.5, "fta": 1.2, "tov": 0.8, "orb": 0.5, "drb": 3.0},
            {"name": "Von Watts", "pos": "PG", "ht": 73, "yr": "JR", "ppg": 5.2, "rpg": 1.8, "apg": 3.2, "spg": 0.8, "bpg": 0.1, "mpg": 17.2, "gp": 32, "fgPct": 40.5, "threePct": 33.8, "ftPct": 78.5, "fga": 4.8, "tpa": 2.2, "fta": 1.0, "tov": 1.2, "orb": 0.2, "drb": 1.6},
            {"name": "Joel Soriano", "pos": "C", "ht": 83, "yr": "SR", "ppg": 4.8, "rpg": 4.2, "apg": 0.5, "spg": 0.3, "bpg": 0.8, "mpg": 14.8, "gp": 30, "fgPct": 55.2, "threePct": 0.0, "ftPct": 60.5, "fga": 3.2, "tpa": 0.0, "fta": 2.0, "tov": 0.6, "orb": 1.8, "drb": 2.4},
        ],
    },
}
# fmt: on


def compute_advanced_from_basic(p: dict, team: dict) -> dict:
    """Compute advanced metrics from basic box score stats."""
    ppg = p["ppg"]
    mpg = p["mpg"]
    fga = p["fga"]
    fta = p.get("fta", 0)
    tpa = p.get("tpa", 0)
    tov = p.get("tov", 0)
    apg = p["apg"]
    orb = p.get("orb", 0)
    drb = p.get("drb", 0)
    spg = p["spg"]
    bpg = p["bpg"]
    fg_pct = p["fgPct"] / 100
    three_pct = p["threePct"] / 100
    ft_pct = p.get("ftPct", 0) / 100

    team_stats = team["teamStats"]
    team_ppg = team_stats["ppg"]
    team_pace = team_stats["pace"]

    # Derived basic per-game estimates
    fgm = fga * fg_pct
    tpm = tpa * three_pct
    ftm = fta * ft_pct if fta > 0 else 0

    # TS% = PTS / (2 * (FGA + 0.44 * FTA))
    ts_denom = 2 * (fga + 0.44 * fta)
    ts_pct = (ppg / ts_denom * 100) if ts_denom > 0 else 0

    # eFG% = (FGM + 0.5 * 3PM) / FGA
    efg = ((fgm + 0.5 * tpm) / fga * 100) if fga > 0 else 0

    # 3PA rate
    three_rate = (tpa / fga * 100) if fga > 0 else 0

    # FT rate
    ftr = (fta / fga * 100) if fga > 0 else 0

    # Usage rate (simplified)
    poss_used = fga + 0.44 * fta + tov
    team_poss = team_pace  # possessions per game ≈ pace
    usage = 100 * (poss_used * 40) / (mpg * team_poss) if mpg > 0 and team_poss > 0 else 0
    usage = min(usage, 40)

    # AST%
    team_fgm = team_ppg * 0.38  # rough team FGM estimate
    teammate_fgm = max(team_fgm - fgm, 1)
    min_ratio = mpg / 40
    ast_pct = 100 * apg / (min_ratio * teammate_fgm) if (min_ratio * teammate_fgm) > 0 else 0
    ast_pct = min(ast_pct, 50)

    # TOV%
    tov_pct = 100 * tov / poss_used if poss_used > 0 else 0

    # Rebound rates
    team_orb = team_ppg * 0.13  # rough
    team_drb = team_ppg * 0.33  # rough
    opp_drb = 25
    opp_orb = 10
    orb_pct = 100 * orb / (min_ratio * (team_orb + opp_drb)) if min_ratio > 0 else 0
    drb_pct = 100 * drb / (min_ratio * (team_drb + opp_orb)) if min_ratio > 0 else 0

    # BLK% and STL%
    opp_fga = 58
    blk_pct = 100 * bpg / (min_ratio * opp_fga * 0.5) if min_ratio > 0 else 0
    stl_pct = 100 * spg / (min_ratio * team_poss) if min_ratio > 0 and team_poss > 0 else 0

    # ORtg (simplified)
    team_ortg = (team_ppg / team_pace) * 100 if team_pace > 0 else 105
    player_eff = ppg / max(poss_used, 0.1)
    team_eff = team_ppg / max(team_poss, 0.1)
    ortg = team_ortg * (0.4 + 0.6 * (player_eff / max(team_eff, 0.01)))
    ortg = max(85, min(128, ortg))

    # DRtg (simplified)
    opp_ppg = team_stats["opp_ppg"]
    team_drtg = (opp_ppg / team_pace) * 100 if team_pace > 0 else 95
    def_contrib = (stl_pct * 0.5 + blk_pct * 0.3 + drb_pct * 0.2) / 10
    drtg = team_drtg - def_contrib
    drtg = max(85, min(112, drtg))

    # BPM
    bpm = (ppg - team_ppg / 5) * 0.3 + (p["rpg"] - 4) * 0.2 + apg * 0.3 - tov * 0.4 + spg * 0.5 + bpg * 0.5
    bpm = max(-6, min(12, bpm))

    return {
        "ortg": round(ortg, 1),
        "drtg": round(drtg, 1),
        "usage": round(usage, 1),
        "efg": round(efg, 1),
        "ts": round(ts_pct, 1),
        "threepPct": round(p["threePct"], 1),
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
        "rpg": round(p["rpg"], 1),
        "apg": round(apg, 1),
        "spg": round(spg, 1),
        "bpg": round(bpg, 1),
        "mpg": round(mpg, 1),
        "gp": p["gp"],
        "fgPct": round(p["fgPct"], 1),
        "ftPct": round(p.get("ftPct", 0), 1),
    }


def generate_seed_data(year: int = 2025):
    """Generate seed data with advanced stats computed from basic stats."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    all_players = []
    print(f"Generating seed data for {len(TEAMS_DATA)} teams...")

    for team_name, team_info in TEAMS_DATA.items():
        for p in team_info["players"]:
            adv = compute_advanced_from_basic(p, team_info)
            player = {
                "name": p["name"],
                "team": team_name,
                "teamId": team_info["espnId"],
                "position": p["pos"],
                "heightInches": p["ht"],
                "year": p["yr"],
                "jersey": "",
                "advancedStats": adv,
            }
            all_players.append(player)

        print(f"  {team_name}: {len(team_info['players'])} players")

    output_path = os.path.join(RAW_DATA_DIR, f"players_{year}.json")
    with open(output_path, "w") as f:
        json.dump(all_players, f, indent=2)

    print(f"\nSaved {len(all_players)} players to {output_path}")
    return output_path


if __name__ == "__main__":
    generate_seed_data()
