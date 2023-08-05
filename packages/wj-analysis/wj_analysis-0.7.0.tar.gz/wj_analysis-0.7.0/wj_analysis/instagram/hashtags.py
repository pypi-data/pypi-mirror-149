import re
import sys
from copy import deepcopy
from datetime import datetime

import pandas as pd

from wj_analysis.instagram import polarity_distribution

ERR_SYS = "\nSystem error: "


class Hashtags:
    def content_type(self, df_hashtags):
        """
        This method calculates the number of publications of each type
        for a specific hashtag call.

        Parameters
        ----------
        df_hashtags:
            type: DataFrame
            This Pandas DataFrame is obtained by the call of a hashtag using the
            official Instagram API by Facebook
        """

        METHOD_NAME = "content_type"

        HASHTAGS_COLUMNS = ["comments_count", "like_count", "type"]

        OUTPUT_COLUMNS = ["type", "counts", "avg_engagement_rate", "percentage"]

        try:
            output = pd.DataFrame(columns=OUTPUT_COLUMNS)
            df_contenttype = deepcopy(df_hashtags[HASHTAGS_COLUMNS])
            df_contenttype["engagement_rate"] = (
                df_contenttype["comments_count"] + df_contenttype["like_count"]
            )
            media_type = df_contenttype["type"].drop_duplicates()
            total_counts = len(df_contenttype)
            for mt in media_type:
                df_type = df_contenttype[df_contenttype["type"] == mt]
                counts = len(df_type)
                avg_engagement_rate = df_type["engagement_rate"].mean()
                percentage = (counts / total_counts) * 100
                output.loc[len(output)] = [mt, counts, avg_engagement_rate, percentage]
            return output
        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(columns=OUTPUT_COLUMNS)

    def sentiment_analysis(self, df_hashtags):
        """
        This method evaluates the sentiment of the text inside each publication that has
        the desire hashtag.

        Parameters
        ----------
        df_hashtags:
            type: DataFrame
            This Pandas DataFrame is obtained by the call of a hashtag using the
            official Instagram API by Facebook
        """

        METHOD_NAME = "sentiment_analysis"

        HASHTAGS_COLUMNS = ["caption"]

        OUTPUT_COLUMNS = ["all", "sentiment"]

        try:
            df_sentimentanalysis = deepcopy(df_hashtags[HASHTAGS_COLUMNS])
            df_sentimentanalysis = df_sentimentanalysis.rename(
                columns={"caption": "text"}
            )
            getpol = polarity_distribution.PolarityDistributionIG(
                df_sentimentanalysis, {}
            )
            getpol.get_polarity()
            return getpol.grouped_polarities(group_by="all")

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(columns=OUTPUT_COLUMNS)

    def time_series(self, df_hashtags, level="hour"):
        """
        This method calculates the frequency that the hashtag had during a period.

        Parameters
        ----------
        df_hashtags:
            type: DataFrame
            This Pandas DataFrame is obtained by the call of a hashtag using the
            official Instagram API by Facebook
        level:
            type: string
            This has to be one of the values of the variable "frequency", will filter
            the way the output would group.
        """

        METHOD_NAME = "time_series"

        HASHTAGS_COLUMNS = ["timestamp", "id"]

        OUTPUT_COLUMNS = ["created_at", "counts", "level"]

        frequency = {
            "business_day": "B",
            "calendar_day": "D",
            "weekly": "W",
            "monthly": "M",
            "15days": "SM",
            "hour": "H",
            "minutes": "T",
            "seconds": "S",
        }
        try:

            df_post_by_date = deepcopy(df_hashtags)
            # -----extract shortcode from permalink---------------------------------------
            df_post_by_date["shortcode"] = ""
            for i in range(0, len(df_post_by_date)):
                link = df_post_by_date["permalink"][i]
                shortcode = link[25:]
                type_shortcode = shortcode[:3]
                if type_shortcode == "/p/":
                    shortcode = shortcode[3:]
                    shortcode = re.sub("/", "", shortcode)
                else:
                    shortcode = shortcode[4:]
                    shortcode = re.sub("/", "", shortcode)

                df_post_by_date["shortcode"][i] = shortcode
            # ----------------------------------------------------------------------------

            df_post_by_date = df_post_by_date[["timestamp", "shortcode"]]
            df_post_by_date["timestamp"] = df_post_by_date["timestamp"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S+%f")
            )
            for j in range(0, len(df_post_by_date)):
                if level == "calendar_day":
                    date = df_post_by_date["timestamp"][j]
                    df_post_by_date["timestamp"][j] = date.replace(
                        hour=0, minute=0, second=0, microsecond=0
                    )
                elif level == "hour":
                    date = df_post_by_date["timestamp"][j]
                    df_post_by_date["timestamp"][j] = date.replace(
                        minute=0, second=0, microsecond=0
                    )
            df_post_by_date = (
                df_post_by_date.groupby("timestamp")["shortcode"]
                .apply(list)
                .reset_index(name="list_id_post")
            )
            df_post_by_date = df_post_by_date.sort_values("timestamp")

            df_timeseries = deepcopy(df_hashtags[HASHTAGS_COLUMNS])
            df_timeseries["timestamp"] = df_timeseries["timestamp"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S+%f")
            )
            output = (
                df_timeseries.groupby(
                    [pd.Grouper(key="timestamp", freq=frequency[level])]
                )
                .size()
                .reset_index(name="counts")
            )
            output = output.rename(columns={"timestamp": "created_at"})

            output = output.sort_values("created_at")
            output["level"] = level

            output["list_post_id"] = ""
            for i in range(0, len(output)):
                for k in range(0, len(df_post_by_date)):
                    if df_post_by_date["timestamp"][k] == output["created_at"][i]:
                        output["list_post_id"][i] = df_post_by_date["list_id_post"][k]
            for i in range(0, len(output)):
                if output["list_post_id"][i] == "":
                    output["list_post_id"][i] = []
            return output

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(columns=OUTPUT_COLUMNS)

    def additional_hashtags(self, df_hashtags, top=10):
        """
        This method filters the hashtags that accompany the original
        and calculates their number of calls.

        Parameters
        ----------
        df_hashtags:
            type: DataFrame
            This Pandas DataFrame is obtained by the call of a hashtag using the
            official Instagram API by Facebook
        top:
            type: int
            Top number of hashtags that want to be return.
        """

        METHOD_NAME = "additional_hashtags"

        HASHTAGS_COLUMNS = ["caption"]

        OUTPUT_COLUMNS = ["hashtags", "counts"]

        try:
            df_aditionalhashtags = deepcopy(df_hashtags[HASHTAGS_COLUMNS])
            df_aditionalhashtags = df_aditionalhashtags.rename(
                columns={"caption": "text"}
            )
            df_aditionalhashtags = df_aditionalhashtags.dropna()
            df_aditionalhashtags["text"] = df_aditionalhashtags["text"].apply(
                lambda text: re.sub(r"[^0-9a-zA-Z#]", " ", text).replace("#", " #")
            )
            hashtags_list = []
            df_aditionalhashtags["text"].apply(
                lambda text: [
                    hashtags_list.append(word) for word in text.split() if "#" in word
                ]
            )
            output = (
                pd.DataFrame(
                    [hashtag.lower() for hashtag in hashtags_list], columns=["hashtags"]
                )["hashtags"]
                .value_counts()
                .reset_index(name="counts")
            )
            output = output[~output["index"].isin(["#"])]
            return output.iloc[1 : top + 1].reset_index(drop=True)

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(columns=OUTPUT_COLUMNS)
