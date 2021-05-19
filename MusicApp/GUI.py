from kivy.app import App
from kivy.uix.widget import Widget

class MusicPlayer(Widget):
    pass

class Player(App):
    def build(self):
        return MusicPlayer()

player = Player()
player.run()