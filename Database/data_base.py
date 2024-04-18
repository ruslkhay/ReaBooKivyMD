"""Module for handling flesh-cards storage."""

import sqlite3 as sql
from os import chdir

chdir('Database')

con = sql.connect("content.db")
cur = con.cursor()


def db_init():
    """Make necessary tables for database."""
    with open("schema.sql") as f:
        cur.executescript(f.read())


def dummy_insert(word=None, translation=None):
    """Insert, used only for one-to-one, non-repeated input."""
    if not isinstance(word, str) and not isinstance(translation, str):
        raise ValueError(
            'only one word and one translation. '
            + f"Got {word} with len{len(word)} and {translation}")
    else:
        query = """
            INSERT INTO "dictionary"("word", "meaning")
            VALUES (?, ?)
            """
    cur.execute(query, [word, translation])
    con.commit()  # saving database manipulations above


def delete_word(word=None, translation=None):
    """Remove word out of a database."""
    pass

# def insert_data(word=None, translations=None):
#     """Insert new data into two tables below."""
#     from re import split
#     separate_trans = split('[,.;\\/]', translations)
#     trans = list(map(str.strip, separate_trans)) # remove whitespaces
#     print(word)

#     # Insert new 'foreign' word
#     query = """
#         INSERT INTO "words"("name")
#         VALUES (?)
#         """
#     cur.execute(query, [word])

#     # Getting current (MAX) id for words table
#     query = """
#             SELECT "id" FROM "words"
#             WHERE "name" = (?);
#             """
#     word_id = cur.execute(query, [word]).fetchall()[0][0]
#     print(word_id)
#     # Insert new word's translation
#     for tran in trans:
#         query = """
#             INSERT INTO "translations"("meaning")
#             VALUES (?);
#             """
#         cur.execute(query, [tran])

#     # # Getting current (MAX) id for translations table
#     # query = """
#     #         SELECT "id" FROM "translations"
#     #         WHERE "name" = (?);
#     #         """
#     # word_id = cur.execute(query, [word]).fetchall()[0][0]
#     # for i in range(3):
#     #     query = """
#     #         INSERT INTO "translate"("word_id", "translation_id")
#     #         VALUES (?,?);
#     #         """
#     #     cur.execute(query, (word_id, i+1))

#     con.commit()  # saving database manipulations above


def read_data() -> dict:
    """Return content of a database."""
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
    dictionary = cur.execute(""" SELECT * FROM "dictionary";""").fetchall()
    return dictionary


if __name__ == "__main__":
    (db_init())
    dummy_insert(word='race', translation="гонка")
    # cur.execute("""DELETE FROM "words" WHERE "name" = 'spring'; """)
    print(run_process())
