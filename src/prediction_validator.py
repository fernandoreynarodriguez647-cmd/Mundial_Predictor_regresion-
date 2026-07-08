import pandas as pd
from pathlib import Path
from src import config as cfg


def validate_predictions(stage: str, report: dict):

    official = pd.read_csv(cfg.DATA_RAW / "official_results.csv")

    official = official[official["stage"] == stage]

    rows = []

    hits = 0

    for match in report["matches"]:

        real = official[official["match_id"] == match["match_id"]]

        if real.empty:
            continue

        real = real.iloc[0]

        correct = match["predicted_winner"] == real["winner_final"]

        if correct:
            hits += 1

        rows.append({
            "match_id": match["match_id"],
            "team_a": match["team_a"],
            "team_b": match["team_b"],
            "predicted": match["predicted_winner"],
            "official": real["winner_final"],
            "correct": correct
        })

    df = pd.DataFrame(rows)

    output = cfg.DATA_PROCESSED / f"{stage}_comparison.csv"

    df.to_csv(output, index=False)

    accuracy = 0

    if len(df) > 0:
        accuracy = hits / len(df)

    summary = {
    "matches": len(df),
    "hits": hits,
    "misses": len(df) - hits,
    "accuracy": accuracy,
}

    return summary, output