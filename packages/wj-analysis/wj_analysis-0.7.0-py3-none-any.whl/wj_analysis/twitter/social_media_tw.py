#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:26:06 2020

@author: oscar
"""

import re as reg
import traceback
from copy import deepcopy
from sys import exc_info

import pandas as pd

ERR_SYS = "system error: "


def thread_mention(df_media_tw):
    """
    thread_mention this function filters the twitter threads

    Parameters
    ----------
    df_media_tw : TYPE dataframe
        DESCRIPTION. dataframe with mentios

    Returns
    -------
    df_media_tw : TYPE dataframe
        DESCRIPTION. dataframe with mentiosbut filter threads

    """
    if len(df_media_tw) > 2:
        thread = []
        i_t = 0
        f_t = 1
        while i_t < len(df_media_tw):
            if df_media_tw.in_reply_to_status_id.iloc[i_t] == None:
                thread.append(0)
            else:
                if (
                    float(df_media_tw.in_reply_to_status_id.iloc[i_t])
                    / float(df_media_tw.tweet_id.iloc[f_t])
                    == 1
                ):
                    thread.append(1)
                else:
                    thread.append(0)
            i_t += 1
            if f_t < len(df_media_tw) - 1:
                f_t += 1
        df_media_tw["thread"] = thread
        df_media_tw = df_media_tw[df_media_tw.thread == 0]
        df_media_tw = df_media_tw.drop(columns=["thread"])
        df_media_tw = df_media_tw.sort_values(["tweet_id", "created_at"])

    return df_media_tw


def create_regex(list_terms):
    """
    Parameters
    ----------
    list_terms : TYPE list
        DESCRIPTION. list with the text to apply

    Returns
    -------
    pat : TYPE list
        DESCRIPTION. lislist without @name

    """
    pattern = r"\b@*" + r"\b|\b@*".join(list_terms) + r"\b"
    pat = reg.compile(pattern)
    return pat


class SocialpresTW:
    def __init__(self, df_tw, df_count, brand, auto_n=True, thread=True):
        """Digital social presence
        This function calculates social presence, comparing it with the
        weight of each digital media

        Parameters
        ----------
        df_ig : TYPE dataframe
            DESCRIPTION. Contains the information collected from social media
            in Instagram
        df_count : TYPE dataframe
            DESCRIPTION. Contains the media information to consult
        media_weights : TYPE dict
            DESCRIPTION.Weights and names the digital media
        brand : TYPE string
            DESCRIPTION. brand analyze
        auto_n : TYPE bolean
            DESCRIPTION. remove mentions of the same account if true
        thread : TYPE bolean
            DESCRIPTION. remove mentions of thread twitter if true

        Returns
        -------
        None.

        """

        self.df_tw = df_tw
        self.df_count = df_count
        self.brand = brand
        self.auto_n = auto_n
        self.thread = thread

    def c_pres_tw(self):
        """Twitter media presence
        calculates Twitter only number of appearances

        Returns
        -------
        df_med_c
        TYPE dataframe
            DESCRIPTION. each count number of appearances in Twitter

        """
        col_med = ["created_at", "description", "text", "tweet_id", "screen_name"]

        df_tw = self.df_tw
        df_c = self.df_count
        auto_n = self.auto_n
        df_empty_c = pd.DataFrame(columns=["media", "mentions"])
        method_name = "c_pres_tw"

        try:
            df_tw = df_tw[col_med]
            df_tw = deepcopy(df_tw)
            df_tw.created_at = pd.to_datetime(df_tw.created_at)

            df_tw.text = df_tw.text.apply(lambda x: str(x))
            df_tw.text = df_tw.text.apply(lambda x: x.lower())

            df_m = deepcopy(df_tw)
            for idd, row in df_c.set_index("nombre").iterrows():
                if idd:
                    account_terms_regex = create_regex(
                        [t.strip() for t in row.terminos.split(",")]
                    )
                    df_m[f"{idd}"] = df_m["text"].str.contains(
                        account_terms_regex, regex=True
                    )

            df_m["auto"] = 0

            if auto_n:
                col_names = df_m.columns[5:-1]
                for col in col_names:
                    for index in range(len(df_m)):
                        temp_1 = df_m[col]
                        if (temp_1.iloc[index]) & (df_m.screen_name.iloc[index] == col):
                            df_m.auto.iloc[index] = 1
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_c = df_m2.drop(
                columns=["created_at", "description", "text", "tweet_id", "auto"]
            ).groupby("screen_name")
            df_med_c = df_med_c.sum().T

            df_med_c = pd.DataFrame(df_med_c.T.sum())
            df_med_c = df_med_c.reset_index()
            df_med_c = df_med_c.rename(columns={0: "mentions", "index": "media"})
            df_med_c = df_med_c.sort_values("mentions", ascending=False)
            df_med_c = df_med_c.reset_index(drop=True)

        except KeyError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            traceback.print_exc()

            df_med_c = df_empty_c

        except AttributeError as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            traceback.print_exc()

            df_med_c = df_empty_c

        except Exception as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            traceback.print_exc()

            df_med_c = df_empty_c

        return df_med_c

    def id_pres_tw(self):
        """Twitter media presence
        calculates Twitter only number of appearances

        Returns
        -------
        df_med_id
        TYPE dataframe
            DESCRIPTION. each count number of appearances in Twitter

        """
        col_med = [
            "created_at",
            "description",
            "text",
            "tweet_id",
            "in_reply_to_status_id",
            "screen_name",
        ]

        df_tw = self.df_tw
        df_c = self.df_count
        brand = self.brand
        auto_n = self.auto_n
        thread = self.thread
        df_empty_id = pd.DataFrame(
            columns=["created_at", "text", "screen_name", "tweet_id"]
        )
        method_name = "id_pres_tw"

        try:
            df_tw = df_tw[col_med]
            df_tw = deepcopy(df_tw)
            df_tw.created_at = pd.to_datetime(df_tw.created_at)

            df_tw.text = df_tw.text.apply(lambda x: str(x))
            df_tw.text = df_tw.text.apply(lambda x: x.lower())

            df_m = deepcopy(df_tw)
            for idd, row in df_c.set_index("nombre").iterrows():
                if idd:
                    account_terms_regex = create_regex(
                        [t.strip() for t in row.terminos.split(",")]
                    )
                    df_m[f"{idd}"] = df_m["text"].str.contains(
                        account_terms_regex, regex=True
                    )

            df_m["auto"] = 0

            if auto_n:
                col_names = df_m.columns[6:-1]
                for col in col_names:
                    for index in range(len(df_m)):
                        temp_1 = df_m[col]
                        if (temp_1.iloc[index]) & (df_m.screen_name.iloc[index] == col):
                            df_m.auto.iloc[index] = 1
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_id = df_m2[
                [
                    "created_at",
                    "text",
                    "screen_name",
                    "tweet_id",
                    "in_reply_to_status_id",
                    brand,
                ]
            ]
            df_med_id = df_med_id[df_med_id[brand]]
            df_med_id = df_med_id.drop(columns=brand)
            df_med_id = df_med_id.reset_index(drop=True)

            if thread:
                df_med_id_th = thread_mention(df_med_id)
                df_med_id_th = df_med_id_th.drop(columns="in_reply_to_status_id")
            else:
                df_med_id_th = deepcopy(df_med_id)
                df_med_id_th = df_med_id_th.drop(columns="in_reply_to_status_id")

        except KeyError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            traceback.print_exc()

            df_med_id_th = df_empty_id

        except AttributeError as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            traceback.print_exc()

            df_med_id_th = df_empty_id

        except Exception as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            traceback.print_exc()

            df_med_id_th = df_empty_id

        return df_med_id_th
