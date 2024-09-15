"""Run's application."""

from os import chdir
from os.path import split

chdir(split(__file__)[0])


if __name__ == "ReaBoo":
    from .app.main import ReaBooApp

    ReaBooApp().run()
