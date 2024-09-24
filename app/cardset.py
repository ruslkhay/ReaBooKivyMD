"""Logic of CardsetScreen.

This screen should provide next options:
1. Look through added content (cards),
2. Add new cards,
3. Amend existing cards,
4. Delete old cards,

Therefor next Widget are needed:
1. ScrollView for containing all cards
2. Items of ScrollView
3. CardWidget for work with specific card."""

from typing import Union

from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem
from kivymd.uix.card.card import MDCard
from kivymd.app import MDApp

from database.database import DataBase


def binary_search(a, target, b, t=None):
    """Return card with specified id."""
    if t is None:
        t = len(a)
    while b <= t:
        m = b + (t - b) // 2
        midval = a[m]
        if midval.card_id < target:
            t = m - 1
        elif midval.card_id > target:
            b = m + 1
        else:
            return midval
    return None


class CardListItem(MDListItem):
    """Unit of card list."""

    card_id = NumericProperty()
    word = StringProperty()
    meaning = StringProperty()
    image = StringProperty()


# TODO: Implement "order by" option for showing content
class CardsListScreen(MDScreen):
    """Cardset content as scrollable list."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db: DataBase = MDApp.get_running_app().db

    # TODO: fix button_save.disabled
    def open_item(self, item: CardListItem = None):
        """Load content of card on separate screen."""

        sm = self.parent
        screen_card: CardScreen = sm.get_screen("Card")
        if not item:
            screen_card.ids.button_delete.disabled = True
            screen_card.fill_with(None)
        else:
            screen_card.ids.button_delete.disabled = False
            card = self.db.select_to_dicts(
                """
                SELECT card_id, word, meaning, example, image FROM content
                WHERE "card_id" = {};
                """.format(item.card_id)
            )[0]
            screen_card.fill_with(card)
        sm.current = "Card"

    def find_item(self, card_id: int):
        """Return card (widget) from list by it's id."""
        cards = self.ids.container.children
        return binary_search(cards, card_id, b=0)

    def add_item(self, card_id: int):
        """Add new element from storage to screen list"""

        card = self.db.select_to_dicts(
            """
            SELECT card_id, word, meaning, image FROM content
            WHERE "card_id" = {};
            """.format(card_id)
        )[0]
        self.ids.container.add_widget(
            CardListItem(
                **card,
                on_release=self.open_item,
            )
        )

    def update_item(
        self,
        card_id: int,
    ):
        """Update content of existed card in list."""
        fresh_card = self.db.select_to_dicts(
            """
            SELECT card_id, word, meaning, image FROM content
            WHERE "card_id" = {};
            """.format(card_id)
        )[0]
        card = self.find_item(card_id)
        card.word = fresh_card["word"]
        card.meaning = fresh_card["meaning"]
        card.image = fresh_card["image"]

    def remove_item(self, card_id: int):
        """Remove element from card list."""
        card = self.find_item(card_id)
        self.ids.container.remove_widget(card)

    def search(self, storage: DataBase):  # TODO: think of smarter approach
        """Implement functionality of search bar."""
        valid_ids = storage.search(self.ids.search_bar.text)
        self.ids.container.clear_widgets()
        if len(valid_ids) == 1:  # For query below not to crash
            valid_ids = f"({valid_ids[0]})"
        valid_cards = storage.select_to_dicts(
            """
            SELECT card_id FROM content
            WHERE "card_id" IN {};
            """.format(valid_ids)
        )
        for card in valid_cards:
            self.add_item(**card)


# TODO: check whitespace and general validity of inputs
# TODO: secure valid inputs to database to store.
class CardScreen(MDScreen):
    """Manage content of one flash-card unit."""

    card_id = NumericProperty()
    word = StringProperty()
    meaning = StringProperty()
    example = StringProperty()
    image = StringProperty()

    def fill_with(self, card: Union[dict | None]):
        if card is None:
            card = {
                "card_id": 0,
                "word": "",
                "meaning": "",
                "example": "",
                "image": "",
            }
        self.card_id = card["card_id"]
        self.word = card["word"]
        self.meaning = card["meaning"]
        self.example = card["example"]
        self.image = card["image"]

    def save(self, storage: DataBase):
        sm = self.parent
        cl: CardsListScreen = sm.get_screen("Cards")
        if self.card_id == 0:  # i.e. element wasn't in list
            # Saving to database
            storage.insert(
                "content",
                {
                    "id_dict": 1,
                    "word": self.word,
                    "meaning": self.meaning,
                    "example": self.example,
                    "image": self.image,
                },
            )
            # Adding to screen
            new_card = storage.select_to_dicts(
                """SELECT MAX(card_id) as card_id FROM content;"""
            )
            cl.add_item(**new_card[0])
        else:
            # Update in database
            storage.update(
                self.card_id,
                {
                    "word": self.word,
                    "meaning": self.meaning,
                    "example": self.example,
                    "image": self.image,
                },
            )
            # Update on screen
            cl.update_item(card_id=self.card_id)

        self.close()

    def delete(self, storage: DataBase):
        """Remove opened card from cardset and database content."""

        cl = self.parent.get_screen("Cards")
        cl.remove_item(self.card_id)  # Remove from screen
        storage.hard_delete("content", self.card_id)  # Remove from database
        self.close()

    def close(self):
        """Go back from opened card to cardset screen."""
        sm = self.parent
        sm.current = "Cards"
        # print(sm.screens)


class FlashCard(MDCard):
    """Card, that is used in study screen."""

    word = StringProperty("")
    meaning = StringProperty("")
    meaning2 = StringProperty("")
    show_meaning = BooleanProperty(False)

    def open_meaning(self):  # TODO: get rid of self.meaning2
        """Change meaning on None or original one."""
        if self.show_meaning:
            self.meaning2 = self.meaning
            self.meaning = ""
        else:
            self.meaning = self.meaning2
        self.show_meaning = not self.show_meaning
