import pafy
import os

directory = os.getcwd().__str__()
#directory += '\VLC'
#print(directory)
#os.add_dll_directory(directory)
import vlc


class AudioPlayer():
    def __init__(self):
        self.actualSong = "https://www.youtube.com/watch?v=HdWw9SksiwQ"
        self.video = pafy.new(self.actualSong)
        best = self.video.getbestaudio()
        self.media = vlc.MediaPlayer(best.url)
        self.isPlaying = False
        self.media.audio_set_volume(50)

    def playSong(self, songUrl):
        self.isPlaying = True
        if songUrl != self.actualSong:
            self.actualSong = songUrl
            self.media.stop()
            self.video = pafy.new(songUrl)
            # getting best audio stream
            best = self.video.getbestaudio()
            self.media = vlc.MediaPlayer(best.url)
            self.media.play()
        else:
            self.media.play()
            if self.isPlaying == False:
                self.media.play()

    def pauseSong(self):
        if self.isPlaying and self.media.can_pause():
            self.media.pause()
            self.isPlaying = False

    def changeVolume(self, value):
        self.media.audio_set_volume(value)

    def setTime(self, time):
        self.media.set_time(time)

    def getTime(self):
        return self.media.get_time()

    def getLength(self):
        return self.media.get_length()