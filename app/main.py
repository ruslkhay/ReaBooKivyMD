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
from kivy.uix.screenmanager import NoTransition

from cardset import CardsListScreen, FlashCard


class BaseMDNavigationItem(MDNavigationItem):
    """Describe widgets on navigation bar."""

    icon = StringProperty()
    text = StringProperty()


class StudyScreen(MDScreen):
    """Main screen, that appears first."""

    def remove_top_widget(self):
        card_stack = [child for child in self.children if isinstance(child, FlashCard)]
        self.remove_widget(card_stack[0])

    def loop_through(self):
        card_stack = [child for child in self.children if isinstance(child, FlashCard)]
        top_card = card_stack[0]
        height = len(card_stack) - 1  # widget_stack_height
        self.remove_widget(top_card)
        self.add_widget(top_card, height)


# class CardsSet(MDCard):
#     """One set of flashcards."""

#     title = StringProperty()


# class DictionaryScreen(MDScreen):
#     """Second screen, manager of flash-cards sets."""

#     def add(self):
#         self.ids.container_dicts.add_widget(
#             CardsSet(
#                 MDLabel(
#                     text=str(len(self.ids.container_dicts.children)), halign="center"
#                 )
#             )
#         )


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


Builder.load_file("./screen_dict.kv")
Builder.load_file("./screen_cardset.kv")


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
        # previous = self.root.ids.screen_manager.current
        # print('prev',previous)
        # print(item_text, '\n')
        sm = self.root.ids.screen_manager
        sm.transition = NoTransition()

        # match previous:
        #     case "Flashcards":
        #         match item_text:
        #             case "Study":
        #                 sm.transition = SlideTransition(direction="down")
        #             case "Cards":
        #                 sm.transition = FadeTransition()
        # case "Study":
        #     sm.transition = SlideTransition(direction="right")
        # case "Cards":
        #     sm.transition = SlideTransition(direction="left")
        sm.current = item_text
        sm.transition = NoTransition()

    def start_learning(self):
        sm = self.root.ids.screen_manager
        # sm.transition = SlideTransition(direction="up")
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
        s: StudyScreen = self.root.ids.screen_study
        # ds: DictionaryScreen = self.root.ids.screen_dict
        for i in range(18):
            word = f"Word {i}"
            meaning = f"meaning {i}"
            cl.add_item(i, word, meaning, "", "data/icon_512.png")
            s.add_widget(FlashCard(word=word, meaning2=meaning))
            # ds.add()


if __name__ == "__main__":
    ReaBooApp().run()
