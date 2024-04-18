"""Module for handling flesh-cards storage."""

import sqlite3 as sql
from os import chdir

chdir('Database')

con = sql.connect("dictionary.db")
cur = con.cursor()


def db_init():
    """Make necessary tables for database."""
    with open("schema.sql") as f:
        cur.executescript(f.read())


def insert_data(word=None, translations=None):
    """Insert new data into two tables below."""
    from re import split
    separate_trans = split('[,.;\\/]', translations)
    trans = list(map(str.strip, separate_trans)) # remove whitespaces
    print(word)

    # Insert new 'foreign' word
    query = """
        INSERT INTO "words"("name")
        VALUES (?)
        """
    cur.execute(query, [word])

    # Getting current (MAX) id for words table
    query = """
            SELECT "id" FROM "words"
            WHERE "name" = (?);
            """
    word_id = cur.execute(query, [word]).fetchall()[0][0]
    print(word_id)
    # Insert new word's translation
    for tran in trans:
        query = """
            INSERT INTO "translations"("meaning")
            VALUES (?);
            """
        cur.execute(query, [tran])

    # # Getting current (MAX) id for translations table
    # query = """
    #         SELECT "id" FROM "translations"
    #         WHERE "name" = (?);
    #         """
    # word_id = cur.execute(query, [word]).fetchall()[0][0]
    for i in range(3):
        query = """
            INSERT INTO "translate"("word_id", "translation_id")
            VALUES (?,?);
            """
        cur.execute(query, (word_id, i+1))

    con.commit() # saving database manipulations above 


def feed_data():
    """Insert data into database."""
    dummy_dict = [
        ('apple', 'яблоко'),
        ('drug', 'лекарство'),
        ('think', 'думать')
    ]
    for elem in dummy_dict:
        query = """
                INSERT INTO dictionary(initial_word, translation)
                VALUES (?, ?)"""

        cur.execute(query, elem)

    # cur.commit()
    # con.commit()


def read_data() -> dict:
    """ """
    words = cur.execute(""" SELECT * FROM words""").fetchall()
    translations = cur.execute(""" SELECT * FROM translations""").fetchall()
    translate = cur.execute(""" SELECT * FROM translate""").fetchall()
    content = dict(words=words, 
                   translations=translations,
                   translate=translate)
    return content



def run_process():
    """Call all initial functions for creating database."""
    db_init()
    feed_data()
    return read_data()


if __name__ == "__main__":
    (db_init())
    insert_data(word='spring', translations="весна, прыгать;пружина")
    # cur.execute("""DELETE FROM "words" WHERE "name" = 'spring'; """)
    print(read_data())
