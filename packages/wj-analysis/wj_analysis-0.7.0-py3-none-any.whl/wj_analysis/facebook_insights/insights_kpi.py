#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 15:22:27 2021

@author: oscar
"""

import ast
import traceback
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


ERR_SYS = "system error: "

COL_POST_F = [
    "page_id",
    "post_id",
    "post_from",
    "permalink_url",
    "shares",
    "likes",
    "comments",
    "reactions_love",
    "reactions_wow",
    "reactions_haha",
    "created_time",
    "reactions_sad",
    "reactions_angry",
    "reactions_thankful",
    "full_picture",
]

COL_INS_F = [
    "post_id",
    "post_impressions",
    "post_impressions_unique",
    "post_impressions_paid_unique",
    "post_impressions_organic_unique",
]

COL_POST_I = [
    "account_id",
    "owner_username",
    "shortcode",
    "date_local",
    "url",
    "likes_count",
    "comment_count",
]

COL_INS_I = ["name", "period", "value", "end_time", "shortcode"]

METHOD_NAME = ["reach", "interact", "impressions", "engagement_rate", "ts_reach"]

CLASS_NAME = "insights_kpi"

# flags with cases in compare periods
FLAGS = ["n==b", "n>b", "n<b", "n<period_and_b==0", "b==0", "except"]


def select_last_post(df_p, id_name, id_last):
    """
    This function extract the last record in the database
    with equal identifier

    Parameters
    ----------
    df_p : TYPE, dataframe
        DESCRIPTION. dataframe with post identifier
    id_name : TYPE string
        DESCRIPTION. post identifier
    id_last : TYPE string
        DESCRIPTION. columns to max select

    Returns
    -------
    df_post : TYPE dataframe
        DESCRIPTION. dataframe with last record

    """
    df_post_temp = pd.DataFrame()
    for i in df_p[id_name].unique():
        temp1 = df_p[df_p[id_name] == i]
        temp2 = max(temp1[id_last])
        temp1 = temp1[temp1[id_last] == temp2]
        df_post_temp = pd.concat([df_post_temp, temp1])
    if len(df_post_temp) == 0:
        df_post = pd.DataFrame(columns=df_p.columns)
    else:
        df_post = df_post_temp

    return df_post


def dataframes_ts(df_r1, df_r2, date_max, days, column_reach):
    """
    This function generates the time series and makes a cumulative sum of the data

    Parameters
    ----------
    df_r1 : TYPE dataframe
        DESCRIPTION. with first period
    df_r2 : TYPE dataframe
        DESCRIPTION. with second period
    date_max : TYPE datetime.date
        DESCRIPTION. date incial to analice
    days : TYPE int
        DESCRIPTION. period to analice
    column_reach : TYPE str
        DESCRIPTION. name of colum to analice

    Returns
    -------
    df_ts1 : TYPE dataframe
        DESCRIPTION. with first period with time serie
    df_ts2 : TYPE dataframe
        DESCRIPTION. with second period with time serie

    """

    date_range1 = []
    for day in range(days):
        date_range1.append(date_max - pd.to_timedelta(day, unit="d"))

    date_range2 = []
    for day in range(days):
        date_range2.append(
            (date_range1[-1] - pd.to_timedelta(1, unit="d"))
            - pd.to_timedelta(day, unit="d")
        )

    if len(df_r1) > 0:
        df_r1 = df_r1.groupby("date", as_index=False).sum()

    if len(df_r2) > 0:
        df_r2 = df_r2.groupby("date", as_index=False).sum()

    df_ts1 = pd.DataFrame(columns=["date", "reach", "period", "pos"])
    df_ts2 = pd.DataFrame(columns=["date", "reach", "period", "pos"])

    date_range1 = list(reversed(date_range1))
    date_range2 = list(reversed(date_range2))

    df_ts1["date"] = date_range1
    it_d = 0
    for day1 in date_range1:
        df_ts1["date"].iloc[it_d] = day1
        df_ts1["period"].iloc[it_d] = "now"
        df_ts1["pos"].iloc[it_d] = it_d
        df_temp1 = df_r1[df_r1["date"] == day1]
        if len(df_temp1) > 0:
            df_ts1["reach"].iloc[it_d] = df_temp1[column_reach].iloc[0]
        else:
            df_ts1["reach"].iloc[it_d] = 0
        it_d += 1

    df_ts2["date"] = date_range2
    it_d = 0
    for day2 in date_range2:
        df_ts2["date"].iloc[it_d] = day2
        df_ts2["period"].iloc[it_d] = "before"
        df_ts2["pos"].iloc[it_d] = it_d
        df_temp2 = df_r2[df_r2["date"] == day2]
        if len(df_temp2) > 0:
            df_ts2["reach"].iloc[it_d] = df_temp2[column_reach].iloc[0]
        else:
            df_ts2["reach"].iloc[it_d] = 0
        it_d += 1

    return df_ts1, df_ts2


def delta(data1, data2, rou=1):
    """
    delta calculate percentage difference between two numbers

    Parameters
    ----------
    data1 : TYPE. int or float
        DESCRIPTION. first number
    data2 : TYPE int or float
        DESCRIPTION. second number
    rou : TYPE, optional int
        DESCRIPTION. The default is 1. roun doutput

    Returns
    -------
    dta : TYPE float
        DESCRIPTION. percentage difference between two numbers

    """

    if data2 > 0:
        dta = (1 - (data1 / data2)) * 100
        dta = round(dta, rou)
    else:
        dta = 0

    return dta


def reactions_cal(df_reach, social_n):
    """
    This function sums the reactions

    Parameters
    ----------
    df_reach : TYPE dataframe
        DESCRIPTION. dataframe whit Facebook or Instagram columns
    social_n : TYPE string
        DESCRIPTION. social network

    Returns
    -------
    all_reactions : TYPE dict
        DESCRIPTION. dict with the sum of the reactions
    total_reactions : TYPE
        DESCRIPTION. sum total reactions

    """
    if social_n == "fb":

        all_reactions = {
            "total_shares": sum(df_reach["shares"]),
            "total_likes": sum(df_reach["likes"]),
            "total_comments": sum(df_reach["comments"]),
            "total_love": sum(df_reach["reactions_love"]),
            "total_wow": sum(df_reach["reactions_wow"]),
            "total_haha": sum(df_reach["reactions_haha"]),
            "total_sad": sum(df_reach["reactions_sad"]),
            "total_angry": sum(df_reach["reactions_angry"]),
            "total_thankful": sum(df_reach["reactions_thankful"]),
        }

    else:
        all_reactions = {
            "total_saved": sum(df_reach["saved"]),
            "total_video_views": sum(df_reach["video_views"]),
            "total_likes_count": sum(df_reach["likes_count"]),
            "total_comment_count": sum(df_reach["comment_count"]),
        }

    reactions = []
    for reaction in all_reactions:
        reactions.append(all_reactions.get(reaction))

    total_reactions = sum(reactions)

    return all_reactions, total_reactions


def extrac_period(df_no_dt, days, social_n):
    """
    This function extract the period to analyze and the dates

    Parameters
    ----------
    df_no_dt : TYPE dataframe
        DESCRIPTION. dataframe whith post information
    days : TYPE int
        DESCRIPTION. period in days to analice
    social_n : TYPE str only 'fb' or 'ig'
        DESCRIPTION. 'fb' to Facebook, 'ig' to Instagram,

    Returns
    -------
    df_period_now : TYPE dataframe
        DESCRIPTION. filtered data of the current period
    df_period_bef : TYPE dataframe
        DESCRIPTION. filtered data from the previous period
    flag : TYPE str
        DESCRIPTION. indicates the behavior of the periods, as follows:
            'n==b': periods have the same amount of data data
            'n>b': the first period has more data than the second
            'n<b': the second period has more data than the first
            'n<period and b==0': the first period has less data than
            those consulted and the second has no data
            'b==0': the second perdiod has no data
            'except': an exception occurred
    delta_time : TYPE date
        DESCRIPTION. list with date range

    """

    if social_n == "fb":
        column = "created_time"
        col_post = COL_POST_F

    elif social_n == "ig":
        column = "date_local"
        col_post = COL_POST_I
    else:
        print(f"{social_n} no valid social network")

    df_period_now_empty = pd.DataFrame(columns=col_post)
    df_period_before_empty = pd.DataFrame(columns=col_post)

    try:

        df_no_dt[column] = pd.to_datetime(df_no_dt[column])
        df_no_dt["date"] = df_no_dt[column].apply(lambda x: x.date)

        period = pd.to_timedelta(days, unit="d")

        date_max1 = max(df_no_dt["date"])
        date_min1 = date_max1 - (period - pd.to_timedelta(1, unit="d"))
        date_max2 = date_min1 - pd.to_timedelta(1, unit="d")
        date_min2 = date_max2 - period

        df_period_now = df_no_dt[
            (df_no_dt["date"] <= date_max1) & (df_no_dt["date"] >= date_min1)
        ]
        df_period_bef = df_no_dt[
            (df_no_dt["date"] <= date_max2) & (df_no_dt["date"] >= date_min2)
        ]

        df_period_now = df_period_now.drop_duplicates()
        df_period_bef = df_period_bef.drop_duplicates()

        if (len(df_period_now) == len(df_period_bef)) and (len(df_period_bef) != 0):
            flag = FLAGS[0]
        elif (len(df_period_now) > len(df_period_bef)) and (len(df_period_bef) != 0):
            flag = FLAGS[1]
        elif (len(df_period_now) < len(df_period_bef)) and (len(df_period_bef) != 0):
            flag = FLAGS[2]
        elif (len(df_period_now) < period.days) and (len(df_period_bef) == 0):
            flag = FLAGS[3]
        elif len(df_period_bef) == 0:
            flag = FLAGS[4]

        delta_time = [date_max1, date_min1, date_max2, date_min2]

    except KeyError as e_1:
        print("".center(60, "="))
        print(e_1)
        print("".center(60, "="))
        print(ERR_SYS + str(exc_info()[0]))
        print("".center(60, "="))
        print(f"Class: {CLASS_NAME}")
        print("".center(60, "="))
        traceback.print_exc()

        df_period_now = df_period_now_empty
        df_period_bef = df_period_before_empty
        flag = FLAGS[5]
        delta_time = ["", "", "", ""]

    except AttributeError as e_2:
        print("".center(60, "="))
        print(e_2)
        print("".center(60, "="))
        print(ERR_SYS + str(exc_info()[0]))
        print("".center(60, "="))
        print(f"Class: {CLASS_NAME}")
        print("".center(60, "="))
        traceback.print_exc()

        df_period_now = df_period_now_empty
        df_period_bef = df_period_before_empty
        flag = FLAGS[5]
        delta_time = ["", "", "", ""]

    except ValueError as e_3:
        print("".center(60, "="))
        print(e_3)
        print("".center(60, "="))
        print(ERR_SYS + str(exc_info()[0]))
        print("".center(60, "="))
        print(f"Class: {CLASS_NAME}")
        print("".center(60, "="))
        traceback.print_exc()

        df_period_now = df_period_now_empty
        df_period_bef = df_period_before_empty
        flag = "except"
        delta_time = ["", "", "", ""]

    return df_period_now, df_period_bef, flag, delta_time


def extract_name(df_post, column="name"):
    """
    extract_name of the facebook brand to analyze

    Parameters
    ----------
    df_post : TYPE dataframe
        DESCRIPTION. datafraem whith post
    column : TYPE, optional
        DESCRIPTION. The default is 'name', for extract id 'id'

    Returns
    -------
    df : TYPE dataframe
        DESCRIPTION. dataframe whit column parameter name

    """

    try:
        brand_name = df_post["post_from"].apply(ast.literal_eval)
        id_column = []
        for i in range(len(df_post)):
            temp_1 = brand_name.iloc[i][column]
            id_column.append(temp_1)
        df_post[column] = id_column
        df_post.drop(columns="post_from", inplace=True)

    except KeyError as e_1:
        print("".center(60, "="))
        print(e_1)
        print("".center(60, "="))
        print(ERR_SYS + str(exc_info()[0]))
        print("".center(60, "="))
        print(f"Class: {CLASS_NAME}")
        print("".center(60, "="))
        traceback.print_exc()

        df_post[column] = "no_name"

    return df_post


class InsightsKpi:
    """
    This class calculates the information needed for the kpi for
    the Facebook and Instagram reach dashboard.
    """

    def __init__(self, df_p, df_i, days, social_n):
        """
        This function prepare data

        Parameters
        ----------
        df_p : TYPE dataframe
            DESCRIPTION. dataframe whith post information
        df_i : TYPE dataframe
            DESCRIPTION. dataframe whith insights information
        days : TYPE int
            DESCRIPTION. period in days to analice
        social_n : TYPE str only 'fb' or 'ig'
            DESCRIPTION. 'fb' to Facebook, 'ig' to Instagram,

        Returns
        -------
        None.

        """

        if social_n == "fb":
            df_p = extract_name(df_post=df_p, column="name")
            column = "post_id"
        elif social_n == "ig":
            column = "shortcode"
            df_p = select_last_post(df_p=df_p, id_name="shortcode", id_last="id")
        else:
            print("".center(60, "="))
            print(f"=>{social_n}<= !!!!!!! no valid social network")
            print("".center(60, "="))
            column = ""

        self.social_n = social_n

        self.days = days

        if days <= 1:
            print("the minimum period is two days")
            days = 2

        df_all = df_p.merge(df_i, on=column, how="outer")
        self.df_1, self.df_2, self.flag, self.d_time = extrac_period(
            df_no_dt=df_all, days=days, social_n=social_n
        )
        self.df_1 = self.df_1.fillna(0)
        self.df_2 = self.df_2.fillna(0)

        self.dates = {
            "date_max1": self.d_time[0],
            "date_min1": self.d_time[1],
            "date_max2": self.d_time[2],
            "date_min2": self.d_time[3],
        }

    def reach(self):
        """
        This function calculate reac

        Returns
        -------
        reach : TYPE dict
            DESCRIPTION. information reach

        """

        social_n = self.social_n
        reach_date_max1 = self.dates.get("date_max1")
        reach_date_min1 = self.dates.get("date_min1")
        reach_date_max2 = self.dates.get("date_max2")
        reach_date_min2 = self.dates.get("date_min2")

        if social_n == "fb":
            col_reach = [
                "date",
                "post_impressions_unique",
                "post_impressions_organic_unique",
                "post_impressions_paid_unique",
            ]
        else:
            col_reach = ["date", "impressions", "reach"]

        try:
            df_reach1 = self.df_1[col_reach]
            df_reach2 = self.df_2[col_reach]

            # Reach facebook
            if social_n == "fb":
                reach = sum(df_reach1["post_impressions_unique"])
                if self.flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    reach_delta = 0
                else:
                    reach_delta = delta(
                        reach, sum(df_reach2["post_impressions_unique"])
                    )

                reach_organic = sum(df_reach1["post_impressions_organic_unique"])
                reach_paid = sum(df_reach1["post_impressions_paid_unique"])

                reach = {
                    "reach": reach,
                    "reach_delta": abs(reach_delta),
                    "reach_organic": reach_organic,
                    "reach_paid": reach_paid,
                    "reach_date_max1": reach_date_max1,
                    "reach_date_min1": reach_date_min1,
                    "reach_date_max2": reach_date_max2,
                    "reach_date_min2": reach_date_min2,
                    "flag": self.flag,
                }

            # Reach Instagram
            elif social_n == "ig":
                reach = sum(df_reach1["reach"])
                if self.flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    reach_delta = 0
                else:
                    reach_delta = delta(reach, sum(df_reach2["reach"]))

                reach_impressions = sum(df_reach1["impressions"])

                reach = {
                    "reach": reach,
                    "reach_delta": abs(reach_delta),
                    "reach_impressions": reach_impressions,
                    "reach_date_max1": reach_date_max1,
                    "reach_date_min1": reach_date_min1,
                    "reach_date_max2": reach_date_max2,
                    "reach_date_min2": reach_date_min2,
                    "flag": self.flag,
                }

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME} => {METHOD_NAME[0]}")
            print("".center(60, "="))
            traceback.print_exc()

            if social_n == "fb":
                reach = {
                    "reach": "",
                    "reach_delta": "",
                    "reach_organic": "",
                    "reach_paid": "",
                    "reach_date_max1": "",
                    "reach_date_min1": "",
                    "reach_date_max2": "",
                    "reach_date_min2": "",
                    "flag": self.flag,
                }
            else:
                reach = {
                    "reach": "",
                    "reach_delta": "",
                    "reach_impressions": "",
                    "reach_date_max1": "",
                    "reach_date_min1": "",
                    "reach_date_max2": "",
                    "reach_date_min2": "",
                    "flag": self.flag,
                }

        return reach

    def interact(self):
        """
        This function calculate interact (likes, share ...)

        Returns
        -------
        inter : TYPE dict
            DESCRIPTION. information interact

        """

        social_n = self.social_n

        if social_n == "fb":
            col_inter = [
                "date",
                "shares",
                "likes",
                "comments",
                "reactions_love",
                "reactions_wow",
                "reactions_haha",
                "reactions_sad",
                "reactions_angry",
                "reactions_thankful",
            ]
        else:
            col_inter = ["date", "likes_count", "comment_count", "saved", "video_views"]

        try:
            # Interact Facebook
            if social_n == "fb":

                all_inter1, total_inter1 = reactions_cal(
                    self.df_1[col_inter], social_n=social_n
                )
                _, total_inter2 = reactions_cal(self.df_2[col_inter], social_n=social_n)

                if self.flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    inter_delta = 0
                else:
                    inter_delta = delta(total_inter1, total_inter2)

                inter = {
                    "interact": total_inter1,
                    "inter_delta": abs(inter_delta),
                    "inter_likes": all_inter1.get("total_likes"),
                    "inter_shares": all_inter1.get("total_shares"),
                    "inter_comments": all_inter1.get("total_comments"),
                    "inter_date_max1": self.dates.get("date_max1"),
                    "inter_date_min1": self.dates.get("date_min1"),
                    "inter_date_max2": self.dates.get("date_max2"),
                    "inter_date_min2": self.dates.get("date_min2"),
                    "flag": self.flag,
                }

            # Interact Instagram
            elif social_n == "ig":
                all_inter1, total_inter1 = reactions_cal(
                    self.df_1[col_inter], social_n=social_n
                )
                _, total_inter2 = reactions_cal(self.df_2[col_inter], social_n=social_n)

                if self.flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    inter_delta = 0
                else:
                    inter_delta = delta(total_inter1, total_inter2)

                inter = {
                    "interact": total_inter1,
                    "inter_delta": abs(inter_delta),
                    "inter_likes": all_inter1.get("total_likes_count"),
                    "inter_comment": all_inter1.get("total_comment_count"),
                    "inter_saved": all_inter1.get("total_saved"),
                    "inter_video_views": all_inter1.get("total_video_views"),
                    "inter_date_max1": self.dates.get("date_max1"),
                    "inter_date_min1": self.dates.get("date_min1"),
                    "inter_date_max2": self.dates.get("date_max2"),
                    "inter_date_min2": self.dates.get("date_min2"),
                    "flag": self.flag,
                }

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME} => {METHOD_NAME[1]}")
            print("".center(60, "="))
            traceback.print_exc()

            if social_n == "fb":
                inter = {
                    "interact": "",
                    "inter_delta": "",
                    "inter_likes": "",
                    "inter_shares": "",
                    "inter_comments": "",
                    "inter_date_max1": "",
                    "inter_date_min1": "",
                    "inter_date_max2": "",
                    "inter_date_min2": "",
                    "flag": self.flag,
                }
            else:
                inter = {
                    "interact": "",
                    "inter_delta": "",
                    "inter_likes": "",
                    "inter_comment": "",
                    "inter_saved_count": "",
                    "inter_video_views": "",
                    "inter_date_max1": "",
                    "inter_date_min1": "",
                    "inter_date_max2": "",
                    "inter_date_min2": "",
                    "flag": self.flag,
                }

        return inter

    def impressions(self):
        """
        This function calculate impressions

        Returns
        -------
        impress : TYPE dict
            DESCRIPTION. information impressions

        """

        flag = self.flag
        social_n = self.social_n
        impress_date_max1 = self.dates.get("date_max1")
        impress_date_min1 = self.dates.get("date_min1")
        impress_date_max2 = self.dates.get("date_max2")
        impress_date_min2 = self.dates.get("date_min2")

        if social_n == "fb":
            col_inter = ["date", "post_impressions"]
        else:
            col_inter = ["date", "impressions"]

        try:
            df_reach1 = self.df_1[col_inter]
            df_reach2 = self.df_2[col_inter]

            # Impressions Facebook
            if social_n == "fb":
                impressions = sum(df_reach1["post_impressions"])
                impressions2 = sum(df_reach2["post_impressions"])

                if flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    impress_delta = 0
                else:
                    impress_delta = delta(impressions, impressions2)

                impress = {
                    "impressions": impressions,
                    "impress_delta": abs(impress_delta),
                    "impress_date_max1": impress_date_max1,
                    "impress_date_min1": impress_date_min1,
                    "impress_date_max2": impress_date_max2,
                    "impress_date_min2": impress_date_min2,
                    "flag": flag,
                }

            # Impressions Instagram
            elif social_n == "ig":
                impressions = sum(df_reach1["impressions"])
                impressions2 = sum(df_reach2["impressions"])

                if flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    impress_delta = 0
                else:
                    impress_delta = delta(impressions, impressions2)

                impress = {
                    "impressions": impressions,
                    "impress_delta": abs(impress_delta),
                    "impress_date_max1": impress_date_max1,
                    "impress_date_min1": impress_date_min1,
                    "impress_date_max2": impress_date_max2,
                    "impress_date_min2": impress_date_min2,
                    "flag": flag,
                }

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME} => {METHOD_NAME[2]}")
            print("".center(60, "="))
            traceback.print_exc()

            impress = {
                "impressions": "",
                "impress_delta": "",
                "impress_date_max1": "",
                "impress_date_min1": "",
                "impress_date_max2": "",
                "impress_date_min2": "",
                "flag": flag,
            }

        return impress

    def engagement_rate(self):
        """
        This function calculate engagement_rate

        Returns
        -------
        engagement_rate : TYPE dict
            DESCRIPTION. information engagement_rate

        """

        flag = self.flag
        social_n = self.social_n

        if social_n == "fb":
            col_inter = [
                "date",
                "shares",
                "likes",
                "comments",
                "reactions_love",
                "reactions_wow",
                "reactions_haha",
                "reactions_sad",
                "reactions_angry",
                "reactions_thankful",
                "post_impressions_unique",
            ]
        else:
            col_inter = [
                "date",
                "likes_count",
                "comment_count",
                "saved",
                "video_views",
                "reach",
            ]

        try:
            df_reach1 = self.df_1[col_inter]
            df_reach2 = self.df_2[col_inter]

            # Engagement Facebook
            if social_n == "fb":
                _, total_inter1 = reactions_cal(df_reach1, social_n=social_n)
                _, total_inter2 = reactions_cal(df_reach2, social_n=social_n)

                if (
                    sum(df_reach1["post_impressions_unique"]) != 0
                    and sum(df_reach2["post_impressions_unique"]) != 0
                ):
                    eng = (
                        total_inter1 / sum(df_reach1["post_impressions_unique"])
                    ) * 100
                    eng2 = (
                        total_inter2 / sum(df_reach2["post_impressions_unique"])
                    ) * 100
                else:
                    eng = 0
                    eng2 = 0

                if flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    eng_delta = 0
                else:
                    eng_delta = delta(eng, eng2)

                engagement_rate = {
                    "engagement_rate": round(eng, 1),
                    "delta_eng": abs(eng_delta),
                    "flag": flag,
                }

            # Engagement Instagram
            elif social_n == "ig":
                _, total_inter1 = reactions_cal(df_reach1, social_n=social_n)
                _, total_inter2 = reactions_cal(df_reach2, social_n=social_n)

                if sum(df_reach1["reach"]) != 0 and sum(df_reach2["reach"]) != 0:
                    eng = (total_inter1 / sum(df_reach1["reach"])) * 100
                    eng2 = (total_inter2 / sum(df_reach2["reach"])) * 100
                else:
                    eng = 0
                    eng2 = 0

                if flag in (FLAGS[4], FLAGS[3], FLAGS[5]):
                    eng_delta = 0
                else:
                    eng_delta = delta(eng, eng2)

                engagement_rate = {
                    "engagement_rate": round(eng, 1),
                    "delta_eng": abs(eng_delta),
                    "flag": flag,
                }

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME} => {METHOD_NAME[3]}")
            print("".center(60, "="))
            traceback.print_exc()

            engagement_rate = {"engagement_rate": "", "delta_eng": "", "flag": flag}

        return engagement_rate

    def ts_reach(self, all_df=True):
        """
        This function generate time series with period to analyse

        Parameters
        ----------
        all_df : TYPE, optional
            DESCRIPTION. The default is True. If it is false,
            it only generates the time series of the current period.

        Returns
        -------
        df_all_reach : TYPE dataframe
            DESCRIPTION. dataframe with time serie selected

        """

        days = self.days
        social_n = self.social_n

        try:

            date_max1 = self.dates.get("date_max1")

            if social_n == "fb":
                column_reach_sn = "post_impressions_unique"
            else:
                column_reach_sn = "reach"

            col_inter = ["date", column_reach_sn]

            df_reach1 = self.df_1[col_inter]
            df_reach2 = self.df_2[col_inter]

            if all_df:
                df_ts1, df_ts2 = dataframes_ts(
                    df_r1=df_reach1,
                    df_r2=df_reach2,
                    date_max=date_max1,
                    days=days,
                    column_reach=column_reach_sn,
                )
                df_ts1["reach"] = df_ts1["reach"].cumsum()
                df_ts2["reach"] = df_ts2["reach"].cumsum()
                df_all_reach = pd.concat([df_ts1, df_ts2])
                df_all_reach = df_all_reach.reset_index(drop=True)

            else:
                df_ts1, _ = dataframes_ts(
                    df_r1=df_reach1,
                    df_r2=df_reach2,
                    date_max=date_max1,
                    days=days,
                    column_reach=column_reach_sn,
                )
                df_all_reach = df_ts1
                df_all_reach["reach"] = df_all_reach["reach"].cumsum()

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME} => {METHOD_NAME[4]}")
            print("".center(60, "="))
            traceback.print_exc()

            df_all_reach = pd.DataFrame(columns=["date", "reach", "period", "pos"])

        return df_all_reach
