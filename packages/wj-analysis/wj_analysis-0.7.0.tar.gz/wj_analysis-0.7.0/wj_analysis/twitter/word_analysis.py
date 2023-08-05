import sys
from collections import Counter
from copy import deepcopy

import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.es.stop_words import STOP_WORDS

from ..common.nlp_utils import CleanText

ERR_SYS = "\nSystem error: "


class WordAnalysis:
    # @profile
    def evaluate(self, df_sentiment, df_replies, threshold=10, group=False, top=10):
        """
        This method evaluates the term frequency and the TF-IDF of a set of post'.

        Parameters
        ----------
        df_sentiment:
            type: DataFrame
            Information of comments by sentiment
        df_replies:
            type: DataFrame
            Information of the tweets or the twitter replies.
            This Pandas DataFrame must have columns 'text', 'twitter_id', 'screen_name',  and 'replying_to_id' and 'replying_to' if the data frame contains tweet replies.
        threshold:
            type: int
            Minimum number of comments to be able to evaluate frequency and TF-IDF.
        group:
            type: bool
            Defines if is grouped by "group" or "brand".
        top:
            type: int
            Defines the number of words return in each dictionary.
        """
        METHOD_NAME = "evaluate"

        REPLIES_COLUMNS = ["text", "in_reply_to_status_id"]

        if group:
            var_analysis = ["group"]
        else:
            var_analysis = ["_object_id", "_object_name"]

        OUTPUT_COLUMNS = [
            "negative_frequency",
            "neutral_frequency",
            "positive_frequency",
            "negative_tfidf",
            "neutral_tfidf",
            "positive_tfidf",
        ]
        OUTPUT_COLUMNS.extend(var_analysis)

        if len(df_sentiment) > 0 and len(df_replies) > 0:
            try:
                self.df_getpolarity = deepcopy(df_replies[REPLIES_COLUMNS])
                self.df_getpolarity = self.df_getpolarity.rename(
                    columns={
                        "in_reply_to_status_id": "post_id",
                        "text": "message",
                    }
                )
                self.df_getpolarity = pd.merge(
                    self.df_getpolarity, df_sentiment, how="left", on="post_id"
                )
                self.df_getpolarity = self.df_getpolarity.dropna(
                    subset=["sentiment"]
                ).reset_index(drop=True)
                self.df_getpolarity[
                    "negative_count"
                ] = self.df_getpolarity.sentiment.apply(
                    lambda polarity: polarity.get(-1.0, 0.0) + polarity.get(-0.5, 0.0)
                )
                self.df_getpolarity[
                    "neutral_count"
                ] = self.df_getpolarity.sentiment.apply(
                    lambda polarity: polarity.get(0.0, 0.0)
                )
                self.df_getpolarity[
                    "positive_count"
                ] = self.df_getpolarity.sentiment.apply(
                    lambda polarity: polarity.get(1.0, 0.0) + polarity.get(0.5, 0.0)
                )
                if "processed_text" not in self.df_getpolarity.keys():
                    self.df_getpolarity["processed_text"] = self.df_getpolarity[
                        "message"
                    ].apply(
                        lambda msg: CleanText(msg).process_text(
                            mentions=True, hashtags=True, links=True, spec_chars=True
                        )
                    )
                    self.df_getpolarity["processed_text"] = self.df_getpolarity[
                        "processed_text"
                    ].apply(
                        lambda msg: " ".join(
                            [
                                word
                                for word in str(msg).split(" ")
                                if word not in STOP_WORDS
                            ]
                        )
                    )
                self.df_getpolarity = self.df_getpolarity.dropna(
                    subset=["processed_text"]
                )
                self.df_getpolarity = self.df_getpolarity.drop(
                    self.df_getpolarity[
                        self.df_getpolarity["processed_text"] == ""
                    ].index
                )
                self.df_output = pd.DataFrame(columns=OUTPUT_COLUMNS)
                item_list = self.df_getpolarity[var_analysis[0]].drop_duplicates()
                for item in item_list:
                    df_tfidf = self.df_getpolarity[
                        self.df_getpolarity[var_analysis[0]] == item
                    ]
                    temp = [
                        self.frequency(
                            df_tfidf[df_tfidf["negative_count"] >= threshold], top
                        ),
                        self.frequency(
                            df_tfidf[df_tfidf["neutral_count"] >= threshold], top
                        ),
                        self.frequency(
                            df_tfidf[df_tfidf["positive_count"] >= threshold], top
                        ),
                        self.tfidf(
                            df_tfidf[df_tfidf["negative_count"] >= threshold], top
                        ),
                        self.tfidf(
                            df_tfidf[df_tfidf["neutral_count"] >= threshold], top
                        ),
                        self.tfidf(
                            df_tfidf[df_tfidf["positive_count"] >= threshold], top
                        ),
                        item,
                    ]
                    if not group:
                        temp.extend([df_tfidf[var_analysis[1]].iloc[0]])
                    self.df_output.loc[len(self.df_output)] = temp
            except Exception as e:
                exception_type = sys.exc_info()[0]
                print(ERR_SYS + str(exception_type))
                print(e)
                print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
                self.df_output = pd.DataFrame(columns=OUTPUT_COLUMNS)

    def tfidf(self, df, top):
        if len(df) < 2:
            return {}
        else:
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform(df["processed_text"])
            feature_names = vectorizer.get_feature_names()
            dense = vectors.todense()
            denselist = dense.tolist()
            return (
                pd.DataFrame(denselist, columns=feature_names)
                .sum(axis=0, skipna=True)
                .sort_values(ascending=False)
                .head(top)
                .to_dict()
            )

    def frequency(self, df, top):
        if df.empty:
            return {}
        else:
            text = " ".join(list(df["processed_text"]))
            bagofwords = text.split(" ")
            tf_dict = {}
            bagofwordscount = len(bagofwords)
            for word, count in Counter(bagofwords).items():
                tf_dict[word] = count / float(bagofwordscount)
            return dict(sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)[:top])
