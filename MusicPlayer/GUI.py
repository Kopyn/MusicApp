from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

import Test

class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.rows = 1



    def playSong(self, instance):
        Test.playSong()

    def pauseSong(self, instance):
        Test.pauseSong()


class MusicApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    p = MusicApp()
    p.run()