"""
I want to extract the following:
1. The date
2. The topic/category to which this article belongs
Those two I will extract mainly from the URL.

UPDATE: 21/04/22
I've remodified this code. Now it will do the following:
- Extract the metadata mentioned earlier
- Remove any weird articles (articles that don't have '.html' at the end of their url)
"""
import json
import os
import configurations
import utilities

CONFIG = configurations.get_config_file()


def main():
    file_names = os.listdir(CONFIG["DIR_PATH"]["SRC_DIR"])
    bad_articles = 0
    with utilities.DataLoader() as data_loader:
        for article_index, article_data in enumerate(data_loader):
            article_url = article_data["article_link"]
            file_name = article_data["file_name"]
            if article_url[-5:] != ".html":
                bad_articles += 1
                print(f"Bad article: {bad_articles}")
                continue
            try:
                article_url_split = article_url.split("/")

                article_url_topic = article_url_split[3]
                article_url_date = article_url_split[5:8]

                article_data["topic_category"] = article_url_topic
                article_data["publication_date"] = {
                    "year": article_url_date[0],
                    "month": article_url_date[1],
                    "day": article_url_date[2],
                }

                json.dump(
                    article_data,
                    open(f'{CONFIG["DIR_PATH"]["TGT_DIR"]}/{file_name}', "w"),
                )
            except Exception as e:
                print(e)
                print(file_name)
                print(article_url_split)
                bad_articles += 1
                print(f"Bad article: {bad_articles}")
                continue


if __name__ == "__main__":
    main()