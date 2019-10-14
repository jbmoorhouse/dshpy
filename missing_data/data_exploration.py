import pandas as pd

class MissingDataAnalysis(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)