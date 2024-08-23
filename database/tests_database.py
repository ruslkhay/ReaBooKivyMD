"""Tests for flash-cards database."""

import unittest
from .database import DataBase


class InsertTestCase(unittest.TestCase):
    """Tests for one-to-one insert for flash-card database."""

    def setUp(self):
        """Create dummy flash-card storage."""
        self.db_name = "test"
        self.db = DataBase(name=self.db_name, schema="Database/schema.sql")

    def test_insert(self):
        """Check if data is inserted right way for each table."""
        self.db.oto_insert(word="raise", translation="поднять")
        self.db.oto_insert(
            word="hop",
            translation="прыгать",
            example="Girl hopped from stone to stone.",
        )
        self.db.oto_insert(word="spring", translation="прыгать", image="some url-link")
        self.db.oto_insert(
            word="spring",
            translation="весна",
            example="Spring was warm.",
            image="picture's path",
        )

        self.assertEqual(
            self.db.select_from("words"), [(1, "raise"), (2, "hop"), (3, "spring")]
        )
        self.assertEqual(
            self.db.select_from("translations"),
            [(1, "поднять"), (2, "прыгать"), (3, "весна")],
        )
        self.assertEqual(
            self.db.select_from("dictionary"),
            [
                (1, "raise", "поднять", None, None),
                (2, "hop", "прыгать", "Girl hopped from stone to stone.", None),
                (3, "spring", "прыгать", None, "some url-link"),
                (4, "spring", "весна", "Spring was warm.", "picture's path"),
            ],
        )
        self.assertEqual(
            self.db.select_from("translate"),
            [
                (1, 1, 1, None, None, 0),
                (2, 2, 2, "Girl hopped from stone to stone.", None, 0),
                (3, 3, 2, None, "some url-link", 0),
                (4, 3, 3, "Spring was warm.", "picture's path", 0),
            ],
        )

    def tearDown(self):
        """Remove storage and close connection to database."""
        from os import remove

        self.db.close()
        remove(self.db_name + ".db")


