import sys
from copy import deepcopy

import numpy as np
import pandas as pd

from wj_analysis.facebook import polarity_distribution

ERR_SYS = "\nSystem error: "


class TopPolarityScoreFB:
    def top_post(self, df_sentiment, df_posts, df_pages, threshold=10):
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

        METHOD_NAME = "posts"

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

        if len(df_sentiment) > 0 and len(df_posts) > 0:
            try:
                df_pages_temp = deepcopy(df_pages[PAGES_COLUMNS])
                df_getpolarity = deepcopy(df_posts[POSTS_COLUMNS])
                df_getpolarity["name"] = df_getpolarity["page_id"].map(
                    dict(df_pages_temp[PAGES_COLUMNS].values)
                )
                df_getpolarity["sentiment"] = df_getpolarity["post_id"].map(
                    dict(df_sentiment[SENTIMENT_COLUMNS].values)
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
