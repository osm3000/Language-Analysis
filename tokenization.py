"""
Perform some basic analysis over the articles
"""
import logging
import configparser
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import utilities
import tokenizer

config = configparser.ConfigParser()
config.read("./config/config.ini")

logging.basicConfig(
    filename=f"{config['DIR_PATH']['LOG_DIR']}/tokenization.log",
    format="%(levelname)s:%(funcName)s:%(asctime)s:%(message)s",
    level=logging.INFO,
)


FILTERS = dict(config["FILTERS"])

SRC_DIR = config["DIR_PATH"]["SRC_DIR"]
TGT_DIR = config["DIR_PATH"]["TGT_DIR"]
FILTER_DIR = ""


def prepare_words_to_store(unique_words: dict) -> pd.DataFrame:
    """
    Perform some organization for the list of words, since this is a final product in itself.
    """
    data_frame = pd.DataFrame()
    data_frame["words"] = list(unique_words)
    data_frame["occurrences"] = [unique_words[word] for word in unique_words]
    data_frame["frequency"] = (
        data_frame["occurrences"] * 100 / data_frame["occurrences"].sum()
    )
    data_frame.sort_values(by="occurrences", ascending=False, inplace=True)

    return data_frame


def get_articles():
    """
    The main loop over each article, to filter it and tokenize the words.
    """
    all_new_words = {}

    all_verbs = {}
    all_nouns = {}
    all_adverbs = {}
    all_entities = {}

    all_years = []
    all_months = []
    all_days = []

    nb_of_articles = 0

    total_insertion_speed = []  # How many new words each article add?

    total_number_of_words = 0

    word_tokenizer = tokenizer.Spacy_Tokenizer()

    with utilities.DataLoader(limit=-1) as data_handler:
        for file_index, article_data in enumerate(data_handler):
            article_insertion_speed = 0
            if utilities.apply_filter_value(article_data, filters=FILTERS):
                if file_index % 500 == 0:
                    logging.info("%s files are done", file_index)
                # logging.info("Processing file: %s, %s", file_index, file_name)
                nb_of_articles += 1
                (
                    all_words,
                    verbs,
                    nouns,
                    adverbs,
                    entities,
                ) = word_tokenizer(article_data)

                for new_entity_label in entities:
                    if new_entity_label not in all_entities:
                        all_entities[new_entity_label] = {}

                    for new_entity_txt in entities[new_entity_label]:
                        try:
                            all_entities[new_entity_label][new_entity_txt] += entities[
                                new_entity_label
                            ][new_entity_txt]
                        except KeyError:
                            all_entities[new_entity_label][new_entity_txt] = entities[
                                new_entity_label
                            ][new_entity_txt]

                for new_word in all_words:
                    try:
                        all_new_words[new_word] += all_words[new_word]
                    except KeyError:
                        all_new_words[new_word] = all_words[new_word]
                        article_insertion_speed += 1
                    total_number_of_words += all_words[new_word]

                for new_word in verbs:
                    try:
                        all_verbs[new_word] += verbs[new_word]
                    except KeyError:
                        all_verbs[new_word] = verbs[new_word]

                for new_word in nouns:
                    try:
                        all_nouns[new_word] += nouns[new_word]
                    except KeyError:
                        all_nouns[new_word] = nouns[new_word]

                for new_word in adverbs:
                    try:
                        all_adverbs[new_word] += adverbs[new_word]
                    except KeyError:
                        all_adverbs[new_word] = adverbs[new_word]

                all_years.append(article_data["publication_date"]["year"])
                all_days.append(article_data["publication_date"]["day"])
                all_months.append(article_data["publication_date"]["month"])

                total_insertion_speed.append(article_insertion_speed)

    # print(f"Insertion speeds: {total_insertion_speed}")
    logging.info("Nb of total words seen so far: %s", total_number_of_words)
    logging.info("Nb of unique words seen so far: %s", len(all_new_words))
    logging.info("Nb of unique verbs seen so far: %s", len(all_verbs))
    logging.info("Nb of unique nouns seen so far: %s", len(all_nouns))
    logging.info("Nb of unique adverbs seen so far: %s", len(all_adverbs))
    # print(f"Nb of unique entities seen so far: {len(all_entities)}")
    # exit()
    log_file = {
        "total_insertion_speed": total_insertion_speed,
        "total_number_of_words": total_number_of_words,
        "all_years": all_years,
        "all_months": all_months,
        "all_days": all_days,
        "entities": all_entities,
    }

    with open(f"{TGT_DIR}/{FILTER_DIR}/logs.json", "w") as file_handle:
        json.dump(log_file, file_handle)

    clean_all_new_words_df = prepare_words_to_store(all_new_words)
    clean_all_new_words_df.to_csv(
        f"{TGT_DIR}/{FILTER_DIR}/unique_words.csv", index=False
    )
    clean_and_store_word_dictionaries(all_new_words, "allWords")
    clean_and_store_word_dictionaries(all_nouns, "allNouns")
    clean_and_store_word_dictionaries(all_verbs, "allVerbs")
    clean_and_store_word_dictionaries(all_adverbs, "allAdverbs")

    draw_insertion_speed(total_insertion_speed)
    draw_word_cloud(all_new_words, "allWords")
    draw_word_cloud(all_nouns, "allNouns")
    draw_word_cloud(all_verbs, "allVerbs")
    draw_word_cloud(all_adverbs, "allAdverbs")
    for entity in all_entities:
        draw_word_cloud(all_entities[entity], f"allEnts_{entity}")


