import json
import sys
import warnings
from copy import deepcopy

import pandas as pd

from ..common import general_utils
from ..common.nlp_utils import CleanText, Features

warnings.filterwarnings("ignore", "This pattern has match groups")
warnings.filterwarnings("ignore", category=DeprecationWarning)

ERR_SYS = "\nSystem error: "


class MostEffectiveContentIG:
    """
    This class computes the different atributes of the posts with
    higher engagement rate.
    """

    def __init__(self, df_posts, groups, mode="status"):
        """
        This method computes the DataFrame 'df_posts_full'
        which contains all the information of the posts, including column
        'group'.

        Parameters
        ----------
        df_posts:
            type: DataFrame
            Information of the posts.
            This Pandas DataFrame must have columns 'page_id',
            'page_name', 'message' and 'engagement_rate_by_post'.
        groups:
            type: dict
            Maps the groups (client, compentition, archetype, trends) to the
            corresponding page ids for each group.
        """

        METHOD_NAME = "__init__"

        self.features = None
        self.mode = mode

        if self.mode == "status":

            POSTS_COLUMNS = [
                "owner_id",
                "owner_username",
                "shortcode",
                "caption",
                "typename",
                "caption_hashtags",
                "caption_mentions",
                "group",
                "engagement_rate_by_post",
                "rel_engagement_rate_by_post",
            ]

            OUTPUT_COLUMNS = [
                "owner_id",
                "owner_username",
                "shortcode",
                "caption",
                "typename",
                "caption_hashtags",
                "caption_mentions",
                "group",
                "engagement_rate_by_post",
                "rel_engagement_rate_by_post",
            ]

            if len(df_posts) > 0:
                try:
                    df_posts_full = deepcopy(df_posts[POSTS_COLUMNS])
                    df_posts_full["owner_id"] = df_posts_full["owner_id"].apply(
                        lambda uid: str(uid)
                    )

                    df_posts_full["group"] = df_posts_full["owner_id"].apply(
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
                print("Warning: The DataFrame is empty. It cannot be computed.")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)
                self.len_posts_full = len(self.df_posts_full)

        elif self.mode == "hashtags":
            HASHTAGS_COLUMNS = [
                "followers",
                "group",
                "likes_count",
                "comment_count",
                "typename",
                "caption",
                "engagement_rate_by_post",
            ]
            OUTPUT_COLUMNS = [
                "followers",
                "group",
                "likes_count",
                "comment_count",
                "typename",
                "caption",
                "engagement_rate_by_post",
            ]
            try:
                df_posts_full = deepcopy(df_posts[HASHTAGS_COLUMNS])
                # rel_engagement no tiene sentido en este caso por eso está quemado
                df_posts_full["rel_engagement_rate_by_post"] = df_posts_full[
                    "engagement_rate_by_post"
                ]

                self.df_posts_full = df_posts_full
                self.len_posts_full = len(self.df_posts_full)
            except Exception:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_posts_full = pd.DataFrame(columns=OUTPUT_COLUMNS)
                self.len_posts_full = len(self.df_posts_full)

    def posts(self, n_most_eff=5, engagement_rate="engagement_rate_by_post", **kwargs):
        """
        This function computes the DataFrame 'df_most_eff_posts_ig'
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
            df_most_eff_posts_ig = self.df_posts_full[
                self.df_posts_full.owner_id.isin(account_ids)
            ][
                [
                    "owner_id",
                    "owner_username",
                    "shortcode",
                    "caption",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_ig = self.df_posts_full[
                self.df_posts_full.owner_username.isin(account_names)
            ][
                [
                    "owner_id",
                    "owner_username",
                    "shortcode",
                    "caption",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        else:
            df_most_eff_posts_ig = deepcopy(self.df_posts_full)[
                [
                    "owner_id",
                    "owner_username",
                    "shortcode",
                    "caption",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        try:
            df_most_eff_posts_ig["url"] = df_most_eff_posts_ig["shortcode"].apply(
                lambda x: f"instagram.com/p/{x}"
            )
            df_most_eff_posts_ig = df_most_eff_posts_ig.sort_values(
                engagement_rate, ascending=False
            ).head(n_most_eff)

            return df_most_eff_posts_ig

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=[
                    "owner_id",
                    "owner_username",
                    "shortcode",
                    "caption",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "url",
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
            PAGE_COLUMNS = ["owner_id", "owner_username"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_posts_type_ig = self.df_posts_full[
                self.df_posts_full.owner_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["typename", "caption", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_type_ig = self.df_posts_full[
                self.df_posts_full.owner_username.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["typename", "caption", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_posts_type_ig = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + ["typename", "caption", engagement_rate, "rel_" + engagement_rate]
                ]
            )

        try:
            df_most_eff_posts_type_ig = df_most_eff_posts_type_ig.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            df_most_eff_posts_type_ig["caption_count"] = 1
            df_most_eff_posts_type_ig = (
                df_most_eff_posts_type_ig[
                    PAGE_COLUMNS
                    + [
                        "typename",
                        "caption_count",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
                .groupby(PAGE_COLUMNS + ["typename"])
                .agg(
                    {
                        "caption_count": "count",
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                    }
                )
            )
            df_most_eff_posts_type_ig = df_most_eff_posts_type_ig.rename(
                columns={
                    "caption_count": "counts",
                    engagement_rate: "avg_engagement_rate",
                    "rel_" + engagement_rate: "avg_rel_engagement_rate",
                }
            )
            if PAGE_COLUMNS:
                df_most_eff_posts_type_ig["percentage"] = (
                    df_most_eff_posts_type_ig["counts"]
                    .groupby(level=0)
                    .apply(lambda c: 100.0 * c / float(c.sum()))
                    .round(2)
                )
                df_most_eff_posts_type_ig = (
                    df_most_eff_posts_type_ig.reset_index().rename(
                        columns={
                            PAGE_COLUMNS[0]: "_object_id",
                            PAGE_COLUMNS[1]: "_object_name",
                        }
                    )
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            else:
                df_most_eff_posts_type_ig["percentage"] = (
                    100.0
                    * df_most_eff_posts_type_ig["counts"]
                    / df_most_eff_posts_type_ig["counts"].sum()
                ).round(2)
                df_most_eff_posts_type_ig = df_most_eff_posts_type_ig.reset_index()

            return df_most_eff_posts_type_ig.sort_values(
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
                columns=PAGE_COLUMNS
                + [
                    "typename",
                    "counts",
                    "avg_engagement_rate",
                    "avg_rel_engagement_rate",
                    "percentage",
                ]
            )

    def construct_most_eff_objects(
        self,
        df_most_eff_objects_ig,
        objs,
        engagement_rate="engagement_rate_by_post",
        grouped=True,
        sort_column="engagement_rate_by_post",
    ):
        """
        This function computes the output DataFrame for hashtags or mentions
        with their respective count and engagement rate.

        Parameters
        ----------
        df_most_eff_objects_ig:
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
            PAGE_COLUMNS = ["owner_id", "owner_username"]

        try:
            objs_ig = []
            objs_eff_ig = []
            objs_rel_eff_ig = []
            objs_group_ig = []
            if PAGE_COLUMNS:
                objs_ids_ig = []
                objs_names_ig = []
            objs_counts_ig = []

            for _, row in df_most_eff_objects_ig.iterrows():
                objs_ig = objs_ig + row["caption_" + objs]
                objs_eff_ig = objs_eff_ig + [row[engagement_rate]] * len(
                    row["caption_" + objs]
                )
                objs_rel_eff_ig = objs_rel_eff_ig + [
                    row["rel_" + engagement_rate]
                ] * len(row["caption_" + objs])
                objs_group_ig = objs_group_ig + [row.group] * len(
                    row["caption_" + objs]
                )
                if PAGE_COLUMNS:
                    objs_ids_ig = objs_ids_ig + [row[PAGE_COLUMNS[0]]] * len(
                        row["caption_" + objs]
                    )
                    objs_names_ig = objs_names_ig + [row[PAGE_COLUMNS[1]]] * len(
                        row["caption_" + objs]
                    )
                objs_counts_ig = objs_counts_ig + [1] * len(row["caption_" + objs])

            most_eff_objs_ig = pd.DataFrame(
                {
                    objs[:-1]: objs_ig,
                    engagement_rate: objs_eff_ig,
                    "rel_" + engagement_rate: objs_rel_eff_ig,
                    "group": objs_group_ig,
                    f"{objs[:-1]}_count": objs_counts_ig,
                }
            )

            if PAGE_COLUMNS:
                most_eff_objs_ig[PAGE_COLUMNS[0]] = objs_ids_ig
                most_eff_objs_ig[PAGE_COLUMNS[1]] = objs_names_ig

            most_eff_objs_ig = (
                most_eff_objs_ig.groupby(PAGE_COLUMNS + ["group", objs[:-1]])
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

            return most_eff_objs_ig

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            most_eff_objs_ig = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    objs[:-1],
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    f"{objs[:-1]}_count",
                ]
            )

            return most_eff_objs_ig

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
          - 'most_eff_hashtags_ig' and 'most_eff_mentions_ig'
            which contains the hastags and mentions with higher associated
            engagement rate for the accounts selected.

          - 'compare_hashtags_ig' and 'compare_mentions_ig'
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
            PAGE_COLUMNS = ["owner_id", "owner_username"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_hashtags_mentions_ig = self.df_posts_full[
                self.df_posts_full.owner_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + [
                    "caption_hashtags",
                    "caption_mentions",
                    "group",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_hashtags_mentions_ig = self.df_posts_full[
                self.df_posts_full.owner_username.isin(account_names)
            ][
                PAGE_COLUMNS
                + [
                    "caption_hashtags",
                    "caption_mentions",
                    "group",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        else:
            df_most_eff_hashtags_mentions_ig = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + [
                        "caption_hashtags",
                        "caption_mentions",
                        "group",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
            )

        df_compare_hashtags_mentions_ig = self.df_posts_full[
            self.df_posts_full.group == compare_group
        ][
            PAGE_COLUMNS
            + [
                "caption_hashtags",
                "caption_mentions",
                "group",
                engagement_rate,
                "rel_" + engagement_rate,
            ]
        ]

        try:
            df_most_eff_hashtags_mentions_ig[
                "caption_hashtags"
            ] = df_most_eff_hashtags_mentions_ig["caption_hashtags"].apply(
                lambda hashtags: json.loads(hashtags)
            )
            df_most_eff_hashtags_mentions_ig[
                "caption_hashtags"
            ] = df_most_eff_hashtags_mentions_ig["caption_hashtags"].apply(
                lambda hashtags: hashtags if hashtags else None
            )

            df_most_eff_hashtags_mentions_ig[
                "caption_mentions"
            ] = df_most_eff_hashtags_mentions_ig["caption_mentions"].apply(
                lambda mentions: json.loads(mentions)
            )
            df_most_eff_hashtags_mentions_ig[
                "caption_mentions"
            ] = df_most_eff_hashtags_mentions_ig["caption_mentions"].apply(
                lambda mentions: mentions if mentions else None
            )

            df_compare_hashtags_mentions_ig[
                "caption_hashtags"
            ] = df_compare_hashtags_mentions_ig["caption_hashtags"].apply(
                lambda hashtags: json.loads(hashtags)
            )
            df_compare_hashtags_mentions_ig[
                "caption_hashtags"
            ] = df_compare_hashtags_mentions_ig["caption_hashtags"].apply(
                lambda hashtags: hashtags if hashtags else None
            )

            df_compare_hashtags_mentions_ig[
                "caption_mentions"
            ] = df_compare_hashtags_mentions_ig["caption_mentions"].apply(
                lambda mentions: json.loads(mentions)
            )
            df_compare_hashtags_mentions_ig[
                "caption_mentions"
            ] = df_compare_hashtags_mentions_ig["caption_mentions"].apply(
                lambda mentions: mentions if mentions else None
            )

            df_most_eff_hashtags_mentions_ig = (
                df_most_eff_hashtags_mentions_ig.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            df_compare_hashtags_mentions_ig = (
                df_compare_hashtags_mentions_ig.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            # Hashtags
            df_most_eff_hashtags_ig = df_most_eff_hashtags_mentions_ig[
                ~df_most_eff_hashtags_mentions_ig["caption_hashtags"].isna()
            ]
            most_eff_hashtags_ig = self.construct_most_eff_objects(
                df_most_eff_hashtags_ig, objs="hashtags", grouped=grouped
            )

            # Group to compare with
            df_compare_hashtags_ig = df_compare_hashtags_mentions_ig[
                ~df_compare_hashtags_mentions_ig["caption_hashtags"].isna()
            ]
            compare_hashtags_ig = self.construct_most_eff_objects(
                df_compare_hashtags_ig,
                objs="hashtags",
                grouped=grouped,
                sort_column="hashtag_count",
            )

            # Mentions
            df_most_eff_mentions_ig = df_most_eff_hashtags_mentions_ig[
                ~df_most_eff_hashtags_mentions_ig["caption_mentions"].isna()
            ]
            most_eff_mentions_ig = self.construct_most_eff_objects(
                df_most_eff_mentions_ig, objs="mentions", grouped=grouped
            )

            # Group to compare with
            df_compare_mentions_ig = df_compare_hashtags_mentions_ig[
                ~df_compare_hashtags_mentions_ig["caption_mentions"].isna()
            ]
            compare_mentions_ig = self.construct_most_eff_objects(
                df_compare_mentions_ig,
                objs="mentions",
                grouped=grouped,
                sort_column="mention_count",
            )

            if PAGE_COLUMNS:
                most_eff_hashtags_ig = most_eff_hashtags_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_hashtags_ig = compare_hashtags_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_mentions_ig = most_eff_mentions_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_mentions_ig = compare_mentions_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]

            return (
                most_eff_hashtags_ig,
                compare_hashtags_ig,
                most_eff_mentions_ig,
                compare_mentions_ig,
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_hashtags_ig = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "hashtag_count",
                ]
            )
            compare_hashtags_ig = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "hashtag_count",
                ]
            )
            most_eff_mentions_ig = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "mention_count",
                ]
            )
            compare_mentions_ig = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "mention_count",
                ]
            )
            return (
                most_eff_hashtags_ig,
                compare_hashtags_ig,
                most_eff_mentions_ig,
                compare_mentions_ig,
            )

    def construct_most_eff_words(
        self,
        df_most_eff_words_ig,
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
        df_most_eff_objects_ig:
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
            PAGE_COLUMNS = ["owner_id", "owner_username"]

        try:
            words_ig = []
            lemmas_ig = []
            pos_tags_ig = []
            words_counts_ig = []
            words_eff_ig = []
            words_rel_eff_ig = []
            words_group_ig = []
            if PAGE_COLUMNS:
                words_ids_ig = []
                words_names_ig = []
            for _, row in df_most_eff_words_ig.iterrows():
                words_ig = words_ig + row.words
                lemmas_ig = lemmas_ig + row.lemmas
                pos_tags_ig = pos_tags_ig + row.pos_tags
                words_counts_ig = words_counts_ig + [1] * len(row.words)
                words_eff_ig = words_eff_ig + [row[engagement_rate]] * len(row.words)
                words_rel_eff_ig = words_rel_eff_ig + [
                    row["rel_" + engagement_rate]
                ] * len(row.words)
                words_group_ig = words_group_ig + [row.group] * len(row.words)
                if PAGE_COLUMNS:
                    words_ids_ig = words_ids_ig + [row[PAGE_COLUMNS[0]]] * len(
                        row.words
                    )
                    words_names_ig = words_names_ig + [row[PAGE_COLUMNS[1]]] * len(
                        row.words
                    )

            most_eff_words_ig = pd.DataFrame(
                {
                    "word": words_ig,
                    "lemma": lemmas_ig,
                    "pos_tag": pos_tags_ig,
                    "word_count": words_counts_ig,
                    engagement_rate: words_eff_ig,
                    "rel_" + engagement_rate: words_rel_eff_ig,
                    "group": words_group_ig,
                }
            )

            if PAGE_COLUMNS:
                most_eff_words_ig[PAGE_COLUMNS[0]] = words_ids_ig
                most_eff_words_ig[PAGE_COLUMNS[1]] = words_names_ig

            if lemmatize:
                word_column = "lemma"
            else:
                word_column = "word"
            most_eff_words_ig = (
                most_eff_words_ig[
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
            most_eff_words_ig = most_eff_words_ig[
                most_eff_words_ig["word_count"] >= min_count
            ]

            most_eff_words_ig = most_eff_words_ig.sort_values(
                PAGE_COLUMNS + ["pos_tag", "group", engagement_rate], ascending=False
            ).reset_index()

            most_eff_nouns_ig = most_eff_words_ig[
                most_eff_words_ig["pos_tag"] == "NOUN"
            ]
            most_eff_verbs_ig = most_eff_words_ig[
                most_eff_words_ig["pos_tag"] == "VERB"
            ]
            most_eff_adjs_ig = most_eff_words_ig[most_eff_words_ig["pos_tag"] == "ADJ"]

            return (
                most_eff_words_ig,
                most_eff_nouns_ig,
                most_eff_verbs_ig,
                most_eff_adjs_ig,
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
            most_eff_words_ig = pd.DataFrame(
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
            most_eff_nouns_ig = pd.DataFrame(columns=show_columns)
            most_eff_verbs_ig = pd.DataFrame(columns=show_columns)
            most_eff_adjs_ig = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words_ig,
                most_eff_nouns_ig,
                most_eff_verbs_ig,
                most_eff_adjs_ig,
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
          - 'most_eff_words_ig'
            which contains the words with higher associated
            engagement rate for the accounts selected, it is tagged with
            the part of speech tag of the word.

          - most_eff_nouns_ig, most_eff_verbs_ig and most_eff_adjs_ig
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
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'.
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
            PAGE_COLUMNS = ["owner_id", "owner_username"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_words_ig = self.df_posts_full[
                self.df_posts_full.owner_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["caption", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_words_ig = self.df_posts_full[
                self.df_posts_full.owner_username.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["caption", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_words_ig = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + ["caption", "group", engagement_rate, "rel_" + engagement_rate]
                ]
            )

        try:
            df_most_eff_words_ig = df_most_eff_words_ig.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            if "processed_text" not in df_most_eff_words_ig.keys():
                df_most_eff_words_ig[
                    "processed_text"
                ] = df_most_eff_words_ig.caption.apply(
                    lambda msg: CleanText(msg).process_text(
                        mentions=True, hashtags=True, links=True, spec_chars=True
                    )
                )
            df_most_eff_words_ig["processed_text"] = df_most_eff_words_ig[
                "processed_text"
            ].apply(lambda txt: self.features.pos_tags(txt))

            df_most_eff_words_ig["words"] = df_most_eff_words_ig[
                "processed_text"
            ].apply(lambda pt: pt["words"])
            df_most_eff_words_ig["lemmas"] = df_most_eff_words_ig[
                "processed_text"
            ].apply(lambda pt: pt["lemmas"])
            df_most_eff_words_ig["pos_tags"] = df_most_eff_words_ig[
                "processed_text"
            ].apply(lambda pt: pt["pos_tags"])

            df_most_eff_words_ig = df_most_eff_words_ig[
                ~df_most_eff_words_ig["processed_text"].isna()
            ]

            (
                most_eff_words_ig,
                most_eff_nouns_ig,
                most_eff_verbs_ig,
                most_eff_adjs_ig,
            ) = self.construct_most_eff_words(
                df_most_eff_words_ig,
                lemmatize=lemmatize,
                engagement_rate=engagement_rate,
                grouped=grouped,
                min_count=min_count,
            )

            if PAGE_COLUMNS:
                most_eff_words_ig = most_eff_words_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_nouns_ig = most_eff_nouns_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_verbs_ig = most_eff_verbs_ig.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_adjs_ig = most_eff_adjs_ig.reset_index().rename(
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
                most_eff_words_ig,
                most_eff_nouns_ig[show_columns],
                most_eff_verbs_ig[show_columns],
                most_eff_adjs_ig[show_columns],
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_words_ig = pd.DataFrame(
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
            most_eff_nouns_ig = pd.DataFrame(columns=show_columns)
            most_eff_verbs_ig = pd.DataFrame(columns=show_columns)
            most_eff_adjs_ig = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words_ig,
                most_eff_nouns_ig,
                most_eff_verbs_ig,
                most_eff_adjs_ig,
            )
