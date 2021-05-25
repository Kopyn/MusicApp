from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from functools import *
import threading
import time
from PlaylistManager import *
import YoutubeAPI
from AudioPlayer import *
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

#create playlist manager object
playlistManager = PlaylistManager()
#create audio player object
audioPlayer = AudioPlayer()
isPlaying = False

#seting minimal window size
Window.size = (500, 400)
Window.minimum_width = 580
Window.minimum_height = 400

actualSongTitle = ""

#class representing search result
class VideoItem(BoxLayout):

    def __init__(self, imageSource, title, videoID):
        super(VideoItem, self).__init__()
        #store video data
        self.id = videoID
        self.title = title
        self.actualSongImage = imageSource
        self.orientation = 'horizontal'
        #place image and title on screen
        imag = AnchorLayout(anchor_x='center')
        ttl = AnchorLayout(anchor_x = 'right', anchor_y = 'bottom')
        toPlaylist = AnchorLayout(anchor_x='right', anchor_y='top', size_hint = (.1, .1))
        #add button to add song to playlist
        toPlaylist.add_widget(Button(text = '+', on_press = self.showBuuble))
        img = AsyncImage(source = imageSource)
        btn = Button(background_color = (0, 0, 0, 0))
        btn.bind(on_press = self.playSong)
        imag.add_widget(btn)
        imag.add_widget(img)
        ttl.add_widget(Label(text = title, text_size = (200, None)))
        #add all widgets
        self.add_widget(imag)
        self.add_widget(ttl)
        self.add_widget(toPlaylist)
        self.bubbleClicked = False

    #method to play a result song
    def playSong(self, instance):
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + self.id)
        MainLayout.actualSongImage = self.actualSongImage
        if MainLayout.firstSong:
            audioPlayer.pauseSong()
            audioPlayer.playSong("https://www.youtube.com/watch?v=" + self.id)
            MainLayout.firstSong = False

    #method to add song to playlist
    def addToPlaylist(self, playlist, title, image, song, bubble, instance):
        playlistManager.addToPlaylist(playlist, title, image, song)
        self.remove_widget(bubble)

    #method to show bubble with playlists
    def showBuuble(self, instance):
        #if bubble is already clicked
        if self.bubbleClicked:
            self.remove_widget(self.bubb)
            self.bubbleClicked = False
        #if bubble is not clicked
        else:
            self.bubb = Bubble(orientation='horizontal', arrow_pos='bottom_mid')

            l = playlistManager.getPlaylists()
            for playlist in l:
                self.bubb.add_widget(Button(text=playlist,
                                       on_press=partial(self.addToPlaylist, playlist, self.title, self.actualSongImage,
                                                        self.id, self.bubb),
                                       size_hint=(.2, .2), size=(200, 200)))
            self.add_widget(self.bubb)
            self.bubbleClicked = True

