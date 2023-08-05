import sys
from copy import deepcopy
from datetime import timedelta

import numpy as np
import pandas as pd

# from memory_profiler import profile
from wj_analysis.facebook import polarity_distribution

ERR_SYS = "\nSystem error: "


class PolarityAnalysisFB:
    def __init__(self, df_sentiment):
        self.df_sentiment = df_sentiment

    def top_post(self, df_posts, df_pages, threshold=10):
        """
        This method returns the top posts of the day calculating the relative polarity of the comments.

        Parameters
        ----------
        df_posts : DataFrame
            DataFrame with the posts of Facebook
        df_pages : DataFrame
            DataFrame with the pages of Facebook

        Returns
        df : DataFrame
            add column 'rel_polarity' that calculates the relative polarity of the comments, organized from the most meaningful to the least meaningful
        ----------
        """
        METHOD_NAME = "top_post"

        PAGES_COLUMNS = ["page_id", "name"]
        POSTS_COLUMNS = ["page_id", "post_id", "message", "permalink_url"]
        SENTIMENT_COLUMNS = ["post_id", "sentiment"]

        OUTPUT_COLUMNS = [
            "page_id",
            "post_id",
            "message",
            "permalink_url",
            "name",
            "sentiment",
            "count_comments",
            "rel_polarity",
        ]

        if len(self.df_sentiment) > 0 and len(df_posts) > 0:
            try:
                df_pages_temp = deepcopy(df_pages[PAGES_COLUMNS])
                df_getpolarity = deepcopy(df_posts[POSTS_COLUMNS])
                df_getpolarity["name"] = df_getpolarity["page_id"].map(
                    dict(df_pages_temp[PAGES_COLUMNS].values)
                )
                df_getpolarity["sentiment"] = df_getpolarity["post_id"].map(
                    dict(self.df_sentiment[SENTIMENT_COLUMNS].values)
                )
                df_getpolarity = df_getpolarity.dropna(
                    subset=["sentiment"]
                ).reset_index(drop=True)
                df_getpolarity["count_comments"] = [
                    sum(polarity.values()) for polarity in df_getpolarity["sentiment"]
                ]
                df_getpolarity = df_getpolarity[df_getpolarity["count_comments"] >= 10]
                if len(df_getpolarity) > 0:
                    df_getpolarity["rel_polarity"] = df_getpolarity.apply(
                        lambda row: np.dot(
                            list(row["sentiment"].keys()),
                            [
                                value / row["count_comments"]
                                for value in row["sentiment"].values()
                            ],
                        )
                    )
                    df_getpolarity = df_getpolarity[
                        df_getpolarity["rel_polarity"] > 0.1
                    ]
                    return (
                        df_getpolarity.sort_values(by=["rel_polarity"], ascending=False)
                        .reset_index(drop=True)
                        .head(threshold)
                    )
                else:
                    print(
                        "Warning: no post has more than 10 comments, thus can't be analyze"
                    )
                    return pd.DataFrame(columns=OUTPUT_COLUMNS)
            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                return pd.DataFrame(columns=OUTPUT_COLUMNS)
        else:
            print("Warning: One of the DataFrames is empty. It cannot be computed.")
            self.df_getpolarity = pd.DataFrame(columns=OUTPUT_COLUMNS)
            self.len_getpolarity = len(self.df_getpolarity)

    def timeaccount_post(self):
        """
        This method returns the sentiment analyzed by time and account.

        Parameters
        ----------

        Returns
        df_timeaccount : DataFrame
            returns a dataframe with the sentiment analyzed gruping by account
        --------
        """

        METHOD_NAME = "timeaccount_post"

        OUTPUT_COLUMNS = ["_object_id", "_object_name", "date", "day_sentiment"]

        if len(self.df_sentiment) > 0:
            try:
                self.df_sentiment["created_time"] = pd.to_datetime(
                    self.df_sentiment["created_time"]
                ) - timedelta(hours=5)
                self.df_sentiment["date"] = self.df_sentiment["created_time"].apply(
                    lambda d: d.date()
                )
                df_timeaccount = pd.DataFrame(columns=OUTPUT_COLUMNS)
                page_names = dict(
                    self.df_sentiment[["_object_id", "_object_name"]].values
                )
                for brand_id in self.df_sentiment["_object_id"].drop_duplicates():
                    df_brand = self.df_sentiment[
                        self.df_sentiment["_object_id"] == brand_id
                    ]
                    for date in df_brand["date"].drop_duplicates():
                        df_date = df_brand[df_brand["date"] == date]
                        day_sentiment = {
                            -1.0: 0.0,
                            -0.5: 0.0,
                            0.0: 0.0,
                            0.5: 0.0,
                            1.0: 0.0,
                        }
                        for dict_values in df_date["sentiment"]:
                            for key in np.arange(-1.0, 1.5, 0.5):
                                day_sentiment[key] += dict_values[key]
                        df_timeaccount.loc[len(df_timeaccount)] = [
                            brand_id,
                            page_names[brand_id],
                            date,
                            day_sentiment,
                        ]
                df_timeaccount["count_comments"] = [
                    sum(polarity.values())
                    for polarity in df_timeaccount["day_sentiment"]
                ]
                if len(df_timeaccount) > 0:
                    for index, row in df_timeaccount.iterrows():
                        for key in row["day_sentiment"].keys():
                            if row["count_comments"] != 0:
                                row["day_sentiment"][key] /= row["count_comments"]
                df_timeaccount["list_posts"] = ""
                for i in range(0, len(df_timeaccount)):
                    date = df_timeaccount["date"][i]
                    object_id = df_timeaccount["_object_id"][i]
                    list_post_id = []
                    for j in range(0, len(self.df_sentiment)):
                        if date == self.df_sentiment["date"][j]:
                            if object_id == self.df_sentiment["_object_id"][j]:
                                list_post_id.append(self.df_sentiment["post_id"][j])
                    df_timeaccount["list_posts"][i] = list_post_id
                    df_timeaccount["list_posts"][i] = list(
                        set(df_timeaccount["list_posts"][i])
                    )
                return df_timeaccount
            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                return pd.DataFrame(columns=OUTPUT_COLUMNS)
        else:
            print("Warning: One of the DataFrames is empty. It cannot be computed.")
            self.df_getpolarity = pd.DataFrame(columns=OUTPUT_COLUMNS)
            self.len_getpolarity = len(self.df_getpolarity)

    def timeaccount_post_group(self):

        # METHOD_NAME = "timeaccount_post_group"
        # OUTPUT_COLUMNS = ["_object_id", "_object_name", "date", "day_sentiment"]

        self.df_sentiment["created_time"] = pd.to_datetime(
            self.df_sentiment["created_time"]
        ) - timedelta(hours=5)
        self.df_sentiment["date"] = self.df_sentiment["created_time"].apply(
            lambda d: d.date()
        )

        if len(self.df_sentiment) > 0:
            negative_1 = []
            negative_05 = []
            neutral = []
            positive_05 = []
            positive_1 = []

            for i in range(0, len(self.df_sentiment)):
                temp_1 = self.df_sentiment["sentiment"].iloc[i]
                dict(temp_1)
                negative_1.append(temp_1.get(-1.0))
                negative_05.append(temp_1.get(-0.5))
                neutral.append(temp_1.get(0.0))
                positive_05.append(temp_1.get(0.5))
                positive_1.append(temp_1.get(1.0))

            self.df_sentiment[-1.0] = negative_1
            self.df_sentiment[-0.5] = negative_05
            self.df_sentiment[0.0] = neutral
            self.df_sentiment[0.5] = positive_05
            self.df_sentiment[1.0] = positive_1
            # print(self.df_sentiment.columns)
            self.df_sentiment["count_comments"] = 1
            grouped = self.df_sentiment.groupby(["group", "date"], as_index=False).agg(
                {
                    -1.0: "mean",
                    -0.5: "mean",
                    0.0: "mean",
                    0.5: "mean",
                    1.0: "mean",
                    "count_comments": "count",
                }
            )

            sentiment = grouped[[-1.0, -0.5, 0.0, 0.5, 1.0]]
            sentiment = sentiment.to_dict("records")
            grouped["day_sentiment"] = ""
            for i in range(0, len(grouped)):
                grouped["day_sentiment"][i] = sentiment[i]
            grouped = grouped[["group", "date", "day_sentiment", "count_comments"]]

            grouped["list_posts"] = ""
            for i in range(0, len(grouped)):
                date = grouped["date"][i]
                group = grouped["group"][i]
                list_post_id = []
                for j in range(0, len(self.df_sentiment)):
                    if date == self.df_sentiment["date"][j]:
                        if group == self.df_sentiment["group"][j]:
                            list_post_id.append(self.df_sentiment["post_id"][j])
                grouped["list_posts"][i] = list_post_id
                grouped["list_posts"][i] = list(set(grouped["list_posts"][i]))
            return grouped
