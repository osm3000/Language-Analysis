"""
Results:
1. First pass is slow. I don't know how much relative to pure sequential. But slow enough for me
2. Second pass is much faster! Is the data being kept in the cash/ram somewhere? I don't get it.
"""
from scrap_all_archive import main
import utilities
import asyncio
import time


def query(article_file: dict):
    # if "Russie".lower() in article_file["article_content"]["title"].lower():
    if "mentale".lower() in article_file["article_content"]["title"].lower():
        return (
            article_file["article_content"]["title"],
            article_file["article_link"].split("/")[-4],
        )
    # return article_file["article_content"]["title"]


# async def main():
async def main():
    # query_engine = utilities.AsyncDataQueries(limit=50000)
    query_engine = utilities.FunctionalDataQueries(limit=100000)
    # results = await query_engine.execute_query(query)
    results = query_engine.execute_query(query)
    for item in results:
        print(item)
    print(len(results))


if __name__ == "__main__":
    time_0 = time.time()
    asyncio.run(main())
    print(time.time() - time_0)
