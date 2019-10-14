import pandas as pd

class MissingDataAnalysis(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def summary(self, 
                features = None, 
                precision = 2, 
                return_missing_only = True, 
                col_name = "%_missing_data"):
        
        if isinstance(features, (list, tuple)):
            i, j = features
            
        missing = self.iloc[:, i:j].isnull().mean().to_frame() * 100
        missing.columns = [col_name]
        
        if return_missing_only:
            return missing.loc[missing[col_name] > 0]
        
        return missing.round(precision)