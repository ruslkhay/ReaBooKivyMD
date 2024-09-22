from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem
from kivymd.uix.card.card import MDCard

from database.database import DataBase


class CardListItem(MDListItem):
    """Unit of card list."""

    card_id = NumericProperty(defaultvalue=-1)
    word = StringProperty()
    meaning = StringProperty()
    example = StringProperty()
    image = StringProperty(defaultvalue="data/fill_image_placeholder.png")


class CardsListScreen(MDScreen):
    """Manage and look through flash-cards set content."""

    def get_item(self, card_id: int):
        """Return card (widget) from list by it's id."""
        cards = self.ids.container.children
        ids = list(map(lambda x: x.card_id, cards))
        return cards[ids.index(card_id)]

    def remove_item(self, card_id: int):
        """Remove element from card list."""
        self.ids.container.remove_widget(self.get_item(card_id))
        pass

    def add_item(
        self,
        card_id: int,
        word: str,
        meaning: str,
        example: str,
        image: str,
        *args,
        **kwargs,
    ):
        self.ids.container.add_widget(
            CardListItem(
                card_id=card_id,
                word=word,
                meaning=meaning,
                example=example,
                image=image,
                on_release=self.open_item,
            )
        )

    def update_item(
        self,
        card_id: int,
        word: str,
        meaning: str,
        example: str,
        image: str,
        *args,
        **kwargs,
    ):  # TODO: rewrite
        """Update content of existed card in list."""
        card = self.get_item(card_id)
        card.word = word
        card.meaning = meaning
        card.example = example
        card.image = image

    def open_item(self, item: CardListItem = None):
        sm = self.parent
        card = sm.get_screen("Card")
        card.ids.button_delete.disabled = False
        if not item:
            card.ids.button_delete.disabled = True
            item = CardListItem()
        card.card_id = item.card_id
        card.word = item.word
        card.meaning = item.meaning
        card.example = item.example
        card.image = item.image
        sm.current = "Card"

    def search(self, storage: DataBase):
        """Implement functionality of search bar."""
        valid_ids = storage.search(self.ids.search_bar.text)
        self.ids.container.clear_widgets()
        if len(valid_ids) == 1:  # For query not to crash
            valid_ids = f"({valid_ids[0]})"
        valid_cards = storage.select_to_dicts(
            """
            SELECT card_id, word, meaning, example, image FROM content
            WHERE "card_id" IN {};
            """.format(valid_ids)
        )
        for card in valid_cards:
            self.add_item(**card)


class CardScreen(MDScreen):
    """Manage content of one flash-card unit."""

    card_id = NumericProperty(defaultvalue=88)
    word = StringProperty()
    meaning = StringProperty()
    example = StringProperty()
    image = StringProperty()

    def save(self, storage: DataBase):
        sm = self.parent
        cl: CardsListScreen = sm.get_screen("Cards")
        if self.card_id == -1:
            cl.add_item(
                card_id=-1,
                word=self.word,
                meaning=self.meaning,
                example=self.example,
                image=self.image,
            )
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
        else:  # i.e. element was in list
            cl.update_item(
                card_id=self.card_id,
                word=self.word,
                meaning=self.meaning,
                example=self.example,
                image=self.image,
            )
            storage.update(
                self.card_id,
                {
                    "word": self.word,
                    "meaning": self.meaning,
                    "example": self.example,
                    "image": self.image,
                },
            )
        self.close()

    def delete(self, storage: DataBase):
        """Remove opened card from cardset content."""
        cl = self.parent.get_screen("Cards")
        cl.remove_item(self.card_id)
        storage.hard_delete("content", self.card_id)
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

    def open_meaning(self):
        """Change meaning on None or original one."""
        if self.show_meaning:
            self.meaning2 = self.meaning
            self.meaning = ""
        else:
            self.meaning = self.meaning2
        self.show_meaning = not self.show_meaning

    def right_guess(self):
        """Mark card as learned."""
        self.parent.remove(self)

    def wrong_guess(self):
        """Mark card as needed to be repeated."""
        self.parent.walk(loopback=True)
        self.parent.remove_widget(self.parent.children[0])


if __name__ == "__main__":
    from kivymd.app import MDApp

    class CardsetApp(MDApp):
        """Main application class."""

        def build(self):
            """Launch application, first method, that runs."""
            self.theme_cls.primary_palette = "Blue"
            return CardsListScreen()

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
