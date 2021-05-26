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
        ttl.add_widget(Label(bold = True, font_size = '22sp', text = title, text_size = (200, None)))
        #add all widgets
        self.add_widget(imag)
        self.add_widget(ttl)
        self.add_widget(toPlaylist)
        self.bubbleClicked = False

    #method to play a result song
    def playSong(self, instance):
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + self.id)
        MainLayout.actualSongImage = self.actualSongImage
        MainLayout.actualSongLength = audioPlayer.getLength()
        #change flag if it's first song
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
    actualSongLength = 0

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.rows = 1
        self.killThread = False
        #run second thread
        self.t = threading.Thread(target = self.timeUpdate)
        self.t.start()
        self.actualSongImage = ""
        #bind volume change slider
        self.ids.volume_control.bind(value = self.changeVolume)

    #method running in second thread, used to update song progress and actual song image
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
                self.ids.playback_control.max = audioPlayer.getLength()
                self.manager.get_screen('LibraryScreen').ids.playback_control.max = audioPlayer.getLength()
                self.ids.now_playing.add_widget(AsyncImage(source=MainLayout.actualSongImage))
                self.manager.get_screen('LibraryScreen').ids.now_playing.add_widget(AsyncImage(source=MainLayout.actualSongImage))
            else:
                break

    #method to update progress bar
    def updateProgress(self, value):
        self.ids.playback_control.value = value

    #method to play song
    def playSong(self):
        if not MainLayout.firstSong:
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

    #method to pause song
    def pauseSong(self):
        audioPlayer.pauseSong()

    #method to play item from playlist
    def pickFromPlaylist(self,image, songID, instance):
        MainLayout.actualSongImage = image
        audioPlayer.stopPlayer()
        MainLayout.firstSong = False
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + songID)

    #method to kill second thread and stop program work
    def kill_thread(self):
        audioPlayer.changeVolume(0)
        self.killThread = True
        print(self.killThread)

    #method to change audio volume
    def changeVolume(self, instance, volume):
        audioPlayer.changeVolume(int(volume))

    def getTime(self, instance):
        return audioPlayer.getTime()

    #method to search for song results
    def searchSong(self):
        #create Youtube API request
        YoutubeAPI.searchQuery = self.ids.search_box.text
        videoResultsData = YoutubeAPI.getSongs()
        #clear previous results
        self.ids.results.clear_widgets()
        self.l = GridLayout()
        self.l.cols = 1
        if len(videoResultsData) > 0:
            # add all results to layout
            i = 0
            while i < len(videoResultsData) - 2:
                self.l.add_widget(VideoItem(videoResultsData[i], videoResultsData[i + 1], videoResultsData[i + 2]))
                i += 3
            # view results
            self.ids.results.add_widget(self.l)

    #play next playlist item
    def getNext(self):
        if len(playlistManager.actualPlaylist) > 0:
            next = playlistManager.getNext()
            print(next)
            self.manager.get_screen('LibraryScreen').pickFromPlaylist(next[1], next[2])

    #play previous playlist item
    def getPrevious(self):
        if len(playlistManager.actualPlaylist) > 0:
            previous = playlistManager.getPrevious()
            self.manager.get_screen('LibraryScreen').pickFromPlaylist(previous[1], previous[2])

#class representing library panel
class LibraryScreen(Screen):

    def __init__(self, **kwargs):
        super(LibraryScreen, self).__init__(**kwargs)
        self.rows = 1
        self.actualSongImage = ""
        Window.size = (1000, 600)
        Window.minimum_width = 580
        Window.minimum_height = 400
        #binding volume change to slider
        self.ids.volume_control.bind(value=self.changeVolume)
        self.ids.playback_control.value = 1
        self.getPlaylists()

    #method to get all existing playlists
    def getPlaylists(self):
        l = playlistManager.getPlaylists()
        for playlist in l:
            self.ids.playlists.add_widget(Button(text = playlist, on_press = partial(self.playPlaylist, playlist), size_hint = (.2, .2), size = (200, 200)))

    #method to create new playlist
    def addPlaylist(self):
        playlistManager.addPlaylist(self.ids.playlist_name_box.text)
        self.ids.playlists.clear_widgets()
        self.getPlaylists()

    #play a playlist
    def playPlaylist(self, playlistName, instance):
        self.ids.playlist_items.clear_widgets()
        self.manager.get_screen('MainLayout').ids.playlist_items.clear_widgets()
        self.ids.playlist_name.text = playlistName
        self.manager.get_screen('MainLayout').ids.playlist_name.text = playlistName
        playlist = playlistManager.readPlaylist(playlistName)
        playlistManager.actualPlaylist = playlist
        #view all songs from playlist
        for song in playlist:
            self.ids.playlist_items.add_widget(Button(bold = True, background_color = (0, 0, 0, 0.3), text=song[0], size_hint=(1, .07), font_size = '9sp', text_size = (self.ids.playlist_items.width, None),
                                                      halign = 'center', on_press = partial(self.pickFromPlaylist, song[1], song[2])))
            self.manager.get_screen('MainLayout').ids.playlist_items.add_widget(
                Button(bold = True, background_color = (0, 0, 0, 0.3), text=song[0], size_hint=(1, .07), font_size = '9sp', text_size = (self.ids.playlist_items.width, None),
                       halign = 'center', on_press = partial(self.pickFromPlaylist, song[1], song[2])))
        #if playlist contains songs - play first song
        if len(playlist) > 0:
            self.pickFromPlaylist(playlist[0][1], playlist[0][2])

    #method to play song from library panel
    def playSong(self):
        self.manager.get_screen('MainLayout').playSong()

    #method to update actual song image
    def updateImage(self, image):
        self.actualSongImage = image
        self.manager.get_screen('MainLayout').actualSongImage = image

    #method to play song from playlist
    def pickFromPlaylist(self, image, songID, instance = None):
        MainLayout.actualSongImage = image
        audioPlayer.stopPlayer()
        MainLayout.firstSong = False
        audioPlayer.playSong("https://www.youtube.com/watch?v=" + songID)

    #method to pause song from library panel
    def pauseSong(self):
        self.manager.get_screen('MainLayout').pauseSong()

    #method to change audio volume
    def changeVolume(self, instance, volume):
        audioPlayer.changeVolume(int(volume))

    def getTime(self, instance):
        return audioPlayer.getTime()

    #method to play next song from playlist
    def getNext(self):
        if len(playlistManager.actualPlaylist) > 0:
            next = playlistManager.getNext()
            print(next)
            self.manager.get_screen('LibraryScreen').pickFromPlaylist(next[1], next[2])

    #method to play previous song from playlist
    def getPrevious(self):
        if len(playlistManager.actualPlaylist) > 0:
            previous = playlistManager.getPrevious()
            self.manager.get_screen('LibraryScreen').pickFromPlaylist(previous[1], previous[2])

#class representing main app
class MusicApp(App):

    def build(self):
        #adding screen manager
        sm = ScreenManager(transition = FadeTransition())
        self.icon = 'Images/playerIcon.png'
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
