from html import entities
from pydoc_data.topics import topics
from turtle import color
import spacy
from spacy.lang.fr.examples import sentences
import json
import os
import numpy as np
import pandas as pd
from os import path
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import configparser
import tqdm
import logging

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
nlp = None


def prepare_words_to_store(unique_words: dict) -> pd.DataFrame:
    """
    Perform some organization for the list of words, since this is a final product in itself.
    """
    df = pd.DataFrame()
    df["words"] = [word for word in unique_words]
    df["occurrences"] = [unique_words[word] for word in unique_words]
    df["frequency"] = df["occurrences"] * 100 / df["occurrences"].sum()
    df.sort_values(by="occurrences", ascending=False, inplace=True)

    return df


def clean_word(word: str) -> str:
    """
    This part is based on visual investigation of the output words.
    """
    if word in ["-", "’", "–", "−"]:
        return ""

    word = word.lower()
    word = word.replace("-", "").replace("–", "").replace("”", "")

    if len(word) > 0:
        if (word[-1] == "’") or (word[-1] == "'"):
            word = word.replace("’", "e")
            word = word.replace("'", "e")
    return word


def get_words_from_article(article_text):
    doc = nlp(article_text)

    words = {}
    verbs = {}
    nouns = {}
    adverbs = {}
    entities = {}

    for entity in doc.ents:
        try:
            entities[entity.label_][entity.text.lower()] += 1
        except:
            try:
                entities[entity.label_][entity.text.lower()] = 1
            except:
                entities[entity.label_] = {entity.text.lower(): 1}

    for token in doc:
        if token.pos_ in ["SPACE", "PUNCT", "NUM", "SYM", "ADP", "DET"]:
            continue

        # Perform extract cleaning on the word
        final_token = clean_word(token.lemma_)
        if len(final_token) == 0:
            continue

        if token.pos_ in ["VERB"]:
            try:
                verbs[final_token] += 1
            except:
                verbs[final_token] = 1

        if token.pos_ in ["NOUN"]:
            try:
                nouns[final_token] += 1
            except:
                nouns[final_token] = 1

        if token.pos_ in ["ADV"]:
            try:
                adverbs[final_token] += 1
            except:
                adverbs[final_token] = 1

        try:
            words[final_token] += 1
        except:
            words[final_token] = 1
        # all_words.append(final_token)
    # return words, " ".join(all_words)
    return words, verbs, nouns, adverbs, entities


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


def load_one_article(article_data):
    article_main_text = (
        article_data["article_content"]["title"]
        + " "
        + article_data["article_content"]["description"]
        + " "
        + article_data["article_content"]["content"]
    )

    all_words, verbs, nouns, adverbs, entities = get_words_from_article(
        article_main_text
    )
    return all_words, verbs, nouns, adverbs, entities


def get_articles(directory):
    file_names = os.listdir(directory)
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

    for file_index, file_name in enumerate(
        tqdm.tqdm(file_names, desc="Processing files", colour="green")
    ):
        # if file_index >= 1000:
        #     break
        if (file_name != "all_links_recorded.json") and (
            file_name != "all_topic_collected.json"
        ):
            article_insertion_speed = 0
            article_data = json.load(open(f"{directory}/{file_name}", "r"))
            if apply_filter_value(article_data, filters=FILTERS):
                if file_index % 500 == 0:
                    logging.info("%s files are done", file_index)
                # logging.info("Processing file: %s, %s", file_index, file_name)
                nb_of_articles += 1
                all_words, verbs, nouns, adverbs, entities = load_one_article(
                    article_data
                )

                for new_entity_label in entities:
                    if new_entity_label not in all_entities:
                        all_entities[new_entity_label] = {}

                    for new_entity_txt in entities[new_entity_label]:
                        try:
                            all_entities[new_entity_label][new_entity_txt] += entities[
                                new_entity_label
                            ][new_entity_txt]
                        except:
                            all_entities[new_entity_label][new_entity_txt] = entities[
                                new_entity_label
                            ][new_entity_txt]

                for new_word in all_words:
                    try:
                        all_new_words[new_word] += all_words[new_word]
                    except:
                        all_new_words[new_word] = all_words[new_word]
                        article_insertion_speed += 1
                    total_number_of_words += all_words[new_word]

                for new_word in verbs:
                    try:
                        all_verbs[new_word] += verbs[new_word]
                    except:
                        all_verbs[new_word] = verbs[new_word]

                for new_word in nouns:
                    try:
                        all_nouns[new_word] += nouns[new_word]
                    except:
                        all_nouns[new_word] = nouns[new_word]

                for new_word in adverbs:
                    try:
                        all_adverbs[new_word] += adverbs[new_word]
                    except:
                        all_adverbs[new_word] = adverbs[new_word]

                all_years.append(article_data["publication_date"]["year"])
                all_days.append(article_data["publication_date"]["day"])
                all_months.append(article_data["publication_date"]["month"])

                total_insertion_speed.append(article_insertion_speed)

        # return all_words

    # print(f"Insertion speeds: {total_insertion_speed}")
    logging.info("Nb of total words seen so far: %s", total_number_of_words)
    logging.info("Nb of unique words seen so far: %s", len(all_new_words.keys()))
    logging.info("Nb of unique verbs seen so far: %s", len(all_verbs.keys()))
    logging.info("Nb of unique nouns seen so far: %s", len(all_nouns.keys()))
    logging.info("Nb of unique adverbs seen so far: %s", len(all_adverbs.keys()))
    # print(f"Nb of unique entities seen so far: {len(all_entities.keys())}")

    log_file = {
        "total_insertion_speed": total_insertion_speed,
        "total_number_of_words": total_number_of_words,
        "all_years": all_years,
        "all_months": all_months,
        "all_days": all_days,
        "entities": all_entities,
    }

    json.dump(log_file, open(f"{TGT_DIR}/{FILTER_DIR}/logs.json", "w"))

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
    prepare_words_to_store(words_dict).to_csv(
        f"{TGT_DIR}/{FILTER_DIR}/{file_name}.csv", index=False
    )
    logging.info("Stored clean words - %s", file_name)


def draw_insertion_speed(insertion_speeds_list: list):
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
        FILTER_DIR += "-".join(parse_single_filter_list(filters[item])) + "_"
    FILTER_DIR = FILTER_DIR[:-1]  # to remove the last '-' from the code
    if FILTER_DIR == "":
        FILTER_DIR = "noFilter"
    try:
        os.mkdir(f"{TGT_DIR}/{FILTER_DIR}")
    except Exception as e:
        logging.warning("COULDN'T MAKE DIRECTORY --- %s", e)

    logging.info("Filter configuration: %s", FILTER_DIR)

    return FILTER_DIR


def main():
    logging.info("/*" * 20)
    logging.info("/*" * 20)
    logging.info("Fresh new run")
    form_results_folder_name(filters=FILTERS)
    get_articles(SRC_DIR)


if __name__ == "__main__":
    nlp = spacy.load(config["SPACY_PARAM"]["LANG_MODEL"])
    main()
