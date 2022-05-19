"""
Facilities required for a better re-factorization of the code
"""
import configurations
import logging
import os
import tqdm
import json
import asyncio

CONFIG = configurations.get_config_file()


class FunctionalDataQueries:
    """
    Go through all the files in a functional way
    """

    def __init__(self, limit: int = -1, batch_size=10000) -> None:
        self.batch_size = batch_size
        # self.src_data_path = CONFIG["DIR_PATH"]["SRC_DIR"]
        self.src_data_path = "./ALL_DATA"

        self.all_file_names = os.listdir(self.src_data_path)
        self.limit = limit
        self._get_clean_file_names()

    def execute_query(self, query_function):
        final_results = []
        if self.limit == -1:
            nb_of_articles_left = len(self.clean_file_names)
        else:
            nb_of_articles_left = self.limit

        results = map(
            lambda link: self.scan_one_article(link, query_function),
            self.clean_file_names[:nb_of_articles_left],
        )
        filtered_results = []
        for item in results:
            if item is not None:
                filtered_results.append(item)
        final_results = filtered_results

        return final_results

    def scan_one_article(self, file_name: str, query_function):
        article_data = None
        with open(f"{self.src_data_path}/{file_name}", "r") as file_handle:
            article_data = json.load(file_handle)

        return query_function(article_data)

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


class AsyncDataQueries:
    """
    Going through the files in asynchronous manner to execute different queries
    """

    def __init__(self, limit: int = -1, batch_size=10000) -> None:
        self.batch_size = batch_size
        # self.src_data_path = CONFIG["DIR_PATH"]["SRC_DIR"]
        self.src_data_path = "./ALL_DATA"

        self.all_file_names = os.listdir(self.src_data_path)
        self.limit = limit
        self._get_clean_file_names()

    async def execute_query(self, query_function):
        final_results = []
        if self.limit == -1:
            nb_of_articles_left = len(self.clean_file_names)
        else:
            nb_of_articles_left = self.limit

        files_counter = 0
        while nb_of_articles_left > 0:
            print(nb_of_articles_left)
            if nb_of_articles_left < self.batch_size:
                links_batch = self.clean_file_names[
                    files_counter : files_counter + nb_of_articles_left
                ]
            else:
                links_batch = self.clean_file_names[
                    files_counter : files_counter + self.batch_size
                ]
            results = await asyncio.gather(
                *[
                    self.scan_one_article(link, query_function)
                    for link_index, link in enumerate(links_batch)
                ]
            )
            filtered_results = []
            for item in results:
                if item is not None:
                    filtered_results.append(item)
            if len(filtered_results) > 0:
                final_results += filtered_results

            files_counter += self.batch_size
            nb_of_articles_left -= self.batch_size

        return final_results

    async def scan_one_article(self, file_name: str, query_function):
        article_data = None
        with open(f"{self.src_data_path}/{file_name}", "r") as file_handle:
            article_data = json.load(file_handle)

        return query_function(article_data)

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


class DataLoader:
    def __init__(self, limit: int = -1, use_tokenized=False, data_path="") -> None:
        self.use_tokenized = use_tokenized
        if data_path == "":
            if use_tokenized:
                self.src_data_path = CONFIG["DIR_PATH"]["TOKENIZED_DIR"]
            else:
                self.src_data_path = CONFIG["DIR_PATH"]["SRC_DIR"]
        else:
            self.src_data_path = data_path

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
        print(f"exc_type: {exc_type}")
        print(f"exc_value: {exc_value}")
        print(f"exc_traceback: {exc_traceback}")
        print("Exited the DataLoader")
        return True

    def _load_files_iterator(self):
        for file_index, file_name in enumerate(
            tqdm.tqdm(self.clean_file_names, desc="Processing files", colour="green")
        ):
            # if file_index < 1035700:
            #     continue
            try:
                article_data = json.load(open(f"{self.src_data_path}/{file_name}", "r"))
            except:
                # print("corrupt file")
                os.remove(f"{self.src_data_path}/{file_name}")
                continue

            article_data["file_name"] = file_name
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
                    if file_counter >= self.limit:
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


def check_file_for_content(file_contents: dict):
    """
    Check if the file has proper contents. A damage/corruption can happen due to server problems, connection problems, interruption in the scrapping process, ....etc.
    STATUS: NOT-TESTED
    """
    if len(file_contents["article_content"]["content"]) == 0:  # Corrupted content
        return False
    else:  # Good content
        return True
