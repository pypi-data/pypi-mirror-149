import sys
from copy import deepcopy

import pandas as pd

from ..common import general_utils
from ..common.nlp_utils import CleanText, Features, Polarity

ERR_SYS = "\nSystem error: "


class PolarityDistributionIG:
    """
    This class computes the polarity of the texts.
    """

    def __init__(self, df_comments, groups, r_group=False):
        """
        This method stores the input DataFrames and checks that they are not empty'.

        Parameters
        ----------
        df_comments:
            type: DataFrame
            Information of the instagram comments.
            This Pandas DataFrame must have columns 'post_owner_id', 'post_owner_username', 'text'.
        groups:
            type: dict
            Maps the groups (client, competition, archetype, trends) to the
            corresponding page ids for each group.
        r_group:
            type: bool
            varibale that indicates if the class return the column group

        """

        METHOD_NAME = "__init__"
        df_comments_full = deepcopy(df_comments)
        self.df_comments_full = df_comments_full
        self.groups = groups
        self.r_group = r_group

        try:
            if df_comments.empty:
                print("Warning: input data DataFrame is empty.")
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_comments_full = pd.DataFrame(columns=[""])

    def get_polarity(self):
        """
        This method cleans the text in the comments and get its polarity.

        """

        METHOD_NAME = "get_polarity"
        try:

            # cleaning text:
            if "processed_text" not in self.df_comments_full.keys():
                self.df_comments_full["processed_text"] = self.df_comments_full[
                    "text"
                ].apply(
                    lambda msg: CleanText(msg).process_text(
                        mentions=True, hashtags=True, links=True, spec_chars=True
                    )
                )

            # drop empty comments
            self.df_comments_full = self.df_comments_full.dropna(
                subset=["processed_text"]
            )
            self.df_comments_full = self.df_comments_full.drop(
                self.df_comments_full[
                    self.df_comments_full["processed_text"] == ""
                ].index
            )

            # getting the polarity of the clean text
            if (
                "polarity" not in self.df_comments_full.keys()
                or None in self.df_comments_full.polarity.values
            ):
                self.df_comments_full = Polarity().polarity(self.df_comments_full)
                df_comments = self.df_comments_full
                df_comments = df_comments.dropna(subset=["polarity"])
                return df_comments
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_comments_full["processed_text"] = ""
            self.df_comments_full["polarity"] = ""

    def grouped_polarities(self, group_by="group"):
        """
        This method get the text's polarity using the method get polarity. It then groups the texts and their polarity. It returns a data frame with number of texts in each polarity category for each group.

        Parameters
        ----------
        group_by:
            type: string
            takes four possible values: 'account' when the texts are grouped by individual instagram account, 'group' when the texts are grouped by the pre-defined (in the df_groups data frame) categories, 'all' when only one group contains all the analysed texts, and 'STTM_group' when the grouping is done using the clustering categories from an sttm algorithm. if no grouping information is found the default is "all"

        Returns
        df_groupedpolarity:
        Pandas DataFrame with with number of texts in each polarity category for each group.
        ----------
        """
        METHOD_NAME = "grouped_polarities"

        if (
            "polarity" not in self.df_comments_full.keys()
            or None in self.df_comments_full.polarity.values
        ):
            self.get_polarity()

        try:
            if "post_owner_id" in self.df_comments_full.keys():
                self.df_comments_full["group"] = self.df_comments_full[
                    "post_owner_id"
                ].apply(lambda pid: general_utils.get_group(pid, self.groups))
            else:
                self.df_comments_full["group"] = "no group"
                print(
                    "Warning: in Polarity_distibution_IG.grouped polarities no 'post_owner_id' column in DataFrame"
                )

            if "post_owner_username" not in self.df_comments_full.keys():
                print(
                    "Warning: in Polarity_distibution_IG.grouped polarities no 'post_owner_username' column in DataFrame"
                )
                self.df_comments_full["post_owner_username"] = "no name"

            self.df_comments_full["all"] = "all groups"

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            if "group" not in self.df_comments_full.keys():
                self.df_comments_full["group"] = "no group"
            if "post_owner_username" not in self.df_comments_full.keys():
                self.df_comments_full["post_owner_username"] = "no name"
            self.df_comments_full["all"] = "all groups"
            self.df_comments_full = self.df_comments_full.dropna(subset=["polarity"])

        try:
            if group_by == "post":
                df_groupedpolarity = (
                    self.df_comments_full.groupby(
                        ["shortcode", "post_owner_id", "post_owner_username", "group"]
                    )["polarity"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                df_groupedpolarity = df_groupedpolarity.reset_index().rename(
                    columns={
                        "shortcode": "post_id",
                        "post_owner_id": "_object_id",
                        "post_owner_username": "_object_name",
                    }
                )
                return df_groupedpolarity[
                    ["_object_id", "_object_name", "post_id", "sentiment", "group"]
                ]
            elif group_by == "account":
                df_groupedpolarity = (
                    self.df_comments_full.groupby(
                        ["post_owner_id", "post_owner_username", "group"]
                    )["polarity"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                df_groupedpolarity = df_groupedpolarity.reset_index().rename(
                    columns={
                        "post_owner_id": "_object_id",
                        "post_owner_username": "_object_name",
                    }
                )
                return df_groupedpolarity[
                    ["_object_id", "_object_name", "group", "sentiment"]
                ]
            elif group_by == "group":
                df_groupedpolarity = (
                    self.df_comments_full.groupby("group")["polarity"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                return df_groupedpolarity.reset_index()[["group", "sentiment"]]
            elif group_by == "all":
                df_groupedpolarity = (
                    self.df_comments_full.groupby("all")["polarity"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                return df_groupedpolarity.reset_index()[["all", "sentiment"]]
            elif group_by == "time-account":
                df_groupedpolarity = (
                    self.df_comments_full.groupby(
                        [
                            "created_at_utc",
                            "post_owner_id",
                            "post_owner_username",
                            "shortcode",
                            "group",
                        ]
                    )["polarity"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                df_groupedpolarity = df_groupedpolarity.reset_index().rename(
                    columns={
                        "created_at_utc": "created_time",
                        "post_owner_id": "_object_id",
                        "shortcode": "post_id",
                        "post_owner_username": "_object_name",
                    }
                )
                columns = [
                    "created_time",
                    "_object_id",
                    "_object_name",
                    "sentiment",
                    "post_id",
                ]
                if self.r_group == True:
                    columns.append("group")
                return df_groupedpolarity[columns].reset_index()
            else:
                print(
                    f"Warning: {group_by} Invalid parameter value for parameter group_by, grouping by all"
                )
                df_groupedpolarity = (
                    self.df_comments_full.groupby("all")["polarity"]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                return df_groupedpolarity.reset_index()[["all", "sentiment"]]

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            if group_by == "account":
                df_groupedpolarity = pd.DataFrame(
                    columns=["_object_id", "_object_name", "group", "sentiment"]
                )
            elif group_by == "group":
                df_groupedpolarity = pd.DataFrame(columns=["group", "sentiment"])
            elif group_by == "all":
                df_groupedpolarity = pd.DataFrame(columns=["all", "sentiment"])
            else:
                print(
                    f"Warning: {group_by} Invalid parameter value for parameter group_by, grouping by all"
                )
                df_groupedpolarity = pd.DataFrame(columns=["all", "sentiment"])
            return df_groupedpolarity
