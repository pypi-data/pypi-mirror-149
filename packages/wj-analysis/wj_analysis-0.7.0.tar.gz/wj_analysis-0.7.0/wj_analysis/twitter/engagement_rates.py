import json
import re
import sys
from copy import deepcopy
from datetime import timedelta

import pandas as pd

from ..common import general_utils, metric_transformation

ERR_SYS = "\nSystem error: "


class EngagementRateTW:
    def __init__(self, df_tweets, df_replies, groups, mode="status", remove_rt=True):
        """
        This method computes the DataFrame 'df_tweets_full' with the column 'reply_count_no_api'
        which is a count of the replies for every post.

        Parameters
        ----------
        df_tweets:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'tweet_id'.
        df_replies:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'text', 'in_reply_to_status_id'.
        groups:
            type: dict
            Maps the groups (client, compentition, archetype, trends) to the
            corresponding page ids for each group.
        mode:
            type: str
            Selects the module to compute the engagement rates for.
            default = 'status'
            If set to 'terms' df_replies and groups are no used.
        """

        METHOD_NAME = "__init__"

        REPLIES_COLUMNS = ["text", "in_reply_to_status_id"]
        TWEETS_COLUMNS = [
            "twitter_id",
            "screen_name",
            "created_at",
            "tweet_id",
            "favorite_count",
            "retweet_count",
            "ac_followers_count",
            "in_reply_to_status_id",
            "media_entities",
            "user_mentions",
            "hashtags",
            "text",
            "profile_image",
        ]
        OUTPUT_COLUMNS = [
            "reply_count_no_api",
            "twitter_id",
            "screen_name",
            "group",
            "created_at",
            "tweet_id",
            "ac_followers_count",
            "favorite_count",
            "retweet_count",
            "in_reply_to_status_id",
            "media_entities",
            "user_mentions",
            "hashtags",
            "text",
            "profile_image",
        ]
        self.remove_rt = remove_rt
        self.mode = mode

        if mode == "status":
            if len(df_tweets) > 0 and len(df_replies) > 0:
                try:
                    df_tweets_full = deepcopy(
                        df_tweets[df_tweets["in_reply_to_status_id"].isna()][
                            TWEETS_COLUMNS
                        ]
                    )
                    df_tweets_full = df_tweets_full.drop_duplicates(
                        subset=[
                            "screen_name",
                            "created_at",
                            "user_mentions",
                            "hashtags",
                            "text",
                        ],
                        keep=False,
                    )
                    df_replies_count = (
                        df_replies[REPLIES_COLUMNS]
                        .groupby("in_reply_to_status_id")
                        .count()
                        .reset_index()
                    )
                    df_replies_count = df_replies_count.rename(
                        columns={
                            "in_reply_to_status_id": "tweet_id",
                            "text": "reply_count_no_api",
                        }
                    )
                    df_tweets_full = pd.merge(
                        df_tweets_full, df_replies_count, on=["tweet_id"], how="left"
                    )
                    df_tweets_full["reply_count_no_api"] = df_tweets_full[
                        "reply_count_no_api"
                    ].fillna(0)
                    df_tweets_full["group"] = df_tweets_full["twitter_id"].apply(
                        lambda tid: general_utils.get_group(tid, groups)
                    )
                    df_tweets_full["created_at"] = pd.to_datetime(
                        df_tweets_full["created_at"]
                    ) - timedelta(hours=5)
                    self.df_tweets_full = df_tweets_full

                except Exception as e:
                    exception_type = sys.exc_info()[0]
                    print(ERR_SYS + str(exception_type))
                    print(e)
                    print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                    self.df_tweets_full = pd.DataFrame(
                        columns=OUTPUT_COLUMNS, dtype=object
                    )

            else:
                print("Warning: One of the DataFrames is empty. It cannot be computed.")
                self.df_tweets_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

        elif mode == "terms":
            try:
                df_tweets_full = deepcopy(df_tweets[TWEETS_COLUMNS])
                df_tweets_full = df_tweets_full.drop_duplicates(
                    subset=[
                        "screen_name",
                        "created_at",
                        "user_mentions",
                        "hashtags",
                        "text",
                        "media_entities",
                    ],
                    keep=False,
                )
                df_tweets_full[
                    "reply_count_no_api"
                ] = 0  # set replies to zero, temporary until official API
                df_tweets_full["group"] = "terms"  # set group to 'terms'
                df_tweets_full = df_tweets_full[
                    df_tweets_full["ac_followers_count"] != 0
                ]  # Avoiding division by zero for users with zero followes.
                df_tweets_full["created_at"] = pd.to_datetime(
                    df_tweets_full["created_at"]
                ) - timedelta(hours=5)
                if remove_rt:
                    rt_flag_list, unique_text_list, author_name_list = [], [], []
                    rt_pattern = re.compile(r"^(?:RT|rt) \@[a-zA-Z0-9\-\_]+\:\s")
                    for index, row in df_tweets_full.iterrows():
                        findings = re.findall(rt_pattern, row["text"])
                        rt_flag = 0
                        unique_text, author_name = row["text"], row["screen_name"]
                        if len(findings) > 0:
                            rt_flag = 1
                            unique_text = re.sub(rt_pattern, "", row["text"])
                            author_name = re.sub(
                                re.compile(r"^(?:RT|rt) \@"), "", findings[0]
                            ).replace(": ", "")
                        rt_flag_list.append(rt_flag)
                        unique_text_list.append(unique_text.lower())
                        author_name_list.append(author_name)
                    df_tweets_full["rt_flag"] = rt_flag_list
                    df_tweets_full["unique_text"] = unique_text_list
                    df_tweets_full["author_name"] = author_name_list
                self.df_tweets_full = df_tweets_full

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_tweets_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

        else:
            raise RuntimeError(
                f'Mode {mode} is not available. Modes available: "status" and "terms".'
            )

    def by_reach(self):
        """
        This method computes the engagement rate for every post based on the
        reach of the post. It stores it on the column
        'engagement_rate_by_reach' on the input Pandas DataFrame 'df_tweets_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_reach"

        df_tweets_full = self.df_tweets_full
        try:
            df_tweets_full["engagement_rate_by_reach"] = df_tweets_full.apply(
                lambda row: 100
                * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                / row.reach_count,
                axis=1,
            )
            return df_tweets_full.dropna(subset=["engagement_rate_by_reach"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_tweets_full.columns) + ["engagement_rate_by_reach"]
            )

    def by_post(self):
        """
        This method computes the engagement rate for every post based on the
        number of followers of the account. It stores it on the column
        'engagement_rate_by_post' on the input Pandas DataFrame 'df_tweets_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_post"

        df_tweets_full = self.df_tweets_full
        try:
            if self.mode == "terms":
                df_tweets_full["engagement_rate_by_post"] = df_tweets_full.apply(
                    lambda row: row.favorite_count
                    + row.retweet_count
                    + row.reply_count_no_api,
                    axis=1,
                )

                if self.remove_rt:
                    df_tweets_max_er = df_tweets_full[
                        ["screen_name", "unique_text", "engagement_rate_by_post"]
                    ]
                    df_tweets_max_er = (
                        df_tweets_max_er.groupby(["screen_name", "unique_text"])
                        .max()
                        .reset_index()
                    )
                    df_tweets_full = df_tweets_full.merge(
                        df_tweets_max_er,
                        left_on=[
                            "author_name",
                            "unique_text",
                            "engagement_rate_by_post",
                        ],
                        right_on=[
                            "screen_name",
                            "unique_text",
                            "engagement_rate_by_post",
                        ],
                        how="inner",
                    )
                    df_tweets_full = df_tweets_full.drop(
                        ["rt_flag", "unique_text", "author_name", "screen_name_y"],
                        axis=1,
                    )
                    df_tweets_full = df_tweets_full.rename(
                        columns={"screen_name_x": "screen_name"}
                    )

            else:
                df_tweets_full["engagement_rate_by_post"] = df_tweets_full.apply(
                    lambda row: 100
                    * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                    / row.ac_followers_count,
                    axis=1,
                )

            METRIC = "engagement_rate_by_post"
            ITEM_COLUMN = "twitter_id"
            df_tweets_full = df_tweets_full.sort_values(by=["created_at"])
            df_tweets_full = metric_transformation.MetricCategorization(
                df_tweets_full, METRIC, ITEM_COLUMN
            ).categorize()

            return df_tweets_full.dropna(subset=["engagement_rate_by_post"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_tweets_full.columns)
                + ["engagement_rate_by_post", "boundary", "rel_engagement_rate_by_post"]
            )

    def by_impressions(self):
        """
        This method computes the engagement rate for every post based on the
        impressions of the post. It stores it on the column
        'engagement_rate_by_impressions' on the input Pandas DataFrame 'df_tweets_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_impressions"

        df_tweets_full = self.df_tweets_full
        try:
            df_tweets_full["engagement_rate_by_impressions"] = df_tweets_full.apply(
                lambda row: 100
                * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                / row.impressions_count,
                axis=1,
            )
            return df_tweets_full.dropna(subset=["engagement_rate_by_impressions"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_tweets_full.columns)
                + ["engagement_rate_by_impressions"]
            )

    def by_day(self, grouped=True):
        """
        This method computes the engagement rate by day for each account
        based on the number of followers. It stores it on the column
        'engagement_rate_by_impressions' on the output Pandas DataFrame 'df_eng_by_day'.

        Parameters
        ----------
        grouped:
            type: bool
            If False retunrs the DataFrame by account by day.
            If True returns the DataFrame by group by day, default=True.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_day"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        df_tweets_full = self.df_tweets_full
        try:
            df_eng_by_day = deepcopy(df_tweets_full)
            df_eng_by_day["date"] = df_eng_by_day.created_at.apply(lambda d: d.date)
            df_post_by_date = df_eng_by_day

            df_eng_by_day = (
                df_eng_by_day[
                    [
                        "twitter_id",
                        "screen_name",
                        "group",
                        "date",
                        "retweet_count",
                        "reply_count_no_api",
                        "favorite_count",
                        "ac_followers_count",
                    ]
                ]
                .groupby(["twitter_id", "screen_name", "date"])
                .agg(
                    {
                        "group": "last",
                        "retweet_count": "sum",
                        "favorite_count": "sum",
                        "reply_count_no_api": "sum",
                        "ac_followers_count": "max",
                    }
                )
            )
            df_eng_by_day["engagement_rate_by_day"] = df_eng_by_day.apply(
                lambda row: 100
                * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                / row.ac_followers_count,
                axis=1,
            )
            df_eng_by_day = df_eng_by_day.reset_index()

            if grouped:
                df_eng_by_day = (
                    df_eng_by_day[["group", "date", "engagement_rate_by_day"]]
                    .groupby(["group", "date"])
                    .mean()
                )
                df_eng_by_day = df_eng_by_day.reset_index()
                PAGE_COLUMNS = []
                ITEM_COLUMN = "group"
                df_post_by_date = df_post_by_date.reset_index()
                df_eng_by_day["list_posts"] = ""
                for i in range(0, len(df_eng_by_day)):
                    date = df_eng_by_day["date"][i]
                    group = df_eng_by_day["group"][i]
                    list_post_id = []
                    for j in range(0, len(df_post_by_date)):
                        if date == df_post_by_date["date"][j]:
                            if group == df_post_by_date["group"][j]:
                                list_post_id.append(df_post_by_date["tweet_id"][j])
                    df_eng_by_day["list_posts"][i] = list_post_id
                    df_eng_by_day["list_posts"][i] = list(
                        set(df_eng_by_day["list_posts"][i])
                    )

            else:
                df_eng_by_day = df_eng_by_day.rename(
                    columns={"twitter_id": "_object_id", "screen_name": "_object_name"}
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]
                ITEM_COLUMN = "_object_id"
                df_post_by_date = df_post_by_date.reset_index()
                df_eng_by_day["list_posts"] = ""
                for i in range(0, len(df_eng_by_day)):
                    date = df_eng_by_day["date"][i]
                    object_id = df_eng_by_day["_object_id"][i]
                    list_post_id = []
                    for j in range(0, len(df_post_by_date)):
                        if date == df_post_by_date["date"][j]:
                            if object_id == df_post_by_date["twitter_id"][j]:
                                list_post_id.append(df_post_by_date["tweet_id"][j])
                    df_eng_by_day["list_posts"][i] = list_post_id
                    df_eng_by_day["list_posts"][i] = list(
                        set(df_eng_by_day["list_posts"][i])
                    )

            METRIC = "engagement_rate_by_day"
            df_eng_by_day = df_eng_by_day.sort_values(by=["date"])
            df_eng_by_day = metric_transformation.MetricCategorization(
                df_eng_by_day, METRIC, ITEM_COLUMN
            ).categorize()
            return df_eng_by_day[
                PAGE_COLUMNS
                + [
                    "group",
                    "date",
                    "engagement_rate_by_day",
                    "boundary",
                    "rel_engagement_rate_by_day",
                    "list_posts",
                ]
            ].dropna(subset=["engagement_rate_by_day"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=[
                    "_object_id",
                    "_object_name",
                    "group",
                    "date",
                    "engagement_rate_by_day",
                    "boundary",
                    "rel_engagement_rate_by_day",
                ]
            )

    def by_views(self):
        """
        This method computes the engagement rate for every video post based on the
        views. It stores it on the column 'engagement_rate_by_post'
        on the output Pandas DataFrame 'df_eng_by_views'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_views"

        df_tweets_full = self.df_tweets_full
        try:
            df_eng_by_views = deepcopy(df_tweets_full)
            df_eng_by_views = df_eng_by_views[~df_eng_by_views.media_entities.isna()]
            if len(df_eng_by_views) > 0:
                df_eng_by_views.media_entities = df_eng_by_views.media_entities.apply(
                    lambda ent: json.loads(ent)
                )

                df_eng_by_views["engagement_rate_by_views"] = df_eng_by_views.apply(
                    lambda row: 100
                    * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                    / row.view_count
                    if row.media_entities[0]["type"] == "video"
                    else None,
                    axis=1,
                )
                return df_eng_by_views.dropna(subset=["engagement_rate_by_views"])
            else:
                print("There are no tweets with videos.")

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_tweets_full.columns) + ["engagement_rate_by_views"]
            )

    def by_accounts(self, grouped=True):
        """
        This method computes the engagement rate by page
        based on the number of followers. It stores it on the column
        'engagement_rate_by_accounts' on the output Pandas DataFrame 'df_eng_by_accounts'.

        Parameters
        ----------
        grouped:
            type: bool
            If False retunrs the DataFrame by account.
            If True returns the DataFrame by group, default=True

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_accounts"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        df_tweets_full = self.df_tweets_full
        try:
            df_eng_by_accounts = deepcopy(df_tweets_full)

            df_eng_by_accounts = (
                df_eng_by_accounts[
                    [
                        "twitter_id",
                        "screen_name",
                        "group",
                        "retweet_count",
                        "reply_count_no_api",
                        "favorite_count",
                        "ac_followers_count",
                    ]
                ]
                .groupby(["twitter_id", "screen_name"])
                .agg(
                    {
                        "group": "last",
                        "retweet_count": "sum",
                        "favorite_count": "sum",
                        "reply_count_no_api": "sum",
                        "ac_followers_count": "max",
                    }
                )
            )
            df_eng_by_accounts[
                "engagement_rate_by_accounts"
            ] = df_eng_by_accounts.apply(
                lambda row: 100
                * (row.favorite_count + row.retweet_count + row.reply_count_no_api)
                / row.ac_followers_count,
                axis=1,
            )
            df_eng_by_accounts = df_eng_by_accounts.reset_index()

            if grouped:
                df_eng_by_accounts = (
                    df_eng_by_accounts[["group", "engagement_rate_by_accounts"]]
                    .groupby(["group"])
                    .mean()
                )
                df_eng_by_accounts = df_eng_by_accounts.reset_index()
                PAGE_COLUMNS = []
                ITEM_COLUMN = "group"
            else:
                df_eng_by_accounts = df_eng_by_accounts.rename(
                    columns={"twitter_id": "_object_id", "screen_name": "_object_name"}
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]
                ITEM_COLUMN = "_object_id"

            METRIC = "engagement_rate_by_accounts"
            df_eng_by_accounts = df_eng_by_accounts.sort_values(by=["group"])
            df_eng_by_accounts = metric_transformation.MetricCategorization(
                df_eng_by_accounts, METRIC, ITEM_COLUMN
            ).categorize()

            return df_eng_by_accounts[
                PAGE_COLUMNS
                + [
                    "group",
                    "engagement_rate_by_accounts",
                    "boundary",
                    "rel_engagement_rate_by_accounts",
                ]
            ].dropna(subset=["engagement_rate_by_accounts"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=[
                    "_object_id",
                    "_object_name",
                    "group",
                    "engagement_rate_by_accounts",
                    "boundary",
                    "rel_engagement_rate_by_accounts",
                ],
                dtype=object,
            )
