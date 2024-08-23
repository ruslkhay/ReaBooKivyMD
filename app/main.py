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
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import FadeTransition, SlideTransition, NoTransition
from kivymd.uix.card import MDCard

from cardset import CardsListScreen


class BaseMDNavigationItem(MDNavigationItem):
    """Describe widgets on navigation bar."""

    icon = StringProperty()
    text = StringProperty()


class StudyScreen(MDScreen):
    """Main screen, that appears first."""


class CardsSet(MDCard):
    """One set of flashcards."""

    title = StringProperty()


class DictionaryScreen(MDScreen):
    """Second screen, manager of flash-cards sets."""

    def add(self):
        self.ids.container_dicts.add_widget(
            CardsSet(
                MDLabel(
                    text=str(len(self.ids.container_dicts.children)), halign="center"
                )
            )
        )


def load_cards(i):
    """Load cards."""
    from kivymd.uix.card import MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox
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

    ...


Builder.load_file("screen_dict.kv")
Builder.load_file("screen_cardset.kv")


__version__ = "2.0.0"


class ReaBooApp(MDApp):
    """Main application class."""

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        """Behavior for transition between screens"""
        previous = self.root.ids.screen_manager.current
        # print('prev',previous)
        # print(item_text, '\n')
        sm = self.root.ids.screen_manager
        sm.transition = NoTransition()

        match previous:
            case "Flashcards":
                match item_text:
                    case "Study":
                        sm.transition = SlideTransition(direction="down")
                    case "Cards":
                        sm.transition = FadeTransition()
            # case "Study":
            #     sm.transition = SlideTransition(direction="right")
            # case "Cards":
            #     sm.transition = SlideTransition(direction="left")
        sm.current = item_text
        sm.transition = NoTransition()

    def start_learning(self):
        sm = self.root.ids.screen_manager
        sm.transition = SlideTransition(direction="up")
        sm.current = "Flashcards"
        # self.root.remove_widget(self.root.ids.navigation_bar)

    def build(self):
        """Launch application, first method, that runs."""
        self.theme_cls.primary_palette = "Blue"
        pass

    #     return Builder.load_file(KVfile)

    def on_start(self):
        """Make actions after launch, but before load up of app."""
        print(self.root.ids)
        cl: CardsListScreen = self.root.ids.screen_cardlist
        # ds: DictionaryScreen = self.root.ids.screen_dict
        for i in range(5):
            cl.add_item(i, f"Word {i}", f"meaning {i}", "", "data/icon_512.png")
            # ds.add()


ReaBooApp().run()
