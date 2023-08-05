import json
import os
import re
import sys

import pandas as pd
import requests

ERR_SYS = "\nSystem error: "
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_MS_MODELOS = os.getenv("URL_MS_MODELOS", None)


def delete_file_dataframe(file_to_send, file_send):
    """
    this function delete temporal files send to ms_modelos

    Parameters
    ----------
    file_to_send : TYPE
        DESCRIPTION.
    file_send : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    try:
        file_send["model_json"].close()
        os.remove(file_to_send) if os.path.exists(file_to_send) else None
    except OSError as error:
        print("Error con eliminacion archivo" + error)
    except Exception as e_1:
        print("Error con eliminacion archivo" + e_1)


class CleanText:
    """
    this function clean and prepare text to analysis
    """

    def __init__(self, input_txt, verbose=False):
        """
        This functions validates if the input of the class is a string.

        Parameters
        ----------
        input_txt:
            type: str
            String to clean.
        mentions:
            verbose: bool
            If True prints when the input is not a string.
        """
        method_name = "__init__"

        self.bad_words = ["de", "que", "la", "los", "el", "las"]
        with open(BASE_DIR + "/common/stopwords/English.txt", "r") as file:
            self.stopwords = file.read().splitlines()
        self.bad_words.extend(self.stopwords)
        with open(BASE_DIR + "/common/stopwords/Spanish.txt", "r") as file:
            self.stopwords = file.read().splitlines()
        self.bad_words.extend(self.stopwords)

        if type(input_txt) == str:
            self.input_txt = input_txt
        else:
            if verbose:
                print(f'WARNING: Input {input_txt} is not a string. Default set to "".')
                print(f"Class: {self.__str__()}\nMethod: {method_name}")
            self.input_txt = ""

    def process_text(
        self,
        rts=False,
        mentions=False,
        hashtags=False,
        links=False,
        spec_chars=False,
        stop_words=True,
    ):
        """
        This functions cleans the input text.

        Parameters
        ----------
        rts:
            type: bool
            If True the patterns associated with retweets are removed
            from the text, default=False.
        mentions:
            type: bool
            If True the mentions are removed from the text, default=False.
        hashtags:
            type: bool
            If True the hashtags are removed from the text, default=False.
        links:
            type: bool
            If True the patterns associated with links (urls) are removed
            from the text, default=False.
        spec_chars:
            type: bool
            If True all special characters (except accents, # and @) are removed
            from the text, default=False.
        stop_words:
            type: bool
            If True stop_words are removed from the, text, default=True.

        Returns
        -------
        str
        """

        input_txt = self.input_txt.lower()
        if rts:
            rt_pattern = re.compile(r"^(?:RT|rt) \@[a-zA-Z0-9\-\_]+\b")
            input_txt = re.sub(rt_pattern, "", input_txt)
        if mentions:
            mention_pattern = re.compile(r"\@[a-zA-Z0-9\-\_]+\b")
            input_txt = re.sub(mention_pattern, "", input_txt)
        else:
            # procect '@' signs of being removed in spec_chars
            input_txt = input_txt.replace("@", "xxatsignxx")
        if hashtags:
            hashtag_pattern = re.compile(r"\#[a-zA-Z0-9\-\_]+\b")
            input_txt = re.sub(hashtag_pattern, "", input_txt)
        else:
            # procect '#' signs to being removed in spec_chars
            input_txt = input_txt.replace("#", "xxhashtagsignxx")
        if links:
            link_pattern = re.compile(r"\bhttps:.+\b")
            input_txt = re.sub(link_pattern, "", input_txt)
            link_pattern = re.compile(r"\bhttp:.+\b")
            input_txt = re.sub(link_pattern, "", input_txt)
        if spec_chars:
            input_txt = re.sub(r"[^a-zA-Z\u00C0-\u00FF ]", " ", input_txt)

        if stop_words:
            temp_txt = input_txt.split()
            temp_txt = [word for word in temp_txt if word not in self.bad_words]
            output_txt = " ".join(temp_txt)

        output_txt = output_txt.replace("xxatsignxx", "@")
        output_txt = output_txt.replace("xxhashtagsignxx", "#")

        return output_txt


class Features:
    def __init__(self):
        """
        This functions loads the spacy model for spanish.

        """

    def pos_tags(self, input_txt):
        """
        This functions get the features of the words in the input_txt parameter.

        Parameters
        ----------
        input_txt:
            type: str
            String to get the features from.

        Returns
        -------
        dict: keys -> tokens, lemmas and part of speech tags.
        i
        """
        method_name = "pos_tags"
        self.input_txt = input_txt
        if type(input_txt) != str:
            print("ERROR: Input is not a string.")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            self.input_txt = ""

        try:
            out_dict = send_to_model(
                data={"value": input_txt},
                ms_models_path=URL_MS_MODELOS + "/models_reg/features/pos_tags",
            )
        except Exception as e_1:
            print(e_1)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            out_dict = {"words": [], "lemmas": [], "pos_tags": []}

        return out_dict


class Polarity:
    def __init__(self):
        self.polscore = [-1.0, -0.5, 0, 0.5, 1.0]

    def tokenize_texts(self, text_list, max_length=128):
        try:
            model_name = "polarity"
            model_type = "tokenize_texts"
            encoded_dict = df_to_formatted(
                text_list, URL_MS_MODELOS, model_name, model_type
            )
        except Exception as e_1:
            print(e_1)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            raise e_1
        input_ids_b = encoded_dict["input_ids"]
        attention_masks_b = encoded_dict["attention_mask"]

        return (input_ids_b, attention_masks_b)

    def forward_model(self, data):
        try:
            model_name = "polarity"
            model_type = "tokenize_texts"
            (out,) = df_to_formatted(data, URL_MS_MODELOS, model_name, model_type)
        except Exception as e_1:
            print(e_1)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            raise e_1

        sentiment = list(out.argmax(1).numpy())

        return sentiment

    def batch_forward(self, text_list, batch_size, max_length):

        num_texts = len(self.df_text)
        batch_idx = slice(0, num_texts, batch_size)

        polarity = []
        for i in range(num_texts // batch_size):
            batch_idx = slice(batch_size * i, batch_size * (i + 1), 1)
            (input_ids_b, attention_masks_b) = self.tokenize_texts(
                text_list[batch_idx], max_length=max_length
            )
            sentiment_list = self.forward_model((input_ids_b, attention_masks_b))

            polarity.extend(sentiment_list)

        if num_texts % batch_size:
            batch_idx = slice(batch_size * (num_texts // batch_size), num_texts, 1)
            (input_ids_b, attention_masks_b) = self.tokenize_texts(
                text_list[batch_idx], max_length=max_length
            )
            sentiment_list = self.forward_model((input_ids_b, attention_masks_b))

            polarity.extend(sentiment_list)

        return polarity

    def batch_polarity(
        self, df_text, text_column_name="processed_text", batch_size=2, max_length=128
    ):
        """
        This function returns the polarity of an input texts procesed by batches.

        Parameters
        ----------
        df_text:
            type: str, list of strings, pandas DataFrame with a text column.
            clean text for which the polarity is obtained

        text_column_name (optional):
            type: str, name of the text column in the pandas DataFrame.

        batch_size (optional):
            type: int, number of text to process at the same time by doing a forward in the model.
            default: 20

        Returns
        -------
        pandas DataFrame with a 'polarity' column with the polarity values.
        (warning, this method returns -100 if input is not a list of strings or pandas DataFrame.)

        """

        method_name = "batch_polarity"

        if isinstance(df_text, list) and all(isinstance(text, str) for text in df_text):
            df_text = pd.DataFrame(columns=["processed_text"], data=df_text)

        if isinstance(df_text, pd.DataFrame):
            try:
                df_text["polarity"] = self.batch_forward(
                    list(df_text[text_column_name]),
                    batch_size=batch_size,
                    max_length=max_length,
                )
                dict_polscore = {idx: score for idx, score in enumerate(self.polscore)}
                df_text["polarity"] = df_text["polarity"].map(dict_polscore)

            except Exception as e_1:
                print(e_1)
                error_1 = sys.exc_info()[0]
                print(ERR_SYS + str(error_1))
                print(f"Class: {self.__str__()}\nMethod: {method_name}")
                df_text["polarity"] = ""
            return df_text

        elif isinstance(df_text, str):
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print(
                "Must recieve a list of string of pandas DataFrame with strings. returning -100 ..."
            )
            return -100

        else:
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print(
                "Calling polarity method for a non-string variable. returning -100 ..."
            )
            polarity = -100
            return polarity

    def polarity(self, df_text):
        """
        This function returns the polarity of an input text(s).

        Parameters
        ----------
        df_text:
            type: str, list of strings, pandas DataFrame with a text column.
            clean text for which the polarity is obtained

        text_column_name (optional):
            type: str, name of the text column in the pandas DataFrame.

        Returns
        -------
        polarity value or pandas DataFrame with a 'polarity' column with
        the polarity values. (warning, this method returns -100 if input
                              is not a string or if input text is too long.)

        """
        try:
            model_name = "polarity"
            model_type = "polarity"
            polarity = df_to_formatted(df_text, URL_MS_MODELOS, model_name, model_type)
            return polarity
        except Exception as e_1:
            print(e_1)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            raise e_1

    def polarity_only(self, df_text):
        """
        This function returns the polarity of an dataframe


        Parameters
        ----------
        df_text : TYPE dataframe
            DESCRIPTION.dataframe, with the column polarity to be calculated
        column_text : TYPE, string
            DESCRIPTION. text column.with the polarity to be calculated
            for Facebook = message
            for Instagram = text
            for Twitter = text

        Returns
        -------
        polarity value or pandas DataFrame with a 'polarity' column with the polarity values
        """
        try:
            model_name = "polarity"
            model_type = "polarity_only"
            polarity = df_to_formatted(df_text, URL_MS_MODELOS, model_name, model_type)
            return polarity
        except Exception as e_1:
            print(e_1)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            raise e_1


class STTM:
    def __init__(self, df_data, text_column_name="tokenized_text"):
        """
        This function stores the input DataFrame.

        Parameters
        ----------
        df_data:
            type: DataFrame
            This Pandas DataFrame must have the column 'tokenized text'.

        """

        self.df_data = df_data
        self.text_column_name = text_column_name

    def sttm_model(self):
        """
        This function classifies the tokenized texts into groups
        of similar texts. It creates the 'sttm_group' column with the
        number of the group that the text was classified into.

        Parameters
        ----------
        K:
            type: int
            Number of initial groups that the texts are classified into.
        alpha:
            type: float
            Parameter of the sttm model .
        beta:
            type: float
            Parameter of the sttm model.
        n_iters:
            type: int
            Number of iterations of the sttm model.

        Returns
        ----------
        df_data:
            DataFrame with the 'sttm_group' column

        """

        try:
            model_name = "sttm"
            model_type = "sttm_model"
            self.df_data = df_to_formatted(
                self.df_data, URL_MS_MODELOS, model_name, model_type
            )
        except Exception as e_1:
            print(e_1)
            error_1 = sys.exc_info()[0]
            print(ERR_SYS + str(error_1))
            raise e_1
        return self.df_data


def send_to_model(data, ms_models_path, ensure_ascii=True):
    """
    Auxiliar function used to send data to models microservice

    Parameters
    ----------
    data :
        Request body
    ms_models : [type]
        Path of models microservice
    """

    response = requests.post(url=ms_models_path, data=json.dumps(data))

    if response.ok:
        return response.json()
    else:
        raise RuntimeError(f"Models microservice error {response.status_code}")


def df_to_formatted(df, url_model, model_name, model_type):
    ms_models_path = url_model + "/models_reg/" + model_name + "/" + model_type

    if model_name == "polarity":
        df["polarity"] = df["processed_text"].apply(
            lambda txt: send_to_model({"value": txt}, ms_models_path)
        )
    elif model_name == "sttm":

        response = send_to_model(
            data=df[["id", "tokenized_text"]].to_dict(orient="records"),
            ms_models_path=ms_models_path,
            ensure_ascii=False,
        )

        df = pd.merge(df, pd.DataFrame(response, columns=["id", "sttm_group"]), on="id")
    else:
        raise NotImplementedError()

    return df
