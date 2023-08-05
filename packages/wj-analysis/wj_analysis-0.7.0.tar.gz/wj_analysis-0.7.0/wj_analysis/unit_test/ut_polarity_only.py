#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  19 17:50:42 2021

@author: oscar
"""
import os
import unittest

import pandas as pd

from wj_analysis.common.nlp_utils import CleanText, Polarity

pd.options.mode.chained_assignment = None

sample_data = 100

FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df_com_fb = pd.read_csv(
    FOLDER
    + "/Pruebas_OR/Pruebas_clases/test_develop/Informes_030521/Facebook/facebook_lib_facebook_comments.csv",
    low_memory=False,
)

df_com_ig = pd.read_csv(
    FOLDER
    + "/Pruebas_OR/Pruebas_clases/test_develop/Informes_030521/Instagram/instagram_lib_comment.csv",
    low_memory=False,
)

df_com_tw = pd.read_csv(
    FOLDER
    + "/Pruebas_OR/Pruebas_clases/test_develop/Informes_030521/Twitter/twitter_lib_tweetreply.csv",
    low_memory=False,
    lineterminator="\n",
)

print("".center(60, "="))
print("ut_polarity_only.py")
print("comments = " + str(sample_data * 3))
print("".center(60, "="))


class Test(unittest.TestCase):
    def setUp(self):
        """
        Variables to use in tests

        Returns
        -------
        None.

        """

        self.df_com_s_fb = df_com_fb.sample(n=sample_data)
        self.df_com_s_fb["processed_text"] = self.df_com_s_fb["message"].apply(
            lambda msg: CleanText(msg).process_text(
                mentions=True, hashtags=True, links=True, spec_chars=True
            )
        )

        self.df_com_s_ig = df_com_ig.sample(n=sample_data)
        self.df_com_s_ig["processed_text"] = self.df_com_s_ig["text"].apply(
            lambda msg: CleanText(msg).process_text(
                mentions=True, hashtags=True, links=True, spec_chars=True
            )
        )

        self.df_com_s_tw = df_com_tw.sample(n=sample_data)
        self.df_com_s_tw["processed_text"] = self.df_com_s_tw["text"].apply(
            lambda msg: CleanText(msg).process_text(
                mentions=True, hashtags=True, links=True, spec_chars=True
            )
        )

        self.df_empty = pd.DataFrame(columns=self.df_com_s_tw.columns)

    def test_data_normal(self):
        """
        This test with data ok

        Returns
        -------
        None.

        """
        print("".center(60, "="))
        print("TEST_DATA_NORMAL...")
        df_fb_normal = self.df_com_s_fb
        print(df_fb_normal.head(5))
        df_ig_normal = self.df_com_s_ig
        df_tw_normal = self.df_com_s_tw

        df_fb_normal = Polarity().polarity(df_text=df_fb_normal)
        df_ig_normal = Polarity().polarity(df_text=df_ig_normal)
        df_tw_normal = Polarity().polarity(df_text=df_tw_normal)

        # valida dataframe no vacio
        self.assertGreater(len(df_fb_normal), 0)
        self.assertGreater(len(df_ig_normal), 0)
        self.assertGreater(len(df_ig_normal), 0)

        # valida una columna adicional con la polaridad
        self.assertEqual(len(df_fb_normal.columns), 17)
        self.assertEqual(len(df_ig_normal.columns), 11)
        self.assertEqual(len(df_tw_normal.columns), 45)

        print("".center(60, "-"))

    def test_data_empty(self):
        """
        This test with data empty

        Returns
        -------
        None.

        """
        print("".center(60, "="))
        print("TEST_DATA_EMPTY...")
        df_empty = self.df_empty

        df_empty = Polarity().polarity(df_text=df_empty)

        self.assertEqual(len(df_empty), 0)

        print("".center(60, "-"))


if __name__ == "__main__":
    unittest.main()
