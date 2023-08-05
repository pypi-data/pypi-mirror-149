#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:04:09 2020

@author: oscar
"""

from copy import deepcopy
from sys import exc_info

import pandas as pd

NEG = "page_negative_feedback_by_type_unique"
ERR_SYS = "System error: "


class NegFeedback:
    def __init__(self, df_r, lim_sdt=True, lim_sdt_p=1, lim=0):
        """
        Negative Feedback
        this function generates an alarm the moment its value goes out of limits

        Parameters
        ----------
        df_r : TYPE dataframe
            DESCRIPTION. dataframe with information from facebook insights, should
            have page_negative_feedback_by_type_unique
        lim_sdt : TYPE, boolean
            DESCRIPTION. The default is true. if the limit is the standard deviation
        lim_sdt_p : TYPE, float
            DESCRIPTION. The default is 1. standard deviation adjustment
        lim : TYPE, float
            DESCRIPTION. The default is 0. manual upper limit value if lim_sdt is false

        Returns
        -------
        None.

        """

        self.df_r = df_r
        self.lim_sdt = lim_sdt
        self.lim_sdt_p = lim_sdt_p
        self.lim = lim

    def neg_feedback(self):
        """
        Negative Feedback
        this function generates an alarm the moment its value goes out of limits

        Returns
        -------
        perf_n : TYPE string
            DESCRIPTION. higher: alarm,
            ok: expected performance
        val_neg : TYPE int
            DESCRIPTION. value page_negative_feedback_by_type_unique

        """

        df_r = deepcopy(self.df_r)
        lim_sdt = self.lim_sdt
        lim_sdt_p = self.lim_sdt_p
        lim = self.lim

        var_empty = None
        method_name = "neg_feedback"

        df_r = df_r[df_r.name == NEG]
        df_r = df_r[df_r.period == "day"]
        df_r.end_time = pd.to_datetime(df_r.end_time)

        try:
            df_group = df_r.groupby(["end_time", "name"], as_index=False).sum()
            df_mod = df_group[df_group.end_time != max(df_r.end_time)]
            df_neg = df_group[df_group.end_time == max(df_r.end_time)]
            val_neg = df_neg.value.iloc[0]

            if lim_sdt:
                lim_sup = df_mod.value.std() * lim_sdt_p
            else:
                lim_sup = lim

            if val_neg >= lim_sup:
                perf_n = "higher"
            else:
                perf_n = "ok"

        except AttributeError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            perf_n = var_empty
            val_neg = var_empty

        except IndexError as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            perf_n = var_empty
            val_neg = var_empty

        except Exception as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            perf_n = var_empty
            val_neg = var_empty

        return perf_n, val_neg
