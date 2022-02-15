"""
Using different word vectorization technicques, what can tell about our documents?
1. What are the important words?
2. What the cluster of topics?
"""
import configparser
from sklearn.feature_extraction.text import TfidfVectorizer
from tokenization import apply_filter_value
import numpy as np
from collections.abc import Mapping, Sequence
import os
from typing import List
import json

config = configparser.ConfigParser()
config.read("./config/config.ini")

FILTERS = dict(config["FILTERS"])


def load_articles(directory: str) -> List[dict]:
    file_names = os.listdir(directory)
    counter = 0
    list_of_all_text = []
    for file_index, file_name in enumerate(file_names):
        # if file_index >= 1000:
        #     break
        if (file_name != "all_links_recorded.json") and (
            file_name != "all_topic_collected.json"
        ):
            article_data = json.load(open(f"{directory}/{file_name}", "r"))

            if apply_filter_value(article_data, filters=FILTERS):
                counter += 1
                list_of_all_text.append(article_data["article_content"]["content"])

    print(f"All articles: {counter}")
    return list_of_all_text


def tf_idf_transformation(documents: List[str]) -> np.ndarray:
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents)
    pass


def clustering(vectorized_documents: np.ndarray, documents_id: List[str]):
    pass


def main():
    load_articles(directory=config["DIR_PATH"]["SRC_DIR"])


if __name__ == "__main__":
    main()