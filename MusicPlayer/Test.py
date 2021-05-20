import pafy
import os
directory = os.getcwd().__str__()
directory += '\VLC'
print(directory)
os.add_dll_directory(directory)
from urllib.parse import *
import vlc
YT_API_KEY = "AIzaSyAa6evu2V_0SjFCns0TWE_9-6frQvxw_JM"

# url of the video
url = "https://www.youtube.com/watch?v=HdWw9SksiwQ"

url1 = 'https://www.youtube.com/watch?v=RSRKFAmfqnI'

# creating pafy object of the video
video = pafy.new(url)

#print(video)

streams = video.audiostreams

# getting best stream
best = video.getbestaudio()

#print(best)

#print(urlparse('https://www.youtube.com/watch?v=HrgckFxmFgU'))

#print(urlparse(str(best.url)))

#print(str(best.url))

#print("---")


# creating vlc media player object
media = vlc.MediaPlayer(best.url)

#print(media)

# start playing video


def playSong():
    media.play()

def pauseSong():
    media.pause()

#while True:
#    pass