#class representing search panel
class MainLayout(Screen):
    actualSongImage = ""
    firstSong = True

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.rows = 1
        self.killThread = False
        self.t = threading.Thread(target = self.timeUpdate)
        self.t.start()
        self.actualSongImage = ""
        self.ids.volume_control.bind(value = self.changeVolume)
        self.ids.playback_control.value = 1

    def timeUpdate(self):
        if not self.killThread:
            while MainLayout.firstSong:
                time.sleep(0.5)
                if self.killThread:
                    break
        self.pauseSong()
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

    def updateProgress(self, value):
        self.ids.playback_control.value = value

    def playSong(self):
        if self.killThread:
            self.ids.playback_control.max = audioPlayer.getLength()
        else:
            self.ids.playback_control.max = audioPlayer.getLength()
        self.manager.get_screen('LibraryScreen').ids.playback_control.max = audioPlayer.getLength()
        self.ids.playback_control.max = audioPlayer.getLength()
        audioPlayer.playSong(audioPlayer.actualSong)
        if MainLayout.firstSong:
            audioPlayer.pauseSong()
            time.sleep(2)
            audioPlayer.playSong(audioPlayer.actualSong)
            MainLayout.firstSong = False

    def pauseSong(self):
        audioPlayer.pauseSong()

    def pickFromPlaylist(self,image, songID, instance):
        MainLayout.actualSongImage = image
        audioPlayer.stopPlayer()
        MainLayout.firstSong = False
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + songID)

    def kill_thread(self):
        audioPlayer.changeVolume(0)
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

    def getNext(self):
        next = playlistManager.getNext()
        print(next)
        self.manager.get_screen('LibraryScreen').pickFromPlaylist(next[1], next[2])

    def getPrevious(self):
        previous = playlistManager.getPrevious()
        self.manager.get_screen('LibraryScreen').pickFromPlaylist(previous[1], previous[2])

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
            self.ids.playlists.add_widget(Button(text = playlist, on_press = partial(self.playPlaylist, playlist), size_hint = (.2, .2), size = (200, 200)))

    def addPlaylist(self):
        playlistManager.addPlaylist(self.ids.playlist_name_box.text)
        self.ids.playlists.clear_widgets()
        self.getPlaylists()

    def playPlaylist(self, playlistName, instance):
        self.ids.playlist_items.clear_widgets()
        self.manager.get_screen('MainLayout').ids.playlist_items.clear_widgets()
        self.ids.playlist_name.text = playlistName
        self.manager.get_screen('MainLayout').ids.playlist_name.text = playlistName
        playlist = playlistManager.readPlaylist(playlistName)
        playlistManager.actualPlaylist = playlist
        for song in playlist:
            self.ids.playlist_items.add_widget(Button(background_color = (0, 0, 0, 0.3), text=song[0], size_hint=(1, .07), font_size = '9sp', text_size = (self.ids.playlist_items.width, None),
                                                      halign = 'center', on_press = partial(self.pickFromPlaylist, song[1], song[2])))
            self.manager.get_screen('MainLayout').ids.playlist_items.add_widget(
                Button(background_color = (0, 0, 0, 0.3), text=song[0], size_hint=(1, .07), font_size = '9sp', text_size = (self.ids.playlist_items.width, None),
                       halign = 'center', on_press = partial(self.pickFromPlaylist, song[1], song[2])))
        if len(playlist) > 0:
            self.pickFromPlaylist(playlist[0][1], playlist[0][2])

    def playSong(self):
        self.manager.get_screen('MainLayout').playSong()

    def updateImage(self, image):
        self.actualSongImage = image
        self.manager.get_screen('MainLayout').actualSongImage = image

    def pickFromPlaylist(self, image, songID, instance = None):
        MainLayout.actualSongImage = image
        audioPlayer.stopPlayer()
        MainLayout.firstSong = False
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + songID)

    def pauseSong(self):
        self.manager.get_screen('MainLayout').pauseSong()

    def changeVolume(self, instance, volume):
        audioPlayer.changeVolume(int(volume))

    def setTime(self, instance, time):
        audioPlayer.setTime(int(time))

    def getTime(self, instance):
        return audioPlayer.getTime()

    def getNext(self):
        next = playlistManager.getNext()
        print(next)
        self.manager.get_screen('LibraryScreen').pickFromPlaylist(next[1], next[2])

    def getPrevious(self):
        previous = playlistManager.getPrevious()
        self.manager.get_screen('LibraryScreen').pickFromPlaylist(previous[1], previous[2])
        
class MusicApp(App):

    def build(self):
        #adding screen manager
        sm = ScreenManager(transition = FadeTransition())

        self.mainLayout = MainLayout(name = 'MainLayout')
        sm.add_widget(self.mainLayout)
        sm.add_widget(LibraryScreen(name = 'LibraryScreen'))
        sm.current = 'MainLayout'
        return sm

    #method to stop the program work
    def stop(self, *largs):
        #stop thread loop
        self.mainLayout.kill_thread()
        time.sleep(0.3)
        super(MusicApp, self).stop(*largs)

if __name__ == '__main__':
    p = MusicApp()
    p.run()