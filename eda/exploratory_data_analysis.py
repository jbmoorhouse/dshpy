import seaborn as sns
import pandas as pd
from bokeh.io import show, output_notebook
from bokeh.layouts import row, layout
from bokeh.models import ColumnDataSource, CustomJS, DataRange1d, BoxSelectTool, LassoSelectTool
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select

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
    
    def bivariate_plot(self):
        df = self.data.copy()
        
        df['x'] = df.iloc[:, 0]
        df['y'] = df.iloc[:, 1]
        
        p = figure(
            x_range = DataRange1d(range_padding=.1), 
            y_range = DataRange1d(range_padding=.1),
            background_fill_color = "#fafafa"
        )
        
        source = ColumnDataSource(df)
        p.scatter('x', 'y', source=source)
        
        # Custom javascript method for updating the plot axes.
        def _custom_js(source, col):
            return CustomJS(
                args={'source' : source, 'col' : col}, code="""
                var data = source.data;
                data[col] = data[cb_obj.value];
                source.change.emit();
                """
            )
        
        # Define Select box structure
        cols = df.columns.tolist()
        
        x_select = Select(
            title = "Select x:", 
            value = cols[0], 
            options = cols[:-2]
        )
        
        y_select = Select(
            title = "Select y:", 
            value = cols[1], 
            options = cols[:-2]
        )

        # Add the callback to the select widget. 
        y_select.callback = _custom_js(source = source, col='y')
        x_select.callback = _custom_js(source = source, col='x')

        show(layout([[x_select, y_select], [p]]))
    
    def bokeh_univariate(self):
        pass