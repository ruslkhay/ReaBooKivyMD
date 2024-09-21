"""Contain key class of application."""

import os

if os.uname()[1] == "VB16":  # MY MACHINE NAME !!!
    # Enlarges widgets for highly resolution screens
    scale = 2
    os.environ["KIVY_METRICS_DENSITY"] = str(scale)
    # Simulate my Xiaomi Redmi 12 screen
    from kivy.core.window import Window
    from kivy.metrics import sp

    Window.size = [sp(1080) / scale, sp(2400) / scale]


from kivy.lang import Builder
from kivy.properties import StringProperty, DictProperty
from kivy.uix.screenmanager import NoTransition

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox

from cardset import CardsListScreen, FlashCard
from database.database import DataBase

Builder.load_file("./screen_dict.kv")
Builder.load_file("./cardset.kv")


__version__ = "0.1.0"


class BaseMDNavigationItem(MDNavigationItem):
    """Describe widgets on navigation bar."""

    icon = StringProperty()
    text = StringProperty()


class StudyScreen(MDScreen):
    """Main screen, that appears first."""

    content = DictProperty()

    def remove_top_widget(self):
        card_stack = [child for child in self.children if isinstance(child, FlashCard)]
        self.remove_widget(card_stack[0])

    def loop_through(self):
        card_stack = [child for child in self.children if isinstance(child, FlashCard)]
        top_card = card_stack[0]
        height = len(card_stack) - 1  # widget_stack_height
        self.remove_widget(top_card)
        self.add_widget(top_card, height)


def load_cards(i):
    """Load cards."""
    from kivymd.uix.list import OneLineListItem

    card_item = MDCardSwipe(
        MDCardSwipeLayerBox(),
        MDCardSwipeFrontBox(
            OneLineListItem(
                id="content",
                text=f"One-line item {i}",
                _no_ripple_effect=True,
            )
        ),
        size_hint_y=None,
        height="48dp",
    )
    return card_item


class MainScreen(MDScreen):
    """Main Screen.

    I've planned that here would be something close to
    DuoCards window with mammoth."""


class ReaBooApp(MDApp):
    """Main application class."""

    def __init__(self, **kwargs):
        """Reload MDApp method to include database storage."""
        super().__init__(**kwargs)
        self.db = DataBase(
            name="content",
            path=MDApp.get_running_app().user_data_dir,
            schema="app/database/schema.sql",
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
        for row in self.db.select_to_dicts("SELECT word, meaning FROM content;"):
            word = row["word"]
            meaning = row["meaning"]
            s.add_widget(FlashCard(word=word, meaning2=meaning))

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
        for row in self.db.select_to_dicts("SELECT * FROM content;"):
            card_id = row["card_id"]
            word = row["word"]
            meaning = row["meaning"]
            cl.add_item(card_id, word, meaning, "", "data/icon_512.png")

    def on_stop(self):
        """Close database before exiting the app.

        Event handler for the on_stop event which is fired when the application
        has finished running
        """
        self.db.close()


if __name__ == "__main__":
    ReaBooApp().run()
