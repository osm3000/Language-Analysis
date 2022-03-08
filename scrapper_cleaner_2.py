"""
TODO: 
I want to restructure this in a much cleaner way to include:
* Use asyncio/threads in order to perform the requests
* Wrap the code for LeMonde alone (I want to get the data from other sources as well)
* Store the whole articles, with the relevant metadata.
* Extract the dates of the articles as well
"""
# from typing import final
from ntpath import join
import requests
from bs4 import BeautifulSoup
import json
import asyncio
import uuid
import configparser

SECRETS = configparser.ConfigParser()
SECRETS.read("./config/auth_lemonde.ini")

GET_FRESH = True
# GET_FRESH = False
DIRECTORY = "./data_4"
all_type_of_links = {
    "articles_pages": {
        "https://www.lemonde.fr/sciences/",
        "https://www.lemonde.fr/sciences/2/",
        "https://www.lemonde.fr/idees/",
        "https://www.lemonde.fr/idees/2/",
        "https://www.lemonde.fr/societe/",
        "https://www.lemonde.fr/societe/2/",
        "https://www.lemonde.fr/planete/",
        "https://www.lemonde.fr/planete/2/",
        "https://www.lemonde.fr/politique/",
        "https://www.lemonde.fr/politique/2/",
        "https://www.lemonde.fr/election-presidentielle-2022/",
        "https://www.lemonde.fr/election-presidentielle-2022/2/",
        "https://www.lemonde.fr/politique/",
        "https://www.lemonde.fr/politique/2/",
        # New topics
        "https://www.lemonde.fr/medecine/",
        "https://www.lemonde.fr/medecine/2/",
        "https://www.lemonde.fr/sante/",
        "https://www.lemonde.fr/sante/2/",
        "https://www.lemonde.fr/campus/",
        "https://www.lemonde.fr/campus/2/",
        "https://www.lemonde.fr/economie/",
        "https://www.lemonde.fr/economie/2/",
        "https://www.lemonde.fr/emploi/",
        "https://www.lemonde.fr/emploi/2/",
        "https://www.lemonde.fr/mathematiques/",
        "https://www.lemonde.fr/mathematiques/2/",
        "https://www.lemonde.fr/cosmos/",
        "https://www.lemonde.fr/cosmos/2/",
        "https://www.lemonde.fr/afrique/",
        "https://www.lemonde.fr/afrique/2/",
        "https://www.lemonde.fr/culture/",
        "https://www.lemonde.fr/culture/2/",
        "https://www.lemonde.fr/election-presidentielle-2012/",
        "https://www.lemonde.fr/election-presidentielle-2012/2/",
        "https://www.lemonde.fr/election-presidentielle-2017/",
        "https://www.lemonde.fr/election-presidentielle-2017/2/",
        "https://www.lemonde.fr/le-monde-des-religions/",
        "https://www.lemonde.fr/le-monde-des-religions/2/",
    },  # pages with articles inside
    "articles_links": set(),
}

seen_articles_pages = set()
seen_articles_links = set()
# URL = "https://www.lemonde.fr/sciences/"
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, "html.parser")

# print(soup.title)

sess = None


async def get_article_content(article_url):
    global sess
    # page = requests.get(article_url)
    print(f"Before the get: {article_url}")
    page = sess.get(article_url)
    # print(f"After the GET: {article_url}")
    soup = BeautifulSoup(page.content, "html.parser")
    # soup.str
    img_links = []
    img_captions = []
    all_href = []
    all_href_text = []
    # print(soup.find_all("figure"))
    for item in soup.find_all("figure"):
        # print(item)
        link = item.find("img")
        caption = item.find("figcaption")

        # print(caption.text)

        try:
            x = link["src"]
            y = caption.text
            img_links.append(x)
            img_captions.append(y)
        except:
            continue

    for item in soup.find_all("a"):
        try:
            x = item["href"]
            y = item.text
            all_href.append(x)
            all_href_text.append(y)
        except:
            continue

    title = ""
    try:
        title = soup.find("h1", class_="article__title").text
    except:
        title = ""

    author_name = ""
    try:
        author_name = soup.find("span", class_="author__name").text
    except:
        author_name = ""

    description = ""
    try:
        description = soup.find("p", class_="article__desc").text
    except:
        description = ""

    date = ""
    try:
        date = soup.find("span", class_="meta__date").text
    except:
        date = ""

    reading_time = ""
    try:
        reading_time = soup.find("p", class_="meta__reading-time").text
    except:
        reading_time = ""

    paragraphs = soup.find_all("p", class_="article__paragraph")

    content = ""
    for para in paragraphs:
        content += para.text + "\n"

    article_content = {
        "title": title,
        "author_name": author_name,
        "description": description,
        "content": content,
        "date": date,
        "reading_time": reading_time,
    }

    other_articles_titles = []
    other_articles_links = []
    other_articles_desc = []

    related_articles_links = soup.find_all("a", class_="teaser__link")
    related_articles_desc = soup.find_all("p", class_="teaser__desc")
    related_articles_titles = soup.find_all("span", class_="teaser__title")

    for item in related_articles_titles:
        print(item)
        other_articles_titles.append(item.text)

    for item in related_articles_desc:
        other_articles_desc.append(item.text)

    for item in related_articles_links:
        other_articles_links.append(item["href"])

    package = {
        "article_link": article_url,
        "all_href": all_href,
        "all_href_text": all_href_text,
        "img_links": img_links,
        "img_captions": img_captions,
        "article_content": article_content,
        "other_articles_mentioned": {
            "titles": other_articles_titles,
            "desc": other_articles_desc,
            "links": other_articles_links,
        },
    }

    return package