class DeleteTestCase(unittest.TestCase):
    """Tests for deleting content out of flash-card database."""

    def setUp(self):
        """Create filled flash-card storage."""
        self.db_name = "test"
        self.db = DataBase(name=self.db_name, schema="Database/schema.sql")

        self.db.oto_insert(word="raise", translation="поднять")
        self.db.oto_insert(
            word="hop",
            translation="прыгать",
            example="Girl hopped from stone to stone.",
        )
        self.db.oto_insert(word="spring", translation="прыгать", image="some url-link")
        self.db.oto_insert(
            word="spring",
            translation="весна",
            example="Spring was warm.",
            image="picture's path",
        )

    def test_hard_delete_0(self):
        """Delete unique word and unique translation.

        Delete from dictionary one row, where word is not used in another row
        and translation is also not used in another row.
        """
        self.db.delete_word("raise", "поднять")

        self.assertNotIn((1, "raise"), self.db.select_from("words"))
        self.assertNotIn((1, "поднять"), self.db.select_from("translations"))
        self.assertNotIn(
            ("raise", "поднять", None, None), self.db.select_from("dictionary")
        )

        self.assertEqual(self.db.select_from("words"), [(2, "hop"), (3, "spring")])
        self.assertEqual(
            self.db.select_from("translations"), [(2, "прыгать"), (3, "весна")]
        )
        self.assertEqual(
            self.db.select_from("dictionary"),
            [
                (2, "hop", "прыгать", "Girl hopped from stone to stone.", None),
                (3, "spring", "прыгать", None, "some url-link"),
                (4, "spring", "весна", "Spring was warm.", "picture's path"),
            ],
        )
        self.assertEqual(
            self.db.select_from("translate"),
            [
                (2, 2, 2, "Girl hopped from stone to stone.", None, 0),
                (3, 3, 2, None, "some url-link", 0),
                (4, 3, 3, "Spring was warm.", "picture's path", 0),
            ],
        )

    def test_hard_delete_1(self):
        """Delete not unique word and not unique translation.

        Delete from dictionary one row, where word is used in another row
        and translation is also used in another row.
        """
        self.db.delete_word("spring", "прыгать")

        self.assertEqual(
            self.db.select_from("words"), [(1, "raise"), (2, "hop"), (3, "spring")]
        )
        self.assertEqual(
            self.db.select_from("translations"),
            [(1, "поднять"), (2, "прыгать"), (3, "весна")],
        )
        self.assertEqual(
            self.db.select_from("dictionary"),
            [
                (1, "raise", "поднять", None, None),
                (2, "hop", "прыгать", "Girl hopped from stone to stone.", None),
                (4, "spring", "весна", "Spring was warm.", "picture's path"),
            ],
        )
        self.assertEqual(
            self.db.select_from("translate"),
            [
                (1, 1, 1, None, None, 0),
                (2, 2, 2, "Girl hopped from stone to stone.", None, 0),
                (4, 3, 3, "Spring was warm.", "picture's path", 0),
            ],
        )

    def test_hard_delete_2(self):
        """Delete unique word and not unique translation.

        Delete from dictionary one row, where word is not used in another row
        by translation is.
        """
        self.db.delete_word("hop", "прыгать")
        self.assertEqual(self.db.select_from("words"), [(1, "raise"), (3, "spring")])
        self.assertEqual(
            self.db.select_from("translations"),
            [(1, "поднять"), (2, "прыгать"), (3, "весна")],
        )
        self.assertEqual(
            self.db.select_from("dictionary"),
            [
                (1, "raise", "поднять", None, None),
                (3, "spring", "прыгать", None, "some url-link"),
                (4, "spring", "весна", "Spring was warm.", "picture's path"),
            ],
        )
        self.assertEqual(
            self.db.select_from("translate"),
            [
                (1, 1, 1, None, None, 0),
                (3, 3, 2, None, "some url-link", 0),
                (4, 3, 3, "Spring was warm.", "picture's path", 0),
            ],
        )

    def test_hard_delete_3(self):
        """Delete not unique word and unique translation.

        Delete from dictionary one row, where word is used in another row
        but translation is not.
        """
        self.db.delete_word("spring", "весна")
        self.assertEqual(
            self.db.select_from("words"), [(1, "raise"), (2, "hop"), (3, "spring")]
        )
        self.assertEqual(
            self.db.select_from("translations"), [(1, "поднять"), (2, "прыгать")]
        )
        self.assertEqual(
            self.db.select_from("dictionary"),
            [
                (1, "raise", "поднять", None, None),
                (2, "hop", "прыгать", "Girl hopped from stone to stone.", None),
                (3, "spring", "прыгать", None, "some url-link"),
            ],
        )
        self.assertEqual(
            self.db.select_from("translate"),
            [
                (1, 1, 1, None, None, 0),
                (2, 2, 2, "Girl hopped from stone to stone.", None, 0),
                (3, 3, 2, None, "some url-link", 0),
            ],
        )

    def tearDown(self):
        """Remove storage and close connection to database."""
        from os import remove

        self.db.close()
        remove(self.db_name + ".db")


def refreshed_content(database: DataBase):
    """Return new values out of tables after update."""

    def F(d: dict):
        def extract(x):
            for i, param in enumerate(d.keys()):
                d[param].append(x[i])

        return extract

    Dict = {"id": [], "word": [], "meaning": [], "example": [], "image": []}
    list(map(F(Dict), database.select_from("dictionary")))
    Word = {"id": [], "name": []}
    list(map(F(Word), database.select_from("words")))
    Tran = {"id": [], "meaning": []}
    list(map(F(Tran), database.select_from("translations")))
    return Dict, Word, Tran


def get_new_ids(db: DataBase, word: str, meaning: str):
    """Return first appropriate 'id'."""
    Ids = {"word": 0, "meaning": 0, "example": 0, "image": 0}
    Ids["example"] = db.select_from(
        "dictionary", "id", f"WHERE word = '{word}' AND meaning = '{meaning}'"
    )[0][0]
    Ids["image"] = Ids["example"]
    Ids["word"] = db.select_from("translations", "id", f"WHERE meaning = '{meaning}'")[
        0
    ][0]
    Ids["meaning"] = db.select_from("words", "id", f"WHERE name = '{word}'")[0][0]
    return Ids


