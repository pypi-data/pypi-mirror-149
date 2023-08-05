#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 19:50:57 2020

@author: oscar
"""

from copy import deepcopy
from sys import exc_info

import pandas as pd

ERR_SYS = "System error: "


class EffectMomentsIG:
    def __init__(self, df_ig, trends=False, grouped=True):
        """Effective moments Instagram
        This class calculates the average of the effectiveness in one day,
        the average of the effectiveness per hour in a week
        and the effectiveness of the hours of a week for Instagram

        Parameters
        ----------
        df_FB : TYPE, dataframe
            DESCRIPTION. with twitter accounts filtered by account or
            accounts, competitor and archetype, with calculated effectiveness
        trends : TYPE, bolean
            DESCRIPTION. if required trends in the data
        grouped : TYPE, bolean
            DESCRIPTION. if False it is grouped by brands, if True by groups


        Returns
        -------
        None.

        """
        self.df_org = df_ig
        self.trends = trends
        self.grouped = grouped

    def moments(self):
        """Moments effective Instagram
        This function calculates the average of the effectiveness in one day,
        the average of the effectiveness per hour,
        in a week and the effectiveness of the hours of a week for Instagram

        Returns
        -------
        df_eff_day : TYPE dataframe
            DESCRIPTION. effectiveness hours day
        df_eff_hours : TYPE dataframe
            DESCRIPTION. effectiveness hour a week
        df_eff_days_hours : TYPE dataframe
            DESCRIPTION. effectiveness days and hour with a week

        """

        colum_ig = [
            "owner_id",
            "created_at",
            "owner_username",
            "shortcode",
            "group",
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post",
        ]
        group = ["brand", "archetypes", "competitors"]
        method_name = "moments"

        if self.grouped is True:
            df_empty_day = pd.DataFrame(
                columns=[
                    "day",
                    "group",
                    "counts",
                    "engagement_rate_by_post",
                    "rel_engagement_rate_by_post",
                ]
            )
            df_empty_hours = pd.DataFrame(
                columns=[
                    "hour",
                    "group",
                    "counts",
                    "engagement_rate_by_post",
                    "rel_engagement_rate_by_post",
                ]
            )
            df_empty_days_week = pd.DataFrame(
                columns=[
                    "hour",
                    "day",
                    "group",
                    "counts",
                    "engagement_rate_by_post",
                    "rel_engagement_rate_by_post",
                ]
            )
        else:
            df_empty_day = pd.DataFrame(
                columns=[
                    "day",
                    "group",
                    "_object_name",
                    "counts",
                    "_object_id",
                    "engagement_rate_by_post",
                    "rel_engagement_rate_by_post",
                ]
            )
            df_empty_hours = pd.DataFrame(
                columns=[
                    "hour",
                    "group",
                    "_object_name",
                    "counts",
                    "_object_id",
                    "engagement_rate_by_post",
                    "rel_engagement_rate_by_post",
                ]
            )
            df_empty_days_week = pd.DataFrame(
                columns=[
                    "hour",
                    "day",
                    "group",
                    "counts",
                    "_object_name",
                    "_object_id",
                    "engagement_rate_by_post",
                    "rel_engagement_rate_by_post",
                ]
            )

        try:
            df_original = self.df_org[colum_ig]
            df_original = deepcopy(df_original)
            if df_original.isna().any().any():
                df_original = None

        except KeyError as e_1:
            print(e_1)
            error_1 = exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
        trends = self.trends
        grouped = self.grouped

        if trends:
            group.append("trends")

        try:
            df_original.created_at = pd.to_datetime(df_original.created_at)
            df_copy = deepcopy(df_original)

            df_copy["day"] = df_copy.created_at.apply(lambda x: x.weekday())
            df_copy["hour"] = df_copy.created_at.apply(lambda x: x.hour)
            df_copy["date"] = df_copy.created_at.apply(lambda x: x.date())
            df_copy["hour"] = df_copy.hour.apply(lambda x: str(x))
            df_copy["day"] = df_copy.day.apply(lambda x: str(x))

            df_filter = deepcopy(df_copy.reset_index())

            if grouped is True:
                grouped_id = "group"
            else:
                grouped_id = "owner_id"

            df_eff_day = pd.DataFrame()
            for sel_group in group:
                temp_1 = df_filter[df_filter.group == sel_group]
                if grouped is True:
                    temp_1 = temp_1.groupby(["day", grouped_id], as_index=False).agg(
                        {"engagement_rate_by_post": "mean", "shortcode": "count"}
                    )
                else:
                    temp_1 = temp_1.groupby(
                        ["day", "group", grouped_id], as_index=False
                    ).agg(
                        {
                            "engagement_rate_by_post": "mean",
                            "owner_username": "last",
                            "shortcode": "count",
                        }
                    )
                df_eff_day = pd.concat([df_eff_day, temp_1])

            df_eff_day = df_eff_day.sort_values(
                "engagement_rate_by_post", ascending=False
            ).reset_index()
            df_eff_day = df_eff_day.drop(columns="index")
            df_eff_day = df_eff_day.rename(
                columns={
                    "owner_id": "_object_id",
                    "owner_username": "_object_name",
                    "shortcode": "counts",
                }
            )

            df_eff_hours = pd.DataFrame()
            for sel_group in group:
                temp_1 = df_filter[df_filter.group == sel_group]
                if grouped is True:
                    temp_1 = temp_1.groupby(["hour", grouped_id], as_index=False).agg(
                        {"engagement_rate_by_post": "mean", "shortcode": "count"}
                    )
                else:
                    temp_1 = temp_1.groupby(
                        ["hour", "group", grouped_id], as_index=False
                    ).agg(
                        {
                            "engagement_rate_by_post": "mean",
                            "owner_username": "last",
                            "shortcode": "count",
                        }
                    )
                df_eff_hours = pd.concat([df_eff_hours, temp_1])

            df_eff_hours = df_eff_hours.sort_values(
                "engagement_rate_by_post", ascending=False
            ).reset_index()
            df_eff_hours = df_eff_hours.drop(columns="index")
            df_eff_hours = df_eff_hours.rename(
                columns={
                    "owner_id": "_object_id",
                    "owner_username": "_object_name",
                    "shortcode": "counts",
                }
            )

            df_eff_days_hours = pd.DataFrame()
            for group in group:
                temp_1 = df_filter[df_filter.group == group]
                if grouped is True:
                    temp_1 = temp_1.groupby(
                        ["hour", "day", grouped_id], as_index=False
                    ).agg({"engagement_rate_by_post": "mean", "shortcode": "count"})
                else:
                    temp_1 = temp_1.groupby(
                        ["hour", "day", "group", grouped_id], as_index=False
                    ).agg(
                        {
                            "engagement_rate_by_post": "mean",
                            "owner_username": "last",
                            "shortcode": "count",
                        }
                    )

                df_eff_days_hours = pd.concat([df_eff_days_hours, temp_1])

            df_eff_days_hours = df_eff_days_hours.sort_values(
                "engagement_rate_by_post", ascending=False
            ).reset_index()
            df_eff_days_hours = df_eff_days_hours.drop(columns="index")
            df_eff_days_hours = df_eff_days_hours.rename(
                columns={
                    "owner_id": "_object_id",
                    "owner_username": "_object_name",
                    "shortcode": "counts",
                }
            )

        except UnboundLocalError as e_2:
            print(e_2)
            error_1 = exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_eff_day = df_empty_day
            df_eff_hours = df_empty_hours
            df_eff_days_hours = df_empty_days_week

        except KeyError as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_eff_day = df_empty_day
            df_eff_hours = df_empty_hours
            df_eff_days_hours = df_empty_days_week

        except Exception as e_4:
            print(e_4)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_eff_day = df_empty_day
            df_eff_hours = df_empty_hours
            df_eff_days_hours = df_empty_days_week

        return df_eff_day, df_eff_hours, df_eff_days_hours
