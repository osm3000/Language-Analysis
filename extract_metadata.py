"""
I want to extract the following:
1. The date
2. The topic/category to which this article belongs
Those two I will extract mainly from the URL.
"""
import json
import os

SRC_DIR = "./data_3"
TGT_DIR = "./data_4"


def main():
    file_names = os.listdir(SRC_DIR)
    all_topics = {}

    for file_index, file_name in enumerate(file_names):
        # if file_index >= 100:
        #     break
        # if file_index <= 11049:
        # continue
        # print("/-/" * 20)

        if (file_name != "all_links_recorded.json") and (
            file_name != "all_topic_collected.json"
        ):
            print(file_index, " -->> ", file_name)
            article_data = json.load(open(f"{SRC_DIR}/{file_name}", "r"))
            article_url = article_data["article_link"]
            article_url_split = article_url.split("/")

            article_url_topic = article_url_split[3]
            article_url_date = article_url_split[5:8]

            # print(f"Whole URL: {article_url}")
            # print(f"Category: {article_url_topic}")
            # print(f"Date: {article_url_date}")

            try:
                all_topics[article_url_topic] += 1
            except:
                all_topics[article_url_topic] = 1

            article_data["topic_category"] = article_url_topic
            try:  # There can be very rare case, where it is not really an article, thus, doesn't follow the normal schema
                article_data["publication_date"] = {
                    "year": article_url_date[0],
                    "month": article_url_date[1],
                    "day": article_url_date[2],
                }
            except:
                print("not a good article")
                continue

            json.dump(article_data, open(f"{TGT_DIR}/{file_name}", "w"))

    json.dump(all_topics, open(f"{TGT_DIR}/all_topic_collected.json", "w"))
    print(f"Nb of unique topics: {len(all_topics.keys())}")
    for item in all_topics:
        print(f"{item} -->> {all_topics[item]}")


if __name__ == "__main__":
    main()