import sqlite3
import utilities
import hashlib

with sqlite3.connect("mydatabase.db") as db_conn:
    cursor = db_conn.cursor()
    # cursor = db_conn.execute("SELECT * FROM Student")
    try:
        cursor.execute(
            """
        CREATE TABLE ARTICLES (
            ID TEXT,
            link TEXT, 
            title TEXT, 
            topic TEXT, 
            author TEXT, 
            description TEXT, 
            content TEXT, 
            year INTEGER, 
            month INTEGER, 
            day INTEGER)
            """
        )
    except:
        print("Table has already been created")
    bad_articles = 0
    with utilities.DataLoader() as data_loader:
        for article_index, article_file in enumerate(data_loader):
            try:
                if article_file["article_link"][-1] == "/":
                    article_file["article_link"] = article_file["article_link"][:-1]
                year = article_file["article_link"].split("/")[-4]
                month = article_file["article_link"].split("/")[-3]
                day = article_file["article_link"].split("/")[-2]
                id = hashlib.md5(article_file["article_link"].encode()).hexdigest()
                link = article_file["article_link"]
                topic = article_file["article_link"].split("/")[-6]
                title = article_file["article_content"]["title"]
                author_name = article_file["article_content"]["author_name"]
                description = article_file["article_content"]["description"]
                content = article_file["article_content"]["content"]

                # print(f"{id}, {link}, {title}, {topic}, {year}, {month}, {day}")

                cursor.execute(
                    f'insert into ARTICLES VALUES ("{id}", "{link}", "{title}", "{topic}", "{author_name}", "{description}", "{content}", {year}, {month}, {day})'
                )
            except:
                bad_articles += 1
                print(bad_articles)

    db_conn.commit()
