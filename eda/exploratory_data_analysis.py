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
    
    def bokeh_joint_plot(self):
        output_notebook()

        boston = load_boston()
        df = pd.DataFrame(data = boston['data'], columns = boston['feature_names'])
        #df = train_df
        df['x'] = df.iloc[:, 0]
        df['y'] = df.iloc[:, 1]

        p = figure()#x_axis_location=None, y_axis_location=None,)
        p.background_fill_color = "#fafafa"
        p.y_range, p.x_range = DataRange1d(range_padding=0.1), DataRange1d(range_padding=0.1) 

        source = ColumnDataSource(df)
        p.scatter('x', 'y', source=source)

        # create the horizontal histogram
        hhist, hedges = np.histogram(source.data['x'], bins=20)
        hzeros = np.zeros(len(hedges)-1)
        hmax = max(hhist)*1.1

        LINE_ARGS = dict(color="#3A5785", line_color=None)

        ph = figure(toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
                    y_range=(-hmax/4, hmax), min_border_left=10, y_axis_location="left")
        ph.xgrid.grid_line_color = None
        ph.yaxis.major_label_orientation = np.pi/4
        ph.background_fill_color = "#fafafa"

        ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
        hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
        hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)


        # create the vertical histogram
        vhist, vedges = np.histogram(source.data['y'], bins=20)
        vzeros = np.zeros(len(vedges)-1)
        vmax = max(vhist)*1.1

        pv = figure(toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(-vmax, vmax),
                    y_range=p.y_range, min_border=10, y_axis_location="right")
        pv.ygrid.grid_line_color = None
        pv.xaxis.major_label_orientation = np.pi/4
        pv.background_fill_color = "#fafafa"

        pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white", line_color="#3A5785")
        vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
        vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)

        cols = df.columns.tolist()
        y_select = Select(title="Select y:", value = cols[0], options = cols[:-2])
        x_select = Select(title="Select x:", value = cols[1], options = cols[:-2])


        y_callback = CustomJS(args={'source':source},code="""
                var data = source.data;
                data['y'] = data[cb_obj.value];
                source.change.emit();
        """)

        x_callback = CustomJS(args={'source':source},code="""
                var data = source.data;
                data['x'] = data[cb_obj.value];
                source.change.emit();
        """)

        # Add the callback to the select widget. 
        y_select.callback = y_callback
        x_select.callback = x_callback

        layout = layout([ [y_select, x_select], [p, pv], [ph]])
        curdoc().add_root(layout)
        show(layout)
    
    def bokeh_univariate(self):
        pass