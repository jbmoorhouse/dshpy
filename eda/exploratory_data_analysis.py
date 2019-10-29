import pandas as pd
import numpy as np

from bokeh.io import show, output_notebook
from bokeh.layouts import row, layout
from bokeh.models import ColumnDataSource, CustomJS, DataRange1d, BoxSelectTool, LassoSelectTool
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select

class EDA():
    
    output_notebook()
     
    # ----------------------------------------------------------------------
    # Constructors
    
    def __init__(self, data):
        self.data = data
    
    def _make_bivariate_dataset(self):
        df = self.data.copy()
        
        df['x'] = df.iloc[:, 0]
        df['y'] = df.iloc[:, 1]
        
        return df
    
    def _make_univariate_dataset(self, bins, density):
        df = self.data.copy()
        
        for col in df:
            hist, edges = np.histogram(df[col], bins=bins, density=density)

            yield pd.DataFrame({
                "top_" + str(col) : hist,
                "left_" + str(col) : edges[:-1],
                "right_" + str(col) : edges[1:]
            })
        
    # ----------------------------------------------------------------------
    # Plotting
    
    def bivariate_plot(self):
        df = self._make_bivariate_dataset()
        
        p = figure(
            x_range = DataRange1d(range_padding=.1), 
            y_range = DataRange1d(range_padding=0.1),
            background_fill_color = "#fafafa"
        )

        source = ColumnDataSource(df)
        p.scatter('x', 'y', source=source)
        
        def bivariate_custom_js(source, col):

            return CustomJS(
                args={'source' : source, 'col' : col}, code="""
                var data = source.data;
                data[col] = data[cb_obj.value];
                source.change.emit();
                """
            )
        
        cols = self.data.columns.tolist()
        x_select = Select(
            title = "Select x:",
            value = cols[0], 
            options = cols
        )
        y_select = Select(
            title = "Select y:", 
            value = cols[1], 
            options = cols
        )

        # Add the callback to the select widget. 
        y_select.callback = bivariate_custom_js(source = source, col='y')
        x_select.callback = bivariate_custom_js(source = source, col='x')
        
        l = layout([[x_select, y_select], [p]])
        show(l)

        
    def univariate_plot(self, bins = 25, density = True):
        concat = self._make_univariate_dataset(bins, density)
        
        # Change this to df.assign
        df = pd.concat(*[ list(concat) ], axis=1)
        df[['top', 'left', 'right']] = df.iloc[:, 0:3] 
        
        source = ColumnDataSource(df)
        p = figure(tools='', background_fill_color="#fafafa")
        
        p.quad(
            top = 'top',
            bottom=0, 
            left='left', 
            right='right', 
            source = source,
            fill_color="navy", 
            line_color="white", 
            alpha=0.5
        )
        
        def univariate_custom_js(source):
            return CustomJS(
                args={'source' : source}, code="""
                var data = source.data;
                var prefix = cb_obj.value;

                data['top'] = data['top_'.concat(prefix)];
                data['left'] = data['left_'.concat(prefix)];
                data['right'] = data['right_'.concat(prefix)];

                source.change.emit();
                """
            )
        
        cols = self.data.columns.tolist()
        x_select = Select(
            title = "Select x:", 
            value = cols[0], 
            options = cols
        )
        x_select.callback = univariate_custom_js(source = source)

        show(layout([p, x_select]))
        
        
    def scatter_matrix(self):
        pass
    
