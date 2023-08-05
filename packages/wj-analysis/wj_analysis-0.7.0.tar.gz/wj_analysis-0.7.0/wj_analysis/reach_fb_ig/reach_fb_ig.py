#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 19:27:23 2021

@author: oscar
"""

import ast
import traceback
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


ERR_SYS = "system error: "

POSTS_COLUMNS_FB = ["post_from", "post_id", "created_time", "permalink_url"]
EMPTY_COLUMNS_FB = [
    "post_id",
    "created_time",
    "name",
    "post_impressions",
    "post_impressions_unique",
    "post_impressions_paid",
    "post_impressions_paid_unique",
    "post_impressions_fan",
    "post_impressions_fan_unique",
    "post_impressions_fan_paid",
    "post_impressions_fan_paid_unique",
    "post_impressions_organic",
    "post_impressions_organic_unique",
    "post_impressions_viral",
    "post_impressions_viral_unique",
    "post_impressions_nonviral",
    "post_impressions_nonviral_unique",
    "post_impressions_by_story_type",
    "post_impressions_by_story_type_unique",
]

POSTS_COLUMNS_IG = ["owner_username", "shortcode", "date_utc", "url"]
EMPTY_COLUMNS_IG = [
    "shortcode",
    "date_utc",
    "name",
    "impressions",
    "reach",
    "engagement",
]
COLUMNS_SD_IG = [
    "carousel_album_engagement",
    "carousel_album_impressions",
    "carousel_album_reach",
    "carousel_album_saved",
    "carousel_album_video_views",
]


class ReachFaceInst:
    """
    This class match posts to reach
    """

    def __init__(self, df_post, df_ins, social_n="fb", url=False):
        """
        This method joins the information of publications with the information of insights,
        reads the information of several brands, in list format is important

        Parameters
        ----------
        df_post : TYPE dataframe
            DESCRIPTION. posts information
        df_ins : TYPE dataframe
            DESCRIPTION. insights information
        social_n : TYPE string
            DESCRIPTION. indicates social network, 'fb': Facebook, 'ig': Instagram
        url : TYPE string
            DESCRIPTION. is True if load post url.

        Returns
        -------
        None.

        """

        self.df_post = df_post
        self.df_ins = df_ins
        self.social_n = social_n
        self.url = url

    def reach(self):
        """
        joint informtion posts and insights

        Returns
        -------
        df_reach : TYPE dataframe
            DESCRIPTION. dataframe whit reach, brand, date and post_id.

        """

        df_post = self.df_post
        df_ins = self.df_ins
        social_n = self.social_n
        url = self.url
        method_name = "reach Facebook Instagram"

        try:

            if social_n == "fb":
                if url:
                    EMPTY_COLUMNS_FB.append("permalink_url")

                empty_columns = EMPTY_COLUMNS_FB
                posts_columns = POSTS_COLUMNS_FB
                post_from = "post_from"
                on_id = "post_id"
                name = "name"

                df_reach_empty = pd.DataFrame(columns=empty_columns)

                if df_post[post_from].isna().values.any():
                    df_post = df_post[df_post[post_from].notna()]

                brand_name = df_post[post_from].apply(lambda x: ast.literal_eval(x))
                name_list = []
                for i in range(len(df_post)):
                    temp_3 = brand_name.iloc[i][name]
                    name_list.append(temp_3)

                df_post = df_post[posts_columns]
                df_post = df_post.drop(columns="post_from")
                df_post[name] = name_list

            elif social_n == "ig":

                sidecar = len(set(COLUMNS_SD_IG).intersection(list(df_ins.columns))) > 0

                if sidecar:

                    df_ins = df_ins.rename(
                        columns={
                            "carousel_album_engagement": "engagement",
                            "carousel_album_impressions": "impressions",
                            "carousel_album_reach": "reach",
                        }
                    )

                if url:
                    EMPTY_COLUMNS_IG.append("url")

                df_post = df_post.rename(columns={"owner_username": "name"})
                empty_columns = EMPTY_COLUMNS_IG
                posts_columns = POSTS_COLUMNS_IG
                post_from = "shortcode"
                on_id = "shortcode"
                name = "name"

                df_reach_empty = pd.DataFrame(columns=empty_columns)

                if df_post[post_from].isna().values.any():
                    df_post = df_post[df_post[post_from].notna()]

            else:
                print(f"{social_n} is not a valid value")

            df_reach = pd.merge(df_post, df_ins, on=on_id, how="outer")
            df_reach = df_reach[empty_columns]
            df_reach = df_reach.dropna().reset_index(drop=True)

        except KeyError as e_1:
            print("".center(60, "="))
            print(e_1)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("".center(60, "="))
            traceback.print_exc()

            df_reach = df_reach_empty

        except AttributeError as e_2:
            print("".center(60, "="))
            print(e_2)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("".center(60, "="))
            traceback.print_exc()

            df_reach = df_reach_empty

        except Exception as e_3:
            print("".center(60, "="))
            print(e_3)
            print("".center(60, "="))
            print(ERR_SYS + str(exc_info()[0]))
            print("".center(60, "="))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("".center(60, "="))
            traceback.print_exc()

            df_reach = df_reach_empty

        return df_reach
