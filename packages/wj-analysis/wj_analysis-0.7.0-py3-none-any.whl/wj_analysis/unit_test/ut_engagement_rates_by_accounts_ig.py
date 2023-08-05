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

import wj_analysis.instagram.engagement_rates as IG

pd.options.mode.chained_assignment = None

groups_ig = {}

FOLDER = "D:/whale_jaguar/datos_redes_sociales/Informes_020421/Instagram/"

df_pages = pd.read_csv(FOLDER + "instagram_lib_profile.csv", low_memory=False)
df_posts = pd.read_csv(FOLDER + "instagram_lib_posts.csv", low_memory=False)

print("ut_effec_moments_ig.py")
print("post = " + str(len(df_posts)))
print("brands = " + str(len(df_posts.owner_id.unique())))
print("================================================")


class Test(unittest.TestCase):
    def setUp(self):
        """
        Variables to use in tests

        Returns
        -------
        None.

        """
        erfb = IG.EngagementRateIG(df_posts, df_pages, groups=groups_ig)
        self.df_ef_post = erfb.by_post()
        self.df_ef_account = erfb.by_accounts()
        self.df_pages_empty = pd.DataFrame(columns=df_pages.columns, dtype=object)
        self.df_posts_empty = pd.DataFrame(columns=df_posts.columns, dtype=object)

        brands = df_posts.groupby("owner_username", as_index=False).agg(
            {"owner_id": "last"}
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

        erfb_empty = IG.EngagementRateIG(
            self.df_posts_empty, self.df_pages_empty, groups=groups_ig
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

        print("nan in pages")
        df_pages_null = deepcopy(df_pages)
        array_ef = random.sample(
            list(range(len(df_pages_null))), len(df_pages_null) // 5
        )
        for i in array_ef:
            df_pages_null.date.iloc[i] = float("nan")
            df_pages_null.followers.iloc[i] = float("nan")

        erfb = IG.EngagementRateIG(df_posts, df_pages_null, groups=groups_ig)
        df_ef_acc_pa = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_pa), 0)

        print("nan in posts")
        df_post_null = deepcopy(df_posts)
        array_ef = random.sample(list(range(len(df_post_null))), len(df_post_null) // 5)
        for i in array_ef:
            # df_post_null.date_utc.iloc[i] = float("nan")
            df_post_null.owner_id.iloc[i] = float("nan")

        erfb = IG.EngagementRateIG(df_post_null, df_pages, groups=groups_ig)
        df_ef_acc_pa = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_pa), 0)

        print("nan in posts and pages")
        erfb = IG.EngagementRateIG(df_post_null, df_pages_null, groups=groups_ig)
        df_ef_acc_pa = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_pa), 0)

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

        print(brand1["owner_username"])
        df_pages_brand1 = df_pages[df_pages.userid == brand1["owner_id"]]
        df_posts_brand1 = df_posts[df_posts.owner_id == brand1["owner_id"]]
        erfb_brand1 = IG.EngagementRateIG(
            df_posts_brand1, df_pages_brand1, groups=groups_ig
        )
        df_ef_acc_brand1 = erfb_brand1.by_accounts()

        self.assertGreater(len(df_ef_acc_brand1), 0)

        print(brand2["owner_username"])
        df_pages_brand2 = df_pages[df_pages.userid == brand2["owner_id"]]
        df_posts_brand2 = df_posts[df_posts.owner_id == brand2["owner_id"]]
        erfb_brand2 = IG.EngagementRateIG(
            df_posts_brand2, df_pages_brand2, groups=groups_ig
        )
        df_ef_acc_brand2 = erfb_brand2.by_accounts()

        self.assertGreater(len(df_ef_acc_brand2), 0)

        print(brand3["owner_username"])
        df_pages_brand3 = df_pages[df_pages.userid == brand3["owner_id"]]
        df_posts_brand3 = df_posts[df_posts.owner_id == brand3["owner_id"]]
        erfb_brand3 = IG.EngagementRateIG(
            df_posts_brand3, df_pages_brand3, groups=groups_ig
        )
        df_ef_acc_brand3 = erfb_brand3.by_accounts()

        self.assertGreater(len(df_ef_acc_brand3), 0)

        print("================================================")


if __name__ == "__main__":
    unittest.main()
