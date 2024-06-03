"""Provides GUI for flash-card learning app."""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivymd.uix.card import MDCardSwipe

if __name__ != "__main__":
    # if launching after pip installation
    from .Database import database as my_db
else:
    from Database import database as my_db

# from kivy.core.window import Window
# Window.size = (1080//2, 1920//2)

class StudyWindow(MDScreen):
    """Window for learning flash-cards."""

    pass


class MainWindow(MDScreen):
    """Initial loading window."""

    pass


class LineDictionary(MDCardSwipe):
    """Main compound of dictionary list - list row."""

    text = StringProperty()
    secondary_text = StringProperty()


class DictionaryWindow(MDScreen):
    """Window for handling and amending dictionary."""

    def add_to_list_word_trans(self, word, trans):
        """Insert new element (if it is not in dictionary) into scroll list."""
        self.ids.container.add_widget(
            LineDictionary(
                text=word,
                secondary_text=trans
            )
        )

    def load_dictionary(self, database: my_db):
        """Load up data from dictionary database."""
        dictionary = database.select_from('dictionary')
        for word, trans in dictionary:
            self.add_to_list_word_trans(word, trans)

    def add_new_card(self):
        """Pop-up widget for creating and saving new word in dictionary."""
        self.ids.topbar.left_action_items = [[
            "playlist-plus",
            lambda x: x,
            "Add new word"
            ]]
        self.add_widget(
            NewCard()
        )

    def close_card(self, name, bool=True):
        """Close up 'NewCard' pop-up widget."""
        if bool:
            self.remove_widget(name)
            self.ids.topbar.left_action_items = [[
                "playlist-plus",
                lambda x: self.add_new_card(),
                "Add new word"
                ]]


class NewCard(MDCard):
    """Implements a material card."""

    def check_word(self):
        """Test text trigger."""
        if self.ids.word.text.isspace():
            self.ids.word.error = True
        else:
            self.ids.word.text = self.ids.word.text.lstrip()

    def check_translations(self):
        """Highlights text input widget: if input is correct or non-valid."""
        if self.ids.translation.text.isspace():
            self.ids.translation.error = True
        else:
            self.ids.translation.text = self.ids.translation.text.lstrip()

    def save_to_db(self, database, word, translation):
        """Insert one word card into database."""
        database.oto_insert(word, translation)


class MyScreenManager(ScreenManager):
    """Screen stack controller."""

    pass


class ReabooApp(MDApp):
    """Main application."""

    # Internationalization and localization for GUI components.
    import gettext
    # translation = gettext.translation('reaboo', 'po', ["ru_RU.UTF-8"])
    translation = gettext.NullTranslations()  # Text in english
    _ = translation.gettext

    def __init__(self, **kwargs):
        """Reload MDApp method to include database storage."""
        super().__init__(**kwargs)
        self.db = my_db.DataBase(
            name='content',
            path='Database',
            schema='schema.sql'
        )

    def build(self):
        """Return the root of your widget tree."""
        return MyScreenManager()

    def on_start(self):
        """Preload database on dictionary window.

        Event handler for the on_start event which is fired after
        initialization but before the application has started running.
        """
        dw: DictionaryWindow = self.root.get_screen('dictionary_window')
        dw.load_dictionary(self.db)

    def remove_item(self, instance):
        """Remove one line from dictionary."""
        self.root.children[0].ids.container.remove_widget(instance)
        self.db.delete_word(
            word=instance.text,
            translation=instance.secondary_text
        )

    def exit_to_main_screen(self):
        """Exit to main screen and clear word list on dictionary screen."""
        self.root.current = 'main_window'
        self.root.transition.direction = 'right'

    def on_stop(self):
        """Close database before exiting the app.

        Event handler for the on_stop event which is fired when the application
        has finished running
        """
        self.db.close()


if __name__ == "__main__":
    ReabooApp().run()
