"""
Given a data lake of articles, the objective is to transfer this data to my DB (FINALLY)
steps
1. Fix the timestamp
"""
import pymongo
import json
import utilities
from bson import BSON
import datetime

ARTICLES_DB = None
LEMONDE_COL = None


def extract_article_id(article_filename: str):
    """
    Just remove the .json at the end
    """
    return article_filename[:-5]


def transfer_one_article(article_content: dict):
    # article_content = BSON.encode(article_content)
    response = LEMONDE_COL.insert_one(article_content)
    return response


def fix_datetime(article_content: dict):
    """
    This is a one-time solution for now. To be incorporated later in the main pipeline of the articles
    """
    # print(article_content["publication_date"])
    # print(article_content["file_name"])
    # print(article_content["article_link"])
    # print("-/" * 50)
    year = int(article_content["publication_date"]["year"])
    month = int(article_content["publication_date"]["month"])
    day = int(article_content["publication_date"]["day"])
    article_content["publication_date"] = datetime.datetime(
        year=year, month=month, day=day
    )
    return article_content


def main():
    with utilities.DataLoader(data_path="./ALL_DATA_2") as data_loader:
        for article_content in data_loader:
            fixed_article_content = fix_datetime(article_content)
            fixed_article_content["_id"] = extract_article_id(
                fixed_article_content["file_name"]
            )

            if LEMONDE_COL.count_documents({"_id": fixed_article_content["_id"]}) > 0:
                print("Article seen before: ", fixed_article_content["_id"])
            else:
                response = transfer_one_article(article_content)

            # print(response.acknowledged, response.inserted_id)


if __name__ == "__main__":
    with pymongo.MongoClient("mongodb://10.100.74.70:27017/") as db_client:
        ARTICLES_DB = db_client["Articles"]
        LEMONDE_COL = ARTICLES_DB["lemonde"]
        main()