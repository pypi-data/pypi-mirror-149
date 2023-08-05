#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:03:01 2020

@author: oscarprecensia
"""

import re as reg
from copy import deepcopy
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


COL_MED = ["date_published", "title", "text", "url", "source"]
ERR_SYS = "system error: "


def create_regex(list_terms):
    """
    This class extract @name from a list

    Parameters
    ----------
    list_terms : TYPE list
        DESCRIPTION. list with the text to apply

    Returns
    -------
    pat : TYPE list
        DESCRIPTION. list without @name

    """
    pattern = r"\b@*" + r"\b|\b@*".join(list_terms) + r"\b"
    pat = reg.compile(pattern)
    return pat


class MediaPres:
    def __init__(self, dfm, df_count, brand, auto_n=True):
        """Digital media presence
        This function calculates digital media presence, comparing it with the
        weight of each digital media

        Parameters
        ----------
        dfm : TYPE dataframe
            DESCRIPTION. Contains the information collected from digital media
        df_count : TYPE dataframe
            DESCRIPTION. Contains the media information to consult
        count : string
            DESCRIPTION. brand analyze
        auto_n : TYPE bolean
            DESCRIPTION. remove mentions of the same account if true

        Returns
        -------
        None.

        """

        self.df_m = dfm
        self.df_count = df_count
        self.brand = brand
        self.auto_n = auto_n

    def count_pres(self):
        """Digital count media presence
        calculates digital media presence, only number of appearances

        Returns
        -------
        df_med_c
        TYPE dataframe
            DESCRIPTION. each count number of appearances in digital media

        """

        df_all = self.df_m
        df_c = self.df_count
        auto_n = self.auto_n
        df_empty_c = pd.DataFrame(columns=["media", "mentions"])
        method_name = "count_pres"

        try:
            df_w = df_all[COL_MED]
            df_w = deepcopy(df_w)
            df_w.date_published = pd.to_datetime(df_w.date_published)
            df_w.text = df_w.text.apply(lambda x: str(x))
            df_w.text = df_w.text.apply(lambda x: x.lower())
            df_m = deepcopy(df_w)

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
                    temp_1 = df_m[col]
                    for index in range(len(df_m)):
                        if (temp_1[index] == True) & (df_m.source[index] == col):
                            df_m.auto.iloc[index] = 1
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_c = df_m2.drop(
                columns=["date_published", "title", "text", "auto"]
            ).groupby("source")
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

            df_med_c = df_empty_c

        except AttributeError as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_c = df_empty_c

        except Exception as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_c = df_empty_c

        return df_med_c

    def url_pres(self):
        """Digital url media presence
        shows the url where the brand appears

        Returns
        -------
        df_med_url
        TYPE dataframe
            DESCRIPTION. url where the brand appears

        """

        df_all = self.df_m
        df_c = self.df_count
        brand = self.brand
        auto_n = self.auto_n
        df_empty_url = pd.DataFrame(
            columns=["date_published", "source", "title", "url"]
        )
        method_name = "url_pres"

        try:
            df_w = df_all[COL_MED]
            df_w = deepcopy(df_w)
            df_w.date_published = pd.to_datetime(df_w.date_published)

            df_w.text = df_w.text.apply(lambda x: str(x))
            df_w.text = df_w.text.apply(lambda x: x.lower())

            df_m = deepcopy(df_w)
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
                        if (temp_1[index] == True) & (df_m.source[index] == col):
                            df_m.auto.iloc[index] = 1
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_url = df_m2[["date_published", "source", "title", "url", brand]]
            df_med_url = df_med_url[df_med_url[brand] == True]
            df_med_url = df_med_url.drop(columns=brand)
            df_med_url = df_med_url.reset_index(drop=True)

        except KeyError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_url = df_empty_url

        except AttributeError as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_url = df_empty_url

        except Exception as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_url = df_empty_url

        return df_med_url
