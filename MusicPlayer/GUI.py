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

#wimg = Image(source='mylogo.png')

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
        Test.playSong()

class MainLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.rows = 1

    def playSong(self):
        Test.playSong()

    def pauseSong(self):
        Test.pauseSong()

    def viewSongs(self, listOfImages):
        pass

    def searchSong(self):
        print(self.ids.search_box.text)

        self.ids.results.clear_widgets()
        self.l = GridLayout()
        self.l.cols = 1
        if random.randint(1, 20) >= 2:
            self.l.add_widget(VideoItem('https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg',
                                        'https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg', 1))
            self.l.add_widget(VideoItem('https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg',
                                        'https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg', 1))
            self.l.add_widget(VideoItem('https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg',
                                        'https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg', 1))
        else:
            self.l.add_widget(AsyncImage(source='https://i.ytimg.com/vi/HdWw9SksiwQ/hqdefault.jpg'))
            self.l.add_widget(Label(text='hello'))
            self.l.add_widget(Button(text='OK'))
            self.l.add_widget(AsyncImage(source='https://i.ytimg.com/vi/WEQnzs8wl6E/hqdefault.jpg'))
            self.l.add_widget(Label(text='hello'))
            self.l.add_widget(Button(text='OK'))
            print("ayy")
        self.ids.results.add_widget(self.l)


class MusicApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    p = MusicApp()
    p.run()