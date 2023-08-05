import sys
from copy import deepcopy

import numpy as np
import pandas as pd

from ..common import general_utils as gu

ERR_SYS = "\nSystem error: "


class Synchronization:
    def __init__(self, df_posts, platform, engagement_rate="engagement_rate_by_post"):
        """
        This functions computes weekday and hour of the posts.

        Parameters
        ----------
        platform:
            type: str
            Determines the name of the column to compute the weekday and hour from.
        engagement_rate:
            type: str
            Type of engagement rate, default='engagement_rate'.
        """

        METHOD_NAME = "__init__"

        if platform == "twitter" or platform == "instagram":
            DATE_COLUMN = "created_at"
        elif platform == "facebook":
            DATE_COLUMN = "created_time"
        else:
            raise RuntimeError("Platform not available.")

        try:
            df_weekday_hour = deepcopy(df_posts[[DATE_COLUMN, engagement_rate]])

            df_weekday_hour["weekday"] = df_weekday_hour[DATE_COLUMN].apply(
                lambda d: d.weekday()
            )
            df_weekday_hour["hour"] = df_weekday_hour[DATE_COLUMN].apply(
                lambda d: d.hour
            )

            df_weekday_hour = df_weekday_hour.drop(columns=[DATE_COLUMN])
            df_weekday_hour["n_posts"] = 1

            self.df_weekday_hour = df_weekday_hour
            self.engagement_rate = engagement_rate

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            self.df_weekday_hour = pd.DataFrame(
                columns=[DATE_COLUMN, engagement_rate, "weekday", "hour", "n_posts"]
            )
            self.engagement_rate = engagement_rate

    def weekday(self, n_groups=10, threshold_group=3):
        """
        This functions computes the engagement rate, activity and sychronization index
        as a function of weekday of the posts.

        Parameters
        ----------
        n_groups:
            type: str
            Number of groups to split the engagement rate and the activity.
            default=10
        threshold_group:
            type: int
            Minimum level of activity to consider in synchronization. default=3.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "weekday"

        engagement_rate = self.engagement_rate
        df_wd = deepcopy(self.df_weekday_hour[["weekday", "n_posts", engagement_rate]])

        try:
            df_wd = (
                df_wd.groupby("weekday")
                .agg({"n_posts": "count", engagement_rate: "mean"})
                .reset_index()
            )

            gu.discretize(
                df_wd, engagement_rate, to_column="eng_group", n_groups=n_groups
            )
            gu.discretize(df_wd, "n_posts", to_column="act_group", n_groups=n_groups)

            eff_grouped = np.zeros(7)
            act_grouped = np.zeros(7)
            for idd, row in df_wd.iterrows():
                eff_grouped[row.weekday] = row.eng_group
                act_grouped[row.weekday] = row.act_group

            df_wd_out = pd.DataFrame(
                {
                    "weekday": range(7),
                    "activity": eff_grouped,
                    "effectivity": act_grouped,
                }
            )

            df_wd_out["synchronization"] = df_wd_out.apply(
                lambda row: (n_groups - 1) ** 2 - (row.effectivity - row.activity) ** 2
                if row.activity >= threshold_group
                else "N/A",
                axis=1,
            )

            return df_wd_out.sort_values("weekday")

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=["weekday", "activity", "effectivity", "synchronization"]
            )

    def hour(self, n_groups=10, threshold_group=3):
        """
        This functions computes the engagement rate, activity and sychronization index
        as a function of hour of the posts.

        Parameters
        ----------
        n_groups:
            type: str
            Number of groups to split the engagement rate and the activity.
            default=10
        threshold_group:
            type: int
            Minimum level of activity to consider in synchronization. default=3.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "hour"

        engagement_rate = self.engagement_rate
        df_h = deepcopy(self.df_weekday_hour[["hour", "n_posts", engagement_rate]])

        try:
            df_h = (
                df_h.groupby("hour")
                .agg({"n_posts": "count", engagement_rate: "mean"})
                .reset_index()
            )

            gu.discretize(
                df_h, engagement_rate, to_column="eng_group", n_groups=n_groups
            )
            gu.discretize(df_h, "n_posts", to_column="act_group", n_groups=n_groups)

            eff_grouped = np.zeros(24)
            act_grouped = np.zeros(24)
            for idd, row in df_h.iterrows():
                eff_grouped[row.hour] = row.eng_group
                act_grouped[row.hour] = row.act_group

            df_h_out = pd.DataFrame(
                {"hour": range(24), "activity": eff_grouped, "effectivity": act_grouped}
            )

            df_h_out["synchronization"] = df_h_out.apply(
                lambda row: (n_groups - 1) ** 2 - (row.effectivity - row.activity) ** 2
                if row.activity >= threshold_group
                else "N/A",
                axis=1,
            )

            return df_h_out.sort_values("hour")

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=["hour", "activity", "effectivity", "synchronization"]
            )

    def weekday_hour(self, n_groups=10, threshold_group=3):
        """
        This functions computes the engagement rate, activity and sychronization index
        as a function of weekday-hour of the posts.

        Parameters
        ----------
        n_groups:
            type: str
            Number of groups to split the engagement rate and the activity.
            default=10
        threshold_group:
            type: int
            Minimum level of activity to consider in synchronization. default=3.

        Returns
        -------
        tuple of DataFrames
        """

        METHOD_NAME = "weekday_hour"

        engagement_rate = self.engagement_rate
        df_wdh = deepcopy(
            self.df_weekday_hour[["weekday", "hour", "n_posts", engagement_rate]]
        )

        try:
            df_wdh = (
                df_wdh.groupby(["weekday", "hour"])
                .agg({"n_posts": "count", engagement_rate: "mean"})
                .reset_index()
            )

            gu.discretize(
                df_wdh, engagement_rate, to_column="eng_group", n_groups=n_groups
            )
            gu.discretize(df_wdh, "n_posts", to_column="act_group", n_groups=n_groups)

            eff_grouped = np.zeros((24, 7))
            act_grouped = np.zeros((24, 7))
            for idd, row in df_wdh.iterrows():
                eff_grouped[row.hour, row.weekday] = row.eng_group
                act_grouped[row.hour, row.weekday] = row.act_group

            eff_df = pd.DataFrame(eff_grouped)
            act_df = pd.DataFrame(act_grouped)
            sync_df = pd.DataFrame(
                np.where(
                    act_grouped >= threshold_group,
                    (n_groups - 1) ** 2 - (eff_grouped - act_grouped) ** 2,
                    "N/A",
                )
            )

            return eff_df, act_df, sync_df

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            eff_df = np.zeros((24, 7))
            act_df = np.zeros((24, 7))
            sync_df = np.zeros((24, 7))
            return eff_df, act_df, sync_df
