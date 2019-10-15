import pandas as pd

class MissingDataAnalysis():
    def __init__(self, data = None):
        self.data = data
        
    def quality_summary(self, 
                start = None,
                stop = None,
                step = None,
                precision = 2, 
                return_missing_only = True):
        
        features = self.data.iloc[:, start : stop : step]
        
        # summary data definitions
        data = {
            "count" : features.isnull().sum().astype(int),
            "cardinality" : features.nunique(),
            "%_missing" : (features.isnull().mean() * 100).round(2),
            "feature_type" : features.dtypes
        }
        
        missing = pd.DataFrame.from_dict(data)
                
        # determine if only missing values are returned in the analysis
        if return_missing_only:
            return missing.loc[missing["count"] > 0]
        else:
            return missing