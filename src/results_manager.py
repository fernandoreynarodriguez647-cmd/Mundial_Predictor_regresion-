from pathlib import Path
import pandas as pd


class ResultsManager:

    def __init__(self):

        self.file = Path("data/raw/matches_played.csv")


    def load(self):

        pass


    def save(self, df):

        pass


    def validate(self, df):

        pass


    def calculate_winners(self, df):

        pass


    def stage_completed(self, stage):

        pass


    def get_stage_matches(self, stage):

        pass