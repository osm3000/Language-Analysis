"""
A set of analysis functions, in order to address the required questions
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import pandas as pd
from collections.abc import Sequence
import logging
import configparser
import tokenization
import utilities

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


def tf_idf():
    """
    Identify what is the important words -> the words less frequent
    """
    # Form the corpus
    corpus = []
    nb_of_articles = 0
    with utilities.DataLoader(limit=-1, use_tokenized=True) as data_handler:
        for file_index, article_data in enumerate(data_handler):
            if utilities.apply_filter_value(article_data, filters=FILTERS):
                nb_of_articles += 1
                article_content = article_data["article_content"]["content"]
                corpus.append(article_content)

    # Apply TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(f"Nb of articles: {nb_of_articles}")

    used_vocab = np.array(vectorizer.get_feature_names())
    importances = vectorizer.idf_

    important_words = used_vocab[importances > 6.5]

    # print(important_words.tolist())
    print(important_words.shape)
    # print(vectorizer.idf_.shape)
    print(X.shape)

    # pca = PCA(n_components=500)
    # pca.fit(X.todense())

    # print(np.sum(pca.explained_variance_ratio_))

    # print(pca.singular_values_)

    # plt.figure()
    # plt.hist(X.todense().flatten())
    # plt.show()

    # x = X[:, ]

    X = X.todense().flatten()
    print(f"Total: ", X.shape[1])
    thresholds = [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 0.8, 1]
    for index, threshold in enumerate(thresholds):
        print(threshold)
        # print(X[X < threshold].shape)

        if index == 0:
            print(X[X < threshold].shape[1])
        else:
            value = (
                X[X < thresholds[index]].shape[1]
                - X[X < thresholds[index - 1]].shape[1]
            )
            print(
                value
                # - X[X >= thresholds[index - 1]].shape[1]
            )


def main():
    logging.info("/**/" * 20)
    logging.info("Fresh new start")
    # all_words = pd.read_csv(f"{TGT_DIR}/{RESULTS_DIR}/allWords.csv")
    # extract_words_to_percentage(all_words, [10, 20, 50])
    tf_idf()


if __name__ == "__main__":
    main()