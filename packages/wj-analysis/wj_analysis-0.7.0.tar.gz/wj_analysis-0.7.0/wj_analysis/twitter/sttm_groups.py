import sys
from collections import Counter
from copy import deepcopy
from datetime import timedelta

import pandas as pd
from numpy import unique

from ..common import general_utils
from ..common.nlp_utils import STTM, CleanText, Features, Polarity

ERR_SYS = "\nSystem error: "


class STTMgroupsTW:
    """
    This class groups texts into groups of similar topics.
    """

    def __init__(self, df_replies, account_ids=[], account_names=[]):
        """
        This method computes the DataFrame 'df_replies_full'
        which contains all the information of the twitter replies, including column 'group' and 'polarity'.

        Parameters
        ----------
        df_replies:
            type: DataFrame
            Information of the tweets or the twitter replies.
            This Pandas DataFrame must have columns 'text', 'twitter_id', 'screen_name',  and 'replying_to_id' and 'replying_to' if the data frame contains tweet replies.
        account_ids=[]:
            type: list
            list of accounts ids in case filtering by account id is needed.
        account_names=[]:
            type: list
            list of accounts names in case filtering by account name is needed.
        """
        METHOD_NAME = "__init__"
        df_replies_full = deepcopy(df_replies)
        self.df_replies_full = df_replies_full

        try:
            if "replying_to" in self.df_replies_full.keys():
                self.df_replies_full["name"] = self.df_replies_full["replying_to"]

            else:
                self.df_replies_full["name"] = self.df_replies_full["screen_name"]
            self.df_replies_full["all"] = "all groups"

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            print(
                "Warning: Class: {self.__str__()}\nMethod: {METHOD_NAME}' no 'replying_to' or 'screen_name' column in DataFrame"
            )
            if "name" not in self.df_replies_full.keys():
                self.df_replies_full["name"] = "no name"

        if account_ids:
            self.df_replies_full = self.df_replies_full[
                self.df_replies_full.replying_to_id.isin(account_ids)
            ]
        elif account_names:
            self.df_replies_full = self.df_replies_full[
                self.df_replies_full.name.isin(account_names)
            ]

        try:
            if df_replies.empty:
                print("Warning: input data DataFrame is empty.")
        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_replies_full = pd.DataFrame(columns=[""])

    def remove_from_text(self, text, toremove):
        """
        removes words from text.

        Parameters
        ----------
        text
            type: list of strings
            text of the post or comment.

        toremove:
            type: list of strings
            list of words to remove from text.

        Returns
        -------
        list of strings
        """
        text_copy = deepcopy(text)
        for word in text:
            if word in toremove:
                text_copy.remove(word)
        return text_copy

    def get_sttm_groups(self, with_remove=False, list_remove=[], min_texts=100):
        """
        Uses Short Text Topic Modelling to group the texts.
        Returns the input DataFrame with an additional column (sttm_group) with the group number to which each text was assigned.

        Parameters
        ----------
        with_remove (optional, default False)
            type: boolean
            set to True if user wants to remove a list of words from the texts before grouping.

        list_remove
            type: list
            list of words that the user wants to remove

        min_texts
            type: int
            minimum number of texts in the DataFrame (after cleaning and dropping empty texts) that is required to proceed with the sttm analysis.

        Returns
        -------
        DataFrame with an additional column (sttm_groups)
        """

        METHOD_NAME = "get_sttm_groups"

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

            # drop empty replies
            self.df_replies_full = self.df_replies_full.dropna(
                subset=["processed_text"]
            )
            self.df_replies_full = self.df_replies_full.drop(
                self.df_replies_full[self.df_replies_full["processed_text"] == ""].index
            )

            if list_remove:
                self.df_replies_full["processed_text"] = self.df_replies_full[
                    "processed_text"
                ].apply(lambda x: str(x).split(" "))
                self.df_replies_full["processed_text"] = self.df_replies_full[
                    "processed_text"
                ].apply(lambda x: self.remove_from_text(x, list_remove))
                self.df_replies_full["processed_text"] = self.df_replies_full[
                    "processed_text"
                ].apply(lambda msg: str(msg))

            # getting the polarity of the clean text
            if "polarity" not in self.df_replies_full.keys():
                self.df_replies_full = Polarity().polarity(df_text=self.df_replies_full)

            # tokenized text:
            if "tokenized_text" not in self.df_replies_full.keys():
                getfeatures = Features()
                self.df_replies_full[
                    "tokenized_text"
                ] = self.df_replies_full.processed_text.apply(
                    lambda msg: getfeatures.pos_tags(msg)["words"]
                )

            # drop empty comments
            self.df_replies_full = self.df_replies_full.dropna(
                subset=["tokenized_text"]
            )
            self.df_replies_full = self.df_replies_full.drop(
                self.df_replies_full[self.df_replies_full["tokenized_text"] == ""].index
            )
            self.df_replies_full[
                "len_text"
            ] = self.df_replies_full.tokenized_text.apply(lambda msg: len(msg))
            self.df_replies_full = self.df_replies_full[
                self.df_replies_full["len_text"] != 0
            ]

            # getting sttm groups
            if self.df_replies_full.tokenized_text.shape[0] > min_texts:
                self.df_replies_full = STTM(self.df_replies_full).sttm_model()
            else:
                print(
                    "warning: in",
                    f"Class: {self.__str__()}\nMethod: {METHOD_NAME}",
                    "not enough texts in DataFrame for STTM grouping. Returning value 1 for group column for sttm_group",
                )
                self.df_replies_full["sttm_group"] = 1

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            if "polarity" not in self.df_replies_full.keys():
                self.df_replies_full["polarity"] = ""
            if "sttm_group" not in self.df_replies_full.keys():
                self.df_replies_full["sttm_group"] = ""

    def get_sttm_groups_withremove(
        self, df_preprocessed_sttm, list_toremove=[], min_texts=100
    ):
        """
        Uses Short Text Topic Modelling to group the texts.
        Returns the input DataFrame with an additional column (sttm_group) with the group number to which each text was assigned.

        Parameters
        ----------
        df_preprocessed_sttm
            type: DataFrame
            Preprocessed DataFrame so that the grouping can be redone without redoing the tokenizing of the text..

        list_toremove
            type: list
            list of words that the user wants to remove.

        min_texts
            type: int
            minimum number of texts in the DataFrame (after cleaning and dropping empty texts) that is required to proceed with the sttm analysis.

        Returns
        -------
        DataFrame with column (sttm_groups)
        """

        METHOD_NAME = "get_sttm_groups_withremove"
        self.df_preprocessed_sttm = deepcopy(df_preprocessed_sttm)

        try:
            self.df_preprocessed_sttm["tokenized_text"] = self.df_preprocessed_sttm[
                "tokenized_text"
            ].apply(lambda x: x[2:-2])
            self.df_preprocessed_sttm["tokenized_text"] = self.df_preprocessed_sttm[
                "tokenized_text"
            ].apply(lambda x: str(x).split("', '"))

            self.df_preprocessed_sttm["tokenized_text"] = self.df_preprocessed_sttm[
                "tokenized_text"
            ].apply(lambda x: self.remove_from_text(x, list_toremove))

            # drop empty comments
            self.df_preprocessed_sttm = self.df_preprocessed_sttm.dropna(
                subset=["tokenized_text"]
            )
            self.df_preprocessed_sttm = self.df_preprocessed_sttm.drop(
                self.df_preprocessed_sttm[
                    self.df_preprocessed_sttm["tokenized_text"] == ""
                ].index
            )
            self.df_preprocessed_sttm = self.df_preprocessed_sttm.drop(
                self.df_preprocessed_sttm[
                    self.df_preprocessed_sttm["tokenized_text"] == " "
                ].index
            )
            self.df_preprocessed_sttm[
                "len_text"
            ] = self.df_preprocessed_sttm.tokenized_text.apply(lambda msg: len(msg))
            self.df_preprocessed_sttm = self.df_preprocessed_sttm[
                self.df_preprocessed_sttm["len_text"] != 0
            ]

            # getting sttm groups
            if self.df_preprocessed_sttm.tokenized_text.shape[0] > min_texts:
                self.df_preprocessed_sttm = STTM(self.df_preprocessed_sttm).sttm_model()
            else:
                print(
                    "warning: in",
                    f"Class: {self.__str__()}\nMethod: {METHOD_NAME}",
                    "\n Not enough texts in DataFrame for STTM grouping. Returning value 1 for group column for sttm_group",
                )
                self.df_preprocessed_sttm["sttm_group"] = 1

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")
            self.df_preprocessed_sttm["sttm_group"] = ""

    def counter_of_words(self, words, mention, n_words=10):
        """
        Counts the elements in the list 'words' and returns
        the 'n_words' most frequent.

        Parameters
        ----------
        words
            type: list
            List of words to count.
        mention:
            type: str
            Mention to delete from the counter to avoid overcounting
            mentions in responses to a certain account.
        n_words:
            type: int
            Number of most frequent words to return

        Returns
        -------
        dict
        """

        counter = Counter(words)
        try:
            del counter["@" + mention.lower()]
        except Exception:
            pass
        return dict(counter.most_common(n_words))

    def get_percentage(self, counter):
        """
        Computes the frequency (percentage) of the elements in the
        dictionary 'counter'.

        Parameters
        ----------
        counter
            type: dict
            Dictionary of elements to count.

        Returns
        -------
        dict
        """

        percentage = Counter(counter)
        percentage = dict(
            [
                (i, perc / sum(percentage.values()) * 100.0)
                for i, perc in percentage.most_common()
            ]
        )
        return percentage

    def message_to_group_columns(self):
        """
        This function constructs the columns to group the dataframe
        'data' for audiencies visualizations.

        Returns
        -------
        DataFrame
        """

        data_texts = deepcopy(self.df_replies_full)

        if "__date_cot" not in data_texts.keys():
            data_texts["__date_cot"] = pd.to_datetime(
                data_texts["created_at"]
            ) - timedelta(hours=5)

        if "replying_to" in data_texts.keys():
            data_texts = data_texts[
                [
                    "sttm_group",
                    "tokenized_text",
                    "replying_to",
                    "__date_cot",
                    "polarity",
                ]
            ]
            data_texts = data_texts.rename(columns={"replying_to": "__mention"})
        else:
            data_texts = data_texts[
                ["sttm_group", "tokenized_text", "__date_cot", "polarity"]
            ]
            data_texts["__mention"] = ""

        self.data_texts = data_texts

    def remove_insignificant_groups(
        self,
        df_sttm_groups,
        min_num_docs=15,
        min_group_percent=10,
        max_num_groups=5,
        min_num_groups=2,
    ):

        """
        this function removes the groups that have very little relevance due to the small number of elements (comments) or the small percentage that they represent.

        Parameters
        ----------
        df_sttm_groups:
            type: DataFrame
            DataFrame containing the comments and the group they belong to.

        min_num_docs:
            type:int
            minimum number of comments that a group has to have in order to be show in the platform.

        min_group_percent:
            type: float
            percentage threshold that a group has to represent in order to be show in the platform.

        max_num_groups:
            type:int
            maximun number of groups shown by the platform.

        min_num_groups:
            type:int
            minimum number of groups shown by the platform.

        Returns
        -------
        DataFrame with only the groups that comply with the criteria.
        """
        METHOD_NAME = "remove_insignificant_groups"
        if min_num_groups > max_num_groups:
            min_num_groups = max_num_groups

        if df_sttm_groups.shape[0] < min_num_groups:
            min_num_groups = df_sttm_groups.shape[0]
            max_num_groups = df_sttm_groups.shape[0]

        try:
            if (
                df_sttm_groups["__n_docs"][min_num_groups - 1] <= min_num_docs
                or df_sttm_groups["__percentage"][min_num_groups - 1]
                <= min_group_percent
            ):
                df_sttm_groups = df_sttm_groups.head(min_num_groups)

            else:
                df_sttm_groups = df_sttm_groups[
                    df_sttm_groups["__n_docs"] >= min_num_docs
                ]

                df_sttm_groups = df_sttm_groups[
                    df_sttm_groups["__percentage"] >= min_group_percent
                ]

                df_sttm_groups = df_sttm_groups.head(max_num_groups)

        except Exception as e:
            print(e)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}")

        return df_sttm_groups

    def get_examples_from_sttm_groups(
        self,
        df_data_grouped,
        group,
        num_examples=3,
        num_top_words_group=5,
        min_text_lenght=1,
    ):
        """
        this function returns examples of comments in each sttm group.

        Parameters
        ----------

        df_data_grouped:
            type: pandas DataFrame
            max number ofDataFrame with grouped information for each sttm group.

        group:
            type:int
            group number.

        num_examples: (optional, default=3)
            type:int
            number of examples selected for each sttm group.

        num_top_words_group: (optional, default=5)
            type:int
            number of most frequent words for each group that will be used as a selection crtiteria to decide wether or not a comment will be used as an example comment for the group.

        min_text_lenght: (optional, default=1)
            type:int
            minimum number of tokens in the selected comment examples.

        Returns
        -------
        a list of IDs of the selected example comments
        """

        df_replies = deepcopy(self.df_replies_full)
        post_examples_id = []

        group_word_list = [
            *df_data_grouped[df_data_grouped["sttm_group"] == group]["__words"].iloc[0]
        ]
        num_top_words_group = min(num_top_words_group, len(group_word_list))

        num_examples = min(
            num_examples, df_replies[df_replies["sttm_group"] == group].shape[0]
        )
        group_word_list = group_word_list[:num_top_words_group]

        df_replies["len_comments"] = df_replies.tokenized_text.apply(lambda x: len(x))
        df_replies["word_in_comment"] = df_replies.tokenized_text.apply(
            lambda x: True if (set(x) & set(group_word_list)) else False
        )
        df_sample = df_replies.where(
            (df_replies["len_comments"] >= min_text_lenght)
            & (df_replies["word_in_comment"] == True)
        )
        df_sample = df_sample.dropna(subset=["len_comments", "word_in_comment"])
        if df_sample.shape[0] > num_examples:
            post_examples_id = df_sample.twitter_id.sample(num_examples).values.tolist()
        else:
            post_examples_id = df_sample.comment_id.values.tolist()
        return post_examples_id

    def get_grouped_dataframe(self):
        """
        Groups the DataFrame 'data' into a DataFrame containing information
        abput the groups of texts.

        Parameters
        ----------
        data
            type: DataFrame
            DataFrame containing information about the texts.

        Returns
        -------
        DataFrame
        """
        data_grouped = deepcopy(
            self.data_texts[
                ["sttm_group", "tokenized_text", "__mention", "__date_cot", "polarity"]
            ]
        )

        data_grouped["polarity"] = data_grouped["polarity"].apply(lambda pol: str(pol))

        data_grouped["__weekday"] = data_grouped["__date_cot"].apply(
            lambda d: d.strftime("%A")
        )

        data_grouped["__n_docs"] = 1

        data_grouped = (
            data_grouped[
                [
                    "sttm_group",
                    "__n_docs",
                    "tokenized_text",
                    "__mention",
                    "__weekday",
                    "polarity",
                ]
            ]
            .groupby("sttm_group")
            .agg(
                {
                    "__n_docs": "count",
                    "tokenized_text": "sum",
                    "__mention": "last",
                    "__weekday": lambda x: ",".join(x)
                    if len(unique(data_grouped["__weekday"])) > 1
                    else "",
                    "polarity": lambda x: ",".join(x),
                }
            )
        )

        data_grouped["__percentage"] = (
            data_grouped["__n_docs"] * 100 / sum(data_grouped["__n_docs"])
        )

        data_grouped = data_grouped.rename(columns={"tokenized_text": "__words"})

        data_grouped["__words"] = data_grouped.apply(
            lambda row: self.counter_of_words(row["__words"], row["__mention"]), axis=1
        )

        data_grouped = data_grouped.reset_index().sort_values(
            "__percentage", ascending=False
        )
        data_grouped = self.remove_insignificant_groups(data_grouped)

        data_grouped = data_grouped.drop(columns=["__mention"])

        data_grouped["__weekday"] = data_grouped["__weekday"].apply(
            lambda wd: wd.split(",")
        )
        data_grouped = data_grouped.rename(columns={"__weekday": "__presence"})
        data_grouped["__presence"] = data_grouped["__presence"].apply(
            lambda p: self.get_percentage(p)
        )

        data_grouped["polarity"] = data_grouped["polarity"].apply(
            lambda wd: wd.split(",")
        )
        data_grouped = data_grouped.rename(
            columns={"polarity": "__polarity_distribution"}
        )
        data_grouped["__polarity_distribution"] = data_grouped[
            "__polarity_distribution"
        ].apply(lambda p: self.get_percentage(p))

        data_grouped["__examples_comments"] = data_grouped.sttm_group.apply(
            lambda g: self.get_examples_from_sttm_groups(
                data_grouped, g, num_examples=3
            )
        )

        # reorganize and rename sttm groups
        data_grouped = data_grouped.reset_index()
        data_grouped["sttm_group"] = data_grouped.index
        data_grouped["sttm_group"] = data_grouped["sttm_group"].apply(lambda i: i + 1)
        data_grouped = data_grouped.drop(columns="index")
        self.data_grouped = data_grouped

        return data_grouped
