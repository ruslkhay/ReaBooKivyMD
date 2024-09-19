"""Module for handling flash-cards storage."""
from typing import List, Tuple, Any
from sqlite3 import connect, IntegrityError, Row


class DataBase:
    """Class for handling flash-cards storage."""

    def __init__(self, name="content", path="", schema=None) -> None:
        """Create connection to database and use given schema id given."""
        from os.path import join

        self.name = name
        self.connect = connect(join(path, name) + ".db")
        self.cursor = self.connect.cursor()

        # Make necessary tables for database.
        if schema:
            with open(schema) as f:
                self.cursor.executescript(f.read())

    def close(self) -> None:
        """Close connection to database."""
        self.connect.close()

    def delete_all(self) -> None:
        """Delete all from database.

        `dictionary` table is a parent for all others, so we can clear only it."""
        self.cursor.execute("""DELETE FROM dictionary;""")
        self.connect.commit()

    def select_from(
        self, table: str, cols: str = "*", cond: str = ""
    ) -> List[Tuple[Any]]:
        """Query analog of 'SELECT cols FROM table;'."""
        table_content = self.cursor.execute(f""" SELECT {cols} FROM {table} {cond}""")
        return table_content.fetchall()

    def select_to_dicts(self, select_query):
        """Returns data from an SQL query as a list of dicts."""
        try:
            self.connect.row_factory = Row
            things = self.connect.execute(select_query).fetchall()
            unpacked = [{k: item[k] for k in item.keys()} for item in things]
            return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
            return []

    def insert(self, table: str, values: dict) -> None:
        """Insert values into given table of database."""
        cols = str(list(values.keys()))[1:-1]
        vals = str(list(values.values()))[1:-1]
        query = f"""
            INSERT INTO {table}({cols})
            VALUES ({vals});"""
        try:
            self.cursor.execute(query)
            self.connect.commit()  # saving database manipulations above
        except IntegrityError as err:
            message: str = err.args[0]
            match message.rsplit(" ")[0]:
                case "UNIQUE":
                    raise ValueError(
                        f'{err.args[0]}\nValues {values} are already in "{table}"'
                    )
                case "FOREIGN":
                    raise ValueError(
                        f"{err.args[0]}\nThere is no {values} in parent table {table}"
                    )
                case _:
                    print(err.args)

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

    def hard_delete(self, table: str, id: int) -> None:
        """Hard remove from database table.

        Data can't be restored.
        """
        match table:
            case "content":
                id_name = "card_id"
            case "dictionary":
                id_name = "id"

        query = f"""
        DELETE FROM {table}
        WHERE {id_name} = {id};
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
