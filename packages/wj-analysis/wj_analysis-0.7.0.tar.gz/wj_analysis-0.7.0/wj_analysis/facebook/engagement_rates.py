import sys
from copy import deepcopy
from datetime import timedelta

import pandas as pd

from ..common import general_utils, metric_transformation

ERR_SYS = "\nSystem error: "


def get_name(pid, dict_page_id_to_name):
    try:
        out_name = dict_page_id_to_name[pid]
    except Exception:
        out_name = "no_name"
    return out_name


class EngagementRateFB:
    def __init__(self, df_posts, df_pages, groups):
        """
        This method computes the DataFrame 'df_posts_full' with the columns
        'group' and 'fan_count' which is a count of the fans in the day the post was made.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            this Pandas DataFrame must have columns
            'created_time' and 'page_id'.
        df_pages:
            type: DataFrame
            this Pandas DataFrame must have columns
            'fan_count', 'page_id' and 'created_at'.
        groups:
            type: dict
            Maps the groups (client, competition, archetype, trends) to the
            corresponding page ids for each group.
        """

        METHOD_NAME = "__init__"

        PAGES_COLUMNS = ["fan_count", "page_id", "created_at"]
        POSTS_COLUMNS = [
            "page_id",
            "created_time",
            "post_id",
            "likes",
            "reactions_love",
            "reactions_wow",
            "reactions_haha",
            "reactions_sad",
            "reactions_angry",
            "reactions_thankful",
            "shares",
            "comments",
            "message",
            "permalink_url",
            "type",
            "message_tags",
        ]
        OUTPUT_COLUMNS = [
            "fan_count",
            "page_id",
            "page_name",
            "date",
            "group",
            "created_time",
            "post_id",
            "likes",
            "reactions_love",
            "reactions_wow",
            "reactions_haha",
            "reactions_sad",
            "reactions_angry",
            "reactions_thankful",
            "shares",
            "comments",
            "message",
            "permalink_url",
            "type",
            "message_tags",
        ]

        if len(df_posts) > 0 and len(df_pages) > 0:
            try:
                df_fan_count = (
                    df_pages[PAGES_COLUMNS]
                    .groupby(["page_id", "created_at"])
                    .last()
                    .reset_index()
                )

                df_fan_count["created_at"] = pd.to_datetime(
                    df_fan_count["created_at"], format="%Y-%m-%dT%H:%M:%S"
                )
                df_fan_count["created_at"] = pd.to_datetime(
                    df_fan_count["created_at"]
                ) - timedelta(hours=5)
                df_fan_count["date"] = df_fan_count["created_at"].apply(
                    lambda d: d.date
                )
                df_fan_count = df_fan_count.drop(columns=["created_at"])

                df_posts_full = deepcopy(df_posts[POSTS_COLUMNS])

                page_id_name_fb = {}
                for idd, row in df_pages.iterrows():
                    page_id_name_fb[row.page_id] = row["name"]
                df_posts_full["page_name"] = df_posts_full.page_id.apply(
                    lambda pid: get_name(pid, page_id_name_fb)
                )

                df_posts_full["created_time"] = pd.to_datetime(
                    df_posts_full["created_time"]
                ) - timedelta(hours=5)
                df_posts_full["date"] = df_posts_full["created_time"].apply(
                    lambda d: d.date
                )
                df_posts_full = pd.merge(
                    df_posts_full, df_fan_count, on=["page_id", "date"], how="left"
                )
                df_posts_full["fan_count"] = df_posts_full.sort_values(
                    ["page_id", "date"]
                )["fan_count"].fillna(method="bfill")

                df_posts_full = df_posts_full.sort_values("date").drop_duplicates(
                    subset=["post_id"], keep="last"
                )

                df_posts_full["group"] = df_posts_full["page_id"].apply(
                    lambda pid: general_utils.get_group(pid, groups)
                )

                self.df_posts_full = df_posts_full

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

        else:
            print("Warning: One of the DataFrames is empty. It cannot be computed.")
            self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS, dtype=object)

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
            df_posts_full["engagement_rate_by_reach"] = df_posts_full.apply(
                lambda row: 100
                * (
                    row.likes
                    + row.reactions_love
                    + row.reactions_wow
                    + row.reactions_haha
                    + row.reactions_sad
                    + row.reactions_angry
                    + row.reactions_thankful
                    + row.shares
                    + row.comments
                )
                / row.reach_count,
                axis=1,
            )
            return df_posts_full.dropna(subset=["engagement_rate_by_reach"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=list(df_posts_full.columns) + ["engagement_rate_by_reach"]
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

        METHOD_NAME = "by_post"

        df_posts_full = self.df_posts_full
        try:
            df_posts_full["engagement_rate_by_post"] = df_posts_full.apply(
                lambda row: 100
                * (
                    row.likes
                    + row.reactions_love
                    + row.reactions_wow
                    + row.reactions_haha
                    + row.reactions_sad
                    + row.reactions_angry
                    + row.reactions_thankful
                    + row.shares
                    + row.comments
                )
                / row.fan_count,
                axis=1,
            )

            METRIC = "engagement_rate_by_post"
            ITEM_COLUMN = "page_id"
            df_posts_full = df_posts_full.sort_values(by=["created_time"])
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
                * (
                    row.likes
                    + row.reactions_love
                    + row.reactions_wow
                    + row.reactions_haha
                    + row.reactions_sad
                    + row.reactions_angry
                    + row.reactions_thankful
                    + row.shares
                    + row.comments
                )
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

        df_posts_full = self.df_posts_full
        try:
            df_eng_by_day = deepcopy(df_posts_full)
            df_post_by_date = df_eng_by_day
            df_eng_by_day = (
                df_eng_by_day[
                    [
                        "page_id",
                        "page_name",
                        "group",
                        "date",
                        "shares",
                        "comments",
                        "likes",
                        "reactions_love",
                        "reactions_wow",
                        "reactions_haha",
                        "reactions_sad",
                        "reactions_angry",
                        "reactions_thankful",
                        "fan_count",
                    ]
                ]
                .groupby(["page_id", "page_name", "date"])
                .agg(
                    {
                        "group": "last",
                        "shares": "sum",
                        "comments": "sum",
                        "likes": "sum",
                        "reactions_love": "sum",
                        "reactions_wow": "sum",
                        "reactions_haha": "sum",
                        "reactions_sad": "sum",
                        "reactions_angry": "sum",
                        "reactions_thankful": "sum",
                        "fan_count": "max",
                    }
                )
            )
            df_eng_by_day["engagement_rate_by_day"] = df_eng_by_day.apply(
                lambda row: 100
                * (
                    row.likes
                    + row.reactions_love
                    + row.reactions_wow
                    + row.reactions_haha
                    + row.reactions_sad
                    + row.reactions_angry
                    + row.reactions_thankful
                    + row.shares
                    + row.comments
                )
                / row.fan_count,
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
                # pdb.set_trace()
                for i in range(0, len(df_eng_by_day)):
                    date = df_eng_by_day["date"][i]
                    group = df_eng_by_day["group"][i]
                    list_post_id = []
                    for j in range(0, len(df_post_by_date)):
                        if date == df_post_by_date["date"][j]:
                            if group == df_post_by_date["group"][j]:
                                list_post_id.append(df_post_by_date["post_id"][j])
                    df_eng_by_day["list_posts"][i] = list_post_id
                    df_eng_by_day["list_posts"][i] = list(
                        set(df_eng_by_day["list_posts"][i])
                    )

            else:
                df_eng_by_day = df_eng_by_day.rename(
                    columns={"page_id": "_object_id", "page_name": "_object_name"}
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
                            if object_id == df_post_by_date["page_id"][j]:
                                list_post_id.append(df_post_by_date["post_id"][j])
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
                    "boundary",
                    "rel_engagement_rate_by_day",
                    "engagement_rate_by_day",
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
            df_eng_by_views = df_eng_by_views[df_eng_by_views.type == "video"]
            if len(df_eng_by_views) > 0:
                df_eng_by_views["engagement_rate_by_views"] = df_eng_by_views.apply(
                    lambda row: 100
                    * (
                        row.likes
                        + row.reactions_love
                        + row.reactions_wow
                        + row.reactions_haha
                        + row.reactions_sad
                        + row.reactions_angry
                        + row.reactions_thankful
                        + row.shares
                        + row.comments
                    )
                    / row.view_count,
                    axis=1,
                )
                return df_eng_by_views.dropna(subset=["engagement_rate_by_views"])
            else:
                print("There are no posts with videos.")
                return pd.DataFrame(
                    columns=list(df_posts_full.columns) + ["engagement_rate_by_views"]
                )

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

        df_posts_full = self.df_posts_full
        try:
            df_eng_by_accounts = deepcopy(df_posts_full)

            df_eng_by_accounts = (
                df_eng_by_accounts[
                    [
                        "page_id",
                        "page_name",
                        "group",
                        "shares",
                        "comments",
                        "likes",
                        "reactions_love",
                        "reactions_wow",
                        "reactions_haha",
                        "reactions_sad",
                        "reactions_angry",
                        "reactions_thankful",
                        "fan_count",
                        "post_id",
                    ]
                ]
                .groupby(["page_id", "page_name"])
                .agg(
                    {
                        "group": "last",
                        "shares": "sum",
                        "comments": "sum",
                        "likes": "sum",
                        "reactions_love": "sum",
                        "reactions_wow": "sum",
                        "reactions_haha": "sum",
                        "reactions_sad": "sum",
                        "reactions_angry": "sum",
                        "reactions_thankful": "sum",
                        "fan_count": "max",
                    }
                )
            )
            df_eng_by_accounts[
                "engagement_rate_by_accounts"
            ] = df_eng_by_accounts.apply(
                lambda row: 100
                * (
                    row.likes
                    + row.reactions_love
                    + row.reactions_wow
                    + row.reactions_haha
                    + row.reactions_sad
                    + row.reactions_angry
                    + row.reactions_thankful
                    + row.shares
                    + row.comments
                )
                / row.fan_count,
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
                    columns={"page_id": "_object_id", "page_name": "_object_name"}
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
