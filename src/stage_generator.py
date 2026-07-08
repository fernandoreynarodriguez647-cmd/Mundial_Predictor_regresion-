import pandas as pd
from src import config as cfg


def generate_next_stage(stage: str):

    official = pd.read_csv(cfg.DATA_RAW / "official_results.csv")

    winners = official.loc[
        official["stage"] == stage,
        ["match_id", "winner_final"]
    ]

    output = cfg.DATA_PROCESSED / f"{stage}_winners.csv"

    winners.to_csv(output, index=False)

    return output