#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3.6.9
Created on Tue 2020-07-31

@author: Felipe Gomez-Cortes
@gitlab: felipegomez_wj
@mail: felipeg@whaleandjaguar.co

TODO: Handling corrupted dataframe (wrong data)
TODO: Add window time for the analysis (initial date, end date)
TODO: Add max_age parameter
TODO: Make the script lexible to cover

"""

from copy import deepcopy

import numpy as np
import pandas as pd

ERR_SYS = "\nSystem error: "


class PostEngagementRateSensor:
    """
    This class computes the average performance on different features (clicks,
    normalized clicks, engagement_fb) and their derivatives (delta_feature)
    of a set of posts, and returns when some of them are deviated
    from the average with an performance indicator (good, average, poor). The
    limits of the average behavior can be manual or automaticly established.
    """

    def __init__(self, df_posts):
        """
        Generates an instance of PostEngagementRateSensor after checking the
        columns and size of the input DataFrame.

        Parameters:
        -----------
        df_posts:
            type DataFrame
            Daily update information of the posts.
            This Pandas DataFrame must have columns 'post_id',
            'created_time', 'snapshot_time', 'post_clicks' and
            'post_impressions'
        """

        METHOD_NAME = "__init__"

        EXPECTED_COLUMNS = [
            "post_id",
            "created_time",
            "snapshot_time",
            "post_clicks",
            "post_impressions",
            "post_impressions_organic",
            "post_impressions_viral",
            "post_impressions_paid",
        ]
        EXPECTED_COLUMNS.sort()

        df = df_posts.dropna()

        if len(df) > 0:
            df_columns = list(df.columns.values)
            df_columns.sort()
            EXPECTED_COLUMNS.sort()
            if df_columns != EXPECTED_COLUMNS:
                print(
                    METHOD_NAME,
                    "\nWarning: the DataFrame has not the expected columns.",
                )
        else:
            print(
                METHOD_NAME,
                "\nWarning: the DataFrames is empty. It cannot be computed.",
            )
        # TODO: handling corrupted data.
        self.df = df

    def load_sensor(self):
        """
        This function computes the normalized clicks, and the derivative (delta)
        of post_clicks, post_clicks_normalized and efficiency_fb
        """
        METHOD_NAME = "load_sensor"

        df = self.df

        try:
            # convert strings to datetime formant
            # df["created_time"] = df["created_time"].apply(lambda _: pd.to_datetime(_) )
            # df["snapshot_time"] = df["snapshot_time"].apply(lambda _ : pd.to_datetime(_))
            df.loc[:, "created_time"] = deepcopy(
                pd.to_datetime(df.loc[:, "created_time"]).copy()
            )
            df.loc[:, "snapshot_time"] = deepcopy(
                pd.to_datetime(df.loc[:, "snapshot_time"])
            )

            # sort posts with this specific order to make easier to calculate
            # derivatives
            df = df.sort_values(by=["created_time", "post_id", "snapshot_time"])

            # define maximum of clicks to normalize clicks.
            post_id_list = df.post_id.unique()
            for i in range(len(post_id_list)):
                post_id = post_id_list[i]
                index = df["post_id"] == post_id
                Y = df.loc[index, "post_clicks"]
                post_clicks_max = Y.max()
                df.loc[index, "post_clicks_max"] = post_clicks_max
            df["effectivity_fb"] = 100 * df["post_clicks"] / df["post_impressions"]
            df["post_clicks_normalized"] = df["post_clicks"] / df["post_clicks_max"]

            # Derivatives
            # computes the derivative of the feature using
            # delta_feature = ( feature_today - feature_yesterday) / 1_day
            # Requieres the dataframe sorted by "created time", "post_id" and
            # "snapshot_time" in that specific order.
            delta_clicks = []
            delta_effectivity = []
            for i in range(len(df.index)):
                idx = df.index[i]
                idx_prev = df.index[i - 1]

                # First DataFrame element, or first register of the post.
                if (i == 0) or (df.loc[idx, "post_id"] != df.loc[idx_prev, "post_id"]):
                    delta_clicks.append(np.nan)
                    delta_effectivity.append(np.nan)

                # Compute Delta if it is a regular post with today and yesterday's data.
                elif i != 0:
                    delta_clicks.append(
                        df.loc[idx, "post_clicks"] - df.loc[idx_prev, "post_clicks"]
                    )
                    delta_effectivity.append(
                        df.loc[idx, "effectivity_fb"]
                        - df.loc[idx_prev, "effectivity_fb"]
                    )

            df["delta_clicks"] = delta_clicks
            df["delta_clicks_normalized"] = df["delta_clicks"] / df["post_clicks_max"]
            df["delta_effectivity_fb"] = delta_effectivity

            df["post_age_days"] = (df["snapshot_time"] - df["created_time"]).dt.days

            self.df = df
        except Exception as e:
            print(e)
            print(METHOD_NAME)

    def time_series(self, feature="post_clicks"):
        return self.df[[feature, "post_id", "snapshot_time", "post_age_days"]]

    def performance_indicator(
        self, feature="effectivity_fb", stat="std", upp_lim=0, low_lim=0, beta=1
    ):
        """
        Parameters:
        feature: Select one feature to compute the performance. It may be one
            from the list [post_clicks, post_clicks_normalized,
            effectivity_fb, delta_post_clicks, delta_post_clicks_normalized
            delt_effectivity_fb]
        stat: Defines how to define what is the 'average performance' of a post:
            'std': using the standard deviation and a beta multiplier
            'quartiles': using the first and third quartiles
            'manual': select the limits by hand.
        beta: (float) If stat='std', selects
            upp_lim = mean + beta * standard_deviation
            low_lim = mean - beta * standard_deviation
        upp_lim: (float) manual upper limit, only if stat="manual"
        low_lim: (float) manual lower limit, only if stat="manual

        Returns:
        DataFrame with the columns:
            created_time: (datetime) Post created time
            post_age_days: (int) self explanatory
            feature: (float) the value of the feature selected by the user
            perf_upp_lim: (float) performance upper limit as defined by the user
            perf_mean. (float) Mean performance calculated for same age posts
            perf_low_lim: (float) performance lower limit as defined by the user
            performance: (str) [good, average, poor]
        """

        df = self.df
        ages = range(0, 6)  # TODO: manual selection of the age period.

        df["performance"] = "average"
        df["perf_mean"] = np.nan
        df["perf_upp_lim"] = np.nan
        df["perf_low_lim"] = np.nan

        for age in ages:
            index = df["post_age_days"] == age

            series = df.loc[index, feature]
            series_mean = series.mean()
            series_std = series.std()

            if stat == "std":
                upp_lim = series_mean + beta * series_std
                low_lim = series_mean - beta * series_std
            if stat == "quartiles":
                upp_lim = series.quantile(0.75)
                low_lim = series.quantile(0.25)

            df.loc[index, "perf_mean"] = series_mean
            df.loc[index, "perf_upp_lim"] = upp_lim
            df.loc[index, "perf_low_lim"] = low_lim

        idx = df[feature] == np.nan
        df.loc[idx, "performance"] = np.nan

        idx = df[feature] < df["perf_low_lim"]
        df.loc[idx, "performance"] = "poor"

        idx = df[feature] > df["perf_upp_lim"]
        df.loc[idx, "performance"] = "good"

        return df.loc[
            :,
            [
                "created_time",
                "post_age_days",
                feature,
                "perf_upp_lim",
                "perf_mean",
                "perf_low_lim",
                "performance",
            ],
        ]
