#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:26:06 2020

@author: oscar
"""


import re as reg
from copy import deepcopy
from sys import exc_info

import pandas as pd

COL_MED = ["date_local", "typename", "caption", "shortcode", "owner_username"]
ERR_SYS = "system error: "


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


class SocialpresIG:
    def __init__(self, df_ig, df_count, brand, auto_n=True):
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

        Returns
        -------
        None.

        """

        self.df_ig = df_ig
        self.df_count = df_count
        self.brand = brand
        self.auto_n = auto_n

    def c_pres_ig(self):
        """Social media presence
        calculates Instagram only number of appearances

        Returns
        -------
        df_med_c
        TYPE dataframe
            DESCRIPTION. each count number of appearances in Instagram

        """

        df_ig = self.df_ig
        df_c = self.df_count
        auto_n = self.auto_n
        df_empty_c = pd.DataFrame(columns=["media", "mentions"])
        method_name = "c_pres_ig"

        try:
            df_ig = df_ig[COL_MED]
            df_ig = deepcopy(df_ig)
            df_ig.date_local = pd.to_datetime(df_ig.date_local)

            df_ig.caption = df_ig.caption.apply(lambda x: str(x))
            df_ig.caption = df_ig.caption.apply(lambda x: x.lower())

            df_m = deepcopy(df_ig)
            for idd, row in df_c.set_index("nombre").iterrows():
                if idd:
                    account_terms_regex = create_regex(
                        [t.strip() for t in row.terminos.split(",")]
                    )
                    df_m[f"{idd}"] = df_m["caption"].str.contains(
                        account_terms_regex, regex=True
                    )

            df_m["auto"] = 0

            if auto_n:
                col_names = df_m.columns[5:-1]
                for col in col_names:
                    for index in range(len(df_m)):
                        temp_1 = df_m[col]
                        if (temp_1[index] == True) & (
                            df_m.owner_username[index] == col
                        ):
                            df_m.auto.iloc[index] = 1
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_c = df_m2.drop(
                columns=["date_local", "typename", "caption", "shortcode", "auto"]
            ).groupby("owner_username")
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

    def id_pres_ig(self):
        """Instagram media presence
        calculates Instagram only number of appearances

        Returns
        -------
        df_med_id
        TYPE dataframe
            DESCRIPTION. each count number of appearances in Instagram

        """

        df_ig = self.df_ig
        df_c = self.df_count
        brand = self.brand
        auto_n = self.auto_n
        df_empty_id = pd.DataFrame(
            columns=["date_local", "caption", "owner_username", "shortcode"]
        )
        method_name = "id_pres_ig"

        try:
            df_ig = df_ig[COL_MED]
            df_ig = deepcopy(df_ig)
            df_ig.date_local = pd.to_datetime(df_ig.date_local)

            df_ig.caption = df_ig.caption.apply(lambda x: str(x))
            df_ig.caption = df_ig.caption.apply(lambda x: x.lower())

            df_m = deepcopy(df_ig)
            for idd, row in df_c.set_index("nombre").iterrows():
                if idd:
                    account_terms_regex = create_regex(
                        [t.strip() for t in row.terminos.split(",")]
                    )
                    df_m[f"{idd}"] = df_m["caption"].str.contains(
                        account_terms_regex, regex=True
                    )

            df_m["auto"] = 0

            if auto_n:
                col_names = df_m.columns[5:-1]
                for col in col_names:
                    for index in range(len(df_m)):
                        temp_1 = df_m[col]
                        if (temp_1[index] == True) & (
                            df_m.owner_username[index] == col
                        ):
                            df_m.auto.iloc[index] = 1
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_id = df_m2[
                ["date_local", "caption", "owner_username", "shortcode", brand]
            ]
            df_med_id = df_med_id[df_med_id[brand] == True]
            df_med_id = df_med_id.drop(columns=brand)
            df_med_id = df_med_id.reset_index(drop=True)

        except KeyError as e_1:
            print(e_1)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_id = df_empty_id

        except AttributeError as e_2:
            print(e_2)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_id = df_empty_id

        except Exception as e_3:
            print(e_3)
            print(ERR_SYS + str(exc_info()[0]))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")

            df_med_id = df_empty_id

        return df_med_id
