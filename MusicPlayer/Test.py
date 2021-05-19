from pafy.backend_shared import BasePafy
import pafy
import youtube_dl
import os
directory = os.getcwd().__str__()
directory += '\VLC'
print(directory)
os.add_dll_directory(directory)
from urllib.parse import *
from urllib import *

YT_API_KEY = "AIzaSyAa6evu2V_0SjFCns0TWE_9-6frQvxw_JM"

import vlc

# url of the video
url = "https://www.youtube.com/watch?v=HdWw9SksiwQ"

url1 = 'https://www.youtube.com/watch?v=RSRKFAmfqnI'

# creating pafy object of the video
video = pafy.new(url)

print(video)

streams = video.audiostreams

# getting best stream
best = video.getbestaudio()

print(best)

print(urlparse('https://www.youtube.com/watch?v=HrgckFxmFgU'))

print(urlparse(str(best.url)))

print(str(best.url))

print("---")

#playsound(best.url)

# creating vlc media player object
media = vlc.MediaPlayer(best.url)

print(media)

# start playing video
media.play()

while True:
    pass

#playsound('http://b2.hostuje.info/_tmp/id-9f3652ac9d95a5593caa18d385a1f7a2-p-1.mp3')