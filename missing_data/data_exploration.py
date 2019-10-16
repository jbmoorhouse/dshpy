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
        
        
    # ----------------------------------------------------------------------
    # Public methods 
    
    def type_summary(self, start=None, stop=None):
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
        
        
    def quality_summary(self, 
                start = None,
                stop = None,
                step = None,
                precision = 2):
        
        if start:
            features = self.missing.iloc[:, start : stop : step]
        else:
            features = self.missing
        
        # summary data definitions
        data = {
            "count" : features.isnull().sum().astype(int),
            "cardinality" : features.nunique(),
            "%_missing" : (features.isnull().mean() * 100).round(2),
            "feature_type" : features.dtypes
        }
        
        return pd.DataFrame.from_dict(data)
        