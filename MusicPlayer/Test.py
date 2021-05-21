import pafy
import os
directory = os.getcwd().__str__()
directory += '\VLC'
print(directory)
os.add_dll_directory(directory)
from urllib.parse import *
import vlc

query = ""


"""actualSong = "https://www.youtube.com/watch?v=HdWw9SksiwQ"

# url of the video
url = actualSong

url1 = 'https://www.youtube.com/watch?v=RSRKFAmfqnI'

# creating pafy object of the video
video = pafy.new(url)

# getting best audio stream
best = video.getbestaudio()

# creating vlc media player object
media = vlc.MediaPlayer(best.url)"""

#method to play a song
def playSong(url2):
    actualSong = url2

    # url of the video
    url = actualSong

    url1 = 'https://www.youtube.com/watch?v=RSRKFAmfqnI'

    # creating pafy object of the video
    video = pafy.new(url)

    # getting best audio stream
    best = video.getbestaudio()

    # creating vlc media player object
    media = vlc.MediaPlayer(best.url)
    media.play()

#method to pause a song
def pauseSong():
    media.pause()