class UpdateTestCase(unittest.TestCase):
    """Tests for updating content of flash-card's database.

    Test table contains 4 cards:
    1. Unique word + Unique translation,
    2. Unique word + Common translation,
    3. Common word + Common translation,
    4. Common word + Unique translation.

    For each of them exist specific tests, where all possible fields (and their
    combinations) are updated.
    """

    # Initial content of database
    OLD_CARDS = (
        ["raise", "поднять", None, None],
        ["hop", "прыгать", "Girl hopped from stone to stone.", None],
        ["spring", "прыгать", None, "some url-link"],
        ["spring", "весна", "Spring was warm.", "picture's path"],
    )
    # Updated content of database
    NEW_CARDS = (
        ["lift", "приподнимать", "Lift heavy bar", "bar's image"],
        ["bob", "скакать", None, "image's path"],
        ["bounce", "пружинить", "Walk with a bounce", "illustration"],
        ["autumn", "осень", None, None],
    )
    # Convert contents to `dict` type
    KEYS = [["word", "meaning", "example", "image"]]
    OLD_CARDS = list(map(dict, map(zip, KEYS * len(OLD_CARDS), OLD_CARDS)))
    NEW_CARDS = list(map(dict, map(zip, KEYS * len(NEW_CARDS), NEW_CARDS)))

    def setUp(self):
        """Create filled flash-card storage."""
        # Creating and connecting to database
        self.db_name = "test"
        self.db = DataBase(name=self.db_name, schema="Database/schema.sql")
        # Filling values. '*-u' = 'unique', '*-c' = 'common', 'X' = 'None'
        # 'W', 'T', 'E', 'I' - corresponding abbreviations
        self.db.oto_insert(*self.OLD_CARDS[0].values())  # W-u T-u X X
        self.db.oto_insert(*self.OLD_CARDS[1].values())  # W-u T-c E X
        self.db.oto_insert(*self.OLD_CARDS[2].values())  # W-c T-c X I
        self.db.oto_insert(*self.OLD_CARDS[3].values())  # W-c T-u E I

    def __prepare_cases(self, card_id: int):
        """Construct cases for testing database update option."""
        from itertools import combinations

        old_card = self.OLD_CARDS[card_id - 1]  # initial card
        upd_card = self.NEW_CARDS[card_id - 1]  # updated card
        # Create all possible input combinations
        for num_param in range(1, 1 + len(self.KEYS[0])):
            # Run update option for each of parameter's combinations
            for comb in combinations(list(upd_card.items()), num_param):
                params = dict(comb)
                self.tearDown()
                self.setUp()
                card = old_card.copy()
                card.update(params)
                # Target function (update option) call
                self.db.update_word(card_id, *card.values())
                # Extract new database data
                D, W, T = refreshed_content(self.db)
                ID = get_new_ids(self.db, card["word"], card["meaning"])
                yield D, W, T, ID, old_card, upd_card, params

    @staticmethod
    def multi_test(card_id: int):
        """Decorate test case call."""

        def inner_decor(func):
            """Enable argument input option for previous decorator."""
            import functools

            @functools.wraps(func)
            def wrapper(self: "UpdateTestCase"):
                """Run all subtests for given test case."""
                case = self.__prepare_cases(card_id)
                for args in case:
                    *res, params = args
                    with self.subTest(**params):
                        list(map(lambda x: func(self, x, *res), params.keys()))

            return wrapper

        return inner_decor

    # @unittest.skip
    @multi_test(card_id=1)
    def test_dec_check_1(
        self,
        key: str,
        Dict: dict,
        Word: dict,
        Tran: dict,
        newIds: tuple,
        old_card: dict,
        upd_card: dict,
    ):
        """Check update of card, with unique word and unique translation.

        Test database behavior, when all possible card's content updates are
        applied.
        """
        # Dictionary table should hold all updated values
        self.assertIn(upd_card[key], Dict[key])
        match key:
            case "word":
                # previous word shouldn't be in database
                self.assertNotIn(old_card[key], Word["name"])
                self.assertNotIn(old_card[key], Dict[key])
                # updated word must be in table
                self.assertIn(upd_card[key], Word["name"])
            case "meaning":
                # previous translation shouldn't be in database
                self.assertNotIn(old_card[key], Tran[key])
                self.assertNotIn(old_card[key], Dict[key])
                # updated translation must be in table
                self.assertIn(upd_card[key], Tran[key])
            case "example" | "image":
                self.assertNotIn(
                    (newIds[key], old_card[key]), list(zip(Dict["id"], Dict[key]))
                )

    @multi_test(card_id=2)
    def test_check_2(
        self,
        key: str,
        Dict: dict,
        Word: dict,
        Tran: dict,
        newIds: tuple,
        old_card: dict,
        upd_card: dict,
    ):
        """Check update of card, with unique word and common translation.

        Test database behavior, when all possible card's content updates are
        applied.
        """
        # Dictionary table should hold all updated values
        self.assertIn(upd_card[key], Dict[key])
        match key:
            case "word":
                # previous word shouldn't be in database
                self.assertNotIn(old_card[key], Word["name"])
                self.assertNotIn(old_card[key], Dict[key])
                # updated word must be in table
                self.assertIn(upd_card[key], Word["name"])
            case "meaning":
                self.assertIn(old_card[key], Tran[key])
                self.assertIn(old_card[key], Dict[key])
                self.assertIn(upd_card[key], Tran[key])
            case "example" | "image":
                self.assertNotIn(
                    (newIds[key], old_card[key]), list(zip(Dict["id"], Dict[key]))
                )

    @multi_test(card_id=3)
    def test_check_3(
        self,
        key: str,
        Dict: dict,
        Word: dict,
        Tran: dict,
        newIds: tuple,
        old_card: dict,
        upd_card: dict,
    ):
        """Check update of card, with common word and common translation.

        Test database behavior, when all possible card's content updates are
        applied.
        """
        # Dictionary table should hold all updated values
        self.assertIn(upd_card[key], Dict[key])
        match key:
            case "word":
                # previous word shouldn't be in database
                self.assertIn(old_card[key], Word["name"])
                self.assertIn(old_card[key], Dict[key])
                # updated word must be in table
                self.assertIn(upd_card[key], Word["name"])
            case "meaning":
                self.assertIn(old_card[key], Tran[key])
                self.assertIn(old_card[key], Dict[key])
                self.assertIn(upd_card[key], Tran[key])
            case "example" | "image":
                self.assertNotIn(
                    (newIds[key], old_card[key]), list(zip(Dict["id"], Dict[key]))
                )

    @multi_test(card_id=4)
    def test_check_4(
        self,
        key: str,
        Dict: dict,
        Word: dict,
        Tran: dict,
        newIds: tuple,
        old_card: dict,
        upd_card: dict,
    ):
        """Check update of card, with common word and unique translation.

        Test database behavior, when all possible card's content updates are
        applied.
        """
        # Dictionary table should hold all updated values
        self.assertIn(upd_card[key], Dict[key])
        match key:
            case "word":
                self.assertIn(old_card[key], Word["name"])
                self.assertIn(old_card[key], Dict[key])
                # updated word must be in table
                self.assertIn(upd_card[key], Word["name"])
            case "meaning":
                # previous word shouldn't be in database
                self.assertNotIn(old_card[key], Tran[key])
                self.assertNotIn(old_card[key], Dict[key])
                # updated word must be in table
                self.assertIn(upd_card[key], Tran[key])
            case "example" | "image":
                self.assertNotIn(
                    (newIds[key], old_card[key]), list(zip(Dict["id"], Dict[key]))
                )

    def tearDown(self):
        """Remove storage and close connection to database."""
        from os import remove

        self.db.close()
        remove(self.db_name + ".db")
