import pandas as pd

class MissingDataAnalysis():
    def __init__(self, data):
        self.data = data
        
    def summary(self, 
                start = None,
                stop = None,
                step = None,
                precision = 2, 
                return_missing_only = True):
        
        data = self.data
        features = data.iloc[:, start : stop : step]
        
        stat_columns = ["missing_count", "%_missing", "feature_type"]
        data = np.array([
            features.isnull().sum(),
            (features.isnull().mean() * 100).round(2),
            features.dtypes
        ])
        
        missing = pd.DataFrame(data.T, columns=stat_columns)
                
        if return_missing_only:
            return missing.loc[missing["missing_count"] > 0]
        else:
            return missing