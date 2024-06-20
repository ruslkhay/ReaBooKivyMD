"""Tests for flash-cards database."""

import unittest
from .database import DataBase


class InsertTestCase(unittest.TestCase):
    """Tests for one-to-one insert for flash-card database."""

    def setUp(self):
        """Create dummy flash-card storage."""
        self.db_name = 'test'
        self.db = DataBase(
            name=self.db_name,
            schema='Database/schema.sql'
        )

    def test_insert(self):
        """Check if data is inserted right way for each table."""
        self.db.oto_insert(
            word='raise',
            translation='поднять')
        self.db.oto_insert(
            word='hop',
            translation='прыгать',
            example='Girl hopped from stone to stone.')
        self.db.oto_insert(
            word='spring',
            translation='прыгать',
            image='some url-link')
        self.db.oto_insert(
            word='spring',
            translation='весна',
            example='Spring was warm.',
            image='picture\'s path')

        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'raise'), (2, 'hop'), (3, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'поднять'), (2, 'прыгать'), (3, 'весна')]
        )
        self.assertEqual(
            self.db.select_from('dictionary'),
            [(1, 'raise', 'поднять', None, None),
             (2, 'hop', 'прыгать', 'Girl hopped from stone to stone.', None),
             (3, 'spring', 'прыгать', None, 'some url-link'),
             (4, 'spring', 'весна', 'Spring was warm.', 'picture\'s path')]
        )
        self.assertEqual(
            self.db.select_from('translate'),
            [(1, 1, 1, None, None, 0),
             (2, 2, 2, 'Girl hopped from stone to stone.', None, 0),
             (3, 3, 2, None, 'some url-link', 0),
             (4, 3, 3, 'Spring was warm.', 'picture\'s path', 0)]
        )

    def tearDown(self):
        """Remove storage and close connection to database."""
        from os import remove
        self.db.close()
        remove(self.db_name + '.db')


