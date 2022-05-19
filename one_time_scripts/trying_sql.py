import sqlite3
import json
import os

with sqlite3.connect("mydatabase.db") as db_conn:
    # db_conn.execute("CREATE TABLE Student (id, age)")
    # db_conn.commit()

    # for i in range(10):
    #     db_conn.execute("insert into Student (?, ?)", i, i * 10)

    # xx = db_conn.execute("UPDATE Student SET id = '5' where age='50'")
    cursor = db_conn.execute("SELECT * FROM Student")
    for row in cursor:
        print(row)

    # db_conn.commit()
    # print("Total number of rows updated :", db_conn.total_changes)
    # db_conn.

    cursor.fetchall()