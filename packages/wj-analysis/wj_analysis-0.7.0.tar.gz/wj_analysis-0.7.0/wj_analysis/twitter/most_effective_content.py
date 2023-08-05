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


def get_content_type(string):
    """
    This functions gets the content type for the corresponding str object given.

    Parameters
    ----------
    tid:
        type: str
        twitter_id to conpute the group for.
    groups:
        type: dict
        Maps the group to the twitter ids.

    Returns
    -------
    str

    """
    try:
        content_type = json.loads(string)[0]["type"]
    except Exception:
        content_type = "text"
    return content_type


class MostEffectiveContentTW:
    """
    This class computes the different atributes of the posts with
    higher engagement rate.
    """

    def __init__(self, df_tweets, groups, mode="status"):
        """
        This method computes the DataFrame 'df_posts_full'
        which contains all the information of the posts, including column
        'group'.

        Parameters
        ----------
        df_tweets:
            type: DataFrame
            Information of the posts.
            This Pandas DataFrame must have columns 'page_id',
            'page_name', 'message' and 'engagement_rate_by_post'.
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

        TWEETS_COLUMNS = [
            "twitter_id",
            "screen_name",
            "tweet_id",
            "text",
            "media_entities",
            "hashtags",
            "user_mentions",
            "group",
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post",
        ]

        OUTPUT_COLUMNS = [
            "twitter_id",
            "screen_name",
            "tweet_id",
            "text",
            "media_entities",
            "hashtags",
            "user_mentions",
            "group",
            "engagement_rate_by_post",
            "rel_engagement_rate_by_post",
        ]

        self.features = None

        if mode == "status":
            if len(df_tweets) > 0:
                try:
                    df_posts_full = deepcopy(
                        df_tweets[df_tweets["in_reply_to_status_id"].isna()][
                            TWEETS_COLUMNS
                        ]
                    )

                    df_posts_full["group"] = df_posts_full["twitter_id"].apply(
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

        elif mode == "terms":
            try:
                df_posts_full = deepcopy(df_tweets[TWEETS_COLUMNS])

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
            raise RuntimeError(
                f'Mode {mode} is not available. Modes available: "status" and "terms".'
            )

    def posts(
        self, n_most_eff=None, engagement_rate="engagement_rate_by_post", **kwargs
    ):
        """
        This function computes the DataFrame 'df_most_eff_posts_tw'
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
            df_most_eff_posts_tw = self.df_posts_full[
                self.df_posts_full.twitter_id.isin(account_ids)
            ][
                [
                    "twitter_id",
                    "screen_name",
                    "tweet_id",
                    "text",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_tw = self.df_posts_full[
                self.df_posts_full.screen_name.isin(account_names)
            ][
                [
                    "twitter_id",
                    "screen_name",
                    "tweet_id",
                    "text",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        else:
            df_most_eff_posts_tw = deepcopy(
                self.df_posts_full[
                    [
                        "twitter_id",
                        "screen_name",
                        "tweet_id",
                        "text",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
            )
        try:
            df_most_eff_posts_tw["url"] = df_most_eff_posts_tw["tweet_id"].apply(
                lambda x: f"twitter.com/user/status/{x}"
            )
            if n_most_eff:
                max_n = min(n_most_eff, len(df_most_eff_posts_tw))
            else:
                max_n = min(100, len(df_most_eff_posts_tw))

            df_most_eff_posts_tw = df_most_eff_posts_tw.sort_values(
                engagement_rate, ascending=False
            ).head(max_n)

            return df_most_eff_posts_tw

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(
                columns=[
                    "twitter_id",
                    "screen_name",
                    "tweet_id",
                    "text",
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
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_posts_type_tw = self.df_posts_full[
                self.df_posts_full.twitter_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["media_entities", "text", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_posts_type_tw = self.df_posts_full[
                self.df_posts_full.screen_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["media_entities", "text", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_posts_type_tw = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + [
                        "media_entities",
                        "text",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
            )

        try:
            df_most_eff_posts_type_tw = df_most_eff_posts_type_tw.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)
            df_most_eff_posts_type_tw["type"] = df_most_eff_posts_type_tw[
                "media_entities"
            ].apply(lambda med_ent: get_content_type(med_ent))

            df_most_eff_posts_type_tw["text_count"] = 1
            df_most_eff_posts_type_tw = (
                df_most_eff_posts_type_tw[
                    PAGE_COLUMNS
                    + ["type", "text_count", engagement_rate, "rel_" + engagement_rate]
                ]
                .groupby(PAGE_COLUMNS + ["type"])
                .agg(
                    {
                        "text_count": "count",
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                    }
                )
            )
            df_most_eff_posts_type_tw = df_most_eff_posts_type_tw.rename(
                columns={
                    "text_count": "counts",
                    engagement_rate: "avg_engagement_rate",
                    "rel_" + engagement_rate: "avg_rel_engagement_rate",
                }
            )
            if PAGE_COLUMNS:
                df_most_eff_posts_type_tw["percentage"] = (
                    df_most_eff_posts_type_tw["counts"]
                    .groupby(level=0)
                    .apply(lambda c: 100.0 * c / float(c.sum()))
                    .round(2)
                )
                df_most_eff_posts_type_tw = (
                    df_most_eff_posts_type_tw.reset_index().rename(
                        columns={
                            PAGE_COLUMNS[0]: "_object_id",
                            PAGE_COLUMNS[1]: "_object_name",
                        }
                    )
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            else:
                df_most_eff_posts_type_tw["percentage"] = (
                    100.0
                    * df_most_eff_posts_type_tw["counts"]
                    / df_most_eff_posts_type_tw["counts"].sum()
                ).round(2)
                df_most_eff_posts_type_tw = df_most_eff_posts_type_tw.reset_index()

            return df_most_eff_posts_type_tw.sort_values(
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
        df_most_eff_objects_tw,
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
        df_most_eff_objects_tw:
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
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        try:
            objs_tw = []
            objs_eff_tw = []
            objs_rel_eff_tw = []
            objs_group_tw = []
            if PAGE_COLUMNS:
                objs_ids_tw = []
                objs_names_tw = []
            objs_counts_tw = []

            for _, row in df_most_eff_objects_tw.iterrows():
                objs_tw = objs_tw + row[objs]
                objs_eff_tw = objs_eff_tw + [row[engagement_rate]] * len(row[objs])
                objs_rel_eff_tw = objs_rel_eff_tw + [
                    row["rel_" + engagement_rate]
                ] * len(row[objs])
                objs_group_tw = objs_group_tw + [row.group] * len(row[objs])
                if PAGE_COLUMNS:
                    objs_ids_tw = objs_ids_tw + [row[PAGE_COLUMNS[0]]] * len(row[objs])
                    objs_names_tw = objs_names_tw + [row[PAGE_COLUMNS[1]]] * len(
                        row[objs]
                    )
                objs_counts_tw = objs_counts_tw + [1] * len(row[objs])

            objs = objs[:-1].split("_")[-1]

            most_eff_objs_tw = pd.DataFrame(
                {
                    objs: objs_tw,
                    engagement_rate: objs_eff_tw,
                    "rel_" + engagement_rate: objs_rel_eff_tw,
                    "group": objs_group_tw,
                    f"{objs}_count": objs_counts_tw,
                }
            )

            if PAGE_COLUMNS:
                most_eff_objs_tw[PAGE_COLUMNS[0]] = objs_ids_tw
                most_eff_objs_tw[PAGE_COLUMNS[1]] = objs_names_tw

            most_eff_objs_tw = (
                most_eff_objs_tw.groupby(PAGE_COLUMNS + ["group", objs])
                .agg(
                    {
                        engagement_rate: "mean",
                        "rel_" + engagement_rate: "mean",
                        f"{objs}_count": "sum",
                    }
                )
                .sort_values(PAGE_COLUMNS + [sort_column], ascending=False)
                .reset_index()
            )

            return most_eff_objs_tw

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            most_eff_objs_tw = pd.DataFrame(
                columns=PAGE_COLUMNS
                + [
                    objs,
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    f"{objs}_count",
                ]
            )

            return most_eff_objs_tw

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
          - 'most_eff_hashtags_tw' and 'most_eff_mentions_tw'
            which contains the hastags and mentions with higher associated
            engagement rate for the accounts selected.

          - 'compare_hashtags_tw' and 'compare_mentions_tw'
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
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_hashtags_mentions_tw = self.df_posts_full[
                self.df_posts_full.twitter_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + [
                    "hashtags",
                    "user_mentions",
                    "group",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_hashtags_mentions_tw = self.df_posts_full[
                self.df_posts_full.screen_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + [
                    "hashtags",
                    "user_mentions",
                    "group",
                    engagement_rate,
                    "rel_" + engagement_rate,
                ]
            ]
        else:
            df_most_eff_hashtags_mentions_tw = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + [
                        "hashtags",
                        "user_mentions",
                        "group",
                        engagement_rate,
                        "rel_" + engagement_rate,
                    ]
                ]
            )

        df_compare_hashtags_mentions_tw = self.df_posts_full[
            self.df_posts_full.group == compare_group
        ][
            PAGE_COLUMNS
            + [
                "hashtags",
                "user_mentions",
                "group",
                engagement_rate,
                "rel_" + engagement_rate,
            ]
        ]

        try:
            df_most_eff_hashtags_mentions_tw[
                "hashtags"
            ] = df_most_eff_hashtags_mentions_tw["hashtags"].apply(
                lambda hashtags: hashtags.split(",") if hashtags else None
            )
            df_most_eff_hashtags_mentions_tw[
                "user_mentions"
            ] = df_most_eff_hashtags_mentions_tw["user_mentions"].apply(
                lambda mentions: mentions.split(",") if mentions else None
            )
            df_compare_hashtags_mentions_tw[
                "hashtags"
            ] = df_compare_hashtags_mentions_tw["hashtags"].apply(
                lambda hashtags: hashtags.split(",") if hashtags else None
            )
            df_compare_hashtags_mentions_tw[
                "user_mentions"
            ] = df_compare_hashtags_mentions_tw["user_mentions"].apply(
                lambda mentions: mentions.split(",") if mentions else None
            )

            df_most_eff_hashtags_mentions_tw = (
                df_most_eff_hashtags_mentions_tw.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            df_compare_hashtags_mentions_tw = (
                df_compare_hashtags_mentions_tw.sort_values(
                    engagement_rate, ascending=False
                ).head(from_n_most_eff)
            )
            # Hashtags
            df_most_eff_hashtags_tw = df_most_eff_hashtags_mentions_tw[
                ~df_most_eff_hashtags_mentions_tw["hashtags"].isna()
            ]
            most_eff_hashtags_tw = self.construct_most_eff_objects(
                df_most_eff_hashtags_tw, objs="hashtags", grouped=grouped
            )

            # Group to compare with
            df_compare_hashtags_tw = df_compare_hashtags_mentions_tw[
                ~df_compare_hashtags_mentions_tw["hashtags"].isna()
            ]
            compare_hashtags_tw = self.construct_most_eff_objects(
                df_compare_hashtags_tw,
                objs="hashtags",
                grouped=grouped,
                sort_column="hashtag_count",
            )

            # Mentions
            df_most_eff_mentions_tw = df_most_eff_hashtags_mentions_tw[
                ~df_most_eff_hashtags_mentions_tw["user_mentions"].isna()
            ]
            most_eff_mentions_tw = self.construct_most_eff_objects(
                df_most_eff_mentions_tw, objs="user_mentions", grouped=grouped
            )

            # Group to compare with
            df_compare_mentions_tw = df_compare_hashtags_mentions_tw[
                ~df_compare_hashtags_mentions_tw["user_mentions"].isna()
            ]
            compare_mentions_tw = self.construct_most_eff_objects(
                df_compare_mentions_tw,
                objs="user_mentions",
                grouped=grouped,
                sort_column="mention_count",
            )

            if PAGE_COLUMNS:
                most_eff_hashtags_tw = most_eff_hashtags_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_hashtags_tw = compare_hashtags_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_mentions_tw = most_eff_mentions_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                compare_mentions_tw = compare_mentions_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                PAGE_COLUMNS = ["_object_id", "_object_name"]

            return (
                most_eff_hashtags_tw,
                compare_hashtags_tw,
                most_eff_mentions_tw,
                compare_mentions_tw,
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_hashtags_tw = pd.DataFrame(
                columns=[
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "hashtag_count",
                ]
            )
            compare_hashtags_tw = pd.DataFrame(
                columns=[
                    "hashtag",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "hashtag_count",
                ]
            )
            most_eff_mentions_tw = pd.DataFrame(
                columns=[
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "mention_count",
                ]
            )
            compare_mentions_tw = pd.DataFrame(
                columns=[
                    "mention",
                    engagement_rate,
                    "rel_" + engagement_rate,
                    "group",
                    "mention_count",
                ]
            )
            return (
                most_eff_hashtags_tw,
                compare_hashtags_tw,
                most_eff_mentions_tw,
                compare_mentions_tw,
            )

    def construct_most_eff_words(
        self,
        df_most_eff_words_tw,
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
        df_most_eff_objects_tw:
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
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        try:
            words_tw = []
            lemmas_tw = []
            pos_tags_tw = []
            words_counts_tw = []
            words_eff_tw = []
            words_rel_eff_tw = []
            words_group_tw = []
            if PAGE_COLUMNS:
                words_ids_tw = []
                words_names_tw = []
            for _, row in df_most_eff_words_tw.iterrows():
                words_tw = words_tw + row.words
                lemmas_tw = lemmas_tw + row.lemmas
                pos_tags_tw = pos_tags_tw + row.pos_tags
                words_counts_tw = words_counts_tw + [1] * len(row.words)
                words_eff_tw = words_eff_tw + [row[engagement_rate]] * len(row.words)
                words_rel_eff_tw = words_rel_eff_tw + [
                    row["rel_" + engagement_rate]
                ] * len(row.words)
                words_group_tw = words_group_tw + [row.group] * len(row.words)
                if PAGE_COLUMNS:
                    words_ids_tw = words_ids_tw + [row[PAGE_COLUMNS[0]]] * len(
                        row.words
                    )
                    words_names_tw = words_names_tw + [row[PAGE_COLUMNS[1]]] * len(
                        row.words
                    )

            most_eff_words_tw = pd.DataFrame(
                {
                    "word": words_tw,
                    "lemma": lemmas_tw,
                    "pos_tag": pos_tags_tw,
                    "word_count": words_counts_tw,
                    engagement_rate: words_eff_tw,
                    "rel_" + engagement_rate: words_rel_eff_tw,
                    "group": words_group_tw,
                }
            )

            if PAGE_COLUMNS:
                most_eff_words_tw[PAGE_COLUMNS[0]] = words_ids_tw
                most_eff_words_tw[PAGE_COLUMNS[1]] = words_names_tw

            if lemmatize:
                word_column = "lemma"
            else:
                word_column = "word"
            most_eff_words_tw = (
                most_eff_words_tw[
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
            most_eff_words_tw = most_eff_words_tw[
                most_eff_words_tw["word_count"] >= min_count
            ]

            most_eff_words_tw = most_eff_words_tw.sort_values(
                PAGE_COLUMNS + ["pos_tag", "group", engagement_rate], ascending=False
            ).reset_index()

            most_eff_nouns_tw = most_eff_words_tw[
                most_eff_words_tw["pos_tag"] == "NOUN"
            ]
            most_eff_verbs_tw = most_eff_words_tw[
                most_eff_words_tw["pos_tag"] == "VERB"
            ]
            most_eff_adjs_tw = most_eff_words_tw[most_eff_words_tw["pos_tag"] == "ADJ"]

            return (
                most_eff_words_tw,
                most_eff_nouns_tw,
                most_eff_verbs_tw,
                most_eff_adjs_tw,
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
            most_eff_words_tw = pd.DataFrame(
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
            most_eff_nouns_tw = pd.DataFrame(columns=show_columns)
            most_eff_verbs_tw = pd.DataFrame(columns=show_columns)
            most_eff_adjs_tw = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words_tw,
                most_eff_nouns_tw,
                most_eff_verbs_tw,
                most_eff_adjs_tw,
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
          - 'most_eff_words_tw'
            which contains the words with higher associated
            engagement rate for the accounts selected, it is tagged with
            the part of speech tag of the word.

          - most_eff_nouns_tw, most_eff_verbs_tw and most_eff_adjs_tw
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
            PAGE_COLUMNS = ["twitter_id", "screen_name"]

        if "account_ids" in kwargs.keys() and kwargs["account_ids"]:
            account_ids = kwargs["account_ids"]
            df_most_eff_words_tw = self.df_posts_full[
                self.df_posts_full.twitter_id.isin(account_ids)
            ][
                PAGE_COLUMNS
                + ["text", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        elif "account_names" in kwargs.keys() and kwargs["account_names"]:
            account_names = kwargs["account_names"]
            df_most_eff_words_tw = self.df_posts_full[
                self.df_posts_full.screen_name.isin(account_names)
            ][
                PAGE_COLUMNS
                + ["text", "group", engagement_rate, "rel_" + engagement_rate]
            ]
        else:
            df_most_eff_words_tw = deepcopy(
                self.df_posts_full[
                    PAGE_COLUMNS
                    + ["text", "group", engagement_rate, "rel_" + engagement_rate]
                ]
            )

        try:
            df_most_eff_words_tw = df_most_eff_words_tw.sort_values(
                engagement_rate, ascending=False
            ).head(from_n_most_eff)

            if "processed_text" not in df_most_eff_words_tw.keys():
                df_most_eff_words_tw[
                    "processed_text"
                ] = df_most_eff_words_tw.text.apply(
                    lambda msg: CleanText(msg).process_text(
                        mentions=True,
                        hashtags=True,
                        links=True,
                        spec_chars=True,
                        rts=True,
                    )
                )
            df_most_eff_words_tw["processed_text"] = df_most_eff_words_tw[
                "processed_text"
            ].apply(lambda txt: self.features.pos_tags(txt))

            df_most_eff_words_tw["words"] = df_most_eff_words_tw[
                "processed_text"
            ].apply(lambda pt: pt["words"])
            df_most_eff_words_tw["lemmas"] = df_most_eff_words_tw[
                "processed_text"
            ].apply(lambda pt: pt["lemmas"])
            df_most_eff_words_tw["pos_tags"] = df_most_eff_words_tw[
                "processed_text"
            ].apply(lambda pt: pt["pos_tags"])

            df_most_eff_words_tw = df_most_eff_words_tw[
                ~df_most_eff_words_tw["processed_text"].isna()
            ]

            (
                most_eff_words_tw,
                most_eff_nouns_tw,
                most_eff_verbs_tw,
                most_eff_adjs_tw,
            ) = self.construct_most_eff_words(
                df_most_eff_words_tw,
                lemmatize=lemmatize,
                engagement_rate=engagement_rate,
                grouped=grouped,
                min_count=min_count,
            )

            if PAGE_COLUMNS:
                most_eff_words_tw = most_eff_words_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_nouns_tw = most_eff_nouns_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_verbs_tw = most_eff_verbs_tw.rename(
                    columns={
                        PAGE_COLUMNS[0]: "_object_id",
                        PAGE_COLUMNS[1]: "_object_name",
                    }
                )
                most_eff_adjs_tw = most_eff_adjs_tw.rename(
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
                most_eff_words_tw,
                most_eff_nouns_tw[show_columns],
                most_eff_verbs_tw[show_columns],
                most_eff_adjs_tw[show_columns],
            )

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            if PAGE_COLUMNS:
                PAGE_COLUMNS = ["_object_id", "_object_name"]
            most_eff_words_tw = pd.DataFrame(
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
            most_eff_nouns_tw = pd.DataFrame(columns=show_columns)
            most_eff_verbs_tw = pd.DataFrame(columns=show_columns)
            most_eff_adjs_tw = pd.DataFrame(columns=show_columns)
            return (
                most_eff_words_tw,
                most_eff_nouns_tw,
                most_eff_verbs_tw,
                most_eff_adjs_tw,
            )
