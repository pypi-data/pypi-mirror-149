#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:26:06 2020

@author: oscar
"""

import ast
import re as reg
from copy import deepcopy
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


COL_MED = ["created_time", "message", "post_id", "description", "name_id"]
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


def extrac_name(df_n):
    """Extract name
    this function extracts the name of the post_from column

    Parameters
    ----------
    df : TYPE dataframe
        DESCRIPTION. dataframe with the column post_from

    Returns
    -------
    df : TYPE dataframe
        DESCRIPTION. dataframe with the name

    """
    df_name = df_n.post_from.apply(lambda x: ast.literal_eval(x))
    df_clean = []
    for i in range(len(df_n)):
        temp_1 = df_name.iloc[i]["name"]
        df_clean.append(temp_1)
    df_n["name_id"] = df_clean
    df_n = df_n.drop(columns="post_from")
    return df_n


class SocialpresFB:
    def __init__(self, df_fb, df_count, brand, auto_n=True):
        """Digital social presence
        This function calculates social presence in facebook, comparing it with the
        weight of each digital media

        Parameters
        ----------
        df_fb : TYPE dataframe
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

        self.df_fb = df_fb
        self.df_count = df_count
        self.brand = brand
        self.auto_n = auto_n

    def c_pres_fb(self):
        """Social media presence
        calculates Facebook only number of appearances

        Returns
        -------
        df_med_c
        TYPE dataframe
            DESCRIPTION. each count number of appearances in Facebook

        """

        df_org = self.df_fb
        df_c = self.df_count
        auto_n = self.auto_n
        df_empty_c = pd.DataFrame(columns=["media", "mentions"])
        method_name = "c_pres_fb"

        try:
            df_org = extrac_name(df_org)
            df_org = df_org[COL_MED]
            df_org = deepcopy(df_org)
            df_org.created_time = pd.to_datetime(df_org.created_time)

            df_org.message = df_org.message.apply(lambda x: str(x))
            df_org.message = df_org.message.apply(lambda x: x.lower())

            df_m = deepcopy(df_org)
            for idd, row in df_c.set_index("nombre").iterrows():
                if idd:
                    account_terms_regex = create_regex(
                        [t.strip() for t in row.terminos.split(",")]
                    )
                    df_m[f"{idd}"] = df_m["message"].str.contains(
                        account_terms_regex, regex=True
                    )

            df_m["auto"] = 0

            if auto_n:
                col_names = df_m.columns[5:-1]
                for col in col_names:
                    for index in range(len(df_m)):
                        temp_1 = df_m[col]
                        if (temp_1[index] == True) & (df_m.name_id[index] == col):
                            df_m.auto.iloc[index] = 1
                        else:
                            continue
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_c = df_m2.drop(
                columns=["created_time", "message", "description", "post_id", "auto"]
            ).groupby("name_id")
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

    def id_pres_fb(self):
        """Instagram media presence
        calculates Instagram only number of appearances

        Returns
        -------
        df_med_id
        TYPE dataframe
            DESCRIPTION. each count number of appearances in Instagram

        """

        df_org = self.df_fb
        df_c = self.df_count
        brand = self.brand
        auto_n = self.auto_n
        df_empty_id = pd.DataFrame(
            columns=["created_time", "message", "name_id", "post_id"]
        )
        method_name = "url_pres"

        try:

            df_org = extrac_name(df_org)
            df_org = df_org[COL_MED]
            df_org.created_time = pd.to_datetime(df_org.created_time)

            df_org.message = df_org.message.apply(lambda x: str(x))
            df_org.message = df_org.message.apply(lambda x: x.lower())

            df_m = deepcopy(df_org)
            for idd, row in df_c.set_index("nombre").iterrows():
                if idd:
                    account_terms_regex = create_regex(
                        [t.strip() for t in row.terminos.split(",")]
                    )
                    df_m[f"{idd}"] = df_m["message"].str.contains(
                        account_terms_regex, regex=True
                    )

            df_m["auto"] = 0

            if auto_n:
                col_names = df_m.columns[5:-1]
                for col in col_names:
                    for index in range(len(df_m)):
                        temp_1 = df_m[col]
                        if (temp_1[index] == True) & (df_m.name_id[index] == col):
                            df_m.auto.iloc[index] = 1
                        else:
                            continue
                df_m2 = df_m[df_m.auto == 0]
                df_m2 = df_m2.reset_index(drop=True)
            else:
                df_m2 = df_m

            df_med_id = df_m2[["created_time", "message", "name_id", "post_id", brand]]
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
