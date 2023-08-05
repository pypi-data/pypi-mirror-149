#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 09:07:01 2020

@author: oscar
"""

from copy import deepcopy
from sys import exc_info

import pandas as pd
import statsmodels.api as sm

IMP = "page_posts_impressions_paid_unique"
POS = "page_positive_feedback_by_type_unique"
ERR_SYS = "System error: "


class PerfImprPos:
    def __init__(self, df_r, lim_sdt=True, lim_sdt_p=1, lim_s=0, lim_i=0):
        """
        Impressions Performance Vs positive feedback
        this class calculates the performance of the impressions in a period,
        considering the data backwards

        Parameters
        ----------
        df_r : TYPE dataframe
            DESCRIPTION. dataframe with information from facebook insights, should
            have page_posts_impressions_paid_unique and page_positive_feedback_by_type_unique
        lim_sdt : TYPE, boolean
            DESCRIPTION. The default is true. if the limit is the standard deviation
        lim_sdt_p : TYPE, float
            DESCRIPTION. The default is 1. standard deviation adjustment
        lim_s : TYPE, float
            DESCRIPTION. The default is 0. manual upper limit value if lim_sdt is false
        lim_i : TYPE, float
            DESCRIPTION. The default is 0. manual lower limit value if lim_sdt is false

        Returns
        -------
        None.

        """
        self.df_r = df_r
        self.lim_sdt = lim_sdt
        self.lim_sdt_p = lim_sdt_p
        self.lim_s = lim_s
        self.lim_i = lim_i

    def perf_imp_pos(self):
        """
        Impressions Performance Vs positive feedback
        This function calculates the performance of the impressions in a period,
        considering the data backwards

        Returns
        -------
        perf : TYPE str
            DESCRIPTION. less: low performance,
            higher: hight perfomance,
            ok: expected performance
        y_real : TYPE float
            DESCRIPTION. value of real data page_positive_feedback_by_type_unique
        y_pred : TYPE float
            DESCRIPTION. value of predicted data page_positive_feedback_by_type_unique
        df_mod : TYPE dataframe optional
            DESCRIPTION. regression data
        data : TYPE dataframe
            DESCRIPTION. data calculation

        """

        df_r = deepcopy(self.df_r)
        lim_sdt = self.lim_sdt
        lim_sdt_p = self.lim_sdt_p
        lim_s = self.lim_s
        lim_i = self.lim_i

        var_empty = None
        method_name = "perf_imp_pos"

        df_r = df_r[(df_r.name == IMP) | (df_r.name == POS)]
        df_r = df_r[df_r.period == "day"]
        df_r.end_time = pd.to_datetime(df_r.end_time)

        try:
            df_group = df_r.groupby(["end_time", "name"], as_index=False).sum()
            df_mod = df_group[df_group.end_time != max(df_group.end_time)]

            imp_m = list(df_mod.value[df_mod.name == IMP])
            pos_m = list(df_mod.value[df_mod.name == POS])
            df_reg = pd.DataFrame({"imp": imp_m, "pos": pos_m})

            x_m = df_reg["imp"]
            x_m = sm.add_constant(x_m)
            y_m = df_reg["pos"]

            mod = sm.OLS(y_m, x_m).fit()

            data = df_group[df_group.end_time == max(df_group.end_time)]

            if lim_sdt:
                lim_sup = mod.fittedvalues.std() * lim_sdt_p
                lim_inf = -mod.fittedvalues.std() * lim_sdt_p
            else:
                lim_sup = lim_s
                lim_inf = lim_i

            x_imp = data[data.name == IMP].value.iloc[0]
            y_pred = (mod.params[1] * x_imp) + mod.params[0]

            y_real = data[data.name == POS].value.iloc[0]

            if y_real < lim_inf + y_pred:
                perf = "less"
            elif y_real > lim_sup + y_pred:
                perf = "higher"
            else:
                perf = "ok"

        except AttributeError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            perf = var_empty
            y_real = var_empty
            y_pred = var_empty

        except Exception as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            perf = var_empty
            y_real = var_empty
            y_pred = var_empty

        return perf, y_real, y_pred
