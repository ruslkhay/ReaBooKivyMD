"""Logic of StudyScreen.


Purpose of Stack class:
1. Have different learning exercise
2. Optimize performance (load just a part of content)
"""

# TODO: Implement Stack class

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.properties import BooleanProperty, NumericProperty

from cardset import FlashCard
from database.database import DataBase


# TODO: Manage pile. Now "card_stack = [child ... if isinstance(child, FlashCard)]""
class StudyScreen(MDScreen):
    """Main screen, that appears first."""

    empty = BooleanProperty(True)
    stack_height = NumericProperty(2)  # Amount of widgets on the screen

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: DataBase = MDApp.get_running_app().db

    def __load_content(self, order="random"):
        """Pull data from database."""
        import random

        self.content: list = self.db.select_to_dicts(
            """
            SELECT word, meaning, image FROM content;
            """
        )
        match order:
            case "random":
                random.shuffle(self.content)

    def fill(self):
        """Pull content and add initial cards."""
        if self.empty:
            self.__load_content()
            if self.content is not None:
                for _ in range(self.stack_height):
                    card = self.content.pop(0)
                    self.add_widget(
                        FlashCard(word=card["word"], meaning2=card["meaning"])
                    )
                self.empty = False

    def remove_top_widget(self):
        """Action when card is considered as learned.

        Remove card from the screen. Take next element from pull content and
        put it on the pile bottom."""
        if not self.empty:
            card_stack = [
                child for child in self.children if isinstance(child, FlashCard)
            ]
            if len(card_stack) == 1:
                self.empty = True
            self.remove_widget(card_stack[0])
            if self.content:
                card = self.content.pop(0)
                self.add_widget(
                    FlashCard(word=card["word"], meaning2=card["meaning"]),
                    self.stack_height - 1,
                )

    # TODO: Put not learned card on the bottom of the pile
    def loop_through(self):
        """Action when card is considered as not learned.

        Put current card to pile bottom."""
        if not self.empty:
            card_stack = [
                child for child in self.children if isinstance(child, FlashCard)
            ]
            top_card = card_stack[0]
            height = len(card_stack) - 1  # widget_stack_height
            self.remove_widget(top_card)
            self.add_widget(top_card, height)
