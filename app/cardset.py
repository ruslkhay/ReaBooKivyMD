from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem
from kivymd.uix.card.card import MDCard


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
        self, card_id: int, word: str, meaning: str, example: str, image: str, *args
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
        self, card_id: int, word: str, meaning: str, example: str, image: str, *args
    ):
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


class CardScreen(MDScreen):
    """Manage content of one flash-card unit."""

    card_id = NumericProperty(defaultvalue=88)
    word = StringProperty()
    meaning = StringProperty()
    example = StringProperty()
    image = StringProperty()

    def save(self):
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
        else:  # i.e. element was in list
            cl.update_item(
                card_id=self.card_id,
                word=self.word,
                meaning=self.meaning,
                example=self.example,
                image=self.image,
            )
        self.close()

    def delete(self):
        """Remove opened card from cardset content."""
        self.close()
        cl = self.parent.get_screen("Cards")
        cl.remove_item(self.card_id)

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

    # def show_meaning(self):
    #     """Show meaning of the word."""
    #     self.children[0].children[1].text_color = (0, 0, 0, 1)

    def right_guess(self):
        """Mark card as learned."""
        self.parent.remove(self)

    def wrong_guess(self):
        """Mark card as needed to be repeated."""
        self.parent.walk(loopback=True)
        # self.parent.clear_widgets()

        self.parent.remove_widget(self.parent.children[0])
