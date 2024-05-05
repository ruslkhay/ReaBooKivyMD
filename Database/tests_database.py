"""Tests for flesh-cards database."""

import unittest
from database import DataBase


class DatabaseTestCase(unittest.TestCase):
    """Tests for one-to-one insert for flesh-card database."""

    def setUp(self):
        """Create dummy flesh-card storage."""
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
            [('hop', 'прыгать'), ('spring', 'прыгать'), ('spring', 'весна')]
        )
        self.assertEqual(
            self.db.select_from('translate'),
            [(1, 1, 0), (2, 1, 0), (2, 2, 0)]
        )

    def test_insert_0(self):
        """One 'foreign' word, many translations."""
        self.db.oto_insert('jump', 'прыгать')
        self.db.oto_insert('jump', 'прыгнуть')

        self.assertEqual(
            self.db.select_from('dictionary'),
            [('jump', 'прыгать'), ('jump', 'прыгнуть')]
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
            [('hop', 'прыгать'), ('spring', 'прыгать')]
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
            [('hop', 'прыгать'), ('spring', 'прыгать'), ('jump', 'прыгать'),
             ('spring', 'весна'), ('bewilder', 'озадачить')]
        )
        self.assertEqual(
            self.db.select_from('words'),
            [(1, 'hop'), (2, 'spring'), (3, 'jump'), (4, 'bewilder')]
        )
        self.assertEqual(
            self.db.select_from('translations'),
            [(1, 'прыгать'), (2, 'весна'), (3, 'озадачить')]
        )

    def test_delete_0(self):
        """Delete softly (hide) word and it's translation from dictionary."""
        self.db.oto_insert('hop', 'прыгать')
        self.db.oto_insert('spring', 'прыгать')
        self.db.oto_insert('spring', 'весна')

        self.db.delete_word('spring', 'прыгать')

        self.assertEqual(
            self.db.select_from('translate'),
            [(1, 1, 0), (2, 1, 1), (2, 2, 0)]
        )

    def tearDown(self):
        """Remove dummy storage."""
        from os import remove
        self.db.close()
        remove('test.db')
