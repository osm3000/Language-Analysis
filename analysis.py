"""
A set of analysis functions, in order to address the required questions
"""
from matplotlib.artist import Artist
import pandas as pd
from collections.abc import Sequence
import logging
import configparser
import tokenization

config = configparser.ConfigParser()
config.read("./config/config.ini")

FILTERS = dict(config["FILTERS"])
RESULTS_DIR = tokenization.form_results_folder_name(FILTERS)
TGT_DIR = config["DIR_PATH"]["TGT_DIR"]
TOKENIZED_DIR = config["DIR_PATH"]["TOKENIZED_DIR"]

# logging.basicConfig(
#     filename=f"{config['DIR_PATH']['LOG_DIR']}/results.log",
#     format="%(levelname)s:%(funcName)s:%(asctime)s:%(message)s",
#     level=logging.INFO,
# )


def extract_words_to_percentage(
    words_df: pd.DataFrame, required_percentages: Sequence
) -> Sequence:
    """
    For a specific percentage, how many words are there?
    """
    words_df["freq_cumsum"] = words_df["frequency"].cumsum()
    for percentage in required_percentages:
        words_of_interest = (words_df["freq_cumsum"] < percentage).value_counts()
        print(f"Percentage: {percentage}")
        print(words_of_interest)


def n_gram_analysis(data: dict, n_grams: int = 2):
    """
    Given the tokenized articles, return the n-gram dictionaries
    """
    n_grams_lists = []
    for article in data:
        article_content = article["article_content"]["content"]
        single_words = article_content.split(" ")
        for word_index, word in enumerate(single_words[: -(n_grams - 1)]):
            one_n_grams = []
            for word_sub_index in range(n_grams):
                one_n_grams.append(single_words[word_index + word_sub_index])

            n_grams_lists.append(one_n_grams)

    return n_grams_lists


def main():
    logging.info("/**/" * 20)
    logging.info("Fresh new start")
    all_words = pd.read_csv(f"{TGT_DIR}/{RESULTS_DIR}/allWords.csv")
    extract_words_to_percentage(all_words, [10, 20, 50])


if __name__ == "__main__":
    main()