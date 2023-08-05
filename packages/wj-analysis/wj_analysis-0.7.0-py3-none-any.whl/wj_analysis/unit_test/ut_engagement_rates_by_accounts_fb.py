#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:50:42 2021

@author: oscar
"""
import ast
import random
import unittest
from copy import deepcopy

import pandas as pd

import wj_analysis.facebook.engagement_rates as FB

pd.options.mode.chained_assignment = None

groups_fb = {}

FOLDER = "D:/whale_jaguar/datos_redes_sociales/Informes_020421/Facebook/"

df_pages = pd.read_csv(
    FOLDER + "facebook_lib_facebook_pages.csv", index_col=0, low_memory=False
)
df_posts = pd.read_csv(
    FOLDER + "facebook_lib_facebook_posts.csv", index_col=0, low_memory=False
)

print("ut_engegament_rate_fb.py")
print("post = " + str(len(df_posts)))
print("brands = " + str(len(df_posts.page_id.unique())))
print("================================================")


class Test(unittest.TestCase):
    def setUp(self):
        """
        Variables to use in tests

        Returns
        -------
        None.

        """
        erfb = FB.EngagementRateFB(df_posts, df_pages, groups=groups_fb)
        self.df_ef_account = erfb.by_accounts()
        self.df_ef_post = erfb.by_post()
        self.df_pages_empty = pd.DataFrame(columns=df_pages.columns, dtype=object)
        self.df_posts_empty = pd.DataFrame(columns=df_posts.columns, dtype=object)

        df_name = df_posts.post_from.apply(lambda x: ast.literal_eval(x))
        names = []
        for i in range(len(df_name)):
            temp_1 = df_name.iloc[i]["name"]
            names.append(temp_1)
        df_posts["self_name"] = names

        brands = df_posts.groupby("self_name", as_index=False).agg({"page_id": "last"})
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

        erfb_empty = FB.EngagementRateFB(
            self.df_posts_empty, self.df_pages_empty, groups=groups_fb
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
            df_pages_null.created_at.iloc[i] = float("nan")
            df_pages_null.fan_count.iloc[i] = float("nan")

        erfb = FB.EngagementRateFB(df_posts, df_pages_null, groups=groups_fb)
        df_ef_acc_pa = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_pa), 0)

        print("nan in posts")
        df_post_null = deepcopy(df_posts)
        array_ef = random.sample(list(range(len(df_post_null))), len(df_post_null) // 5)
        for i in array_ef:
            df_post_null.created_at.iloc[i] = float("nan")
            df_post_null.page_id.iloc[i] = float("nan")

        erfb = FB.EngagementRateFB(df_post_null, df_pages, groups=groups_fb)
        df_ef_acc_po = erfb.by_accounts()

        self.assertGreater(len(df_ef_acc_po), 0)

        print("nan in posts and pages")
        erfb = FB.EngagementRateFB(df_post_null, df_pages_null, groups=groups_fb)
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

        print(brand1["self_name"])
        df_pages_brand1 = df_pages[df_pages.page_id == brand1["page_id"]]
        df_posts_brand1 = df_posts[df_posts.page_id == brand1["page_id"]]
        erfb_brand1 = FB.EngagementRateFB(
            df_posts_brand1, df_pages_brand1, groups=groups_fb
        )
        df_ef_acc_brand1 = erfb_brand1.by_accounts()

        self.assertGreater(len(df_ef_acc_brand1), 0)

        print(brand2["self_name"])
        df_pages_brand2 = df_pages[df_pages.page_id == brand2["page_id"]]
        df_posts_brand2 = df_posts[df_posts.page_id == brand2["page_id"]]
        erfb_brand2 = FB.EngagementRateFB(
            df_posts_brand2, df_pages_brand2, groups=groups_fb
        )
        df_ef_acc_brand2 = erfb_brand2.by_accounts()

        self.assertGreater(len(df_ef_acc_brand2), 0)

        print(brand3["self_name"])
        df_pages_brand3 = df_pages[df_pages.page_id == brand3["page_id"]]
        df_posts_brand3 = df_posts[df_posts.page_id == brand3["page_id"]]
        erfb_brand3 = FB.EngagementRateFB(
            df_posts_brand3, df_pages_brand3, groups=groups_fb
        )
        df_ef_acc_brand3 = erfb_brand3.by_accounts()

        self.assertGreater(len(df_ef_acc_brand3), 0)

        print("================================================")


if __name__ == "__main__":
    unittest.main()
