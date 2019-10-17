import seaborn as sns
import pandas as pd

class EDA():
    
    sns.set()
    
    # ----------------------------------------------------------------------
    # Constructors
    
    def __init__(self, data):
        self.data = data
        
    def _grid_shape(self, n_features, n_cols):
        """
        Defines the plot grid shape to which feature plots are assigned.

        Parameters
        ----------
        n_features : int
            Number of features intended to be plotted
        n_cols : int
            Desired number of columns in the grid plot.

        Returns
        -------
        rows : int 
            Number of rows in the grid plot.
        cols : int
            Number of cols in the grid plot.
        """

        if n_features % n_cols == 0:
            rows, cols = n_features / n_cols, n_cols
        else:
            rows, cols = (n_features // n_cols) + 1, n_cols

        return int(rows), int(cols)
    
        
    def univariate(self, features, n_cols=2, style = 'dark'):
        
        #Add logic to prevent more than 25 plots in one go
        
        if isinstance(features, str):
            features = [features]
            
        df = self.data[features]
        rows, cols = self._grid_shape(df.shape[1], n_cols)
        
        df.hist(bins = 25, figsize=(50, 15 * rows), layout=(rows, cols))
        
    
    def zero_inflated(self):
        pass