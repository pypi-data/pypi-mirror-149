import sys
from copy import deepcopy
from datetime import timedelta

import pandas as pd

from ..common import general_utils, metric_transformation

ERR_SYS = "\nSystem error: "


class EngagementRateIG:
    def __init__(self, df_posts, df_pages, groups, mode="status"):
        """
        This method computes the DataFrame 'df_posts_full' with the columns
        'group' and 'followers' which is a count of the fans in the day the post was made.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'owner_id' and 'date_utc'.
        df_pages:
            type: DataFrame
            this Pandas DataFrame muts have columns
            'followers', 'userid' and 'date'.
        groups:
            type: dict
            Maps the groups (client, compentition, archetype, trends) to the
            corresponding page ids for each group.
        """

        METHOD_NAME = "__init__"

        METHOD_NAME = "__init__"

        self.mode = mode

        if self.mode == "status":
            PAGES_COLUMNS = ["followers", "userid", "date"]

            POSTS_COLUMNS = [
                "owner_id",
                "owner_username",
                "date_utc",
                "shortcode",
                "likes_count",
                "comment_count",
                "caption_hashtags",
                "typename",
                "caption_mentions",
                "caption",
                "mediaid",
            ]
            OUTPUT_COLUMNS = [
                "followers",
                "owner_id",
                "owner_username",
                "group",
                "created_at",
                "shortcode",
                "likes_count",
                "comment_count",
                "caption_hashtags",
                "typename",
                "caption_mentions",
                "caption",
            ]

            if len(df_posts) > 0 and len(df_pages) > 0:
                try:
                    df_fan_count = deepcopy(df_pages[PAGES_COLUMNS])
                    df_fan_count["userid"] = df_fan_count["userid"].apply(
                        lambda uid: str(uid)
                    )

                    df_fan_count["date"] = pd.to_datetime(
                        df_fan_count["date"], format="%Y-%m-%dT%H:%M:%S"
                    )
                    df_fan_count["date"] = pd.to_datetime(
                        df_fan_count["date"]
                    ) - timedelta(hours=5)
                    df_fan_count["date"] = df_fan_count["date"].apply(lambda d: d.date)
                    df_fan_count = (
                        df_fan_count.groupby(["userid", "date"]).last().reset_index()
                    )

                    df_fan_count = df_fan_count.rename(columns={"userid": "owner_id"})

                    df_posts_full = deepcopy(df_posts[POSTS_COLUMNS])
                    df_posts_full["owner_id"] = df_posts_full["owner_id"].apply(
                        lambda uid: str(uid)
                    )

                    df_posts_full["date"] = pd.to_datetime(
                        df_posts_full["date_utc"], format="%Y-%m-%dT%H:%M:%S"
                    )
                    df_posts_full["created_at"] = pd.to_datetime(
                        df_posts_full["date"]
                    ) - timedelta(hours=5)
                    df_posts_full["date"] = pd.to_datetime(
                        df_posts_full["date"]
                    ) - timedelta(hours=5)
                    df_posts_full["date"] = df_posts_full["date"].apply(
                        lambda d: d.date
                    )
                    df_posts_full = pd.merge(
                        df_posts_full, df_fan_count, on=["owner_id", "date"], how="left"
                    )
                    df_posts_full["followers"] = df_posts_full.sort_values(
                        ["owner_id", "date"]
                    )["followers"].fillna(method="bfill")

                    df_posts_full = df_posts_full.sort_values("date").drop_duplicates(
                        subset=["shortcode"], keep="last"
                    )

                    df_posts_full["group"] = df_posts_full["owner_id"].apply(
                        lambda pid: general_utils.get_group(pid, groups)
                    )

                    self.df_posts_full = df_posts_full

                except Exception as e:
                    exception_type = sys.exc_info()[0]
                    print(ERR_SYS + str(exception_type))
                    print(e)
                    print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                    self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)

            else:
                print("Warning: One of the DataFrames is empty. It cannot be computed.")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)
        elif self.mode == "hashtags":
            HASHTAG_COLUMNS = [
                "caption",
                "comments_count",
                "like_count",
                "media_type",
                "timestamp",
            ]
            OUTPUT_COLUMNS = [
                "followers",
                "group",
                "created_at",
                "likes_count",
                "comment_count",
                "typename",
                "caption",
            ]
            try:
                df_hashtag_full = deepcopy(
                    df_posts[HASHTAG_COLUMNS]
                )  # df_hashtag camuflado
                df_hashtag_full = df_hashtag_full.rename(
                    columns={
                        "comments_count": "comment_count",
                        "like_count": "likes_count",
                        "media_type": "typename",
                        "timestamp": "date_utc",
                    }
                )

                df_hashtag_full = df_hashtag_full.drop_duplicates()
                df_hashtag_full["followers"] = 1
                df_hashtag_full["group"] = "hashtags"
                df_hashtag_full["date"] = pd.to_datetime(
                    df_hashtag_full["date_utc"], format="%Y-%m-%dT%H:%M:%S"
                )
                df_hashtag_full["created_at"] = pd.to_datetime(
                    df_hashtag_full["date"]
                ) - timedelta(hours=5)
                self.df_posts_full = df_hashtag_full[OUTPUT_COLUMNS]
            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
        else:
            self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)

    def by_reach(self):
        """
        This method computes the engagement rate for every post based on the
        reach of the post. It stores it on the column
        'engagement_rate_by_reach' on the input Pandas DataFrame 'df_posts_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_reach"

        df_posts_full = self.df_posts_full
        try:
            if self.mode == "hashtags":
                df_posts_full["engagement_rate_by_post"] = df_posts_full.apply(
                    lambda row: (row.likes_count + row.comment_count) / row.followers,
                    axis=1,
                )

            else:
                df_posts_full["engagement_rate_by_post"] = df_posts_full.apply(
                    lambda row: 100
                    * (row.likes_count + row.comment_count)
                    / row.followers,
                    axis=1,
                )
                METRIC = "engagement_rate_by_post"
                ITEM_COLUMN = "owner_id"
                df_posts_full = df_posts_full.sort_values(by=["created_at"])
                df_posts_full = metric_transformation.MetricCategorization(
                    df_posts_full, METRIC, ITEM_COLUMN
                ).categorize()

            return df_posts_full.dropna(subset=["engagement_rate_by_post"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns)
                + ["engagement_rate_by_post", "boundary", "rel_engagement_rate_by_post"]
            )

    def by_post(self):
        """
        This method computes the engagement rate for every post based on the
        number of followers of the account. It stores it on the column
        'engagement_rate_by_post' on the input Pandas DataFrame 'df_posts_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_reach"

        df_posts_full = self.df_posts_full
        try:
            df_posts_full["engagement_rate_by_post"] = df_posts_full.apply(
                lambda row: 100 * (row.likes_count + row.comment_count) / row.followers,
                axis=1,
            )

            METRIC = "engagement_rate_by_post"
            ITEM_COLUMN = "owner_id"
            df_posts_full = df_posts_full.sort_values(by=["created_at"])
            df_posts_full = metric_transformation.MetricCategorization(
                df_posts_full, METRIC, ITEM_COLUMN
            ).categorize()

            return df_posts_full.dropna(subset=["engagement_rate_by_post"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns)
                + ["engagement_rate_by_post", "boundary", "rel_engagement_rate_by_post"]
            )

    def by_impressions(self):
        """
        This method computes the engagement rate for every post based on the
        impressions of the post. It stores it on the column
        'engagement_rate_by_impressions' on the input Pandas DataFrame 'df_posts_full'.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_impressions"

        df_posts_full = self.df_posts_full
        try:
            df_posts_full["engagement_rate_by_impressions"] = df_posts_full.apply(
                lambda row: 100
                * (row.likes_count + row.comment_count)
                / row.impressions_count,
                axis=1,
            )
            return df_posts_full.dropna(subset=["engagement_rate_by_impressions"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns) + ["engagement_rate_by_impressions"]
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
            If True returns the DataFrame by group by day, default=True

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "by_day"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["owner_id", "owner_username"]
        df_posts_full = self.df_posts_full

        try:
            df_eng_by_day = deepcopy(df_posts_full)
            df_post_by_date = df_eng_by_day
            df_eng_by_day = (
                df_eng_by_day[
                    [
                        "owner_id",
                        "owner_username",
                        "group",
                        "date",
                        "comment_count",
                        "likes_count",
                        "followers",
                    ]
                ]
                .groupby(["owner_id", "owner_username", "date"])
                .agg(
                    {
                        "group": "last",
                        "comment_count": "sum",
                        "likes_count": "sum",
                        "followers": "max",
                    }
                )
            )
            df_eng_by_day["engagement_rate_by_day"] = df_eng_by_day.apply(
                lambda row: 100 * (row.likes_count + row.comment_count) / row.followers,
                axis=1,
            )
            df_eng_by_day = df_eng_by_day.reset_index()

            if grouped:
                df_eng_by_day = (
                    df_eng_by_day[["group", "date", "engagement_rate_by_day"]]
                    .groupby(["group", "date"])
                    .mean()
                )

                PAGE_COLUMNS = []
                ITEM_COLUMN = "group"
                df_eng_by_day = df_eng_by_day.reset_index()
                df_post_by_date = df_post_by_date.reset_index()
                df_eng_by_day["list_posts"] = ""
                # pdb.set_trace()
                for i in range(0, len(df_eng_by_day)):
                    date = df_eng_by_day["date"][i]
                    group = df_eng_by_day["group"][i]
                    list_post_id = []
                    for j in range(0, len(df_post_by_date)):
                        if date == df_post_by_date["date"][j]:
                            if group == df_post_by_date["group"][j]:
                                list_post_id.append(df_post_by_date["shortcode"][j])
                    df_eng_by_day["list_posts"][i] = list_post_id
                    df_eng_by_day["list_posts"][i] = list(
                        set(df_eng_by_day["list_posts"][i])
                    )

            else:
                df_eng_by_day = df_eng_by_day.rename(
                    columns={"owner_id": "_object_id", "owner_username": "_object_name"}
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
                            if object_id == df_post_by_date["owner_id"][j]:
                                list_post_id.append(df_post_by_date["shortcode"][j])
                    df_eng_by_day["list_posts"][i] = list_post_id
                    df_eng_by_day["list_posts"][i] = list(
                        set(df_eng_by_day["list_posts"][i])
                    )

            METRIC = "engagement_rate_by_day"
            df_eng_by_day = df_eng_by_day.sort_values(by=["date"])
            df_eng_by_day = metric_transformation.MetricCategorization(
                df_eng_by_day, METRIC, ITEM_COLUMN
            ).categorize()
            # df_eng_by_day['list_post_id'] = df_post_by_date
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

        df_posts_full = self.df_posts_full
        try:
            df_eng_by_views = deepcopy(df_posts_full)
            df_eng_by_views = df_eng_by_views[df_eng_by_views.is_video == True]
            if len(df_eng_by_views) > 0:
                df_eng_by_views["engagement_rate_by_views"] = df_eng_by_views.apply(
                    lambda row: 100
                    * (row.likes_count + row.comment_count)
                    / row.video_view_count,
                    axis=1,
                )
                return df_eng_by_views.dropna(subset=["engagement_rate_by_views"])
            else:
                print("There are no posts with videos.")

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns) + ["engagement_rate_by_views"]
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
            PAGE_COLUMNS = ["owner_id", "owner_username"]

        df_posts_full = self.df_posts_full
        try:
            df_eng_by_accounts = deepcopy(df_posts_full)

            df_eng_by_accounts = (
                df_eng_by_accounts[
                    [
                        "owner_id",
                        "owner_username",
                        "group",
                        "comment_count",
                        "likes_count",
                        "followers",
                    ]
                ]
                .groupby(["owner_id", "owner_username"])
                .agg(
                    {
                        "group": "last",
                        "comment_count": "sum",
                        "likes_count": "sum",
                        "followers": "max",
                    }
                )
            )
            df_eng_by_accounts[
                "engagement_rate_by_accounts"
            ] = df_eng_by_accounts.apply(
                lambda row: 100 * (row.likes_count + row.comment_count) / row.followers,
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
                    columns={"owner_id": "_object_id", "owner_username": "_object_name"}
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
