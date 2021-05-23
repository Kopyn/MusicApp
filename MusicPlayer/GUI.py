from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.core.window import Window
import threading
import time
from PlaylistManager import *
import YoutubeAPI
from AudioPlayer import *
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


playlistManager = PlaylistManager()
audioPlayer = AudioPlayer()
isPlaying = False

actualSongTitle = ""

class VideoItem(BoxLayout):
    def __init__(self, imageSource, title, videoID):
        super(VideoItem, self).__init__()
        self.id = videoID
        self.orientation = 'horizontal'
        self.actualSongImage = imageSource
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
        MainLayout.actualSongImage = self.actualSongImage
        if MainLayout.firstSong:
            print("first song")
            time.sleep(1)
            audioPlayer.pauseSong()
            time.sleep(1)
            audioPlayer.playSong("https://www.youtube.com/watch?v=" + self.id)
            MainLayout.firstSong = False
        isPlaying = True


class MainLayout(Screen):
    actualSongImage = ""
    firstSong = True

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.rows = 1
        self.killThread = False
        playlistManager.addPlaylist("Test")
        self.t = threading.Thread(target = self.timeUpdate)
        self.t.start()
        self.actualSongImage = ""
        Window.size = (800, 500)
        self.ids.volume_control.bind(value = self.changeVolume)
        self.ids.playback_control.value = 1

    def timeUpdate(self):
        if not self.killThread:
            while MainLayout.firstSong:
                time.sleep(0.5)
                print("hey")
                if self.killThread:
                    break
        self.pauseSong()
        print("qwer")
        time.sleep(0.5)
        self.playSong()
        while True:
            if not self.killThread:
                time.sleep(1)
                if(MainLayout.actualSongImage != self.actualSongImage):
                    self.ids.now_playing.clear_widgets()
                    self.manager.get_screen('LibraryScreen').ids.now_playing.clear_widgets()
                    self.ids.now_playing.add_widget(AsyncImage(source=MainLayout.actualSongImage))
                    self.manager.get_screen('LibraryScreen').ids.now_playing.add_widget(AsyncImage(source=MainLayout.actualSongImage))
                if int(audioPlayer.getTime()) > 0:
                    self.updateProgress(audioPlayer.getTime())
                    self.manager.get_screen('LibraryScreen').ids.playback_control.value = audioPlayer.getTime()
                self.ids.now_playing.add_widget(AsyncImage(source=MainLayout.actualSongImage))
                self.manager.get_screen('LibraryScreen').ids.now_playing.add_widget(AsyncImage(source=MainLayout.actualSongImage))
            else:
                break
        print("end of loop main layout")

    def updateProgress(self, value):
        self.ids.playback_control.value = value

    def playSong(self):
        if self.killThread:
            print("thread not killed")
            print(self.killThread)
            self.ids.playback_control.max = audioPlayer.getLength()

        else:
            self.ids.playback_control.max = audioPlayer.getLength()
            print("hey")
        self.manager.get_screen('LibraryScreen').ids.playback_control.max = audioPlayer.getLength()
        self.ids.playback_control.max = audioPlayer.getLength()
        audioPlayer.playSong(audioPlayer.actualSong)
        if MainLayout.firstSong:
            audioPlayer.pauseSong()
            time.sleep(2)
            audioPlayer.playSong(audioPlayer.actualSong)
            MainLayout.firstSong = False

    def pauseSong(self):
        isPlaying = False
        if self.killThread:
            self.killThread = True
        else:
            print("yay")
        print("thread is killed")
        audioPlayer.pauseSong()

    def kill_thread(self):
        print("killing")
        self.killThread = True
        print(self.killThread)

    def changeVolume(self, instance, volume):
        audioPlayer.changeVolume(int(volume))

    def setTime(self, instance, time):
        audioPlayer.setTime(int(time))

    def getTime(self, instance):
        return audioPlayer.getTime()

    def searchSong(self):
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

class LibraryScreen(Screen):
    def __init__(self, **kwargs):
        super(LibraryScreen, self).__init__(**kwargs)
        self.rows = 1
        self.actualSongImage = ""
        Window.size = (800, 500)
        self.ids.volume_control.bind(value=self.changeVolume)
        self.ids.playback_control.value = 1
        self.getPlaylists()

    def getPlaylists(self):
        l = playlistManager.getPlaylists()
        for playlist in l:
            aLayout = AnchorLayout(anchor_x = 'left', anchor_y = 'top', padding = 5)
            aLayout.add_widget(Button(text = playlist, on_press = self.playPlaylist, size_hint = (.2, .2), size = (200, 200), spacing = 5))
            self.ids.playlists.add_widget(aLayout)

    def playPlaylist(self, instance):
        pass

    def playSong(self):
        self.manager.get_screen('MainLayout').playSong()

    def pauseSong(self):
        self.manager.get_screen('MainLayout').pauseSong()

    def changeVolume(self, instance, volume):
        audioPlayer.changeVolume(int(volume))

    def setTime(self, instance, time):
        audioPlayer.setTime(int(time))

    def getTime(self, instance):
        return audioPlayer.getTime()
        
class MusicApp(App):
    def build(self):
        sm = ScreenManager(transition = FadeTransition())
        self.mainLayout = MainLayout(name = 'MainLayout')
        sm.add_widget(self.mainLayout)
        sm.add_widget(LibraryScreen(name = 'LibraryScreen'))
        #sm.current = 'LibraryScreen'
        sm.current = 'MainLayout'
        return sm

    def stop(self, *largs):
        self.mainLayout.kill_thread()
        time.sleep(1)
        super(MusicApp, self).stop(*largs)

if __name__ == '__main__':
    p = MusicApp()
    p.run()