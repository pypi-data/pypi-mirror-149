#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 20:44:09 2020

@author: Joan-Felipe Mendoza
"""
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None

ERR_SYS = "System error: "


class TacTips:
    def __init__(
        self,
        df_s,
        dim,
        item_col,
        item_name,
        met="engagement_rate_by_post",
        terms_size=5,
    ):
        """
        These functions deliver tac-tips based on the content of a pre-calculated dataframe (df_s),
        considering a met (metric) and the dimension to be analyzed.

        Parameters
        ----------
        df_s:
            type: Pandas DataFrame
            Pre-calculated dataframe containing the data needed to calculate the tac-tips
            (including metrics and dimensions).
        dim:
            type: string
            Name of dimension ('hashtag', 'word', 'mention', 'most_effective_pages', 'day', 'hour')
        item_col:
            type: string
            Name of the column that contains the item_name
        item_name:
            type: string
            Name of the item to analyze (in case of group: 'trends', 'competitors', 'no_group', 'brand', 'archetypes')
        met:
            type: string
            Name of the column within df_s containing the metric.
        terms_size:
            type: integer
            Number of terms to be included within the tac-tip
            (for HT, mentions, words, or most effective pages)
        """
        self.df_s = df_s
        self.met = met
        self.terms_size = terms_size
        self.dim = dim
        self.item_col = item_col
        self.item_name = item_name

    def get_tactip_values(self):
        """
        Returns
        -------
        TYPE string
            DESCRIPTION. values for tactip message
        """
        method_name = "get_tactip_values"

        try:
            df_item = self.df_s[self.df_s[self.item_col] == self.item_name]

            if self.dim in ["hashtag", "word", "mention"]:
                terms = df_item.nlargest(self.terms_size, self.met)[self.dim].tolist()
                dim_v1 = ", ".join(terms[:-1])
                dim_v2 = terms[-1]
                return dim_v1, dim_v2

            if self.dim == "most_effective_pages":
                df_pages = (
                    df_item[["page_name", self.met]].groupby(["page_name"]).mean()
                )
                df_pages = df_pages.reset_index()
                terms = df_pages.nlargest(self.terms_size, self.met)[
                    "page_name"
                ].tolist()
                dim_v1 = ", ".join(terms[:-1])
                dim_v2 = terms[-1]
                return dim_v1, dim_v2

            if self.dim in ["day", "hour"]:
                metric_avg = df_item[self.met].mean()
                df_item["perc_diff_vs_avg"] = (
                    df_item[self.met] - metric_avg
                ) / metric_avg
                df_item["perc_diff_vs_avg"] = df_item["perc_diff_vs_avg"] * 100
                best_m, best_p, temp_1 = (
                    df_item.nlargest(1, self.met)[
                        [self.dim, self.met, "perc_diff_vs_avg"]
                    ]
                    .values[0]
                    .tolist()
                )
                max_i = int(round(temp_1, 0))
                worst_m, worst_p, temp_2 = (
                    df_item.nsmallest(1, self.met)[
                        [self.dim, self.met, "perc_diff_vs_avg"]
                    ]
                    .values[0]
                    .tolist()
                )
                min_i = int(round(temp_2, 0))
                return best_m, best_p, max_i, worst_m, worst_p, min_i

            if self.dim in ["perc_audience", "diff_audience"]:
                df_item = df_item.rename(columns={"date": self.dim})
                metric_avg = df_item[self.met].mean()
                df_item["perc_diff_vs_avg"] = (
                    df_item[self.met] - metric_avg
                ) / metric_avg
                df_item["perc_diff_vs_avg"] = df_item["perc_diff_vs_avg"] * 100
                best_m, best_p, temp_1 = (
                    df_item.nlargest(1, self.met)[
                        [self.dim, self.met, "perc_diff_vs_avg"]
                    ]
                    .values[0]
                    .tolist()
                )
                max_i = int(round(temp_1, 0))
                worst_m, worst_p, temp_2 = (
                    df_item.nsmallest(1, self.met)[
                        [self.dim, self.met, "perc_diff_vs_avg"]
                    ]
                    .values[0]
                    .tolist()
                )
                min_i = int(round(temp_2, 0))
                return best_m, best_p, max_i, worst_m, worst_p, min_i

            if self.dim in ["moment_of_day"]:
                metric_avg = df_item[self.met].mean()
                df_item["perc_diff_vs_avg"] = (
                    df_item[self.met] - metric_avg
                ) / metric_avg
                df_item["perc_diff_vs_avg"] = df_item["perc_diff_vs_avg"] * 100
                best_d, best_h, best_p, temp_1 = (
                    df_item.nlargest(1, self.met)[
                        ["day", "hour", self.met, "perc_diff_vs_avg"]
                    ]
                    .values[0]
                    .tolist()
                )
                max_i = int(round(temp_1, 0))
                worst_d, worst_h, worst_p, temp_2 = (
                    df_item.nsmallest(1, self.met)[
                        ["day", "hour", self.met, "perc_diff_vs_avg"]
                    ]
                    .values[0]
                    .tolist()
                )
                min_i = int(round(temp_2, 0))
                return best_d, best_h, best_p, max_i, worst_d, worst_h, worst_p, min_i

        except TypeError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            values = None
            if self.dim in ["hashtag", "word", "mention", "most_effective_pages"]:
                values = [None] * 2
            if self.dim in ["day", "hour", "perc_audience", "diff_audience"]:
                values = [None] * 6
            if self.dim in ["moment_of_day"]:
                values = [None] * 8
            return values

        except Exception as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            values = None
            if self.dim in ["hashtag", "word", "mention", "most_effective_pages"]:
                values = [None] * 2
            if self.dim in ["day", "hour", "perc_audience", "diff_audience"]:
                values = [None] * 6
            if self.dim in ["moment_of_day"]:
                values = [None] * 8
            return values
