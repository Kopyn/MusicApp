import os

class PlaylistManager():
    def __init__(self):
        self.actualSongIndex = 0
        self.allPlaylists = []
        self.actualPlaylistFile = ""

    def addPlaylist(self, playlistName):
        filepath = "./Playlists/" + str(playlistName) + ".txt"
        print(filepath)
        f = open(filepath, "w")

    def addToPlaylist(self, playlist, song):
        pass

    def readPlaylist(self, playlistName):
        pass

    def getPlaylists(self):
        files = []
        for file in os.listdir("./Playlists"):
            if str(file).__contains__(".txt"):
                files.append(file.split(".")[0])
        return files