def clean_and_store_word_dictionaries(words_dict: dict, file_name: str) -> None:
    """
    Remove
    """
    prepare_words_to_store(words_dict).to_csv(
        f"{TGT_DIR}/{FILTER_DIR}/{file_name}.csv", index=False
    )
    logging.info("Stored clean words - %s", file_name)


def draw_insertion_speed(insertion_speeds_list: list):
    """
    A function to draw the insertion speed -> how each article contribute
    to the knowledge of new words.
    """
    # insertion_speeds_np = np.sort(np.array(insertion_speeds_list))[::-1]
    insertion_speeds_np = np.array(insertion_speeds_list)
    # plt.figure()
    plt.figure(figsize=(20, 10))
    plt.title("Insertion Speed - Not ordered")
    plt.rc("font", size=20)  # controls default text size
    plt.plot(np.arange(insertion_speeds_np.shape[0]), insertion_speeds_np)
    plt.xlabel("Articles")
    plt.ylabel("Number of new words")
    plt.savefig(f"./{TGT_DIR}/{FILTER_DIR}/insertionSpeedNOTOrdered.png")

    insertion_speeds_np = np.sort(np.array(insertion_speeds_list))[::-1]
    # plt.figure()
    plt.figure(figsize=(20, 10))
    plt.title("Insertion Speed - Ordered")
    plt.rc("font", size=20)  # controls default text size

    plt.plot(np.arange(insertion_speeds_np.shape[0]), insertion_speeds_np)
    plt.xlabel("Articles")
    plt.ylabel("Number of new words")
    # plt.hist(insertion_speeds_np)
    plt.savefig(f"./{TGT_DIR}/{FILTER_DIR}/insertionSpeedOrdered.png")
    logging.info("Insertion Graph speed is done")


def draw_word_cloud(words_frequencies: dict, name: str):
    """
    A function to draw Word Clouds
    """
    wordcloud = WordCloud(
        max_words=1000, background_color="white", width=1000, height=1000
    )

    # wordcloud.generate_from_frequencies(all_new_words)
    wordcloud.generate_from_frequencies(words_frequencies)

    plt.figure(figsize=(50, 50))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f"{TGT_DIR}/{FILTER_DIR}/wordCloud_{name}.png")

    logging.info("Word cloud for %s is DONE", name)


def form_results_folder_name(filters: dict):
    """
    It will be ./results/<filter query join>
    I will assume the filter is a single query
    Make this directory
    """
    global FILTER_DIR
    FILTER_DIR = ""
    for item in filters:
        FILTER_DIR += "-".join(utilities.parse_single_filter_list(filters[item])) + "_"
    FILTER_DIR = FILTER_DIR[:-1]  # to remove the last '-' from the code
    if FILTER_DIR == "":
        FILTER_DIR = "no_filter"
    try:
        os.mkdir(f"{TGT_DIR}/{FILTER_DIR}")
    except OSError as exc:
        logging.warning("COULDN'T MAKE DIRECTORY --- %s", exc)

    logging.info("Filter configuration: %s", FILTER_DIR)

    return FILTER_DIR


def main():
    logging.info("/*" * 20)
    logging.info("/*" * 20)
    logging.info("Fresh new run")
    form_results_folder_name(filters=FILTERS)
    get_articles()


if __name__ == "__main__":
    main()
