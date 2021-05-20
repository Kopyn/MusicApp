import pafy
import os
directory = os.getcwd().__str__()
directory += '\VLC'
print(directory)
os.add_dll_directory(directory)
from urllib.parse import *
import vlc
YT_API_KEY = "AIzaSyAa6evu2V_0SjFCns0TWE_9-6frQvxw_JM"
API_ENDPOINT = "https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyAa6evu2V_0SjFCns0TWE_9-6frQvxw_JM&type=video" \
             "&maxResults=10&q={}"
query = ""

actualSong = "https://www.youtube.com/watch?v=HdWw9SksiwQ"

def formatEndpoint(q):
    return API_ENDPOINT.format(query)

# url of the video
url = actualSong

url1 = 'https://www.youtube.com/watch?v=RSRKFAmfqnI'

# creating pafy object of the video
video = pafy.new(url)

# getting best audio stream
best = video.getbestaudio()

# creating vlc media player object
media = vlc.MediaPlayer(best.url)

#method to play a song
def playSong():
    media.play()

#method to pause a song
def pauseSong():
    media.pause()