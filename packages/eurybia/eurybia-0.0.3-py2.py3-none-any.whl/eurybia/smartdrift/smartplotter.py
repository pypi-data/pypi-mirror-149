"""
Smart plotter module
"""

#----- Eurybia packages
from os import scandir
import copy
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly
from typing import Optional
from eurybia.report.utils import truncate_str
from eurybia.report.common import VarType, compute_col_types
from eurybia.style.style_utils import colors_loading, select_palette, define_style



class SmartPlotter:
    """
    The smartplotter class includes all the methods used to display graphics

    Each SmartPlotter method is easy to use from a Smart Drift object,
    just use the following syntax

    Attributes :


    Example
    --------
    >>> SD = Smartdrift()
    >>> SD.compile()
    >>> SD.plot.my_plot_method(param=value)

    """

    def __init__(self, smartdrift):
        self._palette_name = list(colors_loading().keys())[0]
        self._style_dict = define_style(select_palette(colors_loading(), self._palette_name))
        self.round_digit = None
        self.smartdrift = smartdrift

        


    def generate_fig_univariate(self, 
                                col: str,
                                hue: Optional[str]=None,
                                df_all: Optional[pd.DataFrame]=None, 
                                dict_color_palette: Optional[dict]=None) -> plt.Figure:
        """
        Returns a plotly figure containing the distribution of any kind of feature
        (continuous, categorical).

        If the feature is categorical and contains too many categories, the smallest
        categories are grouped into a new 'Other' category so that the graph remains
        readable.

        The input dataframe should contain the column of interest and a column that is used
        to distinguish two types of values (ex. 'train' and 'test')

        Parameters
        ----------
        df_all : pd.DataFrame
            The input dataframe that contains the column of interest
        col : str
            The column of interest
        hue : str
            The column used to distinguish the values (ex. 'train' and 'test')
        type: str
            The type of the series ('continous' or 'categorical')

        Returns
        -------
        plotly.graph_objs._figure.Figure
        """
        if hue is None:
            hue = self.smartdrift._datadrift_target
        if df_all is None:
            df_all = self.smartdrift._df_concat
            df_all.loc[df_all[hue] == 0, hue] = list(self.smartdrift.dataset_names.keys())[1]
            df_all.loc[df_all[hue] == 1, hue] = list(self.smartdrift.dataset_names.keys())[0]
        if dict_color_palette is None:
            dict_color_palette = self._style_dict
        col_types = compute_col_types(df_all=df_all)
        if col_types[col] == VarType.TYPE_NUM:
            fig = self.generate_fig_univariate_continuous(df_all, col, hue=hue, dict_color_palette=dict_color_palette)
        elif col_types[col] == VarType.TYPE_CAT:
            fig = self.generate_fig_univariate_categorical(df_all, col, hue=hue, dict_color_palette=dict_color_palette)
        else:
            raise NotImplementedError("Series dtype not supported")
        return fig


    def generate_fig_univariate_continuous(self, 
                                            df_all: pd.DataFrame, 
                                            col: str, 
                                            hue: str,
                                            dict_color_palette: dict, 
                                            template: Optional[str]=None, 
                                            title: Optional[str]=None, 
                                            xaxis_title: Optional[str]=None, 
                                            yaxis_title: Optional[str]=None, 
                                            xaxis: Optional[str]=None, 
                                            height: Optional[str]=None, 
                                            width: Optional[str]=None, 
                                            hovermode: Optional[str]=None) -> plotly.graph_objs._figure.Figure:

        """
        Returns a plotly figure containing the distribution of a continuous feature.

        Parameters
        ----------
        df_all : pd.DataFrame
            The input dataframe that contains the column of interest
        col : str 
            The column of interest
        hue : str
            The column used to distinguish the values (ex. 'train' and 'test')
        template: str, , optional
            Template (background style) for the plot
        title: str, optional
            Plot title
        xaxis_title: str, , optional
            X axis title
        yaxis_title: str, , optional
            y axis title
        xaxis: str, , optional
            X axis options (spike line, margin, range ...)
        height: str, , optional
            Height of the plot
        width: str, , optional
            Width of the plot
        hovermode: str,n , optional
            Type of labels displaying on mouse hovering
        Returns
        -------
        plotly.graph_objs._figure.Figure
        """
        df_all.loc[:, col].fillna(0, inplace=True)
        datasets = [
            df_all[df_all[hue] == val][col].values.tolist()
            for val in df_all[hue].unique()]

        fig = ff.create_distplot(datasets, 
                                group_labels=[str(val) for val in df_all[hue].unique()],
                                colors=list(self._style_dict["univariate_cont_bar"].values()),                  
                                show_hist=False,
                                show_curve=True,
                                show_rug=False)
        if template is None :
            template = self._style_dict["template"]
        if title is None :
            title = self._style_dict["dict_title"]
        if xaxis_title is None :
            xaxis_title = self._style_dict["dict_xaxis_title"]
        if yaxis_title is None:
            yaxis_title = self._style_dict["dict_yaxis_continuous"]
        if xaxis is None:
            xaxis = self._style_dict['dict_xaxis']
        if height is None:
            height = self._style_dict["height"]
        if width is None:
            width = self._style_dict["width"]
        if hovermode is None:
            hovermode = self._style_dict["hovermode"]

        fig.update_layout(template=template,
                        title=title, 
                        xaxis_title=xaxis_title, 
                        yaxis_title=yaxis_title, 
                        xaxis=xaxis, 
                        height=height, 
                        width=width,
                        hovermode=hovermode)
        fig.update_traces(hovertemplate='%{y:.2f}', showlegend=True)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        return fig


    def generate_fig_univariate_categorical(
            self,
            df_all: pd.DataFrame,
            col: str,
            hue: str,
            dict_color_palette: dict,
            nb_cat_max: int = 15,
            template: Optional[str]=None, 
            title: Optional[str]=None, 
            xaxis_title: Optional[str]=None, 
            yaxis_title: Optional[str]=None, 
            xaxis: Optional[str]=None, 
            height: Optional[str]=None, 
            width: Optional[str]=None, 
            hovermode: Optional[str]=None,
            legend: Optional[str]=None
    ) -> plotly.graph_objs._figure.Figure:
        """
        Returns a plotly figure containing the distribution of a categorical feature.

        If the feature is categorical and contains too many categories, the smallest
        categories are grouped into a new 'Other' category so that the graph remains
        readable.

        Parameters
        ----------
        df_all : pd.DataFrame
            The input dataframe that contains the column of interest
        col : str
            The column of interest
        hue : str
            The column used to distinguish the values (ex. 'train' and 'test')
        nb_cat_max : int
            The number max of categories to be displayed. If the number of categories
            is greater than nb_cat_max then groups smallest categories into a new
            'Other' category
        template: str, optional
            Template (background style) for the plot
        title: str, optional
            Plot title
        xaxis_title: str, optional
            X axis title
        yaxis_title: str, optional
            y axis title
        xaxis: str, optional
            X axis options (spike line, margin, range ...)
        height: str, optional
            Height of the plot
        width: str, optional
            Width of the plot
        hovermode: str, optional
            Type of labels displaying on mouse hovering
        legend: str, optional
            Axis legends
        Returns
        -------
        plotly.graph_objs._figure.Figure 
        """
        df_cat = df_all.groupby([col, hue]).agg({col: 'count'})\
                    .rename(columns={col: "count"}).reset_index()
        df_cat['Percent'] = df_cat['count'] * 100 / df_cat.groupby(hue)['count'].transform('sum')

        if pd.api.types.is_numeric_dtype(df_cat[col].dtype):
            df_cat = df_cat.sort_values(col, ascending=True)
            df_cat[col] = df_cat[col].astype(str)

        nb_cat = df_cat.groupby([col]).agg({'count': 'sum'}).reset_index()[col].nunique()

        if nb_cat > nb_cat_max:
            df_cat = self._merge_small_categories(df_cat=df_cat, col=col, hue=hue, nb_cat_max=nb_cat_max)

        df_to_sort = df_cat.copy().reset_index(drop=True)
        df_to_sort['Sorted_indicator'] = df_to_sort.sort_values([col]).groupby([col])['Percent'].diff()
        df_to_sort['Sorted_indicator'] = np.abs(df_to_sort['Sorted_indicator'])
        df_sorted = df_to_sort.dropna()[[col, "Sorted_indicator"]]

        df_cat = df_cat.merge(df_sorted, how="left", on=col)\
                    .sort_values("Sorted_indicator", ascending=True)\
                    .drop("Sorted_indicator", axis=1)

        df_cat["Percent_displayed"] = df_cat["Percent"].apply(lambda row : str(round(row, 2)) + " %")

        modalities = df_cat[hue].unique().tolist()

        fig1 = px.bar(
            df_cat[df_cat[hue] == modalities[0]], 
            x='Percent', 
            y=col, 
            orientation='h', 
            barmode="group", 
            color=hue, 
            text="Percent_displayed")
        fig1.update_traces(marker_color=list(self._style_dict["univariate_cat_bar"].values())[0], showlegend=True)
        
        fig2 = px.bar(
            df_cat[df_cat[hue] == modalities[1]], 
            x='Percent', y=col, 
            orientation='h', 
            barmode="group", 
            color=hue, 
            text="Percent_displayed")
        fig2.update_traces(marker_color=list(self._style_dict["univariate_cat_bar"].values())[1], showlegend=True)
        

        fig = fig1.add_trace(fig2.data[0])

        fig.update_xaxes(showgrid=False, showticklabels=True)
        fig.update_yaxes(showgrid=False, showticklabels=True, automargin=True)
        fig.update_traces( showlegend=True, textposition='outside', cliponaxis=False)

        if template == None :
            template = self._style_dict["template"]
        if title == None :
            title = self._style_dict["dict_title"]
        if xaxis_title is None :
            xaxis_title = self._style_dict["dict_xaxis_title"]
        if yaxis_title is None:
            yaxis_title = self._style_dict["dict_yaxis_continuous"]
        if height is None:
            height = self._style_dict["height"]
        if width is None:
            width = self._style_dict["width"]
        if hovermode is None:
            hovermode = self._style_dict["hovermode"]
        if legend is None:
            legend = self._style_dict["dict_legend"]


        fig.update_layout(
                template=template,
                title=title,
                xaxis_title=xaxis_title,
                height=height,
                width=width,
                yaxis_title=yaxis_title,
                hovermode=hovermode,
                legend=legend,
                xaxis_range=[0,max(df_cat["Percent"]) + 10]
            )

        return fig


    def _merge_small_categories(self,
                            df_cat: pd.DataFrame,
                            col: str,
                            hue: str,
                            nb_cat_max: int) -> pd.DataFrame:
        """
        Merges categories of column 'col' of df_cat into 'Other' category so that
        the number of categories is less than nb_cat_max.
        """
        df_cat_sum_hue = df_cat.groupby([col]).agg({'count': 'sum'}).reset_index()
        list_cat_to_merge = df_cat_sum_hue.sort_values('count', ascending=False)[
            col].to_list()[nb_cat_max - 1:]
        df_cat_other = df_cat.loc[df_cat[col].isin(list_cat_to_merge)] \
            .groupby(hue, as_index=False)[["count", "Percent"]].sum()
        df_cat_other[col] = "Other"
        return df_cat.loc[~df_cat[col].isin(list_cat_to_merge)].append(df_cat_other)


    def scatter_feature_importance(
        self,
        feature_importance: pd.DataFrame=None,
        datadrift_stat_test: pd.DataFrame=None) -> plotly.graph_objs._figure.Figure:
        """
        Displays scatter of feature importance between drift
        model and production one extracted from a datasets created
        during the compile step.

        Parameters
        ----------
        feature_importance : pd.DataFrame, optional
            DataFrame containing feature importance for each features from production and drift model.
        datadrift_stat_test: pd.DataFrame, optional
            DataFrame containing the result of datadrift univariate tests
        Returns
        -------
        plotly.express.scatter
        """  
        dict_t = copy.deepcopy(self._style_dict["dict_title"])
        dict_xaxis = copy.deepcopy(self._style_dict["dict_xaxis_title"])
        dict_yaxis = copy.deepcopy(self._style_dict["dict_yaxis_title"])
        title = f"<b>Datadrift Vs Feature Importance</b>"
        dict_t['text'] = title
        dict_xaxis['text'] = '1 - PValue Datadrift Univariate Test'
        dict_yaxis['text'] = 'Feature Importance - Deployed Model'

        if feature_importance is None:
            feature_importance = self.smartdrift.feature_importance.set_index("feature")
        if datadrift_stat_test is None:
            datadrift_stat_test = self.smartdrift.datadrift_stat_test

        data = datadrift_stat_test.join(feature_importance)
        data["1-pvalue"] = 1 - data["pvalue"]
        data["features"] = data.index
        # symbols
        stat_test_list = list(data["testname"].unique())
        symbol_list = [0, 13]
        symbol_dict = dict(zip(stat_test_list, symbol_list))

        importance_max = data["deployed_model"].max()

        hv_text = [f"<b>Feature: {feat}</b><br />Deployed Model Importance: {depimp*100:.1f}%<br />" + \
           f"Datadrift test: {t} - pvalue: {pv:.5f}<br />" + \
           f"Datadrift model Importance: {ddrimp*100:.1f}"
           for feat, depimp, t, pv, ddrimp in zip(*map(data.get, ['features','deployed_model','testname','pvalue','datadrift_classifier']))]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=data["1-pvalue"],
                y=data["deployed_model"],
                marker_symbol=datadrift_stat_test["testname"].apply(lambda x : symbol_dict[x]),
                mode='markers',
                showlegend=False,
                hovertext=hv_text,
                hovertemplate='%{hovertext}<extra></extra>'
            )
        )

        fig.update_traces(
            marker={
                'size': 15,
                'opacity': 0.8,
                'line': {'width': 0.8, 'color': 'white'}
            }
        )

        fig.add_trace(
            go.Scatter(
                x=[0.95, 0.95],
                y=[0, importance_max],
                mode="lines",
                hovertext="Datadrift threshold (1-pvalue = 0.95)",
                hoverinfo="text",
                line=dict(color=self._style_dict["scatter_line"]["vertical"], dash="dot"),
                showlegend=False,
            )
        )

        if importance_max > 0.05:
            fig.add_trace(
                go.Scatter(
                    x=[0, 1],
                    y=[0.05, 0.05],
                    mode="lines",
                    hovertext="Importance threshold (5%)",
                    hoverinfo="text",
                    line=dict(color=self._style_dict["scatter_line"]["horizontal"], dash="dot"),
                    showlegend=False,
                )
            )

        col_scale = self.tuning_colorscale(scale_name="featimportance_colorscale",values=data["datadrift_classifier"])
        fig.data[0].marker.color = data["datadrift_classifier"]
        fig.data[0].marker.coloraxis = 'coloraxis'
        fig.layout.coloraxis.colorscale = col_scale
        fig.layout.coloraxis.colorbar = {'title': {'text': "DataDrift<br />Importance"}}

        height = self._style_dict["height"]
        width = self._style_dict["width"]
        hovermode = self._style_dict["hovermode"]
        template = self._style_dict["template"]

        fig.update_layout(
            template=template,
            title=dict_t,
            xaxis_title=dict_xaxis,
            yaxis_title=dict_yaxis,
            height=height,
            width=width,
            hovermode=hovermode
        )

        return fig


    def generate_auc_historical(
        self, 
        auc_historical: pd.DataFrame=None,
        template: Optional[str]=None, 
        title: Optional[str]=None, 
        xaxis_title: Optional[str]=None, 
        yaxis_title: Optional[str]=None, 
        xaxis: Optional[str]=None, 
        height: Optional[str]=None, 
        width: Optional[str]=None, 
        hovermode: Optional[str]=None) -> plotly.graph_objs._figure.Figure:
        """
        Displays line plot of the evolution of the AUC computed
        monthly with the drift model trained with
        training dataset and current dataset during the compile step.

        Parameters
        ----------
        auc_historical : pd.DataFrame
            DataFrame containing the date associated with the computed auc at this date.
        template: str, optional 
            Template (background style) for the plot
        title: str, optional
            Plot title
        xaxis_title: str, optional
            X axis title
        yaxis_title: str, optional
            y axis title
        xaxis: str, optional
            X axis options (spike line, margin, range ...)
        height: str, optional
            Height of the plot
        width: str, optional
            Width of the plot
        hovermode: str, optional
            Type of labels displaying on mouse hovering
        Returns
        -------
        plotly.express.line
        """
        if auc_historical is None:
            auc_historical = self.smartdrift.historical_auc
        auc_historical = auc_historical[["date", "auc"]]

        auc_historical = auc_historical.groupby('date')['auc'].mean()\
                                    .reset_index()
        auc_historical.sort_values(by="date", inplace=True)

        
        auc_historical["auc_displayed"] = auc_historical["auc"].round(2)
        

        fig = px.line(auc_historical, x='date', y='auc',
                    title="AUC's Evolution of data drift classifier",
                    text="auc_displayed"
    ,                 )

        fig.update_traces(
            textposition="bottom right"
        )

        if template == None :
            template = self._style_dict["template"]
        if title == None :
            title = self._style_dict["dict_title"]
        if xaxis_title is None :
            xaxis_title = self._style_dict["dict_xaxis_title"]
        if yaxis_title is None:
            yaxis_title = self._style_dict["dict_yaxis_continuous"]
        if height is None:
            height = self._style_dict["height"]
        if width is None:
            width = self._style_dict["width"]
        if hovermode is None:
            hovermode = self._style_dict["hovermode"]

        fig.update_xaxes(showgrid=False)
        fig.update_layout(
            template=template,
            title=title,
            xaxis_title=xaxis_title,
            height=height,
            width=width,
            yaxis_title=yaxis_title,
            hovermode=hovermode
        )
        fig.data[0].line.color = self._style_dict["auc_historical"]
        fig.data[-1].marker.color = self._style_dict["auc_historical"]
        return fig

    def generate_modeldrift_data(self, 
                                data_modeldrift: pd.DataFrame=None,
                                metric: str="performance",
                                reference_columns: list=list(),
                                template: Optional[str]=None, 
                                title: Optional[str]=None, 
                                xaxis_title: Optional[str]=None, 
                                yaxis_title:Optional[str]=None, 
                                xaxis: Optional[str]=None, 
                                height: Optional[str]=None, 
                                width: Optional[str]=None, 
                                hovermode: Optional[str]=None) -> plotly.graph_objs._figure.Figure:
        """
        Displays line plot of the evolution of the Lift computed for deployed model with several criterias.

        Parameters
        ----------
        data_modeldrift : pd.DataFrame
            DataFrame containing the aggregated informations to display modeldrift.
        metric : str
            Column name of the metric computed
        reference_columns : list
            list of reference columns used to display the metric according to different criteria
        title: str, optional
            Plot title
        xaxis_title: str, optional
            X axis title
        yaxis_title: str, optional
            y axis title
        xaxis: str, optional
            X axis options (spike line, margin, range ...)
        height: str, optional
            Height of the plot
        width: str, optional
            Width of the plot
        hovermode: str, optional
            Type of labels displaying on mouse hovering
        Returns
        -------
        plotly.express.line
        """
        if data_modeldrift is None:
            data_modeldrift = self.smartdrift.data_modeldrift
            if data_modeldrift is None:
                raise Exception("""You should run the add_data_modeldrift method before displaying model drift performances.
                For more information see the documentation""")
        data_modeldrift[metric] = data_modeldrift[metric].apply(lambda row :
                                                                round(row, len([char for char 
                                                                in str(row).split(".")[1] 
                                                                if char == "0"]) + 1))

        fig = px.line(data_modeldrift, x='Date', y=metric,
                    hover_data=reference_columns,
                    title="Performance's Evolution on deployed model",
                    text=metric)

        fig.update_traces(
            textposition="top right")

        if template == None :
            template = self._style_dict["template"]
        if title == None :
            title = self._style_dict["dict_title"]
        if xaxis_title is None :
            xaxis_title = self._style_dict["dict_xaxis_title"]
        if yaxis_title is None:
            yaxis_title = self._style_dict["dict_yaxis_continuous"]
        if height is None:
            height = self._style_dict["height"]
        if width is None:
            width = self._style_dict["width"]
        if hovermode is None:
            hovermode = self._style_dict["hovermode"]

        fig.update_xaxes(showgrid=False)
        fig.update_layout(
            template=template,
            title=title,
            xaxis_title=xaxis_title ,
            height=height,
            width=width,
            yaxis_title=yaxis_title,
            hovermode=hovermode
        )

        fig.data[0].line.color = self._style_dict["auc_historical"]
        fig.data[-1].marker.color = self._style_dict["auc_historical"]
        
        return fig


    def define_style_attributes(
        self, 
        palette_name: str):
        """
        define_style_attributes allows eurybia user to change the color of plot

        Parameters
        ----------
        palette_name: string
            Name of the palette to use for each plot
        """
        palette = select_palette(colors_loading(), palette_name)
        self._palette_name = palette_name
        self._style_dict = define_style(palette)

        if hasattr(self, "pred_colorscale"):
            delattr(self, "pred_colorscale")
            
    def tuning_colorscale(
        self, 
        scale_name: str,
        values: pd.Series) -> list():
        """
        adapts the color scale to the distribution of points

        Parameters
        ----------
        scale_name: str
            name of the _style_dict scale to tune
        values: 1 column pd.Series
            values ​​whose quantiles must be calculated
        """
        desc_df = values.describe(percentiles=np.arange(0.1, 1, 0.1).tolist())
        min_pred, max_pred = list(desc_df.loc[['min', 'max']].values)
        desc_pct_df = (desc_df.loc[~desc_df.index.isin(['count', 'mean', 'std'])] - min_pred) / \
                      (max_pred - min_pred)
        color_scale = list(map(list, (zip(desc_pct_df.values.flatten(), self._style_dict[scale_name]))))
        #remove unnecessary items
        dropindex = []
        for num, x in enumerate(color_scale):
            if num > 0 and x[0] == color_scale[num-1][0]:
                dropindex.append(num)   
            dropindex = sorted(dropindex, reverse=True)
            for num in dropindex:
                color_scale.pop(num)

        return color_scale
