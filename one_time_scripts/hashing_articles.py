"""
Hashing the URL of the articles, and change the file name to be the hashed.
Now, this is a one time use. For the future, it is better to integrate this with the the scrapping function directly.
"""
import hashlib
import configurations
import logging
import os
import tqdm
import json
import utilities
import os

CONFIG = configurations.get_config_file()

# CONSUMING_DIR = ["./data_4", "./data_5", "./data_6"]
CONSUMING_DIR = ["/home/osm3000/new_data/data"]

TARGET_FOLDER = "./ALL_DATA"


class DataLoader_specific_hashing(utilities.DataLoader):
    """
    A copy from the DataLoader modified in order to read files as input to the instant, not from the configuration files
    """

    def __init__(
        self, limit: int = -1, use_tokenized=False, folder_path: str = "./data_4"
    ) -> None:
        self.use_tokenized = use_tokenized
        self.src_data_path = folder_path

        self.all_file_names = os.listdir(self.src_data_path)
        self.limit = limit
        self._get_clean_file_names()


def hash_string(str_to_hash: str):
    return hashlib.md5(str_to_hash.encode()).hexdigest()


def main():
    for folder_path in CONSUMING_DIR:
        print(f"Folder: {folder_path}")
        with DataLoader_specific_hashing(folder_path=folder_path) as data_handle:
            for file_index, article_data in enumerate(data_handle):
                hashed_url = hash_string(article_data["article_link"])
                # print(hashed_url)
                json.dump(article_data, open(f"{TARGET_FOLDER}/{hashed_url}.json", "w"))


if __name__ == "__main__":
    main()