class DeleteTestCase(unittest.TestCase):
    """Tests for deleting content out of flash-card database."""

    def setUp(self):
        """Create filled flash-card storage."""

        self.db_name = 'test'
        self.db = DataBase(
            name=self.db_name,
            schema='Database/schema.sql'
        )

        self.db.oto_insert(
            word='raise',
            translation='поднять')
        self.db.oto_insert(
            word='hop',
            translation='прыгать',
            example='Girl hopped from stone to stone.')
        self.db.oto_insert(
            word='spring',
            translation='прыгать',
            image='some url-link')
        self.db.oto_insert(
            word='spring',
            translation='весна',
            example='Spring was warm.',
            image='picture\'s path')

    # def test_delete_0(self):
    #     """Delete softly (hide) word and it's translation from dictionary."""
    #     self.db.oto_insert('hop', 'прыгать')
    #     self.db.oto_insert('spring', 'прыгать')
    #     self.db.oto_insert('spring', 'весна')

    #     self.db.delete_word('spring', 'прыгать')

    #     self.assertEqual(
    #         self.db.select_from('translate'),
    #         [(1, 1, 0), (2, 1, 1), (2, 2, 0)]
    #     )

    def test_hard_delete_0(self):
        """Delete unique word and unique translation.

        Delete from dictionary one row, where word is not used in another row
        and translation is also not used in another row.
        """
        self.db.delete_word('raise', 'поднять')

        self.assertNotIn((1, 'raise'), self.db.select_from('words'))
        self.assertNotIn((1, 'поднять'), self.db.select_from('translations'))
        self.assertNotIn(
            ('raise', 'поднять', None, None),
            self.db.select_from('dictionary')
        )

        self.assertEqual(
            self.db.select_from('words'),
            [(2, 'hop'), (3, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(2, 'прыгать'), (3, 'весна')]
        )
        self.assertEqual(
            self.db.select_from('dictionary'),
            [(2, 'hop', 'прыгать', 'Girl hopped from stone to stone.', None),
             (3, 'spring', 'прыгать', None, 'some url-link'),
             (4, 'spring', 'весна', 'Spring was warm.', 'picture\'s path')]
        )
        self.assertEqual(
            self.db.select_from('translate'),
            [(2, 2, 2, 'Girl hopped from stone to stone.', None, 0),
             (3, 3, 2, None, 'some url-link', 0),
             (4, 3, 3, 'Spring was warm.', 'picture\'s path', 0)]
        )

    def test_hard_delete_1(self):
        """Delete not unique word and not unique translation.

        Delete from dictionary one row, where word is used in another row
        and translation is also used in another row.
        """
        self.db.delete_word('spring', 'прыгать')

        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'raise'), (2, 'hop'), (3, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'поднять'), (2, 'прыгать'), (3, 'весна')]
        )
        self.assertEqual(
            self.db.select_from('dictionary'),
            [(1, 'raise', 'поднять', None, None),
             (2, 'hop', 'прыгать', 'Girl hopped from stone to stone.', None),
             (4, 'spring', 'весна', 'Spring was warm.', 'picture\'s path')]
        )
        self.assertEqual(
            self.db.select_from('translate'),
            [(1, 1, 1, None, None, 0),
             (2, 2, 2, 'Girl hopped from stone to stone.', None, 0),
             (4, 3, 3, 'Spring was warm.', 'picture\'s path', 0)]
        )

    def test_hard_delete_2(self):
        """"Delete unique word and not unique translation.

        Delete from dictionary one row, where word is not used in another row
        by translation is.
        """

        self.db.delete_word('hop', 'прыгать')
        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'raise'), (3, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'поднять'), (2, 'прыгать'), (3, 'весна')]
        )
        self.assertEqual(
            self.db.select_from('dictionary'),
            [(1, 'raise', 'поднять', None, None),
             (3, 'spring', 'прыгать', None, 'some url-link'),
             (4, 'spring', 'весна', 'Spring was warm.', 'picture\'s path')]
        )
        self.assertEqual(
            self.db.select_from('translate'),
            [(1, 1, 1, None, None, 0),
             (3, 3, 2, None, 'some url-link', 0),
             (4, 3, 3, 'Spring was warm.', 'picture\'s path', 0)]
        )

    def test_hard_delete_3(self):
        """Delete not unique word and unique translation.

        Delete from dictionary one row, where word is used in another row
        but translation is not.
        """

        self.db.delete_word('spring', 'весна')
        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'raise'), (2, 'hop'), (3, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'поднять'), (2, 'прыгать')]
        )
        self.assertEqual(
            self.db.select_from('dictionary'),
            [(1, 'raise', 'поднять', None, None),
             (2, 'hop', 'прыгать', 'Girl hopped from stone to stone.', None),
             (3, 'spring', 'прыгать', None, 'some url-link')]
        )
        self.assertEqual(
            self.db.select_from('translate'),
            [(1, 1, 1, None, None, 0),
             (2, 2, 2, 'Girl hopped from stone to stone.', None, 0),
             (3, 3, 2, None, 'some url-link', 0)]
        )

    def tearDown(self):
        """Remove storage and close connection to database."""
        from os import remove
        self.db.close()
        remove(self.db_name + '.db')


def refreshed_content(database: DataBase):
    """Return new values out of tables after update."""
    def F(d: dict):
        def extract(x):
            for i, param in enumerate(d.keys()):
                d[param].append(x[i])
        return extract
    Dict = {'id': [], 'word': [], 'meaning': [],
            'example': [], 'image': []}
    list(map(F(Dict), database.select_from('dictionary')))
    Word = {'id': [], 'name': []}
    list(map(F(Word), database.select_from('words')))
    Tran = {'id': [], 'meaning': []}
    list(map(F(Tran), database.select_from('translations')))
    return Dict, Word, Tran


