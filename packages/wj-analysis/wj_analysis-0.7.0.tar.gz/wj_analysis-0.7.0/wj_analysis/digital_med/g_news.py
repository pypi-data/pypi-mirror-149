#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 15:15:45 2021

@author: oscar
"""

import traceback
from copy import deepcopy
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


ERR_SYS = "system error: "

COLUMNS_DATA = [
    "headline",
    "text",
    "content",
    "url",
    "image",
    "created_at",
    "source.name",
    "word",
]


def words_filter(df_w, words, column, n_f):
    """
    words_filter

    Parameters
    ----------
    df_w : TYPE dataframe
        DESCRIPTION. dataframe with data from google-news
    words : TYPE array
        DESCRIPTION. array with the words to search
    column : TYPE, string
        DESCRIPTION. column to search word
    n_f : TYPE, string
        DESCRIPTION. return value word is not found
    Returns
    -------
    df_m_filter : TYPE dataframe
        DESCRIPTION. dataframe with column 'word'

    """

    df_m_filter_empty = pd.DataFrame(columns=COLUMNS_DATA)
    method_name = "GNews_words_filter"
    df_m = deepcopy(df_w)
    df_m["word"] = "-"

    if len(df_m) != 0:

        try:
            for i in range(len(df_m)):
                for word in words:
                    if str(df_m[column].iloc[i]).find(str(word)) > 0:
                        df_m.word.iloc[i] = str(word)
                    else:
                        continue

            df_m_filter = df_m[df_m.word != "-"]

            if len(df_m_filter) == 0:
                data_c = []
                row_c = 0
                while row_c < len(COLUMNS_DATA):
                    data_c.append(n_f)
                    row_c += 1
                df_m_filter = pd.DataFrame([data_c], columns=COLUMNS_DATA)

        except KeyError as e_1:
            print("==========================================================")
            print(e_1)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Method: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_m_filter = df_m_filter_empty

        except AttributeError as e_2:
            print("==========================================================")
            print(e_2)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Method: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_m_filter = df_m_filter_empty

        except Exception as e_3:
            print("==========================================================")
            print(e_3)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Method: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_m_filter = df_m_filter_empty
    else:
        print("Dataframe news empty!")
        df_m_filter = df_m_filter_empty

    return df_m_filter


def prepare_data(df_p, words, column, n_f):
    """
    prepare_data

    Parameters
    ----------
    df_p : TYPE dataframe
        DESCRIPTION. dataframe to search words
    words : TYPE array
        DESCRIPTION. array with the words to search
    column : TYPE, string
        DESCRIPTION. column to search word
    n_f : TYPE, string
        DESCRIPTION. return value word is not found

    Returns
    -------
    df_filter : TYPE dataframe
        DESCRIPTION. dataframe with column 'word'

    """
    df_filter_empty = pd.DataFrame(
        columns=[
            "headline",
            "text",
            "content",
            "url",
            "image",
            "created_at",
            "source",
            "word",
        ]
    )
    method_name = "GNews_prepare_data"

    try:
        df_p["created_at"] = pd.to_datetime(
            df_p["created_at"], format="%Y-%m-%d %H:%M:%S.%f"
        )
        df_filter = words_filter(df_w=df_p, words=words, column=column, n_f=n_f)
        df_filter = df_filter.drop_duplicates()

    except KeyError as e_1:
        print("==========================================================")
        print(e_1)
        print("==========================================================")
        print(ERR_SYS + str(exc_info()[0]))
        print("==========================================================")
        print(f"Method: {method_name}")
        print("==========================================================")
        traceback.print_exc()

        df_filter = df_filter_empty

    except AttributeError as e_2:
        print("==========================================================")
        print(e_2)
        print("==========================================================")
        print(ERR_SYS + str(exc_info()[0]))
        print("==========================================================")
        print(f"Method: {method_name}")
        print("==========================================================")
        traceback.print_exc()

        df_filter = df_filter_empty

    except Exception as e_3:
        print("==========================================================")
        print(e_3)
        print("==========================================================")
        print(ERR_SYS + str(exc_info()[0]))
        print("==========================================================")
        print(f"Method: {method_name}")
        print("==========================================================")
        traceback.print_exc()

        df_filter = df_filter_empty

    return df_filter


class GNews:
    """
    This class search words in Gnews data
    """

    def __init__(self, df_g, query, column="text", n_f="not_found"):
        """


        Parameters
        ----------
        df_g : TYPE dataframe
            DESCRIPTION. dataframe with columns:
            'headline', 'text', 'content', 'url', 'image', 'created_at', 'source.name'
        query : TYPE array
            DESCRIPTION. array with the words to search
        column : TYPE, optional
            DESCRIPTION. The default is 'text' column to search word
        n_f : TYPE, optional
            DESCRIPTION. The default is 'not_found' return value word is not found

        Returns
        -------
        None.

        """

        self.df_g = df_g
        self.query = query
        self.n_f = n_f
        self.column = column
        self.df_filter = prepare_data(df_p=df_g, words=query, column=column, n_f=n_f)

    def count_pres(self):
        """
        count_pres

        Returns
        -------
        df_filter_c : TYPE dataframe
            DESCRIPTION. dataframe with words and count by word

        """
        df_filter_c = self.df_filter
        df_filter_c_empty = pd.DataFrame(columns=["word", "count"])
        method_name = "count_pres"

        try:

            df_filter_c = df_filter_c.groupby("word", as_index=False).agg(
                {"headline": "count"}
            )
            df_filter_c = df_filter_c.rename(columns={"headline": "count"})

        except KeyError as e_1:
            print("==========================================================")
            print(e_1)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_filter_c = df_filter_c_empty

        except AttributeError as e_2:
            print("==========================================================")
            print(e_2)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_filter_c = df_filter_c_empty

        except Exception as e_3:
            print("==========================================================")
            print(e_3)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_filter_c = df_filter_c_empty

        return df_filter_c

    def url_pres(self):
        """
        url_pres

        Returns
        -------
        df_filter_u : TYPE dataframe
            DESCRIPTION. dataframe with word match and columns 'created_at',
            'source.name', 'word', 'url', 'headline'

        """
        df_filter_u = self.df_filter
        df_filter_u_empty = pd.DataFrame(
            columns=["created_at", "source.name", "word", "url", "headline"]
        )
        method_name = "url_pres"

        try:

            df_filter_u = df_filter_u.groupby("url", as_index=False).agg(
                {
                    "word": "last",
                    "created_at": "last",
                    "headline": "last",
                    "source.name": "last",
                }
            )
            df_filter_u = df_filter_u.sort_values("created_at").reset_index(drop=True)

        except KeyError as e_1:
            print("==========================================================")
            print(e_1)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_filter_u = df_filter_u_empty

        except AttributeError as e_2:
            print("==========================================================")
            print(e_2)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_filter_u = df_filter_u_empty

        except Exception as e_3:
            print("==========================================================")
            print(e_3)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_filter_u = df_filter_u_empty

        return df_filter_u
