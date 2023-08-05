import sys
from copy import deepcopy

import pandas as pd

from ..common import general_utils
from ..common.nlp_utils import CleanText, Features, Polarity  # , Polarity2

ERR_SYS = "\nSystem error: "


class PolarityDistributionTW:
    """
    This class computes the polarity of the texts.
    """

    def __init__(self, df_replies, groups, r_group=False):
        """
        This method stores the input DataFrames and checks that they are not empty'.

        Parameters
        ----------
        df_replies:
            type: DataFrame
            Information of the tweets or the twitter replies.
            This Pandas DataFrame must have columns 'text', 'twitter_id', 'screen_name',  and 'replying_to_id' and 'replying_to' if the data frame contains tweet replies.
        df_users:
            type: DataFrame
            Information of the twitter users.
        groups:
            type: dict
            Maps the groups (client, competition, archetype, trends) to the
            corresponding page ids for each group.
        r_group:
            type: bool
            varibale that indicates if the class return the column group
        """
        METHOD_NAME = "__init__"
        df_replies_full = deepcopy(df_replies)
        self.df_replies_full = df_replies_full
        self.groups = groups
        self.r_group = r_group

        try:
            if df_replies.empty:
                print("Warning: input data DataFrame is empty.")
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_replies_full = pd.DataFrame(columns=[""])

    def get_polarity(self):
        """
        This method cleans the text in the replies and get its polarity.

        """
        METHOD_NAME = "get_polarity"

        try:

            # cleaning text:
            if "processed_text" not in self.df_replies_full.keys():
                self.df_replies_full["processed_text"] = self.df_replies_full[
                    "text"
                ].apply(
                    lambda msg: CleanText(msg).process_text(
                        mentions=True, hashtags=True, links=True, spec_chars=True
                    )
                )

            # drop empty comments
            self.df_replies_full = self.df_replies_full.dropna(
                subset=["processed_text"]
            )
            self.df_replies_full = self.df_replies_full.drop(
                self.df_replies_full[self.df_replies_full["processed_text"] == ""].index
            )

            # getting the polarity of the clean text
            if (
                "polarity" not in self.df_replies_full.keys()
                or None in self.df_replies_full.polarity.values
            ):
                self.df_replies_full = Polarity().polarity(df_text=self.df_replies_full)
                data_replies = self.df_replies_full
                return data_replies
                # return polarity_dataframe(df, '_text')
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_replies_full["processed_text"] = ""
            self.df_replies_full["polarity"] = ""

    def grouped_polarities(self, group_by="group"):
        """
        This method get the text's polarity using the method get polarity. It then groups the texts and their polarity. It returns a data frame with number of texts in each polarity category for each group.

        Parameters
        ----------
        group_by:
            type: string
            takes four possible values: 'account' when the texts are grouped by individual twitter account, 'group' when the texts are grouped by the pre-defined (in the df_groups data frame) categories, 'all' when only one group contains all the analysed texts, and 'STTM_group' when the grouping is done using the clustering categories from an sttm algorithm. if no grouping information is found the default is "all"

        Returns
        df_groupedpolarity:
        Pandas DataFrame with with number of texts in each polarity category for each group.
        ----------
        """
        METHOD_NAME = "grouped_polarities"

        if (
            "polarity" not in self.df_replies_full.keys()
            or None in self.df_replies_full.polarity.values
        ):
            self.get_polarity()
        try:
            if "replying_to" in self.df_replies_full.keys():
                self.df_replies_full["page_name"] = self.df_replies_full["replying_to"]
                self.df_replies_full[
                    "group"
                ] = self.df_replies_full.replying_to_id.apply(
                    lambda pid: general_utils.get_group(pid, self.groups)
                )
                self.df_replies_full["page_id"] = self.df_replies_full["replying_to_id"]

            else:
                self.df_replies_full["page_name"] = self.df_replies_full["screen_name"]
                self.df_replies_full["group"] = self.df_replies_full.twitter_id.apply(
                    lambda pid: general_utils.get_group(pid, self.groups)
                )
                self.df_replies_full["page_id"] = self.df_replies_full["twitter_id"]
            self.df_replies_full["all"] = "all groups"

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            print(
                "Warning: in Polarity_distibution_TW.grouped_polarities no 'replying_to' or 'screen_name' column in DataFrame"
            )
            if "page_name" not in self.df_replies_full.keys():
                self.df_replies_full["page_name"] = "no name"
            if "group" not in self.df_replies_full.keys():
                self.df_replies_full["group"] = "no group"
            self.df_replies_full["all"] = "all groups"

        try:
            if group_by == "post":
                df_groupedpolarity = (
                    self.df_replies_full.groupby(
                        ["in_reply_to_status_id", "page_id", "page_name", "group"]
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
                        "in_reply_to_status_id": "post_id",
                        "page_id": "_object_id",
                        "page_name": "_object_name",
                    }
                )
                return df_groupedpolarity[
                    ["post_id", "_object_id", "_object_name", "group", "sentiment"]
                ]
            elif group_by == "account":
                df_groupedpolarity = (
                    self.df_replies_full.groupby(["page_id", "page_name", "group"])[
                        "polarity"
                    ]
                    .value_counts()
                    .unstack()
                    .fillna(0)
                )
                df_groupedpolarity["sentiment"] = df_groupedpolarity.to_dict(
                    orient="records"
                )
                df_groupedpolarity = df_groupedpolarity.reset_index().rename(
                    columns={"page_id": "_object_id", "page_name": "_object_name"}
                )
                return df_groupedpolarity[
                    ["_object_id", "_object_name", "group", "sentiment"]
                ]
            elif group_by == "group":
                df_groupedpolarity = (
                    self.df_replies_full.groupby("group")["polarity"]
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
                    self.df_replies_full.groupby("all")["polarity"]
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
                    self.df_replies_full.groupby(
                        [
                            "created_at",
                            "page_id",
                            "page_name",
                            "group",
                            "in_reply_to_status_id",
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
                        "created_at": "created_time",
                        "page_id": "_object_id",
                        "page_name": "_object_name",
                        "in_reply_to_status_id": "post_id",
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
                    self.df_replies_full.groupby("all")["polarity"]
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
