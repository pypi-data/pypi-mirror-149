import sys
from collections import Counter
from copy import deepcopy
from datetime import datetime

import pandas as pd

ERR_SYS = "\nSystem error: "


def join(iterator, seperator):
    """
    This function casts the elements of iterator to strings then merges those strings together with a string
    representation of seperator.
    Had to write a custom join to handle very, very long lists of things. "".join falls appart above 3013.
    params
    iterator: an iterator.  This function makes use of the overload + operator for strings
    seperator: an item of the same class as is contained in our iterator to be added between every pair of instances.
    returns
    The sum of the iterator values with seperator iterposed between each.
    """
    it = map(str, iterator)
    seperator = str(seperator)
    string = next(it, "")
    for s in it:
        string += seperator + s
    return string


unique_join = lambda x: join(x, ",")


class TermTrend:
    def __init__(self, df_tweets):
        """
        This function copies the input DataFrame.

        Parameters
        ----------
        df_tweets:
            type: DataFrame
            Information of the posts.
            This Pandas DataFrame must have columns 'created_at', 'twitter_id',
            'screen_name', 'user_mentions', 'text', 'ac_followers_count'.
        """

        METHOD_NAME = "__init__"

        TWEETS_COLUMNS = [
            "twitter_id",
            "screen_name",
            "created_at",
            "text",
            "ac_followers_count",
            "user_mentions",
            "profile_image",
            "engagement_rate_by_post",
            "tweet_id",
        ]

        try:

            if "engagement_rate_by_post" not in df_tweets.keys():
                df_tweets["engagement_rate_by_post"] = None

            df_tweets_in = deepcopy(df_tweets[TWEETS_COLUMNS])
            if not df_tweets.empty:
                df_tweets_in["created_at"] = pd.to_datetime(
                    df_tweets_in["created_at"]
                )  # revisar con back si se tiene que hacer corrección horaria

            else:
                print("Warning: The dataframe is empty.")

            self.df_tweets_in = df_tweets_in

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            self.df_tweets_in = pd.DataFrame(columns=TWEETS_COLUMNS)

    def time_series(self, level="hour"):
        """
        This function computes the time series for the posts in the input DataFrame.

        Parameters
        ----------
        level:
            type: str
            Determines the level of resolution to plot in the time series.

        Returns
        -------
        DataFrame
        """

        METHOD_NAME = "time_series"

        df_tweets_out = deepcopy(self.df_tweets_in[["created_at"]])
        df_tweets_id = deepcopy(self.df_tweets_in[["created_at", "tweet_id"]])

        try:
            df_tweets_out["mention_counts"] = 1
            df_tweets_out["created_at"] = df_tweets_out["created_at"].apply(
                lambda dt: datetime(
                    year=dt.year, month=dt.month, day=dt.day, hour=dt.hour
                )
            )
            df_tweets_id["created_at"] = df_tweets_out["created_at"].apply(
                lambda dt: datetime(
                    year=dt.year, month=dt.month, day=dt.day, hour=dt.hour
                )
            )
            df_tweets_id = (
                df_tweets_id.groupby("created_at")["tweet_id"]
                .apply(list)
                .reset_index(name="list_id_post")
            )
            df_tweets_out = (
                df_tweets_out.groupby("created_at")
                .count()
                .reset_index()
                .sort_values("created_at")
            )
            df_tweets_out["level"] = level
            df_tweets_out["list_post_id"] = df_tweets_id["list_id_post"]

            return df_tweets_out

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(columns=["created_at", "mention_counts", "level"])

    def mentions_network(self, n_most_posts=None, min_group=10, max_nodes=None):
        """
        This function computes the mentions network for the posts in the input DataFrame.

        Parameters
        ----------
        n_most_posts:
            type: int
            Determines the number of posts to create the network from.
            Default = None.
        min_group:
            type: int
            Determines the minimum number of mentions that form a group of
            mentions in the visualization. Default = 10.

        Returns
        -------
        Tuple of DataFrames
        """

        METHOD_NAME = "mentions_network"

        try:
            df_tweets_out = deepcopy(
                self.df_tweets_in[
                    [
                        "twitter_id",
                        "screen_name",
                        "user_mentions",
                        "text",
                        "ac_followers_count",
                        "profile_image",
                    ]
                ]
            )
            df_tweets_out = df_tweets_out[~df_tweets_out["user_mentions"].isna()]

            data_nx = df_tweets_out.groupby(["twitter_id", "screen_name"]).agg(
                {
                    "user_mentions": unique_join,
                    "text": "count",
                    "ac_followers_count": "max",
                    "profile_image": "last",
                }
            )

            if not n_most_posts:
                n_most_posts = len(data_nx)

            data_nx = (
                data_nx.sort_values("text", ascending=False)
                .reset_index()
                .head(n_most_posts)
            )

            # Nodes with posts in the input DataFrame
            nodes_ini = data_nx[
                [
                    "twitter_id",
                    "screen_name",
                    "text",
                    "ac_followers_count",
                    "profile_image",
                ]
            ]
            nodes_ini = nodes_ini.rename(
                columns={
                    "twitter_id": "id",
                    "screen_name": "label",
                    "text": "value",
                    "profile_image": "image",
                }
            )
            nodes_ini["title"] = nodes_ini["ac_followers_count"].apply(
                lambda fw: f"Followers: {fw}"
            )
            nodes_ini = nodes_ini.drop(columns=["ac_followers_count"])

            # Nodes without posts in the input DataFrame
            ment_list = []
            for ment in ",".join(data_nx["user_mentions"]).split(","):
                if ment not in list(data_nx["screen_name"]):
                    ment_list.append(ment)
            ment_list = Counter(ment_list)

            id_list = [f"id_{acc}" for acc in ment_list.keys()]

            nodes_fin = pd.DataFrame(
                {
                    "id": id_list,
                    "label": list(ment_list.keys()),
                    "value": list(ment_list.values()),
                }
            )
            nodes_fin["title"] = 'Followers: "unk"'

            # Concatenation of all nodes
            nodes = pd.concat([nodes_ini, nodes_fin]).reset_index()

            nodes_dict = {}
            for _, row in nodes.iterrows():
                nodes_dict[row.label] = row.id

            # Edges
            from_list = []
            to_list = []
            for _, row in data_nx.iterrows():
                for ment in row.user_mentions.split(","):
                    from_list.append(row.twitter_id)
                    to_list.append(nodes_dict[ment])
            edges = pd.DataFrame({"from": from_list, "to": to_list})

            edges["value"] = 1
            edges = edges.groupby(["from", "to"]).count().reset_index()

            # Grouping nodes and edges to
            nodes["id"] = nodes["id"].apply(lambda i: str(i))
            edges["from"] = edges["from"].apply(lambda i: str(i))
            edges["to"] = edges["to"].apply(lambda i: str(i))

            to_number = (
                edges.groupby(["from"])
                .agg({"to": lambda x: ",".join(x), "value": "count"})
                .reset_index()
            )

            one_to_edges = to_number[to_number["value"].eq(1)]["from"]
            one_to_edges = list(
                set(one_to_edges) - set(edges[edges["to"].isin(one_to_edges)]["to"])
            )

            group_edges_from = (
                edges[edges["from"].isin(one_to_edges)]
                .groupby("to")
                .agg({"value": "count", "from": lambda x: ",".join(x)})
                .reset_index()
            )

            new_nodes_from = group_edges_from[group_edges_from["value"] >= min_group]

            if not new_nodes_from.empty:
                new_nodes_from["label"] = new_nodes_from.apply(
                    lambda row: f'{row["value"]} usuarios', axis=1
                )
                new_nodes_from["title"] = new_nodes_from.apply(
                    lambda row: f'Se agruparon: {row["value"]} usuarios', axis=1
                )
                new_nodes_from["image"] = "group_from"
                new_nodes_from["id"] = new_nodes_from.apply(
                    lambda row: f'{row["value"]}_a_{row["to"]}', axis=1
                )

                for _, row in new_nodes_from.iterrows():
                    edge_remove = row["from"].split(",")
                    nodes = nodes[~nodes["id"].isin(edge_remove)]
                    edges = edges[~edges["from"].isin(edge_remove)]

                new_nodes_from = new_nodes_from.drop(columns=["from", "to"])
                nodes = pd.concat([nodes, new_nodes_from])
                try:
                    nodes = nodes.drop(columns=["index"])
                except Exception:
                    pass

                new_edges = nodes[nodes["image"].eq("group_from")]
                new_edges["to"] = new_edges["id"].apply(
                    lambda index: index.split("_", 2)[2]
                )
                new_edges = new_edges.rename(columns={"id": "from"})
                new_edges = new_edges[["from", "to", "value"]]
                edges = pd.concat([edges, new_edges])

            # Grouping nodes and edges from

            nodes["id"] = nodes["id"].apply(lambda i: str(i))
            edges["from"] = edges["from"].apply(lambda i: str(i))
            edges["to"] = edges["to"].apply(lambda i: str(i))

            from_number = (
                edges.groupby(["to"])
                .agg({"from": lambda x: ",".join(x), "value": "count"})
                .reset_index()
            )

            one_from_edges = from_number[from_number["value"].eq(1)]["to"]
            one_from_edges = list(
                set(one_from_edges)
                - set(edges[edges["from"].isin(one_from_edges)]["from"])
            )

            group_edges_to = (
                edges[edges["to"].isin(one_from_edges)]
                .groupby("from")
                .agg({"value": "count", "to": lambda x: ",".join(x)})
                .reset_index()
            )

            new_nodes_to = group_edges_to[group_edges_to["value"] >= min_group]

            if not new_nodes_to.empty:
                new_nodes_to["label"] = new_nodes_to.apply(
                    lambda row: f'{row["value"]} usuarios', axis=1
                )
                new_nodes_to["title"] = new_nodes_to.apply(
                    lambda row: f'Se agruparon: {row["value"]} usuarios', axis=1
                )
                new_nodes_to["image"] = "group_to"
                new_nodes_to["id"] = new_nodes_to.apply(
                    lambda row: f'{row["from"]}_a_{row["value"]}', axis=1
                )

                for _, row in new_nodes_to.iterrows():
                    edge_remove = row["to"].split(",")
                    nodes = nodes[~nodes["id"].isin(edge_remove)]
                    edges = edges[~edges["to"].isin(edge_remove)]

                new_nodes_to = new_nodes_to.drop(columns=["from", "to"])
                nodes = pd.concat([nodes, new_nodes_to])
                try:
                    nodes = nodes.drop(columns=["index"])
                except Exception:
                    pass

                new_edges = nodes[nodes["image"].eq("group_to")]
                new_edges["from"] = new_edges["id"].apply(
                    lambda index: index.split("_")[0]
                )
                new_edges = new_edges.rename(columns={"id": "to"})
                new_edges = new_edges[["from", "to", "value"]]
                edges = pd.concat([edges, new_edges])

            # apply max_nodes filter
            if max_nodes:
                nodes = nodes.sort_values("value", ascending=False)
                nodes = nodes.head(max_nodes)

                edges = edges[edges["from"].isin(nodes["id"])]
                edges = edges[edges["to"].isin(nodes["id"])]

            nodes = nodes.drop_duplicates(subset=["id"], keep="last")

            return nodes, edges

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            nodes = pd.DataFrame(columns=["id", "label", "value", "title", "image"])
            edges = pd.DataFrame(columns=["from", "to", "value"])
            return nodes, edges

    def accounts(self, engagement_rate="engagement_rate_by_post"):
        """
        This function computes the number of times an account is in the input DataFrame and its
        average engagement rate.

        Parameters
        ----------
        engagement_rate:
            type: str
            Determines the column of engagement rate for the computations,
            default='engagement_rate_by_post'

        Returns
        -------
        DataFrames
        """

        METHOD_NAME = "accounts"

        try:
            df_tweets_out = deepcopy(
                self.df_tweets_in[["screen_name", engagement_rate]]
            )
            df_tweets_out["posts_count"] = 1
            df_tweets_out = (
                df_tweets_out.groupby("screen_name")
                .agg({"posts_count": "count", engagement_rate: "mean"})
                .reset_index()
            )

            return df_tweets_out.sort_values("posts_count", ascending=False)

        except Exception as e:
            exception_type = sys.exc_info()[0]
            print(ERR_SYS + str(exception_type))
            print(e)
            print(f"Class: {self.__str__()}\nMethod: {METHOD_NAME}\n")
            return pd.DataFrame(columns=["screen_name", engagement_rate, "posts_count"])