def get_article_links_in_the_page(page):
    all_links = page.find_all("a", class_="teaser__link")
    for link in all_links:
        # print(link.get("href"))
        all_type_of_links["articles_links"].add(link.get("href"))


def get_categories(page):
    all_category_links = page.find_all("a", class_="page__button")
    for link in all_category_links:
        # print(link.get("href"))
        all_type_of_links["articles_pages"].add(link.get("href"))
        all_type_of_links["articles_pages"].add(link.get("href") + "2")


async def main():
    # Get all possible article pages
    global all_type_of_links
    index = 0
    if GET_FRESH:
        while len(all_type_of_links["articles_pages"]) > 0:
            await asyncio.gather(
                *[
                    get_all_links_in_page(article_page)
                    for article_page in all_type_of_links["articles_pages"]
                ]
            )

            all_links_visited = True
            for link_0 in all_type_of_links["articles_pages"]:
                if link_0 not in seen_articles_pages:
                    all_links_visited = False
                    # print(f"Link: {link_0} was not seen")
            print(
                f'Current number of articles: {len(all_type_of_links["articles_links"])}'
            )
            print(f'What is left: {len(all_type_of_links["articles_pages"])}')
            print(f"What has been seen: {len(seen_articles_pages)}")
            print("-------------------------------------")

            if all_links_visited:
                break
    else:
        with open(f"{DIRECTORY}/all_links_recorded.json", "r") as file_handle:
            all_type_of_links = json.load(file_handle)

    all_type_of_links["articles_pages"] = list(all_type_of_links["articles_pages"])
    all_type_of_links["articles_links"] = list(all_type_of_links["articles_links"])
    # print(f"All collected links: {all_type_of_links['articles_links']}")

    with open(f"{DIRECTORY}/all_links_recorded.json", "w") as file_handle:
        json.dump(all_type_of_links, file_handle)

    await asyncio.gather(
        *[
            get_contents_of_articles(link_index, link)
            for link_index, link in enumerate(list(all_type_of_links["articles_links"]))
        ]
    )
    # for link_index, link in enumerate(list(all_type_of_links["articles_links"])):
    #     await get_contents_of_articles(link_index, link)
    # get_contents_of_articles()


async def get_all_links_in_page(article_page):
    global sess
    if article_page not in seen_articles_pages:
        seen_articles_pages.add(article_page)

        page = sess.get(article_page)

        soup = BeautifulSoup(page.content, "html.parser")

        get_article_links_in_the_page(soup)

        get_categories(soup)


async def get_contents_of_articles(articles_index, articles_link):
    # Get all articles content

    if articles_link not in seen_articles_links:
        seen_articles_links.add(articles_link)

        # print(articles_link)
        print(
            f"Article Index: {articles_index} / {len(all_type_of_links['articles_links'])}"
        )
        article_content = await get_article_content(articles_link)
        with open(f"{DIRECTORY}/{articles_index}.json", "w") as file_handle:
            json.dump(
                article_content,
                file_handle,
            )

        print("/*" * 50)


if __name__ == "__main__":
    payload = {
        "email": SECRETS["AUTH"]["email"],
        "password": SECRETS["AUTH"]["password"],
    }

    sess = requests.Session()
    res = sess.get("https://secure.lemonde.fr/sfuser/connexion")
    signin = BeautifulSoup(res._content, "html.parser")
    # payload['csrf_token'] = signin.find('input', id='csrf_token')['value']
    # print(signin.text)
    # print("/*-" * 100)
    res = sess.post("https://secure.lemonde.fr/sfuser/connexion", data=payload)

    success = BeautifulSoup(res._content, "html.parser")
    # print(success.text)
    try:
        asyncio.run(main())
    except:
        pass
    sess.close()