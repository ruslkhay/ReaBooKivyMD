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
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.card import MDCard

import Database.data_base as my_db
# Builder.load_file("tracker.kv")class


from kivy.core.window import Window

Window.size = (1080, 1920)
# Window.fullscreen = 'auto'


class LanguageBar(MDFloatLayout):
    """Top bar with current language."""

    pass


class MainWindow(MDScreen):
    """Initial loading window."""

    pass


class DictionaryWindow(MDScreen):
    """Window for handling and mending dictionary."""

    def add_list_word_trans(self, word, trans):
        """Insert new element (if it is not in dictionary) into scroll list."""
        self.ids.container.add_widget(
            TwoLineAvatarIconListItem(
                IconRightWidget(
                    icon="dots-vertical",
                ),
                text=word,
                secondary_text=trans
            )
        )

    # dictionary = my_db.run_process()
    def load_dict(self):
        """Load up data from dictionary database."""
        for word, trans in my_db.run_process():
            self.add_list_word_trans(word, trans)

    # def update_dict(self, List, **kwargs):
    #     List.add_widget(
    #             TwoLineAvatarIconListItem(
    #                 IconRightWidget(
    #                     icon="dots-vertical"
    #                 ),
    #                 **kwargs
    #                 # font_style='H4',
    #                 # secondary_font_style='H5'
    #             )
    #         )

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

    def myprint(self):
        """Test text trigger."""
        if self.ids.word.text.isspace():
            self.ids.word.error = True
        else:
            self.ids.word.text = self.ids.word.text.lstrip()
        return self.ids.word.error

    def check_translations(self):
        """Highlights text input widget: if input is correct or non-valid."""
        if self.ids.translation.text.isspace():
            self.ids.translation.error = True
        else:
            # from re import split
            # separate_trans = split('[,.;\\/]', self.ids.translation.text)
            # trans = list(map(str.strip, separate_trans)) # remove whitespaces
            self.ids.translation.text = self.ids.translation.text.lstrip()
        return self.ids.translation.error

    def save_to_db(self, word, translation):
        """Insert data into database."""
        if not word or not translation:
            print('in one')
            self.ids.word.error = True
        elif word == 'do error':
            print('in two')
            self.ids.word.error = True
        else:
            print('in three')
            my_db.dummy_insert(word, translation)
    # text = StringProperty('NewCard text here')
    pass


class MyScreenManager(ScreenManager):
    """Screen stack controller."""

    pass


class ReabooApp(MDApp):
    """Main application."""

    def build(self):
        """Return the root of your widget tree."""
        # return MainWindow()
        return MyScreenManager()


if __name__ == "__main__":
    ReabooApp().run()
