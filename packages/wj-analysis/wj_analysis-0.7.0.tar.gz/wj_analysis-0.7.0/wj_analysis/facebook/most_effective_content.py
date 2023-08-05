import ast
import re
import sys
import warnings
from copy import deepcopy

import pandas as pd

from ..common import general_utils
from ..common.nlp_utils import CleanText, Features

warnings.filterwarnings("ignore", "This pattern has match groups")
warnings.filterwarnings("ignore", category=DeprecationWarning)

ERR_SYS = "\nSystem error: "


class MostEffectiveContentFB:
    """
    This class computes the different atributes of the posts with
    higher engagement rate.
    """

    def __init__(self, df_posts, df_pages, groups):
        """
        This method computes the DataFrame 'df_posts_full'
        which contains all the information of the posts, including columns
        'page_name' and 'group'.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            Information of the posts.
            This Pandas DataFrame must have columns 'page_id',
            'page_name', 'message' and 'engagement_rate_by_post'.
        df_pages:
            type: DataFrame
            Information of the pages.
            This Pandas DataFrame must have columns 'page_id' and 'name.
            It is used just to set the page name in the DataFrame 'df_posts'.
        groups:
            type: dict
            Maps the groups (client, compentition, archetype, trends) to the
            corresponding page ids for each group.
        """

        METHOD_NAME = "__init__"

        POSTS_COLUMNS = [
            "page_id",
            "page_name",
            "post_id",
            "message",
            "permalink_url",
            "type",
            "message_tags",
            "group",
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post",
        ]

        OUTPUT_COLUMNS = [
            "page_id",
            "page_name",
            "post_id",
            "message",
            "permalink_url",
            "type",
            "message_tags",
            "group",
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post",
        ]

        self.features = None

        if len(df_posts) > 0 and len(df_pages) > 0:
            try:
                df_posts_full = deepcopy(df_posts[POSTS_COLUMNS])

                df_posts_full["group"] = df_posts_full["page_id"].apply(
                    lambda pid: general_utils.get_group(pid, groups)
                )

                self.df_posts_full = df_posts_full
                self.len_posts_full = len(self.df_posts_full)

            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)
                self.len_posts_full = len(self.df_posts_full)
        else:
            print("Warning: One of the DataFrames is empty. It cannot be computed.")
            self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)
            self.len_posts_full = len(self.df_posts_full)

    def posts(self, n_most_eff=5, engagement_rate="engagement_rate_by_post", **kwargs):
        """
        This function computes the DataFrame 'df_most_eff_posts_fb'
        which contains the posts with higher engagement rate for the accounts selected.

        Parameters
        ----------
        n_most_eff:
            type: int
            Number of posts to show, default=5.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "posts"

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_posts_fb = self.df_posts_full[
                self.df_posts_full.page_id.isin(account_ids)
            ][
                [
                    "page_id",
                    "page_name",
                    "post_id",
                    "message",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "permalink_url",
                ]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_fb = self.df_posts_full[
                self.df_posts_full.page_name.isin(account_names)
            ][
                [
                    "page_id",
                    "page_name",
                    "post_id",
                    "message",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "permalink_url",
                ]
            ]
        else:
            df_most_eff_posts_fb = deepcopy(
                self.df_posts_full[
                    [
                        "page_id",
                        "page_name",
                        "post_id",
                        "message",
                        engagement_rate,
                        "rel_" + engagement_rate,
                        "permalink_url",
                    ]
                ]
            )
        try:
            df_most_eff_posts_fb = df_most_eff_posts_fb.sort_values(
                engagement_rate, ascending=False
            ).head(n_most_eff)

            return df_most_eff_posts_fb

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=[
                    "page_id",
                    "page_name",
                    "post_id",
                    "message",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "permalink_url",
                ]
            )

    def posts_type(
        self,
        from_n_most_eff=None,
        engagement_rate="engagement_rate_by_post",
        grouped=True,
        **kwargs,
    ):
        """
        This function computes the DataFrame 'df_most_eff_posts_type_tw'
        which contains for each media type its proportion to the whole number of posts
        and its average engagement rate.

        Parameters
        ----------
        from_n_most_eff:
            type: int
            Number of posts to compute the ratios from, default=None means
            the computations is against all posts.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "posts_type"

        if not from_n_most_eff:
            from_n_most_eff = self.len_posts_full

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["page_id", "page_name"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_posts_type_fb = self.df_posts_full[
                self.df_posts_full.page_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["type", "message", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_type_fb = self.df_posts_full[
                self.df_posts_full.page_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["type", "message", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_posts_type_fb = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + ["type", "message", engagement_rate, "rel_" + engagement_rate]
                ]
            )

        try:
            df_most_eff_posts_type_fb = df_most_eff_posts_type_fb.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            df_most_eff_posts_type_fb["message_count"] = 1
            df_most_eff_posts_type_fb = (
                df_most_eff_posts_type_fb[
                    PAGE_COLUMNS
                    + [
                        "type",
                        "message_count",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
                .groupby(PAGE_COLUMNS + ["type"])
                .agg(
                    {
                        "message_count": "count",
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                    }
                )
            )
            df_most_eff_posts_type_fb = df_most_eff_posts_type_fb.rename(
                columns={
                    "message_count": "counts",
                    engagement_rate: "avg_engagement_rate",
                    "rel_" + engagement_rate: "avg_rel_engagement_rate",
                }
            )
            if PAGE_COLUMNS:
                df_most_eff_posts_type_fb["percentage"] = (
                    df_most_eff_posts_type_fb["counts"]
                    .groupby(level=0)
                    .apply(lambda c: 100.0 * c / float(c.sum()))
                    .round(2)
                )
                df_most_eff_posts_type_fb = (
                    df_most_eff_posts_type_fb.reset_index().rename(
                        columns={
                            PAGE_COLUMNS[0]: "_object_id",
                            PAGE_COLUMNS[1]: "_object_name",
                        }
                    )
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            else:
                df_most_eff_posts_type_fb["percentage"] = (
                    100.0
                    * df_most_eff_posts_type_fb["counts"]
                    / df_most_eff_posts_type_fb["counts"].sum()
                ).round(2)
                df_most_eff_posts_type_fb = df_most_eff_posts_type_fb.reset_index()

            return df_most_eff_posts_type_fb.sort_values(
                PAGE_COLUMNS + ["avg_engagement_rate"], ascending=False
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            return pd.DataFrame(
                columns=[
                    "type",
                    "counts",
                    "avg_engagement_rate",
                    "avg_rel_engagement_rate",
                    "percentage",
                ]
            )

    def construct_most_eff_objects(
        self,
        df_most_eff_objects_fb,
        objs,
        engagement_rate="engagement_rate_by_post",
        grouped=True,
        sort_column="engagement_rate_by_post",
    ):
        """
        This function computes the output DataFrame for words, hashtags or mentions
        with their respective count and engagement rate.

        Parameters
        ----------
        df_most_eff_objects_fb:
            type: DataFrame
            DataFrame with objects (hashtags or mentions) to extract.
        objs:
            type: str
            Objects (hashtags or mentions) to compute the DataFrame.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        sort_column:
            Column to sort the output DataFrame,
            default='engagement_rate_by_post'.

        Returns
        -------
        DataFrames
        """

        METHOD_NAME = "construct_most_eff_objects"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["page_id", "page_name"]

        try:
            objs_fb = []
            objs_eff_fb = []
            objs_rel_eff_fb = []
            objs_group_fb = []
            if PAGE_COLUMNS:
                objs_ids_fb = []
                objs_names_fb = []
            objs_counts_fb = []

            for _, row in df_most_eff_objects_fb.iterrows():
                objs_fb = objs_fb + row[objs]
                objs_eff_fb = objs_eff_fb + [row[engagement_rate]] * len(row[objs])
                objs_rel_eff_fb = objs_rel_eff_fb + [
                    row["rel_" + engagement_rate]
                ] * len(row[objs])
                objs_group_fb = objs_group_fb + [row.group] * len(row[objs])
                if PAGE_COLUMNS:
                    objs_ids_fb = objs_ids_fb + [row[PAGE_COLUMNS[0]]] * len(row[objs])
                    objs_names_fb = objs_names_fb + [row[PAGE_COLUMNS[1]]] * len(
                        row[objs]
                    )
                objs_counts_fb = objs_counts_fb + [1] * len(row[objs])

            most_eff_objs_fb = pd.DataFrame(
                {
                    objs[:-1]: objs_fb,
                    engagement_rate: objs_eff_fb,
                    "rel_" + engagement_rate: objs_rel_eff_fb,
                    "group": objs_group_fb,
                    f"{objs[:-1]}_count": objs_counts_fb,
                }
            )

            if PAGE_COLUMNS:
                most_eff_objs_fb[PAGE_COLUMNS[0]] = objs_ids_fb
                most_eff_objs_fb[PAGE_COLUMNS[1]] = objs_names_fb

            most_eff_objs_fb = (
                most_eff_objs_fb.groupby(PAGE_COLUMNS + ["group", objs[:-1]])
                .agg(
                    {
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                        f"{objs[:-1]}_count": "sum",
                    }
                )
                .sort_values(PAGE_COLUMNS + [sort_column], ascending=False)
                .reset_index()
            )

            return most_eff_objs_fb

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            most_eff_objs_fb = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    objs[:-1],
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    f"{objs[:-1]}_count",
                ]
            )

            return most_eff_objs_fb

    def hashtags_mentions(
        self,
        compare_group="brand",
        from_n_most_eff=None,
        engagement_rate="engagement_rate_by_post",
        grouped=True,
        **kwargs,
    ):
        """
        This function computes the following DataFrames:
          - 'most_eff_hashtags_fb' and 'most_eff_mentions_fb'
            which contains the hastags and mentions with higher associated
            engagement rate for the accounts selected.

          - 'compare_hashtags_fb' and 'compare_mentions_fb'
            which contains the most used hastags and mentions for the account
            to compare with.

        Parameters
        ----------
        compare_group:
            type: str
            Name of the group to compare with. default='brand'.
        from_n_most_eff:
            type: int
            Number of posts to compute the ratios from, default=None means
            the computations is against all posts.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        Tuple of DataFrames
        """

        METHOD_NAME = "hashtags_mentions"

        if not from_n_most_eff:
            from_n_most_eff = self.len_posts_full

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["page_id", "page_name"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_hashtags_mentions_fb = self.df_posts_full[
                self.df_posts_full.page_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["message_tags", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_hashtags_mentions_fb = self.df_posts_full[
                self.df_posts_full.page_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["message_tags", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_hashtags_mentions_fb = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + [
                        "message_tags",
                        "group",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
            )

        df_compare_hashtags_mentions_fb = self.df_posts_full[
            self.df_posts_full.group == compare_group
        ][
            PAGE_COLUMNS
            + ["message_tags", "group", engagement_rate, "rel_" + engagement_rate]
        ]

        try:
            df_most_eff_hashtags_mentions_fb = df_most_eff_hashtags_mentions_fb[
                ~df_most_eff_hashtags_mentions_fb.message_tags.isna()
            ]

            df_most_eff_hashtags_mentions_fb = df_most_eff_hashtags_mentions_fb[
                (
                    (df_most_eff_hashtags_mentions_fb["message_tags"] != "None")
                    & (df_most_eff_hashtags_mentions_fb["message_tags"] != "[]")
                )
            ]
            df_most_eff_hashtags_mentions_fb.message_tags = (
                df_most_eff_hashtags_mentions_fb.message_tags.apply(
                    lambda _json: ast.literal_eval(_json)
                )
            )

            df_most_eff_hashtags_mentions_fb[
                "mentions"
            ] = df_most_eff_hashtags_mentions_fb.message_tags.apply(
                lambda tags: [
                    tag["name"] for tag in tags if not re.search(r"^#.*", tag["name"])
                ]
            )
            df_most_eff_hashtags_mentions_fb[
                "mentions"
            ] = df_most_eff_hashtags_mentions_fb["mentions"].apply(
                lambda ments: ments if ments else None
            )

            df_most_eff_hashtags_mentions_fb[
                "hashtags"
            ] = df_most_eff_hashtags_mentions_fb.message_tags.apply(
                lambda tags: [
                    tag["name"] for tag in tags if re.search(r"^#.*", tag["name"])
                ]
            )
            df_most_eff_hashtags_mentions_fb[
                "hashtags"
            ] = df_most_eff_hashtags_mentions_fb["hashtags"].apply(
                lambda hashs: hashs if hashs else None
            )

            df_compare_hashtags_mentions_fb = df_compare_hashtags_mentions_fb[
                ~df_compare_hashtags_mentions_fb.message_tags.isna()
            ]
            df_compare_hashtags_mentions_fb = df_compare_hashtags_mentions_fb[
                (
                    (df_compare_hashtags_mentions_fb["message_tags"] != "None")
                    & (df_compare_hashtags_mentions_fb["message_tags"] != "[]")
                )
            ]
            df_compare_hashtags_mentions_fb.message_tags = (
                df_compare_hashtags_mentions_fb.message_tags.apply(
                    lambda _json: ast.literal_eval(_json)
                )
            )

            df_compare_hashtags_mentions_fb[
                "mentions"
            ] = df_compare_hashtags_mentions_fb.message_tags.apply(
                lambda tags: [
                    tag["name"] for tag in tags if not re.search(r"^#.*", tag["name"])
                ]
            )
            df_compare_hashtags_mentions_fb[
                "mentions"
            ] = df_compare_hashtags_mentions_fb["mentions"].apply(
                lambda ments: ments if ments else None
            )

            df_compare_hashtags_mentions_fb[
                "hashtags"
            ] = df_compare_hashtags_mentions_fb.message_tags.apply(
                lambda tags: [
                    tag["name"] for tag in tags if re.search(r"^#.*", tag["name"])
                ]
            )
            df_compare_hashtags_mentions_fb[
                "hashtags"
            ] = df_compare_hashtags_mentions_fb["hashtags"].apply(
                lambda hashs: hashs if hashs else None
            )

            df_most_eff_hashtags_mentions_fb = (
                df_most_eff_hashtags_mentions_fb.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            df_compare_hashtags_mentions_fb = (
                df_compare_hashtags_mentions_fb.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            # Hashtags
            df_most_eff_hashtags_fb = df_most_eff_hashtags_mentions_fb[
                ~df_most_eff_hashtags_mentions_fb["hashtags"].isna()
            ]
            most_eff_hashtags_fb = self.construct_most_eff_objects(
                df_most_eff_hashtags_fb, objs="hashtags", grouped=grouped
            )

            # Group to compare with
            df_compare_hashtags_fb = df_compare_hashtags_mentions_fb[
                ~df_compare_hashtags_mentions_fb["hashtags"].isna()
            ]
            compare_hashtags_fb = self.construct_most_eff_objects(
                df_compare_hashtags_fb,
                objs="hashtags",
                grouped=grouped,
                sort_column="hashtag_count",
            )

            # Mentions
            df_most_eff_mentions_fb = df_most_eff_hashtags_mentions_fb[
                ~df_most_eff_hashtags_mentions_fb["mentions"].isna()
            ]
            most_eff_mentions_fb = self.construct_most_eff_objects(
                df_most_eff_mentions_fb, objs="mentions", grouped=grouped
            )

            # Group to compare with
            df_compare_mentions_fb = df_compare_hashtags_mentions_fb[
                ~df_compare_hashtags_mentions_fb["mentions"].isna()
            ]
            compare_mentions_fb = self.construct_most_eff_objects(
                df_compare_mentions_fb,
                objs="mentions",
                grouped=grouped,
                sort_column="mention_count",
            )

            if PAGE_COLUMNS:
                most_eff_hashtags_fb = most_eff_hashtags_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_hashtags_fb = compare_hashtags_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_mentions_fb = most_eff_mentions_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_mentions_fb = compare_mentions_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]

            return (
                most_eff_hashtags_fb,
                compare_hashtags_fb,
                most_eff_mentions_fb,
                compare_mentions_fb,
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_hashtags_fb = pd.DataFrame(
                columns=[
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "hashtag_count",
                ]
            )
            compare_hashtags_fb = pd.DataFrame(
                columns=[
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "hashtag_count",
                ]
            )
            most_eff_mentions_fb = pd.DataFrame(
                columns=[
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "mention_count",
                ]
            )
            compare_mentions_fb = pd.DataFrame(
                columns=[
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "mention_count",
                ]
            )
            return (
                most_eff_hashtags_fb,
                compare_hashtags_fb,
                most_eff_mentions_fb,
                compare_mentions_fb,
            )

    def construct_most_eff_words(
        self,
        df_most_eff_words_fb,
        lemmatize=False,
        engagement_rate="engagement_rate_by_post",
        grouped=True,
        min_count=2,
    ):
        """
        This function computes the output DataFrame for words, hashtags or mentions
        with their respective count and engagement rate.

        Parameters
        ----------
        df_most_eff_objects_fb:
            type: DataFrame
            DataFrame with words to extract.
        lemmatize:
            type: bool
            True if the lemmas are desired instead of words. default=False.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        min_count:
            type: int
            Minimum number of counts on the word to consider in the analysis.

        Returns
        -------
        DataFrames
        """

        METHOD_NAME = "construct_most_eff_words"

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["page_id", "page_name"]

        try:
            words_fb = []
            lemmas_fb = []
            pos_tags_fb = []
            words_counts_fb = []
            words_eff_fb = []
            words_rel_eff_fb = []
            words_group_fb = []
            if PAGE_COLUMNS:
                words_ids_fb = []
                words_names_fb = []
            for _, row in df_most_eff_words_fb.iterrows():
                words_fb = words_fb + row.words
                lemmas_fb = lemmas_fb + row.lemmas
                pos_tags_fb = pos_tags_fb + row.pos_tags
                words_counts_fb = words_counts_fb + [1] * len(row.words)
                words_eff_fb = words_eff_fb + [row[engagement_rate]] * len(row.words)
                words_rel_eff_fb = words_rel_eff_fb + [
                    row["rel_" + engagement_rate]
                ] * len(row.words)
                words_group_fb = words_group_fb + [row.group] * len(row.words)
                if PAGE_COLUMNS:
                    words_ids_fb = words_ids_fb + [row[PAGE_COLUMNS[0]]] * len(
                        row.words
                    )
                    words_names_fb = words_names_fb + [row[PAGE_COLUMNS[1]]] * len(
                        row.words
                    )

            most_eff_words_fb = pd.DataFrame(
                {
                    "word": words_fb,
                    "lemma": lemmas_fb,
                    "pos_tag": pos_tags_fb,
                    "word_count": words_counts_fb,
                    engagement_rate: words_eff_fb,
                    "rel_" + engagement_rate: words_rel_eff_fb,
                    "group": words_group_fb,
                }
            )

            if PAGE_COLUMNS:
                most_eff_words_fb[PAGE_COLUMNS[0]] = words_ids_fb
                most_eff_words_fb[PAGE_COLUMNS[1]] = words_names_fb

            if lemmatize:
                word_column = "lemma"
            else:
                word_column = "word"
            most_eff_words_fb = (
                most_eff_words_fb[
                    PAGE_COLUMNS
                    + [
                        "pos_tag",
                        "group",
                        word_column,
                        "word_count",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
                .groupby(PAGE_COLUMNS + ["pos_tag", "group", word_column])
                .agg(
                    {
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                        "word_count": "sum",
                    }
                )
            )
            most_eff_words_fb = most_eff_words_fb[
                most_eff_words_fb["word_count"] >= min_count
            ]

            most_eff_words_fb = most_eff_words_fb.sort_values(
                PAGE_COLUMNS + ["pos_tag", "group", engagement_rate], ascending=False
            ).reset_index()

            most_eff_nouns_fb = most_eff_words_fb[
                most_eff_words_fb["pos_tag"] == "NOUN"
            ]
            most_eff_verbs_fb = most_eff_words_fb[
                most_eff_words_fb["pos_tag"] == "VERB"
            ]
            most_eff_adjs_fb = most_eff_words_fb[most_eff_words_fb["pos_tag"] == "ADJ"]

            return (
                most_eff_words_fb,
                most_eff_nouns_fb,
                most_eff_verbs_fb,
                most_eff_adjs_fb,
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if lemmatize:
                word_column = "lemma"
            else:
                word_column = "word"
            most_eff_words_fb = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "pos_tag",
                    "group",
                    word_column,
                    "word_count",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            )
            show_columns = PAGE_COLUMNS + [
                "group",
                "word",
                engagement_rate,
                "rel_" + engagement_rate,
                "word_count",
            ]
            most_eff_nouns_fb = pd.DataFrame(columns=show_columns)
            most_eff_verbs_fb = pd.DataFrame(columns=show_columns)
            most_eff_adjs_fb = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words_fb,
                most_eff_nouns_fb,
                most_eff_verbs_fb,
                most_eff_adjs_fb,
            )

    def words(
        self,
        lemmatize=False,
        from_n_most_eff=None,
        min_count=2,
        engagement_rate="engagement_rate_by_post",
        grouped=True,
        **kwargs,
    ):
        """
        This function computes the following DataFrames:
          - 'most_eff_words_fb'
            which contains the words with higher associated
            engagement rate for the accounts selected, it is tagged with
            the part of speech tag of the word.

          - most_eff_nouns_fb, most_eff_verbs_fb and most_eff_adjs_fb
            which contains the nouns, verbs and adjectives with higher associated
            engagement rate for the accounts selected, it is tagged with
            the part of speech tag of the word.

        Parameters
        ----------
        lemmatize:
            type: bool
            True if the lemmas are desired instead of words. default=False.
        from_n_most_eff:
            type: int
            Number of posts to compute the ratios from, default=None means
            the computations is against all posts.
        min_count:
            type: int
            Minimum number of counts on the word to consider in the analysis.
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
        grouped:
            type: bool
            Determines if the output is returned grouped by group or account,
            default=True.
        **kwargs:
            account_ids:
                type: list
                Ids of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.
            account_names:
                type: list
                Name of the accounts to look for.
                If [] takes all the posts in the DataFrame posts.

        Returns
        -------
        Tuple of DataFrames
        """

        METHOD_NAME = "words"

        if not self.features:
            self.features = Features()

        if not from_n_most_eff:
            from_n_most_eff = self.len_posts_full

        PAGE_COLUMNS = []
        if not grouped:
            PAGE_COLUMNS = ["page_id", "page_name"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_words_fb = self.df_posts_full[
                self.df_posts_full.page_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["message", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_words_fb = self.df_posts_full[
                self.df_posts_full.page_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["message", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_words_fb = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + ["message", "group", engagement_rate, "rel_" + engagement_rate]
                ]
            )

        try:
            df_most_eff_words_fb = df_most_eff_words_fb.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            if "processed_text" not in df_most_eff_words_fb.keys():
                df_most_eff_words_fb[
                    "processed_text"
                ] = df_most_eff_words_fb.message.apply(
                    lambda msg: CleanText(msg).process_text(
                        mentions=True, hashtags=True, links=True, spec_chars=True
                    )
                )
            df_most_eff_words_fb["processed_text"] = df_most_eff_words_fb[
                "processed_text"
            ].apply(lambda txt: self.features.pos_tags(txt))

            df_most_eff_words_fb["words"] = df_most_eff_words_fb[
                "processed_text"
            ].apply(lambda pt: pt["words"])
            df_most_eff_words_fb["lemmas"] = df_most_eff_words_fb[
                "processed_text"
            ].apply(lambda pt: pt["lemmas"])
            df_most_eff_words_fb["pos_tags"] = df_most_eff_words_fb[
                "processed_text"
            ].apply(lambda pt: pt["pos_tags"])

            df_most_eff_words_fb = df_most_eff_words_fb[
                ~df_most_eff_words_fb["processed_text"].isna()
            ]

            (
                most_eff_words_fb,
                most_eff_nouns_fb,
                most_eff_verbs_fb,
                most_eff_adjs_fb,
            ) = self.construct_most_eff_words(
                df_most_eff_words_fb,
                lemmatize=lemmatize,
                engagement_rate=engagement_rate,
                grouped=grouped,
                min_count=min_count,
            )

            if PAGE_COLUMNS:
                most_eff_words_fb = most_eff_words_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_nouns_fb = most_eff_nouns_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_verbs_fb = most_eff_verbs_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_adjs_fb = most_eff_adjs_fb.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]

            show_columns = PAGE_COLUMNS + [
                "group",
                "word",
                engagement_rate,
                "rel_" + engagement_rate,
                "word_count",
            ]

            return (
                most_eff_words_fb,
                most_eff_nouns_fb[show_columns],
                most_eff_verbs_fb[show_columns],
                most_eff_adjs_fb[show_columns],
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_words_fb = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "pos_tag",
                    "group",
                    "word",
                    "word_count",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            )
            show_columns = PAGE_COLUMNS + [
                "group",
                "word",
                engagement_rate,
                "rel_" + engagement_rate,
                "word_count",
            ]
            most_eff_nouns_fb = pd.DataFrame(columns=show_columns)
            most_eff_verbs_fb = pd.DataFrame(columns=show_columns)
            most_eff_adjs_fb = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words_fb,
                most_eff_nouns_fb,
                most_eff_verbs_fb,
                most_eff_adjs_fb,
            )
