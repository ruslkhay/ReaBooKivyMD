from kivymd.app import MDApp
# from kivy.lang import Builder
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager

# Builder.load_file("tracker.kv")

from kivy.core.window import Window
Window.size = (1080, 1920)


class LanguageBar(MDFloatLayout):
    """Top bar with current language"""
    pass


class MainWindow(MDScreen):
    """Initial loading window"""
    pass


class DictionaryWindow(MDScreen):
    """Window for handling and mending dictionary """
    def on_enter(self):
        for i in range(50):
            self.ids.container.add_widget(
                TwoLineAvatarIconListItem(
                    IconRightWidget(
                        icon="dots-vertical"
                    ),
                    text=f"item{i}",
                    secondary_text=f"Square = {i**2}"
                )
            )
    # pass


class MyScreenManager(ScreenManager):
    """Screen stack controller"""
    pass


class ReabooApp(MDApp):
    """Main application"""

    def build(self):
        """Returns the root of your widget tree"""
        # return MainWindow()
        return MyScreenManager()


if __name__ == "__main__":
    ReabooApp().run()
