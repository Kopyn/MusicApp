import os

#class representing playlist manager
class PlaylistManager():
    def __init__(self):
        self.actualSongIndex = 0
        self.allPlaylists = []
        self.actualPlaylist = []

    #method to add new playlist
    def addPlaylist(self, playlistName):
        filepath = "./Playlists/" + str(playlistName) + ".txt"
        f = open(filepath, "w")

    #method to add new song to a playlist
    def addToPlaylist(self, playlist, title, image, song):
        f = open("./Playlists/" + playlist + ".txt", "a", encoding = 'utf-8')
        line = title + ";:;" + image + ";:;" + song + "\n"
        f.write(line)
        f.close()

    #method to read playlist items
    def readPlaylist(self, playlistName):
        list = []
        f = open("./Playlists/" + playlistName + ".txt", "r", encoding = 'utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            list.append((line.split(";:;")[0], line.split(";:;")[1], line.split(";:;")[2]))
        return list

    #method to return all existing playlists
    def getPlaylists(self):
        files = []
        for file in os.listdir("./Playlists"):
            if str(file).__contains__(".txt"):
                files.append(file.split(".")[0])
        return files

    #method to play next item from playlist
    def getNext(self):
        self.actualSongIndex += 1
        self.indexFix()
        return self.actualPlaylist[self.actualSongIndex]

    # method to play previous item from playlist
    def getPrevious(self):
        self.actualSongIndex -= 1
        self.indexFix()
        return self.actualPlaylist[self.actualSongIndex]

    #method to fix actual song index
    def indexFix(self):
        if self.actualSongIndex >= len(self.actualPlaylist):
            self.actualSongIndex %= len(self.actualPlaylist)
        if self.actualSongIndex < 0:
            self.actualSongIndex = len(self.actualPlaylist) - 1
