"""
Application built by Szilard LADANYI at sziller.eu
"""

from kivy.app import App  # necessary for the App class
from kivy.lang import Builder  # to freely pick kivy files
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.image import Image

kv = Builder.load_file("gamelayout.kv")


class ScreenBoard(Screen):
    pass


class ScreenProperties(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class TempGrid(Widget):
    pass


class KiAzUrATengeren(App):
    """=== Class name: Analyzer ========================================================================================
    Child of built in class: App

    ============================================================================================== by Sziller ==="""
    # build in function to be redefined.
    # whatever Widget you return using build, will be displayed
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    game = KiAzUrATengeren()
    game.run()
