#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 02 17:22:09 2020, update Feb 12 10:56:00 2021 Oscar Riojas

@author: Joan-Felipe Mendoza
"""
from sys import exc_info

ERR_SYS = "System error: "


def get_series(df_input, item_name, item_col, metric, agg_cols=None, agg_func="mean"):
    """
    get_series

    Parameters
    ----------
    df_input : TYPE dataframe
        DESCRIPTION. input dataframe
    item_name : TYPE str
        DESCRIPTION.
    item_col : TYPE str
        DESCRIPTION.
    metric : TYPE str
        DESCRIPTION. metric transformation
    agg_cols : TYPE, optional
        DESCRIPTION. The default is None.
    agg_func : TYPE, optional
        DESCRIPTION. The default is 'mean'.

    Returns
    -------
    df_out : TYPE
        DESCRIPTION.

    """
    df_out = df_input.copy()
    df_out = df_out[df_out[item_col] == item_name]
    if agg_cols is not None:
        df_out = (
            df_out[agg_cols + [item_col, metric]]
            .groupby(agg_cols + [item_col])
            .agg({metric: agg_func})
        )
    return df_out


def remove_outliers(df_input, metric, method="qtl", n_sigma=3):
    """
    remove_outliers

    Parameters
    ----------
    df_input : TYPE dataframe
        DESCRIPTION. input dataframe
    metric : TYPE
        DESCRIPTION.
    method : TYPE, optional
        DESCRIPTION. The default is 'qtl'.
    n_sigma : TYPE, optional
        DESCRIPTION. The default is 3.

    Returns
    -------
    df_out : TYPE
        DESCRIPTION.

    """
    df_out = df_input.copy()
    pmin = df_out[metric].min()
    pmax = df_out[metric].max()
    df_out["outlier"] = 0
    if method == "qtl":
        q1 = df_out[metric].quantile(0.25)
        q3 = df_out[metric].quantile(0.75)
        irc = q3 - q1
        olb = max(pmin, q1 - n_sigma * irc)
        ohb = min(pmax, q3 + n_sigma * irc)
    if method == "std":
        avg = df_out[metric].mean()
        stdev = df_out[metric].std()
        olb = max(pmin, avg - n_sigma * stdev)
        ohb = min(pmax, avg + n_sigma * stdev)
    df_out.loc[df_out[metric] < olb, "outlier"] = 1
    df_out.loc[df_out[metric] > ohb, "outlier"] = 1
    df_out = df_out[df_out["outlier"] == 0]
    df_out = df_out.drop(columns=["outlier"])
    return df_out


def drop_data(df_input, metric, dr=0.01, dm="highest"):
    """
    drop_data

    Parameters
    ----------
    df_input : TYPE dataframe
        DESCRIPTION. input dataframe
    metric : TYPE
        DESCRIPTION.
    dr : TYPE, optional
        DESCRIPTION. The default is 0.01.
    dm : TYPE, optional
        DESCRIPTION. The default is 'highest'.

    Returns
    -------
    df_out : TYPE
        DESCRIPTION.

    """
    df_out = df_input.copy()
    olb, ohb = df_out[metric].min(), df_out[metric].max()
    if dm == "both":
        olb = df_out[metric].quantile(dr / 2, interpolation="midpoint")
        ohb = df_out[metric].quantile(1 - dr / 2, interpolation="midpoint")
    if dm == "lowest":
        olb = df_out[metric].quantile(dr, interpolation="midpoint")
    if dm == "highest":
        ohb = df_out[metric].quantile(1 - dr, interpolation="midpoint")
    df_out["outlier"] = 0
    df_out.loc[df_out[metric] < olb, "outlier"] = 1
    df_out.loc[df_out[metric] > ohb, "outlier"] = 1
    df_out = df_out[df_out["outlier"] == 0]
    df_out = df_out.drop(columns=["outlier"])
    return df_out


def get_boundaries(
    df_s, method="std", p_window=28, width_bound=1, metric="engagement_rate_by_day"
):
    """
    get_boundaries

    Parameters
    ----------
    df_s : TYPE
        DESCRIPTION.
    method : TYPE, optional
        DESCRIPTION. The default is 'std'.
    p_window : TYPE, optional
        DESCRIPTION. The default is 28.
    width_bound : TYPE, optional
        DESCRIPTION. The default is 1.
    metric : TYPE, optional
        DESCRIPTION. The default is 'engagement_rate_by_day'.

    Returns
    -------
    df_out : TYPE
        DESCRIPTION.

    """
    df_out = df_s.copy()  # Copy DF just for safety
    nrows = df_s.shape[0]
    if p_window < 5:
        p_window = 5
    if nrows > p_window:
        df_out["min"] = df_out[metric].rolling(p_window).min()  # Get MIN rolling column
        df_out["max"] = df_out[metric].rolling(p_window).max()  # Get MAX rolling column
    else:
        df_out["min"] = df_out[metric].min()  # Get MIN column
        df_out["max"] = df_out[metric].max()  # Get MAX column

    if method == "qtl":
        # Get QUANTILES rolling columns
        if nrows > p_window:
            df_out["q1"] = (
                df_out[metric]
                .rolling(p_window)
                .quantile(0.25, interpolation="midpoint")
            )
            df_out["q2"] = (
                df_out[metric]
                .rolling(p_window)
                .quantile(0.50, interpolation="midpoint")
            )
            df_out["q3"] = (
                df_out[metric]
                .rolling(p_window)
                .quantile(0.75, interpolation="midpoint")
            )
        else:
            df_out["q1"] = df_out[metric].quantile(0.25, interpolation="midpoint")
            df_out["q2"] = df_out[metric].quantile(0.50, interpolation="midpoint")
            df_out["q3"] = df_out[metric].quantile(0.75, interpolation="midpoint")
        df_out[["q1", "q2", "q3", "min", "max"]] = df_out[
            ["q1", "q2", "q3", "min", "max"]
        ].fillna(method="bfill")
        # df_out = df_out.dropna()
        # Get BOUNDARIES
        df_out["icr"] = df_out["q3"] - df_out["q1"]
        df_out["outer_lb"] = df_out["q1"] - 2 * width_bound * df_out["icr"]
        df_out["lb"] = df_out["q1"] - 1 * width_bound * df_out["icr"]
        df_out["hb"] = df_out["q3"] + 1 * width_bound * df_out["icr"]
        df_out["outer_hb"] = df_out["q3"] + 2 * width_bound * df_out["icr"]

    if method == "std":
        if nrows > p_window:
            df_out["mavg"] = (
                df_out[metric].rolling(p_window).mean()
            )  # Get MEAN rolling column
            df_out["mstd"] = (
                df_out[metric].rolling(p_window).std()
            )  # Get DEVIATION rolling column
        else:
            df_out["mavg"] = df_out[metric].mean()  # Get MEAN column
            df_out["mstd"] = df_out[metric].std()  # Get DEVIATION column
        df_out[["mavg", "mstd", "min", "max"]] = df_out[
            ["mavg", "mstd", "min", "max"]
        ].fillna(method="bfill")
        # df_out = df_out.dropna()
        # Get BOUNDARIES
        df_out["outer_lb"] = df_out["mavg"] - 2 * df_out["mstd"]
        df_out["lb"] = df_out["mavg"] - 1 * df_out["mstd"]
        df_out["hb"] = df_out["mavg"] + 1 * df_out["mstd"]
        df_out["outer_hb"] = df_out["mavg"] + 2 * df_out["mstd"]

    # Remove inconsistent boundary values
    df_out["outer_lb"] = df_out[["min", "outer_lb"]].max(axis=1)
    df_out["lb"] = df_out[["min", "lb"]].max(axis=1)
    df_out["hb"] = df_out[["max", "hb"]].min(axis=1)
    df_out["outer_hb"] = df_out[["max", "outer_hb"]].min(axis=1)
    df_out = df_out.drop(columns=["min", "max"])
    # Categorize each point within a boundary
    df_out["boundary"] = 0
    df_out.loc[df_out[metric] < df_out["lb"], "boundary"] = -1
    df_out.loc[df_out[metric] < df_out["outer_lb"], "boundary"] = -2
    df_out.loc[df_out[metric] > df_out["hb"], "boundary"] = 1
    df_out.loc[df_out[metric] > df_out["outer_hb"], "boundary"] = 2

    return df_out


class MetricCategorization:
    def __init__(self, df_s, metric, item_col, flag=0):
        """
        These functions deliver dataframes with categorization of metrics

        Parameters
        ----------
        df_s:
            type: Pandas DataFrame
            Pre-calculated dataframe containing all the columns required to do the expected
            categorization
        metric:
            type: str
            Name of the column in df_s containing the metric
        item_col:
            type: str
            Name of the column in df_s containing the items (i.e.: groups or brands)
        """
        self.df_s = df_s
        self.metric = metric
        self.item_col = item_col
        self.flag = flag

    def categorize(
        self, agg_cols=None, method="std", p_window=28, wb=1, dr=0, dm="highest"
    ):
        """
        Delivers a dataframe with boundary calculations and metric categorization in all rows,
        for each element of the item_col column, grouped by the item_col and agg_cols columns
        (optional).
        Parameters
        ----------
        agg_cols:
            type: list
            Names of the columns in df_s that are used as grouping elements.
            It should contain some column that is date.
        method:
            type: str
            Method to be applied to calculate the boundaries
        p_window:
            type: int
            Number of previous points to calculate the boundaries
        wb:
            type: float
            Width of boundary intervals (for a normal distribution, 1 = 1σ)
        dr:
            type: float
            Percentage of the data to be removed (between 0 and 1)
        dm:
            type: string
            Method to remove data ('lowest', 'highest' or 'both')
        Returns
            type: Pandas DataFrame
            Dataframe containing boundary calculations and metric categorization in all rows.
        -------
        """
        method_name = "categorize"
        self.df_s = self.df_s.reset_index(drop=True)

        try:
            df_woo = drop_data(self.df_s, self.metric, dr, dm)
            item_names = df_woo[self.item_col].unique().tolist()  # get item names
            # Get time series for each element in item_names
            df_ts = get_series(
                df_woo, item_names[0], self.item_col, self.metric, agg_cols
            )
            df_out = get_boundaries(df_ts, method, p_window, wb, self.metric)
            for item_name in item_names[1:]:
                df_ts = get_series(
                    df_woo, item_name, self.item_col, self.metric, agg_cols
                )
                df_temp = get_boundaries(df_ts, method, p_window, wb, self.metric)
                df_out = df_out.append(df_temp)
            rel_ef = []
            for row in range(len(df_out)):
                if df_out["mavg"].iloc[row] == 0:
                    rel_ef.append(self.flag)
                else:
                    temp_1 = (
                        100
                        * (df_out[self.metric].iloc[row] - df_out["mavg"].iloc[row])
                        / df_out["mavg"].iloc[row]
                    )
                    rel_ef.append(temp_1)
            df_out["rel_" + self.metric] = rel_ef

            return df_out.reset_index(drop=True)

        except TypeError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            return self.df_s
        except Exception as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            return self.df_s
