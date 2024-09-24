from kivymd.uix.screen import MDScreen
from kivy.properties import DictProperty

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
