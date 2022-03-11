"""
Facilities required for a better re-factorization of the code
"""
import configurations
import logging
import os
import tqdm
import json

CONFIG = configurations.get_config_file()


class DataLoader:
    def __init__(self, limit: int = -1, use_tokenized=False) -> None:
        self.use_tokenized = use_tokenized
        if use_tokenized:
            self.src_data_path = CONFIG["DIR_PATH"]["TOKENIZED_DIR"]
        else:
            self.src_data_path = CONFIG["DIR_PATH"]["SRC_DIR"]

        self.all_file_names = os.listdir(self.src_data_path)
        self.limit = limit
        self._get_clean_file_names()

    def __enter__(self):
        print("Entered the DataLoader")

        return self._load_files_iterator()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self.src_data_path
        del self.use_tokenized
        del self.all_file_names
        del self.limit
        del self.clean_file_names
        print("Exited the DataLoader")
        return True

    def _load_files_iterator(self):
        for file_index, file_name in enumerate(
            tqdm.tqdm(self.clean_file_names, desc="Processing files", colour="green")
        ):
            try:
                article_data = json.load(open(f"{self.src_data_path}/{file_name}", "r"))
            except:
                print("corrupt file")
                os.remove(f"{self.src_data_path}/{file_name}")
                continue
            yield article_data

        return article_data

    def _get_clean_file_names(self):
        self.clean_file_names = []
        if self.limit == -1:
            print("All files will be loaded")
        else:
            print("%s files ONLY will be loaded", self.limit)

        file_counter = 0
        for file_index, file_name in enumerate(self.all_file_names):
            files_to_exclude = parse_single_filter_list(
                CONFIG["FILES_TO_EXCLUDE"]["FILES"]
            )

            if file_name not in files_to_exclude:
                if self.limit != -1:
                    if file_counter > self.limit:
                        break

                self.clean_file_names.append(file_name)
                file_counter += 1


def parse_single_filter_list(value):
    """
    It takes a string, comma separated, of options, and return a list of them
    """
    options_list = value.split(",")
    if options_list[-1] == "":
        return options_list[:-1]
    return options_list


def apply_filter_value(article_data: dict, filters: dict):
    years = filters.get("years", [])
    days = filters.get("days", [])
    months = filters.get("months", [])
    topics = filters.get("topics", [])
    words = filters.get("words", [])  # List of words that has to exist in the article

    article_pass_validation = True
    if len(years) > 0:
        years = parse_single_filter_list(years)
        if article_data["publication_date"]["year"] not in years:
            article_pass_validation = False

    if len(days) > 0:
        days = parse_single_filter_list(days)
        if article_data["publication_date"]["day"] not in days:
            article_pass_validation = False

    if len(months) > 0:
        months = parse_single_filter_list(months)
        if article_data["publication_date"]["month"] not in months:
            article_pass_validation = False

    if len(topics) > 0:
        topics = parse_single_filter_list(topics)
        if article_data["topic_category"] not in topics:
            article_pass_validation = False

    return article_pass_validation


def get_existing_links():
    """
    Return the list of all the links in the current data directory
    Necessary to recover from a failed connection
    """
    list_of_links = []
    with DataLoader() as data_handle:
        for file_index, article_data in enumerate(data_handle):
            list_of_links.append(article_data["article_link"])

    return list_of_links
