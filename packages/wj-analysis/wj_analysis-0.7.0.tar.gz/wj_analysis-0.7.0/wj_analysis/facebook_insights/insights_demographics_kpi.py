#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 20:30:53 2021

@author: oscar
"""

import traceback
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


ERR_SYS = "system error: "
CLASS_NAME = "DemographicKpi"
GENDERS = ["F", "M", "U"]


def cal_perc(df_cp, round_data):
    """
    This function calculate percent a column, create a percent column

    Parameters
    ----------
    df_cp : TYPE dataframe
        DESCRIPTION. dataframe with number column
    round_data : TYPE int
        DESCRIPTION. number of decimals

    Returns
    -------
    Create percent column

    """
    df_cp["percent"] = (df_cp["value"] / sum(df_cp["value"])) * 100
    df_cp["percent"] = round(df_cp["percent"], round_data)


def extract_age_gender(df_et_ag, column_ag="indicator"):
    """
    This function extract age and gender

    Parameters
    ----------
    df_et_ag : TYPE dataframe
        DESCRIPTION. dataframe with indicator column to calculate
    column_ag : TYPE, string optional
        DESCRIPTION. The default is 'indicator'.

    Returns
    -------
    df_et_ag : TYPE dataframe
        DESCRIPTION. dataframe with gender and age column

    """
    try:
        df_et_ag["gender"] = df_et_ag[column_ag].apply(lambda x: x[0])
        df_et_ag["age"] = df_et_ag[column_ag].apply(lambda x: x[2:])

    except TypeError as e_1:
        print("".center(60, "="))
        print(e_1)
        print("".center(60, "="))
        print(ERR_SYS + str(exc_info()[0]))
        print("".center(60, "="))
        print(f"Class: {CLASS_NAME}")
        print("".center(60, "="))
        traceback.print_exc()

        df_et_ag["gender"] = float("nan")
        df_et_ag["age"] = float("nan")

    return df_et_ag


def extract_period(df_dem, column="end_time"):
    """
    This function extract the period to analyze and the dates

    Parameters
    ----------
    df_dem : TYPE dataframe
        DESCRIPTION. dataframe insights demographics
    social_n : TYPE string
        DESCRIPTION. social net 'fb' Facebook, 'ig' Instagram

    Returns
    -------
    column : TYPE string
        DESCRIPTION. column date
    """

    col_ag = ["indicator", "value", "date"]

    df_dem[column] = pd.to_datetime(df_dem[column])
    df_dem["date"] = df_dem[column].apply(lambda x: x.date)
    date_max = max(df_dem["date"])

    df_dem = df_dem[col_ag]
    df_dem = df_dem[df_dem["date"] == date_max].reset_index(drop=True)

    return df_dem


class DemographicKpi:
    """
    This class calculates the insights data for visualizations in Oceana
    """

    def __init__(self, social_n):

        self.social_n = social_n

    def age_gender(self, df_ag, round_d=1):
        """
        This function calculate age and gender

        Parameters
        ----------
        df_ag : TYPE dataframe
            DESCRIPTION. dataframe with insights data
        round_d : TYPE, optionaint
            DESCRIPTION. The default is 1. decimals in percent

        Returns
        -------
        df_gender : TYPE dataframe
            DESCRIPTION. dataframe with data gender
        max_gender : TYPE list
            DESCRIPTION. list with max value gender
        list_age : TYPE list with daframes
            DESCRIPTION. list_age[0], age data
                         list_age[1], gender 'F' group by age
                         list_age[2], gender 'M' group by age
                         list_age[3], gender 'U' group by age

        """

        social_n = self.social_n

        try:

            if social_n == "fb":
                df_ag_n = df_ag
            elif social_n == "ig":
                df_ag_n = df_ag[df_ag["name"] == "audience_gender_age"]
            else:
                print("".center(60, "="))
                print(f"=>{social_n}<= !!!!!!! no valid social network")
                print("".center(60, "="))

            df_ag_n = extract_period(df_dem=df_ag_n)

            df_gender = extract_age_gender(df_et_ag=df_ag_n)

            df_gender = df_gender.groupby("gender", as_index=False).sum()
            df_gender = df_gender.sort_values("value", ascending=False).reset_index(
                drop=True
            )
            cal_perc(df_gender, round_d)
            max_gender = df_gender[df_gender["value"] == max(df_gender["value"])]
            max_gender[["value", "percent"]] = max_gender[["value", "percent"]].astype(
                float
            )
            if max_gender["gender"].iloc[0] == "M":
                max_gender["gender"] = "Hombres"
            elif max_gender["gender"].iloc[0] == "F":
                max_gender["gender"] = "Mujeres"
            elif max_gender["gender"].iloc[0] == "U":
                max_gender["gender"] = "No determinado"
            max_gender = dict(max_gender.iloc[0])

            df_age = df_ag_n.groupby(["gender", "age"], as_index=False).sum()
            df_age_all = df_age.groupby("age", as_index=False).sum()
            df_age_all = df_age_all.sort_values("value", ascending=False)
            cal_perc(df_age_all, round_data=round_d)

            df_age_all["gender"] = "Group"

            max_age = df_age[df_age["value"] == max(df_age["value"])]
            max_age["percent"] = round(
                (max(df_age["value"]) / sum(df_age["value"])) * 100, round_d
            )
            max_age[["value", "percent"]] = max_age[["value", "percent"]].astype(float)
            if max_age["gender"].iloc[0] == "M":
                max_age["gender"] = "Hombres"
            elif max_age["gender"].iloc[0] == "F":
                max_age["gender"] = "Mujeres"
            elif max_age["gender"].iloc[0] == "U":
                max_age["gender"] = "No determinado"
            max_age = dict(max_age.iloc[0])

            for g_e in GENDERS:
                df_g = df_age[df_age["gender"] == g_e]
                df_g = df_g.sort_values("value", ascending=False).reset_index(drop=True)
                cal_perc(df_cp=df_g, round_data=round_d)
                df_age_all = pd.concat([df_age_all, df_g], sort=True)

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_gender = pd.DataFrame(columns=["gender", "value", "percent"])
            max_gender = dict()
            df_age_all = pd.DataFrame(columns=["age", "gender", "percent", "value"])
            max_age = dict()

        except AttributeError as e_2:
            print("".center(60, "="))
            print(e_2)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_gender = pd.DataFrame(columns=["gender", "value", "percent"])
            max_gender = dict()
            df_age_all = pd.DataFrame(columns=["age", "gender", "percent", "value"])
            max_age = dict()

        except ValueError as e_3:
            print("".center(60, "="))
            print(e_3)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_gender = pd.DataFrame(columns=["gender", "value", "percent"])
            max_gender = dict()
            df_age_all = pd.DataFrame(columns=["age", "gender", "percent", "value"])
            max_age = dict()

        return df_gender, max_gender, df_age_all, max_age

    def city(self, df_ci, round_d=1, top_bar=7, top_bur=3):
        """
        this function calculate data of city from insights

        Parameters
        ----------
        df_ci : TYPE dataframe
            DESCRIPTION. dataframe with data city insights
        round_d : TYPE, optional int
            DESCRIPTION. The default is 1. decimal percent
        top_bar : TYPE, optional int
            DESCRIPTION. The default is 7. top cities display barplot
        top_bur : TYPE, optional int
            DESCRIPTION. The default is 3. for the display of bubbles
            the number of bubbles to be displayed

        Returns
        -------
        df_ci_burplot : TYPE dataframe
            DESCRIPTION. data bubbles plot
        df_ci_bur : TYPE dataframe
            DESCRIPTION. data barplot

        """

        social_n = self.social_n

        try:

            if social_n == "fb":
                df_ci_n = df_ci
            elif social_n == "ig":
                df_ci_n = df_ci[df_ci["name"] == "audience_city"]
            else:
                print("".center(60, "="))
                print(f"=>{social_n}<= !!!!!!! no valid social network")
                print("".center(60, "="))

            df_ci_n = extract_period(df_dem=df_ci_n)

            df_ci_n["city"] = df_ci_n["indicator"].apply(lambda x: x.split(",")[0])
            cal_perc(df_ci_n, round_d)
            df_ci_n = df_ci_n[["value", "city", "percent"]]

            df_ci_n = df_ci_n.sort_values("value", ascending=False).reset_index(
                drop=True
            )

            df_ci_bur = df_ci_n[0 : (top_bur - 1)]
            others = dict(df_ci_n[top_bur - 1 :].sum())
            hover = df_ci_n["city"][top_bur - 1 :].tolist()
            df_ci_bur = (
                df_ci_bur.append(
                    {
                        "value": others.get("value"),
                        "city": "Otros",
                        "hover": hover,
                        "percent": round(others.get("percent"), round_d),
                    },
                    ignore_index=True,
                )
            ).fillna(0)

            df_ci_bar_plot = df_ci_n.iloc[0 : top_bar - 1]
            others_bar = dict(df_ci_n[top_bar - 1 :].sum())
            hover_bar = df_ci_n["city"][top_bar - 1 :].tolist()
            df_ci_bar_plot = (
                df_ci_bar_plot.append(
                    {
                        "value": others_bar.get("value"),
                        "city": "Otros",
                        "hover": hover_bar,
                        "percent": round(others_bar.get("percent"), round_d),
                    },
                    ignore_index=True,
                )
            ).fillna(0)

            max_city = df_ci_n[df_ci_n["value"] == max(df_ci_n["value"])]
            max_city[["value", "percent"]] = max_city[["value", "percent"]].astype(
                float
            )
            max_city = dict(max_city.iloc[0])

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_ci_bar_plot = pd.DataFrame(columns=["city", "value", "percent"])
            df_ci_bur = pd.DataFrame(columns=["city", "value", "percent"])
            max_city = dict()

        except AttributeError as e_2:
            print("".center(60, "="))
            print(e_2)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_ci_bar_plot = pd.DataFrame(columns=["city", "value", "percent"])
            df_ci_bur = pd.DataFrame(columns=["city", "value", "percent"])
            max_city = dict()

        except ValueError as e_3:
            print("".center(60, "="))
            print(e_3)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_ci_bar_plot = pd.DataFrame(columns=["city", "value", "percent"])
            df_ci_bur = pd.DataFrame(columns=["city", "value", "percent"])
            max_city = dict()

        return df_ci_bar_plot, df_ci_bur, max_city

    def like_source(self, df_like_s, round_d=1):
        """
        this function is only implemented for Facebook

        Parameters
        ----------
        df_like_s : TYPE dataframe
            DESCRIPTION. dataframe whit data of ads Facebok
        round_d : TYPE, optional int
            DESCRIPTION. The default is 1. decimals of percent

        Returns
        -------
        df_like_s : TYPE dataframe
            DESCRIPTION. dataframe with data ads
        max_like_s : TYPE list
            DESCRIPTION. max value ads

        """

        social_n = self.social_n

        if social_n == "fb":
            pass
        elif social_n == "ig":
            print("Not implemented for Instagram yet")
        else:
            print("".center(60, "="))
            print(f"=>{social_n}<= !!!!!!! no valid social network")
            print("".center(60, "="))

        try:

            names_org = [
                "Ads",
                "News Feed",
                "Page Suggestions",
                "Search",
                "Your Page",
                "Other",
                "Restored Likes from Reactivated Accounts",
            ]
            names_new = [
                "Ads",
                "Feed",
                "Sugeridas",
                "Búsqueda",
                "Directos",
                "Otros",
                "Otros",
            ]

            dict_names = dict(zip(names_org, names_new))

            df_like_s = extract_period(df_dem=df_like_s)
            df_like_s["indicator"] = df_like_s["indicator"].replace(dict_names)

            df_like_s = df_like_s.groupby("indicator", as_index=False).sum()

            cal_perc(df_like_s, round_data=round_d)
            df_like_s = df_like_s.sort_values("value", ascending=False)

            max_like_s = df_like_s[df_like_s["value"] == max(df_like_s["value"])]
            max_like_s = list(max_like_s.iloc[0])

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_like_s = pd.DataFrame(columns=["indicator", "value", "percent"])
            max_like_s = list()

        except AttributeError as e_2:
            print("".center(60, "="))
            print(e_2)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_like_s = pd.DataFrame(columns=["indicator", "value", "percent"])
            max_like_s = list()

        except ValueError as e_3:
            print("".center(60, "="))
            print(e_3)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {CLASS_NAME}")
            print("".center(60, "="))
            traceback.print_exc()

            df_like_s = pd.DataFrame(columns=["indicator", "value", "percent"])
            max_like_s = list()

        return df_like_s, max_like_s
