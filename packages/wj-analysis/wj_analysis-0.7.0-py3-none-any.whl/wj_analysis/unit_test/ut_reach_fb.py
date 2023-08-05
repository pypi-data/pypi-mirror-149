#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:32:33 2021

@author: oscar
"""

import random
import unittest

import pandas as pd

from wj_analysis.reach_fb_ig.reach_fb_ig import ReachFaceInst

FOLDER = "/home/oscar/MEGA/W&J/Insigths_PWJ-1827/Data/"
FILES_INS = ["insights_mov.csv", "insights_wyj.csv"]
FILES_POST = [
    "facebook_lib_facebook_posts_Mov.csv",
    "facebook_lib_facebook_posts_WYJ.csv",
]

SOCIAL_N = "fb"

BRAND = random.sample(range(len(FILES_POST)), 1)

COLUMNS_POST = ["post_from", "post_id", "created_time", "permalink_url"]

DFP = FILES_POST[int(BRAND[0])]
DFI = FILES_INS[int(BRAND[0])]

DF_POST = pd.read_csv(FOLDER + DFP, usecols=COLUMNS_POST)
DF_INS = pd.read_csv(FOLDER + DFI, index_col=0)

print("================================================")
print("ut_reach_FB.py")
print("post = " + str(len(DF_INS)))
print("================================================")


class Test(unittest.TestCase):
    def setUp(self):
        """
        Variables to use in tests

        Returns
        -------
        None.

        """

        self.df_post = DF_POST
        self.df_ins = DF_INS
        self.social_n = SOCIAL_N

    def test_data_normal(self):
        """
        This test with data ok

        Returns
        -------
        None.

        """
        print("TEST_DATA_NORMAL...")

        df_post = self.df_post
        df_ins = self.df_ins
        social_n = self.social_n

        df_reach = ReachFaceInst(
            df_post=df_post, df_ins=df_ins, social_n=social_n
        ).reach()

        self.assertGreater(len(df_reach), 0)

        print("================================================")

    def test_data_empty(self):
        """
        This test with data empty

        Returns
        -------
        None.

        """
        print("TEST_DATA_EMPTY...")

        df_post = self.df_post
        df_ins = self.df_ins
        social_n = self.social_n

        df_post_empty = pd.DataFrame(columns=df_post.columns)

        df_ins_empty = pd.DataFrame(columns=df_ins.columns)

        df_reach_empty = ReachFaceInst(
            df_post=df_post_empty, df_ins=df_ins, social_n=social_n, url=True
        ).reach()
        df_reach_empty_post = ReachFaceInst(
            df_post=df_post_empty, df_ins=df_ins, social_n=social_n, url=True
        ).reach()
        df_reach_empty_ins = ReachFaceInst(
            df_post=df_post, df_ins=df_ins_empty, social_n=social_n, url=True
        ).reach()

        self.assertEqual(len(df_reach_empty), 0)
        self.assertEqual(len(df_reach_empty_post), 0)
        self.assertEqual(len(df_reach_empty_ins), 0)

        print("================================================")

    def test_nan_data(self):
        """
        This test with data 20% nan

        Returns
        -------
        None.

        """
        print("TEST_NAN_DATA...")

        df_post = self.df_post
        df_ins = self.df_ins
        social_n = self.social_n

        df_post_nan = df_post
        column_sample = random.sample(list(df_post_nan.columns), 1)
        array_ef = random.sample(list(range(len(df_post_nan))), len(df_post_nan) // 5)
        for k in array_ef:
            df_post_nan["post_id"].iloc[k] = float("nan")
            df_post_nan[column_sample[0]].iloc[k] = float("nan")

        df_ins_nan = df_ins
        column_sample = random.sample(list(df_ins_nan.columns), 1)
        array_ef = random.sample(list(range(len(df_ins_nan))), len(df_ins_nan) // 5)
        for k in array_ef:
            df_ins_nan["post_id"].iloc[k] = float("nan")
            df_ins_nan[column_sample[0]].iloc[k] = float("nan")

        df_reach_nan = ReachFaceInst(
            df_post=df_post_nan, df_ins=df_ins_nan, social_n=social_n
        ).reach()
        df_reach_nan_post = ReachFaceInst(
            df_post=df_post_nan, df_ins=df_ins, social_n=social_n
        ).reach()
        df_reach_nan_ins = ReachFaceInst(
            df_post=df_post, df_ins=df_ins_nan, social_n=social_n
        ).reach()

        self.assertGreater(len(df_reach_nan), 0)
        self.assertGreater(len(df_reach_nan_post), 0)
        self.assertGreater(len(df_reach_nan_ins), 0)

        print("================================================")

    def test_no_column(self):
        """
        This test three columns are removed

        Returns
        -------
        None.

        """
        print("TEST_NO_COLUMNS...")

        df_post = self.df_post
        df_ins = self.df_ins
        social_n = self.social_n

        df_post_no_col = df_post
        df_post_no_col = df_post_no_col.drop(columns=["post_id"])

        df_ins_no_col = df_ins
        df_ins_no_col = df_ins_no_col.drop(columns=["post_id"])

        df_reach_no_col = ReachFaceInst(
            df_post=df_post_no_col, df_ins=df_ins_no_col, social_n=social_n
        ).reach()
        df_reach_no_col_post = ReachFaceInst(
            df_post=df_post_no_col, df_ins=df_ins, social_n=social_n
        ).reach()
        df_reach_no_col_ins = ReachFaceInst(
            df_post=df_post, df_ins=df_ins_no_col, social_n=social_n
        ).reach()

        self.assertEqual(len(df_reach_no_col), 0)
        self.assertEqual(len(df_reach_no_col_post), 0)
        self.assertEqual(len(df_reach_no_col_ins), 0)


if __name__ == "__main__":
    unittest.main()
