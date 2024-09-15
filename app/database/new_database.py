"""Module for handling flash-cards storage."""
from typing import List, Tuple, Any


class DataBase:
    """Class for handling flash-cards storage."""

    def __init__(self, name="content", path="", schema=None) -> None:
        """Create connection to database and use given schema id given."""
        from sqlite3 import connect
        from os.path import join

        self.connect = connect(join(path, name) + ".db")
        self.cursor = self.connect.cursor()

        # Make necessary tables for database.
        if schema:
            with open(schema) as f:
                self.cursor.executescript(f.read())

    def close(self) -> None:
        """Close connection to database."""
        self.connect.close()

    def select_from(
        self, table: str, cols: str = "*", cond: str = ""
    ) -> List[Tuple[Any]]:
        """Query analog of 'SELECT cols FROM table;'."""
        table_content = self.cursor.execute(f""" SELECT {cols} FROM {table} {cond}""")
        return table_content.fetchall()

    def insert(self, table: str, values: dict) -> None:
        """Insert values into given table of database."""
        cols = str(list(values.keys()))[1:-1]
        vals = str(list(values.values()))[1:-1]
        query = f"""
            INSERT INTO {table}({cols})
            VALUES ({vals});"""
        self.cursor.execute(query)
        self.connect.commit()  # saving database manipulations above

    def search(self, pattern: str = "") -> Tuple[int]:
        """Search flashcard matching pattern.

        Check pattern for flashcard's word and meaning simultaneously.
        If for one of this fields is matching then corresponding card id is
        returned.
        """
        pat = "'%{}%'".format(pattern)
        query = f"""
            SELECT "card_id"
            FROM "content"
            WHERE "word" LIKE {pat} or "meaning" LIKE {pat};
            """
        self.cursor.execute(query)

        return tuple(map(lambda x: x[0], self.cursor.fetchall()))

    def hard_delete(self, card_id: int) -> None:
        """Clear remove of flashcard from database.

        Data can't be restored.
        """
        query = f"""
        DELETE FROM content
        WHERE card_id = {card_id};
        """
        self.cursor.execute(query)
        self.connect.commit()

    def update(self, card_id: int, values: dict) -> None:
        """Update values of specific flashcard."""
        vals = list(map(lambda x: f'"{x[0]}" = "{x[1]}"', values.items()))
        vals = ", ".join(vals)
        print((vals))
        query = f"""
            UPDATE content
            SET {vals}
            WHERE card_id = {card_id};
        """
        self.cursor.execute(query)
        self.connect.commit()


if __name__ == "__main__":
    db = DataBase(name="new_content", path="Database", schema="Database/new_schema.sql")
    # db.insert("content", {"id_dict": 0, "word": "hello", "meaning": "привет"})
    # db.insert("content", {"id_dict": 0, "word": "world", "meaning": "мир"})
    # db.insert("content", {"id_dict": 0, "word": "I", "meaning": "я"})
    # db.insert("content", {"id_dict": 0, "word": "am", "meaning": ""})
    # db.insert("content", {"id_dict": 0, "word": "in", "meaning": "в"})
    # db.insert("content", {"id_dict": 0, "word": "airport", "meaning": "аэропорт"})
    print(db.select_from(table="content"))
    print(db.search(pattern="h"))
    print(db.search())
    print(db.search(pattern="и"))
    print(db.search(pattern="a"))
    db.update(
        card_id=3,
        values={
            "example": "I wrote few examples for future generation",
            "meaning": "Я",
        },
    )

    # db.hard_delete(card_id=1)
    print(db.select_from(table="content"))
