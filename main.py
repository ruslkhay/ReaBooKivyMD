from kivymd.app import MDApp
# from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
# from kivymd.uix.screen import MDScreen
# from kivymd.uix.button import MDButton
# from kivy.lang import Builder

# Builder.load_file("tracker.kv")

from kivy.core.window import Window
Window.size = (1080, 1920)


class LanguageBar(MDFloatLayout):
    pass


class MainWindow(MDBoxLayout):
    pass


# Main App class
class MainApp(MDApp):
    task_list_dialog = None

class ReabooApp(MDApp):
    def build(self):
        return MainWindow()



if __name__ == "__main__":
    MainApp().run()

if __name__ == "__main__":
    ReabooApp().run()
