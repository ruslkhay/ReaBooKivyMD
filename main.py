from kivymd.app import MDApp
# from kivy.lang import Builder

# Builder.load_file("tracker.kv")


# Main App class
class MainApp(MDApp):
    task_list_dialog = None

    def build(self):
        # Setting theme to my favorite theme
        # self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"


if __name__ == "__main__":
    MainApp().run()
