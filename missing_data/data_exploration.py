import pandas as pd

class MissingDataAnalysis():
    
    # -----------------------------------------------------------------------
    def __init__(self, data = None):
        self.data = data
        
    @property
    def type_symmary(self):
        # pd.Series of the distribution of dtypes
        type_summary = self.data.dtypes.value_counts()
        
        # define subplots
        fig, ax = plt.subplots(
            figsize=(10, 10), 
            subplot_kw=dict(aspect="equal")
        )

        # generate wedge pie plot and define label attributes
        wedges, texts = ax.pie(
            counts.values, 
            wedgeprops=dict(width=0.4), 
            startangle=-40
        )
        bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0.9)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center", fontsize=12)

        # annotate the wedges
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
            ax.annotate([str(i) for i in counts.index.tolist()][i], 
                        xy=(x, y), 
                        xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, 
                        **kw)

        ax.set_title("Data type summary", fontdict = {"fontsize" : 15})
        plt.show()
        
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