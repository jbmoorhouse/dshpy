import pandas as pd


class MissingDataAnalysis():
    
    # ----------------------------------------------------------------------
    # Constructors
    
    def __init__(self, data = None):
        self.data = data
        self.missing = self._get_null(data)
        
    # ----------------------------------------------------------------------
    # Non-public methods
    
    def _get_null(self, data):
        df = data.copy()
        
        return df.loc[:, df.isnull().any()]
    
    # ----------------------------------------------------------------------
    # Properities
    
    @property
    def missing_features(self):
        f = (self.missing.shape[1] / self.data.shape[1]) * 100
        print("{}% of the features have missing data".format(int(f)))
    
    @property
    def type_summary(self):
        # pd.Series of the distribution of dtypes
        type_summary = self.missing.dtypes.value_counts()
        
        # define subplots
        fig, ax = plt.subplots(
            figsize=(10, 10), 
            subplot_kw=dict(aspect="equal")
        )

        # generate wedge pie plot 
        wedges, texts = ax.pie(
            type_summary.values, 
            wedgeprops=dict(width=0.4),
            startangle=-40
        )
        
        # define label attributes
        bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0.9)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center", fontsize=12)

        for i, p in enumerate(wedges):
            # set label arrow line angles
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            
            # determine horizontal aligment from arrow line angles
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            
            # display the annotated labels
            ax.annotate(
                [str(i) for i in type_summary.index.tolist()][i], 
                xy=(x, y), 
                xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, 
                **kw
            )

        ax.set_title("Missing data type summary", fontdict = {"fontsize":15})
        plt.show()
        
    # ----------------------------------------------------------------------
    # Public methods
    
    def quality_summary(self, 
                metric = True,
                start = None,
                stop = None,
                step = None,
                precision = 2):
            
        # Need to add logic here to check start, stop and step are valid 
        if start:
            missing = self.missing.iloc[:, start : stop : step]
        else:
            missing = self.missing
        
        # summary data definitions
        # Opted to explicitly define summary statistics as opposed to 
        # concatenating with pd.DataFrame.describe() since this is slow.
        data = {
            "count" : missing.isnull().sum().astype(int),
            "cardinality" : missing.nunique(),
            "%_missing" : (missing.isnull().mean() * 100),
            "feature_type" : missing.dtypes
        }
    
        if metric:
            missing = missing.select_dtypes(include = np.number)
            
            # define the metric summary statistics
            metric_data = {
                'minimum' : missing.min(),
                '25%' : missing.quantile(0.25),
                'mean' : missing.mean(),
                'median' : missing.median(),
                '25%' : missing.quantile(0.75),
                'max' : missing.max(),
                'std. dev.' : missing.std()
            }
            
            return pd.DataFrame({**data, **metric_data}).round(2)
    
        else:
            missing = missing.select_dtypes(exclude = np.number)
            mode = missing.mode()
            
            # define the non-metric summary statistics
            non_metric_data = {
                'mode' : mode.iloc[0],
                'mode_freq' : (missing == mode.iloc[0]).sum(),
                'mode%' : (missing == mode.iloc[0]).mean(),
                '2nd_mode' : mode.iloc[0],
                '2nd_mode_freq' : (missing == mode.iloc[1]).sum(),
                '2nd_mode%' : (missing == mode.iloc[1]).mean()
            }
        
            return pd.DataFrame({**data, **non_metric_data}).round(2)
        