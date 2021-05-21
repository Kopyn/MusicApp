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
from kivy.core.window import Window
import Test
import YoutubeAPI
from AudioPlayer import *

audioPlayer = AudioPlayer()

class VideoItem(BoxLayout):
    def __init__(self, imageSource, title, videoID):
        super(VideoItem, self).__init__()
        self.id = videoID
        self.orientation = 'horizontal'
        imag = AnchorLayout(anchor_x='center')
        ttl = AnchorLayout(anchor_x='right')
        img = AsyncImage(source = imageSource)
        btn = Button(background_color = (0, 0, 0, 0))
        btn.outline_width = 1
        btn.outline_color = (1/255, 2/255, 189/255)
        btn.bind(on_press = self.playSong)
        imag.add_widget(btn)
        imag.add_widget(img)
        ttl.add_widget(Label(text = title, text_size = (200, None)))
        self.add_widget(imag)
        self.add_widget(ttl)

    def playSong(self, instance):
        #Test.actualSong = "https://www.youtube.com/watch?v=" + self.id;
        #MainLayout.playSong("https://www.youtube.com/watch?v=" + self.id)
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + self.id)




class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.rows = 1
        Window.size = (800, 500)
        self.ids.volume_control.bind(value = self.changeVolume)

    @staticmethod
    def playSong(title):
        audioPlayer.playSong(title)

    def playSong(self):
        audioPlayer.playSong()

    def pauseSong(self):
        audioPlayer.pauseSong()

    def changeVolume(self, instance, volume):
        audioPlayer.changeVolume(int(volume))

    def searchSong(self):
        print(self.ids.search_box.text)

        YoutubeAPI.searchQuery = self.ids.search_box.text

        videoResultsData = YoutubeAPI.getSongs()

        self.ids.results.clear_widgets()
        self.l = GridLayout()
        self.l.cols = 1

        i = 0
        while i < len(videoResultsData) - 2:
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