def get_new_ids(db: DataBase, word: str, meaning: str):
    """Return first appropriate 'id'."""
    Ids = {'word': 0, 'meaning': 0, 'example': 0, 'image': 0}
    Ids['example'] = db.select_from(
        'dictionary', 'id',
        f'WHERE word = \'{word}\' AND meaning = \'{meaning}\'')[0][0]
    Ids['image'] = Ids['example']
    Ids['word'] = db.select_from(
        'translations', 'id', f'WHERE meaning = \'{meaning}\'')[0][0]
    Ids['meaning'] = db.select_from(
        'words', 'id', f'WHERE name = \'{word}\'')[0][0]
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

    def setUp(self):
        """Create filled flash-card storage."""
        # Creating and connecting to database
        self.db_name = 'test'
        self.db = DataBase(
            name=self.db_name,
            schema='Database/schema.sql')
        # Filling values. '*-u' = 'unique', '*-c' = 'common', 'X' = 'None'
        # 'W', 'T', 'E', 'I' - corresponding abbreviations
        self.db.oto_insert(  # W-u T-u X X
            word='raise', translation='поднять',
            example=None, image=None)
        self.db.oto_insert(  # W-u T-c E X
            word='hop', translation='прыгать',
            example='Girl hopped from stone to stone.', image=None)
        self.db.oto_insert(  # W-c T-c X I
            word='spring', translation='прыгать',
            example=None, image='some url-link')
        self.db.oto_insert(  # W-c T-u E I
            word='spring', translation='весна',
            example='Spring was warm.', image='picture\'s path')

    def check_1(self, key: str, Dict: dict,
                Word: dict, Tran: dict, newIds: tuple):
        """Check, when unique word and unique translation."""
        # Dictionary table should hold all updated values
        self.assertIn(self.new[key], Dict[key])
        match key:
            case 'word':
                # previous word shouldn't be in database
                self.assertNotIn(self.old[key], Word['name'])
                self.assertNotIn(self.old[key], Dict[key])
                # updated word must be in table
                self.assertIn(self.new[key], Word['name'])
            case 'meaning':
                # previous translation shouldn't be in database
                self.assertNotIn(self.old[key], Tran[key])
                self.assertNotIn(self.old[key], Dict[key])
                # updated translation must be in table
                self.assertIn(self.new[key], Tran[key])
            case 'example' | 'image':
                self.assertNotIn(
                    (newIds[key], self.old[key]),
                    list(zip(Dict['id'], Dict[key])))

    def test_update_1(self):
        """Check update on card with unique word and unique translation.

        If user change word, then it """
        from itertools import combinations

        self.old = dict(word='raise', meaning='поднять',
                        example=None,
                        image=None)
        self.card_id = 1
        self.new = dict(word='lift', meaning='приподнимать',
                        example='Lift heavy bar',
                        image='bar\'s image')
        # Create all possible input combinations
        for num_param in range(1, 1 + len(self.new)):
            param_comb = combinations(list(self.new.items()), num_param)
            # Run TestCase for each of them
            for comb in param_comb:
                params = dict(comb)
                with self.subTest(**params):
                    self.tearDown()
                    self.setUp()
                    card = self.old.copy()
                    card.update(params)
                    self.db.update_word(self.card_id, *card.values())
                    D, W, T = refreshed_content(self.db)
                    # Getting new ids
                    ID = get_new_ids(self.db, card['word'], card['meaning'])
                    list(map(
                        lambda x: self.check_1(x, D, W, T, ID), params.keys()))

    def check_2(self, key: str, Dict: dict,
                Word: dict, Tran: dict, newIds: tuple):
        """Check, when unique word and common translation."""
        # Dictionary table should hold all updated values
        self.assertIn(self.new[key], Dict[key])
        match key:
            case 'word':
                # previous word shouldn't be in database
                self.assertNotIn(self.old[key], Word['name'])
                self.assertNotIn(self.old[key], Dict[key])
                # updated word must be in table
                self.assertIn(self.new[key], Word['name'])
            case 'meaning':
                self.assertIn(self.old[key], Tran[key])
                self.assertIn(self.old[key], Dict[key])
                self.assertIn(self.new[key], Tran[key])
            case 'example' | 'image':
                self.assertNotIn(
                    (newIds[key], self.old[key]),
                    list(zip(Dict['id'], Dict[key])))

    def test_update_2(self):
        """Check update on card with unique word and common translation.

        If user change word, then it """
        from itertools import combinations

        self.old = dict(word='hop', meaning='прыгать',
                        example='Girl hopped from stone to stone.',
                        image=None)
        self.card_id = 2
        self.new = dict(word='bob', meaning='скакать', example=None,
                        image='image\'s path')
        # Create all possible input combinations
        for num_param in range(1, 1 + len(self.new)):
            param_comb = combinations(list(self.new.items()), num_param)
            # Run TestCase for each of them
            for comb in param_comb:
                params = dict(comb)
                with self.subTest(**params):
                    self.tearDown()
                    self.setUp()
                    card = self.old.copy()
                    card.update(params)
                    self.db.update_word(self.card_id, *card.values())
                    D, W, T = refreshed_content(self.db)
                    # Getting new ids
                    ID = get_new_ids(self.db, card['word'], card['meaning'])
                    list(map(
                        lambda x: self.check_2(x, D, W, T, ID), params.keys()))

    def check_3(self, key: str, Dict: dict,
                Word: dict, Tran: dict, newIds: tuple):
        """Check, when common word and common translation."""
        # Dictionary table should hold all updated values
        self.assertIn(self.new[key], Dict[key])
        match key:
            case 'word':
                # previous word shouldn't be in database
                self.assertIn(self.old[key], Word['name'])
                self.assertIn(self.old[key], Dict[key])
                # updated word must be in table
                self.assertIn(self.new[key], Word['name'])
            case 'meaning':
                self.assertIn(self.old[key], Tran[key])
                self.assertIn(self.old[key], Dict[key])
                self.assertIn(self.new[key], Tran[key])
            case 'example' | 'image':
                self.assertNotIn(
                    (newIds[key], self.old[key]),
                    list(zip(Dict['id'], Dict[key])))

    def test_update_3(self):
        """Check update on card with common word and common translation.

        If user change word, then it """
        from itertools import combinations

        self.old = dict(word='spring', meaning='прыгать',
                        example=None, image='some url-link')
        self.card_id = 3
        self.new = dict(word='bounce', meaning='пружинить',
                        example='Walk with a bounce',
                        image='illustration')
        # Create all possible input combinations
        for num_param in range(1, 1 + len(self.new)):
            param_comb = combinations(list(self.new.items()), num_param)
            # Run TestCase for each of them
            for comb in param_comb:
                params = dict(comb)
                with self.subTest(**params):
                    self.tearDown()
                    self.setUp()
                    card = self.old.copy()
                    card.update(params)
                    self.db.update_word(self.card_id, *card.values())
                    D, W, T = refreshed_content(self.db)
                    # Getting new ids
                    ID = get_new_ids(self.db, card['word'], card['meaning'])
                    list(map(
                        lambda x: self.check_3(x, D, W, T, ID), params.keys()))

    def check_4(self, key: str, Dict: dict,
                Word: dict, Tran: dict, newIds: tuple):
        """Check, when unique word and common translation."""
        # Dictionary table should hold all updated values
        self.assertIn(self.new[key], Dict[key])
        match key:
            case 'word':
                self.assertIn(self.old[key], Word['name'])
                self.assertIn(self.old[key], Dict[key])
                # updated word must be in table
                self.assertIn(self.new[key], Word['name'])
            case 'meaning':
                # previous word shouldn't be in database
                self.assertNotIn(self.old[key], Tran[key])
                self.assertNotIn(self.old[key], Dict[key])
                # updated word must be in table
                self.assertIn(self.new[key], Tran[key])
            case 'example' | 'image':
                self.assertNotIn(
                    (newIds[key], self.old[key]),
                    list(zip(Dict['id'], Dict[key])))

    def test_update_4(self):
        """Check update on card with unique word and common translation.

        If user change word, then it """
        from itertools import combinations

        self.old = dict(word='spring', meaning='весна',
                        example='Spring was warm.', image='picture\'s path')
        self.card_id = 4
        self.new = dict(word='autumn', meaning='осень', example=None,
                        image='see here')
        # Create all possible input combinations
        for num_param in range(1, 1 + len(self.new)):
            param_comb = combinations(list(self.new.items()), num_param)
            # Run TestCase for each of them
            for comb in param_comb:
                params = dict(comb)
                with self.subTest(**params):
                    self.tearDown()
                    self.setUp()
                    card = self.old.copy()
                    card.update(params)
                    self.db.update_word(self.card_id, *card.values())
                    D, W, T = refreshed_content(self.db)
                    # Getting new ids
                    ID = get_new_ids(self.db, card['word'], card['meaning'])
                    list(map(
                        lambda x: self.check_4(x, D, W, T, ID), params.keys()))

    def tearDown(self):
        """Remove storage and close connection to database."""
        from os import remove
        self.db.close()
        remove(self.db_name + '.db')
