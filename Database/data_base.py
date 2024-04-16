"""Module for handling flesh-cards storage."""

import sqlite3 as sql

con = sql.connect("Database/dictionary.db")
cur = con.cursor()


def db_init():
    """Make necessary tables for database."""
    query = """ CREATE TABLE IF NOT EXISTS
                dictionary(
                p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                initial_word TINYTEXT,
                translation TINYTEXT
                )
            """
    cur.execute(query)


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


def read_data():
    """Return list with database contents."""
    return cur.execute(""" SELECT * FROM dictionary""").fetchall()


def run_process():
    """Call all initial functions for creating database."""
    db_init()
    feed_data()
    return read_data()


if __name__ == "__main__":
    (run_process())
