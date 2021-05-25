import os

class PlaylistManager():
    def __init__(self):
        self.actualSongIndex = 0
        self.allPlaylists = []
        self.actualPlaylistFile = ""
        self.actualPlaylist = []
        self.isPlaying = False
        self.skipped = False


    def addPlaylist(self, playlistName):
        filepath = "./Playlists/" + str(playlistName) + ".txt"
        f = open(filepath, "w")

    def addToPlaylist(self, playlist, title, image, song):
        f = open("./Playlists/" + playlist + ".txt", "a", encoding = 'utf-8')
        line = title + ";:;" + image + ";:;" + song + "\n"
        f.write(line)
        f.close()

    def readPlaylist(self, playlistName):
        list = []
        f = open("./Playlists/" + playlistName + ".txt", "r", encoding = 'utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            list.append((line.split(";:;")[0], line.split(";:;")[1], line.split(";:;")[2]))
        return list

    def getPlaylists(self):
        files = []
        for file in os.listdir("./Playlists"):
            if str(file).__contains__(".txt"):
                files.append(file.split(".")[0])
        return files

    def getNext(self):
        self.actualSongIndex += 1
        self.indexFix()
        return self.actualPlaylist[self.actualSongIndex]

    def getPrevious(self):
        self.actualSongIndex -= 1
        self.indexFix()
        return self.actualPlaylist[self.actualSongIndex]

    def indexFix(self):
        if self.actualSongIndex >= len(self.actualPlaylist):
            self.actualSongIndex %= len(self.actualPlaylist)
        if self.actualSongIndex < 0:
            self.actualSongIndex = len(self.actualPlaylist) - 1


    def playPlaylist(self, playlistName, audioPlayer, libraryScreen):
        self.actualPlaylist = self.readPlaylist(playlistName)
        while self.actualSongIndex < len(self.actualPlaylist):
            print(self.actualPlaylist[self.actualSongIndex])
            audioPlayer.playSong("https://www.youtube.com/watch?v=" + self.actualPlaylist[self.actualSongIndex][2])
            libraryScreen.updateImage(self.actualPlaylist[self.actualSongIndex][1])
            while audioPlayer.isPlaying and not self.isPlaying:
                if audioPlayer.getTime() == audioPlayer.getLength():
                    audioPlayer.hasEnded = True
                if audioPlayer.hasEnded:
                    break
            self.actualSongIndex += 1
