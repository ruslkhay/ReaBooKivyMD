"""Tests for flash-cards database."""

import unittest
from .database import DataBase


class DatabaseTestCase(unittest.TestCase):
    """Tests for one-to-one insert for flash-card database."""

    from os import chdir, getcwd
    from os.path import join
    chdir(join(getcwd(), 'Database'))

    def setUp(self):
        """Create dummy flash-card storage."""
        self.db = DataBase(
            name='test',
            schema='schema.sql'
        )

    def test_select_from(self):
        """Check if data is inserted right way."""
        self.db.oto_insert('hop', 'прыгать')
        self.db.oto_insert('spring', 'прыгать')
        self.db.oto_insert('spring', 'весна')

        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'hop'), (2, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'прыгать'), (2, 'весна')]
        )
        self.assertEqual(
            self.db.select_from('dictionary'),
            [('hop', 'прыгать', None, None),
             ('spring', 'прыгать', None, None),
             ('spring', 'весна', None, None)]
        )
        # self.assertEqual(
        #     self.db.select_from('translate'),
        #     [(1, 1, 0), (2, 1, 0), (2, 2, 0)]
        # )

    def test_insert_0(self):
        """One 'foreign' word, many translations."""
        self.db.oto_insert('jump', 'прыгать')
        self.db.oto_insert('jump', 'прыгнуть')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('jump', 'прыгать', None, None), 
             ('jump', 'прыгнуть', None, None)]
        )
        self.assertEqual(
            self.db.select_from('words'), [(1, 'jump')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'прыгать'), (2, 'прыгнуть')]
        )

    def test_insert_1(self):
        """Many 'foreign' words, one translation."""
        self.db.oto_insert('hop', 'прыгать')
        self.db.oto_insert('spring', 'прыгать')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('hop', 'прыгать', None, None),
             ('spring', 'прыгать', None, None)]
        )
        self.assertEqual(
            self.db.select_from('words'), [(1, 'hop'), (2, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'), [(1, 'прыгать')]
        )

    def test_insert_2(self):
        """Many 'foreign' words with multiple translations."""
        self.db.oto_insert('hop', 'прыгать')
        self.db.oto_insert('spring', 'прыгать')
        self.db.oto_insert('jump', 'прыгать')
        self.db.oto_insert('spring', 'весна')
        self.db.oto_insert('bewilder', 'озадачить')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('hop', 'прыгать', None, None),
             ('spring', 'прыгать', None, None),
             ('jump', 'прыгать', None, None),
             ('spring', 'весна', None, None),
             ('bewilder', 'озадачить', None, None)]
        )
        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'hop'), (2, 'spring'), (3, 'jump'), (4, 'bewilder')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'прыгать'), (2, 'весна'), (3, 'озадачить')]
        )

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

    def test_hard_delete_1(self):
        """Delete not unique word and not unique translation.
         
        Delete from dictionary one row, where word is used in another row
        and translation is also used in another row.
        """
        self.db.oto_insert('hop', 'прыгать')
        self.db.oto_insert('spring', 'весна')
        self.db.oto_insert('spring', 'прыгать')
        self.db.oto_insert('jump', 'прыгать')
        self.db.oto_insert('bewilder', 'озадачить')

        self.db.delete_word('spring', 'прыгать')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('hop', 'прыгать', None, None),
             ('spring', 'весна', None, None),
             ('jump', 'прыгать', None, None),
             ('bewilder', 'озадачить', None, None)]
        )
        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'hop'), (2, 'spring'), (3, 'jump'), (4, 'bewilder')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'прыгать'), (2, 'весна'), (3, 'озадачить')]
        )

    def test_hard_delete_2(self):
        """"Delete unique word and not unique translation.
         
        Delete from dictionary one row, where word is used in another row
        by translation is not. 
        """
        self.db.oto_insert('hop', 'прыгать')
        self.db.oto_insert('spring', 'прыгать')

        self.db.delete_word('hop', 'прыгать')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('spring', 'прыгать', None, None)]
        )
        self.assertEqual(
            self.db.select_from('words'), [(2, 'spring')]
        )
        self.assertEqual(
            self.db.select_from('translations'), [(1, 'прыгать')]
        )

    def test_hard_delete_3(self):
        """Delete not unique word and unique translation.
         
        Delete from dictionary one row, where word is not used in another row
        but translation is.
        """
        self.db.oto_insert('jump', 'прыгать')
        self.db.oto_insert('jump', 'прыгнуть')

        self.db.delete_word('jump', 'прыгнуть')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('jump', 'прыгать', None, None)]
        )
        self.assertEqual(
            self.db.select_from('words'), [(1, 'jump')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'прыгать')]
        )

    def tearDown(self):
        """Remove dummy storage."""
        from os import remove
        self.db.close()
        remove('test.db')
