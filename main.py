from kivymd.app import MDApp
# from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout

from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDButton
# from kivy.lang import Builder

# Builder.load_file("tracker.kv")

from kivy.core.window import Window
Window.size = (1080, 1920)


class LanguageBar(MDFloatLayout):
    """Top bar with current language"""
    pass


class MainWindow(MDBoxLayout):
    """Initial loading window"""
    pass


class DictionaryWindow(MDBoxLayout):
    """Window for handling and mending dictionary """
    pass


class ReabooApp(MDApp):
    """Main application"""

    def build(self):
        """Returns the root of your widget tree"""
        return DictionaryWindow()

    def on_start(self):
        for i in range(50):
            self.root.ids.container.add_widget(
                TwoLineAvatarIconListItem(
                    IconRightWidget(
                        icon="dots-vertical"
                    ),
                    text=f"item{i}",
                    secondary_text=f"Square = {i**2}"
                )
            )


if __name__ == "__main__":
    ReabooApp().run()
