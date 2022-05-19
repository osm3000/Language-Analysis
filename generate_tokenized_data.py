"""
Tokenize all the articles, and generate a processed version of dataset. Will be useful later for further analysis
"""
import numpy as np
import pandas as pd
import utilities
import tokenizer
import json
import os
import configurations


def main():
    word_tokenizer = tokenizer.Spacy_Tokenizer()
    # if not os.path.isdir(config["DIR_PATH"]["TOKENIZED_DIR"]):
    #     print(f"Folder doesn't exit. Create it")
    #     os.mkdir(config["DIR_PATH"]["TOKENIZED_DIR"])

    with utilities.DataLoader(limit=2, data_path="./ALL_DATA_2") as data_handler:
        for articles_index, article_data in enumerate(data_handler):
            article_file_name = article_data["file_name"]
            tokenized_article = word_tokenizer.tokenize_article(article_data)
            print(tokenized_article["article_content"])

            # with open(
            #     f'{config["DIR_PATH"]["TOKENIZED_DIR"]}/{articles_index}.json', "w"
            # ) as file_handle:
            #     json.dump(
            #         tokenized_article,
            #         file_handle,
            #     )


if __name__ == "__main__":
    main()