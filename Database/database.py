"""Module for handling flash-cards storage."""
from typing import List, Tuple, Any


class DataBase:
    """Class for handling flash-cards storage."""

    def __init__(self, name='content', path='', schema=None) -> None:
        """Create connection to database and use given schema id given."""
        from sqlite3 import connect
        from os.path import join

        self.connect = connect(join(path, name) + '.db')
        self.cursor = self.connect.cursor()

        # Make necessary tables for database.
        if schema:
            with open(schema) as f:
                self.cursor.executescript(f.read())

    def close(self) -> None:
        """Close connection to database."""
        self.connect.close()

    def oto_insert(self, word: str = None, translation: str = None) -> None:
        """One-to-one insert, used only for non-repeated input."""
        query = """
            INSERT INTO "dictionary"("word", "meaning")
            VALUES (?, ?);
            """
        self.cursor.execute(query, [word, translation])
        self.connect.commit()  # saving database manipulations above

    def delete_word(self, word: str = None, translation: str = None) -> None:
        """Hide word out of a database. Mark it as deleted."""
        query = """
            DELETE FROM "dictionary"
            WHERE "word" = ? AND "meaning" = ?
            """
        self.cursor.execute(query, [word, translation])
        self.connect.commit()  # saving database manipulations above

    def select_from(self, table: str, cols: str = '*') -> List[Tuple[Any]]:
        """Query analog of 'SELECT cols FROM table;'."""
        table_content = self.cursor.execute(f""" SELECT {cols} FROM {table}""")
        return table_content.fetchall()
