"""Provides GUI for flesh-card learning app.

class LanguageBar - top bar widget for main window;
class MainWindow - first screen for user to see;
class DictionaryWindow - screen for amending user's dictionary;
class NewCard - widget for creating and amending words in dictionary;
class MyScreenManager - screen stack controller;
class ReaBooApp - the application itself.
"""

from kivymd.app import MDApp
# from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.card import MDCard

from kivy.properties import StringProperty
from kivymd.uix.card import MDCardSwipe

import Database.data_base as my_db

from kivy.core.window import Window

Window.size = (1080, 1920)


class LanguageBar(MDFloatLayout):
    """Top bar with current language."""

    pass


class MainWindow(MDScreen):
    """Initial loading window."""

    pass


class LineDictionary(MDCardSwipe):
    """Main compound of dictionary list - list row."""

    text = StringProperty()
    secondary_text = StringProperty()


class DictionaryWindow(MDScreen):
    """Window for handling and mending dictionary."""

    def add_to_list_word_trans(self, word, trans):
        """Insert new element (if it is not in dictionary) into scroll list."""
        self.ids.container.add_widget(
            LineDictionary(
                text=word,
                secondary_text=trans
            )
        )

    def load_dict(self):
        """Load up data from dictionary database."""
        for word, trans in my_db.run_process():
            self.add_to_list_word_trans(word, trans)

    def add_new_card(self):
        """Pop-up widget for creating new word in dictionary."""
        self.add_widget(
            NewCard()
        )

    def close_card(self, name, bool=True):
        """Close up 'NewCard' pop-up widget."""
        if bool:
            self.remove_widget(name)


class NewCard(MDCard):
    """Implements a material card."""

    def check_word(self):
        """Test text trigger."""
        if self.ids.word.text.isspace():
            self.ids.word.error = True
        else:
            self.ids.word.text = self.ids.word.text.lstrip()

    def check_translations(self):
        """Highlights text input widget: if input is correct or non-valid."""
        if self.ids.translation.text.isspace():
            self.ids.translation.error = True
        else:
            self.ids.translation.text = self.ids.translation.text.lstrip()

    def save_to_db(self, word, translation):
        """Insert data into database."""
        my_db.dummy_insert(word, translation)


class MyScreenManager(ScreenManager):
    """Screen stack controller."""

    pass


class ReabooApp(MDApp):
    """Main application."""

    def build(self):
        """Return the root of your widget tree."""
        my_db.db_init()
        return MyScreenManager()

    def remove_item(self, instance):
        """Remove one line from dictionary."""
        self.root.children[0].ids.container.remove_widget(instance)
        my_db.delete_word(
            word=instance.text,
            translation=instance.secondary_text
        )


if __name__ == "__main__":
    ReabooApp().run()
    my_db.close()
