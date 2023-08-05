#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:50:42 2021

@author: oscar
"""
import random
import unittest
from copy import deepcopy

import pandas as pd

import wj_analysis.twitter.engagement_rates as TW

pd.options.mode.chained_assignment = None

groups_tw = {}

FOLDER = "D:/whale_jaguar/datos_redes_sociales/Informes_020421/Twitter/"

df_posts = pd.read_csv(FOLDER + "twitter_lib_tweet.csv", low_memory=False)
df_com = pd.read_csv(
    FOLDER + "twitter_lib_tweetreply.csv", low_memory=False, lineterminator="\n"
)


print("ut_effec_moments_tw.py")
print("post = " + str(len(df_posts)))
print("brands = " + str(len(df_posts.twitter_id.unique())))
print("================================================")


class Test(unittest.TestCase):
    def setUp(self):
        """
        Variables to use in tests

        Returns
        -------
        None.

        """
        erfb = TW.EngagementRateTW(df_posts, df_com, groups=groups_tw)
        self.df_ef_post = erfb.by_post()
        self.df_ef_account = erfb.by_accounts()
        self.df_com_empty = pd.DataFrame(columns=df_com.columns, dtype=object)
        self.df_posts_empty = pd.DataFrame(columns=df_posts.columns, dtype=object)

        brands = df_posts.groupby("screen_name", as_index=False).agg(
            {"twitter_id": "last"}
        )
        self.brands = brands.to_dict(orient="index")
        self.brand_sample = random.sample(list(range(len(brands))), 3)

    def test_data_normal(self):
        """
        This test with data ok

        Returns
        -------
        None.

        """
        print("TEST_DATA_NORMAL...")

        self.assertGreater(len(self.df_ef_account), 0)

        print("================================================")

    def test_data_empty(self):
        """
        This test with data empty

        Returns
        -------
        None.

        """
        print("TEST_DATA_EMPTY...")

        erfb_empty = TW.EngagementRateTW(
            self.df_posts_empty, self.df_com_empty, groups=groups_tw
        )
        df_ef_account = erfb_empty.by_accounts()
        self.assertAlmostEqual(len(df_ef_account), 0)

        print("================================================")

    def test_nan_data(self):
        """
        This test with data 20% null

        Returns
        -------
        None.

        """
        print("TEST_NAN_DATA...")

        print("nan in comments")
        df_com_null = deepcopy(df_com)
        array_ef = random.sample(list(range(len(df_com_null))), len(df_com_null) // 5)
        for i in array_ef:
            df_com_null.created_at.iloc[i] = float("nan")
            df_com_null.ac_followers_count.iloc[i] = float("nan")

        erfb = TW.EngagementRateTW(df_posts, df_com, groups=groups_tw)
        df_ef_acc_pa = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_pa), 0)

        print("nan in posts")
        df_post_null = deepcopy(df_posts)
        array_ef = random.sample(list(range(len(df_post_null))), len(df_post_null) // 5)
        for i in array_ef:
            df_post_null.created_at.iloc[i] = float("nan")
            df_post_null.tweet_id.iloc[i] = float("nan")

        erfb = TW.EngagementRateTW(df_post_null, df_com_null, groups=groups_tw)
        df_ef_acc_po = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_po), 0)

        print("nan in posts and pages")
        erfb = TW.EngagementRateTW(df_post_null, df_com_null, groups=groups_tw)
        df_ef_acc_all = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_all), 0)

        print("================================================")

    def test_brands(self):
        """
        Test with data from three brands chosen at random

        Returns
        -------
        None.

        """
        print("TEST_BRANDS...")

        brand1 = self.brands[self.brand_sample[0]]
        brand2 = self.brands[self.brand_sample[1]]
        brand3 = self.brands[self.brand_sample[2]]

        print(brand1["screen_name"])
        df_com_brand1 = df_com[df_com.twitter_id == brand1["twitter_id"]]
        df_posts_brand1 = df_posts[df_posts.twitter_id == brand1["twitter_id"]]
        erfb_brand1 = TW.EngagementRateTW(
            df_posts_brand1, df_com_brand1, groups=groups_tw
        )
        df_ef_acc_brand1 = erfb_brand1.by_accounts()

        if len(df_com_brand1) == 0:
            self.assertAlmostEqual(len(df_ef_acc_brand1), 0)
        else:
            self.assertGreater(len(df_ef_acc_brand1), 0)

        print(brand2["screen_name"])
        df_com_brand2 = df_com[df_com.twitter_id == brand2["twitter_id"]]
        df_posts_brand2 = df_posts[df_posts.twitter_id == brand2["twitter_id"]]
        erfb_brand2 = TW.EngagementRateTW(
            df_posts_brand2, df_com_brand2, groups=groups_tw
        )
        df_ef_acc_brand2 = erfb_brand2.by_accounts()

        if len(df_com_brand2) == 0:
            self.assertAlmostEqual(len(df_ef_acc_brand2), 0)
        else:
            self.assertGreater(len(df_ef_acc_brand2), 0)

        print(brand3["screen_name"])
        df_com_brand3 = df_com[df_com.twitter_id == brand3["twitter_id"]]
        df_posts_brand3 = df_posts[df_posts.twitter_id == brand3["twitter_id"]]
        erfb_brand3 = TW.EngagementRateTW(
            df_posts_brand3, df_com_brand3, groups=groups_tw
        )
        df_ef_acc_brand3 = erfb_brand3.by_accounts()

        if len(df_com_brand3) == 0:
            self.assertAlmostEqual(len(df_ef_acc_brand3), 0)
        else:
            self.assertGreater(len(df_ef_acc_brand3), 0)

        print("================================================")


if __name__ == "__main__":
    unittest.main()
