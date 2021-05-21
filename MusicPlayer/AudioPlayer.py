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

    def playSong(self, songUrl):
        print("ey")
        self.isPlaying = True
        print("songURL-" + songUrl)
        print("actualSong-" + self.actualSong)
        if songUrl != self.actualSong:

            self.actualSong = songUrl
            print("songURL-" + songUrl)
            print("actualSong-" + self.actualSong)
            self.media.stop()
            self.video = pafy.new(songUrl)
            # getting best audio stream
            best = self.video.getbestaudio()
            self.media = vlc.MediaPlayer(best.url)
            self.media.play()
        else:
            print("tu problem")
        print(self.media.can_pause())

    def pauseSong(self):
        if self.isPlaying and self.media.can_pause():
            self.media.pause()
            self.isPlaying = False

    def changeVolume(self, value):
        self.media.audio_set_volume(value)