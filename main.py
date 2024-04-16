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


class LanguageBar(MDFloatLayout):
    """Top bar with current language."""

    pass


class MainWindow(MDScreen):
    """Initial loading window."""

    pass


class DictionaryWindow(MDScreen):
    """Window for handling and mending dictionary."""

    # dictionary = my_db.run_process()
    def load_dict(self):
        """Load up data from dictionary database."""
        for elem in my_db.read_data():
            self.ids.container.add_widget(
                TwoLineAvatarIconListItem(
                    IconRightWidget(
                        icon="dots-vertical"
                    ),
                    text=elem[1],
                    secondary_text=elem[2]
                )
            )

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

    def close_card(self, name):
        """Close up 'NewCard' pop-up widget."""
        self.remove_widget(name)


class NewCard(MDCard):
    """Implements a material card."""

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
