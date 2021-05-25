import requests

API_ENDPOINT = "https://www.googleapis.com/youtube/v3/search?part=snippet&key={}&type=video" \
             "&maxResults=3&q={}"

searchQuery = ""

#method to get list of 3 result songs
def getSongs():
    keys = []
    f = open("Keys.txt", "r", encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        if len(line) > 5:
            keys.append(line.split()[0])
    f.close()

    if len(keys) > 0:
        i = 0
        response = requests.get(API_ENDPOINT.format(keys[0], searchQuery))
        while i < len(keys) and response.status_code < 200 or response.status_code > 299:
            i += 1
            response = requests.get(API_ENDPOINT.format(keys[i], searchQuery))
        returnedList = []
        items = response.json()["items"]
        i = 0
        while i < 3:
            # adding video image
            returnedList.append(items[i]["snippet"]["thumbnails"]["high"]["url"])
            # adding video title
            returnedList.append(items[i]["snippet"]["title"])
            # adding video id
            returnedList.append(items[i]["id"]["videoId"])
            i += 1
        return returnedList
    else:
        return []
