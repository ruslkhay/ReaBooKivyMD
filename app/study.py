from kivymd.uix.screen import MDScreen
from kivy.properties import DictProperty
from kivymd.uix.card import MDCardSwipe, MDCardSwipeLayerBox, MDCardSwipeFrontBox

from cardset import FlashCard


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
