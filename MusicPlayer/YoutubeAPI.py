import requests

API_ENDPOINT = "https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyAa6evu2V_0SjFCns0TWE_9-6frQvxw_JM&type=video" \
             "&maxResults=3&q={}"

searchQuery = ""

def getSongs():
    response = requests.get(API_ENDPOINT.format(searchQuery))
    if 200 <= response.status_code <= 299:
        returnedList = []
        items = response.json()["items"]
        i = 0
        while i < 3:
            #adding video image
            returnedList.append(items[i]["snippet"]["thumbnails"]["high"]["url"])
            #adding video title
            returnedList.append(items[i]["snippet"]["title"])
            print(items[i]["snippet"]["title"])
            #adding video id
            returnedList.append(items[i]["id"]["videoId"])
            i += 1
        print(len(returnedList))
        return returnedList
    else:
        return None