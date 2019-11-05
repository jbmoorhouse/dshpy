import pandas as pd
import numpy as np

from itertools import product

from bokeh.io import show, output_notebook
from bokeh.layouts import row, layout, gridplot
from bokeh.models import (
    ColumnDataSource, 
    CustomJS, 
    DataRange1d, 
    BoxSelectTool, 
    LassoSelectTool
)
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Select

class EDA():
    
    output_notebook()
     
    # ----------------------------------------------------------------------
    # Constructors
    
    def __init__(self, data):
        self.data = data
    
    def _bivariate_dataset(self):
        df = self.data.copy()
        
        df['x'] = df.iloc[:, 0]
        df['y'] = df.iloc[:, 1]
        
        return df
    
    def _univariate_dataset(self, bins, density):
        df = self.data.copy()
        
        for col in df:
            hist, edges = np.histogram(df[col], bins=bins, density=density)

            yield pd.DataFrame({
                "top_" + str(col) : hist,
                "left_" + str(col) : edges[:-1],
                "right_" + str(col) : edges[1:]
            })
            
    def _scatter_matrix_dataset(self):
        pass    
        
        
    # ----------------------------------------------------------------------
    # Plotting
    
    def bivariate_plot(self):
        df = self._bivariate_dataset()
        
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
        concat = self._univariate_dataset(bins, density)
        
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
        
        
    def scatter_matrix(self, n_cols):
    
        def _make_plot(n_cols):
            df = self.data
            
            source = ColumnDataSource(
                df.assign(**{
                        'feature_{}'.format(i) : df.iloc[:, i] 
                        for i in range(n_cols)
                    }))

            grid_size = range(n_cols)
            cols = df.columns.to_list()
            cols_iterator = iter(cols)

            for i, (x, y) in enumerate(product(grid_size, grid_size)):

                p = figure(
                    x_range = DataRange1d(range_padding=0.1), 
                    y_range = DataRange1d(range_padding=0.1),
                    plot_width = 175,
                    plot_height = 175,
                    output_backend="webgl"
                )
                p.scatter(
                    'feature_{}'.format(y), 
                    'feature_{}'.format(x), 
                    source=source
                )

                #Define show axis conditions
                cond_one, cond_two = i % n_cols == 0, x == n_cols - 1

                #Add explanation for logic here
                if cond_one: 
                    p.plot_width += (p.plot_width // 4)
                    p.yaxis.axis_label = 'Feature {}'.format(x + 1)

                    if cond_two: 
                        p.plot_height += (p.plot_height // 4)
                        p.xaxis.axis_label = 'Feature {}'.format(y + 1)
                        p.xaxis.visible = True
                    else:
                        p.xaxis.visible = False

                elif cond_two:
                    p.yaxis.visible = False
                    p.xaxis.axis_label = 'Feature {}'.format(y + 1)
                    p.plot_height += (p.plot_height // 4)
                else:
                    p.yaxis.visible = p.xaxis.visible =  False

                # Remove the gridlines
                p.xgrid.grid_line_color = p.ygrid.grid_line_color = None
                
                # Remove the minor axis lines
                p.yaxis.minor_tick_line_color = None
                p.xaxis.minor_tick_line_color = None

                yield p


            for i in range(n_cols):

                select = Select(
                    value = cols[i], 
                    options=cols, 
                    width = (
                        p.plot_width + (p.plot_width // 4)
                    ) if i == 0 else p.plot_width
                )

                # Once None has been yielded for the first
                def xaxis_custom_js(source, i):
                    return CustomJS(
                        args={'source' : source, 'i' : i}, code="""
                        var data = source.data;
                        var col = i;
                        data['feature_'.concat(col)] = data[cb_obj.value];
                        source.change.emit();
                        """
                    )

                select.callback = xaxis_custom_js(source = source, i = i)

                yield select


        l = gridplot(list(_make_plot(n_cols)), ncols = n_cols)
        show(l)