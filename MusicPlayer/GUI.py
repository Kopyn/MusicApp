from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image, AsyncImage
import random
import Test
import YoutubeAPI


class VideoItem(BoxLayout):
    def __init__(self, imageSource, title, videoID):
        super(VideoItem, self).__init__()
        self.id = videoID
        self.orientation = 'horizontal'
        imag = AnchorLayout(anchor_x='center')
        ttl = AnchorLayout(anchor_x='right')
        img = AsyncImage(source = imageSource)
        btn = Button(background_color = (0, 0, 0, 0))
        btn.bind(on_press = self.playSong)
        imag.add_widget(btn)
        imag.add_widget(img)
        ttl.add_widget(Label(text = title))
        self.add_widget(imag)
        self.add_widget(ttl)

    def playSong(self, instance):
        #Test.actualSong = "https://www.youtube.com/watch?v=" + self.id;
        Test.playSong("https://www.youtube.com/watch?v=" + self.id)

class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.rows = 1

    def playSong(self):
        Test.playSong()

    def pauseSong(self):
        Test.pauseSong()

    def searchSong(self):
        print(self.ids.search_box.text)

        YoutubeAPI.searchQuery = self.ids.search_box.text

        videoResultsData = YoutubeAPI.getSongs()

        self.ids.results.clear_widgets()
        self.l = GridLayout()
        self.l.cols = 1

        i = 0
        while i < len(videoResultsData) - 3:
            self.l.add_widget(VideoItem(videoResultsData[i], videoResultsData[i+1], videoResultsData[i+2]))
            i += 3

        #view results
        self.ids.results.add_widget(self.l)


class MusicApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    p = MusicApp()
    p.run()