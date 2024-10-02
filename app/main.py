"""Contain key class of application."""

__version__ = "0.1.1"

import os

#  Scaling application for 4k monitor
if os.uname()[1] == "VB16":  # MY MACHINE NAME !!!
    # Enlarges widgets for highly resolution screens
    scale = 2
    os.environ["KIVY_METRICS_DENSITY"] = str(scale)
    # Simulate my Xiaomi Redmi 12 screen
    from kivy.core.window import Window
    from kivy.metrics import sp

    Window.size = [sp(1080) / scale, sp(2400) / scale]


from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import NoTransition

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen

from cardset import CardsListScreen, FlashCard
from study import StudyScreen
from database.database import DataBase

from pathlib import Path

Builder.load_file("./screen_dict.kv")
Builder.load_file("./cardset.kv")
Builder.load_file("./study.kv")


class BaseMDNavigationItem(MDNavigationItem):
    """Describe widgets on navigation bar."""

    icon = StringProperty()
    text = StringProperty()


class MainScreen(MDScreen):
    """Main Screen.

    I've planned that here would be something close to
    DuoCards window with mammoth."""


class ReaBooApp(MDApp):
    """Main application class."""

    def __init__(self, **kwargs):
        """Reload MDApp method to include database storage."""
        super().__init__(**kwargs)
        cwd = Path(__file__).parent
        self.db = DataBase(
            name=Path("content.db"),
            path=MDApp.get_running_app().user_data_dir,
            schema=cwd / Path("database/schema.sql"),
        )

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        """Behavior for transition between screens"""
        sm = self.root.ids.screen_manager
        sm.transition = NoTransition()
        sm.current = item_text

    def start_learning(self):
        s: StudyScreen = self.root.ids.screen_study
        s.fill()
        sm = self.root.ids.screen_manager
        sm.current = "Flashcards"

    def build(self):
        """Launch application, first method, that runs."""
        self.theme_cls.primary_palette = "Blue"

    def load_content(self, child):
        # if isinstance(child, StudyScreen):
        s: StudyScreen = self.root.ids.screen_study
        for row in self.db.select_to_dicts("SELECT word, meaning FROM content;"):
            word = row["word"]
            meaning = row["meaning"]
            s.add_widget(FlashCard(word=word, meaning2=meaning))

    def on_start(self):
        """Make actions after launch, but before load up of app."""
        try:
            self.db.insert("dictionary", {"title": "debug", "background_image": ""})
        except Exception:
            pass
        cl: CardsListScreen = self.root.ids.screen_cardlist
        query = """SELECT card_id FROM content ORDER BY card_id;"""
        for card_id in self.db.select_to_dicts(query):
            cl.add_item(**card_id)

    def on_stop(self):
        """Close database before exiting the app.

        Event handler for the on_stop event which is fired when the application
        has finished running
        """
        self.db.close()


if __name__ == "__main__":
    ReaBooApp().run()
