import sys
from copy import deepcopy

import numpy as np
import pandas as pd

from wj_analysis.twitter import polarity_distribution

ERR_SYS = "\nSystem error: "


class TopPolarityScoreTW:
    def top_post(self, df_sentiment, df_replies, threshold=10):
        METHOD_NAME = "posts"

        REPLIES_COLUMNS = [
            "screen_name",
            "tweet_id",
            "text",
            "in_reply_to_status_id",
        ]
        SENTIMENT_COLUMNS = ["post_id", "sentiment"]

        OUTPUT_COLUMNS = [
            "screen_name",
            "tweet_id",
            "text",
            "in_reply_to_status_id",
            "sentiment",
            "rel_sentiment",
        ]

        if len(df_sentiment) > 0 and len(df_replies) > 0:
            try:
                df_getpolarity = deepcopy(df_replies[REPLIES_COLUMNS])
                df_getpolarity = df_getpolarity.rename(
                    columns={"in_reply_to_status_id": "post_id"}
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
                    rel_polarity = []
                    for index, row in df_getpolarity.iterrows():
                        for key in row["sentiment"].keys():
                            row["sentiment"][key] /= row["count_comments"]
                        rel_polarity.append(
                            np.dot(
                                list(row["sentiment"].keys()),
                                list(row["sentiment"].values()),
                            )
                        )
                    df_getpolarity["rel_polarity"] = rel_polarity
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
