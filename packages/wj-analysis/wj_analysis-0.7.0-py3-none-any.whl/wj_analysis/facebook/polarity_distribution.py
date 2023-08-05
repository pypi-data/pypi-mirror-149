import sys
from copy import deepcopy

import pandas as pd

from ..common import general_utils
from ..common.nlp_utils import CleanText, Features, Polarity  # , Polarity2

ERR_SYS = "\nSystem error: "


def get_name(pid, dict_page_id_to_name):
    try:
        out_name = dict_page_id_to_name[pid]
    except Exception:
        out_name = "no_name"
    return out_name


class PolarityDistributionFB:
    """
    This class computes the polarity of the texts.
    """

    def __init__(self, df_comments, df_pages, groups, r_group=False):
        """
        This method stores the input DataFrames and checks that they are not empty'.

        Parameters
        ----------
        df_comments:
            type: DataFrame
            Information of the comments.
            This Pandas DataFrame must have columns 'post_id', 'message' and 'page_id'.
        df_pages:
            type: DataFrame
            Information of the pages.
            This Pandas DataFrame must have columns 'page_id' and 'name'.
            It is used just to set the page name in the DataFrame 'df_comments'. That page name corresponds of the page of the post to wich the comment is asociated.
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
        self.df_pages = df_pages
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

        try:
            if df_pages.empty:
                print("Warning: page names DataFrame is empty.")
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_pages = pd.DataFrame(columns=[""])

    def get_polarity(self):
        """
        This method cleans the text in the comments and get its polarity.

        """
        METHOD_NAME = "get_polarity"

        try:

            # cleaning text:
            if "processed_text" not in self.df_comments_full.keys():
                self.df_comments_full["processed_text"] = self.df_comments_full[
                    "message"
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
            takes four possible values: 'account' when the texts are grouped by individual facebook account, 'group' when the texts are grouped by the pre-defined (in the df_groups data frame) group categories, 'all' when only one group contains all the analysed texts, and 'STTM_group' when the grouping is done using the clustering categories from an sttm algorithm. if no grouping information is found the default is "all"

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
            if "post_id" in self.df_comments_full.keys():
                self.df_comments_full["page_id"] = self.df_comments_full.post_id.apply(
                    lambda x: str(x).split("_")[0]
                )
                page_id_name_fb = {}
                for idd, row in self.df_pages.iterrows():
                    page_id_name_fb[row.page_id] = row["name"]
                self.df_comments_full[
                    "page_name"
                ] = self.df_comments_full.page_id.apply(
                    lambda pid: get_name(pid, page_id_name_fb)
                )
                self.df_comments_full["group"] = self.df_comments_full["page_id"].apply(
                    lambda pid: general_utils.get_group(pid, self.groups)
                )
            else:
                page_id_name_fb = {}
                for idd, row in self.df_pages.iterrows():
                    page_id_name_fb[row.page_id] = row["name"]
                self.df_comments_full[
                    "page_name"
                ] = self.df_comments_full.page_id.apply(
                    lambda pid: get_name(pid, page_id_name_fb)
                )
                self.df_comments_full["group"] = self.df_comments_full["page_id"].apply(
                    lambda pid: general_utils.get_group(pid, self.groups)
                )

            self.df_comments_full["all"] = "all groups"
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            if "page_name" not in self.df_comments_full.keys():
                self.df_comments_full["page_name"] = "no name"
            if "group" not in self.df_comments_full.keys():
                self.df_comments_full["group"] = "no group"
            self.df_comments_full["all"] = "all groups"
            self.df_comments_full = self.df_comments_full.dropna(subset=["polarity"])

        # groups texts and returns data frame
        try:
            if group_by == "post":
                df_groupedpolarity = (
                    self.df_comments_full.groupby(
                        ["post_id", "page_id", "page_name", "group"]
                    )["polarity"]
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
                    ["post_id", "_object_id", "_object_name", "group", "sentiment"]
                ]
            elif group_by == "account":
                df_groupedpolarity = (
                    self.df_comments_full.groupby(["page_id", "page_name", "group"])[
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
                        ["created_time", "page_id", "page_name", "post_id", "group"]
                    )["polarity"]
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
                df_groupedpolarity = df_groupedpolarity.sort_values(by=["created_time"])

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
