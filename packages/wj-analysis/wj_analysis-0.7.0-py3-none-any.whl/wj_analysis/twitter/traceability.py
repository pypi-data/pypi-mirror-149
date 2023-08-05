import sys
from copy import deepcopy
from datetime import timedelta

import pandas as pd

from ..common import general_utils

ERR_SYS = "\nSystem error: "


class Traceability:
    def __init__(self, df_pages, groups):
        """
        This function computes the dataframe 'df_fan_count' with the columns
        'fan_count', 'page_id', 'name' 'group' and 'date'.

        Parameters
        ----------
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

        OUTPUT_COLUMNS = [
            "ac_followers_count",
            "twitter_id",
            "screen_name",
            "group",
            "date",
        ]

        if len(df_pages) > 0:
            try:
                df_fan_count = deepcopy(
                    df_pages[
                        ["ac_followers_count", "twitter_id", "screen_name", "date"]
                    ]
                )

                df_fan_count["date"] = pd.to_datetime(df_fan_count["date"]) - timedelta(
                    hours=5
                )
                df_fan_count["date"] = df_fan_count["date"].apply(lambda d: d.date())

                df_fan_count = (
                    df_fan_count.groupby(["twitter_id", "screen_name", "date"])
                    .last()
                    .reset_index()
                )

                df_fan_count["group"] = df_fan_count["twitter_id"].apply(
                    lambda tid: general_utils.get_group(tid, groups)
                )

                self.df_fan_count = df_fan_count

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_fan_count = pd.DataFrame(columns=OUTPUT_COLUMNS)

        else:
            print("Warning: The DataFrame is empty. It cannot be computed.")
            self.df_fan_count = pd.DataFrame(columns=OUTPUT_COLUMNS)

    def absolute(self):
        """
        This method returns a DataFrame with the number of followers for each account
        for every day.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "absolute"

        df_fan_count = self.df_fan_count

        df_fan_count = df_fan_count.sort_values(
            ["group", "twitter_id", "screen_name", "date"]
        )
        df_fan_count = df_fan_count.rename(columns={"ac_followers_count": "value"})

        try:
            return df_fan_count[
                ["group", "twitter_id", "screen_name", "date", "value"]
            ].dropna(subset=["value"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=["group", "twitter_id", "screen_name", "date", "value"]
            )

    def differences(self):
        """
        This method returns a DataFrame with the number of new followers for each account
        for every day.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "differences"

        df_fan_count = self.df_fan_count
        try:
            dfs = []
            for tid in set(df_fan_count.twitter_id):
                df_tmp = df_fan_count[df_fan_count.twitter_id.eq(tid)].sort_values(
                    "date"
                )
                df_tmp["value"] = df_tmp["ac_followers_count"].diff()
                dfs.append(df_tmp)

            df_fan_count_diff = pd.concat(dfs).sort_values(
                ["group", "twitter_id", "screen_name", "date"]
            )

            return df_fan_count_diff[
                ["group", "twitter_id", "screen_name", "date", "value"]
            ].dropna(subset=["value"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=["group", "twitter_id", "screen_name", "date", "value"]
            )

    def percentage(self):
        """
        This method returns a DataFrame with the percentual change of followers for each account
        for every day.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "percentage"

        df_fan_count = self.df_fan_count
        try:
            dfs = []
            for tid in set(df_fan_count.twitter_id):
                df_tmp = df_fan_count[df_fan_count.twitter_id.eq(tid)].sort_values(
                    "date"
                )
                df_tmp["value"] = 100.0 * df_tmp["ac_followers_count"].pct_change()
                dfs.append(df_tmp)

            df_fan_count_perc = pd.concat(dfs).sort_values(
                ["group", "twitter_id", "screen_name", "date"]
            )

            return df_fan_count_perc[
                ["group", "twitter_id", "screen_name", "date", "value"]
            ].dropna(subset=["value"])

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=["group", "twitter_id", "screen_name", "date", "value"]
            )
