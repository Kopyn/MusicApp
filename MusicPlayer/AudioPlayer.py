import pafy
import os

os.add_dll_directory("C:\Program Files\VideoLAN\VLC")
import vlc

#class representing audio player
class AudioPlayer():
    def __init__(self):
        #creating initial media player object
        self.actualSong = "https://www.youtube.com/watch?v=HdWw9SksiwQ"
        self.video = pafy.new(self.actualSong)
        best = self.video.getbestaudio()
        self.media = vlc.MediaPlayer(best.url)
        self.isPlaying = False
        self.hasEnded = False
        self.media.audio_set_volume(50)

    #method to play song
    def playSong(self, songUrl):
        self.isPlaying = True
        if songUrl != self.actualSong:
            self.actualSong = songUrl
            self.media.stop()
            #creating video object
            self.video = pafy.new(songUrl)
            # getting best audio stream
            best = self.video.getbestaudio()
            #creating media player object
            self.media = vlc.MediaPlayer(best.url)
            self.media.play()
        else:
            self.media.play()
            if self.isPlaying == False:
                self.media.play()

    #method to pause song
    def pauseSong(self):
        if self.isPlaying and self.media.can_pause():
            self.media.pause()
            self.isPlaying = False

    #method to change audio volume
    def changeVolume(self, value):
        self.media.audio_set_volume(value)

    #method to get actual time
    def getTime(self):
        return self.media.get_time()

    #method to get audio length
    def getLength(self):
        return self.media.get_length()

    #method to stop player
    def stopPlayer(self):
        self.media.stop()